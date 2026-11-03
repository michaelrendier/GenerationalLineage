# 4. How to use it — the tools

All examples assume you're in the repository root with `import engine` working (see [Install](../README.md#install)).
`engine.EXTENDED` is `True` when the three sibling repositories were found; sections tagged `[EXTENDED]` need it, everything else
runs on a Core install. Each subsection names its runnable tutorial in [`examples/`](../examples/) (the
[tutorial index](Tutorial-Index.md) lists them all).

## 4.1 Run the whole self-check

*Tutorials:* [`01_quickstart`](../examples/01_quickstart.py), [`02_the_two_lines`](../examples/02_the_two_lines.py).

```bash
python3 engine/lineage.py          # 44/44, ~15s, verbose report
python3 -m engine --verify         # every toolset checks itself (see Install)
```
```python
from engine import run_lineage
result = run_lineage(verbose=True)  # same thing, importable
```

This is the thing to run first. It prints every relation in §5 with its
computed detail, then a one-line verdict: *"No new generator required. Every
operation above descends from the tier-0 floor by composition."* — or, if
something broke, exactly which relation and which of the three Status values
it got.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
