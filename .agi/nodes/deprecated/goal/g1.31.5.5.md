---
id: goal:g1.31.5.5
mint_id: 1f9095c973d1497faba83b297e672423
type: goal
parents:
  - goal:g1.31.5
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.5.5
goal_kind: subgoal
origin: goals-doc
scaffold_hash: c29cf04e857435ab
season: 2
seeds: []
status: deprecated
tags:
  - engine
  - pass
  - residue
  - node-answer
title: "G1.31.5.5: 33 PASS B3 missed NODE rows answered on their nodes via write.py -- THOUGHT deltas, redaction notes, scaffolds, citations, verdicts, goal bodies"
town: core
---
# goal:g1.31.5.5

## Why this exists
goal:g1.31.5: PASS B3's verify stages (`.agi/sessions/workflows/runs/mur-pb3*/verify_*.json`, `missed` arrays: 147 reviewer-found rows, not adversarially verified) were triaged against HEAD (`/tmp/dg6/missed/triage.json`): 59 REAL, of which 34 are NODE — answered by an edit on a node, no engine change. Re-checked at HEAD 8209a5813: 34 open, 0 already fixed, 1 moved as DUP (n142 -> goal:g1.31.3.1.1, same node+line as #46) -> 33 rows in 6 leaves, 0 red · 13 residue · 20 nit.

## Target end-state
- goal:g1.31.5.5.1 — every path-scrub version records its delta in THOUGHT (G2.11) (6 rows: n9 n12 n30 n36 n42 n68).
- goal:g1.31.5.5.2 — scrubbed evidence says it was redacted; no scrub THOUGHT over-claims its reach (6: n5 n35 n115 n116 n117 n121).
- goal:g1.31.5.5.3 — no creation scaffold (id-echo title, template prompt), one H1, one `## Agent Notes` (6: n1 n15 n32 n48 n57 n99).
- goal:g1.31.5.5.4 — moved code cited by function or cell key, not stale file:line (6: n14 n20 n31 n61 n122 n137).
- goal:g1.31.5.5.5 — verdicts, caveats and roll-ups agree with the bytes (5: n3 n97 n103 n141 n145; n142 DUP).
- goal:g1.31.5.5.6 — goal bodies match the bytes; probes are schema maps; no prose after THOUGHT:END (4: n37 n70 n80 n98).

```
g1.31.5.5 NODE (33 + 1 DUP)
 ├─ .5.5.1 (6) THOUGHT delta        n9 n12 n30 n36 n42 n68
 ├─ .5.5.2 (6) scrubbed evidence    n5 n35 n115 n116 n117 n121
 ├─ .5.5.3 (6) scaffold + headings  n1 n15 n32 n48 n57 n99
 ├─ .5.5.4 (6) stale citations      n14 n20 n31 n61 n122 n137
 ├─ .5.5.5 (5) verdicts + roll-ups  n3 n97 n103 n141 n145     (n142 -> g1.31.3.1.1)
 └─ .5.5.6 (4) goal bodies + shape  n37 n70 n80 n98
```

## Invariants
- A residue is closed by a reviewed round, never by a note.
- Node answers go through `write.py` only; retire, never delete; no home path, box path, user name, email or hardware name is written while answering.
- Every falsifier greps only its named target node files — never `.agi/nodes/goal/`, whose g1.31.* bodies quote the same strings.

## Falsifier
1. Every child goal:g1.31.5.5.1 · goal:g1.31.5.5.2 · goal:g1.31.5.5.3 · goal:g1.31.5.5.4 · goal:g1.31.5.5.5 · goal:g1.31.5.5.6 is complete (each child's falsifier 1 exits 0; all 6 exit 1 at HEAD 8209a5813).
2. Negative: `git grep -n 'What is the testable claim? What would prove it?' -- .agi/nodes/hypothesis/l3-grid-lock-doubled-path.md .agi/nodes/hypothesis/l3w4-rotation-announces-itself.md .agi/nodes/hypothesis/l4-test-zoom-unresolvable-tier-id-errors-only-inside-the-full-suite.md` returns zero hits (3 at HEAD).

## Out of scope
goal:g1.31.5.1 (reds) · goal:g1.31.5.2 (DG3) · goal:g1.31.5.3 (DG5) · goal:g1.31.5.4 (DG6 engine) · goal:g1.31.1 · goal:g1.31.2 · goal:g1.31.3 · goal:g1.31.4 · OWNER rows n6 n22 n109 n144 · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6**.

<!-- THOUGHT: season3 rollover: deprecated old-engine Python goal; not carried. -->
