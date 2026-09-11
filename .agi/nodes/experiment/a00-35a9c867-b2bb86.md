---
id: experiment:a00-35a9c867-b2bb86
mint_id: 548302c725b842229a0b97e8370a2091
type: experiment
parents:
  - hypothesis:harvest-table-subcommand
next_edges: []
confidence: 0.8
evidence_runs:
  - experiment:a00-35a9c867-b2bb86
loop: hypothesis:harvest-table-subcommand@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: dff3bf6212026b1b
season: 2
title: A00 35a9c867 b2bb86
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-35a9c867-b2bb86

## Experiment

Build-order round for hypothesis:harvest-table-subcommand (its own falsifier:
a live round whose kid-node-ids the table gets wrong when checked by hand).
The parent (a00-9535d851) hit that falsifier: `harvest-table --round
iter-L4.243` attributed the PREVIOUS round's kid
`experiment:a00-9018b453-249cf6` to this round, because `cmd_harvest_table`
resolved the diff base ONCE from the main checkout's current branch
(`season/s2`) instead of from each agent record's `base_branch`.

## Root cause (two defects, one fix)

1. **Base resolved from main's branch, not the round's.** `cmd_harvest_table`
   computed `parent = git branch --show-current` on the main checkout and
   diffed every round against it. On this tree main sits on `season/s2` while
   rounds are cut from `seat/sanctuary-director@s2`, so the diff spanned every
   round since season/s2 and over-attributed earlier rounds' kids.
   `dispatch.py:1931` already records the correct per-agent
   `base_branch` in the manifest — the tool ignored it.
2. **Fallback fired on a resolvable-but-empty diff.** The on-disk fallback
   (scan `wt/.agi/nodes/experiment/*.md` for the target slug) ran whenever
   `not rows_kid and wt.is_dir()`. A freshly cut round with a legitimately
   empty git diff (tip equals base) adopted the previous round's experiment
   node out of the shared worktree checkout.

## Fix (extensions/agi/bin/rotate.py, additive)

- `_harvest_diffstat` now returns `(stat, kids, resolved)`; `resolved` is True
  when the branch resolved AND a merge-base exists — a legitimately empty diff
  is git's honest "no changes" answer, `resolved=True`, no kids.
- Inside the agent loop the base is resolved PER AGENT:
  `base = a.get("base_branch") or parent` (manifest wins; main's current
  branch only when the record has none). Still diffed via
  `merge-base(base, branch)..branch`, never a moved base tip.
- The on-disk fallback now fires only when `not resolved` (git could not
  answer at all), stated explicitly in the code comment.

## Red-first test

`test_harvest_table.py::test_git_base_resolved_per_agent_prevents_cross_round_over_attribution`:
round A branches from master and commits kid A; round B branches from round
A's branch and commits kid B; both worktrees exist; main is left on master;
both manifests record `base_branch`. Asserted `--round B` lists kid B and NOT
kid A (and `--round A` lists kid A). On pre-fix code this FAILED with
`experiment:a00-kidA,experiment:a00-kidB` (over-attribution reproduced).
After the fix it PASSES.

## Evidence

RED (pre-fix):
`pytest extensions/agi/tests/test_harvest_table.py::test_git_base_per_agent... -q`
FAILED — row showed `experiment:a00-kidA,experiment:a00-kidB`.

GREEN (post-fix):
`pytest extensions/agi/tests/test_harvest_table.py -q` → 5 passed.

Live check (this round, main on season/s2, per-agent base from manifest):
`python3 extensions/agi/bin/rotate.py harvest-table --round iter-L4.243 --root .`
→
`iter-L4.243 | a00-35a9c867 | loop/hypothesis-harvest-table-subcomm-a00-35a9c867@s2 | /home/ubuntu/work/agi/.agi/worktrees/a00-35a9c867 | - | - | -`
The stale `experiment:a00-9018b453-249cf6` adoption is gone (empty diff =>
resolved, kids "-").

Suites: test_harvest_table.py 5 passed; test_rotate.py + test_rotate_complete.py
+ test_bin_help_smoke.py → 177 passed, 1 skipped (pre-existing skip).

## Agent Notes
harvest-table: diff base resolved per-agent from manifest base_branch (fallback main branch only when absent); on-disk fallback gated on git unable-to-resolve; RED-first git fixture test reproduced cross-round over-attribution and passes after fix
