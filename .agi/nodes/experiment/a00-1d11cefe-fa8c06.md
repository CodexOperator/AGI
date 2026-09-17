---
id: experiment:a00-1d11cefe-fa8c06
mint_id: 6a2495805af644b2b7173b6deb8a142c
type: experiment
parents:
  - hypothesis:l4-cli-done-refuses-a-kid-past-2x-its-line-ceiling-without-a-rebrief-request
next_edges: []
confidence: 0.9
edited_by: a00-593f494d
evidence_runs:
  - experiment:a00-1d11cefe-fa8c06
line_ceiling: 25
loop: hypothesis:l4-cli-done-refuses-a-kid-past-2x-its-line-ceiling-without-a-rebrief-request@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent fixture kid-tier record, node line_ceiling=30, 61 uncommitted production lines (61>60=2x) no rebrief_request; cli.cmd_done", "expected": "rc 2, stderr carries the exact write.py rebrief_request line, node keeps no verdict: (nothing written)", "observed": "rc 2; stderr has set rebrief_request 61/30; node frontmatter has no verdict:", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "stub cli._kid_done_refusal to log the call + return a refusal; run cmd_done on a kid-tier record", "expected": "cmd_done returns 2 and the stub saw the node id, proving the call site reaches the new function", "observed": "rc 2; stub got node_id=experiment:pe1; refused-by-stub on stderr", "result": "pass"}
  - {"conjunct": 1, "class": "auth", "cmd": "same 61/30 tree but agent record tier=parent (a caller the claim never authorises refusal for)", "expected": "rc 0 and no done-refused message (the gate refuses kids only)", "observed": "rc 0; done refused absent from stderr", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "brief.assemble(tier=kid, line_ceiling=40); scan the rendered kid brief for the checkpoint sentence", "expected": "checkpoint reads Checkpoint before cli.py done; FIRST commit / first test run absent; ceiling number intact", "observed": "new wording present in the rendered brief; old wording absent; PRODUCTION-LINE CEILING: 40 lines intact", "result": "pass"}
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent (a00-593f494d) review of kid a00-1d11cefe-fa8c06: read the bytes of commit c31643258 against merge-base 7c6640a60, not the result file. The kid's own suite (195 passed) is its CLAIM, so I ran 4 independent negative probes of my own (P1-P4, recorded above under probes:) -- gate (61/30 no request -> rc 2 + exact write.py line + nothing written), wire (cmd_done reaches _kid_done_refusal), auth (parent-tier past ceiling is NOT refused -- refusal correctly kid-scoped), and conjunct-2 wire (brief renders Checkpoint before cli.py done, old wording gone). All pass. The two conjuncts are implemented in the delivered diff: _kid_done_refusal + cmd_done hook and the brief wording. Three caveats, none demoting: (1) measurement is git diff --numstat HEAD, which counts staged+tracked mods but NOT untracked production files -- the kid's fixture stages its file, matching the "kid work lands as tracked mods" reality; (2) _kid_done_refusal passes the kid node_id as ceiling target where the harvest passes the hypothesis target id -- they agree whenever the node carries line_ceiling (the normal case), could differ on config-default fallback; (3) the ceiling check sits AFTER the --dry-run early-return, so a kid dry-run never sees a would-be refusal. Verdict proved upheld on my probes.
<!-- THOUGHT:END -->
