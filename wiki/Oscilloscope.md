# oscilloscope — EXTENDED layer

*`engine/oscilloscope.py` · line: **decomposition** · tutorial: [`examples/90_extended_fermat_facet.py`](../examples/90_extended_fermat_facet.py) · transcript: [`examples/transcripts/90_extended_fermat_facet.txt`](../examples/transcripts/90_extended_fermat_facet.txt)*

> **EXTENDED layer** — needs the three sibling repositories (see [Install](../README.md#install)).

## What it is

**EXTENDED layer.** A two-panel SVG: the Fermat N-shape (0…15) and root-system pathway of one number, over the Riemann-facet equidistribution reading. Its ascent is refused: a shape is N mod 16, and recovering N owes the remaining digits.

## The two directions

| direction | what it does |
|---|---|
| **`descend`** (free, `cost = 0`) | stack the two facets (Fermat prompt / Riemann firing) of one number |
| **`build_up`** (work, or refused) | — |


## A worked session

Every line below is the literal output of the tutorial script, which starts from its own imports, so it can be read cold.

```text
>>> import engine
>>> if not engine.EXTENDED:
...     print("EXTENDED layer not installed — skipping (see README, 'Extended install').")
... else:
...     p = engine.quantized_pieces()
...     p["cd_tower_levels"], p["leaf_level"]
...     # The control: real prime counts by residue class mod 16, against Dirichlet equidistribution.
...     engine.pathway_root_system_class(13)
(9, 0)
{'p': 13, 'nshape': 13, 'classification': 'niemeier_odd', 'in_prime_sector': True, 'is_moonshine': True, 'voa_source': 'Niemeier root system (odd h, A-type)', 'fermat_survives': True, 'root_pathway': 'dendritic'}
```

## From the source

The module's own docstring, verbatim — it carries the provenance, the citations and the design notes for this tool.

```text
oscilloscope.py -- the Factorial Relativity oscilloscope.
Model: VAPMIP/layer_spectrograph.py ("The Universal Oscilloscope",
SedenionSpectralRelativity) -- same SVG visual language (dark background,
monospace, stacked panels, shadow/connector lines, ghost outlines for
inapplicable channels). That instrument stacks the 5 CD layers for one
input. This one stacks exactly two panels, because factorial relativity
has exactly two facets, not five:
    FERMAT panel (the PROMPT)  -- which N-shape (0..15) does this number
        occupy, and which root-system pathway (tap root / Monster gap /
        dendritic / even) does that shape belong to? Discrete, structural,
        already-built (telperion_engine.py, fermat_monster_engine.py).
    RIEMANN panel (the RESPONSE) -- where does that N-shape's REAL,
        counted prime density sit relative to Dirichlet equidistribution?
        Continuous, statistical, the actual control this project measured
        (engine.maths.equidistribution_control_test).
"Fermat Defines. Riemann Fires." (fermat_monster_engine.py's own title)
-- read literally here: the Fermat panel asks the question, the Riemann
panel is what the real data answers back. A connector line links a
number's own channel across both panels, prompt to response.
Usage:
    python3 oscilloscope.py <N>   # outputs factorial_oscilloscope.svg
```

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). See also the [Tools Reference](Tools-Reference.md).*
