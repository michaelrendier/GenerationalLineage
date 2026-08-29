# ADD:SCALE:SIGN — the tier-0 datatype (engine + tool in the decomposer suite)

**Formal spec:** `Ainulindale/wiki/107_add_scale_sign_datatype.md` (canonical).
This page is the SFR-side view: the datatype as an **engine** and a **tool** in
the decomposer suite, and the fast inverse square root as its worked example.

**Files:** `engine/add_scale_sign.py` (`ASS`, `ASSWord`, `compose`, `word`,
`fast_inverse_sqrt`, `fisr_word`, `reduces_everything`) — exported from
`engine/__init__.py` as `ASS`, `ASSWord`, `ass_compose`, `ass_word`,
`fast_inverse_sqrt`, `fisr_word`, `reduces_everything`, `CAMSHAFT`,
`ASS_BRACKET`. Tool: `engine/tools.py` `report_add_scale_sign()`.

Standalone port per the module-independence convention — not a cross-repo
import. Same maths as `ValaQuenta/modules/add_scale_sign/`, verified the same
way.

---

## Why it belongs here

The whole decomposer suite (`lineage.py` `root_irreducible` / `ROOT_OF` /
`AFF1`, the roll-down, `decompose()`) *terminates* on ADD, SCALE or SIGN. Every
other module — `clay.py`, `spectral.py`, `bio.py`, `valaquenta_calibration.py`
— rolls its objects down to this floor. This module makes the floor an object
you can hold, compose, invert and read out, not just a label a roll-down stops
at. **This reduces everything** — `reduces_everything(op)` takes any named
operation to its tier-0 root and hands back the root as a live `ASS` generator.

## The value type (1-paragraph)

`ASS(add, scale, sign)` = `x ↦ sign·scale·x + add`. `@` composes, `~` inverts
(and reverses the record), `.residual('SCALE')` strips one generator keeping the
rest (the `str.strip` analogue), `.parts()` splits into `(SIGN, SCALE, ADD)` —
the camshaft order. Word `u = g·ln s + a`; fold `Γ = tanh(u/2)`; ground state
`(0,1,+1)` → `u=0` → `Γ=0`. Firing defect `(g−1)·ln s`. Two lineage orderings:
`chrono` (fired order) and `zeta` (by `|u_k|`). Full spec: wiki/107.

## The fast inverse square root — `fisr_word(x)`

`1/√x = exp(−½·ln x)` is the `ASS` word `SIGN(−1) ∘ SCALE(½)` on `ln x`. Quake
III's `0x5f3759df` computes exactly that in the IEEE-754 exponent field (native
`log₂`):

| step | ADD:SCALE:SIGN |
|---|---|
| `i >> 1` | SCALE by ½ — done as a **shift**, the multiply *skipped* |
| `MAGIC − …` | ADD (the bias offset) |
| sign bit untouched | SIGN |

Mantissa linearity → "good enough" (~3.4 % raw); one Newton step is the
**residual** (~0.17 %). Run: `report_add_scale_sign()`.

## Status v-note

Added to `engine/__init__.py` and `engine/tools.py` 2026-08-28. `run_lineage`
and the existing suite are unaffected (additive). The canonical maths reference
carries the generalized equation `u = Σ_k [g_k·ln s_k + a_k]`, `Γ = tanh(u/2)`.
