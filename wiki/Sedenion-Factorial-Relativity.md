# Sedenion Factorial Relativity

Session origin: 2026-07-17, arising directly out of the SHA-1-first UDEO
session (see `TuringStack`'s `.clauderc_context_1` entry) and Cody's own
tree/root vocabulary for navigating the Cayley-Dickson tower.

## The core move: factorization is relative to which facet you stand at

`H_hat_RB` is one operator with multiple σ-facets (`h_rb_hat/maths.py`):

| σ | Facet | Character |
|---|---|---|
| 0.0 | Fermat (forbidden zone) | no rational solutions — discrete, algebraic |
| 0.5 | Riemann (critical line) | the zeta zeros — continuous, spectral |
| 1.0 | Yang-Mills | gauge |
| 2.0 | General Relativity | curved |

Fermat's facet already has a real, working, already-built mechanism —
the Zero Lattice tree (`telperion_engine.py`). This project's premise:
the same recursive Cayley-Dickson construction, applied at the Riemann
facet instead, should produce its own "extinction" mechanism — not a
metric (already tried, at chance — see Method 3 below), but a genuine
structural fall/survive condition, the way Fermat's facet has one.

**Why "factorial," not "spectral":** `UDEO_RSA_DEMO.py`'s Method 3
("Sedenion Spectral Relativity") already exists and already has a
result — a σ-face geodesic-distance metric, tested against RSA's (e,d),
AT CHANCE. Naming this new work "spectral" would risk quietly reusing
that already-failed mechanism under a new name. "Factorial" names the
actual target precisely: not distance under a metric, but which numbers
get extinguished and which survive — a discrete fall/no-fall condition,
same shape as Fermat's, different facet.

## Orientation inside the tree: leaf, root, and three kinds of roots

Corrected mid-session (Claude had this backwards initially): **k=0 (ℝ,
"The Unit") is the leaf. k=8 (T_256) is the root.** Read as a recursion
tree, not a botanical one — the Cayley-Dickson construction doubles
outward from ℝ (T_256 = CD(T_128,T_128) = ... = CD(ℝ,ℝ) iterated), so
k=0 is the base case where the recursion terminates (the leaf, in the
CS sense — `CayleyDickson.multiply()`'s own `if dim==1: return...` base
case), and k=8 is the top-level construction (the root).
`prime_tower_path()` already walks leaf → root (k=0 → k=8); a composite
falls off that walk at k=4 when its factor pair exposes as a zero-divisor
collision; a prime completes the walk.

Three kinds of "root system" beneath that walk, grounded in
`FourthAgePapers/FermatMonster/engine/fermat_monster_engine.py`:

- **Dendritic roots** — the 23 non-Leech Niemeier lattices, each built
  from a genuine A/D/E-type root system (literal branching Dynkin
  diagrams for D/E), each covering specific N-shapes via its Coxeter
  number h mod 16.
- **Tap root** — the Leech lattice, `LEECH_SHAPE=0`, the one Niemeier
  lattice with *no* root system of its own ("no roots, identity shape"
  — the code's own words). The center axis the other 23 are all cut
  relative to, not one of the branches.
- **Clonal roots** — primes sharing the same h/N-shape aren't
  independently rooted; they converge onto the *same* underlying
  root-system pathway, the way a clonal colony (Pando) presents as many
  trunks sharing one root system underground. A prime's identity as a
  leaf is inseparable from which colony (root-system class) it belongs
  to.

## Quantized pieces and pathways (v1, `engine/maths.py`)

**Pieces:** 9 CD tower levels; 16 N-shapes (8 in `PRIME_SECTOR`, 1
`LEECH_SHAPE`, 3-shape `NIEMEIER_GAP` {1,11,15} — the Monster gap,
unreachable by any A/D/E root system); 24 Niemeier lattices (23 rooted +
Leech); 12 canonical `ZD_CONSTELLATIONS_ODD` 4-tuples; 20 real Riemann
zeros on file (`RIEMANN_ZEROS`, LMFDB/Odlyzko, `h_rb_hat/maths.py`).

**Pathways:** leaf-to-root walk (`prime_tower_path`); the fall branch at
k=4; the clonal branch (shared root-system convergence); the gap-filling
branch (Monster + 70 sibling VOAs cover what no root system reaches).

## The control: the zeta function, stated explicitly

Cody, 2026-07-17: *"the Zeta Function is the Control...it is the
authoritative maths for the order the primes grow."* Concretely:
Dirichlet's theorem — primes are asymptotically equidistributed among
the φ(16)=8 classes coprime to 16 — is itself a consequence of the
non-vanishing of Dirichlet L-functions on the critical line (GRH
territory), i.e. real zeta/L-function structure, not tree geometry.
`telperion_engine.py`'s own module docstring already names the exact
quantity that connects the two — *"Oscillations in π(x;16,k) are driven
by zeros of Dirichlet L-functions L(s,χ). These zeros ARE the spectral
nodes of the Zero Tree"* — but nothing wired that statement to real data
until this project.

**First honest test run (N=200,000):** does the Monster gap {1,11,15}
show a real density deviation from equidistribution — evidence the gap
shapes are structurally special in actual prime counts, not just in the
tree's own classification? Chi-square = 0.38 (7 dof). Gap deviation
−0.083%, dendritic deviation +0.050%. **No detectable signal.** Real
primes don't currently show any density anomaly correlated with the
tree's own gap/dendritic split, at this scale. Recorded, not deleted —
failed predictions stay in the record.

## Open design question — not yet built

The actual Riemann-facet "fall" condition. Fermat's fall is exact and
structural: a composite's factor pair collides as a real zero-divisor at
k=4. What is the Riemann-facet analog — what, structurally, would a
prime's own relationship to the real zeta zeros (not the P1 hash-index
proxy) cause it to "fall" against? Candidates not yet evaluated:
proximity between a prime's some derived quantity and a zero height
γ_n; a prime's contribution to the explicit-formula oscillation term
Li(x^ρ) crossing some threshold; something else entirely. This has to
be defined precisely — the same way "zero-divisor collision" is a
precise, computable condition — before it's a testable engine, not an
analogy.

## On the way back out

Cody, mid-session: *"on the way back out of this rabbit hole, we will
use the negative maths all the way back."* Parked for when the Riemann
facet's fall condition is actually built — `facet_fermat()`'s own
framing (FLT as the *negative* facet of H_hat_RB, "not a projection of
what the operator produces") is the likely anchor for what "negative
maths" means here, not yet connected further.
