# 3. What this engine was built to do

The starting claim (`ValaQuenta/modules/h_rb_hat`, in the sibling ValaQuenta repository; **THEORETICAL** — the engine's own
checks below are computed, they do not depend on it): `Ĥ_RB` has multiple
σ-facets — σ→∞ is the **Fermat facet** (no rational solutions, the
forbidden zone), σ=½ is the **Riemann facet** (the critical line, the zeta
zeros). Same operator, different facet, the way a Laplacian's spectrum
looks different depending on the domain you restrict it to.

**This project's job is the Riemann facet's sibling of the Fermat-facet
engine that already existed** (`AbrikosovTree/engine/telperion_engine.py` —
9-level Cayley–Dickson walk, a composite exposes as a zero-divisor collision
at k=4 and "falls," a prime survives to k=8). So: **factorisation itself is
treated as relative to which facet you're standing at** — not one fixed
algebraic test, a family of them, related by the same recursive
Cayley–Dickson construction at different scales.

Concretely, the engine exists to:

1. Give every named "geometry" in this framework a **tier**, so a claim of
   primitiveness can be checked instead of assumed (§2).
2. Decompose actual numbers, permutations, and algebraic elements against
   the Two Trees domain and report `Ω(n)`, the primary decomposition, the
   fall/survive verdict — exactly, not statistically (§4.2).
3. Provide **instruments** — chart, crystal, join — that measure a
   *relationship* between two things (two ring-quantities, two struts, two
   repeat-positions, two cycles) rather than a property of one thing in
   isolation (§4.4–§4.6). This is the instrument layer: "measurement of
   invisible relationships."
4. Self-check every one of the above against real computed data — **the
   zeta function is the control** (Dirichlet equidistribution of primes by
   residue class), never another layer of the same geometry — and keep
   every failed prediction in the record rather than deleting it.
5. Provide **moves** — one toolset per kind of factor (a period, a recurrence,
   a cycle type, a nilpotent part, a derivation tree, …), each with a free
   descent, an ascent that is paid for or refused, and a self-check (§4.16 and
   §§4.17–4.28).

No free parameters. No renormalisation.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
