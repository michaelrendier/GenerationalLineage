# 0. What this document is

These Concepts pages and the core-facet chapters of this Manual (§§0–8) are the original single-file tutorial for the engine, kept and kept current. The repository is deep enough
that most readers hit the code before they have built the mental model it assumes; this is the map to read first. It defines the
engine's own vocabulary, says plainly what the thing is *for*, then walks every tool it exposes in the order you would reach for
them. The theory write-ups in `wiki/` go deeper on any one idea; the [Glossary](Glossary.md) defines the terms and the
[Tools Reference](Tools-Reference.md) defines every tool.

Every code block in this document is executed by the test suite, and each tutorial in §4 has a runnable script and a generated
transcript in [`examples/`](../examples/). The numbers quoted in the prose were computed by the engine when they were written; §5 is
generated from the engine's own relation log, and [Reproducibility](Reproducibility.md) says how each claim is checked. Where
a statement rests on a sibling repository rather than on anything in this one, it says so.

Design statements quoted with a date and a name ("Cody, 2026-08-25") are the author's own words at the time, kept as provenance:
they record where an idea came from, not that the idea is established. What is established, what is ours and what is theoretical is
labelled where it matters (see [Provenance labels](../README.md#provenance-labels)).

---

# 1. What "Generational Lineage" means, in this engine

Start from the object the engine actually stores. Every fact it knows is one
of these:

```python
from dataclasses import dataclass
from engine import Status                 # HOLDS / MATHS-FAULT / CODE-FAULT

@dataclass
class Relation:                           # the shape of engine.Relation, shown here
    name: str
    claim: str      # one sentence: what is being claimed
    tier: int       # 0 irreducible · 1 reflect/dilate · 2 fixed set · 3 count/ratio
    descends: str   # what this is BUILT FROM — its parent in the lineage
    status: Status  # HOLDS / MATHS-FAULT / CODE-FAULT
    detail: str     # the actual computed numbers backing the claim
```

**Lineage** is the `descends` field, followed all the way down. Nothing in
this engine is allowed to just *be* a geometry or an operation — it has to
say what it's built from, and that chain has to bottom out at one of exactly
three irreducibles:

```
ADD      identity 0, gain 0     Axis 1 {+,−}
SCALE    identity 1, gain 1     Axis 2 {×,÷}
SIGN     identity even-parity   one bit, nothing between
```

**Generation** is depth in that chain — for a number, depth in its
recursive factor tree (a prime is generation 0, a leaf; a composite is an
internal node, one generation per split); for an algebraic operation, depth
in the tier ladder above. `Ω(n)`, the prime-factor count with multiplicity,
is not a statistic *about* a number in this engine — it is defined as the
**length of its lineage**, the number of tier-0 SCALE operations needed to
build it from 1.

**Status** is not binary pass/fail — it's three-way, on purpose, because
"wrong" has more than one cause and conflating them hides which kind you're
looking at:

```
HOLDS         ran, both sides measured, they agree
MATHS-FAULT   ran, both sides measured, they DISAGREE — the claim is false
CODE-FAULT    the check did not run — the claim is UNJUDGED, not confirmed
```

In code the enum members are `Status.HOLDS`, `Status.FALSE` and `Status.UNJUDGED`; their `.value`s — `HOLDS`, `MATHS-FAULT`,
`CODE-FAULT` — are what the reports print.

A relation that never ran is not evidence of anything. This engine has
caught itself in a MATHS-FAULT at least twice (see §7) and left both in the
record rather than quietly fixing the claim and moving on.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
