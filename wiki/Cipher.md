# Cipher — classical cryptanalysis as factoral decomposition

`engine/toolsets/cipher.py` · line: **both** · stdlib only, ported from
`PtolemyDesktop/Kryptos/analysis.py` ("the methods to break each").

Cody, 2026-09-02: *"investigate which direction (text→cipher) or
(cipher→analysis) of each is useful for factoral decomposition… and add those
tools."*

---

## The investigation — which direction serves factoral decomposition

Every method has two directions: **text → cipher** (encrypt — pick a key, apply
a transform) and **cipher → analysis** (break — recover the hidden generator
from the output). Breaking a classical cipher *is* decomposition: you recover a
period, a key length, a substitution, or a partition by deductive sieving. So
**cipher → analysis is the descent (free) direction** for almost all of them;
text → cipher is the emerger (work) direction — a choice.

| method | factoral-useful direction | why | line role |
|---|---|---|---|
| **Kasiski** | cipher → analysis **is factoral decomposition** | repeated substrings → gap multiset → **GCD-vote the gaps** → period. This is `ring.gcd_is_the_detector` / `lineage.gcd_is_lca` applied to a distance multiset. | `descend`: the period. `build_up`: choose a period, synthesise the repeat structure. |
| **Index of Coincidence** (Friedman) | cipher → analysis | the **continuous** estimate of the same period Kasiski gets **discretely** — the Smith-chart / gasket pair (see [`The-Two-Charts-and-Jurisdiction.md`](The-Two-Charts-and-Jurisdiction.md)) on one quantity: the period. | `descend`: column-IoC signal per candidate period. |
| **frequency / χ²** | cipher → analysis | the **facet classifier**: `IoC ≥ 0.060` ⇒ single alphabet (Caesar / substitution / transposition / plaintext); `IoC < 0.052` ⇒ polyalphabetic (period > 1). A monoalphabetic cipher is a tier-0 **SIGN** relabel — the histogram shape survives, only the labels move. | `descend`: classify. `build_up`: pick the substitution. |
| **Caesar / shift** | text → cipher | encryption is pure tier-0 **ADD** on ℤ/26. The break is a bounded 26-way `argmin χ²` — the degenerate ascent that is cheap enough to read for free. | `both`. |
| **word-pattern signature** | cipher → analysis | `pattern_signature("HELLO") = "12334"` is **invariant under any monoalphabetic relabel** — it quotients the alphabet out. The signature *is* the decomposition. | `descend`: the signature. `build_up`: find a word realising a target signature (search — mirrors `t32_nilpotency`). |
| **Vowel Trowel** (Sukhotin) | cipher → analysis | a **spectral partition** of the letter-adjacency graph — the same move as `noether`'s `J_red / J_blue` split, language-agnostic, no frequency table. | `descend`. |
| **transposition** | text → cipher | the key length **divides the ciphertext length** — a factoral constraint that lives on the encryption side. | `descend`: the divisor constraint. |
| **Enigma key-space** | text → cipher | `enigma_keyspace` is a worked **product decomposition of a count**: `60 = 5·4·3`, `17576 = 26³`, `plugboard = 26!/(6!·2⁶·10!)`. Ω-of-a-number territory — a lineage of a keyspace, not a break. | `descend`: factor the count. |

**The load-bearing one is Kasiski.** `period = GCD-vote of the repeat-distance
multiset` is factoral decomposition, exactly — and the IoC is its continuous
shadow.

## descend (free)

`descend(ciphertext, max_period=16)` — one sweep per statistic, no key searched:

```python
from engine import line_descend
r = line_descend('cipher', vigenere_ciphertext)
r['kasiski']        # {'gap_factor_votes': [(7, 9), (14, 7), (21, 7), …], 'gap_gcd': 1, 'period': 7}
#                    gap_gcd collapses to 1 on one coincidental short repeat — the
#                    vote (7 wins) is the noise-robust GCD; that is the period.
r['ioc']            # 0.047  -> r['ioc_class'] = 'flat (polyalphabetic / long key)'
r['ioc_period']     # 7 or a small multiple — the continuous estimate, coarser than Kasiski
r['facet']          # 'polyalphabetic — period > 1; split into columns …'
r['pattern_signatures']   # {'HELLO': '12334', …}  — relabel-invariant
r['vowel_partition']      # {'vowels': [...], 'consonants': [...]}   (Sukhotin)
```

## build_up (work)

```python
from engine import line_build_up
line_build_up('cipher', plaintext, key='LIBERTY')     # text->cipher: encrypt; cost = len(key)
line_build_up('cipher', ciphertext, period=7)         # cipher->key: p·26 column trials
line_build_up('cipher', ciphertext)                   # AscentNotFree('a period (or a key)')
```

`build_up` with neither a key nor a period **refuses** — the period is the owed
constraint, and `descend()` factors it out of the gaps for free.

## verify

`{'ok': True}` — a Vigenère of the Declaration of Independence with key
`LIBERTY` (period 7): Kasiski recovers 7 as the top gap factor; IoC reads
polyalphabetic; `build_up(period=7)` recovers `LIBERTY` and the plaintext;
`build_up(key='LIBERTY')` round-trips to the same ciphertext; `pattern_signature`
invariants hold; a shift-3 text solves back to 3; `IoC` of English ≈ 0.0667;
`build_up` with no constraint raises `AscentNotFree`.

## Related

`engine/lineage.py` — `repeat_distances`, `infer_period_by_stem_vote`,
`vigenere_cipher` (the crystal layer already recovered unseen periods from
repeat structure — Kasiski/Friedman; this toolset is the same move as a
first-class descent) · [`Two-Lines-and-Jurisdiction.md`](Two-Lines-and-Jurisdiction.md)
· [`The-Two-Charts-and-Jurisdiction.md`](The-Two-Charts-and-Jurisdiction.md)
(Kasiski discrete ↔ IoC continuous) · `PtolemyDesktop/Kryptos/analysis.py`
(the port source) · `PtolemyDesktop/wiki/Kryptos.md`.

---

## As a toolset (the two lines)

`engine/toolsets/cipher.py` · line: **both**.

- **descend (free):** ciphertext → its hidden structure — the Kasiski period
  (GCD-vote of the repeat-distance gaps), the IoC (continuous period shadow),
  the χ² facet class, the relabel-invariant pattern signatures, the Sukhotin
  vowel partition. Every read is one sweep; `cost = 0`.
- **build_up (work):** `key=` → encrypt (the emerger choice, `cost = len(key)`);
  `period=` → recover the key by per-column χ² Caesar solves
  (`cost = period · 26`); neither → `AscentNotFree`, the period is what the
  caller owes.
