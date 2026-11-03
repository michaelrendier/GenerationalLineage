# 4.6 The crystal and the join — recovering what you didn't observe

*Tutorial:* [`10_crystal_and_join`](../examples/10_crystal_and_join.py).

Motivated by "crystallography as measurement of invisible relationships":
can a hidden generating parameter be read off a structure's own
repeat-pattern, with the generator itself never observed?

**The crystal** (`PW11`) — an autocorrelation of a sequence against itself,
built from repeats alone (this *is* the Patterson-function move):

```python
from engine import repeat_distances, infer_period_by_stem_vote, vigenere_cipher

plaintext = [ord(c) - 65 for c in "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG" * 8]      # letters as 0..25
cipher = vigenere_cipher(plaintext, key=[3, 9, 15, 2, 7], alphabet=26)  # key length 5, hidden
dists = repeat_distances(cipher, n=4)
infer_period_by_stem_vote(dists, max_period=20)['best_period']   # -> 5, recovered blind
```

This is Kasiski examination / the Friedman test (1863 / 1920s), generalised
past text ciphers to any repeating sequence — R8's gcd/meet, run as a *vote*
across every candidate period instead of one blind reduction (a blind gcd
is fragile: one spurious repeat collapses it to 1). **Honest limit, not
hidden:** a composite period is genuinely ambiguous against its own
divisors by this method alone. Two later toolsets close the gap from either
side: `periodicity` (§4.19) lists every period of a string *exactly*, and
Fine–Wilf is the theorem behind the vote; `cipher` (§4.16) adds the Friedman
index of coincidence (`ioc_by_period`) that real Kasiski cryptanalysis needs
on top.

**The join** (`PW12`) — a permutation's order from its own cycle-length
stems, the lattice-dual of R8's gcd/meet:

```python
from engine import permutation_cycles, permutation_order_direct, permutation_order_via_stems

perm = [1, 2, 0, 4, 3]                          # cycles (0 1 2)(3 4)
permutation_cycles(perm)                        # [[0, 1, 2], [3, 4]]
permutation_order_direct(perm)                  # 6 — apply repeatedly, definitional
permutation_order_via_stems(perm)               # 6 — lcm(3, 2), via primary_decomposition
```

Same stems `G3`'s cepstrum already extracts from an integer's factorisation
(`primary_decomposition`), combined with **max** exponent per prime instead
of R8's **min** — the join instead of the meet. Verified against direct
computation on 400 random permutations, 400/400 agree.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
