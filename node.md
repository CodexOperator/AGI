---
id: experiment:a00-8b7abc41-e419d5
mint_id: 3520ecbfaf3a47a591443de50f16b194
type: experiment
parents:
  - hypothesis:l4-the-harvest-completion-dm-resolves-the-iter-dir-from-the-dispatching-seats-own-tree
next_edges: []
confidence: 0.85
edited_by: a00-8b7abc41
evidence_runs:
  - experiment:a00-8b7abc41-e419d5
line_ceiling: 40
loop: hypothesis:l4-the-harvest-completion-dm-resolves-the-iter-dir-from-the-dispatching-seats-own-tree@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 51
profile: balanced
role: kid
scaffold_hash: 63d33cf19302b0f9
season: 2
title: Harvest dm resolves the iter dir from the seat own tree
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8b7abc41-e419d5

## Experiment

hypothesis:l4-the-harvest-completion-dm-resolves-the-iter-dir-from-the-
dispatching-seats-own-tree — a g15 BUILD ORDER, not a measurement. Built all
three conjuncts and proved them on the built bytes.

PRE-FIX MEASUREMENT (driven on a fixture: local round tree + sibling seat tree,
manifest only under the seat): `_session_manifest_holders(round_graph, iter) == []`
— the old `if not holders: return` was a silent no-op, so a worktree-seated
seat's harvest dm never fired. That is the SM.66 finding, now asserted in the
suite (`test_a_worktree_seats_harvest_dm_fires_from_the_seats_own_tree`).

CHANGES (production lines: 51 per `git diff --numstat` over cli.py + dispatch.py;
40 code-only, the rest docstring/comment):

1. `cli.py:_session_manifest_holders(root, iter_n, extra_iters=())` — candidate
   order is now local -> the DISPATCHING seat's own iteration dir(s) -> MAIN.
   `extra_iters` entries arrive already resolved as iteration dirs (flag bit in
   the candidate tuple); dedupe by path is unchanged, so local == MAIN is still
   the identity yielding exactly one holder.
2. `cli.py:_alarm_dispatcher_on_done(..., record_path=None)` — the done path
   already resolved the round's record via `_resolve_session_record`; `cmd_done`
   now hands that path in. From it the poster derives `record_path.parents[1]`
   (the seat's own iter dir) and reads `dispatched_from_tree` off the same
   record (the tree dispatch.py wrote at spawn). When NO candidate tree holds a
   manifest it prints exactly one line — `harvest dm NOT sent: no iter manifest
   under <tree-a> or <tree-b>` — to stderr and returns 1. Never silent.
3. `dispatch.py` — `"dispatched_from_tree": str(root)` added as a sibling of
   `dispatched_by` in the SAME `agent_record` dict (one file, one field). It is
   the DISPATCHER's graph root, deliberately NOT the agent's `worktree`
   (`branch_ref["worktree"]`, dispatch.py:2750), which is the CHILD's --branch
   checkout.

## Evidence

`python3 -m pytest extensions/agi/tests/test_dispatch_alarms.py
extensions/agi/tests/test_dispatch_scaffold_unregistered.py -q` -> 16 passed.
Four tests, fixture roots only:

* `test_a_worktree_seats_harvest_dm_fires_from_the_seats_own_tree` — conjunct
  (1): asserts the pre-fix empty holder list, then the dm landing in the shared
  inbox once the record path is threaded through.
* `test_a_main_seated_round_is_unchanged` — conjunct (1) regression guard:
  local == seat == shared yields exactly ONE holder, dm still fires once.
* `test_missing_manifest_is_a_named_line_and_nonzero` — conjunct (2): the exact
  named line on stderr (count 1, both trees named) and rc == 1, replacing the old
  test that asserted a silent skip.
* `test_spawn_record_carries_the_dispatching_seats_own_tree` — conjunct (3):
  drives the REAL `dispatch.main()` spawn with Popen stubbed and asserts the
  manifest record's `dispatched_from_tree == str(graph)`, alongside
  `dispatched_by`, and that it is not the agent's `worktree`.

Wider run for regressions: `extensions/agi/tests/test_cli.py`,
`test_kid_reports_to_parent.py`, `test_completion.py`, `test_after_join_service.py`
(172 passed) and `test_dispatch.py`, `test_evidence_gate.py`, `test_heal.py`,
`test_send.py` (606 passed).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THE TENSION AND HOW I RESOLVED IT. The claim says the poster "exits non-zero";
the docstring says the completion dm "is never fatal to the round" (it runs on
the done: path, whose job is to record the verdict). A naive reading of either
loses the other: making `cmd_done` return non-zero would turn every worktree
round's exit code red and is a regression a probe would catch; returning quietly
is the bug itself. I split the two: `_alarm_dispatcher_on_done` returns 1 and
prints the named line; `cmd_done` ignores that return and still exits 0 after
recording the verdict. Non-silent, not fail-closed. Recorded here so the next
reader sees the choice was deliberate.

MECHANISM, NOT WORDING. `record_path` is the already-resolved record, so no new
worktree scan: `parents[1]` is the iter dir by the same layout `_agent_path`
built. Reading `dispatched_from_tree` off that record gives conjunct (3) a
reader as well as a writer, and the `or str(seat_iter.parents[1])` fallback
keeps rounds that predate the field working. Naming the trees in the failure
line is derived, not hard-coded, so a MAIN-seated refusal names MAIN and a
worktree-seated one names the seat's tree.

LINE COUNT: 51 by numstat (ceiling 40, under the 2x stop at 80). Code-only is
40; the rest is the two doc paragraphs and the dispatch comment. I did not set
`rebrief_request` because the round is complete and green, not stalled — the
overage is documentation weight, disclosed rather than hidden.
<!-- THOUGHT:END -->

## Agent Notes
Built all three conjuncts: _session_manifest_holders takes the seat's own iter dir(s) (local -> seat -> MAIN); the poster derived seat_iter/dispatched_from_tree from the record cmd_done already resolved, and refuses with the exact 'harvest dm NOT sent: no iter manifest under <a> or <b>' stderr line + rc 1 while cmd_done stays 0; dispatch.py records dispatched_from_tree=str(root) in the same agent_record as dispatched_by. 4 fixture tests + 778 regression tests green; 51 production lines.
