# The Circle Catalogue — every unit circle, and what its numbers do downstream

*Hand-written companion to the generated [Circle](Circle.md) page. Source: `engine/toolsets/circle.py` (27 self-checks). Tutorial: `examples/50_circle.py`. Scratch evidence (scripts p1–p12 and their outputs): `ContextPlease/claude/scratchpad/2026-10-15_circle_unit_session/`.*

This page is a **cataloguing and relating experiment**: for every constant the project uses, take it as the radius, the diameter, the circumference or the area, write down the other three, and follow the numbers into the equations that use them. It is the fixed-point translator one level up — a translator between the names the same circle goes by.

## 1. A circle is Add : Scale : Sign

| component | circle reading |
|---|---|
| Add | the centre |
| Scale | the radius |
| Sign | the orientation (which way round); the branch of √ an area takes; the antipode e^{iπ} = −1 |

## 2. The relations inside one row

With r the radius: d = 2r · C = πd = 2πr · A = πr² = Cr/2 = Cd/4 · C² = 4πA (isoperimetric, exact) · C/d = π for every circle, including the imaginary ones.
Special circles (all exact): **r = ½** gives d = 1, C = π, A = π/4 (the half-radius circle of the Riemann–Fermat heartbeat, see §9) · **r = 1/(2π)** gives C = 1 · **r = 1/√π** gives A = 1 · **r = 2** gives C = A = 4π · d = C never.

### The log chart makes the roles legible

In u = ln r: ln d = u + ln 2 and ln C = u + ln 2π are **shifts** (Add in the log chart); ln A = 2u + ln π is a **slope of 2** (a Scale). An imaginary radius r → ir is u → u + iπ/2, a quarter turn in the log chart, and it multiplies a degree-k quantity by i^k: C by i, A by i² = −1, the n-ball volume by iⁿ. That is the whole of the imaginary circle's behaviour (§8) and it is the Sign component. *Proposed assignment (Cody to confirm): π placed at the circumference is Add, at the area is Scale, at the diameter is Sign (antipode). The three π-unit circles are computed either way (§4).*

## 3. The catalogue

Every constant in every role. Values to 6 significant figures; "π-lattice" says whether the radius is exactly 2^a·π^b.

### 3a. Constant taken as the **radius**
| constant | radius | diameter | circumference | area | π-lattice of r |
|---|---|---|---|---|---|
| 1/2 | 0.5 | 1 | 3.14159 | 0.785398 | 2^-1·π^0 |
| 1 | 1 | 2 | 6.28319 | 3.14159 | 2^0·π^0 |
| 2 | 2 | 4 | 12.5664 | 12.5664 | 2^1·π^0 |
| pi | 3.14159 | 6.28319 | 19.7392 | 31.0063 | 2^0·π^1 |
| 2pi | 6.28319 | 12.5664 | 39.4784 | 124.025 | 2^1·π^1 |
| 1/pi | 0.31831 | 0.63662 | 2 | 0.31831 | 2^0·π^-1 |
| phi | 1.61803 | 3.23607 | 10.1664 | 8.2248 | — |
| e | 2.71828 | 5.43656 | 17.0795 | 23.2134 | — |
| ln10 | 2.30259 | 4.60517 | 14.4676 | 16.6564 | — |
| sqrt2 | 1.41421 | 2.82843 | 8.88577 | 6.28319 | 2^0.5·π^0 |
| Omega_ZS | 0.567143 | 1.13429 | 3.56347 | 1.0105 | — |
| d* | 0.246307 | 0.492614 | 1.54759 | 0.190592 | — |
| d*_spec | 0.246 | 0.492 | 1.54566 | 0.190117 | — |
| GAP | 0.000707107 | 0.00141421 | 0.00444288 | 1.5708e-06 | — |

### 3b. Constant taken as the **diameter** (so the radius is its half)
| constant | diameter | radius | circumference | area | π-lattice of r |
|---|---|---|---|---|---|
| 1/2 | 0.5 | 0.25 | 1.5708 | 0.19635 | 2^-2·π^0 |
| 1 | 1 | 0.5 | 3.14159 | 0.785398 | 2^-1·π^0 |
| 2 | 2 | 1 | 6.28319 | 3.14159 | 2^0·π^0 |
| pi | 3.14159 | 1.5708 | 9.8696 | 7.75157 | 2^-1·π^1 |
| 2pi | 6.28319 | 3.14159 | 19.7392 | 31.0063 | 2^0·π^1 |
| 1/pi | 0.31831 | 0.159155 | 1 | 0.0795775 | 2^-1·π^-1 |
| phi | 1.61803 | 0.809017 | 5.0832 | 2.0562 | — |
| e | 2.71828 | 1.35914 | 8.53973 | 5.80335 | — |
| ln10 | 2.30259 | 1.15129 | 7.23378 | 4.1641 | — |
| sqrt2 | 1.41421 | 0.707107 | 4.44288 | 1.5708 | 2^-0.5·π^0 |
| Omega_ZS | 0.567143 | 0.283572 | 1.78173 | 0.252625 | — |
| d* | 0.246307 | 0.123154 | 0.773797 | 0.0476479 | — |
| d*_spec | 0.246 | 0.123 | 0.772832 | 0.0475292 | — |
| GAP | 0.000707107 | 0.000353553 | 0.00222144 | 3.92699e-07 | — |

### 3c. Constant taken as the **circumference**
| constant | circumference | radius | diameter | area | π-lattice of r |
|---|---|---|---|---|---|
| 1/2 | 0.5 | 0.0795775 | 0.159155 | 0.0198944 | 2^-2·π^-1 |
| 1 | 1 | 0.159155 | 0.31831 | 0.0795775 | 2^-1·π^-1 |
| 2 | 2 | 0.31831 | 0.63662 | 0.31831 | 2^0·π^-1 |
| pi | 3.14159 | 0.5 | 1 | 0.785398 | 2^-1·π^0 |
| 2pi | 6.28319 | 1 | 2 | 3.14159 | 2^0·π^0 |
| 1/pi | 0.31831 | 0.0506606 | 0.101321 | 0.00806288 | 2^-1·π^-2 |
| phi | 1.61803 | 0.257518 | 0.515036 | 0.208337 | — |
| e | 2.71828 | 0.432628 | 0.865256 | 0.588002 | — |
| ln10 | 2.30259 | 0.366468 | 0.732936 | 0.421912 | — |
| sqrt2 | 1.41421 | 0.225079 | 0.450158 | 0.159155 | 2^-0.5·π^-1 |
| Omega_ZS | 0.567143 | 0.0902637 | 0.180527 | 0.0255962 | — |
| d* | 0.246307 | 0.039201 | 0.078402 | 0.00482775 | — |
| d*_spec | 0.246 | 0.0391521 | 0.0783042 | 0.00481571 | — |
| GAP | 0.000707107 | 0.00011254 | 0.000225079 | 3.97887e-08 | — |

### 3d. Constant taken as the **area**
| constant | area | radius | diameter | circumference | π-lattice of r |
|---|---|---|---|---|---|
| 1/2 | 0.5 | 0.398942 | 0.797885 | 2.50663 | — |
| 1 | 1 | 0.56419 | 1.12838 | 3.54491 | — |
| 2 | 2 | 0.797885 | 1.59577 | 5.01326 | — |
| pi | 3.14159 | 1 | 2 | 6.28319 | 2^0·π^0 |
| 2pi | 6.28319 | 1.41421 | 2.82843 | 8.88577 | 2^0.5·π^0 |
| 1/pi | 0.31831 | 0.31831 | 0.63662 | 2 | 2^0·π^-1 |
| phi | 1.61803 | 0.71766 | 1.43532 | 4.50919 | — |
| e | 2.71828 | 0.930191 | 1.86038 | 5.84456 | — |
| ln10 | 2.30259 | 0.856117 | 1.71223 | 5.37914 | — |
| sqrt2 | 1.41421 | 0.670938 | 1.34188 | 4.21563 | — |
| Omega_ZS | 0.567143 | 0.424885 | 0.84977 | 2.66963 | — |
| d* | 0.246307 | 0.280004 | 0.560007 | 1.75931 | — |
| d*_spec | 0.246 | 0.279829 | 0.559658 | 1.75822 | — |
| GAP | 0.000707107 | 0.0150026 | 0.0300053 | 0.0942643 | — |

Constants: ½, 1, 2, π, 2π, 1/π, φ = golden ratio, e, ln 10, √2, Ω_ZS = W(1) = 0.567143, d* = Ω_ZS/ln 10 = 0.246307, d*_spec = 0.2460 (the disputed fifth d*), GAP = 1/(1000√2). The imaginary constant i is §8.

**Anomaly chase — near-equalities between rows.** 15 cross-constant near-equalities below 1e-3 were found against a chance expectation of 0.23. Verdict: **exact π-lattice algebra** — the constants ½, 1, 2, π, 2π, 1/π, √2 all lie in {2^a π^b}, so their rows coincide exactly (e.g. C(r = ½) = A(r = 1) = π; r = 2 has C = A). φ, e, ln 10, Ω, d*, d*_spec and GAP lie outside the lattice and produced **no** cross-constant hit. `circle.pi_lattice(x)` is the first-line test for "is this coincidence structure or algebra".

## 4. π as the unit

| slot | circle | measures |
|---|---|---|
| π at the circumference (proposed Add) | C = π | r = ½, d = 1, A = π/4 |
| π at the area (proposed Scale) | A = π | r = 1, d = 2, C = 2π |
| π at the diameter (proposed Sign) | d = π | r = π/2, C = π², A = π³/4 |

Gaussian normalisation is the same unit: ∫e^{−πx²}dx = 1 (the area-unit circle's Gaussian).

## 5. Each circle value used as σ_RB

σ_RB = Σ_RB at coupling exponent σ; the per-prime weight is G_p = p^(−σ) (`h_rb_hat.geometric_coupling`). `circle.sigma_reading(σ)` computes G_p over the first 20 primes, the truncated Euler product, the offset from the critical value ½ and the regime; it agrees with `h_rb_hat.euler_product` to machine precision (relative difference 0 over seven test values).

**What σ scales.** σ sets how fast the prime weights fall: G₂ = 2^(−σ) is the weight of the first prime; the sum Σ₂₀ p^(−σ) is the total coupling; σ − ½ is the distance from the critical line (the Noether balance point, forced by R̂† = B̂); 1 − σ is the functional-equation partner. The regime labels are the engine's own (`h_rb_hat.sigma_to_theory`): GR-like σ ≥ 1.9; Yang–Mills-like |σ − 1| < 0.05; critical |σ − ½| < 0.05; Fermat zone 0 < σ < ½; trivial σ ≤ 0; **"intermediate" means only that no label's band covers it**, not a separate regime.

### 5a. The half-radius circle walks the σ ladder
| measure of the half-radius circle | σ | regime | G₂ | Σ₂₀ p^−σ |
|---|---|---|---|---|
| r = ½ | 0.5 | critical (σ≈½) | 0.707107 | 4.98963 |
| d = 1 | 1 | Yang–Mills-like (σ≈1) | 0.5 | 1.74287 |
| A = π/4 | 0.785398 | intermediate | 0.580192 | 2.62771 |
| C = π | 3.14159 | GR-like (σ≥2) | 0.113315 | 0.154828 |

### 5b. The unit-radius circle
| measure of the unit-radius circle | σ | regime | G₂ | Σ₂₀ p^−σ |
|---|---|---|---|---|
| r = 1 | 1 | Yang–Mills-like (σ≈1) | 0.5 | 1.74287 |
| d = 2 | 2 | GR-like (σ≥2) | 0.25 | 0.449703 |
| A = π | 3.14159 | GR-like (σ≥2) | 0.113315 | 0.154828 |
| C = 2π | 6.28319 | GR-like (σ≥2) | 0.0128402 | 0.0138911 |

### 5c. Constants as the radius σ = r
| circle value used as σ | σ | regime (engine's own labels) | G₂ = 2^−σ | Σ₂₀ p^−σ | σ−½ | 1−σ |
|---|---|---|---|---|---|---|
| r = 1/2 | 0.5 | critical (σ≈½) | 0.707107 | 4.98963 | 0 | 0.5 |
| r = 1 | 1 | Yang–Mills-like (σ≈1) | 0.5 | 1.74287 | 0.5 | 0 |
| r = 2 | 2 | GR-like (σ≥2) | 0.25 | 0.449703 | 1.5 | -1 |
| r = pi | 3.14159 | GR-like (σ≥2) | 0.113315 | 0.154828 | 2.64159 | -2.14159 |
| r = 2pi | 6.28319 | GR-like (σ≥2) | 0.0128402 | 0.0138911 | 5.78319 | -5.28319 |
| r = 1/pi | 0.31831 | forbidden/Fermat zone (0<σ<½) | 0.802009 | 7.96085 | -0.18169 | 0.68169 |
| r = phi | 1.61803 | intermediate | 0.325779 | 0.697292 | 1.11803 | -0.618034 |
| r = e | 2.71828 | GR-like (σ≥2) | 0.151955 | 0.223885 | 2.21828 | -1.71828 |
| r = ln10 | 2.30259 | GR-like (σ≥2) | 0.2027 | 0.330287 | 1.80259 | -1.30259 |
| r = sqrt2 | 1.41421 | intermediate | 0.375214 | 0.910651 | 0.914214 | -0.414214 |
| r = Omega_ZS | 0.567143 | intermediate | 0.674952 | 4.24738 | 0.0671433 | 0.432857 |
| r = d* | 0.246307 | forbidden/Fermat zone (0<σ<½) | 0.843052 | 9.69846 | -0.253693 | 0.753693 |
| r = d*_spec | 0.246 | forbidden/Fermat zone (0<σ<½) | 0.843231 | 9.70677 | -0.254 | 0.754 |
| r = GAP | 0.000707107 | forbidden/Fermat zone (0<σ<½) | 0.99951 | 19.9565 | -0.499293 | 0.999293 |
| r = i | 0+1j | trivial (σ≤0) | 0.769239-0.638961j | -11.6826+1.69123j | -0.5+1j | 1-1j |

### 5d. Half-diameter radii σ = X/2 (constant X taken as a diameter)
| circle value used as σ | σ | regime (engine's own labels) | G₂ = 2^−σ | Σ₂₀ p^−σ | σ−½ | 1−σ |
|---|---|---|---|---|---|---|
| r = 1/2/2 (half of diameter 1/2) | 0.25 | forbidden/Fermat zone (0<σ<½) | 0.840896 | 9.59918 | -0.25 | 0.75 |
| r = 1/2 (half of diameter 1) | 0.5 | critical (σ≈½) | 0.707107 | 4.98963 | 0 | 0.5 |
| r = 2/2 (half of diameter 2) | 1 | Yang–Mills-like (σ≈1) | 0.5 | 1.74287 | 0.5 | 0 |
| r = pi/2 (half of diameter pi) | 1.5708 | intermediate | 0.336623 | 0.739995 | 1.0708 | -0.570796 |
| r = 2pi/2 (half of diameter 2pi) | 3.14159 | GR-like (σ≥2) | 0.113315 | 0.154828 | 2.64159 | -2.14159 |
| r = 1/pi/2 (half of diameter 1/pi) | 0.159155 | forbidden/Fermat zone (0<σ<½) | 0.895549 | 12.4261 | -0.340845 | 0.840845 |
| r = phi/2 (half of diameter phi) | 0.809017 | intermediate | 0.570771 | 2.50437 | 0.309017 | 0.190983 |
| r = e/2 (half of diameter e) | 1.35914 | intermediate | 0.389814 | 0.983793 | 0.859141 | -0.359141 |
| r = ln10/2 (half of diameter ln10) | 1.15129 | intermediate | 0.450222 | 1.34832 | 0.651293 | -0.151293 |
| r = sqrt2/2 (half of diameter sqrt2) | 0.707107 | intermediate | 0.612547 | 3.0982 | 0.207107 | 0.292893 |
| r = Omega_ZS/2 (half of diameter Omega_ZS) | 0.283572 | forbidden/Fermat zone (0<σ<½) | 0.821555 | 8.74902 | -0.216428 | 0.716428 |
| r = d*/2 (half of diameter d*) | 0.123154 | forbidden/Fermat zone (0<σ<½) | 0.918178 | 13.8031 | -0.376846 | 0.876846 |
| r = d*_spec/2 (half of diameter d*_spec) | 0.123 | forbidden/Fermat zone (0<σ<½) | 0.918276 | 13.8093 | -0.377 | 0.877 |
| r = GAP/2 (half of diameter GAP) | 0.000353553 | forbidden/Fermat zone (0<σ<½) | 0.999755 | 19.9782 | -0.499646 | 0.999646 |

### 5e. Other measures of selected circles as σ
| circle value used as σ | σ | regime (engine's own labels) | G₂ = 2^−σ | Σ₂₀ p^−σ | σ−½ | 1−σ |
|---|---|---|---|---|---|---|
| d of r=1/2  (2·1/2) | 1 | Yang–Mills-like (σ≈1) | 0.5 | 1.74287 | 0.5 | 0 |
| C of r=1/2  (2π·1/2) | 3.14159 | GR-like (σ≥2) | 0.113315 | 0.154828 | 2.64159 | -2.14159 |
| A of r=1/2  (π·1/2²) | 0.785398 | intermediate | 0.580192 | 2.62771 | 0.285398 | 0.214602 |
| d of r=1  (2·1) | 2 | GR-like (σ≥2) | 0.25 | 0.449703 | 1.5 | -1 |
| C of r=1  (2π·1) | 6.28319 | GR-like (σ≥2) | 0.0128402 | 0.0138911 | 5.78319 | -5.28319 |
| A of r=1  (π·1²) | 3.14159 | GR-like (σ≥2) | 0.113315 | 0.154828 | 2.64159 | -2.14159 |
| d of r=pi  (2·pi) | 6.28319 | GR-like (σ≥2) | 0.0128402 | 0.0138911 | 5.78319 | -5.28319 |
| C of r=pi  (2π·pi) | 19.7392 | GR-like (σ≥2) | 1.14263e-06 | 1.14301e-06 | 19.2392 | -18.7392 |
| A of r=pi  (π·pi²) | 31.0063 | GR-like (σ≥2) | 4.6364e-10 | 4.63641e-10 | 30.5063 | -30.0063 |
| d of r=d*  (2·d*) | 0.492614 | critical (σ≈½) | 0.710736 | 5.08078 | -0.0073856 | 0.507386 |
| C of r=d*  (2π·d*) | 1.54759 | intermediate | 0.34208 | 0.762305 | 1.04759 | -0.547594 |
| A of r=d*  (π·d*²) | 0.190592 | forbidden/Fermat zone (0<σ<½) | 0.876246 | 11.3511 | -0.309408 | 0.809408 |
| d of r=d*_spec  (2·d*_spec) | 0.492 | critical (σ≈½) | 0.711039 | 5.08845 | -0.008 | 0.508 |
| C of r=d*_spec  (2π·d*_spec) | 1.54566 | intermediate | 0.342538 | 0.764203 | 1.04566 | -0.545664 |
| A of r=d*_spec  (π·d*_spec²) | 0.190117 | forbidden/Fermat zone (0<σ<½) | 0.876535 | 11.3665 | -0.309883 | 0.809883 |
| d of r=i  (2i) | 0+2j | trivial (σ≤0) | 0.183457-0.983028j | 2.4216-7.30485j | -0.5+2j | 1-2j |
| C of r=i (2πi) | 0+6.28319j | trivial (σ≤0) | -0.349668+0.936874j | 1.92585+0.976448j | -0.5+6.28319j | 1-6.28319j |
| A of r=i (−π) | -3.14159 | trivial (σ≤0) | 8.82498 | 2.87894e+06 | -3.64159 | 4.14159 |

The full 76-row table (every constant × radius, half-diameter, diameter, circumference, area) is `p8_sigma_scan.csv` in the scratch directory.

### Relationships found

1. **The two Noether currents are the wire profile.** |G_p(σ)/G_p(1−σ)| = p^(1−2σ) = exp(−2(σ−½)·ln p), so with u = σ − ½ the smaller-over-larger current is e^(−2|u| ln p): the wire's B/B_max = e^(−|u|) with the scale 2 ln p. Checked at σ = 0.1, 0.3, 0.7 and p = 2, 3. The functional-equation partner σ → 1−σ is the reflection u → −u, the same fold as circle inversion r → R²/r in the log chart.
2. **The half-radius circle is exactly critical**: σ = r = ½. Its diameter 1 is Yang–Mills-like, its circumference π is GR-like — one circle visits three regimes by changing which measure is read.
3. **Imaginary σ is a pure rotation.** For r = i the diameter 2i gives G_p = p^(−2i), modulus exactly 1 for every prime: no decay, a phase 2·ln p per prime. σ = −π (the imaginary circle's area) lies in the trivial regime with G₂ = 2^π = 8.82, growing, and a divergent Euler product.
4. **d\* lies a half-diameter from the critical value**: 2d* = 0.492614 (engine label "critical" within its 0.05 band), 0.0074 below ½. That is d*'s known 1.5 % distance from ¼, not a new coincidence; no further claim is made.
5. **Half-diameters step down one regime**: d = 2 (GR-like) halves to r = 1 (Yang–Mills-like); d = 1 halves to r = ½ (critical); d = ½ halves to ¼ (Fermat zone).

## 6. The six drawings of one circle, and the seventh

| operator | what it does | law | invariant |
|---|---|---|---|
| `orbit` | the circle itself (identity) | x² + y² = r² | radius |
| `unfold` | circle × drift: the helix | Lorentz force | gyroradius, pitch per turn |
| `cut` | keep an angular window: the arc | B ∝ θ; chord 2r sin(θ/2) | arc ÷ radius = θ |
| `fold` | circle inversion r → R²/r: the wire | B/B_max = e^(−|u|), u = ln(r/R) | the circle r = R |
| `project` | drop onto an axis: the dipole, a 2-to-1 fold | U = −MB cosθ; arcsine density | projected extent ±r |
| `shuffle` | randomise the angle at coupling κ = MB/kT | Boltzmann e^(κcosθ) = von Mises; ⟨cos⟩ = I₁/I₀ (2D), Langevin ≈ κ/3 (3D); sd(θ) → 1/√κ | max-entropy at fixed ⟨cosθ⟩ |

Measured: the dipole energy is a cosine well, not a bell; the Boltzmann weight is von Mises; the angle's spread tends to 1/√κ with vanishing excess kurtosis — **a normal distribution in the limit** — and N dipoles summed approach normal by the central limit theorem (N = 400: skew 0.098, excess kurtosis 0.011). Gravity, Coulomb and the wire share one flux law S_(n−1)(r)·F = enclosed source (wire n = 2, gravity/Coulomb n = 3), differing in Sign (attract/repel) and in the π-factor (2πr against 4πr²); the inversion fold is an exact symmetry only for n = 2. The wire profile is the Mandelbrot multiplier map: c(μ) = μ/2 − μ²/4, |B|/B_max = min(|μ|, 1/|μ|), fold r → R²/r ↔ μ → 1/μ̄, cusp c = ¼ at μ = 1, cardioid area 3π/8, perimeter 4.

**The seventh circle changes the NORM, not the drawing**: the ℓ_p unit circle |x|^p + |y|^p = 1 measured in its own norm, with its own π_p = C/d and area.

| p | q (dual) | π_p | area | area ÷ π_p |
|---|---|---|---|---|
| 1 | inf | 4.000000 | 2.000000 | 0.500000 |
| 1.25 | 5 | 3.498457 | 2.427143 | 0.693775 |
| 1.5 | 3 | 3.259768 | 2.737854 | 0.839892 |
| 1.61803 | 2.61803 | 3.201885 | 2.854754 | 0.891585 |
| 1.41421 | 3.41421 | 3.320814 | 2.641883 | 0.795553 |
| 2 | 2 | 3.141593 | 3.141593 | 1.000000 |
| 3 | 1.5 | 3.259768 | 3.533278 | 1.083905 |
| 2.71828 | 1.58198 | 3.216803 | 3.455367 | 1.074162 |
| 4 | 1.33333 | 3.396935 | 3.708149 | 1.091616 |
| 5 | 1.25 | 3.498457 | 3.800601 | 1.086365 |
| 3.14159 | 1.46694 | 3.281149 | 3.566315 | 1.086910 |
| inf | 1 | 4.000000 | 4.000000 | 1.000000 |

π₂ = π is the **minimum** of π_p (grid minimum 3.14161 at p = 1.992 is grid resolution); π₁ = π_∞ = 4 (taxicab, Chebyshev); **π_p = π_q whenever 1/p + 1/q = 1** (Gołąb 1932; Adler–Tanton 2000), verified to 1e-13 — but the **areas differ** across a dual pair (p = 3: 3.53328; q = 1.5: 2.73785). Duality preserves circumference ÷ diameter, not area. For integer p ≥ 3 the ℓ_p circle is the Fermat curve x^p + y^p = z^p (see the TuringStack page `Lp-Circles-Fermat-Curves-and-the-Two-Factoring-Conics-2026-10-15.md`). The Cayley–Klein triple ε = +1, 0, −1 (x² + εy² = 1) is circle / pair of lines / hyperbola, with one-parameter groups rotation / shear / boost; the first-line test on a unit-determinant 2×2 is |trace| below / equal to / above 2.

## 7. Zeta's heartbeat and the half radius

ζ(½ + it) = e^(−iθ(t))·Z(t) (Riemann–Siegel); the image of the critical line is the polar curve r = Z(t), φ = −θ(t). To leading order Z ≈ 2cos θ, so r = 2 cos φ: a circle through the origin of radius 1 and **area π** — the area under one heartbeat cycle ∫₀^(2π) sin²x dx = π. Normalising by the bounding rectangle 2π × 1 gives mean ½: that is where the **½ radius** comes from — (sin²x − ½)² + (sin x cos x)² = ¼ is the circle of radius ½, d = 1, C = π, A = π/4 through the origin, and its circumference is the heartbeat's area. Measured over 40 lobes between consecutive zeros, the lobe shape factor A/(πD²/4) tracks the phase sweep s (correlation 0.978): s = 1 is a circle, s = 1.5 a cardioid, and the largest lobes (s ≈ 1.75) measure 1.53 — cardioid-like. Open: why the shape factor flattens for s > 1.05.

## 8. The imaginary circle: radius iρ

| measure | value |
|---|---|
| radius | iρ |
| diameter | 2iρ |
| circumference | 2πiρ — for ρ = 1, the period of exp |
| area | −πρ² |
| isoperimetric C² − 4πA | exactly 0 (both −4π²ρ²) |

**Points and chords** (unit imaginary circle, z = i(cos t, sin t)): chord² = −4 sin²(Δ/2), chord = 2i sin(Δ/2); arc = iΔ; sector area = −Δ/2. A triangle inscribed in it has **imaginary sides and real angles** (angle sum π exactly), the law of sines gives a/sin A = 2i for all three sides, and the circumradius from abc/4K is i. The 3-4-5 triangle with sides 3i, 4i, 5i is inscribed in a circle of radius 2.5i (area −6.25π); the ratio triangle area ÷ circle area is 0.305577 for the real and the imaginary version alike — scale and Sign cancel in a ratio.

### The laws of sines and cosines

| surface | law of cosines | law of sines | area |
|---|---|---|---|
| flat | c² = a² + b² − 2ab cos C | a / sin A = 2R | ½ab sin C |
| flat, imaginary sides (a, b, c → ia, ib, ic) | same form, c → ic | a / sin A = 2iρ | −½αβ sin C (degree 2: **sign flips**) |
| sphere radius R | cos(c/R) = cos(a/R)cos(b/R) + sin(a/R)sin(b/R)cos C | sin(a/R) / sin A constant | R²(A + B + C − π) (excess) |
| radius iρ (hyperbolic plane) | cosh(c/ρ) = cosh(a/ρ)cosh(b/ρ) − sinh(a/ρ)sinh(b/ρ)cos C | sinh(a/ρ) / sin A constant | ρ²(π − A − B − C) (deficit) |

Because both laws are homogeneous, scaling every side by i leaves their *form* unchanged; only the sign of every degree-2 quantity flips. **Heron's 16·Area² = (a+b+c)(−a+b+c)(a−b+c)(a+b−c) is degree 4 and is unchanged**; the area itself is its square root, and **which branch is taken is the Sign component**: for the inscribed example Heron's √ gave +1.252229 while ½bc sin A gave −1.252229. A sphere of radius iρ *is* the hyperbolic plane — Lambert's observation — so the "negative π" area is the signed form of the angle *deficit*: 4πR² → −4πρ², and the triangle area R²·(excess) → ρ²·(deficit). Checked on the triangle (0.5, 0.6, 0.7): R = 1 gives excess 0.154060; R = i gives deficit 0.140551; R = 2i gives 0.145306; R = 0.5i gives 0.124447; the law of sines holds at all four.

**n-balls.** V_n(R) = π^(n/2)Rⁿ / Γ(n/2 + 1), so V_n(i) = iⁿ·V_n(1): the Sign rotates a quarter turn per dimension and repeats with period 4 (n = 2: −π; n = 3: −4.18879i; n = 4: +π²/2; n = 5: +5.26379i; n = 6: −5.16771).

**Exponential links.** exp(C) = exp(2πi) = 1; i^i = e^(−π/2) = exp(A/2) = 0.2078796; exp(A) = e^(−π) = (i^i)² = 0.0432139; e^(C/2) = e^(iπ) = −1.

**The Gaussian.** ∫∫exp(−r²/R²) over the plane = πR² when Re(1/R²) > 0. At R = i the integrand is exp(+r²) and the integral **diverges**: −π is the analytic continuation, not a convergent value. At R² = i (the radius e^(iπ/4)) the integral is the Fresnel case, conditionally convergent, with value iπ.

**Real section.** x² + y² = −1 has no real points; its real section in signature (+, −) is the hyperbola x² − y² = −ρ², with hyperbolic angle φ in place of θ, arc ρφ, sector area ρ²φ/2, no π; cos(it) = cosh t, sin(it) = i sinh t.

## 9. Verification and what was chased

- `engine/toolsets/circle.py` `verify()`: 27 checks, all pass; full GL suite 162 passed; `build_docs.py --check` and `transcript.py --check-all` clean.
- Chased to a verdict: π-lattice near-equalities → ALGEBRA; Ω_ZS/(4π) within 0.22 % of the Newton-optimal fast-inverse-sqrt σ → weak coincidence (≈1.9 % chance given the candidates tried); π_p grid minimum at p = 1.992 → METHOD (grid); R → ∞ spherical check failing at R = 1e6 → METHOD (the cosine form cancels catastrophically for R ≳ 1e5; kept as a documented limit, remedy: haversine form); Euler's circle-method returning None for N = 221 → METHOD (a wrong gcd formula in the first draft, fixed to gcd(N, ad ∓ bc)).
- Fast inverse square root: the bit trick is a scale ×(−½) in u = ln x. Near the unit circle (r² = 1 + ε) one Newton step gives 1/r ≈ (3 − r²)/2, relative error ≈ 3ε²/8 — cheaper, but only near the circle; no circle method beats the bit trick for arbitrary x.
- Open: the flattening of the lobe shape factor (§7); how the lobe cusp links to the emerger; the Add/Scale/Sign placement of π; the Lyndon/tense question is unrelated and untouched.

## 10. Citations

Cited from the originals' bibliographic records; **none was downloaded** for this page, so each should be checked against the source before it appears in a paper.

- Gołąb, S. (1932). Quelques problèmes métriques de la géométrie de Minkowski. *Trav. Acad. Mines Cracovie* 6, 1–79.
- Adler, C. L., Tanton, J. (2000). π is the minimum value for pi. *College Math. J.* 31(2), 102–106.
- Gauss, C. F. (1827). *Disquisitiones generales circa superficies curvas.*
- Lambert, J. H. (1766/1786). *Theorie der Parallellinien.*
- von Mises, R. (1918). *Phys. Z.* 19, 490–500. · Langevin, P. (1905). *Ann. Chim. Phys.* 5, 70–127. · Curie, P. (1895). *Ann. Chim. Phys.* 5, 289–405.
- Jaynes, E. T. (1957). Information theory and statistical mechanics. *Phys. Rev.* 106, 620. · Shannon, C. E. (1948). *Bell Syst. Tech. J.* 27, 379.
- Klein, F. (1871). *Math. Ann.* 4, 573–625. · Yaglom, I. M. (1979). *A Simple Non-Euclidean Geometry and its Physical Basis.* Springer.
- Thomson, W. (1845). Extrait d'une lettre. *J. Math. Pures Appl.* 10, 364–367. · Biot–Savart (1820); Ampère (1826).
- Mandelbrot, B. B. (1980). *Ann. N.Y. Acad. Sci.* 357, 249–259. · Edwards, H. M. (1974). *Riemann's Zeta Function.* Academic Press. · Riemann, B. (1859).
- Lomont, C. (2003). *Fast Inverse Square Root.* (the 0x5f37642f constant).
