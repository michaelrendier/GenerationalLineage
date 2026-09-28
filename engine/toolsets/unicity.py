# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
#
# GenerationalLineage is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 3 of the License.
#
# GenerationalLineage is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details. You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-only
"""
GenerationalLineage.engine.toolsets.unicity
============================================
UNICITY — how much ciphertext makes the decomposition unique.

Every cipher-breaking move in this engine recovers a hidden generator (a
period, a key, a substitution). Shannon's unicity distance says *how much
evidence* must be in hand before that recovery is even well-posed:

        U = H(K) / D

    H(K)   the entropy of the key space, in bits — the size of the hidden
           generator's lineage (log₂ of a product of choices)
    D      the redundancy of the plaintext language, bits per character:
           D = log₂|Σ| − H_L, with H_L the language's entropy rate
    U      the ciphertext length (characters) beyond which — in Shannon's
           random-cipher model — the expected number of *spurious* keys
           (wrong keys that also decrypt to something meaningful) falls
           below one:
                E[spurious] = 2^(H(K) − n·D) − 1

Below U, no algorithm can succeed: several keys decrypt to sense and the
data cannot choose between them. Above it, a unique answer exists and the
only remaining question is the cost of finding it. That is a guarantee in
the engine's own sense — a bound on what is *possible*, not a probability
of what a search will find.

TWO REDUNDANCIES, KEPT DISTINCT
    D₀ (computed here, exact)   from the order-0 letter table:
                                D₀ = log₂26 − H₀ ≈ 0.52 bits/char. Since the true
                                entropy RATE H_L ≤ H₀ (context can only help), the
                                true D ≥ D₀, so   U ≤ H(K)/D₀   is a RIGOROUS
                                UPPER BOUND on the unicity distance.
    D_shannon (literature)      D ≈ 3.2 bits/char, from Shannon's H_L ≈ 1.5
                                bits/char estimate for English. An ESTIMATE, labelled
                                as one — not derived here.

DECOMPOSITION (free): `descend({'kind': 'substitution'})` — H(K), both U values,
the redundancy used.
EMERGER (work): `build_up({'kind': …, 'max_spurious': ε})` — the ciphertext
length you must PAY FOR so that E[spurious] ≤ ε; cost = characters.

The counting core the formula rests on (each key is a bijection, so the average
number of keys giving a valid plaintext over all ciphertexts is exactly
|K|·|L_n|/|Σ|ⁿ) is checked EXHAUSTIVELY on a toy language in `verify`.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product
from math import ceil, factorial, log2
from typing import Any, Dict

from ..lines import AscentNotFree

NAME = "unicity"
LINE = "both"

# English single-letter frequencies, percent (same table as toolsets/cipher.py)
ENGLISH_FREQ = {
    "A": 8.17, "B": 1.49, "C": 2.78, "D": 4.25, "E": 12.70, "F": 2.23,
    "G": 2.02, "H": 6.09, "I": 6.97, "J": 0.15, "K": 0.77, "L": 4.03,
    "M": 2.41, "N": 6.75, "O": 7.51, "P": 1.93, "Q": 0.10, "R": 5.99,
    "S": 6.33, "T": 9.06, "U": 2.76, "V": 0.98, "W": 2.36, "X": 0.15,
    "Y": 1.97, "Z": 0.07,
}
H_L_SHANNON = 1.5                     # bits/char — Shannon's estimate for English (literature)


def order0_entropy(freq: Dict[str, float] = ENGLISH_FREQ) -> float:
    tot = sum(freq.values())
    return -sum((v / tot) * log2(v / tot) for v in freq.values() if v > 0)


def redundancy_order0(alphabet: int = 26) -> float:
    return log2(alphabet) - order0_entropy()


def redundancy_shannon(alphabet: int = 26) -> float:
    return log2(alphabet) - H_L_SHANNON


def key_entropy(kind: str, **p) -> float:
    """H(K) in bits for a uniformly chosen key."""
    A = 26
    if kind == "caesar":
        return log2(A)
    if kind == "affine":
        return log2(12 * A)                                   # φ(26)·26 = 312 keys
    if kind == "substitution":
        return log2(factorial(A))
    if kind == "vigenere":
        return p["period"] * log2(A)
    if kind == "columnar":
        return log2(factorial(p["columns"]))
    if kind == "playfair":
        return log2(factorial(25))
    if kind == "enigma":
        # 60 rotor orders × 26³ positions × plugboard(10 leads); ring settings excluded
        plug = factorial(26) // (factorial(6) * 2 ** 10 * factorial(10))
        return log2(60 * 26 ** 3 * plug)
    if kind == "bits":
        return float(p["bits"])
    raise ValueError(f"unknown cipher kind {kind!r}")


def unicity_distance(h_k: float, d: float) -> float:
    return h_k / d


def spurious_keys(h_k: float, d: float, n: int) -> float:
    """Shannon's random-cipher expectation, clipped at 0."""
    return max(0.0, 2.0 ** (h_k - n * d) - 1.0)


def descend(x, **_) -> Dict[str, Any]:
    spec = x if isinstance(x, dict) else {"kind": x}
    spec = dict(spec)
    kind = spec.pop("kind")
    h_k = key_entropy(kind, **spec)
    d0, ds = redundancy_order0(), redundancy_shannon()
    return {
        "toolset": NAME, "kind": kind, "key_entropy_bits": h_k,
        "H0_order0_bits_per_char": order0_entropy(),
        "D0_order0": d0, "D_shannon_estimate": ds,
        "U_upper_bound_rigorous": unicity_distance(h_k, d0),
        "U_shannon_estimate": unicity_distance(h_k, ds),
        "guarantee": "within Shannon's random-cipher model, true U ≤ U_upper_bound_rigorous "
                     "(true D ≥ D0); U_shannon_estimate is a literature estimate, not derived here",
        "note": "below U no algorithm can succeed; above it a unique key exists and only its "
                "cost remains",
    }


def build_up(target, **_) -> Dict[str, Any]:
    if isinstance(target, dict) and "kind" in target:
        spec = dict(target)
        kind = spec.pop("kind")
        eps = float(spec.pop("max_spurious", 1e-3))
        use = spec.pop("redundancy", "shannon")
        h_k = key_entropy(kind, **spec)
        d = redundancy_order0() if use == "order0" else redundancy_shannon()
        n = ceil((h_k - log2(1.0 + eps)) / d)
        n = max(n, 0)
        return {"toolset": NAME, "direction": "ciphertext length owed for uniqueness",
                "characters_needed": n, "expected_spurious_at_n": spurious_keys(h_k, d, n),
                "max_spurious": eps, "redundancy_used": use, "cost": n,
                "note": "the work owed is DATA — this many characters — before search can be well-posed"}
    raise AscentNotFree("{'kind': …, 'max_spurious': ε, 'redundancy': 'shannon' | 'order0'}")


def _toy_counting_core() -> Dict[str, Any]:
    """Alphabet {0,1,2}; keys = the 6 substitutions; language = strings with no two equal
    adjacent letters. For EVERY ciphertext of length n, count keys whose decryption is in the
    language. Each key is a bijection ⇒ the average is EXACTLY |K|·|L_n|/|Σ|ⁿ."""
    keys = list(permutations(range(3)))
    inv = [tuple(sorted(range(3), key=lambda i: k[i])) for k in keys]     # inverse permutations
    out = {}
    for n in range(1, 8):
        total = 0
        for c in product(range(3), repeat=n):
            for k in inv:
                m = [k[s] for s in c]
                if all(m[i] != m[i + 1] for i in range(n - 1)):
                    total += 1
        L_n = 3 * 2 ** (n - 1)
        out[n] = (Fraction(total, 3 ** n), Fraction(len(keys) * L_n, 3 ** n))
    return out


def verify() -> Dict[str, Any]:
    # 1. Shannon's published figure: substitution cipher on English, U ≈ 27.6 letters (D = 3.2)
    d = descend("substitution")
    ok_shannon = abs(d["key_entropy_bits"] - 88.382) < 0.01 and \
        abs(unicity_distance(d["key_entropy_bits"], 3.2) - 27.6) < 0.1

    # 2. computed order-0 numbers are internally consistent
    H0 = order0_entropy()
    ok_h0 = 4.10 < H0 < 4.25 and abs(redundancy_order0() - (log2(26) - H0)) < 1e-12

    # 3. rigorous ordering: upper bound ≥ estimate, for every kind
    kinds = [{"kind": "caesar"}, {"kind": "affine"}, {"kind": "substitution"},
             {"kind": "vigenere", "period": 7}, {"kind": "playfair"}, {"kind": "enigma"},
             {"kind": "columnar", "columns": 8}]
    ok_order = all(descend(k)["U_upper_bound_rigorous"] >= descend(k)["U_shannon_estimate"] for k in kinds)

    # 4. Enigma keyspace entropy — the well-known 1.59e20 ≈ 2^67.1 (ring settings excluded)
    e = key_entropy("enigma")
    ok_enigma = abs(e - 67.1) < 0.1

    # 5. build_up reaches its own target: E[spurious] ≤ ε at n, and > ε at n−1
    ok_up = True
    for k in kinds:
        r = build_up({**k, "max_spurious": 1e-3})
        h = key_entropy(k["kind"], **{a: b for a, b in k.items() if a != "kind"})
        dd = redundancy_shannon()
        if not (spurious_keys(h, dd, r["characters_needed"]) <= 1e-3 + 1e-12
                and spurious_keys(h, dd, r["characters_needed"] - 1) > 1e-3 - 1e-12):
            ok_up = False

    # 6. the counting core, exhaustively, in exact arithmetic
    core = _toy_counting_core()
    ok_core = all(a == b for a, b in core.values())

    try:
        build_up({})
        ok_refuse = False
    except AscentNotFree:
        ok_refuse = True

    return {"ok": all([ok_shannon, ok_h0, ok_order, ok_enigma, ok_up, ok_core, ok_refuse]),
            "shannon_27_6_letters": ok_shannon, "H0_bits": H0, "D0": redundancy_order0(),
            "U_substitution_rigorous_bound": d["U_upper_bound_rigorous"],
            "upper_bound_dominates_estimate": ok_order,
            "enigma_key_entropy_bits": e, "build_up_hits_target": ok_up,
            "toy_counting_core_exact_n1_to_7": ok_core, "refuses_without_kind": ok_refuse}


if __name__ == "__main__":
    print(descend("substitution"))
    print(build_up({"kind": "vigenere", "period": 7}))
    print(verify())
