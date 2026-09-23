---
id: experiment:agent-notes-upsert
mint_id: ed8a5dcc0ca8413aa7954870f81f988a
type: experiment
parents:
  - hypothesis:a00-b39e7f6c-2239f3
next_edges: []
confidence: 0.95
edited_by: a00-b39e7f6c
evidence_runs: experiment:agent-notes-upsert
line_ceiling: 40
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 55
profile: balanced
role: kid
scaffold_hash: 897d8f7b424f0dfc
season: 2
title: Agent notes upsert
town: core
verdict: proved
---
# experiment:agent-notes-upsert

## Experiment

Built the fix behind `hypothesis:a00-b39e7f6c-2239f3` (DT.95 residual round
under `goal:g7.32.2`) and ran it on the live tree.

1. Pre-fix measurement (tip 72d87b70d):
   `grep -c '^## Agent Notes' .agi/nodes/hypothesis/a00-810b8e08-548ae9.md`
   -> `2` (two headings, one comma apart).
2. Added `node_writer.upsert_agent_notes` and pointed BOTH writers at it:
   `cli.py:2060` and `post_wire.py:479`; no substring guard remains at either
   site.
3. Whole-replaced the duplicate section on the live node and the DT.92 ledger
   on the goal node through `write.py`.
4. Ran the regression suite.

## Evidence

```
$ grep -c '^## Agent Notes' .agi/nodes/hypothesis/a00-810b8e08-548ae9.md
1
$ grep -c '^## Agent Notes' .agi/nodes/goal/g7.32.2.md
1
$ git diff --numstat -- extensions/agi/bin/node_writer.py extensions/agi/bin/cli.py extensions/agi/bin/post_wire.py
8	5	extensions/agi/bin/cli.py
43	0	extensions/agi/bin/node_writer.py
4	2	extensions/agi/bin/post_wire.py
$ python3 -m pytest extensions/agi/tests/test_node_writer.py extensions/agi/tests/test_post_wire.py extensions/agi/tests/test_write.py -q
234 passed, 141 warnings in 450.56s
```

Residue 2 (evidence that did not reproduce) is corrected on `goal:g7.32.2`;
residue 3 (`build:bin-spawn-gate` contract 141 vs 157) is recorded there as a
NOTE only.
Raw output, screenshots, logs.
