#!/usr/bin/env python3
"""A tiny sensor demo for the first embryo.

This script shows how a very simple device can report a temperature-like value,
turn it into a mood, and print a short message.
"""

from __future__ import annotations

import random
import time


def mood_from_temp(temp: float) -> str:
    if temp > 35:
        return "distressed"
    if temp < 20:
        return "calm"
    return "focused"


def main() -> None:
    print("Embryo sensor demo starting...")
    for i in range(5):
        temp = 20 + random.random() * 20
        mood = mood_from_temp(temp)
        print(f"cycle={i+1} temp={temp:.1f} mood={mood}")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
