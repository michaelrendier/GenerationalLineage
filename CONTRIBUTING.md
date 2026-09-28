# Contributing to GenerationalLineage

Thank you for looking. This is an engineering tool that is meant to be read as one document, so contributions are judged on whether
they keep it *checkable*: exact where an exact check is possible, explicit where the engine refuses, and honest about what is
established and what is not.

## Licence of contributions

The project is under the **GNU GPL v3.0** (`LICENSE`). By submitting a contribution you agree that it is licensed under the same
terms (`GPL-3.0-only`), and every new source file must carry the notice (see any file in `engine/`; `tests/` and `examples/` use the
short three-line form). `tests/test_cli_and_release.py` fails if a source file lacks it.

## Set up

```bash
git clone https://github.com/michaelrendier/GenerationalLineage.git && cd GenerationalLineage
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m pytest -q                       # must pass before and after your change
```

Core is enough for almost everything. The Extended layer needs three sibling repositories cloned beside this one — see
[`INSTALL.md`](INSTALL.md).

## Adding a move (a toolset)

A move is a module in `engine/toolsets/` honouring the contract in `engine/lines.py`:

```python
NAME = "your_move"
LINE = "both"                       # "decomposition", "emerger" or "both"

def descend(x, **k): ...            # the FREE reading: a single pass, no search
def build_up(target, **k): ...      # the WORK reading: report `cost`; raise lines.AscentNotFree(owed) when it
                                    # is asked for something it cannot build from — the refusal is the result
def verify(): ...                   # return {"ok": bool, ...}; exhaustive where the space allows
```

Then, in this order:

1. **Register it** in `engine/lines.py` (`TOOLSETS`: module, line, one line each for `free` and `work`) and in
   `engine/toolsets/__init__.py`.
2. **Make `verify()` strong.** Prefer an exhaustive check over a finite space to a sample; check against an independent route
   (brute force, a known-answer vector, a second algorithm); test the *refusal*; include a control that should fail.
3. **Write the tutorial** `examples/NN_your_move.py`: a module docstring, then plain top-level statements. It must start from its own
   imports, must not depend on state from another tutorial, and must be deterministic (fixed seeds; nothing machine-dependent
   printed). Generate its transcript: `python3 devtools/transcript.py --write-all`.
4. **Document it.** Add an entry to `MOVES` in `devtools/build_docs.py` (definition, why, guarantee, limits, and a provenance table
   with a `ESTABLISHED` / `OURS` / `THEORETICAL` label per component and a citation for every established one) and a definition to
   `DEFINITIONS`; then `python3 devtools/build_docs.py`. `--check` must report nothing stale.
5. **Run everything:** `python3 -m pytest -q`, `python3 devtools/transcript.py --check-all`, `python3 devtools/build_docs.py --check`.

## House rules

- **Guarantee-first.** Exact or exhaustive over sampled; an explicit refusal over a confident approximation; an unknown reported as
  unknown (`minimal: None`, `period: None`, `determined: False`), never guessed.
- **Label provenance** in the same place as the claim. An established algorithm is cited, not re-derived as though it were new.
- **Say what a check does not cover.** Every move page has a *Limits* paragraph; write it.
- **Standard library and numpy only** in Core. Anything else goes behind an optional import with a clear failure.
- **Mathematics in Unicode** (ℤ, ≡, Σ, ⋊), not LaTeX, in prose and docstrings — the documentation is read in a terminal as often as
  a browser.
- Keep functions short enough to be read; where the code *is* the mechanism, show the code, not a formula standing in for it.

## Reporting bugs and proposing moves

Use the issue templates. For a bug: the output of `python3 -m engine`, your Python and numpy versions, and the smallest input that
shows it. For a proposed move: the *kind of factor*, the residual, why the descent is free, what the ascent must be given, the
exact check that would make it trustworthy, and the citation if it is established.

## Continuous integration

The CI definition is `.github/ci-workflow.yml`; see `.github/README.md` for how it is enabled. Whether or not CI is running, the
checks in *Adding a move*, step 5, are the bar.

## Conduct and security

See [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) and [`SECURITY.md`](SECURITY.md).
