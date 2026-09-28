# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""The fractal block — fall/survive read as dynamics: escape, Lyapunov, bifurcation.

Run:  python3 examples/13_fractal_block.py
"""
from engine import escape_survives, lyapunov_exponent, feigenbaum_delta, newton_basins, MANDELBROT

# escape_survives: True = the orbit stays bounded (it SURVIVES); False = it escapes (it FALLS) —
# the dynamical version of "fall or survive".
escape_survives(complex(-0.5, 0.5), MANDELBROT, maxiter=200)
escape_survives(complex(1.0, 1.0), MANDELBROT, maxiter=200)

# The Lyapunov exponent of the logistic map: negative = order, positive = chaos.
round(lyapunov_exponent(3.2), 4)
round(lyapunov_exponent(3.9), 4)

# The Feigenbaum constant, estimated from the bifurcation cascade:
round(feigenbaum_delta()["feigenbaum"], 6)

# Newton basins of z^5 - 1 split the plane into exactly 5 basins, one per linear factor:
newton_basins(5, N=48)["n_basins"]
