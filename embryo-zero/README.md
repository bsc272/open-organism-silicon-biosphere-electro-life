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
- [firmware/dashboard.py](firmware/dashboard.py) — web dashboard showing live temperature and mood

## Running the firmware demo (no hardware required)

```bash
python3 embryo-zero/firmware/embryo_zero.py --demo --iterations 5
```

## Running the web dashboard (no hardware required)

```bash
pip install flask
python3 embryo-zero/firmware/dashboard.py --demo
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.  The dashboard updates live every two seconds showing temperature, mood, and thermal stress.

To run with a real DHT22 sensor (GPIO 4) on a Raspberry Pi:

```bash
python3 embryo-zero/firmware/dashboard.py
```

## Running the tests

```bash
pip install pytest flask
cd embryo-zero/firmware
python3 -m pytest tests/ -v
```

## Next milestone

Add a real DHT22 sensor and watch the LED react to live temperature changes.
