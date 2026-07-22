# Embryo Zero

This is the first beginner-friendly build in the project.

The goal is simple: create a small device that can feel temperature, express a mood, and blink or speak in response to its own body state.

## Phase 0 — Genesis

The first milestone is to build a simple organism that can:

- sense temperature
- pulse an LED
- express a simple mood
- report a heartbeat or status message

## Suggested starter hardware

- Raspberry Pi or ESP32 board
- LED
- temperature sensor
- breadboard and jumper wires

## Current starter scripts

- [firmware/embryo_zero.py](firmware/embryo_zero.py) — a simple heartbeat and mood demo
- [firmware/simple_sensor_demo.py](firmware/simple_sensor_demo.py) — a sensor-style demo with mood output
- [firmware/pi_led_demo.py](firmware/pi_led_demo.py) — a Raspberry Pi LED blink demo
- [firmware/pi_temp_led_demo.py](firmware/pi_temp_led_demo.py) — a temperature-reactive LED demo
- [firmware/pi_dht22_led_demo.py](firmware/pi_dht22_led_demo.py) — a live DHT22-based demo
- [firmware/main.py](firmware/main.py) — the current Phase 0 board firmware for a DHT22 breath-reactive heartbeat

## Next milestone

Add a real DHT22 sensor and watch the LED react to live temperature changes.

## Phase 0 gate status

Phase 0 is now demonstrated on hardware: live DHT22 readings, breath-reactive humidity spikes, visible LED pulse changes, and JSON heartbeat logging from the board.
