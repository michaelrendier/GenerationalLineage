# ping — the Emerger–Lineage unification

**Engine:** `engine/ping.py` (`ping`, `counter_operator_laplacian`,
`emerger_lineage_unify`, `report_ping`, `flat_diagram_depth_note`).
stdlib + numpy. Every number CALCULATED and reproducible.

Cody, 2026-09-01: *"can we ping 0 from a Modulus? ... using the RSA hardness
counter-operators ... will it draw a path from modulus to 0 along a
bifurcation?"*

---

## The two hop axes, merged

| axis | engine | move | needs factors? |
|---|---|---|---|
| **operator hop** (descent) | `lineage.py` — the RSA-hardness **counter-operators** | apply a counter-operator; if it fires, N → its primes → 0_RB | the SCALE-÷ step does |
| **bracket hop** (ascent) | `emerger.py` | bracket N's 16-vector five ways in σ_RB firing order | **no** — runs free on any modulus |

`ping(N, e=None, corpus=None, order=None, budget=…)` hops through the
counter-operators permutatively and returns: `factored`, `factors`, `regime`,
`path`, the `bracket_map` (free), the `laplacian` summary, and the
`flat_diagram_depth` note.

## The RSA-hardness counter-operators

Each counters one hardness and sits at one point of
`TuringStack/references/logistic_bifurcation_RSA.png` v2:

| counter-operator | counters | bifurcation point | cost |
|---|---|---|---|
| **Fermat** (`N = a²−b²`) | `p ≈ q` | the **r = 3 pitchfork** | `O(|p−q|²/√N)` |
| **trial division** | `q` small | the floor branch | `O(spf N)` |
| **Pollard p−1** | `p−1` smooth | a smooth-tangency window | `O(B log B)` |
| **Williams p+1** | `p+1` smooth | a smooth-tangency window | `O(B log B)` |
| **ECM** (Lenstra) | a mid-size factor | the small-`x` branch | `L_p[1/2]` |
| **Wiener** (CF of `e/N`) | `d` small | off-diagram (key structure) | `O(log N)` |
| **batch GCD** | a shared prime | off-diagram (RNG failure) | `O(#corpus)` |
| **Coppersmith / LLL** | half the bits of `p` known | window entry tangency | poly (stub — note only) |
| **GNFS / Shor** | none of the above | chaotic bulk / the rotation number | `L_N[1/3]` / quantum |

**The first bifurcation is the ± distinction.** The `r = 3` pitchfork
(period-1 → period-2) *is* SIGN: the sheet, `±√N`, the sign-locked sets
`{+p,+q}` and `{−p,−q}`. That is why Fermat lives there — `N = a²−b²` is the
difference of squares, the ± structure itself.

## The counter-operator Laplacian

`counter_operator_laplacian()` builds the graph (edge = counters an adjacent
regime, or hands off) and returns `L = D − A`, its spectrum, algebraic
connectivity, and the Fiedler cut (value-space methods | key-ecosystem
attacks).

**`L` is symmetric — so its spectrum is permutation-invariant.** The regime
**verdict is order-independent**; only the **schedule** (how many probes fire
before the one that works) is order-sensitive. An order-independent Laplacian
is a **classifier, not a pathfinder**: it names the regime, never the
factorisation.

That is the answer to *"will it draw a path from modulus to 0 along a
bifurcation?"* — **yes, for a modulus in a broken regime** (the counter-op
that fires is the path; it lands on the pitchfork for `p≈q`, the floor branch
for small `q`, a smooth window for `p∓1`). **No, for a properly generated
modulus** — `regime = "floor — GNFS/Shor only"`, and GNFS is a bulk sample,
not a bifurcation path.

## The flat diagram carries a TON of information out of view

`flat_diagram_depth_note(N)`: the bifurcation diagram is a **2-D projection**.
On it, N's column shows `~π(√N)²` apparent `p × q` meetings; **exactly one is a
real crossing** (`pq = N`), the rest are **passes** — two prime branches
overlapping in projection with `pq ≠ N`. The distinguishing coordinate is the
projected-out **depth**: the product value, equivalently `ln(q/p)` — the
palindrome centre, the erased coordinate. Reconstructing depth for the
apparent crossings **is** the operator hop = factoring.

For a 69-bit N: `~2.8×10¹⁷` passes, one crossing. The flatness is where the
information went.

## Worked (`report_ping`)

- `3233 = 61·53` → trial division fires at 53 (regime: `q small`).
- `72326039160604451 = 268435459·269435489` (`|p−q| ≈ 10⁶`) → Fermat fires
  (regime: `p ≈ q`).
- A balanced modulus with `p−1` smooth → Pollard p−1 fires (regime:
  `p−1 smooth`). A modulus with none of the above → the floor.

## `emerger_lineage_unify(N)`

Walks both axes for one N: the operator hop's `modulus → 0_RB` path
(`÷ each prime → 1 → Mingling`) and the bracket hop's firing order + ZD-equator
/ gain readout, plus the `ping` regime and the flat-diagram depth. The
descent–ascent pair in one call.

## Honest scope

`ping` is a **complete regime classifier**: it factors any modulus in a broken
regime and honestly names the floor for one that is not. It is not an attack
on the hardness assumptions — RSA is the zero-overhead corner of this map.
See `../README.md` §4.15 and `Sedenion-Factoral-Relativity.md`.
