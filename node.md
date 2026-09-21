---
id: hypothesis:a00-bad7df6a-dd3928
mint_id: 972d8df3644f49b8a8da0bc32fcc9500
type: hypothesis
parents:
  - goal:g8.1
next_edges: []
confidence: 0.5
edited_by: season.py
scaffold_hash: 660ac82f91397d90
season: 1
thought_session: season
title: A00 bad7df6a dd3928
verdict: pending
---
# hypothesis:a00-bad7df6a-dd3928

## Hypothesis

**Claim:** shape 2 (skill package) is NOT a viable distribution shape for the
engine as a whole, because the pi skill format was designed for small agent
integrations (one SKILL.md + one entry point), and the engine carries ~15
entry points (`bin/*.py`, plus `driver.sh`, plus `lib/` scripts), a `src/`
tree, a `extensions/agi/tests/` test suite, and `lib/find-root.sh` — none of
which the skill package format was designed to accommodate.

**What would actually make sense within shape 2** is what the hybrid-split
sibling (`hypothesis:a00-001de563-9bd20a`) proposes: only the pi
integration layer (the `~/.claude/skills/agi` skill definition, the
SessionStart hook, maybe `driver.sh` as the user-facing entry point) could
viably ship as a skill package, while the engine code itself (the Python
scripts, tests, entry points, `lib/` system) stays as a clone or real
install — because those are the things the skill format does not need to
know about.

**What would prove it:** building a minimal skill package that wraps
e.g. `driver.sh --smoke` from the engine tree, and a second skill package
that tries to wrap ALL entry points (`bin/spawn.py`, `bin/locations.py`,
`bin/stitch.py`, `bin/node_writer.py`, `bin/snapshot-goals.py`,
`bin/grid.py`, `bin/crons.py`, `lib/find-root.sh`, plus the `src/` tree and
test suite). If the second package requires significant contortions
(duplicating the engine tree, custom discovery logic, or exporting
internal utilities that the skill format does not expose), shape 2 is
disproved for the whole engine.

**What would disprove it:** if the engine can be packaged into a single skill
package without duplicating its tree structure — e.g. `extensions/` and
`skills/agi/` and `bin/` and `lib/` and `src/` all naturally fit under one
skill package directory and are discoverable by `level3.py` (which reads
git ls-files) without any special adaptation. This would mean the goal
body's concern about "stretching the format past what it is for" was
overstated.

**Why this is distinct from the hybrid-split sibling:** that hypothesis
assumes the split IS the answer (engine code = clone, integration =
package). This hypothesis tests whether shape 2 alone works for the
engine — the premise the split relies on to know which side of the split
each concern belongs to. If shape 2 cannot hold the engine, then the
split is the only way to use a package at all, and the shape decision
becomes a binary between clone + package (the hybrid) versus clone alone.

**Why this is distinct from the pinning-gap siblings:** those all stay
within shape 1 (drop-in clone) and address the L9 commitment. This
hypothesis addresses the core shape question itself — the engine is
currently a clone, but should it be packaged differently, and if so, how?


## Agent Notes
Tested shape 2 (skill package) viability for whole engine under g8.1. Claim: skill format cannot hold ~15 entry points + src/ + tests; only pi integration layer fits. Uniquely tests the shape-2-as-a-whole premise, distinct from pinning-gap (all shape-1) and hybrid-split (assumes split) siblings. No experiment run -- pending.