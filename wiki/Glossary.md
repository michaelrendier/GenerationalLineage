# Glossary

Terms as this engine uses them. Where a term has a standard mathematical meaning it is the standard one; where the engine adds a
reading of its own, the entry says so. See also the [Tools Reference](Tools-Reference.md) and the [README](../README.md).

## The method

**lineage** — the chain of "built from" links that leads from an object down to something irreducible. In the engine every relation
records what it `descends` from; a chain has to bottom out at one of exactly three irreducibles.

**generation** — depth in a lineage. For a number, depth in its recursive factor tree (a prime is generation 0, a leaf; each split
of a composite is one generation). For an algebraic operation, its tier. Ω(n), the prime-factor count with multiplicity, *is* the
length of n's lineage.

**tier** — how far an operation sits above the floor. **0** irreducible · **1** reflect / dilate · **2** a fixed set · **3** a count or
ratio of something else. The four-question tier test (`decompose()`): is it a count or ratio? a fixed set? does it change length
or preserve it? does it need an added constraint to exist? What survives all four is a candidate primitive.

**the tier-0 floor** — ADD (identity 0), SCALE (identity 1), SIGN (identity: even parity). Together the group
x ↦ sign·scale·x + add = Aff(1, ℝ) = ADD ⋊ (SCALE × SIGN): a *semidirect* product, whose one non-trivial bracket is [SCALE, ADD] = ADD.
`ASS` is this group as a value type.

**factor** — in this engine, whatever can be quotiented out of an object while an invariant residual survives: a period, a key length,
a cycle type, a nilpotent part, a spectral line, a bracketing, a re-ordering.

**residual** — what is left when a factor is removed (the primitive root of a string, the nilpotent part of an operator, the largest
prime-order subgroup of a group).

**move** — one factor-extraction method, packaged as a toolset (for example `lyndon`, `permutation`, `jordan_chevalley`).

## The two lines

**decomposition line / descent** — "what built this". Deductive, forward-propagating, no stored tape. **Free**: `descend()` costs
nothing and the dispatcher stamps `free=True, cost=0`.

**emerger line / ascent** — "what does this build". Inductive: to rebuild you must choose (a bracketing, a firing order, a pitch, a
key) or be given a constraint. **Paid**: `build_up()` reports a `cost`. The adjoint is the one that costs; extinction is free,
rebirth requires work.

**toolset** — a module that serves one or both lines and honours the contract: `NAME`, `LINE`, `descend`, `build_up`, `verify`.

**cost** — the work `build_up()` reports: steps taken, candidates tested, samples generated, characters of ciphertext owed. Each
toolset says in its registry entry what its cost counts.

**`AscentNotFree`** — the exception `build_up()` raises when the rebuild is genuinely undetermined without something the caller owes.
It carries `.owed`, a short statement of the missing constraint. **The refusal is the result**, not a failure: it tells you exactly
what the ascent needs.

**`verify_all()`** — runs every toolset's `verify()`. Reports three outcomes and never conflates them: *ran and passed*, *ran and
failed*, *did not run* (skipped). `_ok`: everything that ran passed. `_complete`: `_ok` and nothing skipped.

## Status and provenance

**HOLDS / MATHS-FAULT / CODE-FAULT** — the engine's three-way status. `HOLDS`: the check ran, both sides were measured, they agree.
`MATHS-FAULT`: it ran, both sides were measured, they *disagree* — the claim is false. `CODE-FAULT`: the check did not run — the claim
is *unjudged*, not confirmed.

**ESTABLISHED / OURS / THEORETICAL** — provenance labels on the per-tool pages. *Established*: a published algorithm or theorem,
cited. *Ours*: this project's own contract, framing or construction. *Theoretical*: stated in the framework, not established.

**Core / Extended** — Core is everything that needs only numpy. Extended adds `engine.maths`, `engine.tools`, `engine.oscilloscope`,
which reach four sibling repositories. `engine.EXTENDED` reports which you have.

**guarantee-first** — the engine's working rule: prefer an exact or exhaustive check to a sampled one; prefer an explicit refusal to
a confident approximation; report an unknown as unknown; provide a fallback where no hard guarantee exists.

## The domain

**the two trees** — every integer is exactly one of: **Telperion** (prime — defined by what it *cannot* be decomposed into),
**Laurelin** (composite — defined by what it *is* decomposed into), or **the Mingling** (0 and 1 — the identities of ADD and SCALE, neither
prime nor composite). `two_trees(N)` checks that these partition [0, N] with no overlap and no remainder.

**fall / survive** — a number *falls* if ℤ/(n) has zero divisors (n composite) and *survives* if ℤ/(n) is a field (n prime).

**sieve / un-sieve** — the sieve of Eratosthenes read as lineage (each composite dies on the pass of its smallest prime factor); its
mirror, the un-sieve, switches primes on and watches each composite *arrive*.

**edge, line, pencil (box kite)** — among sixteen Cayley–Dickson placeholders e₀…e₁₅, the 15 nonzero XOR differences are the *edges*
(kinds of relation, not places); a *line* is three relations that compose (a ⊕ b = c); a *pencil* is the seven ways to factor one
relation into two.

**firing order / camshaft** — the order in which the three generators act. The engine's camshaft is (SIGN, SCALE, ADD), SIGN innermost.
The **firing defect** (g − 1)·ln s is zero exactly when SIGN or SCALE is at its identity.

**Γ, the fold** — Γ = tanh(u/2) for the word u = g·ln s + a: the Smith-chart Möbius fold of a tier-0 word.

**J_N** — the map (r, θ) ↦ (1/r, θ + π/2) between the two jurisdictions; four applications return home, two do not.

## The ten moves added in 1.0

**period / border** — a *period* of a string is a shift p under which it matches itself; a *border* is a proper prefix that is also a
suffix. p is a period iff n − p is a border.

**Fine–Wilf** — a string of length ≥ p + q − gcd(p, q) with periods p and q also has period gcd(p, q), and the bound is tight.

**Lyndon word** — a nonempty word strictly smaller than all its proper suffixes (equivalently, all its proper rotations): the canonical
representative of a primitive necklace. Every word factors uniquely into Lyndon words in non-increasing order.

**linear complexity / LFSR** — the length L of the shortest linear recurrence generating a sequence; a linear-feedback shift register
is a generator of one. Berlekamp–Massey finds L from 2L terms.

**order of x modulo P** — the smallest t with xᵗ ≡ 1 (mod P(x)); over GF(2) it is the period of the LFSR whose characteristic
polynomial is P. **Primitive polynomial**: irreducible with order 2^deg − 1.

**log-periodic / discrete scale invariance** — repeating each time x is multiplied by a fixed factor λ: periodic in ln x, not in x.

**Mellin transform** — M[f](s) = ∫₀^∞ f(x) x^(s−1) dx: the Fourier transform on the scaling group (Fourier in ln x).

**flattening artifact** — the distortion of viewing a scale-periodic signal on a linear axis: oscillations bunch and stretch and a
Fourier transform smears the one true frequency.

**cycle type / conjugacy class** — the multiset of cycle lengths of a permutation; two permutations are conjugate iff they share it.

**Lehmer code / factoradic rank** — a permutation's digits in the factorial number system; its index in 0…n! − 1.

**characteristic (Rejewski)** — the cycle types of the products S₁S₄, S₂S₅, S₃S₆ of an Enigma setting: a conjugacy-class invariant the
plugboard cannot change.

**semisimple / nilpotent; Jordan–Chevalley** — S is semisimple if diagonalisable over the algebraic closure; N is nilpotent if some
power is zero. Every matrix is uniquely S + N with SN = NS, and both are polynomials in it.

**nilpotency index** — the least k with Nᵏ = 0: how many generations N lives.

**straight-line program / grammar depth** — a set of rules R → (x, y) generating one sequence; depth is the longest chain of rules.

**group order lineage; smooth order** — the prime factorisation of a group's order; the order is *smooth* if all its prime factors
are small. Discrete-log cost via Pohlig–Hellman is set by the largest prime factor.

**unicity distance** — U = H(K)/D: the ciphertext length beyond which, in Shannon's random-cipher model, a unique key is expected;
H(K) is the key entropy, D the plaintext redundancy.
