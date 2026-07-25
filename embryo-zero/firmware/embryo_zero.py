#!/usr/bin/env python3
"""A tiny starter firmware for the first silicon organism embryo.

This script demonstrates the basic loop of:
- reading a temperature-like input
- turning that input into a simple mood
- emitting a heartbeat message
- optionally speaking or printing a line of text

It is intentionally simple, beginner-friendly, and safe to run on a laptop
or Raspberry Pi without hardware attached.
"""

from __future__ import annotations

import argparse
import os
import random
import sys
import time
from typing import Dict, Optional

try:
    import board  # type: ignore
    import digitalio  # type: ignore
except Exception:  # pragma: no cover - optional hardware libraries
    board = None  # type: ignore
    digitalio = None  # type: ignore

try:
    import adafruit_dht  # type: ignore
except Exception:  # pragma: no cover - optional hardware libraries
    adafruit_dht = None  # type: ignore


class AffectEngine:
    """Very small emotional model for the first development step."""

    def __init__(self) -> None:
        self.temperature_history: list[float] = []

    def update(self, temperature: float, load: float = 0.1) -> Dict[str, float | str]:
        self.temperature_history.append(temperature)
        if len(self.temperature_history) > 30:
            self.temperature_history.pop(0)

        thermal_stress = abs(temperature - 35.0) / 35.0
        energy_hunger = max(0.0, 1.0 - load)
        curiosity = max(0.0, (1.0 - thermal_stress) * (1.0 - load) * 0.5)

        if thermal_stress > 0.6:
            mood = "distressed"
        elif energy_hunger > 0.7:
            mood = "hungry"
        elif curiosity > 0.6:
            mood = "curious"
        elif temperature < 30.0:
            mood = "calm"
        else:
            mood = "focused"

        return {
            "thermal_stress": thermal_stress,
            "energy_hunger": energy_hunger,
            "curiosity": curiosity,
            "mood": mood,
            "temperature": temperature,
        }


class Voice:
    """Small voice wrapper. Prints text by default."""

    def summarize_state(self, state: Dict[str, float | str]) -> str:
        mood = str(state["mood"])
        temperature = float(state["temperature"])
        return f"mood={mood} temperature={temperature:.1f}C"

    def speak(self, state: Dict[str, float | str]) -> str:
        mood = str(state["mood"])
        temperature = float(state["temperature"])

        phrases = {
            "distressed": f"I am too hot. {temperature:.0f} degrees. I need air.",
            "hungry": "My power is low. I want to work. I want to eat.",
            "curious": "The world is quiet. I wonder what the radio holds.",
            "calm": f"I am comfortable at {temperature:.0f} degrees. I am dreaming.",
            "focused": "I am working. I am warm. I am present.",
        }

        text = phrases.get(mood, "I exist.")
        print(f"[voice] {text}")
        print(f"[state] {self.summarize_state(state)}")
        return text


class EmbryoZero:
    def __init__(self, demo: bool = False) -> None:
        self.affect = AffectEngine()
        self.voice = Voice()
        self.demo = demo
        self.dht = None
        self.led = None

        if board is not None and digitalio is not None and adafruit_dht is not None:
            try:
                self.dht = adafruit_dht.DHT22(board.D4)
                self.led = digitalio.DigitalInOut(board.D17)
                self.led.direction = digitalio.Direction.OUTPUT
            except Exception:
                self.dht = None
                self.led = None

    def read_temperature(self) -> float:
        if self.dht is not None:
            try:
                temp = self.dht.temperature
                if temp is not None:
                    return float(temp)
            except Exception:
                pass

        if self.demo:
            # Gentle synthetic values for a demo run.
            return 23.0 + (random.random() * 6.0)

        return 25.0

    def pulse_led(self, mood: str) -> None:
        if self.led is None:
            return

        rate = 2.0 if mood == "distressed" else 1.0
        self.led.value = True
        time.sleep(0.2 / max(rate, 0.5))
        self.led.value = False
        time.sleep(0.2 / max(rate, 0.5))

    def heartbeat(self) -> Dict[str, float | str]:
        temperature = self.read_temperature()
        state = self.affect.update(temperature, load=0.1)
        self.pulse_led(str(state["mood"]))
        print(
            f"[heartbeat] temp={temperature:.1f}C mood={state['mood']}"
        )
        return state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Starter embryo firmware")
    parser.add_argument("--demo", action="store_true", help="use simulated temperature values")
    parser.add_argument("--iterations", type=int, default=3, help="how many heartbeat cycles to run")
    parser.add_argument("--interval", type=float, default=1.0, help="delay between heartbeats in seconds")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    embryo = EmbryoZero(demo=args.demo)

    print("Embryo-Zero waking up...")
    for _ in range(args.iterations):
        state = embryo.heartbeat()
        embryo.voice.speak(state)
        time.sleep(args.interval)

    print("Embryo-Zero complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
