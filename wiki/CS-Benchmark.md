# cs_benchmark — Measure a callable's real wall-clock cost, once, honestly; every result carries its methodology citation (Patterson et al

*`engine/toolsets/cs_benchmark.py` · line: **both** · tutorial: [`examples/32_cs_benchmark.py`](../examples/32_cs_benchmark.py) · transcript: [`examples/transcripts/32_cs_benchmark.txt`](../examples/transcripts/32_cs_benchmark.txt)*

## What it is

Measure a callable's real wall-clock cost, once, honestly; every result carries its methodology citation (Patterson et al. 2021) as a data field.

## The two directions

| direction | what it does |
|---|---|
| **`descend`** (free, `cost = 0`) | benchmark one callable directly, real wall-clock time, one pass |
| **`build_up`** (work, or refused) | rank several candidate callables against a shared reference cost — cost = candidates scanned |

Call it through the registry — `lines.descend("cs_benchmark", ...)`, `lines.build_up("cs_benchmark", ...)` — or import `engine.toolsets.cs_benchmark` directly. `build_up` raises `AscentNotFree` (with `.owed`) when the rebuild is undetermined; the refusal is the result.

## How it is checked

`engine.toolsets.cs_benchmark.verify()` returns `{"ok": bool, ...}`; `python3 -m engine --verify` runs it with every other toolset, and the tutorial transcript below is regenerated from the tutorial script by `python3 devtools/transcript.py` and compared by the test suite.

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
