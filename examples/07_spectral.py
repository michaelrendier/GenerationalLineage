# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Spectral decomposition — factoring a signal into wavelengths, not sedenion-specific.

Run:  python3 examples/07_spectral.py
"""
import math
from engine import spectral_decompose

# Two pure tones (5 and 12 cycles in 64 samples). The decomposition finds exactly two lines.
x = [math.sin(2 * math.pi * 5 * i / 64) + 0.5 * math.sin(2 * math.pi * 12 * i / 64) for i in range(64)]
r = spectral_decompose(x)
r["n_samples"], r["lines_kept"], r["n_lines_total"]
round(r["explained_fraction"], 12)

# Each kept line is a wavelength factor, and the round trip through the spectrum is exact:
bool(r["round_trip_exact"])
sorted(round(f["wavelength"], 3) for f in r["wavelength_factors"])
