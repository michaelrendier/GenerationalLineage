# The Emerger — the ascent dual of Generational Lineage

**Engine:** `engine/emerger.py` (`report_emergence`, `emerge_brackets`,
`bracket_firing_order`, `emerger_verify`). Pure stdlib, `Fraction` throughout,
float only at the output boundary. 14/14 exact self-checks.

Cody, 2026-09-01: *"factoral is the generalized, Spectral is Sedenion
focused."* This module is the generalized half. The sedenion-focused
spectrograph (SVG, prime channels) is `SedenionSpectralRelativity/emerger_spectrum.py`.
The ValaQuenta Full-Engine-Protocol build is `ValaQuenta/modules/emerger/`.

---

## Descent vs ascent

`lineage.py` runs **descent**: what built this operator or number —
`factor_lineage`, `decompose`, the two trees, the four-part tier test.
Differentiate down. Writing.

`emerger.py` runs **ascent**: given a *bracketing* of a Cayley–Dickson
algebra — an ordered partition of its imaginary units — which sub-domains does
that grouping expose, and, because each domain needs the ones under it, in what
**order** do the variables emerge. Integrate up. Reading. Spectroscopy.

## The anchor and the brackets

`e_0` (the real component) is never bracketed. It is the *tilt to the i axis* —
the fixed reference each imaginary group is paired against. A bracketing
partitions `{1..dim-1}`; each group `G`, with the anchor, spans
`span({e_0} ∪ G)`, classified by closure:

| `|G|`, closed? | domain |
|---|---|
| 1 | ℂ |
| 3 | ℍ |
| 7 | 𝕆 |
| any, not closed | **FRAGMENT** — a linear subspace, not a subalgebra; where zero divisors live |

`bracketings_for(dim)`: `dim = 16` → the five canonical sedenion brackets;
any other `2^k` → the nested `ℂ ⊂ ℍ ⊂ 𝕆 ⊂ …` shell chain.

The five sedenion brackets and what each lets emerge:

| bracket | emerges | descends from |
|---|---|---|
| `{1:15}` | Re, `N`, conj, inverse — grades the algebra | the CD grading |
| `{2:14}` | the pointer `z = x₀ + i·x₈`; `\|z\| − Ω_ZS` — the read head | `{1:15}` |
| `{8:8}` | `\|a\|−\|b\|` = distance from the ZD equator; sheet; `J₂` = L vs R | `{1:15}` |
| `{4:4:4:4}` | four SU(2) phases; `Σtilt` = net work around the loop (`= 0 ⇔ σ = ½`) | `{8:8}` |
| `{4:8:4}` | dominant gain class 0 / 1 / √2 — multiplicative role | `{1:15}` + `{4:4:4:4}` |

## Firing order

Load-bearing. `{1:15}` before `{2:14}`, `{8:8}`, `{4:8:4}`; `{8:8}` before
`{4:4:4:4}` before `{4:8:4}`. **4 of the 120 permutations are legal**; the
canonical order is one.

σ_RB picks the entry point: `Σtilt` → rational squash → `⌊12·phase⌋ mod 5`.
The 12 is `lcm(4 d* faces, 3 Lambert-W faces)` — the same "no camshaft" clock
as `add_scale_sign`'s `CAMSHAFT` / `BRACKET` firing-order defect, at sedenion
scale.

## Exact results (`report_emergence()`)

- `is_zero_divisor(x)` = rank-deficiency of `Lₓ` (Gaussian elimination over
  `Fraction`). `on_zd_equator(x)` = purely imaginary + norm-balanced across the
  CD-double boundary — the fixed set of the `J_red ↔ J_blue` swap.
- `e₁+e₁₀` → zero divisor **and** on the ZD equator; `e₁+e₂` → neither;
  `e₀` → unit. `domain_of`: `{1}`=ℂ, `{1,2,3}`=ℍ, `{1..7}`=𝕆, `{1,5,9}`=FRAGMENT.
- `Σaxis = 0` identically (Oblique-Gear T1). σ_RB rotates the firing order.

**Finding, surfaced not hidden:** a σ_RB phase can select a firing order that
is *not* dependency-legal (`e₁+e₁₀` phases into `{2:14}` before `{1:15}`). The
clock names the entry; the engine reports the illegality rather than snapping
to the nearest legal order.

## Related

`engine/lineage.py` (descent) · `engine/spectral.py` ("spectral analysis IS
factoral decomposition") · `engine/add_scale_sign.py` (`CAMSHAFT` / `BRACKET`)
· `ValaQuenta/modules/box_kite` (the exact PSL(2,7) ZD geometry; G₂ is the
blow-up) · `ValaQuenta/modules/emerger` · `SedenionSpectralRelativity/emerger_spectrum.py`.
