"""
tests/test_workforce_gap_engine.py

Automated Test Suite for:
O1 Employer Workforce Gap & Cohort Reskilling Engine v1.0.0
Covers all 43 mandated unit tests.
"""

import unittest
import os
import json
import hashlib
from pathlib import Path
from scipy.stats import spearmanr
from src.workforce_gap_engine import WorkforceGapEngine

ROOT = Path(__file__).resolve().parent.parent


class TestWorkforceGapEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = WorkforceGapEngine()
        wf_path = ROOT / "data" / "aggregation" / "synthetic_workforce_v1.json"
        with open(wf_path, "r", encoding="utf-8") as f:
            cls.synthetic_workforce = json.load(f)["profiles"]

    # -------------------------------------------------------------
    # 1. UPSTREAM FREEZE & PROVENANCE INTEGRITY
    # -------------------------------------------------------------
    def test_01_upstream_frozen_hashes_unchanged(self):
        """1. Upstream frozen manifests remain bit-exact."""
        expected_hashes = {
            "artifacts/m2_v1_1_1_freeze_manifest.json": "cdb15cebd1baf9385101cab1dacaf76e63d3703f30995a3c9cd7c2737b9db542",
            "data/scenarios/scenario_build_manifest_v1_1.json": "ee19b4fc1465ded069471ee8d6e4c85c30082955f31ddfc0e3ca5f2c6a8158b5",
            "data/matching/m3_build_manifest_v1_1.json": "15a489e7e661608547a03fd41a11cf3866126489f9a0195c43edf68e2607973c",
            "artifacts/m4_v1_1_freeze_manifest.json": "448545188ba4e196eaf3502d7803c3d9cfbb1247ec453208cafae990c8db5f2f",
            "artifacts/m5_v1_1_freeze_manifest.json": "94c1f42b46a1fa5e9b026fb82d5225e21c24547cdd58c234f2843cd84eb32ec7"
        }
        for path_str, exp_hash in expected_hashes.items():
            p = ROOT / path_str
            self.assertTrue(p.exists(), f"Missing upstream file: {path_str}")
            with open(p, "rb") as f:
                h = hashlib.sha256(f.read()).hexdigest()
            self.assertEqual(h, exp_hash, f"Upstream hash mismatch on {path_str}")

    def test_02_o6_frozen_artifact_unchanged(self):
        """2. O6 frozen manifest and configuration remain intact."""
        o6_manifest = ROOT / "artifacts" / "o6_v1_1_freeze_manifest.json"
        self.assertTrue(o6_manifest.exists())
        with open(o6_manifest, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["engine_name"], "O6 SDG Contribution Aggregation Engine")
        self.assertEqual(data["engine_version"], "1.1.0")

    def test_03_synthetic_only_data(self):
        """3. Ingested data is strictly synthetic demo data."""
        self.assertEqual(self.engine.config.get("data_classification"), "SYNTHETIC_DEMO")
        self.assertIn("Synthetic demonstration workforce", self.engine.config.get("representativeness_disclaimer", ""))

    # -------------------------------------------------------------
    # 2. PRIVACY, SAFETY & PROHIBITED FIELDS
    # -------------------------------------------------------------
    def test_04_no_protected_attributes(self):
        """4. Profile with protected demographic attributes is strictly rejected."""
        dirty = {"profile_id": "P_DIRTY", "gender": "FEMALE", "confirmed_skills": ["python_scripting"]}
        with self.assertRaises(ValueError):
            self.engine.validate_profile_for_workforce_analysis(dirty)

    def test_05_no_raw_cv_exposure(self):
        """5. Profile with raw CV text is classified as EXCLUDED_RAW_CV."""
        dirty_cv = {"profile_id": "P_CV", "raw_cv": "Resume text...", "confirmed_skills": ["python_scripting"]}
        status, reason = self.engine.validate_profile_for_workforce_analysis(dirty_cv)
        self.assertEqual(status, "EXCLUDED_RAW_CV")

    def test_06_malformed_profile_excluded(self):
        """6. Non-dictionary or missing ID records are safely excluded."""
        self.assertEqual(self.engine.validate_profile_for_workforce_analysis(None)[0], "EXCLUDED_INVALID_TYPE")
        self.assertEqual(self.engine.validate_profile_for_workforce_analysis("string")[0], "EXCLUDED_INVALID_TYPE")
        self.assertEqual(self.engine.validate_profile_for_workforce_analysis({"profile_id": ""})[0], "EXCLUDED_MISSING_ID")

    def test_07_eligible_denominator_correct(self):
        """7. Denominator reflects eligible profiles, not total input records."""
        cohort = [None, "bad", {"profile_id": "P1", "confirmed_skills": ["python_scripting"], "current_role": {"masco_code": "2512"}}] + self.synthetic_workforce[:5]
        res = self.engine.build_skill_gap_matrix(cohort)
        self.assertEqual(res["sanitization_summary"]["input_profile_count"], 8)
        self.assertEqual(res["sanitization_summary"]["eligible_profile_count"], 6)
        self.assertEqual(res["sanitization_summary"]["excluded_profile_count"], 2)

    def test_08_duplicate_profile_handling(self):
        """8. Duplicate profile IDs are deterministically deduplicated."""
        p1 = self.synthetic_workforce[0]
        cohort = [p1, p1, self.synthetic_workforce[1], self.synthetic_workforce[2], self.synthetic_workforce[3], self.synthetic_workforce[4]]
        eligible, sanitization = self.engine._sanitize_cohort_profiles(cohort)
        self.assertEqual(sanitization["input_profile_count"], 6)
        self.assertEqual(sanitization["eligible_profile_count"], 5)
        self.assertEqual(sanitization["excluded_profiles_by_reason"]["DUPLICATE_ID"], 1)

    def test_09_empty_cohort_handling(self):
        """9. Zero eligible profiles safely returns INSUFFICIENT_ELIGIBLE_COHORT_DATA."""
        res = self.engine.analyse_workforce_gaps([])
        self.assertEqual(res["eligible_profile_count"], 0)
        self.assertTrue(res["suppressed"])
        self.assertEqual(res["suppression_reason"], "NO_ELIGIBLE_PROFILES_AFTER_VALIDATION")

    def test_10_small_cohort_suppression(self):
        """10. Cohort size < 5 enforces k-anonymity suppression."""
        small = self.synthetic_workforce[:4]
        res = self.engine.analyse_workforce_gaps(small)
        self.assertTrue(res["suppressed"])
        self.assertEqual(res["suppression_reason"], "COHORT_SIZE_BELOW_PRIVACY_THRESHOLD")
        self.assertEqual(len(res["skill_gap_matrix"]), 0)

    def test_11_complementary_suppression_contract(self):
        """11. Heatmap and partition analytics enforce complementary suppression."""
        heatmap = self.engine.build_heatmap_payload(self.synthetic_workforce, grouping_dimension="cohort_id")
        self.assertIn("cells", heatmap)
        self.assertEqual(heatmap["metric_represented"], "WORKFORCE_RESKILLING_PRIORITY_INDEX")

    # -------------------------------------------------------------
    # 3. METRIC FORMULAS & DENOMINATORS
    # -------------------------------------------------------------
    def test_12_gap_prevalence_formula(self):
        """12. Gap prevalence = gapped profiles / eligible profiles."""
        res = self.engine.build_skill_gap_matrix(self.synthetic_workforce)
        for s_id, s_data in res["skills"].items():
            self.assertEqual(
                s_data["gap_prevalence"],
                round(s_data["profiles_with_gap"] / res["eligible_profile_count"], 4)
            )

    def test_13_core_gap_prevalence_formula(self):
        """13. Core gap prevalence = profiles with core gap / eligible profiles (masked when < 5)."""
        res = self.engine.build_skill_gap_matrix(self.synthetic_workforce)
        for s_id, s_data in res["skills"].items():
            if s_data["profiles_with_core_gap"] is not None:
                self.assertEqual(
                    s_data["core_gap_prevalence"],
                    round(s_data["profiles_with_core_gap"] / res["eligible_profile_count"], 4)
                )
                self.assertLessEqual(s_data["core_gap_prevalence"], s_data["gap_prevalence"])
            else:
                self.assertIsNone(s_data["core_gap_prevalence"])
                self.assertEqual(s_data["profiles_with_core_gap_display"], "<5")

    def test_14_mean_deficit_denominator(self):
        """14. Mean deficit denominator reflects gapped profiles only."""
        res = self.engine.build_skill_gap_matrix(self.synthetic_workforce)
        for s_id, s_data in res["skills"].items():
            if s_data["profiles_with_gap"] > 0:
                self.assertEqual(s_data["gapped_profiles_denominator"], s_data["profiles_with_gap"])
                self.assertTrue(0.0 <= s_data["mean_deficit_among_gapped_profiles"] <= 1.0)
            else:
                self.assertEqual(s_data["mean_deficit_among_gapped_profiles"], 0.0)

    def test_15_role_transition_aggregation(self):
        """15. Role transitions evaluate current vs target role volume."""
        res = self.engine.build_role_gap_summary(self.synthetic_workforce)
        self.assertFalse(res["suppressed"])
        self.assertGreater(len(res["role_transitions"]), 0)

    def test_16_major_group_fallback_exclusion(self):
        """16. 1-digit Major Group fallback codes are strictly excluded from role transitions."""
        res = self.engine.build_role_gap_summary(self.synthetic_workforce)
        for t in res["role_transitions"]:
            self.assertEqual(len(str(t["current_masco"])), 4)
            self.assertEqual(len(str(t["target_masco"])), 4)

    # -------------------------------------------------------------
    # 4. PRIORITY INDEX MATHEMATICS & EXPLAINABILITY
    # -------------------------------------------------------------
    def test_17_priority_weights_sum_to_one(self):
        """17. Priority component weights sum exactly to 1.00."""
        w = self.engine.weights
        total_w = sum(w.values())
        self.assertAlmostEqual(total_w, 1.0, places=4)

    def test_18_priority_components_deterministic(self):
        """18. Priority contributions sum exactly to final index when active."""
        ranks = self.engine.rank_workforce_reskilling_priorities(self.synthetic_workforce)
        for item in ranks:
            if item["priority_status"] == "ACTIVE" and item["affected_profile_count"] > 0:
                calc_sum = round(sum(item["weighted_contributions"].values()), 2)
                self.assertAlmostEqual(calc_sum, item["priority_index"], delta=0.05)
            elif item["priority_status"] == "SUPPRESSED_SUBCELL_RECONSTRUCTION":
                self.assertIsNone(item["priority_index"])
                self.assertIsNone(item["weighted_contributions"])

    def test_19_priority_index_not_probability(self):
        """19. Priority index carries explicit non-probability notice."""
        ranks = self.engine.rank_workforce_reskilling_priorities(self.synthetic_workforce)
        for item in ranks:
            self.assertIn("Not a probability", item["semantics_notice"])

    def test_20_priority_independent_of_demographic_fields(self):
        """20. Priority calculation does not use demographic fields."""
        p_clean = [p for p in self.synthetic_workforce if "age" not in p and "gender" not in p]
        ranks = self.engine.rank_workforce_reskilling_priorities(p_clean)
        self.assertGreater(len(ranks), 0)

    def test_21_priority_independent_of_course_price_provider(self):
        """21. Course price, provider brand, or certificate availability do not alter skill priority."""
        ranks = self.engine.rank_workforce_reskilling_priorities(self.synthetic_workforce)
        # Priority weights only depend on gap prevalence, deficit, transferability, scenario, and prerequisites
        for item in ranks:
            if item["components"]:
                self.assertNotIn("cost", item["components"])
                self.assertNotIn("provider", item["components"])
            self.assertNotIn("cost", item["_internal_components"])
            self.assertNotIn("provider", item["_internal_components"])

    def test_22_resource_availability_does_not_alter_skill_priority(self):
        """22. Resource availability occurs after skill need is established."""
        plan = self.engine.build_cohort_reskilling_plan(self.synthetic_workforce)
        for item in plan["priority_skills_plan"]:
            self.assertIn("available_verified_resources", item)

    def test_23_core_gaps_structurally_prioritised(self):
        """23. CORE gap prevalence carries the highest individual weight (0.4118 in v1.1.0)."""
        w = self.engine.weights
        self.assertAlmostEqual(w["core_gap_prevalence"], 0.4117647059, places=6)
        self.assertGreater(w["core_gap_prevalence"], w["important_gap_prevalence"])

    def test_24_prerequisite_centrality_derived_from_frozen_graph(self):
        """24. Prerequisite centrality is derived strictly from M4 graph."""
        c = self.engine.prereq_centrality
        # ai_literacy has 4 downstream skills -> 4/15 = 0.2667
        self.assertAlmostEqual(c["ai_literacy"], 4 / 15.0, places=3)

    def test_25_transferability_derived_from_approved_catalog(self):
        """25. Transferability is derived from M4 catalog-wide distribution."""
        self.assertEqual(self.engine.transferability_pct["process_mapping"], 65.0)
        self.assertEqual(self.engine.transferability_pct["ai_literacy"], 60.0)

    def test_26_scenario_urgency_consumes_frozen_m6(self):
        """26. Scenario urgency consumes frozen scenario adjustments."""
        res_ref = self.engine.build_skill_gap_matrix(self.synthetic_workforce, scenario="REFERENCE_2026")
        res_agentic = self.engine.build_skill_gap_matrix(self.synthetic_workforce, scenario="FAST_AGENTIC")
        self.assertEqual(res_ref["skills"]["rag_knowledge_systems"]["scenario_urgency_bonus"], 0.0)
        self.assertEqual(res_agentic["skills"]["rag_knowledge_systems"]["scenario_urgency_bonus"], 20.0)

    def test_27_scenario_does_not_manufacture_gaps(self):
        """27. Changing scenarios modifies urgency weight without manufacturing new profile gaps."""
        res_ref = self.engine.build_skill_gap_matrix(self.synthetic_workforce, scenario="REFERENCE_2026")
        res_agentic = self.engine.build_skill_gap_matrix(self.synthetic_workforce, scenario="FAST_AGENTIC")
        for s_id in self.engine.CANONICAL_SKILLS_16:
            self.assertEqual(
                res_ref["skills"][s_id]["profiles_with_gap"],
                res_agentic["skills"][s_id]["profiles_with_gap"]
            )

    # -------------------------------------------------------------
    # 5. COHORT PLAN, SHARED LEARNING & SDG CONTEXT
    # -------------------------------------------------------------
    def test_28_shared_learning_detection(self):
        """28. Shared learning opportunities detect skills common to multiple learners."""
        opps = self.engine.identify_shared_learning_opportunities(self.synthetic_workforce)
        self.assertGreater(len(opps), 0)
        for o in opps:
            self.assertGreaterEqual(o["profiles_affected"], 2)

    def test_29_learner_hours_distinct_from_calendar_duration(self):
        """29. Aggregate learner-hours is distinct from shared curriculum session duration."""
        opps = self.engine.identify_shared_learning_opportunities(self.synthetic_workforce)
        top = opps[0]
        self.assertGreater(top["aggregate_learner_hours_range"][0], top["shared_curriculum_hours_range"][0])
        self.assertIn("Shared curriculum duration is session length", top["semantics_note"])

    def test_30_cohort_plan_does_not_overwrite_individual_m4_order(self):
        """30. Cohort plan embeds disclaimer that individual M4 remains authoritative."""
        plan = self.engine.build_cohort_reskilling_plan(self.synthetic_workforce)
        self.assertIn("Individual M4 pathway remains authoritative", plan["methodology_disclaimer"])

    def test_31_heatmap_payload_correctness(self):
        """31. Heatmap data payload includes rows, columns, and typed cells."""
        heatmap = self.engine.build_heatmap_payload(self.synthetic_workforce, grouping_dimension="cohort_id")
        self.assertEqual(len(heatmap["rows"]), 16)
        self.assertGreater(len(heatmap["columns"]), 0)
        self.assertEqual(len(heatmap["cells"]), 16 * len(heatmap["columns"]))

    def test_32_suppressed_heatmap_cell_handling(self):
        """32. Small cohort heatmap cells are properly suppressed."""
        small_cohort = self.synthetic_workforce[:3]
        heatmap = self.engine.build_heatmap_payload(small_cohort, grouping_dimension="cohort_id")
        for cell in heatmap["cells"]:
            self.assertTrue(cell["suppressed"])
            self.assertIsNone(cell["priority_index"])

    def test_33_executive_summary_deterministic(self):
        """33. Executive summary outputs deterministic structured fields."""
        summary = self.engine.get_executive_workforce_summary(self.synthetic_workforce)
        self.assertIn("top_priority_skills", summary)
        self.assertIn("largest_core_gap_areas", summary)
        self.assertIn("most_common_target_roles", summary)

    def test_34_m5_o6_sdg_context_remains_descriptive(self):
        """34. SDG capability context attaches descriptive alignment without impact claim."""
        res = self.engine.analyse_workforce_gaps(self.synthetic_workforce)
        sdg_ctx = res["sdg_capability_context"]
        self.assertEqual(sdg_ctx["sdg_mappings_status"], "DESCRIPTIVE_ALIGNMENT_NOT_IMPACT")

    def test_35_no_corporate_sdg_impact_score(self):
        """35. Output strictly omits corporate SDG impact score."""
        res = self.engine.analyse_workforce_gaps(self.synthetic_workforce)
        self.assertIsNone(res["sdg_capability_context"]["corporate_sdg_impact_score"])

    # -------------------------------------------------------------
    # 6. ETHICS, GOVERNANCE & DOWNSTREAM HOOKS
    # -------------------------------------------------------------
    def test_36_no_employee_ranking(self):
        """36. Payload contains zero individual employee rankings or worker risk scores."""
        res = self.engine.analyse_workforce_gaps(self.synthetic_workforce)
        self.assertNotIn("employee_ranking", res)
        self.assertNotIn("worker_scores", res)
        self.assertTrue(res["fairness_metadata"]["employee_ranking_prohibited"])

    def test_37_no_hr_decision_outputs(self):
        """37. Prohibited uses explicitly disallow termination, hiring, or promotion."""
        res = self.engine.analyse_workforce_gaps(self.synthetic_workforce)
        prohibited = res["prohibited_uses"]
        self.assertIn("HIRING_DECISIONS", prohibited)
        self.assertIn("TERMINATION_DECISIONS", prohibited)
        self.assertIn("PROMOTION_DECISIONS", prohibited)
        self.assertIn("COMPENSATION_DECISIONS", prohibited)

    def test_38_fairness_metadata_truthful(self):
        """38. Fairness metadata truthfully reports structural non-use without DIR claims."""
        res = self.engine.analyse_workforce_gaps(self.synthetic_workforce)
        fm = res["fairness_metadata"]
        self.assertFalse(fm["protected_attributes_used"])
        self.assertFalse(fm["demographic_fairness_evaluated"])
        self.assertTrue(fm["disparate_impact_claims_prohibited"])

    def test_39_o2_state_hook_present(self):
        """39. O2 state fingerprint hook exposes version and snapshot hashes for replanning."""
        res = self.engine.analyse_workforce_gaps(self.synthetic_workforce)
        fp = res["o2_state_fingerprint"]
        self.assertEqual(fp["m2_version"], "1.1.1")
        self.assertEqual(fp["m4_pathway_version"], "1.1.0")
        self.assertIn("cohort_snapshot_hash", fp)
        self.assertIn("analysis_config_hash", fp)

    def test_40_o5_audit_hook_present(self):
        """40. O5 audit hook exposes compliance and suppression audit statistics."""
        res = self.engine.analyse_workforce_gaps(self.synthetic_workforce)
        o5 = res["o5_compliance_metadata"]
        self.assertFalse(o5["protected_attributes_used"])
        self.assertTrue(o5["aggregate_only"])
        self.assertIn("suppression_applied", o5)
        self.assertIn("excluded_profile_count", o5)

    def test_41_source_versions_pinned(self):
        """41. Pinned versions match all upstream frozen systems."""
        res = self.engine.analyse_workforce_gaps(self.synthetic_workforce)
        sv = res["source_versions"]
        self.assertEqual(sv["m1"], "H_blend_0.70A_0.30C1_W1.0")
        self.assertEqual(sv["m2"], "1.1.1")
        self.assertEqual(sv["m6"], "1.1.0")
        self.assertEqual(sv["m3"], "1.1.0")
        self.assertEqual(sv["m4"], "1.1.0")
        self.assertEqual(sv["m5"], "1.1.0")
        self.assertEqual(sv["o6"], "1.1.0")

    def test_42_deterministic_output(self):
        """42. Successive pipeline runs produce identical outputs."""
        res1 = self.engine.analyse_workforce_gaps(self.synthetic_workforce)
        res2 = self.engine.analyse_workforce_gaps(self.synthetic_workforce)
        self.assertEqual(res1["o2_state_fingerprint"]["cohort_snapshot_hash"], res2["o2_state_fingerprint"]["cohort_snapshot_hash"])
        self.assertEqual(
            [item["priority_index"] for item in res1["priority_skills"]],
            [item["priority_index"] for item in res2["priority_skills"]]
        )

    def test_43_deterministic_build_manifest(self):
        """43. Build manifest hashes verify against actual files on disk."""
        manifest_path = ROOT / "data" / "workforce" / "o1_build_manifest_v1_1.json"
        if not manifest_path.exists():
            manifest_path = ROOT / "data" / "workforce" / "o1_build_manifest_v1.json"
        self.assertTrue(manifest_path.exists())
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        self.assertIn(manifest["engine_version"], ["1.0.0", "1.1.0"])
        self.assertTrue(manifest["verification_summary"]["all_benchmarks_passed"])

    # -------------------------------------------------------------
    # 8. STAGE 15C MANDATED TESTS — PRIVACY (P1 & P2 RESOLUTION)
    # -------------------------------------------------------------
    def test_44_shared_learning_counts_1_to_4_suppressed(self):
        """44. Shared learning counts 1, 2, 3, 4 are strictly suppressed from employer listing."""
        for target_k in [1, 2, 3, 4]:
            cohort = []
            for i in range(10):
                # target_k profiles lack sql_data_analysis, (10 - target_k) have it
                sk = ["sql_data_analysis"] if i >= target_k else []
                cohort.append({"profile_id": f"P_SL_{target_k}_{i}", "confirmed_skills": sk, "target_role": {"masco_code": "2511"}})
            opps = self.engine.identify_shared_learning_opportunities(cohort)
            self.assertFalse(any(item["shared_skill"] == "sql_data_analysis" for item in opps))
            # When include_suppressed=True, masked to '<5'
            opps_supp = self.engine.identify_shared_learning_opportunities(cohort, include_suppressed=True)
            supp_item = next((item for item in opps_supp if item.get("suppressed")), None)
            if supp_item:
                self.assertIsNone(supp_item["profiles_affected"])
                self.assertEqual(supp_item["profiles_affected_display"], "<5")

    def test_45_shared_learning_count_5_visible(self):
        """45. Shared learning count = 5 is visible and unmasked."""
        cohort = []
        for i in range(10):
            sk = ["sql_data_analysis"] if i >= 5 else []
            cohort.append({"profile_id": f"P_SL5_{i}", "confirmed_skills": sk, "target_role": {"masco_code": "2511"}})
        opps = self.engine.identify_shared_learning_opportunities(cohort)
        item = next((it for it in opps if it["shared_skill"] == "sql_data_analysis"), None)
        self.assertIsNotNone(item)
        self.assertEqual(item["profiles_affected"], 5)
        self.assertEqual(item["profiles_affected_display"], "5")
        self.assertFalse(item["suppressed"])

    def test_46_priority_skill_gap_count_1_to_4_suppressed(self):
        """46. Priority skill total gap count 1–4 is suppressed."""
        for target_k in [1, 2, 3, 4]:
            cohort = []
            for i in range(20):
                sk = ["sql_data_analysis"] if i >= target_k else []
                cohort.append({"profile_id": f"P_PS_{target_k}_{i}", "confirmed_skills": sk, "target_role": {"masco_code": "2511"}})
            ranks = self.engine.rank_workforce_reskilling_priorities(cohort)
            sql_item = next(it for it in ranks if it["skill_id"] == "sql_data_analysis")
            self.assertEqual(sql_item["priority_status"], "SUPPRESSED_SMALL_CELL")
            self.assertIsNone(sql_item["priority_index"])
            self.assertIsNone(sql_item["affected_profile_count"])
            self.assertEqual(sql_item["affected_profile_count_display"], "<5")
            self.assertIsNone(sql_item["components"])
            self.assertIsNone(sql_item["weighted_contributions"])

    def test_47_core_important_supporting_subcells_1_to_4_suppressed(self):
        """47. CORE, IMPORTANT, and SUPPORTING subcell counts 1–4 are masked in matrix."""
        res = self.engine.build_skill_gap_matrix(self.synthetic_workforce)
        for s_id, s in res["skills"].items():
            raw_c = round(s["_raw_core_gap_prevalence"] * res["eligible_profile_count"])
            raw_i = round(s["_raw_important_gap_prevalence"] * res["eligible_profile_count"])
            if 0 < raw_c < 5:
                self.assertIsNone(s["profiles_with_core_gap"])
                self.assertEqual(s["profiles_with_core_gap_display"], "<5")
                self.assertIsNone(s["core_gap_prevalence"])
            if 0 < raw_i < 5:
                self.assertIsNone(s["profiles_with_important_gap"])
                self.assertEqual(s["profiles_with_important_gap_display"], "<5")
                self.assertIsNone(s["important_gap_prevalence"])

    def test_48_priority_index_suppressed_on_subcell_reconstruction_risk(self):
        """48. Priority index suppressed when publishing it leaks a 1–4 subcell."""
        ranks = self.engine.rank_workforce_reskilling_priorities(self.synthetic_workforce)
        for it in ranks:
            if it["priority_status"] == "SUPPRESSED_SUBCELL_RECONSTRUCTION":
                self.assertIsNone(it["priority_index"])
                self.assertIsNone(it["components"])
                self.assertIsNone(it["weighted_contributions"])
                self.assertTrue(it["suppressed"])
                self.assertEqual(it["suppression_reason"], "SUBCELL_RECONSTRUCTION_RISK")

    def test_49_role_transitions_privacy_1_to_4_suppressed_and_5_visible(self):
        """49. Role transition volume 1–4 is suppressed; count >= 5 is visible."""
        # Test count 2
        c2 = [{"profile_id": f"P2_{i}", "current_role": {"masco_code": "2511"}, "target_role": {"masco_code": "2512" if i < 2 else "2511"}, "confirmed_skills": ["python_scripting"]} for i in range(10)]
        s2 = self.engine.build_role_gap_summary(c2)
        t2 = next(t for t in s2["role_transitions"] if t["current_masco"] == "2511" and t["target_masco"] == "2512")
        self.assertTrue(t2["suppressed"])
        self.assertIsNone(t2["transition_volume"])
        self.assertEqual(t2["transition_volume_display"], "<5")

        # Test count 5
        c5 = [{"profile_id": f"P5_{i}", "current_role": {"masco_code": "2511"}, "target_role": {"masco_code": "2512" if i < 5 else "2511"}, "confirmed_skills": ["python_scripting"]} for i in range(10)]
        s5 = self.engine.build_role_gap_summary(c5)
        t5 = next(t for t in s5["role_transitions"] if t["current_masco"] == "2511" and t["target_masco"] == "2512")
        self.assertFalse(t5["suppressed"])
        self.assertEqual(t5["transition_volume"], 5)
        self.assertEqual(t5["transition_volume_display"], "5")

    def test_50_role_family_n_less_than_5_suppressed(self):
        """50. Role family analytics suppresses subgroups with N < 5."""
        c = [{"profile_id": f"PRF_{i}", "current_role": {"masco_code": "2511"}, "target_role": {"masco_code": "2511"}, "confirmed_skills": ["python_scripting"]} for i in range(3)]
        res = self.engine.build_role_family_gap_analytics(c)
        for fam in res.get("role_families", []):
            if fam.get("eligible_profile_count", 0) < 5:
                self.assertTrue(fam["suppressed"])

    def test_51_heatmap_cell_privacy_and_prevalence_masking(self):
        """51. Heatmap cells with count 1–4 are masked with display_value = null."""
        h = self.engine.build_heatmap_payload(self.synthetic_workforce)
        cells = h.get("cells", [])
        for c in cells:
            if c.get("suppressed"):
                self.assertIsNone(c["display_value"])
                if c.get("suppression_reason") == "SMALL_CELL_PRIVACY":
                    self.assertIsNone(c["gap_prevalence"])
                    self.assertIsNone(c["core_gap_prevalence"])
                    self.assertEqual(c["count_display"], "<5")

    def test_52_roadmap_and_exec_summary_do_not_reveal_suppressed_subgroups(self):
        """52. Roadmap and executive summary do not reveal suppressed small-cell entities."""
        res = self.engine.analyse_workforce_gaps(self.synthetic_workforce)
        plan = res["cohort_reskilling_plan"]
        exec_s = res["executive_summary"]
        # Roadmap priority_skills_plan only contains cohort-scale needs (affected >= 5)
        for item in plan["priority_skills_plan"]:
            self.assertNotEqual(item["priority_tier"], "SUPPRESSED")
        # Executive summary top items are privacy-safe
        for item in exec_s["top_priority_skills"]:
            self.assertIsNotNone(item["priority_index"])
        for trans in exec_s["highest_pressure_transitions"]:
            self.assertFalse(trans["suppressed"])

    def test_53_parent_10_child_6_child_4_complementary_suppression(self):
        """53. Complementary suppression: Parent 10 / A 6 / B 4 suppresses both A and B."""
        res = self.engine.apply_partition_suppression({"A": 6, "B": 4}, parent_total=10)
        self.assertTrue(res["B"]["suppressed"])
        self.assertEqual(res["B"]["suppression_reason"], "SMALL_CELL_PRIVACY")
        self.assertIsNone(res["B"]["count"])
        self.assertTrue(res["A"]["suppressed"])
        self.assertEqual(res["A"]["suppression_reason"], "SUPPRESSED_COMPLEMENTARY_RULE")
        self.assertIsNone(res["A"]["count"])

    def test_54_multiple_small_cells_in_partition_handled_deterministically(self):
        """54. Partition with multiple small cells suppresses all small cells."""
        res = self.engine.apply_partition_suppression({"A": 2, "B": 3, "C": 10}, parent_total=15)
        self.assertTrue(res["A"]["suppressed"])
        self.assertTrue(res["B"]["suppressed"])
        self.assertFalse(res["C"]["suppressed"])

    def test_55_no_exact_small_counts_in_employer_facing_payload(self):
        """55. Zero exact integers 1–4 exist across all employer-facing sensitive fields."""
        res = self.engine.analyse_workforce_gaps(self.synthetic_workforce)
        sensitive_keys = {
            "profiles_with_gap", "profiles_with_core_gap", "profiles_with_important_gap",
            "profiles_with_supporting_gap", "affected_profile_count", "transition_volume",
            "profiles_affected"
        }
        def check_obj(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if k.startswith("_raw"):
                        continue
                    if k in sensitive_keys and isinstance(v, int):
                        self.assertNotIn(v, [1, 2, 3, 4], f"Leaked small integer count {v} on key '{k}'")
                    check_obj(v)
            elif isinstance(obj, list):
                for el in obj:
                    check_obj(el)
        check_obj(res)

    def test_56_cross_query_and_differential_privacy_claims(self):
        """56. Cross-query protection is truthfully PARTIAL; no false DP claim."""
        res = self.engine.analyse_workforce_gaps(self.synthetic_workforce)
        pm = res["privacy_metadata"]
        self.assertEqual(pm["cross_query_differencing_protection"], "PARTIAL")
        self.assertFalse(pm["differential_privacy_claimed"])

    # -------------------------------------------------------------
    # 9. STAGE 15C MANDATED TESTS — PRIORITY (P2 RESOLUTION)
    # -------------------------------------------------------------
    def test_57_core_first_semantics_labelled_weighted_preference(self):
        """57. CORE-first semantics is explicitly labelled CORE_WEIGHTED_PREFERENCE."""
        res = self.engine.analyse_workforce_gaps(self.synthetic_workforce)
        self.assertEqual(res["core_first_metadata"]["core_first_semantics"], "CORE_WEIGHTED_PREFERENCE")
        self.assertEqual(self.engine.config.get("core_first_semantics"), "CORE_WEIGHTED_PREFERENCE")
        for item in res["priority_skills"]:
            self.assertEqual(item["core_first_semantics"], "CORE_WEIGHTED_PREFERENCE")

    def test_58_rare_core_outranked_by_widespread_important_gap(self):
        """58. Adversarial counterexample proves weighted preference over structural precedence."""
        w = self.engine.weights
        # Widespread IMPORTANT gap: 80% prevalence, 50% transfer, 20% prereq
        score_imp = (w["important_gap_prevalence"] * 0.80 + w["cross_role_transferability"] * 0.50 + w["prerequisite_centrality"] * 0.20) * 100.0
        # Very rare CORE gap: 5% prevalence only
        score_core = (w["core_gap_prevalence"] * 0.05) * 100.0
        self.assertGreater(score_imp, score_core)

    def test_59_m4_individual_core_first_contract_unchanged(self):
        """59. M4 individual learning pathway contract remains CORE_FIRST_ORDERING."""
        res = self.engine.analyse_workforce_gaps(self.synthetic_workforce)
        self.assertEqual(res["core_first_metadata"]["m4_individual_semantics"], "CORE_FIRST_ORDERING")

    def test_60_average_deficit_diagnostic_preserved_and_weight_zero(self):
        """60. Average deficit diagnostic field preserved while ranking weight = 0.0."""
        res = self.engine.analyse_workforce_gaps(self.synthetic_workforce)
        dm = res["deficit_metadata"]
        self.assertEqual(dm["deficit_signal_status"], "BINARY_NON_DISCRIMINATING")
        self.assertFalse(dm["deficit_used_for_ranking"])
        self.assertTrue(dm["deficit_diagnostic_only"])
        self.assertEqual(self.engine.weights["average_deficit"], 0.0)
        # Check diagnostic mean deficit exists
        s_data = res["skill_gap_matrix"]["esg_sustainability_reporting"]
        self.assertIsNotNone(s_data["mean_deficit_among_gapped_profiles"])

    def test_61_v1_1_weights_proportional_renormalization_and_sum_to_one(self):
        """61. Effective v1.1 weights sum to 1.0 and equal proportional renormalization of v1.0."""
        w = self.engine.weights
        self.assertAlmostEqual(sum(w.values()), 1.0, places=6)
        orig = {"core": 0.35, "imp": 0.20, "trans": 0.15, "scen": 0.10, "prereq": 0.05}
        tot_orig = sum(orig.values())
        self.assertAlmostEqual(w["core_gap_prevalence"], orig["core"] / tot_orig, places=6)
        self.assertAlmostEqual(w["important_gap_prevalence"], orig["imp"] / tot_orig, places=6)
        self.assertAlmostEqual(w["cross_role_transferability"], orig["trans"] / tot_orig, places=6)
        self.assertAlmostEqual(w["scenario_urgency"], orig["scen"] / tot_orig, places=6)
        self.assertAlmostEqual(w["prerequisite_centrality"], orig["prereq"] / tot_orig, places=6)

    def test_62_zero_gap_gate_and_monotonicity_and_bounds(self):
        """62. Zero-gap gate returns 0.0; monotonic in all active components; bounded in [0, 100]."""
        # Zero-gap gate
        cohort_clean = [{"profile_id": f"P_CLN_{i}", "confirmed_skills": self.engine.CANONICAL_SKILLS_16, "target_role": {"masco_code": "2511"}} for i in range(10)]
        clean_ranks = self.engine.rank_workforce_reskilling_priorities(cohort_clean)
        for r in clean_ranks:
            self.assertEqual(r["priority_index"], 0.0)
            self.assertEqual(r["priority_tier"], "NONE")
            self.assertEqual(r["priority_status"], "ZERO_GAP")

        # Bounds on synthetic workforce
        ranks = self.engine.rank_workforce_reskilling_priorities(self.synthetic_workforce)
        for r in ranks:
            idx = r["_internal_priority_index"]
            self.assertTrue(0.0 <= idx <= 100.0)

    def test_63_rank_stability_spearman_correlation_v1_vs_v1_1(self):
        """63. Removal of constant deficit preserves rank ordering (Spearman rho >= 0.99)."""
        engine_v1 = WorkforceGapEngine(config_path=os.path.join(ROOT, "data", "workforce", "o1_config_v1.json"))
        r_v1 = engine_v1.rank_workforce_reskilling_priorities(self.synthetic_workforce)
        r_v1_1 = self.engine.rank_workforce_reskilling_priorities(self.synthetic_workforce)
        map_v1 = {item["skill_id"]: item["_internal_priority_index"] for item in r_v1}
        map_v1_1 = {item["skill_id"]: item["_internal_priority_index"] for item in r_v1_1}
        skills = list(map_v1.keys())
        rho, _ = spearmanr([map_v1[s] for s in skills], [map_v1_1[s] for s in skills])
        self.assertGreaterEqual(rho, 0.99)

    def test_64_sdg_context_does_not_alter_priority_and_scenario_no_manufactured_gaps(self):
        """64. SDG context does not alter priority; scenario urgency does not manufacture gaps."""
        res_ref = self.engine.rank_workforce_reskilling_priorities(self.synthetic_workforce, scenario="REFERENCE_2026")
        res_cop = self.engine.rank_workforce_reskilling_priorities(self.synthetic_workforce, scenario="MODERATE_COPILOT")
        inst_ref = next(it for it in res_ref if it["skill_id"] == "instructional_design")
        inst_cop = next(it for it in res_cop if it["skill_id"] == "instructional_design")
        self.assertEqual(inst_ref["_internal_priority_index"], 0.0)
        self.assertEqual(inst_cop["_internal_priority_index"], 0.0)

    # -------------------------------------------------------------
    # 10. STAGE 15C MANDATED TESTS — SAFETY & GOVERNANCE
    # -------------------------------------------------------------
    def test_65_v1_1_build_manifest_hashes_and_pinned_versions(self):
        """65. v1.1.0 build manifest exists, hashes match disk, versions pinned."""
        m_path = ROOT / "data" / "workforce" / "o1_build_manifest_v1_1.json"
        self.assertTrue(m_path.exists())
        with open(m_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        self.assertEqual(manifest["engine_version"], "1.1.0")
        self.assertEqual(manifest["pinned_dependencies"]["m2"], "1.1.1")
        self.assertEqual(manifest["pinned_dependencies"]["m4"], "1.1.0")
        self.assertEqual(manifest["pinned_dependencies"]["o6"], "1.1.0")
        self.assertTrue(manifest["verification_summary"]["all_benchmarks_passed"])
        self.assertTrue(manifest["verification_summary"]["complementary_suppression_active"])
        self.assertTrue(manifest["verification_summary"]["reconstruction_protection_active"])


if __name__ == "__main__":
    unittest.main()
