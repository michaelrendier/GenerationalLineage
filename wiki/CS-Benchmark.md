# cs_benchmark — Measure a callable's real wall-clock cost, once, honestly; every result carries its methodology citation (Patterson et al

*`engine/toolsets/cs_benchmark.py` · line: **both** · tutorial: [`examples/32_cs_benchmark.py`](../examples/32_cs_benchmark.py) · transcript: [`examples/transcripts/32_cs_benchmark.txt`](../examples/transcripts/32_cs_benchmark.txt)*

## What it is

Measure a callable's real wall-clock cost, once, honestly; every result carries its methodology citation (Patterson et al. 2021) as a data field.

## The two directions

| direction | what it does |
|---|---|
| **`descend`** (free, `cost = 0`) | benchmark one callable directly, real wall-clock time, one pass |
| **`build_up`** (work, or refused) | rank several candidate callables against a shared reference cost — cost = candidates scanned |

## API

`engine.toolsets.cs_benchmark` · registry name `cs_benchmark` · line **both** · every call below is made as `lines.<direction>("cs_benchmark", ...)` (`from engine import lines`) or directly on the module.

### `descend` — free — `cost = 0`

```python
descend(fn, args=(), kwargs=None, n=1000)
```

The FREE reading: benchmark ONE callable, directly, n calls, no comparison and no search. Returns real measured seconds/call and calls/sec -- the honest minimum a cost claim needs.

| parameter | default | type |
|---|---|---|
| `fn` | *required* | `Callable` |
| `args` | `()` | `Tuple` |
| `kwargs` | `None` | `Optional[Dict]` |
| `n` | `1000` | `int` |

**Returns** a dict with keys: `toolset` (str), `n_calls` (int), `total_s` (float), `s_per_call` (float), `calls_per_s` (float), `citation` (str), `note` (str).
Example call: `lines.descend("cs_benchmark", sum, args=([1, 2, 3],), n=200)`

### `build_up` — work — reports `cost`, may refuse

```python
build_up(candidates, reference_s_per_call, args=(), kwargs=None, n=1000)
```

The WORK: benchmark every candidate in `candidates`, rank them against a shared `reference_s_per_call` (e.g. a known baseline cost), report each one's speedup. `cost` = candidates scanned.

| parameter | default | type |
|---|---|---|
| `candidates` | *required* | `Dict[str, Callable]` |
| `reference_s_per_call` | *required* | `float` |
| `args` | `()` | `Tuple` |
| `kwargs` | `None` | `Optional[Dict]` |
| `n` | `1000` | `int` |

**Returns** a dict with keys: `toolset` (str), `n_candidates` (int), `reference_s_per_call` (float), `ranked` (list), `fastest` (str), `cost` (int), `citation` (str), `note` (str).
Example call: `lines.build_up("cs_benchmark", {'sum': <built-in function sum>}, 1e-06, args=([1, 2, 3],), n=200)`

### `verify()`

`verify() -> {"ok": bool, ...}` — the toolset checks itself. `lines.verify_all()` runs this for every toolset.

## A worked session

Every line below is the literal output of the tutorial script, which starts from its own imports, so it can be read cold.

```text
>>> from engine.toolsets import cs_benchmark
>>> # descend(): time one callable directly (real wall-clock, one pass).
>>> r = cs_benchmark.descend(sum, args=([1, 2, 3],), n=200)
>>> r["n_calls"], r["s_per_call"] > 0
(200, True)
>>> r["citation"]
'Patterson et al. (2021), "Carbon Emissions and Large Neural Network Training", arXiv:2104.10350'
```

## From the source

The module's own docstring, verbatim — it carries the provenance, the citations and the design notes for this tool.

```text
GenerationalLineage.engine.toolsets.cs_benchmark
CS_BENCHMARK -- measure a callable's real cost, once, honestly. Citation
travels in the code: every result this toolset returns carries `CITATION`
as a data field, not a separate footnote a caller has to remember to keep
attached.
Methodology source: Patterson, Gonzalez, Le, Liang, Munguia, Rothchild, So,
Texier, Dean (2021), "Carbon Emissions and Large Neural Network Training",
arXiv:2104.10350 -- their own footprint identity is
    Footprint = (energy_train + queries * energy_inference) * CO2e_per_KWh
cited here for the discipline it argues for: report the actual measured
cost of a real run, on real hardware, as a first-class transparent number
-- not a theoretical FLOP estimate, not an afterthought. `footprint()`
below is that formula, directly.
DECOMPOSITION (free): `descend` -- benchmark ONE callable, one measurement
pass, no search. The honest, minimal reading.
EMERGER (work): `build_up` -- benchmark several CANDIDATE callables against
a shared reference cost and rank them. Searching for the cheapest
candidate is the work; reading one candidate's own cost is not.
```

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). See also the [Tools Reference](Tools-Reference.md).*
