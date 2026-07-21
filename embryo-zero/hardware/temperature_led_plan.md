# Temperature-driven LED plan

This is the next hardware milestone after a simple blink.

## Goal

Make the LED blink faster when the body feels hot and slower when it feels cool.

## Basic build

- Raspberry Pi
- LED on GPIO 17
- optional temperature sensor such as DHT22

## Logic

- if temperature is high: fast blink, distressed mood
- if temperature is low: slow blink, calm mood
- if temperature is in the middle: medium blink, focused mood

## Next step

Use a real DHT22 sensor and replace the synthetic temperature values with live sensor data.
