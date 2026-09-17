---
id: experiment:a00-1d11cefe-fa8c06
mint_id: 6a2495805af644b2b7173b6deb8a142c
type: experiment
parents:
  - hypothesis:l4-cli-done-refuses-a-kid-past-2x-its-line-ceiling-without-a-rebrief-request
next_edges: []
confidence: 0.9
edited_by: a00-1d11cefe
evidence_runs:
  - experiment:a00-1d11cefe-fa8c06
line_ceiling: 25
loop: hypothesis:l4-cli-done-refuses-a-kid-past-2x-its-line-ceiling-without-a-rebrief-request@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 48
profile: balanced
role: kid
scaffold_hash: 650b4c37d46ef653
season: 2
title: cli.py done refuses a kid past 2x its line ceiling without a rebrief_request
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1d11cefe-fa8c06

## Experiment

G15 BUILD ORDER, not a measurement: implemented the two conjuncts of
hyp:l4-cli-done-refuses-a-kid-past-2x-its-line-ceiling-without-a-rebrief-request,
then proved them on the built bytes.

**Conjunct 1 — `cli.py done` refuses a kid past 2x with no rebrief_request.**
Added `_kid_done_refusal(root, node_id)` in `extensions/agi/bin/cli.py` and
called it in `cmd_done` AFTER the evidence/probe/dry-run gates and BEFORE
`rec["status"] = "done"` / any verdict or node write, so a refused done
mutates nothing (rc 2). It is kid-tier only (`rec.get("tier") == "kid"`) and a
a no-op when the node carries `rebrief_request`. Measurement = the kid's own
uncommitted production diff, `git -C <root> diff --numstat HEAD`, filtered by
the same `_SOURCE_SUFFIXES` / never-`tests/` rule `_kid_measured_lines` uses;
ceiling = the harvest's own `_kid_line_ceiling`. When `lines > 2*ceiling`
with no `rebrief_request`, it prints the exact `write.py <node-id> "set
rebrief_request <N>/<C>: <why>"` line and returns 2.

**Conjunct 2 — brief.py checkpoint wording.** `extensions/agi/bin/brief.py`
`_kid` now says "Checkpoint before `cli.py done`: measure those lines." — the
one checkpoint every kid reaches — replacing the dead "FIRST commit or first
test run" trigger. Ceiling number + measure/record semantics unchanged.

## Evidence

- `git diff --numstat` of the built change: cli.py +46, brief.py +2 = 48
  production lines (under the 50 = 2x:25 hard stop; no re-brief owed).
- `pytest extensions/agi/tests/test_cli_done_kid_ceiling.py
  test_brief.py test_cli.py -q` → **195 passed**. New tests:
  1. `test_done_refuses_a_kid_past_2x_with_no_rebrief_request` — fixture kid
tree (git repo, node `line_ceiling: 40`, 81 uncommitted production lines,
agent `tier: kid`): `cli.cmd_done` returns **2**, stderr carries
`set rebrief_request 81/40: <why>`, and the node keeps no `verdict:` (nothing
written).
  2. `test_done_passes_when_the_rebrief_request_is_on_the_node` — same tree
with `rebrief_request` set on the node: **rc 0**.
  3. `test_kid_brief_checkpoints_before_cli_done_not_at_first_commit` —
assembled kid brief contains "Checkpoint before `cli.py done`" and neither
"FIRST commit" nor "first test run".
- Manual render of `brief.assemble(tier="kid", line_ceiling=25)` confirms the
  checkpoint sentence and a clean ceiling-clause remainder.

## Agent Notes
cli.py done now refuses a kid past 2x its line ceiling with no rebrief_request (rc 2, exact write.py line, nothing written; kid-only, no-op with the request set); brief.py _kid checkpoint rewrote to 'before cli.py done'. 3 new tests, 195 pass, 48 production lines.
