---
name: generational-lineage
description: Track the generational lineage of every operation in a calculation and watch for emergent geometries, decomposing against the Two Trees domain. Use when doing ANY mathematical, physical, or structural derivation in this project — factoring, decomposing operators, checking whether a named "geometry" is primitive or derived, deciding whether a result is a discovery or a restatement, or when the user asks to "watch for emergence", "run the lineage", "decompose this", or "is this a new operator".
version: 0.1.0
---

# Generational Lineage

Every operation descends from something. Track the descent, and emergence
becomes visible instead of surprising.

Built from measurements in the VAPMIP session of 2026-08-18. Everything stated
as a number here was computed, not asserted.

## On the name — deliberately multivalent (Cody, 2026-08-28)

"Generational" carries **four** live senses here, on purpose, and the engine
uses all of them. Do not collapse it to just the first:

1. **Descent / lineage** — "grows out of", birth → death, ancestors →
   descendants. `root_irreducible` walks the ancestry; "descends from"; the
   factor tree.
2. **Generating set** (algebra) — ADD, SCALE, SIGN *generate* Aff(1,ℝ) by
   composition; `decompose(op)` answers "which generators is this built from".
   This is the load-bearing mathematical sense.
3. **Generator = code iterator** — a `yield`-ing, state-holding, paused
   computation that resumes. `factor_lineage` recurses, `sieve_lineage` marches
   pass-by-pass, `MindsEyeRepass.step` never resets. §4's "one path to an
   operator, and the path IS that operator" is this reading — the path held in
   progress.
4. **Generation = level / cohort** — the four CD order-of-ops losses (§1); the
   factor-tree depth; the bifurcation levels.

e10 says it outright: *"Generational (operations) Lineage (order) — the same
object, words swapped."* The name is the bridge word — it sits equidistant from
descent (backward: what built this) and generation (forward: what this builds),
from the generating **set** and the **generated**, from a generator (the
process) and a generation (the snapshot), from the whole path and any single
step. Recorded in `~/.clauderc_user_provenance §1.15`.

## 0. The domain: the Two Trees

Before decomposing anything, know where it can land. **The Two Trees are the
complete domain of all numbers, however partitioned** (Ainulindale/wiki/47),
and factorisation partitions N the same way — exactly, with no remainder.

    TELPERION   B_p  BLUE   Fermat-Weierstrass   what CANNOT BE   backward, entropic
    LAURELIN    R_p  RED    Berry-Keating xp     what IS          forward, inertial
    MINGLING              J_Red = J_Blue         sigma = 1/2      the critical line

Applied to N:

    TELPERION   PRIME       defined by what it cannot be decomposed into
    LAURELIN    COMPOSITE   defined by what it IS decomposed into
    MINGLING    0 and 1     neither prime nor composite

Measured over [0, 100000]: 2 + 9,592 + 90,407 = 100,001 = every integer, zero
overlap. The partition is EXACT. And the trees counter-rotate exactly as
described — prime density and composite density sum to 1.000 at every scale,
which is `J_Red + J_Blue` conserved. The Mingling (equal brightness) sits at
n ~ 9, near e^2 = 7.389; after it Laurelin dominates forever.

**Applied to OPERATIONS — this is the map to decompose against:**

    TELPERION   IRREDUCIBLE   ADD, SCALE, SIGN, REFLECT, DILATE
    LAURELIN    COMPOSITE     chirality, factorial, vector, boundary, origin,
                              fulcrum/anchor, balance, leverage
    MINGLING    NEITHER       the identities — 0 and 1, gain 0 and gain 1

An operation must land in exactly one. If it lands in none, the domain is
incomplete and that is itself the emergence signal. If it lands in two, the
decomposition is wrong.

**Why 0 and 1 keep being the odd ones out:** they are not on either tree. They
are the hour the two trees balance — which is why they are free, why they are
tier 0, and why neither can be prime.

### 0b. The 15 are EDGES, not places

16 sedenion placeholders. The 15 "points" of PG(3,2) are the 15 nonzero XOR
DIFFERENCES between them — kinds of RELATIONSHIP, not positions. Verified:

    C(16,2) = 120 pairs;  15 differences x 8 pairs each = 120, exactly.

So the 15 exactly partition every pair of the 16 placeholders. And a spanning
tree on 16 nodes has n-1 = 15 edges, which is why **e0 is "not a point"**: in
the edge reading e0 is a NODE, the 15 are the EDGES, and the root owns none of
them. (Primer step 5 had this right: "15 edges = a dependency TREE. e0 is the
ROOT (no head, does no work)".)

A LINE is then not three places in a row — it is **three relations that
compose**: `a XOR b = c`, verified for all 35 lines. Knowing two forces the
third.

A PENCIL is the **7 ways to FACTOR one relation into two others**:

    1 = 2^3 = 4^5 = 6^7 = 8^9 = 10^11 = 12^13 = 14^15

exactly 7, because 105 incidences / 15 relations = 7.

**This is why the Two Trees domain is the factoring map.** The whole structure
is factorisation ON THE EDGES: 16 words, 15 relations, each relation decomposing
7 ways. When decomposing an operator, decompose the RELATION it expresses, not
the objects it connects.

## 1. The floor: three irreducibles

    ADD      identity 0             gain 0      Axis 1 {+,-}
    SCALE    identity 1             gain 1      Axis 2 {x,/}
    SIGN     identity even-parity   det +/-1    one bit, nothing between

**0 and 1 are free because they are the identities of the first two.** That is
why neither can be a prime, why they are tier 0 (whitespace, punctuation,
invisible delimiters), and why the gain spectrum of a zero divisor is
{0, 1, sqrt2} — two free, one irrational price.

SIGN's entire content is one bit. Measured: commutator norms in {0, 2} with
nothing between; 1848 of 1848 associator disagreements are pure sign flips;
chirality is det +/-1; legality is even-vs-odd mistakes.

## 2. The tiers

    tier 3   chirality, factorial, leverage, balance
             <- COUNTS and RATIOS of the layer below
    tier 2   vector, boundary, origin, fulcrum/anchor
             <- FIXED SETS, and products of reflect x scale
    tier 1   reflect, rotate, contract/dilate
             <- I - 2uu^T ; the {0,1,sqrt2} spectrum
    tier 0   ADD, SCALE, SIGN

REFLECT and DILATE are both primitive at tier 1 and are **independent**:
Cartan-Dieudonne gives every element of O(n) as at most n reflections
(measured: 300 random O(8), max 7), but no product of reflections can change a
length. So a spectrum splits into its reflection part (gain 1) and its dilation
part (gains != 1).

## 3. The decomposition test

For any named "geometry" or operator, ask in order:

1. **Is it a count or a ratio of something else?** -> tier 3, DERIVED.
   (chirality = parity of reflection count; factorial = order of the coordinate
   reflection group, since a transposition IS a reflection in x_i = x_j)
2. **Is it a fixed set?** -> tier 2, DERIVED.
   (fulcrum = anchor = origin = balance = ker(M - I). One computation, several
   names; the name records only what you were resisting.)
3. **Does it change length?** -> needs DILATE.
   **Does it preserve length?** -> reachable from REFLECT.
4. **Does it need an added constraint to exist?** -> COROLLARY, not a geometry.
   (leverage needs rigidity; remove rigidity and the fulcrum survives while
   leverage does not)

Only what survives all four is a candidate primitive. Say which tier you landed
on, explicitly, every time.

## 4. Order is not an operator

Two reflections give a rotation by twice the mirror angle; swapping them gives
the same rotation backwards (measured: AB != BA, AB@BA = I). Order is what
non-commutativity OF the primitives means.

So **"one path to an operator, and the path IS that operator"** is literal: a
rotation is not a thing applied, it is two reflections in sequence. When order
matters, use a POSITIONAL encoding; when it does not, use a MULTIPLICATIVE one.
Choosing wrong destroys exactly what that layer exists to carry.

## 5. Watch for emergence

Flag a POSSIBLE NEW OPERATOR when any of these appear:

- a quantity that **changes length** where only isometries were in play
- a failure that is **not one bit** (every known failure here is binary — a
  graded failure means a generator nobody has named)
- a **fixed set of the wrong dimension** for the transformations in play
- an operation that is **not reachable by composition** of what is already listed
- a **collision that unpacks** where the encoder should have made it impossible

Emergence is a branch, not a graft: the new operator must descend from the
existing ones by composition, or it is a genuinely new generator and that is a
much bigger claim requiring a much better measurement.

## 6. Three kinds of wrong — always classify

    CODE fault    the check did not run. The claim is UNJUDGED.
    MATHS fault   both sides measured, they disagree. The claim is false.
    METHOD error  code correct, maths correct, wrong approach. Invisible to both.

Gate 1 (correctness) CANNOT catch a design error, and that is correct behaviour:
correctness is about what is written. Method errors surface downstream as a
parting that should have been impossible, and **the detector is the clarifier
failing** — a natural divergence is recoverable, an unnatural one is not,
because the method destroyed the distinction upstream.

## 7. Collisions

    NATURAL     forced by rounding; both sides recoverable   -> a DISCUSSION
    UNNATURAL   the method destroyed a distinction           -> a FAULT
    ENGINEERED  induced deliberately; the disruption IS the product

**An engineered collision is evidence only if its product is measured
independently of the partners chosen to collide.** Chocolate passes (silkiness
is tasted, and could have come out flat). A residual between a defined quantity
and a derived one does not.

## 7b. STANDING DIRECTIVE — the native space

**The monad runs in spherical complex radial polar coordinates**, in testing and
production alike. Hydrogen separates there and does not separate in Cartesian at
all, so "native" means the space in which the operator is already diagonal.
Choosing another imports an off-diagonal coupling that was never in the physics.

A flat linear index is a Cartesian habit. The native form carries (r, theta, phi)
with the radial part separate from the angular, and the complex phase carried
through — never collapsed to |z|^2, which is the one step with no adjoint.

## 8. Standing checks to run before reporting

- **Is the observable on the axis that governs the outcome**, or merely
  correlated with it in this regime? (spelling vs context; provenance vs
  behaviour; colour vs assay; bubbles vs film thickness)
- **Is the reducer valid on this data?** argmax on signed currents, min|x| on
  gated data — both return confident wrong numbers. Return DEGENERATE instead.
- **Did I write the conclusion before the number came back?** Never put an
  interpretation in a print statement that will emit regardless of the result.
  This failed three times in one session; check the prose against the output.
- **Is the space small enough that exhaustive IS exact?** 128 configurations,
  yes. 972 solvent-condition combinations, no. Brute force is a diagnosis —
  it says the address does not support interpolation.
- **A control before the measurement, not after.**
- **Label the provenance of every number in the same sentence as the number.**
  SYNTHETIC tests the code. CALIBRATION tests the pipeline. Only a RESULT tests
  the hypothesis, and only with its control already run. Never report the first
  two as "results".
- **Check the file's mtime before citing it.** Anything older than 2 days is
  non-authoritative — the repositories carry tags and priority labels left by
  earlier agents that were never the author's. The rule tests the FILE, not the
  IDEA: something the author is using right now is authoritative because they
  are saying it, not because a stale file agrees.
- **Derive the parametrisation; do not guess it.** Three times in one thread a
  curve comparison came back False on a translation or a spurious phase, when
  the underlying fact was never in doubt. If a known identity fails to verify,
  suspect your own parametrisation before the mathematics.

## 9. Report format

State, for each operation used:

    operation   tier   descends from   status
    ---------   ----   -------------   ------

and end with either "no new generator required" or an explicit emergence flag
naming which of the section-5 signatures fired.
