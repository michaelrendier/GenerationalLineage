"""SedenionFactoralRelativity.engine.spectral

General spectral decomposition — **not tied to the sedenion framework.**

"Spectral analysis IS factoral decomposition, using a different order datum"
(Cody, 2026-08-25). This engine already factors numbers (`factor_lineage`),
processes (`pathway_decomposition`), units (`unit_lineage_decompose`) and the
sieve (`sieve_recurrence`). This module adds the missing one: factoring a
**signal into its wavelengths**, with the leftover reported as the residual —
the same "what no component absorbs" reading the BAO mass gap uses, made general.

    signal            = the composite
    each spectral line = an irreducible wavelength factor  (a leaf)
    the residual       = what remains after the kept factors are removed

stdlib + numpy only. Works on any real or complex sequence.
"""
from __future__ import annotations

import cmath
import math
from typing import Any, Dict, List, Optional, Sequence

import numpy as np


# ═══════════════════════════════════════════════════════════════════════════
# transform
# ═══════════════════════════════════════════════════════════════════════════

def dft(x: Sequence[complex]) -> np.ndarray:
    """The discrete Fourier transform  X[k] = Σ_n x[n] e^{-2πi kn/N}.
    Complex input allowed; returns the full length-N complex spectrum."""
    return np.fft.fft(np.asarray(x, dtype=complex))


def idft(X: Sequence[complex]) -> np.ndarray:
    """Inverse of `dft`."""
    return np.fft.ifft(np.asarray(X, dtype=complex))


def power_spectrum(x: Sequence[complex]) -> np.ndarray:
    """|X[k]|² / N  — the power at each frequency bin (Parseval-normalised so
    the sum equals the mean square of x)."""
    X = dft(x)
    n = len(X)
    return (np.abs(X) ** 2) / (n * n)


# ═══════════════════════════════════════════════════════════════════════════
# the wavelength factors
# ═══════════════════════════════════════════════════════════════════════════

def spectral_lines(x: Sequence[complex], *, sample_rate: float = 1.0,
                   top: Optional[int] = None, min_rel_power: float = 1e-9,
                   real_signal: Optional[bool] = None) -> List[Dict[str, Any]]:
    """Factor a signal into its wavelengths.

    Returns one dict per line, sorted by power (strongest first):
        k          bin index
        freq       cycles per sample-unit  (k * sample_rate / N)
        wavelength 1 / freq   (∞ for the DC / k=0 term)
        amplitude  peak amplitude of that sinusoid
        phase      radians
        power      |X[k]|²/N²   (fraction of the signal's mean square, if real)
        rel_power  power / total power

    For a real input the k and N-k bins are one physical wavelength; they are
    merged and the amplitude doubled (except DC and Nyquist).
    """
    x = np.asarray(x, dtype=complex)
    N = len(x)
    if N == 0:
        return []
    if real_signal is None:
        real_signal = bool(np.allclose(x.imag, 0.0))

    X = np.fft.fft(x)
    total_pow = float(np.sum(np.abs(X) ** 2) / (N * N)) or 1.0

    seen = set()
    lines: List[Dict[str, Any]] = []
    for k in range(N):
        if k in seen:
            continue
        kk = (N - k) % N
        if real_signal and kk != k:
            seen.add(kk)
            amp = 2.0 * abs(X[k]) / N
            p = (abs(X[k]) ** 2 + abs(X[kk]) ** 2) / (N * N)
        else:
            amp = abs(X[k]) / N
            p = (abs(X[k]) ** 2) / (N * N)
        rel = p / total_pow
        if rel < min_rel_power:
            continue
        freq = k * sample_rate / N
        lines.append({
            'k': k,
            'freq': freq,
            'wavelength': (float('inf') if freq == 0 else 1.0 / freq),
            'amplitude': amp,
            'phase': cmath.phase(X[k]),
            'power': p,
            'rel_power': rel,
        })
    lines.sort(key=lambda d: d['power'], reverse=True)
    if top is not None:
        lines = lines[:top]
    return lines


def reconstruct(lines: Sequence[Dict[str, Any]], n: int, *,
                sample_rate: float = 1.0) -> np.ndarray:
    """Sum the identified wavelength components back into a length-n real signal.
    A line with k in (0, N/2) is a real cosine of the given amplitude/phase; DC
    is a constant; Nyquist is an alternating term."""
    t = np.arange(n)
    y = np.zeros(n, dtype=float)
    for L in lines:
        k = L['k']
        if k == 0:
            y += L['amplitude'] * math.cos(L['phase'])
        elif 2 * k == n:                       # Nyquist
            y += L['amplitude'] * np.cos(math.pi * t + L['phase'])
        else:
            y += L['amplitude'] * np.cos(2.0 * math.pi * k * t / n + L['phase'])
    return y


# ═══════════════════════════════════════════════════════════════════════════
# the residual  —  "what no component absorbs"
# ═══════════════════════════════════════════════════════════════════════════

def spectral_residue(x: Sequence[float], keep: int, *,
                     sample_rate: float = 1.0) -> Dict[str, Any]:
    """Keep the `keep` strongest wavelength factors, subtract them, and report
    the leftover — the residual. `residual_rel` is the residual's RMS as a
    fraction of the signal's RMS: 0 = fully resolved, → 1 = nothing resolved."""
    x = np.asarray(x, dtype=float)
    N = len(x)
    lines = spectral_lines(x, sample_rate=sample_rate, top=keep, min_rel_power=0.0)
    recon = reconstruct(lines, N, sample_rate=sample_rate)
    residual = x - recon
    sig_rms = float(np.sqrt(np.mean(x ** 2))) or 1.0
    res_rms = float(np.sqrt(np.mean(residual ** 2)))
    explained = 1.0 - res_rms / sig_rms
    return {
        'keep': keep,
        'lines': lines,
        'reconstruction': recon,
        'residual': residual,
        'residual_rms': res_rms,
        'residual_rel': res_rms / sig_rms,
        'explained': explained,
        'signal_rms': sig_rms,
    }


# ═══════════════════════════════════════════════════════════════════════════
# period detection  (frequency-space; complements repeat_distances / Kasiski)
# ═══════════════════════════════════════════════════════════════════════════

def autocorrelation(x: Sequence[float]) -> np.ndarray:
    """Biased autocorrelation r[τ] = (1/N) Σ_n x[n] x[n+τ], τ = 0 .. N-1,
    via the spectrum (Wiener–Khinchin): r = IDFT(|DFT(x)|²)."""
    x = np.asarray(x, dtype=float)
    x = x - x.mean()
    N = len(x)
    S = np.abs(np.fft.fft(x, 2 * N)) ** 2
    r = np.fft.ifft(S).real[:N] / N
    return r


def dominant_period(x: Sequence[float], *, min_period: int = 2,
                    max_period: Optional[int] = None) -> Dict[str, Any]:
    """The strongest period, read from the autocorrelation's first major peak
    after τ=0. Returns the period (in samples), its normalised correlation
    strength, and the frequency-space cross-check."""
    r = autocorrelation(x)
    N = len(r)
    hi = min(max_period or N // 2, N - 1)
    # cross-check against the strongest single spectral line
    ps = power_spectrum(np.asarray(x, float) - np.mean(x))
    kbin = int(np.argmax(ps[1:N // 2]) + 1)
    freq_period = N / kbin if kbin else None
    if hi <= min_period:
        return {'period': freq_period, 'strength': 0.0, 'freq_bin': kbin,
                'freq_space_period': freq_period}
    # the autocorrelation "repeating-pattern" period: the first LOCAL maximum
    # after tau=0 (skip the monotonic-decay shoulder that noise/multi-period
    # signals put right after 0)
    tau = None
    for t in range(min_period, hi):
        if r[t] >= r[t - 1] and r[t] >= r[t + 1] and r[t] > 0:
            tau = t
            break
    if tau is None:                       # no clean autocorrelation peak
        tau = int(round(freq_period)) if freq_period else None
        ambiguous = True
    else:
        ambiguous = False
    strength = float(r[tau] / r[0]) if (tau and r[0]) else 0.0
    return {'period': tau, 'strength': strength, 'ambiguous': ambiguous,
            'freq_bin': kbin, 'freq_space_period': freq_period}


# ═══════════════════════════════════════════════════════════════════════════
# the full decomposition
# ═══════════════════════════════════════════════════════════════════════════

def spectral_decompose(x: Sequence[float], *, sample_rate: float = 1.0,
                       keep: Any = 'auto', rel_power_floor: float = 1e-4,
                       converge_tol: float = 1e-3) -> Dict[str, Any]:
    """Full spectral / wavelength factoring of a signal.

    keep = 'auto'  : keep every line above `rel_power_floor`
         = int     : keep that many strongest lines
         = 'all'   : keep all N lines (exact round-trip)

    Reports the wavelength factors, the residual after them, a Parseval
    round-trip check, and a **residue convergence trace** — residual_rel as a
    function of how many lines are kept — flagging when it plateaus (the
    generalisation of "the residue does not move once the real content is out",
    the BAO reading).
    """
    x = np.asarray(x, dtype=float)
    N = len(x)
    all_lines = spectral_lines(x, sample_rate=sample_rate, min_rel_power=0.0)

    if keep == 'all':
        k_keep = len(all_lines)
    elif keep == 'auto':
        k_keep = max(1, sum(1 for L in all_lines if L['rel_power'] >= rel_power_floor))
    else:
        k_keep = int(keep)

    res = spectral_residue(x, k_keep, sample_rate=sample_rate)

    # Parseval: does the full line set carry all the signal's energy?
    tot_line_pow = sum(L['power'] for L in all_lines)
    sig_ms = float(np.mean(x ** 2))
    parseval_err = abs(tot_line_pow - sig_ms) / (sig_ms or 1.0)

    # residue convergence trace: 1, 2, 4, 8, ... lines
    trace, ks, prev = [], [], None
    kk = 1
    while kk <= len(all_lines):
        rr = spectral_residue(x, kk, sample_rate=sample_rate)['residual_rel']
        trace.append(rr)
        ks.append(kk)
        if prev is not None and abs(prev - rr) < converge_tol and kk >= k_keep:
            break
        prev = rr
        kk *= 2
    plateau_at = None
    for i in range(1, len(trace)):
        if abs(trace[i] - trace[i - 1]) < converge_tol:
            plateau_at = ks[i]
            break

    return {
        'n_samples': N,
        'sample_rate': sample_rate,
        'n_lines_total': len(all_lines),
        'lines_kept': k_keep,
        'wavelength_factors': res['lines'],       # the leaves
        'residual': res['residual'],
        'residual_rel': res['residual_rel'],      # RMS residual / RMS signal
        'explained_fraction': res['explained'],
        'round_trip_parseval_error': parseval_err,
        'round_trip_exact': parseval_err < 1e-9,
        'residue_trace_keep': ks,
        'residue_trace_rel': trace,
        'residue_plateaus_at': plateau_at,        # kept lines past which the residual stops moving
        'reading': ('signal = composite; each wavelength_factor = an irreducible '
                    'leaf; residual = what remains after them — the residue no '
                    'wavelength absorbs'),
    }


if __name__ == '__main__':
    rng = np.random.default_rng(20260828)
    N = 512
    t = np.arange(N)
    # three known wavelengths + a small noise floor
    truth = [(1/32, 1.0, 0.3), (1/16, 0.5, 1.1), (1/8, 0.25, -0.7)]
    x = sum(A * np.cos(2*math.pi*f*t + ph) for (f, A, ph) in truth)
    x = x + 0.02 * rng.standard_normal(N)

    print("SPECTRAL DECOMPOSITION — general (no sedenion)\n" + "=" * 52)
    d = spectral_decompose(x, keep='auto')
    print(f"  {N} samples, {d['n_lines_total']} lines total, {d['lines_kept']} kept")
    print(f"  round-trip Parseval error : {d['round_trip_parseval_error']:.2e} "
          f"(exact: {d['round_trip_exact']})")
    print(f"  residual (RMS frac)        : {d['residual_rel']:.4f}   "
          f"explained {d['explained_fraction']*100:.2f}%")
    print(f"  residue plateaus at        : {d['residue_plateaus_at']} lines")
    print(f"  residue trace  keep={d['residue_trace_keep']}")
    print(f"                 rel ={[round(v,4) for v in d['residue_trace_rel']]}")
    print("  recovered wavelength factors (top 4):")
    for L in d['wavelength_factors'][:4]:
        print(f"    λ={L['wavelength']:8.3f}  f={L['freq']:.5f}  "
              f"A={L['amplitude']:.4f}  φ={L['phase']:+.3f}  "
              f"rel_pow={L['rel_power']:.4f}")
    print("  truth: " + ", ".join(f"λ={1/f:.1f}(A={A})" for f, A, _ in truth))

    per = dominant_period(x)
    print(f"\n  dominant_period: {per['period']} samples "
          f"(strength {per['strength']:.3f}); freq-space {per['freq_space_period']:.2f}")

    # exact round trip on a clean signal
    clean = np.cos(2*math.pi*t*5/N) + 0.4*np.cos(2*math.pi*t*17/N + 0.9)
    dc = spectral_decompose(clean, keep='all')
    print(f"\n  clean signal, keep=all: residual_rel = {dc['residual_rel']:.2e}, "
          f"round-trip exact = {dc['round_trip_exact']}")
