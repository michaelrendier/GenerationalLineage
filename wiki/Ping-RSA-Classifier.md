# 4.15 The Emerger–Lineage unification — ping 0 from a modulus  `[TUTORIAL — RSA regime classifier]`

`engine/ping.py` · *Tutorial:* [`09_ping`](../examples/09_ping.py). Full write-up:
[`wiki/Ping-and-the-Counter-Operator-Laplacian.md`](Ping-and-the-Counter-Operator-Laplacian.md).

The two structural hop axes, merged: the **operator hop** (descent — the RSA
hardness **counter-operators**: Fermat ← `p≈q`, trial division ← `q` small,
Pollard p−1 ← `p−1` smooth, Williams p+1, ECM, Wiener, batch GCD, Coppersmith,
and GNFS/Shor as the floor) and the **bracket hop** (ascent — the Emerger,
which runs free on any modulus's embedding, no factors needed).

```python
from engine import ping, counter_operator_laplacian, emerger_lineage_unify, report_ping

report_ping(3233)                     # 61·53 -> trial division fires at 53
ping(72326039160604451)               # |p-q| ~ 1e6 -> Fermat fires (regime: p ~ q)
N, e = 3233, 17
r = ping(N, e=e, corpus=[5183])       # -> {factored, factors, regime, path, bracket_map,
                                      #     laplacian, flat_diagram_depth}
emerger_lineage_unify(N)              # both axes: modulus -> 0_RB path + bracket firing order
```

- **`ping(N)`** hops the counter-operators permutatively. Returns 0_RB — factors
  N — **iff N sits in one broken regime**. For a properly generated modulus,
  `regime = "floor — GNFS/Shor only"`. The bracket-hop structural map comes back
  either way.
- **The first bifurcation is the ± distinction.** The `r = 3` pitchfork
  (period-1 → period-2) *is* SIGN — the sheet, `±√N`, `{+p,+q}` / `{−p,−q}`.
  That is why Fermat (`N = a²−b²`) lives there.
- **`counter_operator_laplacian()`** — `L = D − A` of the counter-operator
  graph. **`L` is symmetric → its spectrum is permutation-invariant → the
  regime verdict is order-independent; only the schedule is order-sensitive.**
  An order-independent Laplacian is a **classifier, not a pathfinder**: it names
  the regime, never the factorisation. So it draws a modulus→0 path *only* for a
  modulus in a broken regime.
- **`flat_diagram_depth_note(N)`** — the bifurcation diagram is a 2-D
  projection. N's column has `~π(√N)²` apparent `p×q` meetings; **exactly one is
  a real crossing**, the rest are **passes** (`pq ≠ N`). The distinguishing
  coordinate is the projected-out **depth** = `ln(q/p)`, the erased coordinate.
  Reconstructing it *is* factoring. For a 69-bit N: `~2.8×10¹⁷` passes, one
  crossing — the flatness is where the information went.

*Reading:* `ping` is a **complete regime classifier** — it factors any modulus
in a broken regime and honestly names the floor for one that is not. RSA is the
zero-overhead corner of this map: `p·q` is the whole specification, so the
inverse has no handhold.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
