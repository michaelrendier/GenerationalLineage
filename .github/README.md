# .github

| file | what it is |
|---|---|
| `ISSUE_TEMPLATE/` | bug report, move proposal, and the security contact link |
| `PULL_REQUEST_TEMPLATE.md` | the checklist a change is expected to meet |
| `workflows/ci.yml` | the continuous-integration definition: a **Core** job (numpy only), an **Extended** job (with the four sibling repositories cloned beside), and the two staleness checks |

## CI

`workflows/ci.yml` runs on every push to `main` and on every pull request: the Core job (numpy only) and the Extended job (with the sibling repositories cloned beside), plus the two staleness checks. Locally, `python3 -m pytest` and `python3 -m engine --verify` are the same checks.
