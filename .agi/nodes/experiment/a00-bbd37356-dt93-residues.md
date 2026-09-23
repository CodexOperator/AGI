---
id: experiment:a00-bbd37356-dt93-residues
mint_id: 5a4211171a754d80a0919f1fa9909308
type: experiment
parents:
  - hypothesis:a00-bbd37356-5bcd9a
next_edges: []
edited_by: a00-bbd37356
line_ceiling: 40
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: f1ee273f740950c2
season: 2
thought_session: iter-DT.93
title: "DT.93: four MUR residues on goal:g7.32.1 cleared or accurately reflected"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-bbd37356-dt93-residues

## Experiment

DT.93 residual round on `goal:g7.32.1` (Grok session ingest), against base tip
`cb7ed04af`, worktree `a00-bbd37356`. No new feature work: clear or accurately
reflect the four MUR residues. Every node edit went through `write.py`; no git,
no `grid.py`, no payload bytes moved.

**Residue 1 — provenance on `hypothesis:a00-4c9e6d97-b569a4`.** Live
frontmatter read this round: `verdict: proved`,
`evidence_runs: [experiment:a00-4c9e6d97-dt90-residues]`; that experiment node
is `type: experiment` with `parents: [hypothesis:a00-4c9e6d97-b569a4]`, 11
probes across conjuncts 1 and 2. The authored THOUGHT block and `## Agent
Notes` were whole-replaced (`'replace body 31:33 -'`, `'replace body 35:58 -'`)
so both now state: verdict `proved`, `evidence_runs` is a real authored
experiment, **the gate did NOT demote at tip**, and the landed parent-review
probes are named. The stale literal `inconclusive_lean_proved:50` is gone
(measured absent).

**Residue 4 — `goal:g7.32.1` Agent Notes / residue table.** Whole-replaced
(`'replace body 39:88 -'`) with six ingest-chain rows, each `verdict:` re-read
from its live node this round, plus a four-row residue table naming the four
MUR residues; the node's THOUGHT was rewritten (`'replace body 87:89 -'`) to
describe this version. Exactly one `## Agent Notes` heading, one THOUGHT region.

**Residue 2 — unpinned stored contract (KNOWN GAP, not patched).** The DT.90
freshness check (`stored contract == fresh level3 derivation`) lives only in a
tmp fixture under `.agi/sessions/iter-DT.90/...`; nothing committed pins it.
Adding a re-derivation test to `extensions/agi/tests/test_ingest_session.py` is
self-defeating: the new test symbol changes the payload's symbol set, so the
freshly derived contract immediately differs from the stored one — the test
fails against the very node it is meant to guard. Documented on the goal node
as a KNOWN GAP with that mechanism; the test was deliberately NOT added.

**Residue 3 — MUR-stage timeout dirt.** Measured clean: no uncommitted WT dirt;
`extensions/agi/bin/workflow.py` holds `_DEFAULT_STAGE_TIMEOUT_S = 3600` and
`extensions/agi/workflows/merge-up-review.json` declares `timeout_s: 1800` twice
(lines 153 and 259). The dispatch wrote the default as "60->600"; the live bytes
say 600->3600 since SM.105, so the measured value is the one recorded.

## Evidence

`python3 .agi/sessions/iter-DT.93/a00-bbd37356/verify_dt93.py`:

```
RESIDUE-4 rows parsed: 6
  a00-e5ef202a-0326f9          table=proved                     live=proved
  a00-c192a02d-f1ce7a          table=proved                     live=proved
  a00-dee8ad86-1ab674          table=inconclusive_lean_disproved:70 live=inconclusive_lean_disproved:70
  a00-a317e857-9dba03          table=inconclusive_lean_disproved:60 live=inconclusive_lean_disproved:60
  a00-a960d972-431933          table=proved                     live=proved
  a00-e9212044-470a98          table=proved                     live=proved
RESIDUE-4 mismatches: []
RESIDUE-4 ^## Agent Notes$ count: 1
RESIDUE-4 thought markers: 1 1
RESIDUE-1 verdict: proved | evidence_runs: ['experiment:a00-4c9e6d97-dt90-residues']
RESIDUE-1 probe count: 11 | conjuncts: [1, 2]
RESIDUE-1 stale literal 'inconclusive_lean_proved:50' present: False
RESIDUE-1 says gate did NOT demote at tip: True
RESIDUE-1 ^## Agent Notes$ count: 1 | thought markers: 1 1
RESIDUE-1 experiment node type: experiment | parents: ['hypothesis:a00-4c9e6d97-b569a4']
RESIDUE-3 workflow _DEFAULT_STAGE_TIMEOUT_S: 3600
RESIDUE-3 merge-up-review timeout_s values: ['1800', '1800']
RESIDUE-2 contract re-derivation test present in pinned file: False
RESIDUE-2 KNOWN GAP documented on goal: True | self-defeating mechanism named: True
```

`write.py` accept lines (all four edits):

```
updated: hypothesis:a00-4c9e6d97-b569a4
updated: hypothesis:a00-4c9e6d97-b569a4
updated: goal:g7.32.1
updated: goal:g7.32.1
```

Scratch files:
`.agi/sessions/iter-DT.93/a00-bbd37356/{verify_dt93.py,verify_out.txt,hyp_thought.txt,hyp_notes.txt,goal_notes.txt,goal_thought.txt}`.

## Production lines
`git diff --numstat` (node prose only): `.agi/nodes/goal/g7.32.1.md` +36/-38, `.agi/nodes/hypothesis/a00-4c9e6d97-b569a4.md` +26/-9. No engine or test file was touched, so `production_lines: 0` against `line_ceiling: 40`; the experiment node itself is new/untracked.
