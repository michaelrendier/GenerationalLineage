# Units and the Equation Index

**`PW16`, 2026-08-25.** A fourth domain for this repo's own
factoral-decomposition discipline. Every relation before this one
decomposed either a **number** (`factor_lineage`: prime/composite, the Two
Trees) or a **process** (`pathway_decomposition`: an operator DAG, RSA
CRT-decrypt as the control case). This page's engine decomposes a
**physical unit** — same discipline, third object, not a new mechanism.

Cody, opening the thread: *"information lives in the units...units can
'spectrally show' direct generational lineage...mitochondrial lineage if
you will...the 'units' are directly 'how the geometries hold the
permutation'...the units will identify exactly what equations
matter...they are the equation index."*

---

## The claim, made precise

A unit is a point in a 7-axis lattice — the SI base dimensions
(`kg,m,s,A,K,mol,cd`, the leaves). Named compounds (Newton, Joule, Watt,
Tesla, ...) are composites with an exact, computable lineage back to them.
Multiplying quantities **adds** exponent vectors; dividing **subtracts**;
cancellation is a component landing on zero. This is standard dimensional
analysis (Buckingham Pi, 1914) — what's new here is treating it as a
first-class object in this engine's own `_record`/`Status` self-test
machinery, the same way `factor_lineage` and `pathway_decomposition`
already are.

## The functions

```python
from engine import SI_BASE, unit_vector, unit_mul, unit_div, unit_lineage_decompose

MOL, LITER = unit_vector((0,0,0,0,0,1,0), name='mol'), unit_vector((0,3,0,0,0,0,0), name='L')
concentration = unit_div(MOL, LITER)          # mol/L
recombined = unit_mul(concentration, LITER)   # cancels back to mol, exactly
```

## The lineage table — a real generational tree

```
N   = kg¹m¹s⁻²                     ← kg, m, s
J   = N¹m¹                         ← N, m
W   = J¹s⁻¹                        ← J, s
V   = W¹A⁻¹                        ← W, A
Wb  = V¹s¹                         ← V, s
T   = Wb¹m⁻²                       ← Wb, m
```

Six generations from Tesla down to the three leaves it actually touches
(`kg, m, s, A`) — traced automatically by `unit_lineage_decompose`, and
checked (not assumed) to recombine to Tesla's own declared vector.

## The bug this engine found in itself — kept in the record

`PW16`'s first draft stored each composite's `lineage` as bare parent
names (`('Wb', 'm')` for Tesla) and always **added** the parents' traced
vectors, regardless of whether the real relationship was a multiply or a
divide. Running the test immediately failed all six named units — Tesla is
`Wb/m²`, not `Wb·m`. Fixed by storing signed `(parent, power)` pairs per
lineage step. Per this project's own §6 discipline (three kinds of wrong:
CODE fault, MATHS fault, METHOD error) — this was a genuine CODE fault,
caught the moment the self-test ran, not a maths disagreement and not
hidden from the record once fixed.

## The equation index — units as "word possibilities"

The exact structural parallel to `wordnet_boxkite.context_vector`
(`VAPMIP`, Phase 31): a word's context vector narrows it to candidate
WordNet senses; a quantity's dimension signature narrows it to candidate
physical laws.

```
(1,2,-2,0,0,0,0)   [Joule]   ->  E=½mv², E=mgh, W=F·d, E=½kx², Q=mcΔT
(1,1,-2,0,0,0,0)   [Newton]  ->  F=ma, F=mg, F=kx, F=mv²/r
(1,0,-2,-1,0,0,0)  [Tesla]   ->  B=Φ/A, F=qvB
```

Same move this repo already runs on numbers (a factorisation narrows N to
its prime lineage) and processes (a pathway decomposition narrows an
algorithm to its real operator DAG) — narrowing a large space to a short,
checkable list from structure alone, not from inspecting the target
directly.

## Units are a geometry — the same finding as `0_RB`, one domain over

A unit vector carries no numeric content and computes nothing on its own —
exactly the "geometry does no work" finding already established for `∅_RB`
and `σ_RB` elsewhere in this project's record — but it is precisely what
decides which recombinations of content are legal. `7.2 J + 3.1 kg` is
illegal; `7.2 J / 3.1 s` is legal and lands on power, `(1,2,-3,0,0,0,0)`,
automatically.

## Report

| operation | tier | descends from | status |
|---|---|---|---|
| `unit_vector`/`unit_mul`/`unit_div` | 0 (ADD/SCALE on the exponent lattice) | tier-0 ADD, SCALE | HOLDS |
| `unit_lineage_decompose` | 3 (a count of composed exponents) | the SAME discipline as `factor_lineage`/`pathway_decomposition` | HOLDS, 11/11 named compounds, engine 44/44 |
| `EQUATION_INDEX` lookup | 3 (a derived narrowing, not a primitive) | the exponent vector itself | HOLDS on the 16 signatures currently tabled |

**No new generator required.** Units are a third — now, with
`ValaQuenta/modules/units/`'s `EQUATION_INDEX`, a fourth-domain-adjacent —
application of decomposition machinery this engine already had, not a new
mechanism.

## Related

`ValaQuenta/wiki/units.md`, `Ainulindale/wiki/97_units_as_the_equation_index.md`
(same day, sibling pages, independent ports per this project's per-repo
self-containment convention); `PtolemyDesktop/Archimedes/UnitVector.py`
(the original string-list-based design this engine's vector arithmetic was
checked against); `The-Generational-Lineage-Engine.md` §4.11 (this repo's own
engine-usage documentation for `PW16`).

---

## As a toolset (the two lines)

`engine/toolsets/units.py` · line: **both**.

- **descend (free):** a compound unit → its exponent vector over the 7 SI axes
  `(kg, m, s, A, K, mol, cd)`. Exact vector arithmetic. `N` →
  `(1, 1, -2, 0, 0, 0, 0)`. `cost = 0`.
- **build_up (work):** a bare exponent vector → the named physical laws of that
  dimension, by scanning the law index. `cost` = entries scanned.

```python
from engine import line_descend, line_build_up
line_descend('units', 'N')          # vector (1,1,-2,0,0,0,0)
line_build_up('units', 'J')         # candidate_laws: ['E = 1/2 m v^2', 'E = m c^2', ...]
```
