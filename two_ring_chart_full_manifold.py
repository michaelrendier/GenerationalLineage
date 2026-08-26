#!/usr/bin/env python3
"""
two_ring_chart_full_manifold.py — the complete fold, both sides of the
unit circle, not just the conventional physical-impedance half.

Cody, 2026-08-25: "lets extend the chart to both complete set of rings,
not just the one section...we need the full set of rings to explore all
relationships across this manifold."

A real, printed Smith chart only shows Re(Z)>=0 (physical resistance
can't be negative), which maps entirely INSIDE the unit circle. That's a
deliberate, conventional restriction of the engineering instrument — the
Mobius fold itself is defined on the WHOLE extended complex plane
(equivalently, the Riemann sphere), and Re(Z)<0 is exactly as well-
defined mathematically, it just lands OUTSIDE the unit circle
(|Gamma|>1), where a passive impedance can never sit. This renders both
halves together: the conventional disk AND its exterior, one continuous
manifold, with the pole at Z=-Z0 (where Gamma blows up to infinity)
visible as the real singularity it is, not hidden by cropping the axes.

Reuses ring_chart_gamma/chart_scale_factor directly — no new fold, just
no longer throwing away half of what it's already defined on.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine.lineage import ring_chart_gamma, chart_scale_factor  # noqa: E402

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

Z0 = complex(1.0, 0.0)

fig, ax = plt.subplots(figsize=(10, 10), dpi=160, facecolor='#0a0a12')
ax.set_facecolor('#0a0a12')

# ── background: exact scale factor, BOTH sides of Re(Z)=0 ────────────────
R = np.linspace(-6, 6, 700)
X = np.linspace(-6, 6, 700)
RR, XX = np.meshgrid(R, X)
ZZ = RR + 1j * XX
with np.errstate(divide='ignore', invalid='ignore'):
    GG = ring_chart_gamma(ZZ, Z0)
    SF = chart_scale_factor(ZZ, Z0)

# clip the pole (Z=-Z0) neighbourhood -- Gamma -> infinity there, a real
# singularity of the map, not a rendering artifact to paper over
finite = np.isfinite(GG.real) & np.isfinite(GG.imag) & (np.abs(GG) < 8)
sc = ax.scatter(GG.real[finite], GG.imag[finite], c=SF[finite], s=1.0,
               cmap='magma', norm=LogNorm(vmin=SF[finite].min() + 1e-6,
                                          vmax=SF[finite].max()))

# ── constant-R circles, BOTH signs of R ────────────────────────────────────
for r in (-8, -5, -3, -2, -1.5, -1.2, -0.8, -0.5, -0.2,
         0.2, 0.5, 0.8, 1.2, 1.5, 2, 3, 5, 8):
    Zline = r + 1j * np.linspace(-30, 30, 1200)
    with np.errstate(divide='ignore', invalid='ignore'):
        G = ring_chart_gamma(Zline, Z0)
    ok = np.abs(G) < 8
    color = '#66ccff' if r > 0 else '#ff5566'
    ax.plot(G.real[ok], G.imag[ok], color=color, lw=0.6, alpha=0.75)

# ── constant-X circles, BOTH signs of X ────────────────────────────────────
for x in (-8, -4, -2, -1, -0.5, 0.5, 1, 2, 4, 8):
    Zline = np.linspace(-15, 15, 1200) + 1j * x
    with np.errstate(divide='ignore', invalid='ignore'):
        G = ring_chart_gamma(Zline, Z0)
    ok = np.abs(G) < 8
    ax.plot(G.real[ok], G.imag[ok], color='#ffaa55', lw=0.5, alpha=0.6)

# the conventional Smith-chart boundary, |Gamma|=1 -- Re(Z)=0, the actual
# physical-impedance/reactance boundary the printed instrument stops at
boundary = np.exp(1j * np.linspace(0, 2 * np.pi, 400))
ax.plot(boundary.real, boundary.imag, color='#ffffff', lw=1.6,
       label='|Gamma|=1  (Re(Z)=0 — where the conventional chart ends)')

ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.legend(loc='upper right', facecolor='#161620', edgecolor='#444444',
         labelcolor='#dddddd', fontsize=8, framealpha=0.9)
ax.set_title("The complete fold — both sides of Re(Z)=0\n"
            "inside the white circle: the conventional (physical-impedance) "
            "Smith chart\noutside it: the same map's other half, real but "
            "never physically realizable as passive impedance",
            color='#dddddd', fontsize=11)
ax.tick_params(colors='#888888', labelsize=8)
cbar = fig.colorbar(sc, ax=ax, fraction=0.045, pad=0.03)
cbar.set_label("local scale factor |dGamma/dZ|", color='#cccccc', fontsize=8.5)
cbar.ax.tick_params(colors='#888888', labelsize=7.5)
for spine in ax.spines.values():
    spine.set_edgecolor('#444444')

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   'two_ring_chart_full_manifold.png')
fig.savefig(out, facecolor=fig.get_facecolor())
print(f"Saved {out}")
