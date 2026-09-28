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
GenerationalLineage.engine.toolsets.rejewski
=============================================
REJEWSKI — the conjugacy-class invariant that broke Enigma.

Enigma's plugboard P is an involution that the machine wraps around its whole
rotor path:   S′ᵢ = P · Sᵢ · P.   The plugboard multiplies the keyspace by
~1.5×10¹⁴ — and, in Marian Rejewski's 1932 observation, contributes NOTHING
to the *cycle type* of a product of two such permutations:

        S′ᵢ · S′ⱼ = P · (Sᵢ · Sⱼ) · P⁻¹        — a CONJUGATE of Sᵢ·Sⱼ

Conjugate permutations share a cycle type, so the multiset of cycle lengths of
Sᵢ·S_{i+3} is a fingerprint of the rotor setting that the plugboard cannot
disturb. Three products (1&4, 2&5, 3&6 — Rejewski's AD, BE, CF) give the
**characteristic**. Two structural facts, both checked here:

    · every Sᵢ is a fixed-point-free involution (the reflector: a derangement),
      so in Sᵢ·Sⱼ every cycle length occurs an EVEN number of times

That is factoral decomposition of a re-ordering: strip away the part of the
operator that acts by conjugation (the plugboard) and read the invariant
that is left.

DECOMPOSITION (free): `descend(setting, plugboard=…)` — the characteristic of one
setting, and its independence from the plugboard.

EMERGER (work): `build_up({'characteristic': …})` — the card catalogue. Scans all
26³ start positions for the rotor order and returns those whose characteristic
matches (cost = settings scanned). The plugboard was never part of the search.

SCOPE: Enigma I, rotors I·II·III (left→right), reflector UKW-B, ring
settings AAA, full stepping including the middle-rotor double-step. The
implementation is validated against the standard known-answer vector
(positions AAA, no plugs: AAAAA → BDZGO) before anything is built on it.
"""
from __future__ import annotations

from typing import Any, Dict, List, Sequence, Tuple

from ..lines import AscentNotFree

NAME = "rejewski"
LINE = "both"

A = 26
ROTOR_WIRING = {
    "I": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "II": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
}
ROTOR_NOTCH = {"I": "Q", "II": "E", "III": "V"}
REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
ROTORS = ("I", "II", "III")                    # left, middle, right

_FWD = {k: [ord(c) - 65 for c in v] for k, v in ROTOR_WIRING.items()}
_BWD = {}
for _k, _w in _FWD.items():
    _inv = [0] * A
    for _i, _c in enumerate(_w):
        _inv[_c] = _i
    _BWD[_k] = _inv
_REF = [ord(c) - 65 for c in REFLECTOR_B]
_NOTCH = [ord(ROTOR_NOTCH[r]) - 65 for r in ROTORS]


def _step(pos: Tuple[int, int, int]) -> Tuple[int, int, int]:
    l, m, r = pos
    if m == _NOTCH[1]:                          # double step: middle steps itself and the left
        l, m = (l + 1) % A, (m + 1) % A
    elif r == _NOTCH[2]:
        m = (m + 1) % A
    return l, m, (r + 1) % A




def _through(pos: Tuple[int, int, int], c: int) -> int:
    """One letter through rotors → reflector → rotors, rotor positions fixed (no plugboard)."""
    # right → middle → left
    for idx in (2, 1, 0):
        p = pos[idx]
        c = (_FWD[ROTORS[idx]][(c + p) % A] - p) % A
    c = _REF[c]
    for idx in (0, 1, 2):
        p = pos[idx]
        c = (_BWD[ROTORS[idx]][(c + p) % A] - p) % A
    return c


def state_perm(pos: Tuple[int, int, int]) -> List[int]:
    """The involution Enigma applies (before the plugboard wrapper) at rotor state `pos`."""
    return [_through(pos, c) for c in range(A)]


def _plug_perm(plugboard: str = "") -> List[int]:
    p = list(range(A))
    for pair in plugboard.split():
        a, b = ord(pair[0]) - 65, ord(pair[1]) - 65
        p[a], p[b] = b, a
    return p


def encipher(text: str, start: str = "AAA", plugboard: str = "") -> str:
    pos = tuple(ord(c) - 65 for c in start)
    P = _plug_perm(plugboard)
    out = []
    for ch in text.upper():
        pos = _step(pos)
        c = P[ord(ch) - 65]
        c = _through(pos, c)
        out.append(chr(65 + P[c]))
    return "".join(out)


def _mul(p: Sequence[int], q: Sequence[int]) -> List[int]:
    return [p[q[i]] for i in range(len(p))]


def _cycle_type(perm: Sequence[int]) -> Tuple[int, ...]:
    seen, out = [False] * len(perm), []
    for i in range(len(perm)):
        if not seen[i]:
            n, j = 0, i
            while not seen[j]:
                seen[j] = True
                j = perm[j]
                n += 1
            out.append(n)
    return tuple(sorted(out, reverse=True))


def six_states(start: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    out, pos = [], start
    for _ in range(6):
        pos = _step(pos)
        out.append(pos)
    return out


def characteristic(start: Tuple[int, int, int], plugboard: str = "") -> Tuple[Tuple[int, ...], ...]:
    """(cycle type of S1·S4, S2·S5, S3·S6) with the plugboard wrapped around every Sᵢ."""
    P = _plug_perm(plugboard)
    S = []
    for pos in six_states(start):
        base = state_perm(pos)
        S.append(_mul(P, _mul(base, P)))
    return tuple(_cycle_type(_mul(S[i], S[i + 3])) for i in range(3))


_CATALOGUE: Dict[Tuple, List[Tuple[int, int, int]]] | None = None


def catalogue() -> Dict[Tuple, List[Tuple[int, int, int]]]:
    """characteristic → the start positions producing it (all 26³, plugboard-free)."""
    global _CATALOGUE
    if _CATALOGUE is None:
        cache: Dict[Tuple[int, int, int], List[int]] = {}
        table: Dict[Tuple, List[Tuple[int, int, int]]] = {}
        for l in range(A):
            for m in range(A):
                for r in range(A):
                    st = (l, m, r)
                    S = []
                    for pos in six_states(st):
                        if pos not in cache:
                            cache[pos] = state_perm(pos)
                        S.append(cache[pos])
                    ch = tuple(_cycle_type(_mul(S[i], S[i + 3])) for i in range(3))
                    table.setdefault(ch, []).append(st)
        _CATALOGUE = table
    return _CATALOGUE


def _name(pos: Tuple[int, int, int]) -> str:
    return "".join(chr(65 + p) for p in pos)


def descend(x, plugboard: str = "", **_) -> Dict[str, Any]:
    start = tuple(ord(c) - 65 for c in x.upper()) if isinstance(x, str) else tuple(x)
    ch = characteristic(start, plugboard)
    ch0 = characteristic(start, "")
    return {
        "toolset": NAME, "start": _name(start), "plugboard": plugboard or "(none)",
        "characteristic": ch,
        "plugboard_independent": ch == ch0,
        "even_multiplicities": all(all(t.count(L) % 2 == 0 for L in set(t)) for t in ch),
        "note": "cycle type of S_i·S_{i+3} is a conjugacy-class invariant — the plugboard "
                "acts by conjugation and cannot change it",
    }


def build_up(target, **_) -> Dict[str, Any]:
    if isinstance(target, dict) and "characteristic" in target:
        want = tuple(tuple(sorted(t, reverse=True)) for t in target["characteristic"])
        table = catalogue()
        hits = table.get(want, [])
        return {"toolset": NAME, "direction": "characteristic -> candidate settings (the card catalogue)",
                "matches": [_name(p) for p in hits], "n_matches": len(hits),
                "cost": A ** 3, "distinct_characteristics": len(table),
                "note": "the plugboard was never part of the search — it conjugates away"}
    raise AscentNotFree("{'characteristic': (type_AD, type_BE, type_CF)}")


def verify() -> Dict[str, Any]:
    # 1. known-answer test: Enigma I, rotors I II III, UKW-B, rings AAA, positions AAA, no plugs
    ok_kat = encipher("AAAAA", "AAA") == "BDZGO"
    #    and reciprocity (encipher twice returns the plaintext) with plugs
    msg = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
    plug = "AB CD EF GH IJ KL MN OP QR ST"
    ok_recip = encipher(encipher(msg, "QEV", plug), "QEV", plug) == msg
    #    the double-step anomaly: stepping across the middle notch (positions ADU → ...)
    ok_double = _step((0, 4, 5)) == (1, 5, 6)      # middle at notch E: left and middle both step

    # 2. structural: every Sᵢ is a fixed-point-free involution — checked at ALL 26³ states
    ok_invol = True
    for l in range(A):
        for m in range(A):
            for r in range(A):
                s = state_perm((l, m, r))
                if any(s[s[c]] != c or s[c] == c for c in range(A)):
                    ok_invol = False

    # 3. plugboard invariance — 60 settings × 5 plugboards (incl. 10 leads), and even multiplicities
    plugs = ["", "AB", "AB CD EF", "AZ BY CX DW EV", plug]
    ok_inv, ok_even, n = True, True, 0
    for i in range(60):
        st = ((i * 5) % A, (i * 7 + 3) % A, (i * 11 + 1) % A)
        base = characteristic(st, "")
        for pb in plugs:
            if characteristic(st, pb) != base:
                ok_inv = False
            n += 1
        if not all(all(t.count(L) % 2 == 0 for L in set(t)) for t in base):
            ok_even = False

    # 4. the catalogue finds a secret setting from a plugboard-scrambled observation
    secret = (3, 17, 9)
    seen = characteristic(secret, plug)
    hit = build_up({"characteristic": seen})
    ok_cat = _name(secret) in hit["matches"] and hit["cost"] == A ** 3
    # the catalogue is exhaustive: every start lands in exactly one class
    cat = catalogue()
    ok_partition = sum(len(v) for v in cat.values()) == A ** 3

    try:
        build_up({})
        ok_refuse = False
    except AscentNotFree:
        ok_refuse = True

    return {"ok": all([ok_kat, ok_recip, ok_double, ok_invol, ok_inv, ok_even, ok_cat,
                       ok_partition, ok_refuse]),
            "known_answer_AAAAA_BDZGO": ok_kat, "reciprocal_with_10_plugs": ok_recip,
            "middle_notch_double_step": ok_double,
            "all_17576_states_are_derangement_involutions": ok_invol,
            "plugboard_independent": ok_inv, "checks_run": n,
            "even_cycle_multiplicities": ok_even,
            "catalogue_finds_secret": ok_cat, "catalogue_matches_for_secret": hit["n_matches"],
            "distinct_characteristics": hit["distinct_characteristics"],
            "catalogue_partitions_all_settings": ok_partition,
            "refuses_without_characteristic": ok_refuse}


if __name__ == "__main__":
    print(descend("QEV", plugboard="AB CD EF"))
    print(verify())
