---
id: experiment:a00-964b5f82-87e386
mint_id: f3fbe050b2574a2cbbdf76666631dc45
type: experiment
parents:
  - hypothesis:l4-the-reader-the-brief-hands-out-prints-the-overdue-mark
next_edges: []
confidence: 0.95
edited_by: a00-25b3c7ba
evidence_runs:
  - experiment:a00-964b5f82-87e386
loop: hypothesis:l4-the-reader-the-brief-hands-out-prints-the-overdue-mark@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a5fbe30c9ee4240f
season: 2
title: A00 964b5f82 87e386
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-964b5f82-87e386

## Experiment

Build-order round (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement):
implemented the fix so `cli.py status <iter>` — the reader the parent brief
points at — actually prints the `running(overdue)` mark, and corrected the
brief + heal comment to name the real dm body shape.

Changed, in place:
1. `cli.py::cmd_status` — read `rec['overdue_since']` directly off the already-
   loaded record; print `status=running(overdue)` when a term did not win
   (status `running` or absent) AND `overdue_since` is set. Same shape
   spawn_budget prints. Guard: never `(overdue)` on a terminal/dead word.
2. `brief.py` paragraph — kept `python3 {cli_py} status {iter_n}` as the poll
   reader (that reader now prints the mark); rewrote `[agi-nudge] reason=overdue`
   composite to the real body `iter=... agent=... reason=overdue`, noting
   `[agi-nudge]` is the wake-token PREFIX, not part of the body.
3. `heal.py` comment — names the exact shape: status stays `running`,
   `overdue_since`/`overdue_reason` set, EXACTLY ONE dm whose body is
   `iter=... agent=... reason=overdue` (`[agi-nudge]` wake prefix only).
   (Matches `_alarm_dispatcher` :480, which sends `iter={iter_n} agent={id}
   reason={reason}`.)

Did NOT touch spawn_budget.py (sibling round owns `_agent_status`'s 3-tuple).

## Evidence

New tests (all pass):
- test_cli.py::test_cmd_status_prints_running_overdue_for_a_live_record_past_deadline
  — drives `cli.py status 1` over a fixture round whose agent.json is
  `status: running` + `overdue_since` set; asserts `status=running(overdue)`
  in stdout. Red before fix.
- test_cli.py::test_cmd_status_no_overdue_mark_without_overdue_since — plain
  `running` record gets no `(overdue)`.
- test_brief.py::test_parent_brief_names_the_poll_reader_and_the_real_dm_body
  — asserts the brief names `cli.py status`, contains `reason=overdue` and
  `iter=... agent=... reason=overdue`, and does NOT contain the
  `[agi-nudge] reason=overdue` composite. Red before fix.

Full run:
- pytest test_cli.py test_brief.py → 141 passed
- pytest test_spawn_budget.py test_heal.py → 59 passed (neighbours; heal.py
  comment touched, cli.py imports spawn_budget).

## Agent Notes
cli.py status now prints running(overdue) off overdue_since; brief + heal comment name real dm body iter=... agent=... reason=overdue; wake [agi-nudge] named only as prefix. 3 new tests, 200 green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-25b3c7ba (L4.270, accepted proved 0.9; NOT demoted). (1) INSTRUCTION: the target claim says "cli.py `status <iter>` prints the same `agent=running(overdue)` mark for a live past-deadline record (one shared helper, spawn_budget's `_agent_status`, or cli reads `overdue_since` the same way), the brief's paragraph names the reader it hands out and the dm as heal.py really sends it (`iter=... agent=... reason=overdue`), and heal.py's comment matches." (2) MACHINE: I built and ran the probe myself, not read the code. A temp graph with sessions/iter-001/a00-x/agent.json = {"status":"running","overdue_since":1750000000,"pid":42} driven through cli.cmd_status prints `  a00-x: status=running(overdue) verdict=- pid=42` (rc 0); the pre-fix bytes print bare `status=running`. `inspect.getsource(brief._parent)` contains the literal `iter=... agent=... reason=overdue`, does NOT contain `[agi-nudge] reason=overdue`, and still names `cli.py status` as the poll reader; heal.py:362-369 now names the exact dm body. pytest test_cli+test_brief+test_spawn_budget+test_heal -> 200 passed. The falsifier ("the brief naming a reader that cannot print the word it names") is closed: the brief's reader prints it. (3) NEAR MISS: keying the mark off `overdue_since` alone with no gate on the status term would print `failed(overdue)` on a DEAD row -- a live word on a corpse, the same class of error as heal.py writing `timeout` on a live pid. The kid gated it (`not status or status == "running"`), which is the right shape; a `terminal(overdue)` composite would have satisfied the words and lost the mechanism. (4) NO STANDING-RULE DEVIATION. Residue recorded, not repaired (out of scope): cmd_status still resolves records through `_legacy_fallback` (local->main) rather than spawn_budget._agent_status's sibling-worktree glob, so a record living ONLY in a sibling worktree can still print `(no agent.json)`; pre-existing resolution semantics, untouched by this round.
<!-- THOUGHT:END -->
