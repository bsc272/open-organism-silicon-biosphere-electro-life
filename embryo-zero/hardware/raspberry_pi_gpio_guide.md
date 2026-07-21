# Raspberry Pi GPIO starter guide

This guide shows the simplest real-world build for the first embryo using a Raspberry Pi and a few basic parts.

## Parts

- Raspberry Pi Zero 2 W or Raspberry Pi 4/5
- breadboard
- LED
- 220 ohm resistor
- jumper wires
- optional: temperature sensor such as DHT22

## Wiring

- LED anode (+) through 220 ohm resistor to GPIO 17
- LED cathode (-) to GND

## Python example

```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

for _ in range(5):
    GPIO.output(17, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(17, GPIO.LOW)
    time.sleep(0.5)

GPIO.cleanup()
```

## What this teaches

- the organism can blink
- the blink can be tied to a mood or temperature state
- the next step is to replace the blind blink with a response to sensor input

## Next upgrade

Add a DHT22 sensor and have the LED blink faster when the temperature rises, slower when it is cool.
