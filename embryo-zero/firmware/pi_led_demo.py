#!/usr/bin/env python3
"""Simple Raspberry Pi LED demo for the first embryo."""

import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("RPi.GPIO not available. This script is intended for a Raspberry Pi.")
    raise SystemExit(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

try:
    for _ in range(6):
        GPIO.output(17, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(17, GPIO.LOW)
        time.sleep(0.3)
finally:
    GPIO.cleanup()
