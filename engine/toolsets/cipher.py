"""
GenerationalLineage.engine.toolsets.cipher
==========================================
CIPHER — the classical-cryptanalysis reads from the Code Book workbench
(`PtolemyDesktop/Kryptos/analysis.py`, "the methods to break each"), ported as
a toolset. Self-contained: stdlib only, no Kryptos import.

WHICH DIRECTION SERVES FACTORAL DECOMPOSITION
--------------------------------------------
Every method has two directions — text → cipher (encrypt) and cipher →
analysis (break). Breaking a classical cipher IS decomposition: you recover the
hidden generator (period, key length, substitution, partition) from the output
by deductive sieving. So **cipher → analysis is the descent (free) direction**
for almost all of them; **text → cipher is the emerger (work) direction** — a
choice of key.

    method            factoral-useful direction                     line
    ---------------   -----------------------------------------      ------------
    Kasiski          cipher→analysis IS factoral decomposition —    descend: GCD-
                     the period is the GCD of the repeat-distance   vote the gap
                     multiset (`gcd_is_the_detector`, on gaps)      multiset
    Index of         cipher→analysis — the CONTINUOUS estimate of   descend: the
    Coincidence      the same period Kasiski gets DISCRETELY: the   Friedman
                     Smith-chart / gasket pair on one quantity,     column-IoC
                     the period                                     signal
    frequency / χ²    cipher→analysis — the FACET classifier: flat   descend:
                     spectrum ⇒ polyalphabetic (period > 1),        mono / poly /
                     shifted spike ⇒ monoalphabetic (a relabel,    plaintext
                     tier-0 SIGN), aligned spike ⇒ plaintext
    Caesar / shift   text→cipher — pure tier-0 ADD on ℤ/26; the     both: encrypt
                     break is a bounded 26-way search (the cheap    = ADD; break =
                     degenerate ascent)                             argmin χ²
    word-pattern     cipher→analysis — `pattern_signature` is       descend: the
    signature        INVARIANT under a monoalphabetic relabel;      signature
                     the signature IS the decomposition (it         quotients out
                     quotients out the alphabet)                    the alphabet
    Vowel Trowel     cipher→analysis — a spectral partition of      descend:
    (Sukhotin)       the letter-adjacency graph (the same move as   partition the
                     `noether`'s J_red / J_blue split)              adjacency graph
    transposition    text→cipher — the key length DIVIDES the       descend: the
                     ciphertext length (a factoral constraint       divisor
                     carried on the encryption side)                constraint
    Enigma key-space text→cipher — a worked PRODUCT DECOMPOSITION   descend: factor
                     of a count: 60 = 5·4·3, 17576 = 26³,          the keyspace
                     plugboard = 26!/(6! · 2⁶ · 10!) …             count's lineage

The load-bearing one is Kasiski: **period = GCD-vote of the gap multiset** is
factoral decomposition, exactly — and its continuous shadow is the IoC.

DECOMPOSITION (free): `descend(ciphertext)` — every statistic is one sweep of
the text; no key is searched.

EMERGER (work): `build_up(target, key=...)` encrypts (the choice, cost =
len(key)); or `build_up(ciphertext, period=p)` spends p·26 column trials to
recover the key. `build_up` with neither raises `AscentNotFree` — the period is
the owed constraint, and `descend()` hands it over for free.
"""
from __future__ import annotations

from collections import Counter
from math import gcd
from typing import Any, Dict, List, Tuple

from ..lines import AscentNotFree

NAME = "cipher"
LINE = "both"

A = 26
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
VOWELS = set("AEIOU")

# English single-letter frequency, percent (al-Kindi reference)
ENGLISH_FREQ = {
    "A": 8.17, "B": 1.49, "C": 2.78, "D": 4.25, "E": 12.70, "F": 2.23,
    "G": 2.02, "H": 6.09, "I": 6.97, "J": 0.15, "K": 0.77, "L": 4.03,
    "M": 2.41, "N": 6.75, "O": 7.51, "P": 1.93, "Q": 0.10, "R": 5.99,
    "S": 6.33, "T": 9.06, "U": 2.76, "V": 0.98, "W": 2.36, "X": 0.15,
    "Y": 1.97, "Z": 0.07,
}
IOC_ENGLISH = 0.0667
IOC_RANDOM = 0.0385


# ── stdlib primitives (ported compactly from Kryptos/analysis.py) ────────────
def _clean(text: str) -> str:
    return "".join(ch for ch in text.upper() if ch in ALPHABET)


def _ioc(s: str) -> float:
    n = len(s)
    if n < 2:
        return 0.0
    c = Counter(s)
    return sum(v * (v - 1) for v in c.values()) / (n * (n - 1))


def _chi2_english(s: str) -> float:
    n = len(s)
    if not n:
        return float("inf")
    c = Counter(s)
    return sum((c.get(ch, 0) - ENGLISH_FREQ[ch] / 100 * n) ** 2
               / (ENGLISH_FREQ[ch] / 100 * n) for ch in ALPHABET)


def _caesar_shift(s: str, k: int) -> str:
    return "".join(ALPHABET[(ALPHABET.index(ch) - k) % A] for ch in s)


def _best_caesar(s: str) -> Tuple[int, float]:
    best_k, best = 0, float("inf")
    for k in range(A):
        sc = _chi2_english(_caesar_shift(s, k))
        if sc < best:
            best_k, best = k, sc
    return best_k, best


def _vigenere(text: str, key: str, decrypt: bool = False) -> str:
    s, k = _clean(text), _clean(key)
    if not k:
        return s
    out, sign = [], (-1 if decrypt else 1)
    for i, ch in enumerate(s):
        shift = ALPHABET.index(k[i % len(k)])
        out.append(ALPHABET[(ALPHABET.index(ch) + sign * shift) % A])
    return "".join(out)


def _kasiski(s: str, min_len: int = 3, max_len: int = 5, max_factor: int = 30):
    """Repeated substrings → gap multiset → factor votes. `gap_gcd` is the
    strict factoral answer (GCD of every gap); `votes` is the noise-robust
    version (a coincidental repeat drags the raw GCD to 1)."""
    detail: Dict[str, List[int]] = {}
    for L in range(min_len, max_len + 1):
        seen: Dict[str, int] = {}
        for i in range(len(s) - L + 1):
            seg = s[i:i + L]
            if seg in seen:
                detail.setdefault(seg, []).append(i - seen[seg])
            seen[seg] = i
    gaps = [g for gs in detail.values() for g in gs]
    votes: Counter = Counter()
    for g in gaps:
        for f in range(2, min(g, max_factor) + 1):
            if g % f == 0:
                votes[f] += 1
    gap_gcd = 0
    for g in gaps:
        gap_gcd = gcd(gap_gcd, g)
    return votes.most_common(), gap_gcd, len(gaps)


def _ioc_by_period(s: str, max_period: int) -> List[Tuple[int, float]]:
    out = []
    for p in range(1, max_period + 1):
        cols = [s[i::p] for i in range(p)]
        iocs = [_ioc(c) for c in cols if len(c) > 1]
        out.append((p, sum(iocs) / len(iocs) if iocs else 0.0))
    return out


def _pattern_signature(word: str) -> str:
    """'HELLO' -> '12334'. Invariant under any monoalphabetic relabel — the
    residue of the alphabet quotiented out."""
    seen: Dict[str, int] = {}
    out, nxt = [], 1
    for ch in _clean(word):
        if ch not in seen:
            seen[ch] = nxt
            nxt += 1
        out.append(str(seen[ch]))
    return "".join(out)


def _sukhotin(s: str) -> Tuple[List[str], List[str]]:
    """Sukhotin's vowel/consonant split — the spectral partition of the letter
    adjacency graph. Language-agnostic, no frequency table."""
    letters = sorted(set(s))
    if not letters:
        return [], []
    idx = {ch: i for i, ch in enumerate(letters)}
    m = [[0] * len(letters) for _ in letters]
    for a, b in zip(s, s[1:]):
        if a != b:
            m[idx[a]][idx[b]] += 1
            m[idx[b]][idx[a]] += 1
    row = [sum(r) for r in m]
    remaining = set(range(len(letters)))
    vowels: List[int] = []
    while True:
        cand = max((i for i in remaining), key=lambda i: row[i], default=None)
        if cand is None or row[cand] <= 0:
            break
        vowels.append(cand)
        remaining.discard(cand)
        for j in remaining:
            row[j] -= 2 * m[cand][j]
    v = [letters[i] for i in vowels]
    return v, [ch for ch in letters if ch not in set(v)]


# ── the toolset contract ────────────────────────────────────────────────────
def descend(ciphertext: str, max_period: int = 16) -> Dict[str, Any]:
    """The FREE cryptanalytic read — one sweep per statistic, no key searched.
    The period is the GCD-vote of the repeat-distance gaps: factoral
    decomposition of the gap multiset."""
    s = _clean(ciphertext)
    ioc = _ioc(s)

    votes, gap_gcd, n_gaps = _kasiski(s)
    kasiski_period = next((f for f, _ in votes if 1 < f <= max_period), None)

    iocbp = _ioc_by_period(s, max_period)
    ioc_period = max(range(2, max_period + 1),
                     key=lambda p: dict(iocbp).get(p, 0.0)) if len(s) > max_period else None

    best_k, best_chi2 = _best_caesar(s)
    if ioc >= 0.060:
        if best_k == 0 and best_chi2 < 0.5 * _chi2_english(_caesar_shift(s, 13)):
            facet = "plaintext / single-alphabet — frequency analysis applies directly"
        else:
            facet = ("monoalphabetic — single alphabet (Caesar/substitution/"
                     "transposition); best Caesar shift %d" % best_k)
    elif ioc < 0.052:
        facet = "polyalphabetic — period > 1; split into columns, solve each as Caesar"
    else:
        facet = "borderline — short text, or period near 1"

    period = kasiski_period or ioc_period
    toks = []
    for t in dict.fromkeys(_clean(w) for w in ciphertext.upper().split()):
        if t and t not in toks:
            toks.append(t)
        if len(toks) >= 6:
            break
    vowels, consonants = _sukhotin(s)

    return {
        "toolset": NAME, "n_letters": len(s),
        "ioc": ioc,
        "ioc_class": ("english-like (single alphabet)" if ioc >= 0.060
                      else "flat (polyalphabetic / long key)" if ioc < 0.052
                      else "borderline"),
        "kasiski": {"gap_factor_votes": votes[:8], "gap_gcd": gap_gcd,
                    "n_gaps": n_gaps, "period": kasiski_period},
        "ioc_by_period": iocbp, "ioc_period": ioc_period,
        "period": period,
        "period_agrees": (kasiski_period is not None and ioc_period is not None
                          and kasiski_period == ioc_period),
        "best_caesar": {"shift": best_k, "chi2": best_chi2},
        "facet": facet,
        "pattern_signatures": {t: _pattern_signature(t) for t in toks},
        "vowel_partition": {"vowels": vowels, "consonants": consonants},
        "note": "period = GCD-vote of the repeat-distance multiset — the "
                "cipher→analysis direction IS factoral decomposition",
    }


def build_up(target: str, period: int | None = None,
             key: str | None = None) -> Dict[str, Any]:
    """The WORK direction.

    key given    → ENCRYPT `target` (plaintext) with `key` (Vigenère). The pure
                   emergence: a choice of key. cost = len(key).
    period given → RECOVER the key of `target` (ciphertext) at that period, by
                   solving each of the `period` columns as a Caesar shift
                   (χ² argmin), then decrypt. cost = period · 26 column trials.
    neither      → AscentNotFree: the period is the owed constraint, and
                   descend() factors it out of the gaps for free.
    """
    if key is not None:
        k = _clean(key)
        if not k:
            raise ValueError("key has no letters")
        ct = _vigenere(target, k)
        return {"toolset": NAME, "direction": "text->cipher (encrypt)",
                "key": k, "ciphertext": ct, "cost": len(k),
                "note": "encryption is the emerger choice — one key, applied"}

    if period is None:
        raise AscentNotFree(
            "a period (or a key)",
            "descend() gets the period from the repeat-distance gaps for free — "
            "pass it here to spend the work on column key-recovery")

    s = _clean(target)
    if period < 1:
        raise ValueError("period must be >= 1")
    recovered = []
    for i in range(period):
        col = s[i::period]
        best_k, best = 0, float("inf")
        for kk in range(A):
            sc = _chi2_english(_caesar_shift(col, kk))
            if sc < best:
                best_k, best = kk, sc
        recovered.append(ALPHABET[best_k])
    key_out = "".join(recovered)
    return {"toolset": NAME, "direction": "cipher->key (constrained ascent)",
            "period": period, "key": key_out,
            "plaintext": _vigenere(s, key_out, decrypt=True),
            "cost": period * A,
            "note": "the period was the owed constraint; %d column trials" % (period * A)}


def verify() -> Dict[str, Any]:
    plain = ("WE HOLD THESE TRUTHS TO BE SELF EVIDENT THAT ALL MEN ARE CREATED "
             "EQUAL THAT THEY ARE ENDOWED BY THEIR CREATOR WITH CERTAIN "
             "UNALIENABLE RIGHTS THAT AMONG THESE ARE LIFE LIBERTY AND THE "
             "PURSUIT OF HAPPINESS") * 2
    ct = _vigenere(plain, "LIBERTY")                       # period 7

    d = descend(ct)
    ok_period = d["kasiski"]["period"] == 7 or \
        7 in [f for f, _ in d["kasiski"]["gap_factor_votes"]]
    ok_ioc = d["ioc"] < 0.052 and "polyalphabetic" in d["facet"]

    b = build_up(ct, period=7)
    ok_break = b["key"] == "LIBERTY" and b["plaintext"] == _clean(plain)

    e = build_up(plain, key="LIBERTY")
    ok_enc = e["ciphertext"] == ct and e["cost"] == 7

    ok_sig = (_pattern_signature("HELLO") == "12334"
              and _pattern_signature("PEOPLE") == "123142")

    shifted = _vigenere("THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG" * 4, "D")
    ok_caesar = _best_caesar(shifted)[0] == 3               # key 'D' = shift 3

    ok_iocval = abs(_ioc(_clean("THE QUICK BROWN FOX" * 30)) - IOC_ENGLISH) < 0.02

    try:
        build_up(ct)
        ok_refuse = False
    except AscentNotFree:
        ok_refuse = True

    return {"ok": all([ok_period, ok_ioc, ok_break, ok_enc, ok_sig, ok_caesar,
                       ok_iocval, ok_refuse]),
            "kasiski_period_7": ok_period, "ioc_polyalphabetic": ok_ioc,
            "break_recovers_key": ok_break, "encrypt_round_trips": ok_enc,
            "pattern_signature_invariant": ok_sig, "caesar_argmin": ok_caesar,
            "ioc_english_value": ok_iocval, "refuses_without_period": ok_refuse}


if __name__ == "__main__":
    import json
    _plain = ("WE HOLD THESE TRUTHS TO BE SELF EVIDENT THAT ALL MEN ARE "
              "CREATED EQUAL") * 3
    _ct = _vigenere(_plain, "LIBERTY")
    print(json.dumps(descend(_ct), indent=2, default=str))
    print(build_up(_ct, period=7))
    print(build_up(_plain, key="LIBERTY"))
    print(verify())
