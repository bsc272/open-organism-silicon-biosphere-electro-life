#!/usr/bin/env python3
"""Raspberry Pi + DHT22 LED demo for the first embryo.

This script reads temperature from a DHT22 sensor and changes the LED blink rate
based on the reading.
"""

import time

try:
    import RPi.GPIO as GPIO
except ImportError:
    print("RPi.GPIO not available. This script is intended for a Raspberry Pi.")
    raise SystemExit(1)

try:
    import adafruit_dht
    import board
except ImportError:
    print("adafruit_dht/board not available. Install requirements first.")
    raise SystemExit(1)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

sensor = adafruit_dht.DHT22(board.D4)

try:
    for _ in range(10):
        try:
            temp = sensor.temperature
            if temp is None:
                temp = 25.0
        except RuntimeError:
            temp = 25.0

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
