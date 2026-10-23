"""Stage 20 End-to-End Full System Integration Test Suite.
Validates the cohesive interoperation of all 12 modules:
M1, M2 v1.1.1, M6 v1.1.0, M3 v1.1.0, M4 v1.1.0, M5 v1.1.0,
O6 v1.1.0, O1 v1.1.0, O2 v1.0.0, O3 v1.0.0, O4 v1.0.0, O5 v1.0.0.
"""

from __future__ import annotations

import json
import threading
import time
import unittest
import urllib.request
import urllib.parse
from http.server import HTTPServer
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "src"))

from main import CompassRequestHandler, ReusableThreadingHTTPServer
from governance_engine import GovernanceEngine


class TestStage20FullSystemIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ReusableThreadingHTTPServer(("127.0.0.1", 0), CompassRequestHandler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def _get(self, path: str) -> tuple[int, dict | str]:
        url = f"http://127.0.0.1:{self.port}{path}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            content_type = resp.headers.get("Content-Type", "")
            raw = resp.read().decode("utf-8")
            if "application/json" in content_type:
                return status, json.loads(raw)
            return status, raw

    def test_01_api_health(self):
        status, data = self._get("/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["uptime_status"], "HEALTHY_OPERATIONAL")
        self.assertTrue(data["all_frozen_verified"])
        self.assertGreaterEqual(data["frozen_subsystems_count"], 10)

    def test_02_api_signals(self):
        status, data = self._get("/api/signals")
        self.assertEqual(status, 200)
        self.assertIn("signals", data)
        self.assertGreater(len(data["signals"]), 0)

    def test_03_api_evaluate(self):
        status, data = self._get("/api/evaluate?profile_id=aisyah_ops&scenario_id=moderate_copilot")
        self.assertEqual(status, 200)
        self.assertIn("profile", data)
        self.assertIn("evaluation", data)
        self.assertEqual(data["evaluation"]["status"], "ok")
        self.assertGreaterEqual(len(data["evaluation"]["ranked_roles"]), 1)

    def test_04_api_employer(self):
        status, data = self._get("/api/employer")
        self.assertEqual(status, 200)
        self.assertIn("workforce_gap_summary", data)
        self.assertIn("sdg_collective_aggregation", data)
        self.assertIn("cohort_gap_heatmap", data["workforce_gap_summary"])

    def test_05_api_replan(self):
        status, data = self._get("/api/replan?profile_id=aisyah_ops")
        self.assertEqual(status, 200)
        self.assertIn("materiality_tier", data)
        self.assertIn("change_detected", data)

    def test_06_api_progress(self):
        status, data = self._get("/api/progress?profile_id=aisyah_ops")
        self.assertEqual(status, 200)
        self.assertIn("overall_completion_pct", data)
        self.assertIn("earned_badges", data)
        self.assertIn("disclaimer", data)

    def test_07_api_governance_and_ledger(self):
        status, data = self._get("/api/governance")
        self.assertEqual(status, 200)
        self.assertEqual(data["status"], "APPROVED")
        self.assertEqual(data["counterfactual_invariance"]["max_score_delta"], 0.0)

        status_json, data_json = self._get("/api/audit-ledger.json")
        self.assertEqual(status_json, 200)
        self.assertEqual(data_json["audit_ledger_version"], "v1.0.0")

    def test_08_api_locales(self):
        for loc in ["en", "ms", "zh-CN"]:
            status, cat = self._get(f"/api/locales/{loc}")
            self.assertEqual(status, 200)
            self.assertIn("app", cat)
            self.assertIn("title", cat["app"])

    def test_09_dashboard_ten_tabs_rendered(self):
        status, html = self._get("/")
        self.assertEqual(status, 200)
        # Verify all 10 tabs exist in HTML
        tabs = [
            "tab-overview",
            "tab-radar",
            "tab-matching",
            "tab-gaps",
            "tab-pathway",
            "tab-scenarios",
            "tab-sdg",
            "tab-progress",
            "tab-employer",
            "tab-governance",
        ]
        for t in tabs:
            self.assertIn(f'id="{t}"', html)
            self.assertIn(f'data-tab="{t}"', html)

    def test_10_low_bandwidth_toggle(self):
        status, html = self._get("/?low_bw=1")
        self.assertEqual(status, 200)
        self.assertIn('data-low-bandwidth="true"', html)
        self.assertIn("Standard Rich Mode", html)

    def test_11_cryptographic_freeze_integrity(self):
        gov = GovernanceEngine()
        ok, rep = gov.verify_freeze_integrity()
        self.assertTrue(ok)
        self.assertTrue(rep["all_frozen_verified"])
        self.assertGreaterEqual(rep["modules_checked"], 9)


if __name__ == "__main__":
    unittest.main()
