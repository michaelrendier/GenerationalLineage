# .github

| file | what it is |
|---|---|
| `ISSUE_TEMPLATE/` | bug report, move proposal, and the security contact link |
| `PULL_REQUEST_TEMPLATE.md` | the checklist a change is expected to meet |
| `ci-workflow.yml` | the continuous-integration definition: a **Core** job (numpy only), an **Extended** job (with the four sibling repositories cloned beside), and the two staleness checks |

## Enabling CI

GitHub only runs a workflow that lives in `.github/workflows/`. `ci-workflow.yml` sits one level up because pushing a file *into*
`.github/workflows/` needs a token with the `workflow` scope, and the token used to publish 1.0.0 had `repo` scope only. To turn it on,
either add the file in the GitHub web UI as `.github/workflows/ci.yml` (paste its contents), or push it with a token that has the
`workflow` scope:

```bash
mkdir -p .github/workflows && git mv .github/ci-workflow.yml .github/workflows/ci.yml
```

Every command in the workflow is one that was run by hand from a clean clone for the 1.0.0 release; the workflow itself has not yet run
on GitHub. Until it is enabled, `python3 -m pytest` is the check.
