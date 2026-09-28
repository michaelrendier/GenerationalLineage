# Security Policy

## Supported versions

| version | supported |
|---|---|
| 1.0.x | yes |

## What this software is, and is not

GenerationalLineage is a mathematical toolkit. Several toolsets (`cipher`, `ping`, `rejewski`, `pohlig_hellman`, `stencil`, `unicity`)
implement textbook cryptanalytic and factoring methods **at teaching scale**, with budgets and explicit refusals. They do not break
modern cryptography and are not a tool for attacking real systems; each one's page states where the method stops. The engine does not
open network connections, read credentials, or write outside its own directory.

## Reporting a vulnerability

If you find a flaw that could harm a user of this software — for example unsafe file handling, code execution from crafted input, or a
dependency problem — please report it **privately**:

- use GitHub's *Report a vulnerability* (private security advisory) on this repository, or
- email the.wandering.god@gmail.com with `SECURITY` in the subject.

Please include the version (`python3 -m engine`), your platform, and the smallest reproduction. This is a one-person research
project: reports are handled best-effort, with no service-level guarantee, and credit is given unless you prefer otherwise.

Correctness bugs in the mathematics (a wrong result, a failed check) are not security issues — please open an ordinary issue.
