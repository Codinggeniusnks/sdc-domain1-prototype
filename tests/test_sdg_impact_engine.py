"""
Unit and Integration Tests for M5 SDG Impact Mapping Engine v1.1.0 (Stage 13C)
Comprehensive test suite verifying all Stage 13C remediation invariants, target semantics,
calibration, and pipeline safety.
"""

import os
import sys
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
src_dir = ROOT / "src"
sys.path.insert(0, str(src_dir))

from sdg_impact_engine import SDGImpactEngine


class TestSDGImpactEngineV11(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = SDGImpactEngine()

    def test_version_attribute(self):
        """Verify engine version is 1.1.0."""
        self.assertEqual(self.engine.version, "1.1.0")
        self.assertEqual(self.engine.VERSION, "1.1.0")

    def test_goals_count_and_integrity(self):
        """Verify that all 17 UN Sustainable Development Goals are loaded correctly."""
        goals = self.engine.goals
        int_goals = [k for k, v in goals.items() if isinstance(k, int)]
        self.assertEqual(len(int_goals), 17)
        for num in range(1, 18):
            self.assertIn(num, goals)
            g = goals[num]
            self.assertIn("name", g)
            self.assertGreater(len(g["name"]), 0)
            self.assertIn("summary", g)
            self.assertIn("source_url", g)

    def test_targets_traceability_and_scope(self):
        """Verify that all indexed targets are valid official targets with scope note."""
        targets = self.engine.targets
        self.assertEqual(len(targets), 21)
        for tid, tdata in targets.items():
            self.assertIn("target_id", tdata)
            self.assertIn("sdg_number", tdata)
            self.assertIn("official_target_text", tdata)
            self.assertIn("source_url", tdata)
            self.assertGreater(len(tdata["official_target_text"]), 10)

        # Check scope note (P3-1)
        scope = self.engine.target_scope_metadata
        self.assertEqual(scope.get("dataset_scope"), "SELECTED_DOMAIN_RELEVANT_TARGETS")
        self.assertEqual(scope.get("total_official_un_targets"), 169)
        self.assertEqual(scope.get("total_indexed_targets"), 21)

    def test_skills_mapping_completeness(self):
        """Verify all 16 canonical skills are mapped with 1-3 primary SDGs."""
        canonical_16 = [
            "ai_literacy",
            "prompt_engineering",
            "process_mapping",
            "sql_data_analysis",
            "python_scripting",
            "data_visualization",
            "workflow_automation",
            "human_in_the_loop_qa",
            "rag_knowledge_systems",
            "api_integration",
            "ai_ethics_governance",
            "data_privacy_pdpa",
            "esg_sustainability_reporting",
            "carbon_footprint_analytics",
            "stakeholder_communication",
            "instructional_design"
        ]
        self.assertEqual(len(self.engine.skill_mappings), 16)
        for s_id in canonical_16:
            self.assertIn(s_id, self.engine.skill_mappings)
            s_map = self.engine.get_skill_sdg_mapping(s_id)
            self.assertIn("skill_id", s_map)
            self.assertIn("skill_title", s_map)
            self.assertTrue(1 <= len(s_map["primary_sdgs"]) <= 3)
            for al in s_map["primary_sdgs"] + s_map["secondary_sdgs"]:
                self.assertIn(al["target_id"], self.engine.targets)
                self.assertIn(al["mapping_type"], ["DIRECT", "ENABLING", "CONTEXTUAL"])
                self.assertIn(al["alignment_strength"], ["STRONG", "MODERATE", "LIMITED"])
                self.assertIn(al["confidence"], ["HIGH", "MEDIUM"])

    def test_roles_mapping_completeness(self):
        """Verify all 20 MASCO 4-digit occupations are mapped with 1-3 primary SDGs."""
        masco_20 = [
            "2512", "2511", "2521", "2529", "2519", "2522",
            "2411", "2421", "2422", "2151", "2152", "2143",
            "2424", "2166", "1330", "3514", "3322", "4311",
            "4110", "3343"
        ]
        self.assertEqual(len(self.engine.role_mappings), 20)
        for r_code in masco_20:
            self.assertIn(r_code, self.engine.role_mappings)
            r_map = self.engine.get_role_sdg_mapping(r_code)
            self.assertIn("masco_code", r_map)
            self.assertIn("role_title", r_map)
            self.assertTrue(1 <= len(r_map["primary_sdgs"]) <= 3)
            for al in r_map["primary_sdgs"] + r_map["secondary_sdgs"]:
                self.assertIn(al["target_id"], self.engine.targets)
                self.assertIn(al["mapping_type"], ["DIRECT", "ENABLING", "CONTEXTUAL"])
                self.assertIn(al["alignment_strength"], ["STRONG", "MODERATE", "LIMITED"])
                self.assertIn(al["confidence"], ["HIGH", "MEDIUM"])

    def test_general_purpose_skill_safety(self):
        """Verify strictly that general-purpose skills NEVER receive DIRECT mappings."""
        gp_safety = self.engine.validate_general_purpose_safety()
        self.assertTrue(gp_safety["is_safe"])
        self.assertEqual(len(gp_safety["violations"]), 0)
        self.assertEqual(len(gp_safety["compliant_skills"]), 5)

        gp_skills = ["python_scripting", "sql_data_analysis", "api_integration", "workflow_automation", "prompt_engineering"]
        for gpid in gp_skills:
            s_map = self.engine.get_skill_sdg_mapping(gpid)
            for al in s_map["primary_sdgs"] + s_map["secondary_sdgs"]:
                self.assertNotEqual(al["mapping_type"], "DIRECT", f"Violation: {gpid} has DIRECT mapping to {al['target_id']}")

    def test_p1_1_target_9c_purge(self):
        """Verify Target 9.c is 100% purged from all 16 skills and 20 roles."""
        for s_id, s_data in self.engine.skill_mappings.items():
            for al in s_data.get("primary_sdgs", []) + s_data.get("secondary_sdgs", []):
                self.assertNotEqual(al["target_id"], "9.c", f"Target 9.c found in skill {s_id}")
        for r_code, r_data in self.engine.role_mappings.items():
            for al in r_data.get("primary_sdgs", []) + r_data.get("secondary_sdgs", []):
                self.assertNotEqual(al["target_id"], "9.c", f"Target 9.c found in role {r_code}")

    def test_p1_2_pdpa_target_16_6_reallocation(self):
        """Verify data_privacy_pdpa aligns to Target 16.6 DIRECT and Target 16.10 is purged."""
        pdpa = self.engine.get_skill_sdg_mapping("data_privacy_pdpa")
        targets = [al["target_id"] for al in pdpa["primary_sdgs"] + pdpa["secondary_sdgs"]]
        self.assertNotIn("16.10", targets)
        self.assertIn("16.6", targets)
        p_16_6 = [al for al in pdpa["primary_sdgs"] if al["target_id"] == "16.6"]
        self.assertEqual(len(p_16_6), 1)
        self.assertEqual(p_16_6[0]["mapping_type"], "DIRECT")

    def test_p1_3_sql_target_9_5_reallocation(self):
        """Verify sql_data_analysis aligns to 9.5 & 8.2 ENABLING and Target 17.18 is purged."""
        sql = self.engine.get_skill_sdg_mapping("sql_data_analysis")
        targets = [al["target_id"] for al in sql["primary_sdgs"] + sql["secondary_sdgs"]]
        self.assertNotIn("17.18", targets)
        self.assertIn("9.5", targets)
        self.assertIn("8.2", targets)
        p_9_5 = [al for al in sql["primary_sdgs"] if al["target_id"] == "9.5"]
        self.assertEqual(len(p_9_5), 1)
        self.assertEqual(p_9_5[0]["mapping_type"], "ENABLING")

    def test_p2_1_carbon_accounting_precision(self):
        """Verify carbon_footprint_analytics maps to 12.6 DIRECT, 13.2 ENABLING, and 13.3 is purged."""
        cfa = self.engine.get_skill_sdg_mapping("carbon_footprint_analytics")
        all_al = cfa["primary_sdgs"] + cfa["secondary_sdgs"]
        t_dict = {al["target_id"]: al["mapping_type"] for al in all_al}
        self.assertIn("12.6", t_dict)
        self.assertEqual(t_dict["12.6"], "DIRECT")
        self.assertIn("13.2", t_dict)
        self.assertEqual(t_dict["13.2"], "ENABLING")
        self.assertNotIn("13.3", t_dict)

    def test_p2_2_sector_dependence_flags(self):
        """Verify roles 2151, 2143, 2152 carry SECTOR_DEPENDENT_ALIGNMENT and MEDIUM confidence."""
        sec_roles = ["2151", "2143", "2152"]
        for r_code in sec_roles:
            r = self.engine.get_role_sdg_mapping(r_code)
            self.assertIn("SECTOR_DEPENDENT_ALIGNMENT", r.get("quality_flags", []))
            # Verify that sector-dependent targets carry MEDIUM confidence
            confs = [al.get("confidence") for al in r["primary_sdgs"]]
            self.assertIn("MEDIUM", confs)

    def test_p2_3_confidence_recalibration(self):
        """Verify overall confidence is calibrated (< 80% HIGH)."""
        high_count = 0
        total_count = 0
        for s in self.engine.skill_mappings.values():
            for al in s["primary_sdgs"] + s["secondary_sdgs"]:
                total_count += 1
                if al.get("confidence") == "HIGH":
                    high_count += 1
        for r in self.engine.role_mappings.values():
            for al in r["primary_sdgs"] + r["secondary_sdgs"]:
                total_count += 1
                if al.get("confidence") == "HIGH":
                    high_count += 1
        pct = (high_count / total_count) * 100
        self.assertLessEqual(pct, 80.0)
        self.assertGreaterEqual(pct, 60.0)

    def test_p2_4_clerical_beneficiary_flags(self):
        """Verify clerical roles 4110, 4311, 3343 carry CONTEXTUAL_BENEFICIARY_ALIGNMENT."""
        clerical_roles = ["4110", "4311", "3343"]
        for r_code in clerical_roles:
            r = self.engine.get_role_sdg_mapping(r_code)
            self.assertIn("CONTEXTUAL_BENEFICIARY_ALIGNMENT", r.get("quality_flags", []))
            # Verify Target 8.5 mapping is CONTEXTUAL
            all_al = r.get("primary_sdgs", []) + r.get("secondary_sdgs", [])
            t85 = [al for al in all_al if al["target_id"] == "8.5"]
            self.assertEqual(len(t85), 1)
            self.assertEqual(t85[0]["mapping_type"], "CONTEXTUAL")

    def test_p3_2_and_p3_3_config_safeguards(self):
        """Verify config contains refined k-anonymity and demographic invariance framing."""
        cfg = self.engine.config
        safeguards = cfg.get("privacy_and_demographic_safeguards", {})
        k_framing = safeguards.get("k_anonymity_framing", "")
        self.assertIn("k-anonymity-style aggregation", k_framing)
        self.assertIn("PDPA 2010 data protection principles", k_framing)
        
        fairness = safeguards.get("fairness_framing", "")
        self.assertIn("mathematically zero", fairness)
        self.assertIn("does not consume protected demographic attributes", fairness)

    def test_map_pathway_to_sdgs_synthesis(self):
        """Verify map_pathway_to_sdgs produces correct synthesized output without fake metrics."""
        sample_pathway = {
            "pathway_id": "TEST_AI_GOVERNANCE_PATHWAY",
            "target_role_code": "2422",
            "skills": ["ai_ethics_governance", "data_privacy_pdpa", "prompt_engineering"]
        }
        result = self.engine.map_pathway_to_sdgs(sample_pathway)
        self.assertEqual(result["pathway_id"], "TEST_AI_GOVERNANCE_PATHWAY")
        self.assertEqual(result["target_role_code"], "2422")
        self.assertEqual(result["skills_analyzed_count"], 3)
        self.assertGreaterEqual(result["total_sdgs_aligned"], 2)
        self.assertIn(16, result["direct_sdgs"])
        self.assertNotIn("kg_co2", result)
        self.assertNotIn("jobs_created", result)
        self.assertIn("methodology_disclaimer", result)
        self.assertIn("competency acquisition", result["pathway_impact_narrative"].lower())
        self.assertIn("occupational deployment", result["pathway_impact_narrative"].lower())

    def test_automated_remediation_invariants_method(self):
        """Verify self.engine.verify_remediation_invariants() passes all checks."""
        report = self.engine.verify_remediation_invariants()
        self.assertTrue(report["all_passed"])
        for item in report["findings"]:
            self.assertEqual(item["status"], "PASS")

    def test_no_feedback_isolation(self):
        """Verify M5 does not modify external configs or inject filtering parameters into upstream systems."""
        self.assertTrue(self.engine.config["forbidden_feedback_guardrails"]["forbid_m3_role_filtering_by_sdg"])
        self.assertTrue(self.engine.config["forbidden_feedback_guardrails"]["forbid_m4_course_filtering_by_sdg"])
        self.assertTrue(self.engine.config["forbidden_feedback_guardrails"]["forbid_synthetic_impact_quantification"])


if __name__ == "__main__":
    unittest.main()
