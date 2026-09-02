#!/usr/bin/env python3
"""
oscilloscope.py -- the Factorial Relativity oscilloscope.

Model: VAPMIP/layer_spectrograph.py ("The Universal Oscilloscope",
SedenionSpectralRelativity) -- same SVG visual language (dark background,
monospace, stacked panels, shadow/connector lines, ghost outlines for
inapplicable channels). That instrument stacks the 5 CD layers for one
input. This one stacks exactly two panels, because factorial relativity
has exactly two facets, not five:

    FERMAT panel (the PROMPT)  -- which N-shape (0..15) does this number
        occupy, and which root-system pathway (tap root / Monster gap /
        dendritic / even) does that shape belong to? Discrete, structural,
        already-built (telperion_engine.py, fermat_monster_engine.py).

    RIEMANN panel (the RESPONSE) -- where does that N-shape's REAL,
        counted prime density sit relative to Dirichlet equidistribution?
        Continuous, statistical, the actual control this project measured
        (engine.maths.equidistribution_control_test).

"Fermat Defines. Riemann Fires." (fermat_monster_engine.py's own title)
-- read literally here: the Fermat panel asks the question, the Riemann
panel is what the real data answers back. A connector line links a
number's own channel across both panels, prompt to response.

Usage:
    python3 oscilloscope.py <N>   # outputs factorial_oscilloscope.svg
"""

import sys
import os

# Import as a package (engine.maths), NOT a bare 'from maths import' --
# engine/maths.py itself does 'from maths import RIEMANN_ZEROS...' to reach
# h_rb_hat's maths.py, and bare-importing engine/maths.py as top-level
# 'maths' collides with that internal disambiguation.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine.maths import (  # noqa: E402
    PRIME_SECTOR, NIEMEIER_GAP, LEECH_SHAPE, prime_sieve,
    equidistribution_control_test,
)

W = 960
LMARGIN = 148
RMARGIN = 24
PANEL_W = W - LMARGIN - RMARGIN
ROW_H = 140
GAP = 40          # the facet gap between Fermat and Riemann -- the "fires" span
TOP_PAD = 70
BOT_PAD = 56
SLOT_W = PANEL_W / 16
BAR_W = max(10, SLOT_W * 0.62)


def shape_category(shape: int) -> tuple:
    """(category, color) for a bare N-shape, independent of whether any
    particular number occupying it is prime -- the category is a property
    of the shape itself (which root system, if any, covers it)."""
    if shape == LEECH_SHAPE:
        return 'tap_root', '#ffd014'
    if shape in NIEMEIER_GAP:
        return 'monster_gap', '#ff4050'
    if shape in PRIME_SECTOR:
        return 'dendritic', '#40c080'
    return 'even_niemeier', '#3a5a8a'


def build_svg(N: int) -> str:
    n_shape = N % 16
    primes = prime_sieve(200_000)
    is_prime = N in set(primes[:1]) or N in primes  # cheap membership check below fixed anyway
    is_prime = N > 1 and (N in primes)

    control = equidistribution_control_test(200_000)
    counts = control['counts_per_class']
    expected = control['expected_per_class_if_equidistributed']
    deviations = {k: (100.0 * (v - expected) / expected) for k, v in counts.items()}
    max_dev = max(abs(d) for d in deviations.values()) or 1.0

    cat, cat_color = shape_category(n_shape)

    H = TOP_PAD + ROW_H * 2 + GAP + BOT_PAD
    lines = []
    e = lines.append

    e('<?xml version="1.0" encoding="UTF-8"?>')
    e(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    e(f'  <rect width="{W}" height="{H}" fill="#080810"/>')
    e(f'  <text x="{W//2}" y="22" font-family="monospace" font-size="11" fill="#888" '
      f'text-anchor="middle">FACTORIAL RELATIVITY OSCILLOSCOPE -- N={N}  '
      f'(N-shape={n_shape}, {"prime" if is_prime else "composite"}, {cat})</text>')
    e(f'  <text x="{W//2}" y="40" font-family="monospace" font-size="9" fill="#555" '
      f'text-anchor="middle">Fermat Defines. Riemann Fires. -- prompt above, response below</text>')

    # channel headers
    for ci in range(16):
        cx = LMARGIN + ci * SLOT_W + SLOT_W / 2
        c, col = shape_category(ci)
        e(f'  <text x="{cx:.1f}" y="{TOP_PAD - 6}" font-family="monospace" font-size="8" '
          f'fill="{col}" text-anchor="middle">{ci}</text>')

    # ── FERMAT panel (prompt) ──────────────────────────────────────────
    fermat_y = TOP_PAD
    fermat_baseline = fermat_y + ROW_H - 20
    e(f'  <rect x="{LMARGIN}" y="{fermat_y}" width="{PANEL_W}" height="{ROW_H}" '
      f'fill="#140a0a" opacity="0.6"/>')
    e(f'  <text x="{LMARGIN-6}" y="{fermat_y+16}" font-family="monospace" font-size="10" '
      f'fill="#ff8080" text-anchor="end">FERMAT</text>')
    e(f'  <text x="{LMARGIN-6}" y="{fermat_y+28}" font-family="monospace" font-size="7" '
      f'fill="#885050" text-anchor="end">(prompt)</text>')
    for ci in range(16):
        c, col = shape_category(ci)
        bx = LMARGIN + ci * SLOT_W + (SLOT_W - BAR_W) / 2
        h = ROW_H - 40
        active = (ci == n_shape)
        opacity = '0.95' if active else '0.30'
        e(f'  <rect x="{bx:.1f}" y="{fermat_y+20:.1f}" width="{BAR_W:.1f}" height="{h:.1f}" '
          f'fill="{col}" opacity="{opacity}"/>')
        if active:
            e(f'  <rect x="{bx-2:.1f}" y="{fermat_y+18:.1f}" width="{BAR_W+4:.1f}" height="{h+4:.1f}" '
              f'fill="none" stroke="#ffffff" stroke-width="1.2"/>')
    e(f'  <text x="{LMARGIN}" y="{fermat_y+ROW_H-4}" font-family="monospace" font-size="7" '
      f'fill="#666">gold=tap root(0)  red=Monster gap{{1,11,15}}  green=dendritic(Niemeier)  '
      f'blue=even</text>')

    # ── the "fires" span ─────────────────────────────────────────────
    riemann_y = fermat_y + ROW_H + GAP
    cx_active = LMARGIN + n_shape * SLOT_W + SLOT_W / 2
    e(f'  <line x1="{cx_active:.1f}" y1="{fermat_y+ROW_H:.1f}" x2="{cx_active:.1f}" '
      f'y2="{riemann_y:.1f}" stroke="{cat_color}" stroke-width="1.5" stroke-dasharray="3,3" '
      f'opacity="0.8"/>')
    e(f'  <text x="{cx_active+6:.1f}" y="{fermat_y+ROW_H+GAP/2:.1f}" font-family="monospace" '
      f'font-size="8" fill="{cat_color}">fires -&gt;</text>')

    # ── RIEMANN panel (response) ─────────────────────────────────────
    e(f'  <rect x="{LMARGIN}" y="{riemann_y}" width="{PANEL_W}" height="{ROW_H}" '
      f'fill="#0a0a18" opacity="0.6"/>')
    e(f'  <text x="{LMARGIN-6}" y="{riemann_y+16}" font-family="monospace" font-size="10" '
      f'fill="#80a0ff" text-anchor="end">RIEMANN</text>')
    e(f'  <text x="{LMARGIN-6}" y="{riemann_y+28}" font-family="monospace" font-size="7" '
      f'fill="#505088" text-anchor="end">(response)</text>')
    mid_y = riemann_y + ROW_H / 2
    e(f'  <line x1="{LMARGIN}" y1="{mid_y:.1f}" x2="{LMARGIN+PANEL_W}" y2="{mid_y:.1f}" '
      f'stroke="#2a2a3a" stroke-width="0.8" stroke-dasharray="3,3"/>')
    e(f'  <text x="{LMARGIN+PANEL_W+4}" y="{mid_y+3:.1f}" font-family="monospace" font-size="7" '
      f'fill="#2a2a3a">0% dev</text>')
    for ci in range(16):
        bx = LMARGIN + ci * SLOT_W + (SLOT_W - BAR_W) / 2
        active = (ci == n_shape)
        if ci not in deviations:
            e(f'  <rect x="{bx:.1f}" y="{mid_y-2:.1f}" width="{BAR_W:.1f}" height="4" '
              f'fill="none" stroke="#1a1a1a" stroke-width="0.4"/>')
            continue
        d = deviations[ci]
        hgt = min(abs(d) / max_dev * (ROW_H * 0.42), ROW_H * 0.42)
        hgt = max(hgt, 2.0)
        col = '#ffffff' if active else ('#80a0ff' if d >= 0 else '#ff8080')
        opacity = '0.95' if active else '0.55'
        y0 = mid_y - hgt if d >= 0 else mid_y
        e(f'  <rect x="{bx:.1f}" y="{y0:.1f}" width="{BAR_W:.1f}" height="{hgt:.1f}" '
          f'fill="{col}" opacity="{opacity}"/>')
        if active:
            e(f'  <text x="{bx+BAR_W/2:.1f}" y="{(y0-4) if d>=0 else (y0+hgt+10):.1f}" '
              f'font-family="monospace" font-size="8" fill="#ffffff" text-anchor="middle">'
              f'{d:+.3f}%</text>')
    e(f'  <text x="{LMARGIN}" y="{riemann_y+ROW_H-4}" font-family="monospace" font-size="7" '
      f'fill="#666">real pi(x;16,k) deviation from Dirichlet equidistribution, '
      f'N={control["N"]:,} (control run)</text>')

    e('</svg>')
    return '\n'.join(lines)


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 97
    svg = build_svg(N)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'factorial_oscilloscope.svg')
    with open(out, 'w') as f:
        f.write(svg)
    print(f"Saved {out}  (N={N})")


# ════════════════════════════════════════════════════════════════════════
#  TOOLSET CONTRACT  (engine/lines.py — the two lines)
#  The oscilloscope is a DESCENT-ONLY instrument: it reads the two facets
#  (Fermat prompt shape, Riemann firing) off one number. There is no free
#  ascent — you cannot recover a number from its two facets without more,
#  so build_up() refuses and names what is owed.
# ════════════════════════════════════════════════════════════════════════
NAME = "oscilloscope"
LINE = "decomposition"


def descend(N: int):
    """FREE: the Fermat N-shape (0..15) of N and its root-system pathway."""
    n = int(N)
    shape = n % 16
    pathway, even = shape_category(shape)
    return {"toolset": NAME, "N": n, "shape": shape, "pathway": pathway,
            "even": even, "free": True, "cost": 0,
            "note": "one mod-16 read plus the root-system lookup",
            "svg_hint": "build_svg(N) renders both panels"}


def build_up(target):
    """WORK: refused. A shape + pathway names a residue class mod 16, not a
    number — the ascent owes the caller the rest of the digits."""
    from .lines import AscentNotFree
    raise AscentNotFree("the number's other digits",
                        "shape is N mod 16; recovering N needs the quotient too")


def verify():
    d = descend(360)
    ok_d = d["shape"] == 360 % 16 and "pathway" in d
    try:
        build_up({"shape": 8})
        ok_b = False
    except Exception as e:                       # AscentNotFree
        ok_b = e.__class__.__name__ == "AscentNotFree"
    return {"ok": ok_d and ok_b, "descend": ok_d, "refuses_ascent": ok_b}
