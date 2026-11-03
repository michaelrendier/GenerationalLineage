# 7. Corrections kept in the record

Two, kept rather than quietly fixed, because "failed predictions stay in
the record" is a standing rule here, not a slogan:

- **F3, the Mingling point.** The generational-lineage skill's own prose
  claimed the two trees reach equal brightness "near `n=9`, near `e²≈7.389`."
  Measured: they cross **three** times, at `n=9, 11, 13` (11 and 13 are
  themselves prime, so Telperion catches up twice more before Laurelin pulls
  ahead for good). `MATHS-FAULT` against the original prose; the relation
  now tests what's actually structural (Laurelin dominates forever after the
  *last* crossing, verified to `N=100,000`) and records the `e²` proximity
  without treating it as a pass condition.
- **G5, the "global annihilator" guess.** Building the trace-Laplacian relation, an early hand-derived guess — that `𝟏₃₂` (the
  all-ones element) is a global annihilator, `x·𝟏=0` for every `x` — turned out to be **false**: it contradicts its own distance
  table (round constants have `Δ=𝟏≠0`). The true statement, machine-verified exhaustively at dim 8 and over 20,000 random samples
  at dim 32, is `Δ(w)=0 ⟺ w²=0`. This was a test of this engine's own trace-Laplacian machinery — work touching other projects not
  scoped here — using SHA-1's five published IV constants as one real-world check case among others (they turn out to
  form a null subalgebra under the test; the four round constants sit at maximum distance instead). The underlying theorem (IV
  nilpotency) stands; the guess was retracted the same day.
- **The README's older prose, audited after 1.0.0.** Checked line by line against the engine, the hand-written text had drifted in
  these ways, all fixed: §5's table listed 40 of the engine's 44 relations (PW13–PW16 were missing — every name it did list was
  correct); `fermat_path(3233)` was documented with excursion 8 (it is 0); `pathway_residues(N, mult=1)` was described as "often
  failing" on an example where it succeeds (§4.4 now uses N = 1451951, which needs multiplier 3); `decompose()`'s documented output
  lacked its `root` field; the pasted `report_emergence` output had older field names; §4.6 said the index of coincidence was "not
  built here yet" although `cipher` builds it; and several passages spoke of "this session". §5, the Emerger report and Appendix A
  are now generated from the engine, so they cannot drift again.
- **The README's code blocks, 1.0.0.** After the 1.0.0 tag, 10 of the README's 21 Python blocks were found to be fragments that used
  names defined only in the surrounding prose, one called a function without its required arguments, and one showed a deliberate
  `AscentNotFree` uncaught. They are fixed and a test now executes every block.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
