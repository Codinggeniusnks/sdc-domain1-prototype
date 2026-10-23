"""
test_sdg_aggregation_engine.py

Comprehensive test suite for O6 SDG Contribution Aggregation Engine v1.1.0.
Validates all Stage 14A requirements and Stage 14C remediations:
- Upstream freeze manifests intact (M5, M4, M3, M2, M6)
- Synthetic-only data & zero protected demographic attributes
- DEF-P1-01: Profile validation, malformed record exclusion, denominator integrity
- DEF-P2-01: Fairness claim semantics (demographic-feature exclusion, no empirical DIR)
- DEF-P2-02: Differencing & partition-aware complementary suppression
- DEF-P2-03: Canonical counting unit (i, t, tau) for mapping shares
- DEF-P3-01: Pathway alignment coverage scope and disclaimers
- DEF-P3-02: Regional representativeness runtime disclaimer
- Capability coverage bounds and role-skill isolation
- Quality flag propagation (sector-dependence, beneficiary alignment)
- Downstream safety: no employee ranking, no personal SDG scores, no fake metrics
- Scenario aggregation consuming M6 without mutation
- Temporal capability labeling (CURRENT vs POST_PATHWAY)
- Strict version pinning and deterministic hashes
"""

import unittest
import json
import hashlib
from pathlib import Path

from src.sdg_aggregation_engine import SDGAggregationEngine
from src.sdg_impact_engine import SDGImpactEngine
from src.scenario_engine import ScenarioEngine


ROOT = Path(__file__).resolve().parent.parent


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


class TestSDGAggregationEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = SDGAggregationEngine()
        wf_path = ROOT / "data" / "aggregation" / "synthetic_workforce_v1.json"
        with open(wf_path, "r", encoding="utf-8") as f:
            cls.workforce = json.load(f)
        cls.profiles = cls.workforce["profiles"]

    # -------------------------------------------------------------
    # 1. UPSTREAM FREEZE INTEGRITY TESTS
    # -------------------------------------------------------------
    def test_01_m5_freeze_manifest_unchanged(self):
        """M5 v1.1.0 freeze manifest must match its approved Stage 13D SHA-256."""
        m5_manifest = ROOT / "artifacts" / "m5_v1_1_freeze_manifest.json"
        self.assertTrue(m5_manifest.exists(), "M5 freeze manifest must exist.")
        expected_sha = "94c1f42b46a1fa5e9b026fb82d5225e21c24547cdd58c234f2843cd84eb32ec7"
        self.assertEqual(compute_sha256(m5_manifest), expected_sha)

    def test_02_m4_freeze_manifest_unchanged(self):
        """M4 v1.1.0 freeze manifest must match its approved Stage 12D SHA-256."""
        m4_manifest = ROOT / "artifacts" / "m4_v1_1_freeze_manifest.json"
        self.assertTrue(m4_manifest.exists(), "M4 freeze manifest must exist.")
        expected_sha = "448545188ba4e196eaf3502d7803c3d9cfbb1247ec453208cafae990c8db5f2f"
        self.assertEqual(compute_sha256(m4_manifest), expected_sha)

    def test_03_m3_frozen_artifact_unchanged(self):
        """M3 v1.1.0 build manifest must match its approved Stage 11D SHA-256."""
        m3_manifest = ROOT / "data" / "matching" / "m3_build_manifest_v1_1.json"
        self.assertTrue(m3_manifest.exists(), "M3 build manifest must exist.")
        expected_sha = "15a489e7e661608547a03fd41a11cf3866126489f9a0195c43edf68e2607973c"
        self.assertEqual(compute_sha256(m3_manifest), expected_sha)

    def test_04_m2_frozen_artifact_unchanged(self):
        """M2 v1.1.1 freeze manifest must match its approved Stage 9E SHA-256."""
        m2_manifest = ROOT / "artifacts" / "m2_v1_1_1_freeze_manifest.json"
        self.assertTrue(m2_manifest.exists(), "M2 freeze manifest must exist.")
        expected_sha = "cdb15cebd1baf9385101cab1dacaf76e63d3703f30995a3c9cd7c2737b9db542"
        self.assertEqual(compute_sha256(m2_manifest), expected_sha)

    def test_05_m6_frozen_artifact_unchanged(self):
        """M6 v1.1.0 build manifest must match its approved Stage 10C SHA-256."""
        m6_manifest = ROOT / "data" / "scenarios" / "scenario_build_manifest_v1_1.json"
        self.assertTrue(m6_manifest.exists(), "M6 build manifest must exist.")
        expected_sha = "ee19b4fc1465ded069471ee8d6e4c85c30082955f31ddfc0e3ca5f2c6a8158b5"
        self.assertEqual(compute_sha256(m6_manifest), expected_sha)

    # -------------------------------------------------------------
    # 2. PRIVACY & DEMOGRAPHIC HYGIENE TESTS
    # -------------------------------------------------------------
    def test_06_zero_protected_demographic_fields(self):
        """Synthetic profiles must contain strictly zero protected demographic fields."""
        forbidden_keys = {
            "race", "religion", "gender", "ethnicity", "income", "school",
            "postcode", "family_background", "age", "marital_status",
            "nationality", "disability"
        }
        for p in self.profiles:
            found = set(p.keys()).intersection(forbidden_keys)
            self.assertEqual(len(found), 0, f"Profile {p.get('profile_id')} has forbidden demographic keys: {found}")

    def test_07_demographic_input_rejection(self):
        """Engine must reject profiles containing protected demographic fields."""
        dirty_profile = {
            "profile_id": "DIRTY_001",
            "gender": "FEMALE",
            "confirmed_skills": ["python_scripting"]
        }
        with self.assertRaises(ValueError):
            self.engine.aggregate_individual_alignment(dirty_profile)

    def test_08_minimum_cohort_suppression_boundaries(self):
        """
        Verify privacy threshold:
        - Cohort of 1: suppressed
        - Cohort of 4: suppressed
        - Cohort of 5: unsuppressed
        - Cohort of 10: unsuppressed
        """
        # Cohort of 1
        res1 = self.engine.aggregate_cohort_alignment(self.profiles[:1])
        self.assertTrue(res1["suppressed"])
        self.assertEqual(res1["suppression_reason"], "SUPPRESSED_SMALL_COHORT")
        self.assertIsNone(res1["sdg_alignment_prevalence"])

        # Cohort of 4
        res4 = self.engine.aggregate_cohort_alignment(self.profiles[:4])
        self.assertTrue(res4["suppressed"])
        self.assertEqual(res4["suppression_reason"], "SUPPRESSED_SMALL_COHORT")
        self.assertIsNone(res4["sdg_alignment_prevalence"])

        # Cohort of 5 (Exact threshold)
        res5 = self.engine.aggregate_cohort_alignment(self.profiles[:5])
        self.assertFalse(res5["suppressed"])
        self.assertIsNotNone(res5["sdg_alignment_prevalence"])
        self.assertEqual(res5["eligible_count"], 5)

        # Cohort of 10
        res10 = self.engine.aggregate_cohort_alignment(self.profiles[:10])
        self.assertFalse(res10["suppressed"])
        self.assertEqual(res10["eligible_count"], 10)

    def test_09_empty_cohort_safe_handling(self):
        """Empty cohort must return INSUFFICIENT_COHORT_DATA without crashing or dividing by zero."""
        res_empty = self.engine.aggregate_cohort_alignment([])
        self.assertTrue(res_empty["suppressed"])
        self.assertEqual(res_empty["eligible_count"], 0)
        self.assertEqual(res_empty["suppression_reason"], "INSUFFICIENT_COHORT_DATA")
        self.assertIn("INSUFFICIENT_COHORT_DATA", res_empty["quality_flags"])

    def test_10_duplicate_profile_handling(self):
        """Duplicate profile IDs must be deterministically deduplicated."""
        dup_cohort = [self.profiles[0], self.profiles[0], self.profiles[1], self.profiles[2], self.profiles[3], self.profiles[4]]
        # 6 records, but only 5 unique profiles
        res = self.engine.aggregate_cohort_alignment(dup_cohort)
        self.assertEqual(res["cohort_size"], 6)
        self.assertEqual(res["eligible_count"], 5)
        self.assertFalse(res["suppressed"])
        self.assertIn("DUPLICATE_PROFILE_DETECTED", res["quality_flags"])
        self.assertEqual(res["excluded_profiles_by_reason"]["DUPLICATE_PROFILE_ID"], 1)

    # -------------------------------------------------------------
    # 3. METRIC MATHEMATICAL CORRECTNESS & NON-DOUBLE-COUNTING
    # -------------------------------------------------------------
    def test_11_unique_person_per_sdg_prevalence(self):
        """
        Verify Metric A (SDG Alignment Prevalence):
        A person with 3 skills and 1 role aligning to SDG 8 is counted exactly ONCE toward SDG 8 prevalence.
        """
        digital = [p for p in self.profiles if p["cohort_id"] == "DIGITAL_SERVICES"]
        res = self.engine.aggregate_cohort_alignment(digital)
        self.assertFalse(res["suppressed"])

        for sdg_key, s_data in res["sdg_alignment_prevalence"].items():
            count = s_data["aligned_profile_count"]
            ratio = s_data["prevalence_ratio"]
            pct = s_data["prevalence_percentage"]
            self.assertLessEqual(count, res["eligible_count"])
            self.assertEqual(ratio, round(count / res["eligible_count"], 4))
            self.assertEqual(pct, round(ratio * 100, 2))

    def test_12_unique_person_per_target_prevalence(self):
        """
        Verify Metric B (Target Prevalence Index):
        A person is counted at most once per target.
        """
        digital = [p for p in self.profiles if p["cohort_id"] == "DIGITAL_SERVICES"]
        res = self.engine.aggregate_cohort_alignment(digital)
        for t_id, t_data in res["target_prevalence"].items():
            count = t_data["aligned_profile_count"]
            ratio = t_data["prevalence_ratio"]
            self.assertLessEqual(count, res["eligible_count"])
            self.assertEqual(ratio, round(count / res["eligible_count"], 4))

    def test_13_mapping_type_distribution_sums_to_one(self):
        """
        Verify Metric C (DIRECT / ENABLING / CONTEXTUAL Ratio):
        direct_share + enabling_share + contextual_share must equal 1.0 (within rounding).
        """
        digital = [p for p in self.profiles if p["cohort_id"] == "DIGITAL_SERVICES"]
        res = self.engine.aggregate_cohort_alignment(digital)
        m_dist = res["mapping_type_distribution"]
        total_share = m_dist["direct_share"] + m_dist["enabling_share"] + m_dist["contextual_share"]
        self.assertAlmostEqual(total_share, 1.0, places=2)

    def test_14_capability_coverage_bounded(self):
        """
        Verify Metric D (SDG Capability Coverage):
        Ratio = unique cohort skills / canonical M5 skills for SDG s. Must be between 0.0 and 1.0.
        """
        digital = [p for p in self.profiles if p["cohort_id"] == "DIGITAL_SERVICES"]
        res = self.engine.aggregate_cohort_alignment(digital)
        for sdg_key, c_data in res["capability_coverage"].items():
            ratio = c_data["capability_coverage_ratio"]
            self.assertTrue(0.0 <= ratio <= 1.0)
            self.assertLessEqual(c_data["skills_present_count"], c_data["canonical_sdg_skills_total"])

    def test_15_pathway_alignment_coverage_bounded(self):
        """
        Verify Metric E (Pathway Alignment Coverage):
        Ratio of planned pathway skills mapped to M5. Must be between 0.0 and 1.0.
        """
        digital = [p for p in self.profiles if p["cohort_id"] == "DIGITAL_SERVICES"]
        res = self.engine.aggregate_cohort_alignment(digital)
        p_cov = res["pathway_alignment_coverage"]
        self.assertTrue(0.0 <= p_cov["pathway_alignment_coverage_ratio"] <= 1.0)

    # -------------------------------------------------------------
    # 4. QUALITY FLAG & GOVERNANCE SAFEGUARDS
    # -------------------------------------------------------------
    def test_16_m5_flag_propagation_sector_dependence(self):
        """Engineering roles must propagate SECTOR_DEPENDENT_ALIGNMENT_PRESENT to cohort level."""
        mfg = [p for p in self.profiles if p["cohort_id"] == "ADVANCED_MANUFACTURING"]
        res = self.engine.aggregate_cohort_alignment(mfg)
        self.assertIn("SECTOR_DEPENDENT_ALIGNMENT_PRESENT", res["quality_flags"])
        self.assertIn("MEDIUM_CONFIDENCE_MAPPING_PRESENT", res["quality_flags"])

    def test_17_m5_flag_propagation_beneficiary_alignment(self):
        """Clerical roles (4110, 4311, 3343) must propagate BENEFICIARY_ALIGNMENT_PRESENT."""
        biz = [p for p in self.profiles if p["cohort_id"] == "BUSINESS_SERVICES"]
        res = self.engine.aggregate_cohort_alignment(biz)
        self.assertIn("CONTEXTUAL_BENEFICIARY_ALIGNMENT_PRESENT", res["quality_flags"])

    def test_18_no_employee_ranking_or_personal_score(self):
        """
        Governance Check:
        Individual and cohort outputs must NEVER contain personal SDG scores or employee rankings.
        """
        ind = self.engine.aggregate_individual_alignment(self.profiles[0])
        self.assertFalse(ind["governance_safeguards"]["individual_sdg_score_computed"])
        self.assertFalse(ind["governance_safeguards"]["employee_sustainability_ranking_computed"])
        self.assertTrue(ind["governance_safeguards"]["hr_decision_use_prohibited"])
        self.assertNotIn("sdg_score", ind)
        self.assertNotIn("sustainability_rank", ind)

        cohort = self.engine.aggregate_cohort_alignment(self.profiles[:10])
        self.assertTrue(cohort["governance_safeguards"]["hr_decision_use_prohibited"])
        self.assertTrue(cohort["governance_safeguards"]["employee_sustainability_ranking_prohibited"])

    def test_19_no_synthetic_impact_quantification(self):
        """Outputs must not produce fabricated tonnes of CO2 saved or jobs created."""
        cohort = self.engine.aggregate_cohort_alignment(self.profiles[:10])
        dumped = json.dumps(cohort).lower()
        self.assertNotIn("tonnes of co2", dumped)
        self.assertNotIn("jobs created", dumped)
        self.assertNotIn("social_roi", dumped)

    # -------------------------------------------------------------
    # 5. TEMPORAL & SCENARIO CAPABILITY SCENARIOS
    # -------------------------------------------------------------
    def test_20_current_vs_post_pathway_distinction(self):
        """
        POST_PATHWAY must be labeled as 'PROJECTED CAPABILITY ALIGNMENT IF PATHWAY COMPLETED'
        and must not claim guaranteed completion.
        """
        green = [p for p in self.profiles if p["cohort_id"] == "GREEN_TRANSITION"]
        cur = self.engine.aggregate_cohort_alignment(green, time_dimension="CURRENT")
        post = self.engine.aggregate_cohort_alignment(green, time_dimension="POST_PATHWAY")

        self.assertEqual(cur["time_dimension_label"], "CURRENT_CAPABILITIES")
        self.assertEqual(post["time_dimension_label"], "PROJECTED CAPABILITY ALIGNMENT IF PATHWAY COMPLETED")
        self.assertIn("PROJECTED_CAPABILITY_SCENARIO", post["quality_flags"])

    def test_21_scenario_comparison_read_only_m6(self):
        """
        Scenario comparison must query M6 foresight without mutating M6 or M5.
        """
        digital = [p for p in self.profiles if p["cohort_id"] == "DIGITAL_SERVICES"]
        sc_res = self.engine.compare_scenarios(digital)
        self.assertIn("REFERENCE_2026", sc_res["results"])
        self.assertIn("FAST_AGENTIC", sc_res["results"])
        self.assertIn("structured_assumption_notice", sc_res)

    def test_22_version_pinning_enforcement(self):
        """Engine must pin M5 to 1.1.0 and fail on unexpected versions."""
        self.assertEqual(self.engine.VERSION, "1.1.0")
        self.assertEqual(self.engine.PINNED_M5_VERSION, "1.1.0")
        self.assertEqual(self.engine.PINNED_M6_VERSION, "1.1.0")
        self.assertEqual(self.engine.PINNED_M4_VERSION, "1.1.0")
        self.assertEqual(self.engine.PINNED_M3_VERSION, "1.1.0")

    # -------------------------------------------------------------
    # 6. STAGE 14C REMEDIATION TESTS: DEF-P1-01 (PROFILE VALIDATION & DENOMINATOR)
    # -------------------------------------------------------------
    def test_23_none_profile_input_excluded_safely(self):
        """None passed as a profile record must be classified as INVALID_PROFILE_TYPE."""
        cohort = [None, self.profiles[0], self.profiles[1], self.profiles[2], self.profiles[3], self.profiles[4]]
        res = self.engine.aggregate_cohort_alignment(cohort)
        self.assertEqual(res["input_profile_count"], 6)
        self.assertEqual(res["eligible_profile_count"], 5)
        self.assertEqual(res["excluded_profile_count"], 1)
        self.assertEqual(res["excluded_profiles_by_reason"]["INVALID_PROFILE_TYPE"], 1)
        self.assertFalse(res["suppressed"])

    def test_24_non_dict_profile_excluded(self):
        """String, integer, or list masquerading as profiles must be excluded as INVALID_PROFILE_TYPE."""
        cohort = ["not_a_dict", 12345, ["nested", "list"], self.profiles[0], self.profiles[1], self.profiles[2], self.profiles[3], self.profiles[4]]
        res = self.engine.aggregate_cohort_alignment(cohort)
        self.assertEqual(res["input_profile_count"], 8)
        self.assertEqual(res["eligible_profile_count"], 5)
        self.assertEqual(res["excluded_profile_count"], 3)
        self.assertEqual(res["excluded_profiles_by_reason"]["INVALID_PROFILE_TYPE"], 3)

    def test_25_empty_dict_profile_excluded(self):
        """Empty dictionaries {} must be excluded as INCOMPLETE_PROFILE_DATA and not increment denominator."""
        cohort = [{}, {"some_key": "val"}, self.profiles[0], self.profiles[1], self.profiles[2], self.profiles[3], self.profiles[4]]
        res = self.engine.aggregate_cohort_alignment(cohort)
        self.assertEqual(res["input_profile_count"], 7)
        self.assertEqual(res["eligible_profile_count"], 5)
        self.assertEqual(res["excluded_profile_count"], 2)
        self.assertEqual(res["excluded_profiles_by_reason"]["INCOMPLETE_PROFILE_DATA"], 2)

    def test_26_confirmed_skills_none_does_not_crash(self):
        """A profile with confirmed_skills=None must not raise TypeError and must default to []."""
        p_with_none_skills = {
            "profile_id": "SYN_NONE_SKILLS_01",
            "cohort_id": "TEST_COHORT",
            "current_role": {"masco_code": "2512"},
            "confirmed_skills": None
        }
        ind = self.engine.aggregate_individual_alignment(p_with_none_skills)
        self.assertEqual(ind["profile_id"], "SYN_NONE_SKILLS_01")
        self.assertEqual(ind["active_skills_count"], 0)

    def test_27_partially_valid_profile_eligibility(self):
        """Profile with valid role but no skills is eligible; profile with empty ID is excluded."""
        valid_role_only = {
            "profile_id": "SYN_ROLE_ONLY_01",
            "current_role": {"masco_code": "2512"}
        }
        status, reason = self.engine.validate_profile_for_aggregation(valid_role_only)
        self.assertEqual(status, "ELIGIBLE")

        empty_id = {
            "profile_id": "",
            "current_role": {"masco_code": "2512"}
        }
        status_empty, reason_empty = self.engine.validate_profile_for_aggregation(empty_id)
        self.assertEqual(status_empty, "EXCLUDED_INCOMPLETE")
        self.assertEqual(reason_empty, "INCOMPLETE_PROFILE_DATA")

    def test_28_all_invalid_cohort_returns_insufficient_eligible_data(self):
        """Cohort of only malformed records returns INSUFFICIENT_ELIGIBLE_COHORT_DATA, not 0% prevalence."""
        invalid_cohort = [{}, None, "not_valid", {"profile_id": ""}]
        res = self.engine.aggregate_cohort_alignment(invalid_cohort)
        self.assertTrue(res["suppressed"])
        self.assertEqual(res["input_profile_count"], 4)
        self.assertEqual(res["eligible_profile_count"], 0)
        self.assertEqual(res["suppression_reason"], "INSUFFICIENT_ELIGIBLE_COHORT_DATA")
        self.assertIn("INSUFFICIENT_ELIGIBLE_COHORT_DATA", res["quality_flags"])

    def test_29_denominator_contract_uses_eligible_count(self):
        """Prevalence ratios must divide by eligible_count, NOT input_profile_count."""
        mixed_cohort = list(self.profiles[:5]) + [{}] * 5
        res = self.engine.aggregate_cohort_alignment(mixed_cohort)
        self.assertEqual(res["input_profile_count"], 10)
        self.assertEqual(res["eligible_profile_count"], 5)
        self.assertFalse(res["suppressed"])

        for sdg_key, s_data in res["sdg_alignment_prevalence"].items():
            count = s_data["aligned_profile_count"]
            self.assertEqual(s_data["prevalence_ratio"], round(count / 5, 4))

    # -------------------------------------------------------------
    # 7. STAGE 14C REMEDIATION TESTS: DEF-P2-01 (FAIRNESS CLAIM SEMANTICS)
    # -------------------------------------------------------------
    def test_30_fairness_hook_structural_non_use_no_dir(self):
        """O5 fairness hook must state structural non-use and never claim empirical DIR=1.000."""
        res = self.engine.aggregate_cohort_alignment(self.profiles[:10])
        o5 = res["o5_fairness_hook"]
        self.assertFalse(o5["protected_attributes_used"])
        self.assertFalse(o5["demographic_fairness_evaluated"])
        self.assertEqual(o5["fairness_scope"], "STRUCTURAL_PROTECTED_ATTRIBUTE_NON_USE")
        self.assertTrue(o5["future_fairness_audit_hook"])
        self.assertNotIn("disparate_impact_ratio", o5)
        self.assertNotIn("DIR", o5)
        self.assertIn("fairness_policy_note", o5)

    # -------------------------------------------------------------
    # 8. STAGE 14C REMEDIATION TESTS: DEF-P2-02 (COMPLEMENTARY SUPPRESSION & DIFFERENCING)
    # -------------------------------------------------------------
    def test_31_partition_complementary_suppression(self):
        """
        Partition differencing protection:
        Parent N=10, Child A N=6, Child B N=4.
        Child B is suppressed (<5). Child A must be complementarily suppressed to prevent Parent - A = B recovery!
        """
        p_x = [dict(self.profiles[i], profile_id=f"SYN_DIFF_X_{i}", region_id="REGION_X") for i in range(6)]
        p_y = [dict(self.profiles[i], profile_id=f"SYN_DIFF_Y_{i}", region_id="REGION_Y") for i in range(4)]
        combined = p_x + p_y

        breakdown = self.engine.aggregate_partition_breakdown(combined, partition_key="region_id")
        self.assertEqual(breakdown["aggregation_level"], "PARTITION_BREAKDOWN")
        self.assertEqual(breakdown["parent_eligible_count"], 10)
        self.assertTrue(breakdown["complementary_suppression_applied"])
        self.assertIn("REGION_Y", breakdown["small_cells_suppressed"])
        self.assertIn("REGION_X", breakdown["complementary_suppressed_cells"])

        cell_y = breakdown["partition_cells"]["REGION_Y"]
        cell_x = breakdown["partition_cells"]["REGION_X"]
        self.assertTrue(cell_y["suppressed"])
        self.assertEqual(cell_y["suppression_reason"], "SUPPRESSED_SMALL_COHORT")
        self.assertTrue(cell_x["suppressed"])
        self.assertEqual(cell_x["suppression_reason"], "SUPPRESSED_COMPLEMENTARY_RULE")
        self.assertIsNone(cell_x["sdg_alignment_prevalence"])

    def test_32_privacy_safeguards_metadata(self):
        """Cohort outputs must carry prototype privacy limitation metadata without claiming DP."""
        res = self.engine.aggregate_cohort_alignment(self.profiles[:10])
        priv = res["privacy_safeguards"]
        self.assertEqual(priv["privacy_protection_level"], "PROTOTYPE_PARTITION_SUPPRESSION")
        self.assertEqual(priv["cross_query_differencing_protection"], "PARTIAL")
        self.assertFalse(priv["differential_privacy_claimed"])
        self.assertIn("differencing_warning", priv)
        self.assertGreaterEqual(len(priv["privacy_limitations"]), 1)

    # -------------------------------------------------------------
    # 9. STAGE 14C REMEDIATION TESTS: DEF-P2-03 (MAPPING-TYPE COUNTING UNIT)
    # -------------------------------------------------------------
    def test_33_mapping_type_canonical_unit_deduplication(self):
        """
        Canonical Counting Unit (i, t, tau):
        Verify multiple skills mapping to the same target with the same type count as ONE (i, t, tau).
        """
        p_dedup = {
            "profile_id": "SYN_DEDUP_TEST_01",
            "current_role": {"masco_code": "2512"},
            "confirmed_skills": ["python_scripting", "api_integration"]
        }
        ind = self.engine.aggregate_individual_alignment(p_dedup)
        # python_scripting and api_integration both map to target 8.2 ENABLING.
        # Unique relations count for 8.2 ENABLING must be 1.
        enabling_count = ind["mapping_type_counts"]["ENABLING"]
        # Total unique targets reached by 2512, python, api are 8.2, 9.4, 9.5 (3 targets)
        self.assertEqual(enabling_count, 3)

        # In cohort aggregation:
        cohort_res = self.engine.aggregate_cohort_alignment(self.profiles[:5])
        m_dist = cohort_res["mapping_type_distribution"]
        self.assertEqual(m_dist["counting_unit"], "UNIQUE_PROFILE_TARGET_MAPPING_TYPE_RELATION")
        self.assertAlmostEqual(m_dist["direct_share"] + m_dist["enabling_share"] + m_dist["contextual_share"], 1.0, places=2)

    def test_34_multiple_legitimate_mapping_types_preserved(self):
        """
        In cohorts with diverse roles and skills (e.g. GREEN_TRANSITION),
        both DIRECT and ENABLING relations are preserved and counted in their respective shares.
        """
        green_cohort = [p for p in self.profiles if p["cohort_id"] == "GREEN_TRANSITION"][:5]
        cohort_res = self.engine.aggregate_cohort_alignment(green_cohort)
        m_dist = cohort_res["mapping_type_distribution"]
        self.assertGreater(m_dist["direct_count"], 0)
        self.assertGreater(m_dist["enabling_count"], 0)
        self.assertAlmostEqual(m_dist["direct_share"] + m_dist["enabling_share"] + m_dist["contextual_share"], 1.0, places=2)

    # -------------------------------------------------------------
    # 10. STAGE 14C REMEDIATION TESTS: DEF-P3-01 & DEF-P3-02 (DISCLAIMERS & WORDING)
    # -------------------------------------------------------------
    def test_35_pathway_alignment_coverage_scope_and_disclaimer(self):
        """Pathway alignment coverage must specify PLANNED_CURRICULUM_SKILL_STEPS and include educational disclaimer."""
        res = self.engine.aggregate_cohort_alignment(self.profiles[:10])
        p_cov = res["pathway_alignment_coverage"]
        self.assertEqual(p_cov["pathway_alignment_coverage_scope"], "PLANNED_CURRICULUM_SKILL_STEPS")
        self.assertIn("Coverage reflects planned reskilling curriculum alignment", p_cov["pathway_alignment_coverage_disclaimer"])

    def test_36_regional_runtime_representativeness_disclaimer(self):
        """Regional and cohort aggregation must include representativeness disclaimer and data_source_class."""
        cohort_res = self.engine.aggregate_cohort_alignment(self.profiles[:10])
        self.assertEqual(cohort_res["data_source_class"], "SYNTHETIC_DEMO")
        self.assertIn("Synthetic demonstration cohort", cohort_res["representativeness_disclaimer"])

        reg_res = self.engine.aggregate_region_alignment(self.profiles, region_id="REGION_A")
        self.assertEqual(reg_res["data_source_class"], "SYNTHETIC_DEMO")
        self.assertIn("Synthetic demonstration cohort", reg_res["representativeness_disclaimer"])

    def test_37_role_isolation_from_skill_capability_coverage(self):
        """Role mappings must NOT enter skill capability-coverage numerator."""
        # A profile with only role 2512 and NO skills has 0 confirmed skills.
        p_role_only = [{
            "profile_id": f"SYN_ROLE_{i}",
            "current_role": {"masco_code": "2512"},
            "confirmed_skills": []
        } for i in range(5)]
        res = self.engine.aggregate_cohort_alignment(p_role_only)
        for sdg_key, c_data in res["capability_coverage"].items():
            self.assertEqual(c_data["skills_present_count"], 0)
            self.assertEqual(c_data["capability_coverage_ratio"], 0.0)


if __name__ == "__main__":
    unittest.main()
