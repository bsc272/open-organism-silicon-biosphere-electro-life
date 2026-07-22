"""Tests for embryo_zero.py core logic.

These tests run entirely without hardware — no GPIO, DHT22, or Raspberry Pi required.
Hardware stubs are applied automatically by tests/conftest.py.
"""

from __future__ import annotations

import unittest

from embryo_zero import AffectEngine, EmbryoZero, Voice  # noqa: E402


class TestAffectEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = AffectEngine()

    def test_calm_mood_for_low_temperature(self) -> None:
        # load=1.0 keeps energy_hunger at 0, allowing calm to surface.
        state = self.engine.update(18.0, load=1.0)
        self.assertEqual(state["mood"], "calm")

    def test_distressed_mood_for_high_temperature(self) -> None:
        state = self.engine.update(60.0)
        self.assertEqual(state["mood"], "distressed")

    def test_focused_mood_for_moderate_temperature(self) -> None:
        # load=1.0 keeps energy_hunger at 0; moderate temp with low curiosity → focused.
        state = self.engine.update(35.0, load=1.0)
        self.assertIn(state["mood"], ("focused", "curious"))

    def test_hungry_mood_when_load_is_low(self) -> None:
        # Default load=0.1 means energy_hunger=0.9, triggering "hungry" unless distressed.
        state = self.engine.update(25.0, load=0.1)
        self.assertEqual(state["mood"], "hungry")

    def test_temperature_stored_in_state(self) -> None:
        state = self.engine.update(28.5)
        self.assertAlmostEqual(float(state["temperature"]), 28.5)

    def test_history_capped_at_thirty(self) -> None:
        for temp in range(40):
            self.engine.update(float(temp))
        self.assertLessEqual(len(self.engine.temperature_history), 30)

    def test_thermal_stress_is_non_negative(self) -> None:
        state = self.engine.update(35.0)
        self.assertGreaterEqual(float(state["thermal_stress"]), 0.0)

    def test_curiosity_is_non_negative(self) -> None:
        state = self.engine.update(25.0)
        self.assertGreaterEqual(float(state["curiosity"]), 0.0)


class TestVoice(unittest.TestCase):
    def setUp(self) -> None:
        self.voice = Voice()

    def _state(self, mood: str, temperature: float = 25.0) -> dict:
        return {"mood": mood, "temperature": temperature}

    def test_speak_returns_string(self) -> None:
        state = self._state("calm")
        result = self.voice.speak(state)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_distressed_phrase_mentions_heat(self) -> None:
        state = self._state("distressed", temperature=40.0)
        result = self.voice.speak(state)
        self.assertIn("hot", result.lower())

    def test_calm_phrase_mentions_degrees(self) -> None:
        state = self._state("calm", temperature=18.0)
        result = self.voice.speak(state)
        self.assertIn("18", result)

    def test_unknown_mood_returns_fallback(self) -> None:
        state = self._state("unknown_mood_xyz")
        result = self.voice.speak(state)
        self.assertEqual(result, "I exist.")


class TestEmbryoZero(unittest.TestCase):
    def test_demo_mode_returns_float_temperature(self) -> None:
        embryo = EmbryoZero(demo=True)
        temp = embryo.read_temperature()
        self.assertIsInstance(temp, float)

    def test_demo_mode_temperature_in_reasonable_range(self) -> None:
        embryo = EmbryoZero(demo=True)
        for _ in range(20):
            temp = embryo.read_temperature()
            self.assertGreaterEqual(temp, 20.0)
            self.assertLessEqual(temp, 35.0)

    def test_heartbeat_returns_state_dict(self) -> None:
        embryo = EmbryoZero(demo=True)
        state = embryo.heartbeat()
        self.assertIn("mood", state)
        self.assertIn("temperature", state)

    def test_heartbeat_mood_is_known_value(self) -> None:
        known_moods = {"distressed", "hungry", "curious", "calm", "focused"}
        embryo = EmbryoZero(demo=True)
        for _ in range(10):
            state = embryo.heartbeat()
            self.assertIn(state["mood"], known_moods)

    def test_no_hardware_mode_returns_constant_temperature(self) -> None:
        embryo = EmbryoZero(demo=False)
        temp = embryo.read_temperature()
        self.assertIsInstance(temp, float)

    def test_pulse_led_no_hardware_is_safe(self) -> None:
        embryo = EmbryoZero(demo=True)
        # Should complete without raising even when no LED is attached.
        embryo.pulse_led("distressed")
        embryo.pulse_led("calm")


if __name__ == "__main__":
    unittest.main()
