# Firmware

This folder holds the earliest software experiments for the organism.

## Current starter scripts

- [embryo_zero.py](embryo_zero.py) — a simple demo loop that simulates a heartbeat and mood response.
- [simple_sensor_demo.py](simple_sensor_demo.py) — a tiny sensor-style demo that turns a temperature-like value into a mood.

## Run the simple demo

```bash
python3 embryo-zero/firmware/simple_sensor_demo.py
```

## Run the heartbeat demo

```bash
python3 embryo-zero/firmware/embryo_zero.py --demo --iterations 2
```

## Next steps

- connect a real temperature sensor
- blink an LED based on mood
- add simple speech output
- add GPS or LoRa later

## Small contribution idea

The firmware now exposes a tiny state summary via the voice layer so contributors can see the embryo’s mood and temperature in one line. This makes a good first pull request: improve the phrasing, add a new mood, or make the output more expressive.
