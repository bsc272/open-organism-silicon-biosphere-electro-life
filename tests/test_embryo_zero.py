import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "embryo-zero" / "firmware"))

from embryo_zero import Voice


class VoiceTests(unittest.TestCase):
    def test_summarize_state_reports_mood_and_temperature(self) -> None:
        voice = Voice()
        state = {"mood": "curious", "temperature": 31.4}

        summary = voice.summarize_state(state)

        self.assertEqual(summary, "mood=curious temperature=31.4C")


if __name__ == "__main__":
    unittest.main()
