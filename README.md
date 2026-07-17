# Sedenion Factorial Relativity

Recursive factorization, à la Laplacians — same operator, different facet.

## What this is

`H_hat_RB` (the RedBlue Hamiltonian, `ValaQuenta/modules/h_rb_hat/`) has
multiple σ-facets: σ→∞ is the Fermat facet (no rational solutions, the
forbidden zone), σ=½ is the Riemann facet (the critical line, the zeta
zeros). Just as a Laplacian's spectrum looks different depending on the
domain you restrict it to while remaining the same operator, this project
treats **factorization itself as relative to which facet you're standing
at** — not one fixed algebraic test, but a family of them, related by the
same recursive Cayley-Dickson tower construction at different scales.

The Fermat facet already has a working engine:
[`AbrikosovTree/engine/telperion_engine.py`](../AbrikosovTree/engine/telperion_engine.py)
("Telperion" / the Zero Lattice tree). It doesn't search for whether a
number factors — it reads the answer directly off the number's position
in a 9-level Cayley-Dickson tower (ℝ → T_256): a composite's factor pair
exposes as a real zero-divisor collision at k=4 (the sedenion level) and
the number "falls"; a prime has no factor pair to expose, so it survives
the whole walk to k=8. Primes are literally the leaves of this tree —
not a metaphor, `classify_prime()`'s own `fermat_survives` flag is
definitional, not searched for.

**This project's job is the Riemann facet's sibling of that same
mechanism — deliberately named "factorial," not "spectral", to keep it
separate from `UDEO_RSA_DEMO.py`'s Method 3 ("Sedenion Spectral
Relativity," a σ-face *geodesic distance* metric, already tested against
RSA and found at chance).** Factorial relativity isn't about distance
between two points under a metric — it's about which numbers get
extinguished, and which survive, changing with which facet of the same
operator you're standing at.

## The control

Stated plainly, 2026-07-17: **the zeta function is the control.** The
geometric tree is a candidate mechanism, not ground truth. Whatever it
predicts about how primes distribute across N-shapes, root systems, and
fall/survive branches has to be checked against the real, counted order
primes actually grow in — governed by the zeros of the relevant Dirichlet
L-functions (Dirichlet's theorem: primes are asymptotically
equidistributed among the φ(16)=8 residue classes coprime to 16). Same
honest-scoring discipline as every other engine in this framework:
propose, then check against a real control, not another layer of the
same geometry.

## Correction, same day: the tree is a consequence, not the source

`FourthAgePapers/FermatMonster/engine/fermat_monster_engine.py`'s own
docstring states the actual foundational claim — the generalized Fermat
equation (x^l+y^m=z^n, independent exponents) IS the Monster Group + 70
Schellekens siblings (71 holomorphic c=24 VOAs), Cody's "Nightmare
Group" — and explicitly lists the ZD-cascade/leaf-tree mechanism this
project is built on as a **consequence** of that claim, not the bridge
itself. See the wiki page for the full correction. Everything in this
README describing the tree as foundational should be read with that
hierarchy in mind.

## Structure

```
engine/
  maths.py   — quantized pieces (CD tower levels, N-shapes, root systems,
               ZD constellations, Monster gap) and pathways (leaf-to-root
               walk, root-system classification), plus the control test
               (real π(x;16,k) vs Dirichlet equidistribution). Imports
               telperion_engine.py and h_rb_hat/maths.py directly — no
               reimplementation of either.
  tools.py   — runnable reports over maths.py.
wiki/
  Sedenion-Factorial-Relativity.md — fuller write-up, orientation
  (leaf/root, dendritic/tap/clonal root systems), open design questions.
```

## Status

v1. The inventory (pieces/pathways) is real and wired to the actual
existing engines. One honest control test is implemented: does the
Monster gap {1,11,15} (the 3 N-shapes no Niemeier root system can reach)
show any real density deviation from Dirichlet equidistribution in
counted primes? First run, N=200,000: chi-square 0.38 (7 dof) — no
detectable deviation. Gap and dendritic classes track the uniform
expectation to within a tenth of a percent.

**Not yet built:** the actual Riemann-facet "fall" condition — a
structural, per-number test analogous to "does this factor pair expose
as a ZD collision," but keyed to a prime's own relationship to the real
zeta zeros (not the P1 hash-index proxy used elsewhere in this
framework). That design question is open, not glossed over — see the
wiki page.

No free parameters. No renormalization. Failed predictions stay in the
record.

White Hat.
