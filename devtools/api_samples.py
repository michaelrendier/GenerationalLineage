# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Sample calls used to generate the API reference pages: one (args, kwargs) per direction per toolset.

build_docs.py runs each sample to list the keys a call returns and what a refused ascent owes, so the reference is read off the
code, not typed. Each sample is also a minimal call a reader can retype."""
import math

# name: (descend_args, descend_kwargs, build_up_args, build_up_kwargs)
SAMPLES = {
    "add_scale_sign": ((3.0,), {"reference": 1.0}, ({"a": 1.0, "s": 2.0, "g": -1},), {}),
    "scale": ((15.0,), {"reference": 3.0}, ({"x": 2.0, "y": 9.0},), {"probes": [(5.0, 21.0)]}),
    "units": (("N",), {}, ("N",), {}),
    "box_kite": (((1, 10),), {}, (11,), {}),
    "noether": (([(0.3, 0.7), (0.5, 0.5), (0.1, 0.9)],), {}, ([[0.3, 0.7], [0.5, 0.5]], 1.0), {}),
    "archimedes_screw": (((2, 6),), {}, (3.0,), {}),
    "inversion": (((2.0, 0.0),), {}, ((2.0, 0.0),), {}),
    "t32_nilpotency": ((123456,), {}, ([5, 0, 0],), {}),
    "cipher": (("LXFOPVEFRNHRLXFOPVEFRNHRLXFOPVEFRNHR",), {}, ("ATTACKATDAWN",), {"key": "LEMON"}),
    "comma_sequence": (([1, 12, 24, 36],), {}, (12,), {}),
    "hyper_linear": ((1546854629, 7283619945), {}, ({"product": 1546854629 * 7283619945, "a": 1546854629},), {}),
    "equation_space": ((0.5 + 0.1j,), {}, ({"start": 0.5 + 0.1j},), {}),
    "spectral_primes": ((100.0,), {}, (10.0,), {"n_zeros": 10}),
    "cs_benchmark": ((sum,), {"args": ([1, 2, 3],), "n": 200}, ({"sum": sum}, 1e-6), {"args": ([1, 2, 3],), "n": 200}),
    "stencil": ((53, 61), {}, (91,), {}),
    "periodicity": (("abcabcabca",), {}, ({"root": "ab", "length": 8},), {}),
    "lyndon": (("banana",), {}, ({"n": 6, "k": 2},), {}),
    "berlekamp_massey": (([1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1],), {}, ({"taps": [1, 0, 1], "init": [1, 0, 0], "length": 12},), {}),
    "logperiodic": ((([1.0 + 0.5 * i for i in range(60)], [math.sin(math.log(1.0 + 0.5 * i) * 6.0) for i in range(60)]),), {}, ({"omega": 6.0, "amp": 1.0, "phase": 0.0, "const": 0.0, "trend": 0.0},), {}),
    "permutation": (([2, 0, 1, 4, 3, 5],), {}, ({"order": 60},), {}),
    "rejewski": (("QEV",), {}, ({"characteristic": [(3, 2, 1, 1), (2, 2, 1, 1)]},), {}),
    "jordan_chevalley": (([[2, 1], [0, 2]],), {}, ({"blocks": [(1, 1), (2, 1), (3, 1)]},), {}),
    "re_pair": (("abracadabra" * 3,), {}, ({"grammar": __import__("engine.toolsets.re_pair", fromlist=["x"]).compress(list("abracadabra" * 3))},), {}),
    "pohlig_hellman": (({"p": 101, "g": 2, "h": 5},), {}, ({"p": 101, "g": 2, "h": 5},), {}),
    "unicity": (("substitution",), {}, ({"kind": "substitution", "max_spurious": 1e-3},), {}),
    "circle": ((0.5, "radius"), {}, (math.pi, "area"), {}),
}
