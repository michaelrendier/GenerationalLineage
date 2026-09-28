# Reproducibility — how every claim in this repository is checked, and how to re-run it

This page is the repository's reproducibility statement. It is deliberately per-component (the same granularity as the provenance
labels) rather than per-paper: a reader should be able to see, for any tool, *what* is checked, *how strongly*, and *with which
command*.

## The four layers of checking

| layer | what it is | how to run it | what a pass means |
|---|---|---|---|
| **1. `verify()` on every toolset** | each of the 28 registered toolsets carries a self-check | `python3 -m engine --verify` | every toolset that ran passed (skips are listed, never counted as passes) |
| **2. the 44 lineage relations** | named claims about the tier-0 floor, the two trees, the pathway layer, the fractal block, each checked against computed data, three-way status | `python3 engine/lineage.py` (≈ 15 s) | `44/44 HOLD` |
| **3. the test suite** | 158 tests: every toolset's self-check, the refusal contract of the ten new toolsets, the dispatcher, all 43 tutorials run standalone, every committed transcript equals what the code prints today, every Python block in the README runs, every README anchor and every relative link in the README and wiki resolves, the CLI, package metadata, the GPL notice on every source file | `pip install -r requirements-dev.txt && python3 -m pytest` | Core: `156 passed, 2 skipped`; Extended: `158 passed` |
| **4. generated documentation** | the tutorial transcripts and the parts of the README/wiki that mirror the code are *generated*, and a staleness check exists for both | `python3 devtools/transcript.py --check-all` · `python3 devtools/build_docs.py --check` | `stale …: none` |

`HOLDS` means the engine's own check passed; it is not a proof of any external conjecture (see the README's *Known limitations*).

## Per component

Labels as defined in the README: **ESTABLISHED** (a published algorithm or theorem, cited), **OURS** (this project's contract or
construction), **THEORETICAL** (stated, not established). "Exhaustive" means every case in the stated finite space was run.

| component | label | check | strength | where the numbers are |
|---|---|---|---|---|
| the toolset contract, `AscentNotFree` refusal | OURS | `tests/test_toolsets.py`: every module has the contract; the ten new toolsets refuse an empty target | exhaustive over toolsets | test suite |
| `verify_all()` skip/complete accounting | OURS | Core vs Extended runs from clean clones | both modes run | [INSTALL.md](../INSTALL.md) |
| `periodicity` | ESTABLISHED | three routes vs brute force; Fine–Wilf; extremal words | exhaustive: all binary strings ≤ 14 (32,766) | [Periodicity](Periodicity.md) |
| `lyndon` | ESTABLISHED | unique factorisation; Möbius and Burnside counts; least rotation | exhaustive: binary strings ≤ 10 (2,046) | [Lyndon-Words](Lyndon-Words.md) |
| `berlekamp_massey` | ESTABLISHED | recovery of primitive polynomials degree 2–16; reducible cases | exhaustive over seeds (94), degrees 2–16 | [Berlekamp-Massey](Berlekamp-Massey.md) |
| `logperiodic` | ESTABLISHED (maths) · numerical fit | Γ identity, scaling identity, planted-ω recovery, control | sampled/analytic; noise not characterised | [Log-Periodic-and-Mellin](Log-Periodic-and-Mellin.md) |
| `permutation` | ESTABLISHED | sign/rank/conjugation; affine law; shuffle orders; min degree | exhaustive over S₁–S₇ (5,913) | [Permutation](Permutation.md) |
| `rejewski` | ESTABLISHED | known-answer vector; involution at every state; plugboard invariance; catalogue partition | exhaustive over 17,576 states; 300 invariance checks | [Rejewski](Rejewski.md) |
| `jordan_chevalley` | ESTABLISHED | exact identities re-checked on seven structures | exact rational arithmetic | [Jordan-Chevalley](Jordan-Chevalley.md) |
| `re_pair` | ESTABLISHED (minimality: not claimed) | exact round trip | exhaustive: 11,471 sequences | [Re-Pair](Re-Pair.md) |
| `pohlig_hellman` | ESTABLISHED | every element of four subgroups solved and verified | exhaustive: 19,704 elements | [Pohlig-Hellman](Pohlig-Hellman.md) |
| `unicity` | ESTABLISHED | Shannon's 27.6; counting core exact | exhaustive on a toy language n = 1…7 | [Unicity](Unicity.md) |
| the 44 relations, the older toolsets | mixed (see each page) | `engine/lineage.py`, each toolset's `verify()` | as each states | README §5, [Tools-Reference](Tools-Reference.md) |
| Clay-problem mappings, σ_RB / Cayley–Dickson readings | THEORETICAL | consistency checks only | a structural reading, not a solution | README §4.12 |

## Environment

Run-tested on: Linux (Ubuntu, kernel 6.8), **Python 3.12.3**, numpy **2.4.6** and **2.5.3**. The code is syntax-checked for Python ≥ 3.9
(`ast.parse` with `feature_version=(3, 9)`, and no runtime-evaluated `X | None` annotations) but has not been *run* there. Windows and
macOS have not been run. Clean-clone installs were verified in fresh virtual environments — Core with numpy only, and Extended with
the four sibling repositories cloned beside it.

## Determinism

- **No result depends on an unseeded random source.** Every use of randomness in the engine, the tests and the tutorials takes a fixed
  seed (`random.Random(seed)`, `np.random.default_rng(seed)`).
- **Tutorial transcripts are exact.** `devtools/transcript.py` runs each script through a REPL-style executor (Python's own `single`
  compile mode, so a bare expression echoes its `repr` even inside a `try`), and the test suite compares the committed transcript to the
  regenerated one byte for byte. Anything machine-dependent is deliberately not printed (the `cs_benchmark` tutorial prints only that
  a time is positive).
- **Numeric reprs** that differ across numpy major versions (`np.True_` versus `True`) are avoided in the tutorials by wrapping in
  `bool()` / `round()`; the transcripts match on numpy 2.4.6 and 2.5.3.

## What is not checked

- Python < 3.12, Windows and macOS: not run.
- `logperiodic` under noise; `re_pair` and `jordan_chevalley` at large sizes.
- The two notebooks: executed headlessly by hand (both run clean, 6 and 5 code cells), not in CI.
- The Extended layer's *content* beyond its self-check: it is imported from four repositories that are separate projects.
- Anything labelled **THEORETICAL**: by definition, not established.

## Reproduce everything

```bash
git clone https://github.com/michaelrendier/GenerationalLineage.git && cd GenerationalLineage
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python3 -m engine --verify                    # layer 1
python3 engine/lineage.py | tail -3           # layer 2
python3 -m pytest -q                          # layer 3
python3 devtools/transcript.py --check-all    # layer 4
python3 devtools/build_docs.py --check        # layer 4
```
