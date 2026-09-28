# References

Every **ESTABLISHED** algorithm or theorem in the ten moves added in 1.0 is cited here (and on that move's own page). Where the
engine adds its own reading, the page's provenance table labels it **OURS**.

*Scope, stated plainly.* This page is a complete bibliography for the 1.0 moves. The older sections of the README (§§0–4.18), the Clay
Millennium mappings and the ValaQuenta calibration carry their citations in the pages that use them; a consolidated bibliography for
that material has not been done yet.

*Care taken.* The entries were written from the standard bibliographic record for each work. If you find one that is wrong or incomplete,
please open an issue — a wrong citation is a bug like any other.

## The ten moves

**Periodicity** (`periodicity`, [page](Periodicity.md))

- Knuth, D. E., Morris, J. H., Pratt, V. R. (1977). Fast pattern matching in strings. *SIAM Journal on Computing* 6(2), 323–350.
- Gusfield, D. (1997). *Algorithms on Strings, Trees, and Sequences.* Cambridge University Press.
- Fine, N. J., Wilf, H. S. (1965). Uniqueness theorems for periodic functions. *Proceedings of the American Mathematical Society* 16, 109–114.

**Lyndon words** (`lyndon`, [page](Lyndon-Words.md))

- Chen, K.-T., Fox, R. H., Lyndon, R. C. (1958). Free differential calculus, IV. The quotient groups of the lower central series. *Annals of Mathematics* 68, 81–95.
- Duval, J.-P. (1983). Factorizing words over an ordered alphabet. *Journal of Algorithms* 4(4), 363–381.
- Lothaire, M. (1983). *Combinatorics on Words.* Addison-Wesley.

**Berlekamp–Massey** (`berlekamp_massey`, [page](Berlekamp-Massey.md))

- Massey, J. L. (1969). Shift-register synthesis and BCH decoding. *IEEE Transactions on Information Theory* 15(1), 122–127.
- Berlekamp, E. R. (1968). *Algebraic Coding Theory.* McGraw-Hill.
- Lidl, R., Niederreiter, H. (1997). *Finite Fields* (2nd ed.). Cambridge University Press.

**Log-periodic + Mellin** (`logperiodic`, [page](Log-Periodic-and-Mellin.md))

- Sornette, D. (1998). Discrete-scale invariance and complex dimensions. *Physics Reports* 297(5), 239–270.
- Titchmarsh, E. C. (1948). *Introduction to the Theory of Fourier Integrals* (2nd ed.). Oxford University Press. (The Mellin transform and its inversion.)

**Permutation** (`permutation`, [page](Permutation.md))

- Knuth, D. E. (1998). *The Art of Computer Programming, Vol. 3: Sorting and Searching* (2nd ed.). Addison-Wesley. (Inversions, the Lehmer code, the factorial number system.)
- Diaconis, P., Graham, R. L., Kantor, W. M. (1983). The mathematics of perfect shuffles. *Advances in Applied Mathematics* 4(2), 175–196.

**Rejewski** (`rejewski`, [page](Rejewski.md))

- Rejewski, M. (1980). An application of the theory of permutations in breaking the Enigma cipher. *Applicationes Mathematicae* 16(4), 543–559.

**Jordan–Chevalley** (`jordan_chevalley`, [page](Jordan-Chevalley.md))

- Humphreys, J. E. (1975). *Linear Algebraic Groups.* Springer GTM 21. (§15, Jordan decomposition.)

**Re-Pair** (`re_pair`, [page](Re-Pair.md))

- Larsson, N. J., Moffat, A. (2000). Off-line dictionary-based compression. *Proceedings of the IEEE* 88(11), 1722–1732.
- Charikar, M., Lehman, E., Liu, D., Panigrahy, R., Prabhakaran, M., Sahai, A., Shelat, A. (2005). The smallest grammar problem. *IEEE Transactions on Information Theory* 51(7), 2554–2576.

**Pohlig–Hellman** (`pohlig_hellman`, [page](Pohlig-Hellman.md))

- Pohlig, S. C., Hellman, M. E. (1978). An improved algorithm for computing logarithms over GF(p) and its cryptographic significance. *IEEE Transactions on Information Theory* 24(1), 106–110.
- Shanks, D. (1971). Class number, a theory of factorization, and genera. *Proceedings of Symposia in Pure Mathematics* 20, 415–440.
- Pollard, J. M. (1975). A Monte Carlo method for factorization. *BIT Numerical Mathematics* 15(3), 331–334.
- Sorenson, J., Webster, J. (2017). Strong pseudoprimes to twelve prime bases. *Mathematics of Computation* 86(304), 985–1003. (Deterministic Miller–Rabin for n < 3.3×10²⁴.)

**Unicity** (`unicity`, [page](Unicity.md))

- Shannon, C. E. (1949). Communication theory of secrecy systems. *Bell System Technical Journal* 28(4), 656–715.

## Older toolsets that name a source in their code

- Patterson, D., Gonzalez, J., Le, Q., Liang, C., Munguia, L.-M., Rothchild, D., So, D., Texier, M., Dean, J. (2021). Carbon emissions
  and large neural network training. arXiv:2104.10350. (`cs_benchmark`)
- Angelini, E., Guy, R. K., Sloane, N. J. A. The comma sequence: a simple sequence with bizarre properties. arXiv:2401.14346; and
  *The comma sequence is finite in other bases*, arXiv:2408.03434. (`comma_sequence`; the constant `IMMORTAL_BASE = 634` is attributed to
  the latter in the code.)
- Smith, P. H. (1939). Transmission line calculator. *Electronics* 12(1), 29–31. (the Smith chart, §4.5 and `scale`)
- Kasiski, F. W. (1863). *Die Geheimschriften und die Dechiffrir-Kunst.* Mittler, Berlin. (`cipher`)
- Friedman, W. F. (1922). *The Index of Coincidence and Its Applications in Cryptography.* Riverbank Publications 22. (`cipher`)
- Baez, J. C. (2002). The octonions. *Bulletin of the American Mathematical Society* 39(2), 145–205. (the Cayley–Dickson construction the
  emerger and box-kite toolsets work in)
- Sloane, N. J. A. (ed.). *The On-Line Encyclopedia of Integer Sequences*, A005132 (Recamán's sequence — `bracketing_firing_order`'s
  self-avoidance test generalises it).

## Data

- Enigma I rotor and reflector wirings and the known-answer vector AAAAA → BDZGO (`rejewski`): standard, widely published Enigma I data.
- English single-letter frequencies (`cipher`, `unicity`): the standard al-Kindi-style table carried in `engine/toolsets/cipher.py`.
