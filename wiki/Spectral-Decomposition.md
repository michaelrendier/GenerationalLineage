# 4.13 General spectral decomposition — factoring wavelengths  `[not sedenion-specific]`

`engine/spectral.py` · *Tutorial:* [`07_spectral`](../examples/07_spectral.py). "Spectral analysis IS factoral decomposition, using a
different order datum" (Cody). This engine factors numbers, processes, units and
the sieve; this module adds **factoring a signal into its wavelengths**, with
the leftover reported as the residual — the BAO "what no component absorbs"
reading, made general. stdlib + numpy, works on any real or complex sequence.

```python
import math
from engine import spectral_decompose, spectral_lines, spectral_residue, dominant_period

signal = [math.sin(2 * math.pi * 5 * i / 64) + 0.5 * math.sin(2 * math.pi * 12 * i / 64) for i in range(64)]
d = spectral_decompose(signal, keep='auto')      # or keep=int, keep='all'
d['wavelength_factors']   # the leaves: [{wavelength, freq, amplitude, phase, power, rel_power}, ...]
d['residual']             # what no wavelength absorbs
d['residual_rel']         # RMS residual / RMS signal  (0 = fully resolved)
d['round_trip_exact']     # Parseval: do the lines carry all the signal's energy?
d['residue_plateaus_at']  # kept lines past which the residual stops moving
```

| function | does |
|---|---|
| `dft` / `idft` / `power_spectrum` | the transform and `|X|²/N` |
| `spectral_lines(x, top=, min_rel_power=)` | the wavelength factors, strongest first; real inputs merge the ±k bins |
| `reconstruct(lines, n)` | sum the identified components back |
| `spectral_residue(x, keep)` | keep the top `keep` lines, subtract, report the leftover |
| `autocorrelation` / `dominant_period` | frequency-space period detection — complements the position-space `repeat_distances` / Kasiski already here |
| `spectral_decompose(x, keep=)` | the full report + a **residue convergence trace** (residual_rel vs lines kept; flags where it plateaus — the generalisation of "the residue does not move once the real content is out") |

*Reading:* signal = composite; each `wavelength_factor` = an irreducible leaf;
residual = the residue no wavelength absorbs. Verified: 3 planted sinusoids +
noise → all three λ, amplitudes and phases recovered, round-trip Parseval error
`1e-15`, residual = the noise floor, plateau detected. The sibling `SedenionSpectralRelativity`
repository remains the sedenion-specific spectrograph; this is the algebra-free tool.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
