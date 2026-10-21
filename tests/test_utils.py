import json
import sys
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from main import CompassRequestHandler, resolve_request_state
from matcher import normalize_profile_skills, rank_roles_for_profile
from signals import extract_taxonomy_entities, fetch_market_signals, load_snapshot_signals, validate_signals
from taxonomy import ROLES_CATALOG, SKILLS_CATALOG, SYNTHETIC_PROFILES
from utils import format_greeting, summarize


class TestUtilsAndCompass(unittest.TestCase):
    def test_format_greeting(self):
        self.assertEqual(format_greeting("Demo"), "Welcome to Demo!")

    def test_summarize(self):
        result = summarize([1, 2, 3])
        self.assertEqual(result["count"], 3)
        self.assertEqual(result["average"], 2.0)

    def test_summarize_empty(self):
        self.assertEqual(summarize([])["count"], 0)

    def test_taxonomy_constraint_no_invented_skills(self):
        skills, roles = extract_taxonomy_entities(
            "Paper on prompt engineering, SQL data analysis, and quantum teleportation magic."
        )
        self.assertIn("prompt_engineering", skills)
        self.assertIn("sql_data_analysis", skills)
        for s in skills:
            self.assertIn(s, SKILLS_CATALOG)
        for r in roles:
            self.assertIn(r, ROLES_CATALOG)

    def test_malformed_or_empty_signals_rejected(self):
        empty_res = validate_signals([])
        self.assertEqual(empty_res["status"], "insufficient_evidence")

        malformed = [
            {"title": "Missing URL and bad date", "published_date": "not-a-date"},
            {
                "title": "Valid date and URL but zero taxonomy skills",
                "published_date": "2026-10-18",
                "retrieved_date": "2026-10-20",
                "source_url": "https://arxiv.org/abs/0000.0000",
                "extracted_skills": ["non_existent_hallucinated_skill"],
            },
        ]
        mal_res = validate_signals(malformed, reference_date="2026-10-21")
        self.assertEqual(mal_res["status"], "insufficient_evidence")
        self.assertEqual(len(mal_res["valid_signals"]), 0)
        self.assertEqual(mal_res["rejected_count"], 2)

        # Ensure matcher halts and returns insufficient_evidence rather than confident ranking
        eval_res = rank_roles_for_profile(SYNTHETIC_PROFILES[0], malformed, reference_date="2026-10-21")
        self.assertEqual(eval_res["status"], "insufficient_evidence")
        self.assertEqual(eval_res["reason"], "signal_evidence_insufficient")
        self.assertEqual(eval_res["ranked_roles"], [])

    def test_stale_signals_rejected(self):
        stale = [
            {
                "id": "old-2019",
                "title": "Old Paper on Python and SQL Analytics",
                "published_date": "2019-01-10",
                "retrieved_date": "2026-10-20",
                "source_url": "https://arxiv.org/abs/1901.00001",
                "extracted_skills": ["python_scripting", "sql_data_analysis"],
            }
        ]
        res = validate_signals(stale, reference_date="2026-10-21", max_age_days=365)
        self.assertEqual(res["status"], "insufficient_evidence")
        self.assertEqual(res["rejected_count"], 1)

    def test_future_dates_and_substring_false_positives_rejected(self):
        future = [dict(title="Future-dated Python SQL paper", published_date="2027-03-01",
                       retrieved_date="2026-10-21", source_url="https://example.org/x",
                       extracted_skills=["python_scripting", "sql_data_analysis"])]
        self.assertEqual(validate_signals(future, reference_date="2026-10-21")["status"], "insufficient_evidence")
        # "leverage"/"powered"/"computer" must not map to RAG / carbon analytics
        skills, _ = extract_taxonomy_entities("We leverage AI-powered computer vision")
        self.assertNotIn("rag_knowledge_systems", skills)
        self.assertNotIn("carbon_footprint_analytics", skills)

    def test_snapshot_signals_are_attributed_research_records(self):
        snap = load_snapshot_signals()
        self.assertTrue(snap["is_fallback"])
        for s in snap["signals"]:
            self.assertTrue(s["source_url"].startswith("https://doi.org/") or "openalex.org" in s["source_url"])
            self.assertIn("OpenAlex", s["source_name"])

    def test_empty_and_sparse_profile_guardrail(self):
        snapshot = load_snapshot_signals()
        # Empty profile
        empty_eval = rank_roles_for_profile({"skills": []}, snapshot)
        self.assertEqual(empty_eval["status"], "insufficient_evidence")
        self.assertEqual(empty_eval["reason"], "sparse_profile_skills")
        self.assertEqual(empty_eval["ranked_roles"], [])

        # Sparse profile (only 1 skill)
        sparse_persona = next(p for p in SYNTHETIC_PROFILES if p["id"] == "sparse_edge_case")
        sparse_eval = rank_roles_for_profile(sparse_persona, snapshot)
        self.assertEqual(sparse_eval["status"], "insufficient_evidence")
        self.assertEqual(sparse_eval["reason"], "sparse_profile_skills")

    def test_ranking_order_missing_skills_and_scenario_shift(self):
        snapshot = load_snapshot_signals()
        priya = next(p for p in SYNTHETIC_PROFILES if p["id"] == "priya_esg")

        res_green = rank_roles_for_profile(priya, snapshot, scenario_id="sdg_green_push")
        self.assertEqual(res_green["status"], "ok")
        roles = res_green["ranked_roles"]
        self.assertEqual(len(roles), len(ROLES_CATALOG))

        # Verify descending score order
        scores = [r["total_score"] for r in roles]
        self.assertEqual(scores, sorted(scores, reverse=True))

        # Under sdg_green_push, Priya (ESG background) should match Sustainable AI Analyst or AI Governance at top
        top_role_ids = [roles[0]["role_id"], roles[1]["role_id"]]
        self.assertIn("sustainable_ai_analyst", top_role_ids)

        # Verify missing skills and pathway steps are populated and traceable
        top_role = roles[0]
        self.assertTrue(len(top_role["matched_required_skills"]) >= 1)
        self.assertTrue(len(top_role["missing_required_skills"]) >= 1)
        self.assertTrue(len(top_role["pathway"]["steps"]) >= 1)
        self.assertTrue(len(top_role["sdg_links"]) >= 1)
        self.assertTrue(len(res_green["scenario_comparison"]) >= 3)

    def test_http_endpoints_end_to_end(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), CompassRequestHandler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            # 1. Health endpoint
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/api/health", timeout=5) as resp:
                self.assertEqual(resp.status, 200)
                health = json.loads(resp.read().decode("utf-8"))
                self.assertEqual(health["status"], "ok")

            # 2. Normal profile HTML dashboard
            with urllib.request.urlopen(
                f"http://127.0.0.1:{port}/?profile_id=aisyah_ops&scenario_id=fast_agentic&signal_mode=fallback",
                timeout=5,
            ) as resp:
                self.assertEqual(resp.status, 200)
                page_html = resp.read().decode("utf-8")
                self.assertIn("AI Skills Compass", page_html)
                self.assertIn("DATED SNAPSHOT FALLBACK", page_html)
                self.assertIn("Rank #1", page_html)
                self.assertIn("UN SDG Alignment", page_html)

            # 3. Sparse profile HTML guardrail
            with urllib.request.urlopen(
                f"http://127.0.0.1:{port}/?profile_id=sparse_edge_case&signal_mode=fallback",
                timeout=5,
            ) as resp:
                self.assertEqual(resp.status, 200)
                sparse_html = resp.read().decode("utf-8")
                self.assertIn("Insufficient Evidence", sparse_html)
                self.assertIn("sparse_profile_skills", sparse_html)

            # 4. Interactive CV intake test
            with urllib.request.urlopen(
                f"http://127.0.0.1:{port}/?profile_id=custom&custom_name=Judge+Tester&cv_bio_text=Experienced+in+process+mapping+and+prompt+engineering&experience_level=mid",
                timeout=5,
            ) as resp:
                self.assertEqual(resp.status, 200)
                intake_html = resp.read().decode("utf-8")
                self.assertIn("Judge Tester", intake_html)
                self.assertIn("Interactive Custom Intake", intake_html)
                self.assertIn("Structured Prompting", intake_html)

            # 5. Employer / HR view & Rising/Declining radar test
            with urllib.request.urlopen(
                f"http://127.0.0.1:{port}/?view=employer_hr",
                timeout=5,
            ) as resp:
                self.assertEqual(resp.status, 200)
                hr_html = resp.read().decode("utf-8")
                self.assertIn("Employer / HR Workforce Skills-Gap Heatmap", hr_html)
                self.assertIn("Top Rising Competencies & Emerging Roles", hr_html)
                self.assertIn("Declining & Highly Automated Routine Tasks", hr_html)
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
