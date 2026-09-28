# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""cipher — classical cryptanalysis as factoral decomposition: the period is the GCD-vote of the repeat gaps.

Run:  python3 examples/27_cipher.py
"""
from engine.toolsets import cipher

plain = ("WE HOLD THESE TRUTHS TO BE SELF EVIDENT THAT ALL MEN ARE CREATED EQUAL "
         "THAT THEY ARE ENDOWED BY THEIR CREATOR WITH CERTAIN UNALIENABLE RIGHTS") * 2

# build_up() with a key encrypts: the emergence direction is a choice of key.
ct = cipher.build_up(plain, key="LIBERTY")["ciphertext"]
ct[:24]

# descend() recovers the period from the ciphertext alone. Kasiski (discrete) and IoC (continuous) both vote.
r = cipher.descend(ct)
r["kasiski"]["period"], round(r["ioc"], 4)
r["ioc_class"]

# With the period in hand, build_up() spends period*26 column trials to recover the key.
b = cipher.build_up(ct, period=7)
b["key"], b["cost"]

# Without a period (or key) the ascent refuses: the period is the owed constraint.
try:
    cipher.build_up(ct)
except Exception as e:
    e.owed
