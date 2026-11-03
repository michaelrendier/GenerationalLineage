# 4.11 The unit lineage — a THIRD domain for the same decomposition

*Tutorial:* [`12_unit_lineage`](../examples/12_unit_lineage.py).

`PW16`. Cody, 2026-08-25: *"information lives in the units...units can
spectrally show direct generational lineage...mitochondrial lineage if you
will...units are directly how the geometries hold the permutation."* Every
named compound SI unit (Newton, Joule, Watt, Volt, Weber, Tesla) is a point
in the 7-axis lattice of SI base dimensions (`kg,m,s,A,K,mol,cd` — the
leaves), with an exact, computable lineage back to them — the same
leaf/composite discipline this file already runs on numbers
(`factor_lineage`) and processes (`pathway_decomposition`), applied to a
third domain rather than reinvented for it. A unit is a **geometry** in
exactly this project's sense: it carries no numeric content and does no
work itself, but it determines which recombinations of content are legal.

```python
from engine import unit_vector, unit_mul, unit_div, unit_lineage_decompose, SI_BASE

MOL, LITER = unit_vector((0,0,0,0,0,1,0), name='mol'), unit_vector((0,3,0,0,0,0,0), name='L')
concentration = unit_div(MOL, LITER)          # mol/L
recombined = unit_mul(concentration, LITER)   # cancels back to mol EXACTLY
```

**Caught and fixed while building this, not hidden**: the first version of
`unit_lineage_decompose` stored a composite's lineage as bare parent names
(`('Wb', 'm')` for Tesla) and always *added* the parents' vectors — running
it immediately failed all six named units, because Tesla is `Wb/m²`, a
divide by a square, not an add of `Wb` and `m`. Fixed by storing signed
`(parent, power)` pairs per lineage step (`(('Wb',1),('m',-2))`); re-run,
all six match exactly (`N,J,W,V,Wb,T` all `True`), and `mol/L * L` returns
bit-for-bit to `mol`. Ported from an independent build,
`Archimedes/UnitVector.py` in the sibling PtolemyDesktop repository (verified there first against the
same Tesla/Joule derivations), not re-derived from scratch here.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
