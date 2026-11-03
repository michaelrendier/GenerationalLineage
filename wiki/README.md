# The Manual

The [README](../README.md) is the first page: install, quickstart, a "which tool do I need?" table and an overview of every tool. **These
pages are the Manual** — what the engine is, what it does, and how to run each kind of analysis. Pages marked *(generated)* are produced
by `devtools/build_docs.py` from the live code and cannot drift from it. Section numbers (§) in the older chapters are kept from the
engine's original single-file tutorial.

## 1. Concepts — read first

| page | what it covers |
|---|---|
| [Concepts-What-It-Means](Concepts-What-It-Means.md) | §0–1: what this is; what "Generational Lineage" means in this engine |
| [Concepts-The-Mathematics](Concepts-The-Mathematics.md) | §2: the two lines and the two charts — same object, or two things kept in sync? |
| [Concepts-What-It-Was-Built-To-Do](Concepts-What-It-Was-Built-To-Do.md) | §3: the engine's job |
| [The-Generational-Lineage-Engine](The-Generational-Lineage-Engine.md) | the session origin and the core move: factorisation is relative to the facet you stand at |
| [Two-Lines-and-Jurisdiction](Two-Lines-and-Jurisdiction.md) | descent free, ascent work, the adjoint is the one that costs |
| [The-Two-Charts-and-Jurisdiction](The-Two-Charts-and-Jurisdiction.md) | the Smith chart and the Apollonian gasket as one loop through PSL(2, ℂ) |
| [Glossary](Glossary.md) | the terms, defined |

## 2. The core facets — how to do each analysis

Each page: what it does, a runnable example, a transcript, where it stops.

| page | analysis |
|---|---|
| [Run-the-Self-Check](Run-the-Self-Check.md) | §4, 4.1 — prove an install; the command line |
| [Decompose-a-Number](Decompose-a-Number.md) | §4.2 — lineage tree, primary decomposition, fall/survive |
| [Tier-of-an-Operation](Tier-of-an-Operation.md) | §4.3 — is a named operation primitive or derived? |
| [Pathway-and-Tuning](Pathway-and-Tuning.md) | §4.4 — factoring as a walk between two anchors, tuned per number |
| [Smith-Chart-Instruments](Smith-Chart-Instruments.md) | §4.5 — the two-ring chart; fold any two quantities through the Möbius map |
| [Crystal-and-Join](Crystal-and-Join.md) | §4.6 — recover an unseen period; a permutation's order from its cycles |
| [Fractal-Block](Fractal-Block.md) | §4.7 — fall/survive as dynamics: escape, Lyapunov, bifurcation |
| [Reports](Reports.md) | §4.8 — the printed reports |
| [Factoral-Spiral](Factoral-Spiral.md) | §4.9 — decomposition as chart geometry |
| [Pathway-Decomposition](Pathway-Decomposition.md) | §4.10 — factoring a process, not a number |
| [Unit-Lineage](Unit-Lineage.md) | §4.11 — a third domain: units in the SI lattice |
| [Clay-Millennium](Clay-Millennium.md) | §4.12 + output — the seven problems: what each builds, what it imports |
| [Spectral-Decomposition](Spectral-Decomposition.md) | §4.13 — factoring wavelengths |
| [The-Emerger-Tutorial](The-Emerger-Tutorial.md) · [The-Emerger-Ascent-Dual](The-Emerger-Ascent-Dual.md) | §4.14 — the ascent dual |
| [Ping-RSA-Classifier](Ping-RSA-Classifier.md) · [Ping-and-the-Counter-Operator-Laplacian](Ping-and-the-Counter-Operator-Laplacian.md) | §4.15 — classify an RSA modulus |
| [Firing-Plans](Firing-Plans.md) | brackets that carry firing orders (`bracketing_firing_order` tool 4) |
| [The-Operator-Tree](The-Operator-Tree.md) | the shapes of mathematics as folds of three generators |
| [ADD-SCALE-SIGN-Datatype](ADD-SCALE-SIGN-Datatype.md) | the tier-0 floor as a datatype |
| [Oscilloscope](Oscilloscope.md) *(generated)* | the two-panel Fermat/Riemann SVG (Extended layer) |

## 3. The toolsets — one page each

[The-Toolsets](The-Toolsets.md) states the contract (`descend`, `build_up`, `verify`, `AscentNotFree`) and lists the registry
*(generated)*. [Tools-Reference](Tools-Reference.md) *(generated)* defines every tool.

| group | pages |
|---|---|
| **the older toolsets** | [Scale](Scale.md) · [Units-and-the-Equation-Index](Units-and-the-Equation-Index.md) · [Box-Kite](Box-Kite.md) · [Noether](Noether.md) · [Archimedes-Screw](Archimedes-Screw.md) · [Inversion](Inversion.md) · [T32-Nilpotency](T32-Nilpotency.md) · [Cipher](Cipher.md) · [Comma-Sequence](Comma-Sequence.md) *(generated)* · [Hyper-Linear-Algebra](Hyper-Linear-Algebra.md) · [Equation-Space](Equation-Space.md) · [Spectral-Primes](Spectral-Primes.md) *(generated)* · [CS-Benchmark](CS-Benchmark.md) *(generated)* · [Stencil](Stencil.md) *(generated)* |
| **the ten moves added in 1.0** *(generated)* | [Periodicity](Periodicity.md) · [Lyndon-Words](Lyndon-Words.md) · [Berlekamp-Massey](Berlekamp-Massey.md) · [Log-Periodic-and-Mellin](Log-Periodic-and-Mellin.md) · [Permutation](Permutation.md) · [Rejewski](Rejewski.md) · [Jordan-Chevalley](Jordan-Chevalley.md) · [Re-Pair](Re-Pair.md) · [Pohlig-Hellman](Pohlig-Hellman.md) · [Unicity](Unicity.md) |
| **the eleventh move** | [Circle](Circle.md) *(generated)* · [Circle-Catalogue](Circle-Catalogue.md) |

## 4. Reference and record

| page | what it is |
|---|---|
| [Tutorial-Index](Tutorial-Index.md) *(generated)* | all 44 tutorials, each with its transcript |
| [Relations](Relations.md) *(generated)* | §5 — every self-checked relation |
| [References](References.md) | the bibliography for every established algorithm |
| [Reproducibility](Reproducibility.md) | how each claim is checked, and how to re-run it |
| [Where-the-Factorial-Lives](Where-the-Factorial-Lives.md) | §6 |
| [Corrections](Corrections.md) | §7 — corrections kept in the record |
| [Whats-Next](Whats-Next.md) | §8 |
| [ValaQuenta-Calibration](ValaQuenta-Calibration.md) | the decomposition run on every ValaQuenta engine, as a check on the decomposition |
