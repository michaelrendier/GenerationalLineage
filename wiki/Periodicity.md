# Periodicity — every period of a string, exactly

*`engine/toolsets/periodicity.py` · tutorial: [`examples/40_periodicity.py`](../examples/40_periodicity.py) · transcript: [`examples/transcripts/40_periodicity.txt`](../examples/transcripts/40_periodicity.txt) · added in 1.0*

**Kind of factor:** periodic structure of a sequence (a shift symmetry).

## Definition

A **period** of a string `s` of length `n` is a `p` with `s[i] = s[i+p]` wherever both sides exist. `descend` returns *every* period, exactly, from one linear pass: `p` is a period iff `n − p` is a **border** (a proper prefix that is also a suffix), and the borders are the chain of the prefix function (the KMP failure function). A second, independent route — the Z function — is computed and must agree. The string's exponent over its primitive root is its *generation length*: `(ab)³²` is `ab` taken 32 times.

## Why it belongs in the engine

`toolsets/cipher.py` recovers a key length by *voting* over the factors of repeat-distance gaps (Kasiski). That is an estimate — one coincidental short repeat can drag the gcd to 1. This tool is its guarantee-first counterpart, and **Fine–Wilf** is why the vote works at all: if a string of length ≥ p + q − gcd(p, q) has periods p and q, it also has period gcd(p, q). `build_up` constructs the extremal word one letter *short* of that bound, so the bound's tightness is witnessed, not quoted.

## The two directions

| direction | what it does | cost |
|---|---|---|
| **`descend`** (free) | every period, the border chain, primitive root and exponent, agreement of two routes, Fine–Wilf check — one linear pass | 0 — a single forward pass, no search |
| **`build_up`** (paid, or refused) | write a periodic string from a chosen root; build the Fine–Wilf extremal word for a chosen (p, q) | reported in `cost`; raises `AscentNotFree` (with `.owed`) when it is asked for something it cannot build from |

**Residual** (what is left when the factor is removed): the primitive root, and its exponent.

## Guarantee and how it is checked

Exact and exhaustive: every period is listed, none voted. Checked against brute force on all 32,766 binary strings of length ≤ 14 (three routes agree, Fine–Wilf holds for every one); the extremal word has both periods and not the gcd for all 22 non-dividing pairs (p, q) < 10.

**Limits, stated plainly:** Exact periods only. A string that is *almost* periodic (with errors) has no period here; approximate periodicity is a different problem this tool does not address.

## API

`engine.toolsets.periodicity` · registry name `periodicity` · line **both** · every call below is made as `lines.<direction>("periodicity", ...)` (`from engine import lines`) or directly on the module.

### `descend` — free — `cost = 0`

```python
descend(x)
```

The FREE read: every period, exactly, by one linear pass.

| parameter | default | type |
|---|---|---|
| `x` | *required* | — |

**Returns** a dict with keys: `toolset` (str), `n` (int), `periods` (list), `min_period` (int), `borders` (list), `primitive_root` (NoneType), `exponent` (NoneType), `fractional_exponent` (float), `is_primitive` (bool), `agrees_with_z_function` (bool), `fine_wilf_holds` (bool), `guarantee` (str), `note` (str).
Example call: `lines.descend("periodicity", 'abcabcabca')`

### `build_up` — work — reports `cost`, may refuse

```python
build_up(target)
```

| parameter | default | type |
|---|---|---|
| `target` | *required* | — |

**Returns** a dict with keys: `toolset` (str), `direction` (str), `string` (str), `cost` (int), `note` (str).
**Raises** `AscentNotFree` (`.owed` names the missing constraint) when the rebuild is undetermined.
Example call: `lines.build_up("periodicity", {'root': 'ab', 'length': 8})`

### `verify()`

`verify() -> {"ok": bool, ...}` — the toolset checks itself. `lines.verify_all()` runs this for every toolset.

### Listing 1 — `prefix_function` (extracted verbatim from `engine/toolsets/periodicity.py`)

The mechanism itself, 13 lines, copied from the source by `devtools/build_docs.py` and executed cold in an empty namespace; `tests/test_listings.py` re-runs the extraction, so this block stops existing if it stops running.

```python
from typing import List, Sequence

def prefix_function(s: Sequence) -> List[int]:
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        k = pi[i - 1]
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi
```

```text
>>> prefix_function("abcabcabca")
[0, 0, 0, 1, 2, 3, 4, 5, 6, 7]
```

## Provenance

| component | label | source |
|---|---|---|
| prefix function, borders, Z function, period ⇔ border | **ESTABLISHED** | Knuth–Morris–Pratt 1977; Gusfield 1997 |
| Fine–Wilf theorem and its tightness | **ESTABLISHED** | Fine & Wilf 1965 |
| extremal-word construction (union-find over i ~ i+p, i ~ i+q) | **ESTABLISHED** | standard; the engine's own implementation |
| generation length = exponent over the primitive root; guarantee-first counterpart of the Kasiski vote | **OURS** | — |

## A worked session

Every line below is the literal output of [`examples/40_periodicity.py`](../examples/40_periodicity.py), regenerated by `python3 devtools/transcript.py` and checked by the test suite; it starts from its own imports, so it can be read cold.

```text
>>> from engine.toolsets import periodicity
>>> # descend(): every period of the string, read off one linear pass. Nothing is voted.
>>> r = periodicity.descend("abcabcabca")
>>> r["periods"]
[3, 6, 9, 10]
>>> r["min_period"], r["borders"]
(3, [7, 4, 1])
>>> # A string made by repeating a root has the root as its primitive period;
>>> # the exponent counts the copies — the string's "generation length".
>>> r = periodicity.descend("ab" * 32)
>>> r["min_period"], r["primitive_root"], r["exponent"]
(2, 'ab', 32)
>>> # Two independent routes (prefix function, Z function) must agree:
>>> r["agrees_with_z_function"]
True
>>> # Fine–Wilf: a string of length ≥ p + q − gcd(p, q) with periods p and q also has period gcd(p, q).
>>> # build_up() constructs the extremal word ONE LETTER SHORT of that bound, with both periods but not the gcd:
>>> w = periodicity.build_up({"p": 5, "q": 8})["string"]
>>> w, len(w)
('abaababaaba', 11)
>>> periodicity.periods(w)
[5, 8, 10, 11]
>>> # It cannot be extended by even one letter and keep both periods:
>>> # the next letter would have to equal both w[-5] and w[-8], and they differ.
>>> w[-5], w[-8]
('b', 'a')
>>> # The ascent is a choice; asked for nothing, it refuses and names what it is owed.
>>> try:
...     periodicity.build_up({})
... except Exception as e:
...     type(e).__name__, e.owed
('AscentNotFree', "a root word and length, or a period pair {'p','q'}")
```

## References

- Knuth, D. E., Morris, J. H., Pratt, V. R. (1977). Fast pattern matching in strings. *SIAM Journal on Computing* 6(2), 323–350.
- Gusfield, D. (1997). *Algorithms on Strings, Trees, and Sequences.* Cambridge University Press.
- Fine, N. J., Wilf, H. S. (1965). Uniqueness theorems for periodic functions. *Proceedings of the American Mathematical Society* 16, 109–114.

*Part of the [Generational Lineage Engine](../README.md). See also the [Tools Reference](Tools-Reference.md) and the [Glossary](Glossary.md).*
