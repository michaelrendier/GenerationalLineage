# 4.10 The pathway decomposition — factoring a PROCESS, not a number

*Tutorial:* [`14_pathway_decomposition`](../examples/14_pathway_decomposition.py) (the RSA control case below, runnable).

`PW14`, the primary forensic tool. Cody, 2026-08-25, the framing this
landed on after two corrections: "building a mathematical 'pathway
decomposition' using 'process operators'...regardless of actual
mathematical equations or operations associated with an Octonion or a
Quaternion...those additional i's [are not] rotations in the maths, they
[are] composite constructions for any process from imaginary to real
meaning." So `pathway_decomposition()` does NOT try to name a Cayley-
Dickson level, does NOT assume a linear chain, and does NOT treat "how
many components" as a question with one right answer. "Imaginary" here
names a ROLE (hidden, generative, composite) applied to any process's own
minimum necessary tool-set, not an algebra with multiplication rules —
the same distinction `spelling_code` vs `context_vector` already drew
in the author's sibling Ptolemy/monad code, which is not part of this
repository (surface form vs relational structure): the SHAPE is borrowed from hypercomplex numbers, the algebra
is not.

```python
from engine import ProcessOperator, pathway_decomposition

input_value = 12
fn_a = lambda inp: inp + 1              # each fn receives the outputs it depends on, positionally, in order
fn_b = lambda inp: inp * 2
fn_c = lambda a, b: a + b

result = pathway_decomposition(input_value, [
    ProcessOperator('a', fn_a, depends_on=('input',)),
    ProcessOperator('b', fn_b, depends_on=('input',)),      # sibling of a, not chained to it
    ProcessOperator('c', fn_c, depends_on=('a', 'b')),       # a genuine combination of two prior operators
], output_name='c')
# result['real']       — output_name's own value
# result['imaginary']  — every OTHER operator's output, in resolution order
# result['dim']        — 1 + len(imaginary) — however many operators the
#                        process needed, discovered by running it
# result['order']      — the actual dependency-resolved order
```

**RSA as the control case** (the key-lifecycle model lives in the Kryptos
workbench's `Ciphers/RSA.py`, sibling repository PtolemyDesktop; the CRT
decryption below is reproduced in the tutorial) —
not the object of study, a real algorithm exercising a genuine dependency
graph: CRT-decrypt's `m1` and `m2` each depend only on the ciphertext
(siblings, not chained to each other); the CRT term `h` depends on BOTH;
the final `m` depends on `h` AND `m2` again — `m2` fans out to two later
operators, which a forced linear chain (this tool's own first, corrected
attempt) cannot represent without lying about the structure via closures
reaching around it. `pathway_decomposition()` resolves this correctly:
`dim=4`, order `[m1, m2, h, m]`. The full key lifecycle (prime `p`, prime
`q`, modulus `n`, totient, public `e`, private `d`, ciphertext, plaintext)
is a different, equally real decomposition of "RSA" — reported there as
`dim=8`, measured in that sibling repository and not re-run here — not a
re-measurement of the same number; there is no single correct count for
an algorithm this size, only whichever real sub-process the tool is
pointed at.

Verified against a real, externally-checkable example alongside the RSA
control case, not a synthetic one: `pw_process_trace_matches_the_cipher`
re-derives the textbook Vigenere pair `ATTACKATDAWN`/`LEMON` →
`LXFOPVEFRNHR` through the same generic DAG runner, independently of
`vigenere_cipher()`'s own hand-written function, AND confirms RSA's `m2`
fan-out resolves correctly — the thing the corrected design exists to get
right.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
