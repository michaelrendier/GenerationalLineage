# The Generational Lineage skill — shipped with this repo

This directory makes the `generational-lineage` skill **travel with the
code**. Anyone who clones this repository and opens it in Claude Code
gets this skill automatically — it doesn't need to be installed
separately, copied into a home directory, or configured by hand.

## What a "skill" is, in Claude Code

A skill is a markdown file (`SKILL.md`) with a name, a one-line
description, and instructions for how to approach a particular kind of
task. Claude Code discovers skills automatically from two places:

- **User-level**: `~/.claude/skills/<name>/SKILL.md` — applies across
  every project on that person's machine.
- **Project-level** (this file): `.claude/skills/<name>/SKILL.md`, inside
  a repository — applies only when Claude Code is working *in that
  repository*, and ships with the repo's own git history.

When both exist for the same name, the project-level one wins for work
happening inside that project — the repo's own copy is authoritative for
anyone working on the repo, regardless of what else is on their machine.

This skill's own `description:` field (front matter of `SKILL.md`) tells
Claude Code *when* to reach for it — for this one, that's any
mathematical, physical, or structural derivation in this project:
factoring, decomposing operators, checking whether a named "geometry" is
primitive or derived, or deciding whether a result is a discovery or a
restatement.

## Going from zero to Claude Code, for someone new to it

1. **Install.** Claude Code is a CLI tool from Anthropic.
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```
   (Requires Node.js. See https://docs.claude.com/claude-code for the
   current install methods if this one has changed since this note was
   written — package managers and install scripts get updated more
   often than repo READMEs do.)

2. **Authenticate.** Run `claude` once from anywhere; it will walk you
   through signing in with an Anthropic account (Claude Pro/Max/Team
   plan or API billing — either works).

3. **Open this repo.**
   ```bash
   cd GenerationalLineage
   claude
   ```
   Claude Code auto-discovers `.claude/skills/generational-lineage/
   SKILL.md` the moment it starts in this directory — nothing to
   `import`, `source`, or manually load.

4. **Confirm it's active.** Ask Claude something the skill's own
   `description:` covers — e.g. *"decompose this operator"* or *"is this
   a new geometry or a restatement of something already here."* If the
   skill loaded, the response will reason in this repo's own vocabulary
   (tiers, `descends`, HOLDS/MATHS-FAULT/CODE-FAULT, the two lines) — not
   generic advice about the topic.

5. **Run the engine itself**, independent of Claude Code, same as always:
   ```bash
   python3 -m engine.lines        # every toolset self-checks -> ALL OK
   ```
   The skill teaches Claude *how to think about* this repo's own
   objects; the engine underneath it runs the same way whether or not
   Claude is in the loop.

## Where the canonical backup lives

The authoritative, versioned copy of every custom skill (this one
included) is kept outside any single repo, at
`ContextPlease/claude/skills/<name>/` — a plain mirror, not a different
version. If this file and that one ever disagree, treat the
`ContextPlease` copy as the one to reconcile against; this repo's copy
is what ships to a clone, not where edits should originate.

## Provenance

`SKILL.md` in this directory is an exact copy of `~/.claude/skills/
generational-lineage/SKILL.md` as of 2026-09-22 — built from measurements
in the VAPMIP session of 2026-08-18 (see the skill's own header). Update
both copies together; don't let the repo-local one drift from the
canonical one silently.
