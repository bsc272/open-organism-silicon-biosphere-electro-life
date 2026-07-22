#!/usr/bin/env python3
"""CircuitPython firmware for Embryo-Zero Phase 0.

This script is intended to run as ``main.py`` on a small microcontroller board.
It reads a DHT22 on GPIO4, pulses an LED faster as temperature rises, and logs
JSON state snapshots roughly every five seconds.
"""

from __future__ import annotations

import json
import time

import adafruit_dht
import board
import digitalio


def resolve_pin(*names: str):
    for name in names:
        pin = getattr(board, name, None)
        if pin is not None:
            return pin
    raise AttributeError(f"None of the requested pins exist on this board: {names}")


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def pulse_rate_hz(temperature_c: float) -> float:
    """Map temperature to a visible heartbeat rate.

    22C maps to a slow 1.8 Hz pulse and 35C maps to a faster 3.6 Hz pulse.
    """

    cool = 22.0
    warm = 35.0
    low_hz = 1.8
    high_hz = 3.6
    clamped_temp = clamp(temperature_c, cool, warm)
    ratio = (clamped_temp - cool) / (warm - cool)
    return low_hz + ((high_hz - low_hz) * ratio)


LED_PIN = resolve_pin("LED", "IO2", "D2")
DHT_PIN = resolve_pin("IO4", "D4", "GP4")

led = digitalio.DigitalInOut(LED_PIN)
led.direction = digitalio.Direction.OUTPUT
sensor = adafruit_dht.DHT22(DHT_PIN, use_pulseio=False)

start_time = time.monotonic()
last_log_time = 0.0
phase = 0

while True:
    try:
        temperature_c = sensor.temperature
        humidity_pct = sensor.humidity
        if temperature_c is None or humidity_pct is None:
            raise RuntimeError("sensor returned null reading")

        pulse_hz = pulse_rate_hz(float(temperature_c))
        half_period = 0.5 / pulse_hz
        now = time.monotonic()

        if now - last_log_time >= 5.0:
            payload = {
                "alive_seconds": int(now - start_time),
                "humidity_pct": round(float(humidity_pct), 1),
                "phase": phase,
                "pulse_hz": round(pulse_hz, 2),
                "status": "embryo",
                "temperature_c": round(float(temperature_c), 1),
            }
            print(json.dumps(payload))
            last_log_time = now

        led.value = True
        time.sleep(half_period)
        led.value = False
        time.sleep(half_period)
        phase = 1 - phase
    except RuntimeError:
        time.sleep(0.25)
