"""Tests for the Embryo-Zero web dashboard (dashboard.py).

These tests run entirely without hardware — no GPIO, DHT22, or Raspberry Pi required.
Hardware stubs are applied automatically by tests/conftest.py.
Flask's built-in test client is used, so no live server is started.
"""

from __future__ import annotations

import json
import unittest

# Import the module under test.
import dashboard  # noqa: E402
from embryo_zero import EmbryoZero  # noqa: E402


class TestDashboardRoutes(unittest.TestCase):
    def setUp(self) -> None:
        dashboard._embryo = EmbryoZero(demo=True)
        self.client = dashboard.app.test_client()

    def test_index_returns_200(self) -> None:
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)

    def test_index_contains_embryo_title(self) -> None:
        resp = self.client.get("/")
        self.assertIn(b"Embryo-Zero", resp.data)

    def test_state_endpoint_returns_json(self) -> None:
        resp = self.client.get("/state")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("application/json", resp.content_type)

    def test_state_endpoint_has_expected_keys(self) -> None:
        resp = self.client.get("/state")
        data = json.loads(resp.data)
        for key in ("temperature", "mood", "thermal_stress", "energy_hunger", "curiosity", "source"):
            self.assertIn(key, data)

    def test_state_temperature_is_number(self) -> None:
        resp = self.client.get("/state")
        data = json.loads(resp.data)
        self.assertIsInstance(data["temperature"], float)

    def test_state_mood_is_string(self) -> None:
        resp = self.client.get("/state")
        data = json.loads(resp.data)
        self.assertIsInstance(data["mood"], str)

    def test_state_source_is_demo(self) -> None:
        resp = self.client.get("/state")
        data = json.loads(resp.data)
        self.assertEqual(data["source"], "demo")

    def test_state_thermal_stress_is_non_negative(self) -> None:
        resp = self.client.get("/state")
        data = json.loads(resp.data)
        self.assertGreaterEqual(data["thermal_stress"], 0.0)


if __name__ == "__main__":
    unittest.main()
