# stencil — The digit-by-digit decomposition machine: `descend` is N = p·q; `build_up` constructs factor pairs from N alone, digit by digit

*`engine/toolsets/stencil.py` · line: **both** · tutorial: [`examples/33_stencil.py`](../examples/33_stencil.py) · transcript: [`examples/transcripts/33_stencil.txt`](../examples/transcripts/33_stencil.txt)*

## What it is

The digit-by-digit decomposition machine: `descend` is N = p·q; `build_up` constructs factor pairs from N alone, digit by digit. Slide 1 run to full depth is exhaustive and exact — every divisor pair is found — and a prime N raises `AscentNotFree`.

## The two directions

| direction | what it does |
|---|---|
| **`descend`** (free, `cost = 0`) | N = p·q — one multiplication, no search (the hand-worked long-multiplication pathway, carries and all, walked forward) |
| **`build_up`** (work, or refused) | given only N, build candidate factor pairs digit by digit; slide 1 run to full depth is exhaustive and exact — every divisor pair is found, and a prime N raises AscentNotFree (the refusal is the result) |

## API

`engine.toolsets.stencil` · registry name `stencil` · line **both** · every call below is made as `lines.<direction>("stencil", ...)` (`from engine import lines`) or directly on the module.

### `descend` — free — `cost = 0`

```python
descend(p, q)
```

FREE: multiply. One pass, cost 0 — the same pathway the hand-worked long multiplication walks explicitly, carry by carry.

| parameter | default | type |
|---|---|---|
| `p` | *required* | `int` |
| `q` | *required* | `int` |

**Returns** a dict with keys: `toolset` (str), `p` (int), `q` (int), `N` (int), `cost` (int).
Example call: `lines.descend("stencil", 53, 61)`

### `build_up` — work — reports `cost`, may refuse

```python
build_up(N, run_slide2=False)
```

WORK: construct N's factor pairs digit by digit (slide 1, exact, exhaustive). Reports `cost` honestly. Raises AscentNotFree if N is prime — no nontrivial (p,q) exists, and that is the correct answer, not a search failure. Pass run_slide2=True to also run the top-down construction (over one factor's own digit length) and report its surviving leading-digit prefixes alongside — the two slides are NOT combined here (see the module docstring's meet-in-the-middle note).

| parameter | default | type |
|---|---|---|
| `N` | *required* | `int` |
| `run_slide2` | `False` | `bool` |

**Returns** a dict with keys: `toolset` (str), `N` (int), `pairs` (list), `cost` (int), `slide1_final_prefixes` (int).
**Raises** `AscentNotFree` (`.owed` names the missing constraint) when the rebuild is undetermined.
Example call: `lines.build_up("stencil", 91)`

### `verify()`

`verify() -> {"ok": bool, ...}` — the toolset checks itself. `lines.verify_all()` runs this for every toolset.

## A worked session

Every line below is the literal output of the tutorial script, which starts from its own imports, so it can be read cold.

```text
>>> from engine.toolsets import stencil
>>> from engine.lines import AscentNotFree
>>> # descend(): N = p*q — one multiplication, no search.
>>> stencil.descend(53, 61)["N"]
3233
>>> # build_up(): given only N, construct the factor pairs digit by digit. Slide 1 to full depth is exact,
>>> # so EVERY divisor pair is found.
>>> b = stencil.build_up(3233)
>>> b["pairs"], b["cost"]
([(53, 61)], 44500)
>>> stencil.build_up(360)["pairs"][:4]
[(2, 180), (3, 120), (4, 90), (5, 72)]
>>> # A prime has no pair, and the refusal is the result:
>>> try:
...     stencil.build_up(3229)
... except AscentNotFree as e:
...     type(e).__name__
'AscentNotFree'
```

## From the source

The module's own docstring, verbatim — it carries the provenance, the citations and the design notes for this tool.

```text
GenerationalLineage.engine.toolsets.stencil
STENCIL — the digit-by-digit decomposition machine.
Cody, 2026-09-13: "i don't care about pruning...this is a decomposition
machine" — "RSA was just common context to use." Not a race against
exhaustive search (that comparison is the wrong axis, and this module does
not make it); a CONSTRUCTIVE, EXACT, GUARANTEED pathway from N to its
factors, the same way long multiplication is a constructive, exact,
traceable pathway from (p,q) to N — carries and all, nothing skipped,
nothing approximated. The hand-worked photograph of 1546854629 x 7283619945
(an hour, two caught errors from a single dropped carry propagating) is
literally what DESCEND looks like when the pathway is walked by hand rather
than assumed free — it is cost-0 in the sense that no SEARCH is needed, not
in the sense that no WORK exists. BUILD_UP is that same kind of pathway,
walked in the other direction, and it is allowed to be long: `cost` reports
how long, honestly, never minimised.
DESCEND (free): given p and q, N = p*q — one multiplication, no search.
BUILD_UP (work): given only N, construct candidate factor pairs digit by
digit. Two slides over the same (p,q) domain, kept SEPARATE here on
purpose (they build from opposite ends of the number — combining them
needs an actual meet-in-the-middle overlap check, not a splice of two
different partial representations; that combination is real, open design
work, not done in this pass — see the module TODO at the bottom):
  SLIDE 1 (bottom-up, exact — `_slide1`): a candidate (P,Q) prefix-pair
  survives from depth k-1 to k only if P*Q matches N's low k+1 digits
  EXACTLY (an integer equality — "can't propagate any borrowing from 10").
  Run to full depth (k = len(str(N))), this is already a COMPLETE,
  GUARANTEED, EXACT decomposition procedure: the exact-equality filter at
  the end is trivial once depth == digit length, and every genuine divisor
  pair of N survives by construction (proved, not assumed — a candidate
  can only be eliminated by failing an EXACT modular equality that every
  real divisor pair satisfies at every depth). It reports every divisor
  pair, not just the "intended" one — a real, correct-by-construction
  side effect of doing this exactly rather than heuristically.
  SLIDE 2 (top-down, magnitude + primality — `_slide2_candidates`):
  hypothesize p's LEADING m digits; the corresponding q = N/p window,
  computed EXACTLY (Fraction, never float), either contains no integer at
  all (a real, provable elimination — not a heuristic) or contains one or
  more; requiring at least one PRIME in that window is a second, different,
  exact filter, kept here as an independent generator over the same domain,
  not yet stitched to slide 1's low-digit output.
Guarantee: slide 1 run to full depth is exhaustive and exact. If N has a
nontrivial factorization it WILL be found; if N is prime, build_up raises
AscentNotFree — the refusal is the result, not a failure (scale.py's own
phrasing for the same idea).
```

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). See also the [Tools Reference](Tools-Reference.md).*
