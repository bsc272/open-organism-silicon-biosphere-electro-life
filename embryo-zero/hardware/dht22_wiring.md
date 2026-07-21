# DHT22 wiring notes

## Basic wiring

- DHT22 VCC -> 3.3V
- DHT22 GND -> GND
- DHT22 DATA -> GPIO 4
- LED anode -> GPIO 17 through 220 ohm resistor
- LED cathode -> GND

## Notes

- Use a 10k pull-up resistor on the data line if your module does not already include one.
- The script uses board.D4 for the data pin.
- This is the first step toward a sensor-driven, mood-based organism.
