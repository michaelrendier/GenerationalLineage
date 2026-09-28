# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
#
# GenerationalLineage is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 3 of the License.
#
# GenerationalLineage is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details. You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-only
"""
devtools/build_docs.py — regenerate the parts of the documentation that mirror the code.

    python3 devtools/build_docs.py            write everything
    python3 devtools/build_docs.py --check    fail if any generated file or README block is stale

What is generated (and therefore cannot drift from the engine):
    wiki/<Page>.md ×10            one page per move added in 1.0, from the authored MOVES below and the
                                  committed tutorial transcripts (examples/transcripts/)
    wiki/Tools-Reference.md       every registered toolset: definition, both directions, tutorial, page
    README.md  between markers    the Install section (from INSTALL.md), the quickstart transcript, the §4.16
                                  toolset table, §4.19–4.28 (the ten moves), the tutorial index, §5 (the relation
                                  tables, from the engine's own log), the Emerger report (§4.14) and Appendix A (Clay output)

Everything else in README.md and wiki/ is hand-written and left alone.
"""
import glob
import importlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from engine import lines  # noqa: E402

TR = os.path.join(ROOT, "examples", "transcripts")


def transcript(ex: str) -> str:
    return open(os.path.join(TR, ex + ".txt"), encoding="utf-8").read().rstrip("\n")


def example_title(ex: str) -> str:
    s = open(os.path.join(ROOT, "examples", ex + ".py"), encoding="utf-8").read()
    m = re.search(r'"""(.*?)"""', s, re.S)
    return m.group(1).strip().split("\n")[0]


# ══════════════════════════════════════════════════════════════════════════════
#  THE TEN MOVES ADDED IN 1.0 — authored once; wiki pages and README §4.19–4.28 are generated from this.
#  Provenance labels follow the house convention: ESTABLISHED (published; cited) · OURS (this project's own
#  framing/contract/construction) · THEORETICAL (stated, not established).
# ══════════════════════════════════════════════════════════════════════════════
MOVES = [
    dict(
        name="periodicity", page="Periodicity", ex="40_periodicity", sec="4.19",
        title="Periodicity — every period of a string, exactly",
        kind="periodic structure of a sequence (a shift symmetry)",
        what=("A **period** of a string `s` of length `n` is a `p` with `s[i] = s[i+p]` wherever both sides exist. "
              "`descend` returns *every* period, exactly, from one linear pass: `p` is a period iff `n − p` is a **border** "
              "(a proper prefix that is also a suffix), and the borders are the chain of the prefix function (the KMP failure "
              "function). A second, independent route — the Z function — is computed and must agree. The string's exponent over "
              "its primitive root is its *generation length*: `(ab)³²` is `ab` taken 32 times."),
        why=("`toolsets/cipher.py` recovers a key length by *voting* over the factors of repeat-distance gaps (Kasiski). That is an "
             "estimate — one coincidental short repeat can drag the gcd to 1. This tool is its guarantee-first counterpart, and "
             "**Fine–Wilf** is why the vote works at all: if a string of length ≥ p + q − gcd(p, q) has periods p and q, it also has "
             "period gcd(p, q). `build_up` constructs the extremal word one letter *short* of that bound, so the bound's tightness is "
             "witnessed, not quoted."),
        residual="the primitive root, and its exponent",
        descend="every period, the border chain, primitive root and exponent, agreement of two routes, Fine–Wilf check — one linear pass",
        ascend="write a periodic string from a chosen root; build the Fine–Wilf extremal word for a chosen (p, q)",
        guarantee="Exact and exhaustive: every period is listed, none voted. Checked against brute force on all 32,766 binary strings of length ≤ 14 (three routes agree, Fine–Wilf holds for every one); the extremal word has both periods and not the gcd for all 22 non-dividing pairs (p, q) < 10.",
        limits="Exact periods only. A string that is *almost* periodic (with errors) has no period here; approximate periodicity is a different problem this tool does not address.",
        prov=[("prefix function, borders, Z function, period ⇔ border", "ESTABLISHED", "Knuth–Morris–Pratt 1977; Gusfield 1997"),
              ("Fine–Wilf theorem and its tightness", "ESTABLISHED", "Fine & Wilf 1965"),
              ("extremal-word construction (union-find over i ~ i+p, i ~ i+q)", "ESTABLISHED", "standard; the engine's own implementation"),
              ("generation length = exponent over the primitive root; guarantee-first counterpart of the Kasiski vote", "OURS", "—")],
        refs=["KMP1977", "Gusfield1997", "FineWilf1965"],
        src="engine/toolsets/periodicity.py",
    ),
    dict(
        name="lyndon", page="Lyndon-Words", ex="41_lyndon", sec="4.20",
        title="Lyndon words — the unique prime factorisation of a word",
        kind="a word's factorisation into irreducible (primitive, minimal-rotation) words",
        what=("A **Lyndon word** is a nonempty word strictly smaller than every one of its proper suffixes (equivalently, than every one "
              "of its proper rotations): the canonical representative of a primitive necklace. The **Chen–Fox–Lyndon theorem**: every "
              "word factors *uniquely* as a concatenation of Lyndon words in non-increasing order. Duval's algorithm finds that "
              "factorisation in one linear pass with no backtracking."),
        why=("It is the fundamental theorem of arithmetic for the free monoid: Lyndon words play the role of primes, the non-increasing "
             "order plays the role of the multiset, and `omega` (the number of factors) plays the role of Ω(n). The same pass yields "
             "the least rotation (the canonical necklace representative) and the primitive root with its exponent."),
        residual="nothing — the factorisation is complete and unique; the necklace representative is the class invariant under rotation",
        descend="Lyndon factors (non-increasing), omega, least rotation, necklace representative, primitive root and exponent",
        ascend="enumerate the Lyndon words of a length over k letters (count checked against the Möbius formula); reassemble a word from chosen Lyndon factors (free — non-increasing order is the only legal one)",
        guarantee="Uniqueness is checked exhaustively: every binary string of length ≤ 10 (2,046 strings) has exactly one non-increasing Lyndon factorisation, and Duval finds it. Lyndon counts match (1/n)Σ μ(d)·k^(n/d) for n ≤ 8, k ∈ {2, 3}; necklace counts match Burnside for n ≤ 12; the least rotation equals the minimum over all rotations for every binary string of length ≤ 9.",
        limits="Alphabet order is fixed by the symbols' natural order; a different alphabet order gives a different (equally unique) factorisation.",
        prov=[("Chen–Fox–Lyndon factorisation; Lyndon words as primitive necklace representatives", "ESTABLISHED", "Chen, Fox & Lyndon 1958; Lothaire 1983"),
              ("Duval's linear-time algorithm; least rotation via Duval on w·w", "ESTABLISHED", "Duval 1983"),
              ("reading Lyndon words as the primes of the word monoid inside the lineage framework", "OURS", "—")],
        refs=["CFL1958", "Duval1983", "Lothaire1983"],
        src="engine/toolsets/lyndon.py",
    ),
    dict(
        name="berlekamp_massey", page="Berlekamp-Massey", ex="42_berlekamp_massey", sec="4.21",
        title="Berlekamp–Massey — the shortest recurrence behind a sequence, and the period it forces",
        kind="the process (linear recurrence) that generates a sequence",
        what=("Given a sequence over GF(p), Berlekamp–Massey returns the *shortest* linear recurrence that generates it. Its length `L` is "
              "the sequence's **linear complexity**; its characteristic polynomial `P(x)` is the generator. Over GF(2) the sequence's "
              "period is the **order of x modulo P**, and that order is read off the *factorisation* of P: for each irreducible factor "
              "f^e, the order is ord(f)·2^⌈log₂ e⌉, and ord(f) divides 2^deg(f) − 1; the sequence's period is their lcm."),
        why=("It is factoral decomposition of a *process*: the sequence is the observable, the recurrence is the operator, and the "
             "operator's own factorisation decides the period. A primitive polynomial of degree L gives the maximal period 2^L − 1; "
             "`build_up` buys that by searching for one."),
        residual="the recurrence (connection polynomial), and its factor structure",
        descend="linear complexity, connection polynomial, whether it is determined, the factorisation, the period, whether the polynomial is primitive",
        ascend="run an LFSR from a chosen polynomial and seed; search for a primitive polynomial of degree L (cost = candidates tested)",
        guarantee="BM is exact only when the sequence supplies at least 2L terms. `descend` reports `determined` and `terms_needed`; below that the result is flagged UNDERDETERMINED — a fit, not a result. The period is computed by exact factorisation for degree ≤ 32; beyond that `period` is `None` with a note, and no approximation is offered. Checked: primitive polynomials of degree 2–16 (BM recovers L and the polynomial from 2L terms; period matches simulation for L ≤ 12), and every non-zero seed of two reducible cases (94 seeds) — the period always matches simulation, never assumed from P.",
        limits="The period computation is over GF(2) only (BM itself runs over any prime field). The trial-division factoriser bounds the period computation at degree 32.",
        prov=[("Berlekamp–Massey algorithm; linear complexity", "ESTABLISHED", "Berlekamp 1968; Massey 1969"),
              ("order of x modulo a polynomial over GF(2) from its factorisation", "ESTABLISHED", "Lidl & Niederreiter 1997"),
              ("flagging results below 2L terms as underdetermined; refusing an uncomputed period rather than approximating", "OURS", "the engine's guarantee discipline")],
        refs=["Massey1969", "Berlekamp1968", "LidlNiederreiter1997"],
        src="engine/toolsets/berlekamp_massey.py",
    ),
    dict(
        name="logperiodic", page="Log-Periodic-and-Mellin", ex="43_logperiodic", sec="4.22",
        title="Log-periodic + Mellin — the spring, read in its own coordinate",
        kind="a periodic function of a non-modular kind: periodic in ln x (a spring / spiral)",
        what=("A quantity that repeats each time x is multiplied by a fixed factor λ is **not** periodic in x. On a linear axis its "
              "oscillations bunch toward small x and stretch at large x, and a Fourier transform in x smears the one true frequency "
              "across a band — the *flattening artifact*. In u = ln x it is an ordinary sinusoid: `y = c + d·ln x + A·cos(ω·ln x + φ)`, "
              "and one turn is x → λx with λ = e^(2π/ω). The **Mellin transform** M[f](s) = ∫ f(x) x^(s−1) dx is exactly the Fourier "
              "transform in u, i.e. the Fourier transform on the *scaling* group."),
        why=("The tier-0 floor ADD ⋊ SCALE has two irreducible axes and so two dual transforms: Fourier on ADD (x → x + a) and Mellin on "
             "SCALE (x → λx). A log-periodic signal is a pure line in the Mellin picture and a smear in the Fourier one. `descend` fits a "
             "trend plus one sinusoid in u (least squares at each ω, so uneven sampling costs nothing extra), and with `compare_flat=True` "
             "runs the *same* model in linear x, so the size of the flattening artifact is a number."),
        residual="the fit residual, and the linear-x fit it is compared against",
        descend="ω, the scale ratio λ, amplitude, phase, constant, trend per ln x, SSE and R²; optionally the linear-x R²",
        ascend="synthesise a spring from a chosen (ω, A, φ, trend, range) — cost = samples",
        guarantee="This one is a numerical fit, not an exact decomposition, and the page says so. Checked: the Mellin transform of e^(−x) equals Γ(s) at s = 1.5, 2, 3.5 (within 1e-4) and the scaling identity M[f(ax)](s) = a^(−s)M[f](s) holds; a planted ω = 6 is recovered to 3×10⁻¹⁰ from 700 samples uniform in x on [1, 2000] (R² = 1.000 in ln x against 0.609 for the same model in x); and a signal periodic in x but not in ln x is rejected (R² = 0.001).",
        limits="Noise robustness has not been characterised — the checks use noise-free data plus a control. One log-frequency plus a linear trend only; the default ω window is [0.5, 30]; the sampling must span several turns of the spring.",
        prov=[("Mellin transform; Mellin = Fourier in ln x; M[e^(−x)] = Γ(s); the scaling property", "ESTABLISHED", "standard integral-transform theory"),
              ("log-periodic oscillations as discrete scale invariance", "ESTABLISHED", "Sornette 1998"),
              ("Fourier-on-ADD / Mellin-on-SCALE as the two dual transforms of the tier-0 floor; the flattening artifact as a measured number", "OURS", "the engine's reading; the identities are classical")],
        refs=["Sornette1998", "Titchmarsh1948"],
        src="engine/toolsets/logperiodic.py",
    ),
    dict(
        name="permutation", page="Permutation", ex="44_permutation", sec="4.23",
        title="Permutation — the invariants of a re-ordering",
        kind="a re-ordering; a periodic permutation (modular affine maps included)",
        what=("Everything worth knowing about a permutation as an operator is read in one pass: its **cycle type** (a partition of n — the "
              "conjugacy class), its **order** (the lcm of the cycle lengths), its **sign** (−1)^(n − #cycles), its reflection length, its "
              "inversion count, its **Lehmer code** and **factoradic rank** (the index in 0…n!−1 — the factorial number system is the "
              "mixed-radix decomposition of a permutation's address). Modular affine permutations x ↦ a·x + b (mod m) are the ADD ⋊ SCALE "
              "group acting on ℤ/m; their cycle structure is read off multiplicative orders."),
        why=("A cycle type is a factorisation of the operator, and the order is the join (lcm) — the dual of the gcd/meet the engine "
             "uses elsewhere. The cheapest permutation of order N uses one cycle per prime power of N, so its degree is Σ p^e over N's "
             "prime-power factorisation: the lineage of N, paid in points. Card shuffles are affine permutations."),
        residual="the cycle type (conjugacy class); the sign",
        descend="cycles, cycle type, order, sign, reflection length, inversions, fixed points, Lehmer code, factoral rank",
        ascend="un-rank a factoradic address; build a permutation of a chosen cycle type; build the cheapest permutation of order N",
        guarantee="Exhaustive over S₁–S₇ (5,913 permutations): sign equals inversion parity, the factoradic rank is a bijection onto 0…n!−1 and un-ranking inverts it, and cycle type is invariant under conjugation. The affine composition law and orbit-length = multiplicative-order are checked for m ∈ {7, 12, 15, 26, 30}. A 52-card deck: out-shuffle order 8, in-shuffle order 52 (the published values). The minimal degree Σ p^e is checked by exhaustive search over cycle types.",
        limits="Permutations are given as explicit lists; nothing here works on implicitly-defined permutations of huge sets.",
        prov=[("cycle type, order, sign, Lehmer code, factorial number system", "ESTABLISHED", "Knuth, TAOCP vol. 3"),
              ("card-shuffle orders as affine permutations", "ESTABLISHED", "Diaconis, Graham & Kantor 1983"),
              ("x ↦ ax + b (mod m) identified with ADD ⋊ SCALE acting on ℤ/m; the cheapest-permutation-of-order-N reading as a lineage", "OURS", "the group law is elementary; the naming is the engine's")],
        refs=["Knuth3", "DGK1983"],
        src="engine/toolsets/permutation.py",
    ),
    dict(
        name="rejewski", page="Rejewski", ex="45_rejewski", sec="4.24",
        title="Rejewski — the invariant the plugboard cannot disturb",
        kind="a conjugacy-class invariant of a re-ordering",
        what=("Enigma's plugboard P is an involution wrapped around the whole rotor path: S′ᵢ = P·Sᵢ·P. Marian Rejewski's 1932 observation is "
              "that a product S′ᵢ·S′ⱼ = P·(Sᵢ·Sⱼ)·P⁻¹ is a *conjugate* of Sᵢ·Sⱼ, and conjugate permutations share a cycle type. So the "
              "multiset of cycle lengths of Sᵢ·S_{i+3} — the three products 1&4, 2&5, 3&6 give the **characteristic** — fingerprints the "
              "rotor setting, and the plugboard, which multiplies the keyspace by ~1.5×10¹⁴, cannot change it."),
        why=("It strips away the part of the operator that acts by conjugation and reads the invariant that is left. Each Sᵢ is a "
             "fixed-point-free involution (the reflector), so in Sᵢ·Sⱼ every cycle length occurs an even number of times. `build_up` is "
             "the *card catalogue*: given an observed characteristic, scan all 26³ start positions; the plugboard is never part of the search."),
        residual="the characteristic (cycle types of the three products)",
        descend="the characteristic of one setting; whether it is plugboard-independent; whether every cycle length is even",
        ascend="the catalogue — all start positions matching an observed characteristic (cost = 26³ = 17,576 settings scanned)",
        guarantee="The implementation is validated against the standard known-answer vector (Enigma I, rotors I·II·III, reflector B, rings AAA, positions AAA, no plugs: AAAAA → BDZGO) and reciprocity with ten plugs. All 17,576 rotor states are checked to be fixed-point-free involutions. Plugboard independence is checked on 60 settings × 5 plugboards (300 checks). The catalogue partitions all 17,576 settings into 6,844 distinct characteristics and finds a planted secret setting from a plugboard-scrambled observation.",
        limits="Scope is Enigma I with rotors I·II·III in that order, reflector UKW-B and ring settings AAA, with full stepping including the middle-rotor double step. Other rotor orders, ring settings and machines are not covered. This is a demonstration of the mathematical invariant on a toy-scale model, not a tool for breaking any real traffic.",
        prov=[("Enigma's rotor wirings, stepping, and the AAAAA → BDZGO vector", "ESTABLISHED", "standard published Enigma I data"),
              ("the cycle-type invariant of conjugates and its use as the characteristic; the card catalogue", "ESTABLISHED", "Rejewski 1980"),
              ("presenting it as a conjugacy-class factor inside the lineage framework, with a refusing ascent", "OURS", "—")],
        refs=["Rejewski1980"],
        src="engine/toolsets/rejewski.py",
    ),
    dict(
        name="jordan_chevalley", page="Jordan-Chevalley", ex="46_jordan_chevalley", sec="4.25",
        title="Jordan–Chevalley — an operator's scaling part and its finite-lifetime part",
        kind="an operator split into two commuting behaviours",
        what=("Every square matrix A over a perfect field is uniquely **A = S + N** with S·N = N·S, S semisimple (diagonalisable over the "
              "algebraic closure — it only *scales*) and N nilpotent (it only shifts along a chain and *dies* after k steps). Both are "
              "polynomials in A. Computed here in exact rational arithmetic: the characteristic polynomial by Faddeev–LeVerrier, its "
              "squarefree part r = χ/gcd(χ, χ′), then Newton's iteration on matrices S ← S − r(S)·r′(S)⁻¹ starting at S = A, which reaches "
              "r(S) = 0 exactly in at most ⌈log₂ n⌉ steps; N = A − S."),
        why=("It is the operator-level version of the lineage: S is the SCALE-like part, N the part with a finite number of generations. "
             "The nilpotency index is how many generations N lives; ranks of the powers of N give the Jordan block sizes (dim ker Nʲ − "
             "dim ker Nʲ⁻¹ counts blocks of size ≥ j, size-1 blocks included)."),
        residual="N (the nilpotent radical), with its nilpotency index and block sizes",
        descend="S, N, nilpotency index, Jordan block sizes of N, the characteristic and squarefree polynomials, the Newton step count, and five re-checked properties",
        ascend="build a matrix with a chosen Jordan structure in a chosen basis (the basis is the added constraint — A alone does not return it)",
        guarantee="Every property is re-checked, not trusted: S + N = A, SN = NS, Nⁿ = 0, r(S) = 0. Checked on seven structures (a single 3-chain, mixed conjugated blocks, two eigenvalues with two chains, diagonalisable, nilpotent, a repeated eigenvalue with a chain and a point, and irrational eigenvalues); S and N also commute with a matrix known to commute with A, as the polynomial-in-A property requires.",
        limits="Exact arithmetic means Fractions grow; intended for small matrices. Over ℚ only.",
        prov=[("Jordan–Chevalley decomposition; S and N are polynomials in A", "ESTABLISHED", "Humphreys 1975, §15"),
              ("characteristic polynomial (Faddeev–LeVerrier); Newton lifting of the semisimple part on the squarefree part", "ESTABLISHED", "standard; the engine's own exact implementation"),
              ("reading S/N as the SCALE-like part and the finite-generation part", "OURS", "an interpretation, not a theorem")],
        refs=["Humphreys1975"],
        src="engine/toolsets/jordan_chevalley.py",
    ),
    dict(
        name="re_pair", page="Re-Pair", ex="47_re_pair", sec="4.26",
        title="Re-Pair — a sequence's own lineage tree",
        kind="a sequence's derivation tree (repeated structure as generations)",
        what=("Re-Pair repeatedly replaces the most frequent adjacent pair with a fresh symbol. What it emits is a straight-line program: "
              "rules R → (x, y) plus a short residual start sequence. That *is* a lineage: a terminal is generation 0, a rule is "
              "1 + the larger generation of its two children, the grammar's depth is the number of generations the sequence needs, and "
              "its size |start| + 2·|rules| is the cost of writing the sequence down through its own repeats."),
        why=("It is `factor_lineage` for strings: `a` × 64 collapses to five rules of depth 5; `abracadabra` × 3 to a handful; a sequence with "
             "no repeated pair does not descend at all (no rules, depth 0)."),
        residual="the start sequence after all repeated pairs are folded",
        descend="rules, start sequence, number of rules, depth, generation of each rule, grammar size, compression ratio, exact round trip",
        ascend="expand a grammar back to its sequence (cost = symbols produced); refuses a cyclic grammar",
        guarantee="The round trip is exact and is checked exhaustively: every binary string of length ≤ 12 and every string over {a, b, c} of length ≤ 7 (11,471 sequences). `a` × 64 gives exactly 5 rules, depth 5, start length 2. **Minimality is NOT claimed:** finding the smallest grammar is NP-hard, Re-Pair is a greedy heuristic, and `descend` reports `minimal: None` (unknown).",
        limits="Greedy and deterministic (ties broken by earliest first occurrence); the implementation is O(n²), fine for tutorial-scale input, not for megabyte inputs.",
        prov=[("Re-Pair dictionary compression", "ESTABLISHED", "Larsson & Moffat 2000"),
              ("the smallest grammar problem is NP-hard", "ESTABLISHED", "Charikar et al. 2005"),
              ("reading the straight-line program as a lineage tree, depth as generation count", "OURS", "—")],
        refs=["LarssonMoffat2000", "Charikar2005"],
        src="engine/toolsets/re_pair.py",
    ),
    dict(
        name="pohlig_hellman", page="Pohlig-Hellman", ex="48_pohlig_hellman", sec="4.27",
        title="Pohlig–Hellman — factor the group, solve per prime, glue by CRT",
        kind="a hard problem's difficulty read off the lineage of a group order",
        what=("The discrete-log problem g^x ≡ h (mod p) looks like one hard problem. Its difficulty is entirely a property of the "
              "*factorisation of the group order* n = ord(g) = ∏ qᵢ^eᵢ: solve x modulo each qᵢ^eᵢ inside the subgroup of that order, one "
              "base-qᵢ digit at a time (each digit a discrete log in a group of prime order qᵢ, by baby-step giant-step), then reassemble "
              "with the Chinese Remainder Theorem. The cost is Σ eᵢ·√qᵢ group operations — set by the *largest prime factor* of the order "
              "and by nothing else."),
        why=("A smooth order collapses to easy; an order with a huge prime factor is untouched, and that residue is exactly where the "
             "hardness lives. `descend` reads the lineage of the order and *predicts* the cost without computing a discrete log; "
             "`build_up` does the solve, counts every group multiplication, verifies gˣ ≡ h, and **refuses** (naming the owed "
             "constraint — a smoother order) when the prediction exceeds the caller's budget."),
        residual="the largest prime-order subgroup — the part no cheaper route reaches in this toolset",
        descend="the factorisation of p − 1 and of ord(g), Ω, the largest prime factor, whether h lies in ⟨g⟩, the predicted and naive costs",
        ascend="solve g^x = h (cost = measured group multiplications); refuse over budget",
        guarantee="Exact and exhaustive on the checked groups: every element of the subgroup ⟨g⟩ is solved and confirmed for four primes (19,704 elements: p = 97, 1009, 8101, 10501); a non-full-order generator (order 675) is solved; the NTT prime 469762049 = 7·2²⁶ + 1 is solved in about 1,500 group operations; and for p = 10⁹ + 7 (p − 1 = 2·500000003) the refusal fires with the prime 500000003 named.",
        limits="Cyclic subgroups of ℤ_p^* for prime p only. Memory for BSGS is √q for the largest prime q handled. The budget default is 5,000,000 group operations. This is the textbook algorithm at teaching scale, not a tool that solves any hard instance.",
        prov=[("Pohlig–Hellman reduction to prime-order subgroups", "ESTABLISHED", "Pohlig & Hellman 1978"),
              ("baby-step giant-step", "ESTABLISHED", "Shanks 1971"),
              ("Miller–Rabin (deterministic bases), Pollard rho factoring", "ESTABLISHED", "Miller 1976; Rabin 1980; Sorenson & Webster 2017; Pollard 1975"),
              ("cost as a function of the group order's lineage; predict-then-refuse contract", "OURS", "—")],
        refs=["PohligHellman1978", "Shanks1971", "Pollard1975", "SorensonWebster2015"],
        src="engine/toolsets/pohlig_hellman.py",
    ),
    dict(
        name="unicity", page="Unicity", ex="49_unicity", sec="4.28",
        title="Unicity — how much ciphertext makes the decomposition unique",
        kind="the amount of evidence a decomposition needs before it is well-posed",
        what=("Every cipher-breaking move recovers a hidden generator (a period, a key, a substitution). Shannon's **unicity distance** "
              "U = H(K)/D says how much evidence must be in hand before that recovery is even well-posed: H(K) is the entropy of the key "
              "space in bits (the size of the hidden generator's lineage), D the redundancy of the plaintext language in bits per "
              "character. Below U, no algorithm can succeed — several keys decrypt to sense and the data cannot choose between them. In "
              "Shannon's random-cipher model the expected number of spurious keys at n characters is 2^(H(K) − n·D) − 1."),
        why=("It is a guarantee in the engine's own sense: a bound on what is *possible*, not a probability of what a search will find. "
             "Two redundancies are kept strictly apart: D₀, computed exactly from the order-0 letter table (≈ 0.525 bits/char), which — "
             "since the true entropy rate can only be lower — gives a **rigorous upper bound** U ≤ H(K)/D₀ on the unicity distance; and "
             "Shannon's literature estimate D ≈ 3.2 (H_L ≈ 1.5 bits/char), labelled as an estimate and not derived here."),
        residual="the number of spurious keys that survive at n characters",
        descend="H(K) for a cipher kind, H₀ and D₀, the rigorous upper bound on U, and the literature estimate of U",
        ascend="the ciphertext length owed so that the expected number of spurious keys is at most ε — the work owed is data",
        guarantee="Reproduces Shannon's published figure: a general substitution cipher on English, H(K) = log₂ 26! = 88.382 bits, U ≈ 27.6 letters (D = 3.2). H₀ = 4.1757 bits, D₀ = 0.5248. Enigma key entropy 67.1 bits (ring settings excluded). The counting core the formula rests on — each key is a bijection, so the average number of keys giving a valid plaintext over all ciphertexts is exactly |K|·|Lₙ|/|Σ|ⁿ — is checked exhaustively in exact arithmetic on a toy language for n = 1…7. `build_up` is checked to hit its own target (ε at n, above ε at n − 1).",
        limits="The bound holds within Shannon's random-cipher model. U is necessary, not sufficient: reaching it says a unique key exists, not that it is cheap to find.",
        prov=[("unicity distance; the random-cipher model; the spurious-key expectation", "ESTABLISHED", "Shannon 1949"),
              ("order-0 redundancy computed from the letter table; the rigorous-bound versus literature-estimate split", "OURS", "—")],
        refs=["Shannon1949"],
        src="engine/toolsets/unicity.py",
    ),
]

REFS = {
    "KMP1977": "Knuth, D. E., Morris, J. H., Pratt, V. R. (1977). Fast pattern matching in strings. *SIAM Journal on Computing* 6(2), 323–350.",
    "Gusfield1997": "Gusfield, D. (1997). *Algorithms on Strings, Trees, and Sequences.* Cambridge University Press.",
    "FineWilf1965": "Fine, N. J., Wilf, H. S. (1965). Uniqueness theorems for periodic functions. *Proceedings of the American Mathematical Society* 16, 109–114.",
    "CFL1958": "Chen, K.-T., Fox, R. H., Lyndon, R. C. (1958). Free differential calculus, IV. The quotient groups of the lower central series. *Annals of Mathematics* 68, 81–95.",
    "Duval1983": "Duval, J.-P. (1983). Factorizing words over an ordered alphabet. *Journal of Algorithms* 4(4), 363–381.",
    "Lothaire1983": "Lothaire, M. (1983). *Combinatorics on Words.* Addison-Wesley.",
    "Massey1969": "Massey, J. L. (1969). Shift-register synthesis and BCH decoding. *IEEE Transactions on Information Theory* 15(1), 122–127.",
    "Berlekamp1968": "Berlekamp, E. R. (1968). *Algebraic Coding Theory.* McGraw-Hill.",
    "LidlNiederreiter1997": "Lidl, R., Niederreiter, H. (1997). *Finite Fields* (2nd ed.). Cambridge University Press.",
    "Sornette1998": "Sornette, D. (1998). Discrete-scale invariance and complex dimensions. *Physics Reports* 297(5), 239–270.",
    "Titchmarsh1948": "Titchmarsh, E. C. (1948). *Introduction to the Theory of Fourier Integrals* (2nd ed.). Oxford University Press. (The Mellin transform and its inversion.)",
    "Knuth3": "Knuth, D. E. (1998). *The Art of Computer Programming, Vol. 3: Sorting and Searching* (2nd ed.). Addison-Wesley. (Inversions, the Lehmer code, the factorial number system.)",
    "DGK1983": "Diaconis, P., Graham, R. L., Kantor, W. M. (1983). The mathematics of perfect shuffles. *Advances in Applied Mathematics* 4(2), 175–196.",
    "Rejewski1980": "Rejewski, M. (1980). An application of the theory of permutations in breaking the Enigma cipher. *Applicationes Mathematicae* 16(4), 543–559.",
    "Humphreys1975": "Humphreys, J. E. (1975). *Linear Algebraic Groups.* Springer GTM 21. (§15, Jordan decomposition.)",
    "LarssonMoffat2000": "Larsson, N. J., Moffat, A. (2000). Off-line dictionary-based compression. *Proceedings of the IEEE* 88(11), 1722–1732.",
    "Charikar2005": "Charikar, M., Lehman, E., Liu, D., Panigrahy, R., Prabhakaran, M., Sahai, A., Shelat, A. (2005). The smallest grammar problem. *IEEE Transactions on Information Theory* 51(7), 2554–2576.",
    "PohligHellman1978": "Pohlig, S. C., Hellman, M. E. (1978). An improved algorithm for computing logarithms over GF(p) and its cryptographic significance. *IEEE Transactions on Information Theory* 24(1), 106–110.",
    "Shanks1971": "Shanks, D. (1971). Class number, a theory of factorization, and genera. *Proceedings of Symposia in Pure Mathematics* 20, 415–440.",
    "Pollard1975": "Pollard, J. M. (1975). A Monte Carlo method for factorization. *BIT Numerical Mathematics* 15(3), 331–334.",
    "SorensonWebster2015": "Sorenson, J., Webster, J. (2017). Strong pseudoprimes to twelve prime bases. *Mathematics of Computation* 86(304), 985–1003. (Deterministic Miller–Rabin for n < 3.3×10²⁴.)",
    "Shannon1949": "Shannon, C. E. (1949). Communication theory of secrecy systems. *Bell System Technical Journal* 28(4), 656–715.",
}

# ── definitions of every registered toolset (authored; the two directions come from the live registry) ────────
DEFINITIONS = {
    "add_scale_sign": "The tier-0 floor as a value type. `ASS(add, scale, sign)` is the map x ↦ sign·scale·x + add, an element of Aff(1, ℝ) = ADD ⋊ (SCALE × SIGN). It composes (`@`), inverts (`~`), strips a generator (`residual`), splits into its three parts, and records the order in which they fired.",
    "scale": "The multiplicative generator. `descend` reads s = value / reference — one division. `build_up` recovers a scale together with an offset, which is underdetermined from one reading and refuses until a second is supplied.",
    "units": "A physical quantity as a point in the 7-axis SI base-dimension lattice (kg, m, s, A, K, mol, cd) — the same decomposition in a third domain. `descend` gives the exact exponent vector; `build_up` narrows a dimension signature to named units and candidate laws.",
    "box_kite": "The geometry the decomposition happens in: sixteen Cayley–Dickson placeholders e₀…e₁₅ whose 15 nonzero XOR differences are the *edges* — kinds of relation, not places. A *line* is three relations that compose (a ⊕ b = c); a *pencil* is the 7 ways to factor one relation into two.",
    "noether": "The conserved invariant of the domain: the red and blue currents trade along a decomposition and the sum you supply is checked to hold; the ascent filters candidate build orders by the conservation law. It checks a sum it is given — it does not derive one (see the SIGN note in `ADD-SCALE-SIGN-Datatype.md` on what is and is not conserved).",
    "archimedes_screw": "The logarithm as a screw: a step from a to b has pitch ln(b/a), and the tier boundaries sit at constant log₂ steps — a constant pitch ln 2. `build_up` climbs a target height in rungs of ln 2 and reports the remainder the ladder cannot lift.",
    "inversion": "J_N: (r, θ) ↦ (1/r, θ + π/2), the map between the two jurisdictions. Four applications return home; two give a point inversion, *not* home — the extinction order is not the rebirth order, in one operator.",
    "t32_nilpotency": "Hyperwebster-style addressing: an integer address decodes (Horner, base 97) to a digit path; a path that reaches 0 when stepped is nilpotent (trailing zeros). `build_up` places digits one at a time to realise a chosen path.",
    "cipher": "Classical cryptanalysis as factoral decomposition, ported from the Kryptos workbench. The period is the GCD-vote of the repeat-distance gaps (Kasiski); the index of coincidence is its continuous shadow; χ² classifies the facet. `build_up` encrypts with a chosen key or, given the period, recovers the key by column trials.",
    "comma_sequence": "The comma sequence (Angelini, Guy & Sloane): each term's step is read off the digits straddling the comma. `descend` checks a walk; `build_up` walks the lexicographically-earliest sequence forward, cost = terms placed.",
    "hyper_linear": "Multiplication read as a regular-representation matrix: each digit of b names one tier-0 SCALE operator composed with a shift (also SCALE, by the base); ADD enters exactly once, at the column sum. Recovering which rows spilled from the bare product is refused (as hard as factoring it); one factor makes it free again.",
    "equation_space": "Steering through a parametrised family of equations by following a collapse function ρ's own gradient rather than searching blind. `descend` reads ρ and its gradient at a point; `build_up` walks to ρ = 0 and refuses if it stalls. `classify_singularity` says whether the locus is a fold or a smooth minimum.",
    "spectral_primes": "The spin/wobble split read as decomposition versus emerger: the spin rate θ′(t) is a smooth monotone carrier (free), and the wobble — the oscillation from the zeros that carries the primes — costs one unit of work per zero.",
    "cs_benchmark": "Measure a callable's real wall-clock cost, once, honestly; every result carries its methodology citation (Patterson et al. 2021) as a data field.",
    "stencil": "The digit-by-digit decomposition machine: `descend` is N = p·q; `build_up` constructs factor pairs from N alone, digit by digit. Slide 1 run to full depth is exhaustive and exact — every divisor pair is found — and a prime N raises `AscentNotFree`.",
    "periodicity": "Every period of a string, exactly (prefix function, cross-checked by the Z function), with the Fine–Wilf theorem that explains the GCD-vote.",
    "lyndon": "The unique factorisation of a word into Lyndon words (the primes of the word monoid), with least rotation and primitive root.",
    "berlekamp_massey": "The shortest linear recurrence behind a sequence and the period it forces, read from the factorisation of its minimal polynomial over GF(2).",
    "logperiodic": "A fit in u = ln x — the spring's own coordinate — with the scale ratio per turn, and the Mellin transform (the Fourier transform on the scaling group).",
    "permutation": "The invariants of a re-ordering — cycle type, order, sign, factoradic rank — and modular affine permutations x ↦ ax + b, the ADD ⋊ SCALE group on ℤ/m.",
    "rejewski": "The Enigma characteristic — cycle types of Sᵢ·S_{i+3} — a conjugacy-class invariant the plugboard cannot disturb, with the card catalogue as the ascent.",
    "jordan_chevalley": "A = S + N exactly, in rational arithmetic: a semisimple part that only scales and a nilpotent part that dies after a finite number of generations.",
    "re_pair": "A sequence's own lineage tree by repeated pairing: rule depth is generation count; exact round trip; minimality reported as unknown.",
    "pohlig_hellman": "Discrete log via the lineage of the group order: predicted cost from the largest prime factor, a solve by BSGS + CRT, and a refusal over budget.",
    "unicity": "Shannon's unicity distance — how much ciphertext makes a decomposition unique — with a rigorous order-0 bound kept apart from the literature estimate.",
    "oscilloscope": "**EXTENDED layer.** A two-panel SVG: the Fermat N-shape (0…15) and root-system pathway of one number, over the Riemann-facet equidistribution reading. Its ascent is refused: a shape is N mod 16, and recovering N owes the remaining digits.",
    "emerger": "The ascent dual of the lineage engine: the bracketing and firing order of emergence of a 16-vector, with e₀ as the fixed anchor and exact zero-divisor tests over rational arithmetic.",
    "lineage": "The decomposition line's anchor: 44 self-checked relations that roll any named operation down to the tier-0 floor (ADD, SCALE or SIGN) and decompose numbers against the two-trees domain.",
}

# existing hand-written wiki pages, by toolset name
WIKI_OF = {
    "add_scale_sign": "ADD-SCALE-SIGN-Datatype", "scale": "Scale", "units": "Units-and-the-Equation-Index",
    "box_kite": "Box-Kite", "noether": "Noether", "archimedes_screw": "Archimedes-Screw",
    "inversion": "Inversion", "t32_nilpotency": "T32-Nilpotency", "cipher": "Cipher",
    "emerger": "The-Emerger-Ascent-Dual", "lineage": "The-Generational-Lineage-Engine",
}
for _m in MOVES:
    WIKI_OF[_m["name"]] = _m["page"]

# tutorial (example) of each toolset
EX_OF = {
    "add_scale_sign": "06_add_scale_sign", "scale": "20_scale", "units": "21_units", "box_kite": "22_box_kite",
    "noether": "23_noether", "archimedes_screw": "24_archimedes_screw", "inversion": "25_inversion",
    "t32_nilpotency": "26_t32_nilpotency", "cipher": "27_cipher", "comma_sequence": "28_comma_sequence",
    "hyper_linear": "29_hyper_linear", "equation_space": "30_equation_space", "spectral_primes": "31_spectral_primes",
    "cs_benchmark": "32_cs_benchmark", "stencil": "33_stencil", "oscilloscope": "90_extended_fermat_facet",
    "emerger": "08_emerger", "lineage": "03_decompose_a_number",
}
for _m in MOVES:
    EX_OF[_m["name"]] = _m["ex"]


def link_ex(ex: str) -> str:
    return f"[`examples/{ex}.py`](examples/{ex}.py)"


# ── generators ─────────────────────────────────────────────────────────────────
def move_page(m: dict) -> str:
    prov = "\n".join(f"| {a} | **{b}** | {c} |" for a, b, c in m["prov"])
    refs = "\n".join(f"- {REFS[k]}" for k in m["refs"])
    return f"""# {m['title']}

*`{m['src']}` · tutorial: [`examples/{m['ex']}.py`](../examples/{m['ex']}.py) · transcript: [`examples/transcripts/{m['ex']}.txt`](../examples/transcripts/{m['ex']}.txt) · added in 1.0*

**Kind of factor:** {m['kind']}.

## Definition

{m['what']}

## Why it belongs in the engine

{m['why']}

## The two directions

| direction | what it does | cost |
|---|---|---|
| **`descend`** (free) | {m['descend']} | 0 — a single forward pass, no search |
| **`build_up`** (paid, or refused) | {m['ascend']} | reported in `cost`; raises `AscentNotFree` (with `.owed`) when it is asked for something it cannot build from |

**Residual** (what is left when the factor is removed): {m['residual']}.

## Guarantee and how it is checked

{m['guarantee']}

**Limits, stated plainly:** {m['limits']}

## Provenance

| component | label | source |
|---|---|---|
{prov}

## A worked session

Every line below is the literal output of [`examples/{m['ex']}.py`](../examples/{m['ex']}.py), regenerated by `python3 devtools/transcript.py` and checked by the test suite; it starts from its own imports, so it can be read cold.

```text
{transcript(m['ex'])}
```

## References

{refs}

*Part of the [Generational Lineage Engine](../README.md). See also the [Tools Reference](Tools-Reference.md) and the [Glossary](Glossary.md).*
"""


def readme_move_block() -> str:
    out = []
    for m in MOVES:
        out.append(f"""### {m['sec']} {m['title']}  `[TUTORIAL — {m['kind']}]`

{m['what']}

{m['why']}

*Guarantee.* {m['guarantee']}

*Limits.* {m['limits']}

Source `{m['src']}` · tutorial {link_ex(m['ex'])} · full page [`wiki/{m['page']}.md`](wiki/{m['page']}.md).

```text
{transcript(m['ex'])}
```
""")
    return "\n".join(out)


def toolset_table() -> str:
    rows = ["| toolset | line | `descend()` — free | `build_up()` — work |", "|---|---|---|---|"]
    for n, d in lines.TOOLSETS.items():
        tag = " *(extended)*" if d.get("requires") else ""
        free = d["free"].replace("|", "\\|").replace("\n", " ")
        work = d["work"].replace("|", "\\|").replace("\n", " ")
        rows.append(f"| **{n}**{tag} | {d['line']} | {free} | {work} |")
    return "\n".join(rows)


def install_block() -> str:
    """The README's Install section is INSTALL.md (the source of truth), one heading level down."""
    t = open(os.path.join(ROOT, "INSTALL.md"), encoding="utf-8").read().split("\n", 1)[1].strip("\n")
    t = re.sub(r"^## ", "### ", t, flags=re.M)
    return "## Install\n\n" + t


def quickstart_block() -> str:
    return "```text\n" + transcript("01_quickstart") + "\n```"


def relations_block() -> str:
    """§5 — every self-checked relation, straight from the engine's own log (its own `claim` sentences)."""
    import engine
    eng = engine.run_lineage(verbose=False)["engine"]
    groups = [
        ("R", ("sigma", "lineage"), "inherited from `engines/e10_generational_lineage.py` in the sibling VAPMIP repository (σ-in-∅_RB; carried over so this repo has its own copy of the discipline it runs on)"),
        ("F", ("factoral",), "the factoral basics (the Two Trees domain, applied to integers)"),
        ("G", ("ring",), "the ring-theory spine (fall ⟺ zero divisors, the same test on two rings)"),
        ("FR", ("fractal",), "the fractal block (§4.7's tower, made concrete)"),
        ("PW", ("pathway", "units"), "the pathway / tuning / instrument layer (§§4.4–4.11) — the newest and most actively growing block"),
    ]
    out = []
    for code, prefixes, blurb in groups:
        rows = [r for r in eng.log if r.name.split(".")[0] in prefixes]
        out.append(f"**{code}1–{code}{len(rows)} — {blurb}**\n")
        out.append("| id | relation | tier | status | claim |\n|---|---|---|---|---|")
        for i, r in enumerate(rows, 1):
            claim = r.claim.replace("|", "\\|").replace("\n", " ")
            out.append(f"| {code}{i} | `{r.name}` | {r.tier} | {r.status.value} | {claim} |")
        out.append("")
    total = len(eng.log)
    held = sum(1 for r in eng.log if r.status.value == "HOLDS")
    out.append(f"*{held}/{total} HOLD.* Regenerated from the engine by `devtools/build_docs.py`; the ids are the relations' order in the engine's log.")
    return "\n".join(out)


def clay_output_block() -> str:
    import subprocess
    r = subprocess.run([sys.executable, "-W", "ignore", "-m", "engine.clay"], cwd=ROOT, capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise SystemExit("python3 -m engine.clay failed:\n" + r.stderr[-800:])
    return "```text\n" + r.stdout.rstrip("\n") + "\n```"


def emerger_report_block() -> str:
    import contextlib
    import io
    import engine
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        engine.report_emergence("e1+e10")
    return "```text\n" + buf.getvalue().strip("\n") + "\n```"


def tutorial_index() -> str:
    files = sorted(glob.glob(os.path.join(ROOT, "examples", "[0-9][0-9]_*.py")))
    n = len(files)
    intro = (f"{n} tutorials, each a runnable script in [`examples/`](examples/) with its generated transcript beside it in "
             "[`examples/transcripts/`](examples/transcripts/). `01`–`18` are the core facets, `20`–`33` the toolsets that predate 1.0, "
             "`40`–`49` the ten moves added in 1.0, and `90` the Extended layer.\n")
    rows = [intro, "| # | tutorial | what it shows |", "|---|---|---|"]
    for p in files:
        ex = os.path.splitext(os.path.basename(p))[0]
        rows.append(f"| {ex[:2]} | [`{ex}.py`](examples/{ex}.py) · [transcript](examples/transcripts/{ex}.txt) | {example_title(ex)} |")
    return "\n".join(rows)


def tools_reference() -> str:
    parts = ["""# Tools Reference — every tool in the Generational Lineage Engine, defined

*Generated by `devtools/build_docs.py` from the live registry (`engine/lines.py`), so the two directions below are exactly what the code declares. The definitions are authored.*

## What a "toolset" is

A **toolset** is a module in `engine/toolsets/` (or one of the three anchors: `lineage`, `emerger`, `oscilloscope`) that serves one or both **lines**:

- The **decomposition line** (*descent*) answers "what is this made of / what built it". It is deductive, forward-propagating, needs no stored tape, and is **free**.
- The **emerger line** (*ascent*) answers "what does this build". It is inductive: to rebuild an object you must *choose* (a bracketing, a firing order, a pitch, a key) or be *given a constraint*. Choice is work.

The two directions are not one computation run backwards; the adjoint is the one that costs.

Every toolset honours one **contract**:

| name | meaning |
|---|---|
| `NAME` | the toolset's registry name |
| `LINE` | `"decomposition"`, `"emerger"`, or `"both"` |
| `descend(x, **k)` | the free reading — a single pass; the dispatcher stamps `free=True`, `cost=0` |
| `build_up(target, **k)` | the work reading — searches or needs an added constraint; reports its `cost`; the dispatcher stamps `free=False` |
| `verify()` | a self-check returning `{"ok": bool, ...}` |
| `AscentNotFree` | the exception `build_up` raises when the rebuild is genuinely undetermined; carries `.owed`, a short statement of the missing constraint. **The refusal is the result**, not a failure. |

`lines.verify_all()` runs every toolset's `verify()` and never conflates three outcomes: **ran and passed**, **ran and failed**, and **did not run** (an *extended*-layer toolset whose sibling repositories are absent, reported as skipped, never as passed).

Call them uniformly with `lines.descend(name, x, ...)` and `lines.build_up(name, target, ...)`, or import a toolset module directly.

## The registry
"""]
    for n, d in lines.TOOLSETS.items():
        ex = EX_OF.get(n)
        wiki = WIKI_OF.get(n)
        tag = "  *(EXTENDED layer — needs the sibling repositories)*" if d.get("requires") else ""
        links = []
        if ex:
            links.append(f"tutorial [`examples/{ex}.py`](../examples/{ex}.py)")
        if wiki:
            links.append(f"page [`{wiki}.md`]({wiki}.md)")
        parts.append(f"""### `{n}`{tag}

{DEFINITIONS.get(n, '')}

- **line:** {d['line']} · **module:** `{d['module']}`
- **descend (free):** {d['free']}
- **build_up (work):** {d['work']}
- {' · '.join(links) if links else 'no tutorial yet'}
""")
    parts.append("\n*Back to the [README](../README.md).*\n")
    return "\n".join(parts)


BEGIN = "<!-- BEGIN: {} (generated by devtools/build_docs.py — do not edit by hand) -->"
END = "<!-- END: {} -->"


def replace_block(text: str, key: str, body: str) -> str:
    b, e = BEGIN.format(key), END.format(key)
    if b not in text:
        raise SystemExit(f"README.md is missing the marker: {b}")
    pre, rest = text.split(b, 1)
    _, post = rest.split(e, 1)
    return f"{pre}{b}\n{body}\n{e}{post}"


def build() -> dict:
    files = {}
    for m in MOVES:
        files[os.path.join("wiki", m["page"] + ".md")] = move_page(m)
    files[os.path.join("wiki", "Tools-Reference.md")] = tools_reference()
    readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    readme = replace_block(readme, "install", install_block())
    readme = replace_block(readme, "quickstart", quickstart_block())
    readme = replace_block(readme, "toolset-table", toolset_table())
    readme = replace_block(readme, "new-moves", readme_move_block())
    readme = replace_block(readme, "relations-table", relations_block())
    readme = replace_block(readme, "clay-output", clay_output_block())
    readme = replace_block(readme, "emerger-report", emerger_report_block())
    readme = replace_block(readme, "tutorial-index", tutorial_index())
    files["README.md"] = readme
    return files


def main(argv) -> int:
    files = build()
    stale = []
    for rel, content in files.items():
        p = os.path.join(ROOT, rel)
        cur = open(p, encoding="utf-8").read() if os.path.exists(p) else None
        if "--check" in argv:
            if cur != content:
                stale.append(rel)
        elif cur != content:
            with open(p, "w", encoding="utf-8") as f:
                f.write(content)
            print("wrote", rel)
    if "--check" in argv:
        print("stale generated docs:", stale or "none")
        return 1 if stale else 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
