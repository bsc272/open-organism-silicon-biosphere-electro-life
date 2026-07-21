#!/usr/bin/env python3
"""Raspberry Pi demo: LED blink rate changes with temperature-like input."""

import time
import random

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("RPi.GPIO not available. This script is intended for a Raspberry Pi.")
    raise SystemExit(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

try:
    for _ in range(8):
        temp = 20 + random.random() * 20
        if temp > 35:
            delay = 0.1
            mood = "distressed"
        elif temp < 22:
            delay = 0.4
            mood = "calm"
        else:
            delay = 0.25
            mood = "focused"

        print(f"temp={temp:.1f}C mood={mood}")
        GPIO.output(17, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(17, GPIO.LOW)
        time.sleep(delay)
finally:
    GPIO.cleanup()
