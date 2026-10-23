"""
test_stage14e_consistency.py

Forensic verification suite for Stage 14E:
Resolves Issue A (Contextual Mapping Types) and Issue B (Capability Coverage Definition).
Executes all 16 required tests:
1. DIRECT relation retained
2. ENABLING relation retained
3. CONTEXTUAL relation retained
4. contextual-beneficiary relation retained
5. same profile-target-type deduplicated
6. different types for same profile-target preserved
7. direct + enabling + contextual shares sum to 1
8. zero-relation case safe
9. capability coverage uses M5 canonical skill denominator
10. role mappings do not affect skill capability coverage
11. CURRENT capability coverage uses current skills
12. POST_PATHWAY adds planned skills only
13. 2-of-4 manual capability fixture = 0.50
14. 3-of-4 = 0.75
15. all existing denominator/privacy tests still pass
16. upstream freeze hashes unchanged.
"""

import unittest
import hashlib
import json
import subprocess
from unittest.mock import MagicMock
from src.sdg_aggregation_engine import SDGAggregationEngine
from src.sdg_impact_engine import SDGImpactEngine


class TestStage14EConsistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = SDGAggregationEngine()
        cls.m5 = cls.engine.m5
        with open("data/aggregation/synthetic_workforce_v1.json") as f:
            cls.synthetic_profiles = json.load(f)["profiles"]

    def test_01_direct_relation_retained(self):
        """1. DIRECT relation retained."""
        p = [{'profile_id': f'P{i}', 'confirmed_skills': ['ai_ethics_governance'], 'current_role': None} for i in range(5)]
        res = self.engine.aggregate_cohort_alignment(p)
        self.assertFalse(res['suppressed'])
        m_dist = res['mapping_type_distribution']
        self.assertGreater(m_dist['direct_count'], 0)
        self.assertGreater(m_dist['direct_share'], 0.0)

    def test_02_enabling_relation_retained(self):
        """2. ENABLING relation retained."""
        p = [{'profile_id': f'P{i}', 'confirmed_skills': ['ai_literacy'], 'current_role': None} for i in range(5)]
        res = self.engine.aggregate_cohort_alignment(p)
        self.assertFalse(res['suppressed'])
        m_dist = res['mapping_type_distribution']
        self.assertGreater(m_dist['enabling_count'], 0)
        self.assertGreater(m_dist['enabling_share'], 0.0)

    def test_03_contextual_relation_retained(self):
        """3. CONTEXTUAL relation retained."""
        p = [{'profile_id': f'P{i}', 'current_role': {'masco_code': '4110'}, 'confirmed_skills': []} for i in range(5)]
        res = self.engine.aggregate_cohort_alignment(p)
        self.assertFalse(res['suppressed'])
        m_dist = res['mapping_type_distribution']
        self.assertGreater(m_dist['contextual_count'], 0)
        self.assertGreater(m_dist['contextual_share'], 0.0)

    def test_04_contextual_beneficiary_relation_retained(self):
        """4. contextual-beneficiary relation retained."""
        p = [{'profile_id': f'P{i}', 'current_role': {'masco_code': '4110'}, 'confirmed_skills': []} for i in range(5)]
        res = self.engine.aggregate_cohort_alignment(p)
        self.assertIn('CONTEXTUAL_BENEFICIARY_ALIGNMENT_PRESENT', res['quality_flags'])
        self.assertGreater(res['mapping_type_distribution']['contextual_count'], 0)

    def test_05_same_profile_target_type_deduplicated(self):
        """5. same profile-target-type deduplicated."""
        mock_m5 = MagicMock(spec=self.m5)
        mock_m5.VERSION = '1.1.0'
        mock_m5.targets = {'16.6': {'target_id': '16.6', 'sdg_number': 16}}
        mock_m5.role_mappings = {}
        mock_m5.skill_mappings = {
            's1': {'skill_id': 's1', 'primary_sdgs': [{'target_id': '16.6', 'sdg_id': 16, 'mapping_type': 'DIRECT'}], 'secondary_sdgs': []},
            's2': {'skill_id': 's2', 'primary_sdgs': [{'target_id': '16.6', 'sdg_id': 16, 'mapping_type': 'DIRECT'}], 'secondary_sdgs': []},
        }
        mock_m5.get_skill_sdg_mapping = lambda s: mock_m5.skill_mappings[s]
        mock_m5.get_role_sdg_mapping = lambda r: {}
        eng = SDGAggregationEngine(m5_engine=mock_m5)
        p = [{'profile_id': 'P1', 'confirmed_skills': ['s1', 's2'], 'current_role': None}] + [
            {'profile_id': f'P{i}', 'confirmed_skills': ['unmapped'], 'current_role': None} for i in range(2, 6)
        ]
        res = eng.aggregate_cohort_alignment(p)
        self.assertEqual(res['mapping_type_distribution']['direct_count'], 1)
        self.assertEqual(res['mapping_type_distribution']['total_mappings_evaluated'], 1)

    def test_06_different_types_same_profile_target_preserved(self):
        """6. different types for same profile-target preserved."""
        mock_m5 = MagicMock(spec=self.m5)
        mock_m5.VERSION = '1.1.0'
        mock_m5.targets = {'16.6': {'target_id': '16.6', 'sdg_number': 16}}
        mock_m5.role_mappings = {}
        mock_m5.skill_mappings = {
            's_dir': {'skill_id': 's_dir', 'primary_sdgs': [{'target_id': '16.6', 'sdg_id': 16, 'mapping_type': 'DIRECT'}], 'secondary_sdgs': []},
            's_ctx': {'skill_id': 's_ctx', 'primary_sdgs': [{'target_id': '16.6', 'sdg_id': 16, 'mapping_type': 'CONTEXTUAL'}], 'secondary_sdgs': []},
        }
        mock_m5.get_skill_sdg_mapping = lambda s: mock_m5.skill_mappings[s]
        mock_m5.get_role_sdg_mapping = lambda r: {}
        eng = SDGAggregationEngine(m5_engine=mock_m5)
        p = [{'profile_id': 'P1', 'confirmed_skills': ['s_dir', 's_ctx'], 'current_role': None}] + [
            {'profile_id': f'P{i}', 'confirmed_skills': ['unmapped'], 'current_role': None} for i in range(2, 6)
        ]
        res = eng.aggregate_cohort_alignment(p)
        self.assertEqual(res['mapping_type_distribution']['direct_count'], 1)
        self.assertEqual(res['mapping_type_distribution']['contextual_count'], 1)
        self.assertEqual(res['mapping_type_distribution']['total_mappings_evaluated'], 2)

    def test_07_direct_enabling_contextual_shares_sum_to_1(self):
        """7. direct + enabling + contextual shares sum to 1."""
        for c_id in ['DIGITAL_SERVICES', 'BUSINESS_SERVICES', 'ADVANCED_MANUFACTURING', 'GREEN_TRANSITION']:
            cohort = [p for p in self.synthetic_profiles if p['cohort_id'] == c_id]
            res = self.engine.aggregate_cohort_alignment(cohort)
            m_dist = res['mapping_type_distribution']
            tot = m_dist['direct_share'] + m_dist['enabling_share'] + m_dist['contextual_share']
            self.assertAlmostEqual(tot, 1.0, places=4)

    def test_08_zero_relation_case_safe(self):
        """8. zero-relation case safe."""
        p = [{'profile_id': f'P{i}', 'confirmed_skills': ['unmapped_skill'], 'current_role': None} for i in range(5)]
        res = self.engine.aggregate_cohort_alignment(p)
        m_dist = res['mapping_type_distribution']
        self.assertEqual(m_dist['status'], 'NO_ALIGNMENT_RELATIONS')
        self.assertEqual(m_dist['direct_share'], 0.0)
        self.assertEqual(m_dist['enabling_share'], 0.0)
        self.assertEqual(m_dist['contextual_share'], 0.0)

    def test_09_capability_coverage_uses_m5_canonical_skill_denominator(self):
        """9. capability coverage uses M5 canonical skill denominator."""
        cov = self.engine.get_capability_coverage(
            [{'profile_id': f'P{i}', 'confirmed_skills': ['ai_ethics_governance'], 'current_role': None} for i in range(5)],
            sdg_id=16
        )
        self.assertEqual(cov['canonical_sdg_skills_total'], len(self.engine._canonical_sdg_skills[16]))
        self.assertGreater(cov['canonical_sdg_skills_total'], 0)

    def test_10_role_mappings_do_not_affect_skill_capability_coverage(self):
        """10. role mappings do not affect skill capability coverage."""
        p_role_only = [{'profile_id': f'P{i}', 'current_role': {'masco_code': '2512'}, 'confirmed_skills': []} for i in range(5)]
        res = self.engine.aggregate_cohort_alignment(p_role_only)
        for sdg_key, c_data in res['capability_coverage'].items():
            self.assertEqual(c_data['skills_present_count'], 0)
            self.assertEqual(c_data['capability_coverage_ratio'], 0.0)

    def test_11_current_capability_coverage_uses_current_skills(self):
        """11. CURRENT capability coverage uses current skills."""
        p = [{
            'profile_id': f'P{i}',
            'confirmed_skills': ['ai_ethics_governance'],
            'reskilling_pathway': {'planned_skills': ['carbon_footprint_analytics']},
            'current_role': None
        } for i in range(5)]
        res = self.engine.aggregate_cohort_alignment(p, time_dimension='CURRENT')
        cov13 = res['capability_coverage']['SDG_13']
        self.assertEqual(cov13['skills_present_count'], 0)

    def test_12_post_pathway_adds_planned_skills_only(self):
        """12. POST_PATHWAY adds planned skills only."""
        p = [{
            'profile_id': f'P{i}',
            'confirmed_skills': ['ai_ethics_governance'],
            'reskilling_pathway': {'planned_skills': ['carbon_footprint_analytics']},
            'current_role': None
        } for i in range(5)]
        res = self.engine.aggregate_cohort_alignment(p, time_dimension='POST_PATHWAY')
        cov13 = res['capability_coverage']['SDG_13']
        self.assertGreater(cov13['skills_present_count'], 0)
        self.assertIn('carbon_footprint_analytics', cov13['skills_present_in_cohort'])

    def test_13_manual_2_of_4_capability_fixture(self):
        """13. 2-of-4 manual capability fixture = 0.50."""
        mock_m5 = MagicMock(spec=self.m5)
        mock_m5.VERSION = '1.1.0'
        mock_m5.targets = {'1.1': {'target_id': '1.1', 'sdg_number': 1}}
        mock_m5.skill_mappings = {
            f'sk_{i}': {'skill_id': f'sk_{i}', 'primary_sdgs': [{'target_id': '1.1', 'sdg_id': 1, 'mapping_type': 'DIRECT'}], 'secondary_sdgs': []}
            for i in range(1, 5)
        }
        mock_m5.role_mappings = {}
        mock_m5.get_skill_sdg_mapping = lambda s: mock_m5.skill_mappings[s]
        mock_m5.get_role_sdg_mapping = lambda r: {}
        eng = SDGAggregationEngine(m5_engine=mock_m5)
        cohort = [{'profile_id': 'P1', 'confirmed_skills': ['sk_1', 'sk_2'], 'current_role': None}] + [
            {'profile_id': f'P{i}', 'confirmed_skills': ['unmapped'], 'current_role': None} for i in range(2, 6)
        ]
        res = eng.aggregate_cohort_alignment(cohort)
        cov = res['capability_coverage']['SDG_1']
        self.assertEqual(cov['skills_present_count'], 2)
        self.assertEqual(cov['canonical_sdg_skills_total'], 4)
        self.assertEqual(cov['capability_coverage_ratio'], 0.50)

    def test_14_manual_3_of_4_capability_fixture(self):
        """14. 3-of-4 = 0.75."""
        mock_m5 = MagicMock(spec=self.m5)
        mock_m5.VERSION = '1.1.0'
        mock_m5.targets = {'1.1': {'target_id': '1.1', 'sdg_number': 1}}
        mock_m5.skill_mappings = {
            f'sk_{i}': {'skill_id': f'sk_{i}', 'primary_sdgs': [{'target_id': '1.1', 'sdg_id': 1, 'mapping_type': 'DIRECT'}], 'secondary_sdgs': []}
            for i in range(1, 5)
        }
        mock_m5.role_mappings = {}
        mock_m5.get_skill_sdg_mapping = lambda s: mock_m5.skill_mappings[s]
        mock_m5.get_role_sdg_mapping = lambda r: {}
        eng = SDGAggregationEngine(m5_engine=mock_m5)
        cohort = [{'profile_id': 'P1', 'confirmed_skills': ['sk_1', 'sk_2', 'sk_3'], 'current_role': None}] + [
            {'profile_id': f'P{i}', 'confirmed_skills': ['unmapped'], 'current_role': None} for i in range(2, 6)
        ]
        res = eng.aggregate_cohort_alignment(cohort)
        cov = res['capability_coverage']['SDG_1']
        self.assertEqual(cov['skills_present_count'], 3)
        self.assertEqual(cov['canonical_sdg_skills_total'], 4)
        self.assertEqual(cov['capability_coverage_ratio'], 0.75)

    def test_15_all_existing_denominator_privacy_tests_pass(self):
        """15. all existing denominator/privacy tests still pass."""
        out = subprocess.run(['python', '-m', 'unittest', 'tests/test_sdg_aggregation_engine.py'], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0)
        self.assertIn('OK', out.stderr)

    def test_16_upstream_freeze_hashes_unchanged(self):
        """16. upstream freeze hashes unchanged."""
        expected_hashes = {
            'artifacts/m2_v1_1_1_freeze_manifest.json': 'cdb15cebd1baf9385101cab1dacaf76e63d3703f30995a3c9cd7c2737b9db542',
            'data/scenarios/scenario_build_manifest_v1_1.json': 'ee19b4fc1465ded069471ee8d6e4c85c30082955f31ddfc0e3ca5f2c6a8158b5',
            'data/matching/m3_build_manifest_v1_1.json': '15a489e7e661608547a03fd41a11cf3866126489f9a0195c43edf68e2607973c',
            'artifacts/m4_v1_1_freeze_manifest.json': '448545188ba4e196eaf3502d7803c3d9cfbb1247ec453208cafae990c8db5f2f',
            'artifacts/m5_v1_1_freeze_manifest.json': '94c1f42b46a1fa5e9b026fb82d5225e21c24547cdd58c234f2843cd84eb32ec7'
        }
        for path, exp_sha in expected_hashes.items():
            h = hashlib.sha256()
            with open(path, 'rb') as f:
                while chunk := f.read(8192):
                    h.update(chunk)
            self.assertEqual(h.hexdigest(), exp_sha, f'Hash mismatch on {path}')


if __name__ == '__main__':
    unittest.main()
