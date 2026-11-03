# comma_sequence — The comma sequence (Angelini, Guy & Sloane): each term's step is read off the digits straddling the comma

*`engine/toolsets/comma_sequence.py` · line: **both** · tutorial: [`examples/28_comma_sequence.py`](../examples/28_comma_sequence.py) · transcript: [`examples/transcripts/28_comma_sequence.txt`](../examples/transcripts/28_comma_sequence.txt)*

## What it is

The comma sequence (Angelini, Guy & Sloane): each term's step is read off the digits straddling the comma. `descend` checks a walk; `build_up` walks the lexicographically-earliest sequence forward, cost = terms placed.

## The two directions

| direction | what it does |
|---|---|
| **`descend`** (free, `cost = 0`) | the comma-group read — each gap a(n+1)−a(n) = b·L + R is lifted straight off the two digits straddling the comma; one pass says whether the walk is valid and whether it has hit a landmine. Resolution is a RATIO (b²:2 = step alphabet : comma window), not a bandwidth — the Flashlight, and mortality is its coarse end |
| **`build_up`** (work, or refused) | walk the lexicographically-earliest comma sequence forward one term at a time (the forced successor is the earliest valid R); cost = terms placed; base<634 dies, base≥634 is immortal |

> **EXPERIMENTAL.** Marked experimental by the author: the comma-group read and its resolution-as-ratio framing have not yet been shown to succeed at what they are for. It is documented and self-checked, but do not treat it as a working tool yet.

## API

`engine.toolsets.comma_sequence` · registry name `comma_sequence` · line **both** · every call below is made as `lines.<direction>("comma_sequence", ...)` (`from engine import lines`) or directly on the module.

### `descend` — free — `cost = 0`

```python
descend(seq, base=10)
```

| parameter | default | type |
|---|---|---|
| `seq` | *required* | `Sequence[int]` |
| `base` | `10` | `int` |

**Returns** a dict with keys: `toolset` (str), `line` (str), `base` (int), `n_terms` (int), `valid_comma_walk` (bool), `first_break` (int), `steps` (list), `at_landmine` (NoneType), `resolution_ratio` (str), `step_alphabet` (int), `mortal_base` (bool), `note` (str).
Example call: `lines.descend("comma_sequence", [1, 12, 24, 36])`

### `build_up` — work — reports `cost`, may refuse

```python
build_up(n_terms, base=10, start=1)
```

| parameter | default | type |
|---|---|---|
| `n_terms` | *required* | `int` |
| `base` | `10` | `int` |
| `start` | `1` | `int` |

**Returns** a dict with keys: `toolset` (str), `line` (str), `base` (int), `start` (int), `sequence` (list), `length` (int), `cost` (int), `reached_target` (bool), `died_at` (NoneType), `immortal_base` (bool), `note` (str).
Example call: `lines.build_up("comma_sequence", 12)`

### `verify()`

`verify() -> {"ok": bool, ...}` — the toolset checks itself. `lines.verify_all()` runs this for every toolset.

## A worked session

Every line below is the literal output of the tutorial script, which starts from its own imports, so it can be read cold.

```text
>>> from engine.toolsets import comma_sequence as cs
>>> # build_up(): walk the earliest valid comma sequence forward; the cost is the number of terms placed.
>>> b = cs.build_up(12)
>>> b["sequence"], b["cost"], b["died_at"]
([1, 12, 35, 94, 135, 186, 248, 331, 344, 387, 461, 475], 12, None)
>>> # descend(): read a sequence back — is it a valid comma walk, and does the base survive?
>>> r = cs.descend(b["sequence"])
>>> r["valid_comma_walk"], r["mortal_base"], r["resolution_ratio"]
(True, True, '100:2')
```

## From the source

The module's own docstring, verbatim — it carries the provenance, the citations and the design notes for this tool.

```text
GenerationalLineage.engine.toolsets.comma_sequence
THE COMMA GROUP (separator) decomposition — the step lives IN the separator.
Numberphile "The Immortal Kangaroo Sequence"; Angelini, Guy & Sloane,
"The Comma Sequence: A Simple Sequence With Bizarre Properties"
(arXiv:2401.14346); "The Comma Sequence is Finite in Other Bases"
(arXiv:2408.03434).
RULE (base b): write the walk with commas.  The gap across a comma is the
two-digit number straddling it —
    a(n+1) - a(n)  =  b * L  +  R ,
      L = last digit of a(n)   (just LEFT of the comma)
      R = leading digit of a(n+1)  (just RIGHT of the comma), R in 1..b-1
so a(n+1) is forced into a window of width b-1, and the earliest valid R
wins.  When no R makes the leading digit match, the kangaroo has hit a
landmine — the walk is MORTAL.  Base 10 dies at 99,999,945 (2,137,453
terms).  Bases 3..633 all die; b >= 634 (and a rule tweak) go immortal.
DECOMPOSITION (free): read a given sequence's steps straight off its commas
in one pass — is it a valid comma walk, and where (if ever) does it die?
"Spectral resolution" here is a RATIO, not a bandwidth: the step alphabet
is b*b values, the comma window is 2 digits — resolution = b:2, a
local:global magnification (the Flashlight), and mortality is the coarse
end of it.
EMERGER (work): generate the lexicographically-earliest comma walk forward,
placing one term at a time until it dies or n_terms is reached.  cost =
terms placed.
```

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). See also the [Tools Reference](Tools-Reference.md).*
