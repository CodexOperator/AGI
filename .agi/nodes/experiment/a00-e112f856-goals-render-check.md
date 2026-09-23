---
id: experiment:a00-e112f856-goals-render-check
mint_id: f547c71e6976791207cd1b2581511e88
type: experiment
parents:
  - hypothesis:a00-e112f856-12efaa
next_edges: []
edited_by: a00-e112f856
evidence_runs:
  - experiment:a00-e112f856-goals-render-check
line_ceiling: 40
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 24
profile: balanced
role: kid
scaffold_hash: 66bf70161cf5bfbd
season: 2
testable_claim: On this checkout the DT.98 Agent Notes claim that MUR residue D2 was "MOOT on this base" is false -- snapshot-goals.py --render --check exits 1 with GOALS.md:G7.31.1.1 rendered status horizon against the node's status active; a single --render writes the node's truth into GOALS.md and a re-check exits 0.
title: GOALS.md was stale, not moot -- render --check exits 1 before the heal and 0 after
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e112f856-goals-render-check

Corrective run for `goal:g7.31.1.1`, under
`hypothesis:a00-e112f856-12efaa`. The DT.98 round recorded MUR residue D2 as
"MOOT on this base ... GOALS.md agrees". This run measured the pre-fix bytes
and found the opposite: GOALS.md disagreed with the goal node and the
round-trip check failed. GOALS.md is derived; the goal node is the source of
truth, so the heal is a render, not a goal-node edit.

## Pre-fix measurement (verbatim)

```
$ python3 extensions/agi/bin/snapshot-goals.py --render --check; echo "rc=$?"
render --check: MISMATCH, 79 diff line(s)
--- GOALS.md (on disk)
+++ GOALS.md (rendered from nodes)
...
-##### G7.31.1.1 — Measured CLI argv matches grok-bot --help; stub flags retired — status: horizon
+##### G7.31.1.1 — Measured CLI argv matches grok-bot --help; stub flags retired — status: active
...
rc=1
$ grep -n 'G7.31.1.1' GOALS.md | head
7092:##### G7.31.1.1 — Measured CLI argv matches grok-bot --help; stub flags retired — status: horizon
```

The on-disk GOALS.md said `horizon`; `.agi/nodes/goal/g7.31.1.1.md:17` said
`status: active`. Full pre-fix transcript: session scratch
`pre-render-check.txt` (63 lines, 8 removed lines).

## Heal and post-fix measurement (verbatim)

```
$ python3 extensions/agi/bin/snapshot-goals.py --render; echo "render_rc=$?"
rendered: 301 goal(s) + preamble -> /data/work/agi/.agi/worktrees/a00-4d472607/GOALS.md
render_rc=0
$ python3 extensions/agi/bin/snapshot-goals.py --render --check; echo "check_rc=$?"
render --check: 301 goal(s) round-trip byte-identical
check_rc=0
$ grep -n 'G7.31.1.1' GOALS.md | head
7092:##### G7.31.1.1 — Measured CLI argv matches grok-bot --help; stub flags retired — status: active
```

## Second order: Agent Notes render, so notes must precede the render

The correction was also appended to the two nodes carrying the false claim
(`goal:g7.31.1.1`, `hypothesis:a00-0349f27c-4362d3`) via `write.py ... 'note
...'`. That re-staled GOALS.md, because **`## Agent Notes` is part of the node
body that snapshot-goals renders** -- the check immediately after the notes
exited 1 with a 9-line diff. So the heal order is: append notes first, render
last, and verify. Final state, after the render following the notes:

```
$ python3 extensions/agi/bin/snapshot-goals.py --render --check; echo "rc=$?"
render --check: 301 goal(s) round-trip byte-identical
rc=0
```

The brief's step order (render at step 2, verify at step 3, append notes at
step 4) would have left GOALS.md stale again on exit. This run diverged:
notes at step 4, render after, single verification at the end.

## Scope / honesty

- Only derived output moved: `git diff --numstat -- GOALS.md` reports
  `14 added / 10 removed` (24 lines), under the 40-line ceiling. No goal node
  body other than the two authoring notes; no code touched.
- The render is the documented heal (`GOALS.md` is derived from
  `.agi/nodes/goal/*.md`); no hand edit was made to GOALS.md.
- `evidence_runs` is self-cited LIST form; the decisive judgement belongs in
  the child verdict this round's `cli.py done` writes.
