---
id: goal:g1.31.5.5.2
mint_id: 45df827635464202831bd3b268d6d6ec
type: goal
parents:
  - goal:g1.31.5.5
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.5.5.2
goal_kind: subgoal
origin: goals-doc
scaffold_hash: a47319dc3e524dc0
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - residue
  - node-answer
  - anonymize
  - evidence
title: "G1.31.5.5.2: scrubbed evidence says it was redacted -- probe output, quotes and reproduce commands on 7 nodes; no scrub THOUGHT over-claims its reach"
town: core
---
# goal:g1.31.5.5.2

## Why this exists
goal:g1.31.5.5: PASS B3 verify stages found 6 rows where a path scrub rewrote EVIDENCE (quoted output, probe `observed`, reproduce commands) or over-claimed its own reach, and no node says so. Triaged REAL at HEAD 8209a5813; 0 already fixed; 2 residue · 4 nit.
```
n    round                                            verify file (.agi/sessions/workflows/runs/)
5    lm-bonsai2-27b-abc-coding-test-on-the-8gb-box    mur-pb3chunk10of20/verify_lm-bonsai2-27b-abc-coding-test-on-the-8gb-box.json
35   engine-code-carries-no-home-user-literal         mur-pb3chunk15of20/verify_engine-code-carries-no-home-user-literal.json
115  lm-every-experiment-path-is-a-config-variable    mur-pb3chunk7of20/verify_lm-every-experiment-path-is-a-config-variable.json
116  lm-every-experiment-path-is-a-config-variable    (same file)
117  lm-every-experiment-path-is-a-config-variable    (same file)
121  a00-600cf080-0cd865                              mur-pb3chunk8of20/verify_a00-600cf080-0cd865.json
```

## Target end-state
- n5 the scrub THOUGHT "…so the graph carries no box path" (`experiment/a00-6ce9cb00-d60152.md:144` · `a00-bb10233d-5a7f1f.md:164` · `a00-c4441397-c8a8c6.md:200`) is true: scoped to repo-root literals, or the absolute data-dir paths (6ce9:34,41 · bb10:139,144,145 · c444:53,131,182) name a config cell instead.
- n35 `experiment/a00-17d2c230-0b33f2.md:66-68` red-probe output (`<home>/…`, which the detector's home class cannot print) carries a note that the observed lines were redacted by the scrub.
- n115 one token for the repo root in the `experiment/a00-1b4d6db0-04de8a.md:53-55` table (today `<repo>` at :53 beside `{root}` at :54-55) — which token is OWNER n6's call.
- n116 `experiment/a00-1b4d6db0-04de8a.md:31` ("Prior bytes … at HEAD 1be529fae") says the quoted bytes at :53 are redacted, not the bytes of that commit.
- n117 `experiment/a00-3f66ba67-f5c25c.md:19` probe 3 `observed` says it was redacted after the run (result `held` unchanged).
- n121 the reproduce commands `experiment/a00-bbdd35c4-595c5f.md:47,63` and the measured clause `a00-28bbc0b9-9d3413.md:35` say the measured prefix was redacted, and point at the reproducer that still holds it (`extensions/agi/tests/test_retired_box_prefix.py`).

## Invariants
- A residue is closed by a reviewed round, never by a note.
- Node answers go through `write.py` only; no home path, box path, user name or hardware name is written back to un-redact evidence — the note says "redacted", the grid keeps the original.

## Falsifier
1. From the repo root:
```bash
bash -c 'N=.agi/nodes; E=$N/experiment
for x in a00-6ce9cb00-d60152 a00-bb10233d-5a7f1f a00-c4441397-c8a8c6; do ! { grep -qE "/data/[a-z]+/" $E/$x.md && grep -q "carries no box path" $E/$x.md; } || exit 1; done &&
! { grep -qF "\`agi_root\` | \`<repo>\`" $E/a00-1b4d6db0-04de8a.md && grep -qF "| \`{root}/" $E/a00-1b4d6db0-04de8a.md; } &&
for f in $E/a00-17d2c230-0b33f2.md $E/a00-1b4d6db0-04de8a.md $E/a00-3f66ba67-f5c25c.md $E/a00-bbdd35c4-595c5f.md $E/a00-28bbc0b9-9d3413.md; do grep -qi redact $f || exit 1; done'
```
   (exits 1 at HEAD 8209a5813; all 9 conjuncts open.)
2. Negative: `git grep -l 'carries no box path' -- .agi/nodes/experiment/a00-6ce9cb00-d60152.md .agi/nodes/experiment/a00-bb10233d-5a7f1f.md .agi/nodes/experiment/a00-c4441397-c8a8c6.md | xargs -r git grep -lE '/data/[a-z]+/' --` prints nothing (3 files at HEAD).

## Out of scope
goal:g1.31.3.1.2 (#5: the moved humaneval folder at bb10:136 · c444:180) · goal:g1.31.3.2 (#33 pi-encoded path in a00-797ee7be; #35 #36 a00-600cf080 M3 / THOUGHT pointers) · OWNER n6 (`<repo>` vs `{root}` vocabulary) · goal:g1.31.5.5.1 · goal:g1.31.5.5.3 · goal:g1.31.5.5.4 · goal:g1.31.5.5.5 · goal:g1.31.5.5.6 · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6**.
