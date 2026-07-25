"""Shared test utilities for embryo-zero firmware tests.

Provides stub factory for optional hardware libraries so tests can be run
without a Raspberry Pi or DHT22 sensor attached.
"""

from __future__ import annotations

import sys
import types


def make_hardware_stubs() -> None:
    """Insert minimal module stubs for optional hardware libraries."""
    for name in ("board", "digitalio", "adafruit_dht"):
        if name not in sys.modules:
            mod = types.ModuleType(name)
            mod.__name__ = name
            sys.modules[name] = mod


# Apply stubs immediately when this conftest is loaded so that all test
# modules in this package can import embryo_zero and dashboard safely.
make_hardware_stubs()
