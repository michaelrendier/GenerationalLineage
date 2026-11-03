# Appendix B — ValaQuenta — Generational Lineage Calibration

`engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`, which only prints; the figures below were checked
against a fresh run on 2026-09-28). The Millennium problems are *open* objects — of course they import. **ValaQuenta
is working, deliberately-designed machinery**, so running the same decomposition
on every ValaQuenta engine is a **calibration check on the factoral
decomposition itself**: a well-designed engine should come out **CLEAN**
(DEFINITIONAL, one clean tier-0 root, a definite Two-Trees node, no import
deficit, no emergence signature). The calibration number is *does the
generational-lineage verdict agree with ValaQuenta's own status label?*

```
engines            : 46
CLEAN              : 22   (decompose as designed)
DESCRIPTIVE-OK     :  6   (instruments / renderers / validators — construct nothing by design)
FLAGGED            : 18   (an import deficit or an emergence signature)

agreement w/ status: 0.957   (verdict matches ValaQuenta's own ESTABLISHED / THEORETICAL /
                              CONJECTURE / OPEN / UNTESTED / defect label)
confusion : CLEAN∩ESTABLISHED 21 · CLEAN∩soft 1 · FLAGGED∩soft 17 · FLAGGED∩ESTABLISHED 1
roots     : SCALE 16 · SIGN 15 · ADD 14 · none 1   (no bias in the tier-0 classifier)
trees     : LAURELIN 25 · MINGLING 11 · TELPERION 10   (most engines construct → Laurelin)

disagreements (the signal) —
  · bao_mass_gap   : FLAGGED (the 10³ factor is un-derived; "Δ = 1/(1000√2)" is a 3-sig-fig
                     coincidence, and the "spectral residue" is the same Ω−d*·ln10 subtraction
                     renamed) but the page says ESTABLISHED. See the Claim audit on that page.
  · t32_nilpotency : CLEAN (the trace-Laplacian test constructs cleanly) but the page says
                     THEORETICAL — the decomposition rates this engine more solid than its label.

  Was 3 disagreements — `noether` (recorded `forced_sigma` large-E defect) FIXED 2026-08-28
  (the balance F=B is linear in σ; one Newton step from any σ₀); FLAG cleared.
```

**Reading:** 95.7% agreement between an independent structural decomposition and
the hand-assigned status labels, on ~46 engines that were each explicitly
designed, is the calibration — the factoral decomposition recovers the design
status. The 18 FLAGGED-and-soft and 20 CLEAN-and-ESTABLISHED engines are the
method and the labels confirming each other; the 2 off-diagonal pairs are the
only places worth a second look. Per-engine blocks are appended toward the
bottom of each `ValaQuenta/wiki/*.md` page (in the sibling ValaQuenta repository; produced with `vq_wiki_block()`).

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
