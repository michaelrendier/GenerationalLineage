# spectral_primes — The spin/wobble split read as decomposition versus emerger: the spin rate θ′(t) is a smooth monotone carrier (free), and the wobble — the oscillation from the zeros that carries the primes — costs one unit of work per zero

*`engine/toolsets/spectral_primes.py` · line: **both** · tutorial: [`examples/31_spectral_primes.py`](../examples/31_spectral_primes.py) · transcript: [`examples/transcripts/31_spectral_primes.txt`](../examples/transcripts/31_spectral_primes.txt)*

## What it is

The spin/wobble split read as decomposition versus emerger: the spin rate θ′(t) is a smooth monotone carrier (free), and the wobble — the oscillation from the zeros that carries the primes — costs one unit of work per zero.

## The two directions

| direction | what it does |
|---|---|
| **`descend`** (free, `cost = 0`) | theta'(t) at one height — the spin/carrier rate, no resonance, no search |
| **`build_up`** (work, or refused) | reconstruct psi(x) from n_zeros known zeros — cost = n_zeros; the primes (Gibbs undershoot at prime jumps) only emerge as more work (more zeros) is spent |

## API

`engine.toolsets.spectral_primes` · registry name `spectral_primes` · line **both** · every call below is made as `lines.<direction>("spectral_primes", ...)` (`from engine import lines`) or directly on the module.

### `descend` — free — `cost = 0`

```python
descend(t)
```

SPIN, free: theta'(t) at height t -- one evaluation, no search. No prime content lives here; that is the point being read off.

| parameter | default | type |
|---|---|---|
| `t` | *required* | `float` |

**Returns** a dict with keys: `toolset` (str), `t` (float), `spin_rate` (float), `resonant` (bool), `note` (str).
Example call: `lines.descend("spectral_primes", 100.0)`

### `build_up` — work — reports `cost`, may refuse

```python
build_up(x, n_zeros=25)
```

WOBBLE, work: reconstruct psi(x) from the oscillatory term of the von Mangoldt explicit formula, summing n_zeros known zeros. cost = n_zeros (the terms actually summed) -- this IS the emerger reading: the primes only emerge as you spend the work of including more zeros.

| parameter | default | type |
|---|---|---|
| `x` | *required* | `float` |
| `n_zeros` | `25` | `int` |

**Returns** a dict with keys: `toolset` (str), `x` (float), `n_zeros_used` (int), `cost` (int), `reconstructed` (float), `exact` (float), `difference` (float), `note` (str).
Example call: `lines.build_up("spectral_primes", 10.0, n_zeros=10)`

### `verify()`

`verify() -> {"ok": bool, ...}` — the toolset checks itself. Self-check: (1) spin is monotonic (no resonance) across the embedded `lines.verify_all()` runs this for every toolset.

## A worked session

Every line below is the literal output of the tutorial script, which starts from its own imports, so it can be read cold.

```text
>>> from engine.toolsets import spectral_primes as sp
>>> # descend(): the spin rate theta'(t) at one height — smooth and monotonic, no peaks by construction.
>>> r = sp.descend(100.0)
>>> round(r["spin_rate"], 6), r["resonant"]
(1.383647, False)
>>> # build_up(): rebuild psi(x) from n zeros. The primes emerge only as work (more zeros) is spent.
>>> b10 = sp.build_up(30.0, n_zeros=10)
>>> b25 = sp.build_up(30.0, n_zeros=25)
>>> round(b10["exact"], 4)
28.4765
>>> abs(b25["difference"]) < abs(b10["difference"])
True
>>> b10["cost"], b25["cost"]
(10, 25)
```

## From the source

The module's own docstring, verbatim — it carries the provenance, the citations and the design notes for this tool.

```text
GenerationalLineage.engine.toolsets.spectral_primes
SPECTRAL PRIMES — the spin/wobble split read as decomposition vs emerger.
Born 2026-09-26 from the theta(t)-rotation construction (RiemannHypothesis
Proof/ADDENDUM_toroidal_theta_structure_2026-09-25.md) and its own live
follow-up (ValaQuenta/modules/spectral_primes/). The split turns out to
already have this engine's own two-jurisdiction shape:
SPIN (major loop, theta'(t)) is the smooth, non-resonant carrier rate —
one evaluation, no search, no stored tape. Reading it off a height t is
exactly a DECOMPOSITION: free, cost=0.
WOBBLE (minor loop) is where the primes live, classically (von Mangoldt /
Weil): reconstructing psi(x) requires SUMMING over the known zeros — a
search whose cost grows with how many zeros you're willing to include.
That is exactly this engine's EMERGER shape: choice (how many terms) is
work, and the result only converges to the true step function as more
work is spent (Gibbs-phenomenon undershoot at the primes themselves is
the visible fingerprint of "not enough work yet").
Module independence (this repo's convention): stdlib + math/cmath only.
The zero table below is a small, literal, embedded set of known Riemann
zero imaginary parts (computed once via mpmath, dps=20, and frozen here as
data — not re-derived at import time). This toolset does NOT reproduce the
tilt-vs-wobble correlation test or the Real-Tilt/Axis crossing check from
ValaQuenta/modules/spectral_primes/maths.py — those need a full
arbitrary-sigma zeta evaluation, which needs mpmath, which this repo's
independence convention excludes. Those two results live in ValaQuenta;
this toolset carries only the two pieces that are honestly stdlib-only:
spin (decomposition) and wobble-via-psi-reconstruction (emerger).
```

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). See also the [Tools Reference](Tools-Reference.md).*
