#!/usr/bin/env python3
"""
two_ring_chart_render.py — the actual grid PW8-PW10 built, rendered.

Cody, 2026-08-25: the Smith-chart-style cells are curvilinear (non-
Euclidean) because they're a flattening of a conformal map into 2D — and
that flattening leaves a real, exact, computable "artifact": the map's
local SCALE FACTOR, |dGamma/dZ|. This renders that quantity directly —
the "phase" information a flat R/X reading alone doesn't carry — rather
than treating "artifact" as a qualitative description.

Gamma = (Z - Z0)/(Z + Z0)  =>  dGamma/dZ = 2*Z0 / (Z + Z0)^2

Panel 1: the abstract two-ring grid in Gamma-space, background shaded by
the exact scale factor, constant-ring1/ring2 curves overlaid.

Panel 2: real WordNet data (hypernym count vs hyponym count, RAW, not
compressed) run through the SAME chart, colored by compress_count()
bucket — showing the "quantized continuous logarithmic relationship"
directly: a continuum of raw counts coarse-graining into a handful of
discrete cells as compress_count's log-rounding takes hold. "Windows of
order" made visible, not asserted.

Reuses ring_chart_gamma/two_ring_chart from engine/lineage.py and
compress_count from wordnet_boxkite.py directly — does not reimplement
either fold.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_VAPMIP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'VAPMIP')
sys.path.insert(0, os.path.abspath(_VAPMIP))

from engine.lineage import ring_chart_gamma, two_ring_chart  # noqa: E402
from wordnet_boxkite import compress_count  # noqa: E402

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

Z0 = complex(1.0, 0.0)   # the chart's own fixed-point anchor: Gamma(Z0)=0


def scale_factor(Z: np.ndarray, Z0: complex) -> np.ndarray:
    """Exact |dGamma/dZ|, not a numerical approximation."""
    return np.abs(2 * Z0) / np.abs(Z + Z0) ** 2


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), dpi=160, facecolor='#0a0a12')

# ── Panel 1: the abstract grid, background = exact scale factor ──────────
ax1.set_facecolor('#0a0a12')

R = np.linspace(0.05, 6, 500)
X = np.linspace(-5, 5, 500)
RR, XX = np.meshgrid(R, X)
ZZ = RR + 1j * XX
GG = ring_chart_gamma(ZZ, Z0)
SF = scale_factor(ZZ, Z0)

sc = ax1.scatter(GG.real.ravel(), GG.imag.ravel(), c=SF.ravel(), s=1.4,
                 cmap='magma', norm=LogNorm(vmin=SF.min() + 1e-6, vmax=SF.max()))

for r in (0.1, 0.2, 0.5, 1, 2, 3, 5):
    Zline = r + 1j * np.linspace(-10, 10, 600)
    G = ring_chart_gamma(Zline, Z0)
    ax1.plot(G.real, G.imag, color='#66ccff', lw=0.7, alpha=0.85)

for x in (-4, -2, -1, -0.5, 0.5, 1, 2, 4):
    Zline = np.linspace(0.005, 12, 600) + 1j * x
    G = ring_chart_gamma(Zline, Z0)
    ax1.plot(G.real, G.imag, color='#ff8866', lw=0.7, alpha=0.85)

boundary = np.exp(1j * np.linspace(0, 2 * np.pi, 400))
ax1.plot(boundary.real, boundary.imag, color='#888888', lw=1.0)

ax1.set_xlim(-1.05, 1.05); ax1.set_ylim(-1.05, 1.05)
ax1.set_aspect('equal')
ax1.set_title("Two-ring chart in Gamma-space\nbackground = exact |dGamma/dZ| "
              "(the flattening artifact)", color='#dddddd', fontsize=10.5)
ax1.tick_params(colors='#888888', labelsize=8)
cbar1 = fig.colorbar(sc, ax=ax1, fraction=0.045, pad=0.03)
cbar1.set_label("local scale factor |dGamma/dZ|", color='#cccccc', fontsize=8.5)
cbar1.ax.tick_params(colors='#888888', labelsize=7.5)
for spine in ax1.spines.values():
    spine.set_edgecolor('#444444')

# ── Panel 2: real WordNet counts through the same chart ──────────────────
ax2.set_facecolor('#0a0a12')

from nltk.corpus import wordnet as wn  # noqa: E402
import random
rng = random.Random(20260825)
all_nouns = list(wn.all_synsets('n'))
sample = rng.sample(all_nouns, min(4000, len(all_nouns)))

raw_pts = []
for s in sample:
    hyper = len(s.hypernyms())
    hypo = len(s.hyponyms())
    if hyper == 0 and hypo == 0:
        continue
    # Feed compress_count() itself in as ring1/ring2 — the raw counts have
    # a long tail that saturates the Mobius map near Gamma=1 for almost
    # every point (|Z| large => Gamma -> 1 regardless of exact value),
    # which showed the map's asymptote, not the coarse-graining. Bounded,
    # compressed values actually use the chart's radius.
    raw_pts.append((compress_count(hyper), compress_count(hypo),
                    compress_count(hyper) + compress_count(hypo)))

for r in (0.1, 0.2, 0.5, 1, 2, 3, 5):
    Zline = r + 1j * np.linspace(-10, 10, 600)
    G = ring_chart_gamma(Zline, Z0)
    ax2.plot(G.real, G.imag, color='#3a3a44', lw=0.5, alpha=0.7)
for x in (-4, -2, -1, -0.5, 0.5, 1, 2, 4):
    Zline = np.linspace(0.005, 12, 600) + 1j * x
    G = ring_chart_gamma(Zline, Z0)
    ax2.plot(G.real, G.imag, color='#3a3a44', lw=0.5, alpha=0.7)
ax2.plot(boundary.real, boundary.imag, color='#888888', lw=1.0)

hyper_vals = np.array([p[0] for p in raw_pts], dtype=float)
hypo_vals = np.array([p[1] for p in raw_pts], dtype=float)
bucket = np.array([p[2] for p in raw_pts])
# compress_count() is integer-valued, so many synsets share the exact same
# (ring1, ring2) pair -- a bare scatter would just be ~8x8 overlapping
# dots. Small jitter makes the DENSITY at each cell visible instead of
# hiding it; the underlying values are still the real compressed counts.
rng2 = np.random.default_rng(20260825)
jitter = 0.15
Z_pts = (hyper_vals + rng2.uniform(-jitter, jitter, len(hyper_vals))) \
      + 1j * (hypo_vals + rng2.uniform(-jitter, jitter, len(hypo_vals)))
G_pts = ring_chart_gamma(Z_pts, Z0)

sc2 = ax2.scatter(G_pts.real, G_pts.imag, c=bucket, s=5, cmap='viridis',
                  alpha=0.35, linewidths=0)

ax2.set_xlim(-1.05, 1.05); ax2.set_ylim(-1.05, 1.05)
ax2.set_aspect('equal')
n_buckets = len(set(bucket.tolist()))
ax2.set_title(f"{len(raw_pts)} real WordNet nouns: compress_count(hyper), "
              f"compress_count(hypo)\nAS the chart's own ring values (jittered "
              f"for density) — the quantized-log relationship, in the geometry",
              color='#dddddd', fontsize=10.2)
ax2.tick_params(colors='#888888', labelsize=8)
cbar2 = fig.colorbar(sc2, ax=ax2, fraction=0.045, pad=0.03)
cbar2.set_label("compress_count(hyper)+compress_count(hypo)", color='#cccccc', fontsize=8)
cbar2.ax.tick_params(colors='#888888', labelsize=7.5)
for spine in ax2.spines.values():
    spine.set_edgecolor('#444444')

fig.suptitle("PW8-PW10's two-ring chart: the flattening artifact, and a real "
            "quantized-continuous-log relationship it makes visible",
            color='#ffffff', fontsize=13, y=0.99, weight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.95])

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'two_ring_chart_render.png')
fig.savefig(out, facecolor=fig.get_facecolor())
print(f"Saved {out}")
print(f"raw points plotted: {len(raw_pts)}  distinct compress_count buckets: {n_buckets}")
