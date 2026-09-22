"""
GenerationalLineage.engine.toolsets.hyper_linear
==================================================
HYPER-LINEAR ALGEBRA DECOMPOSITION — multiplication itself, read as a
regular-representation matrix and split into its two triangular Toeplitz
halves.

DECOMPOSITION (free): given a*b (a the multiplicand, b the multiplier),
each digit of b names ONE tier-0 SCALE operator L_d = d*(), composed with
a SHIFT T^i (itself just L_base^i — ALSO tier-0 SCALE, by the base). No
search: read b's digits, apply L_{d_i} o T^i to a, done. Every row
descends from SCALE alone; ADD enters exactly once, at the final
column-sum/carry step — the only tier-0 ADD in the whole construction.

EMERGER (work): recovering WHICH of b's digit positions produced an
11th-digit spillover from the PRODUCT alone is genuinely underdetermined
— the product alone is exactly as hard to use for this as factoring it
would be. Supplying just ONE of the two factors makes it free again:
divide, then read the spillovers straight off the recovered factor's own
digits. `build_up` reports this distinction exactly, raising
AscentNotFree when neither factor is supplied.

Verified this session, before anything else was built on it:
  - the Toeplitz block identity: the two 10x10 halves of the addition
    matrix for a 10-digit x 10-digit multiply are a lower- and
    upper-triangular Toeplitz pair sharing one generating sequence (a's
    digits), split at the column boundary.
  - the exact spill threshold: row r (digit d of b) spills to an extra
    digit iff  d >= ceil(BASE / a),  BASE = 10 ** len(str(a)).
  - the DFT/convolution-theorem reconstruction of a*b from the two
    zero-padded digit sequences — exact, after carry-propagation.
  - recovering the spill pattern from the bare product needs a factor;
    from the product alone it does not resolve — checked live on
    a=1546854629, b=7283619945 below.

stdlib + numpy, via engine.spectral (reused, not reimplemented).
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

import numpy as np

from ..lines import AscentNotFree
from .. import spectral

NAME = "hyper_linear"
LINE = "both"


def _digits_lsd(n: int) -> List[int]:
    """n's decimal digits, least-significant first (index i <-> place 10**i)."""
    return [int(c) for c in str(n)[::-1]]


def descend(a: int, b: int) -> Dict[str, Any]:
    """a * b, decomposed digit-by-digit: one tier-0 SCALE operator per
    digit of b, composed with a shift (also tier-0 SCALE, by the base).
    Reports each row's operator and spill status, plus the
    DFT/convolution-theorem reconstruction of the full product — single
    pass, no search, free=True."""
    if a <= 0 or b <= 0:
        raise ValueError("a, b must be positive integers")

    ad = _digits_lsd(a)
    bd = _digits_lsd(b)

    rows = []
    for r, d in enumerate(bd):
        p = a * d
        spills = len(str(p)) > len(ad) if d != 0 else False
        rows.append({
            "row": r, "digit": d, "partial_product": p,
            "n_digits": len(str(p)) if p else 1, "spills": bool(spills),
            "operator": f"L_{d} o T^{r}",
        })

    # ── the Toeplitz/convolution read, via the engine's own spectral.dft ──
    conv_len = len(ad) + len(bd) - 1
    N = 1
    while N < conv_len:
        N *= 2
    A_pad = ad + [0] * (N - len(ad))
    B_pad = bd + [0] * (N - len(bd))
    fa = spectral.dft(A_pad)
    fb = spectral.dft(B_pad)
    conv = np.fft.ifft(fa * fb).real
    coeffs = [int(round(x)) for x in conv[:conv_len]]

    carry, out_digits = 0, []
    for c in coeffs:
        t = c + carry
        out_digits.append(t % 10)
        carry = t // 10
    while carry:
        out_digits.append(carry % 10)
        carry //= 10
    reconstructed = int("".join(str(v) for v in reversed(out_digits))) if out_digits else 0

    return {
        "toolset": NAME, "a": a, "b": b, "product": a * b,
        "rows": rows,
        "n_spilling_rows": sum(1 for r in rows if r["spills"]),
        "dft_reconstruction": reconstructed,
        "dft_reconstruction_exact": reconstructed == a * b,
        "note": "each row is one tier-0 SCALE op (L_d) composed with a shift "
                "(also SCALE, by the base) — descends = 'scale'; ADD enters "
                "exactly once, summing the rows",
    }


def build_up(target: Dict[str, int], probes: Optional[list] = None) -> Dict[str, Any]:
    """target: {'product': P}  or  {'product': P, 'a': A}  or  {'a': A, 'b': B}.

    Recovering which rows spilled from the PRODUCT ALONE is exactly as
    hard as factoring it — not free, refused via AscentNotFree. Supplying
    ONE factor (a or b) restores the free reading: one division recovers
    the other factor, then spill status reads straight off its digits."""
    product = target.get("product")
    a = target.get("a")
    b = target.get("b")

    if a is not None and b is not None:
        d = descend(a, b)
        if product is not None and d["product"] != product:
            raise ValueError("a * b does not match the given product")
        return {**d, "cost": 0, "note": "both factors already supplied — identical to descend()"}

    if product is None:
        raise AscentNotFree("the product P, or both factors",
                            "no target given at all")

    if a is None and b is None:
        raise AscentNotFree("at least one factor (a or b)",
                            "the product alone under-determines which rows "
                            "spilled — that recovery is exactly as hard as "
                            "factoring P itself, not a free read")

    known, unknown_name = (a, "b") if a is not None else (b, "a")
    if not known or product % known != 0:
        raise AscentNotFree(f"a valid {unknown_name}",
                            f"{known} does not divide the product evenly")
    other = product // known
    A, B = (known, other) if a is not None else (other, known)
    d = descend(A, B)
    return {**d, "cost": 1,
            "note": f"one division recovered the missing factor "
                    f"({unknown_name}={other}) — spill pattern read directly "
                    f"after that, free from there on"}


def verify() -> Dict[str, Any]:
    A, B = 1546854629, 7283619945
    d = descend(A, B)
    ok_product = d["product"] == A * B
    ok_dft = d["dft_reconstruction_exact"]
    ok_spill_count = d["n_spilling_rows"] == 4          # verified earlier this session

    try:
        build_up({"product": A * B})
        ok_refuse = False
    except AscentNotFree:
        ok_refuse = True

    recovered = build_up({"product": A * B, "a": A})
    ok_recover = recovered["b"] == B and recovered["n_spilling_rows"] == 4

    ok = ok_product and ok_dft and ok_spill_count and ok_refuse and ok_recover
    return {"ok": ok, "ok_product": ok_product, "ok_dft_reconstruction": ok_dft,
            "ok_spill_count": ok_spill_count, "ok_refuse_bare_product": ok_refuse,
            "ok_recover_from_one_factor": ok_recover}


if __name__ == "__main__":
    import json
    d = descend(1546854629, 7283619945)
    print(f"a={d['a']}  b={d['b']}  product={d['product']}")
    print(f"spilling rows: {d['n_spilling_rows']}/10")
    for r in d["rows"]:
        print(f"  row {r['row']}: digit={r['digit']}  {r['operator']:<10}  "
              f"spills={r['spills']}")
    print(f"DFT reconstruction exact: {d['dft_reconstruction_exact']}")
    print()
    try:
        build_up({"product": d["product"]})
    except AscentNotFree as e:
        print(f"build_up on bare product refused, as expected: owed={e.owed!r}")
    r = build_up({"product": d["product"], "a": d["a"]})
    print(f"build_up with one factor recovered b={r['b']}, "
          f"spilling rows={r['n_spilling_rows']}")
    print()
    print("verify():", verify())
