# Install

GenerationalLineage is pure Python 3. It needs **one** third-party package, `numpy`; everything else it imports is the standard library. It is syntax-checked for Python ≥ 3.9 and **run-tested on Python 3.12.3** (numpy 2.4.6 and 2.5.3); older Pythons have not been run.

There are two ways to install it. Almost everything is in the **Core**; the **Extended** layer adds three optional features that reach into sibling repositories.

| | Core | Extended |
|---|---|---|
| what you get | the whole engine: 27 toolsets, the lineage/emerger/ping engines, all tutorials except `90_`, all wiki pages | Core **plus** `engine.maths`, `engine.tools`, `engine.oscilloscope` (the Fermat-facet inventory, the control test, the two-panel SVG) |
| needs | this repository + numpy | this repository + numpy + three sibling repositories cloned beside it |
| `python3 -m engine --verify` | `27 toolsets ran, 27 passed, 1 skipped` | `28 toolsets ran, 28 passed, 0 skipped` |

## Core install

```bash
git clone https://github.com/michaelrendier/GenerationalLineage.git
cd GenerationalLineage
python3 -m venv .venv
source .venv/bin/activate                 # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 -m engine --verify
```

Expected — the last lines:

```text
27 toolsets ran, 27 passed, 1 skipped
RESULT: PASS  (core; extended layer skipped)
```

The one skipped toolset is `oscilloscope`, which belongs to the Extended layer. A skip is reported as a skip, never as a pass: on a Core install `lines.verify_all()` returns `_ok = True` and `_complete = False`.

Check what you have:

```bash
python3 -m engine
```

```text
GenerationalLineage 1.0.0  ·  mode: CORE
python 3.12.3  ·  numpy 2.5.3
extended layer absent: ModuleNotFoundError("No module named 'telperion_engine'")
  (expected on a plain clone — see README, 'Extended install')
```

Run everything from the repository root: the tutorials and the tests use `import engine` with the repository root on the path.

## Development install (tests, notebooks, optional features)

```bash
pip install -r requirements-dev.txt
python3 -m pytest
```

Expected on a Core install: `156 passed, 2 skipped` (the two skips are extended-only checks). On an Extended install: `158 passed`.

`requirements-dev.txt` adds `pytest`, plus `sympy` (the operator-string parser's SymPy output) and `matplotlib` (optional PNG rendering), plus `nbformat`, `nbconvert` and `ipykernel` to execute the two notebooks in `notebooks/`.

Optionally install the package into the virtual environment:

```bash
pip install -e .
```

The importable package is called `engine` (see *Known limitations* in the README) — install it into a virtual environment, not beside another top-level package of the same name.

## Extended install

The Extended layer finds its three sibling repositories **in the same parent directory** as this one (`../AbrikosovTree`, and so on). Clone them side by side:

```bash
mkdir ThePlace && cd ThePlace
for r in GenerationalLineage AbrikosovTree ValaQuenta FourthAgePapers; do
    git clone https://github.com/michaelrendier/$r.git
done
cd GenerationalLineage
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m engine --verify --strict       # --strict: exit 0 only if NOTHING was skipped
```

Expected — the last lines:

```text
28 toolsets ran, 28 passed, 0 skipped
RESULT: PASS
```

and `python3 -m engine` reports `mode: EXTENDED`.

The three siblings are separate projects with their own licences; the Extended layer imports their code at run time and nothing from them is copied into this repository. What each one supplies: `AbrikosovTree` (`telperion_engine`, the 9-level Cayley–Dickson walk), `ValaQuenta` (the `h_rb_hat` maths and the box-kite maths), `FourthAgePapers` (`FermatMonster/engine`, which `telperion_engine` needs on its path). (A fourth sibling, `TuringStack`, was needed through 1.0.0 for a GF(2) Cayley–Dickson multiplier; that dependency was replaced 2026-09-28 with this repository's own `engine.lineage.cd_mul_gf2` — checked bit-identical and faster — so `TuringStack` is no longer required here.)

## Troubleshooting

| you see | it means | do this |
|---|---|---|
| `ModuleNotFoundError: No module named 'numpy'` | the virtual environment is not active, or `pip install -r requirements.txt` was skipped | activate `.venv`, reinstall |
| `mode: CORE` and `extended layer absent` | the three sibling repositories are not beside this one | expected on a plain clone; do the Extended install if you want them |
| `--strict` exits with status 2 | something was skipped | you are on a Core install; that is the honest answer |
| a tutorial or test cannot `import engine` | not run from the repository root | `cd` to the repository root first |
| `--verify` prints `FAIL` for a toolset | a real failure — please open an issue with the full output | include `python3 -m engine` output and your Python and numpy versions |

## Uninstall

Delete the directory (and the `.venv`). Nothing is written outside it.
