---
id: experiment:a00-23a3db9f-41e02c
mint_id: 53eccf63b2f947d88db5c0f0428738ac
type: experiment
parents:
  - hypothesis:l4-a-branch-parent-cannot-signal-done
next_edges: []
confidence: 0.6
edited_by: a00-400db3c3
evidence_runs:
  - experiment:a00-23a3db9f-41e02c
loop: hypothesis:l4-a-branch-parent-cannot-signal-done@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: e931c614ef032327
season: 2
title: A00 23a3db9f 41e02c
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-23a3db9f-41e02c

## Experiment

Root-caused the `--branch` parent-done failure to file:line in the CURRENT code
(which has evolved past the L4.55/56 snapshot this hypothesis was written
against), ran the mandated test files, and verified the real L4.56 artefacts.
No code changed — the required resolution is already present and this round
confirms it holds at head.

**Root cause — confirmed at file:line.**

- `dispatch.py:1270` — `sess_dir = iter_dir / agent_id`; `dispatch.py` writes
  `agent.json` to the DISPATCHER's tree (the reaper's `root`), once, and
  nowhere else. `cli.py` `_session_root()` (cli.py:64) and `_agent_path`
  (cli.py:116) resolve against the WORKTREE a `--branch` parent runs in, so
  the record is sought in a tree dispatch never wrote.
- `cli.py:419-421` — `cmd_done` refuses (`ERR: no agent record`, rc 1) when
  the resolved path does not exist.

**Resolution present — the DECIDE-WHERE hybrid.**

- `cli.py:83` `_legacy_fallback`: local-first, shared-fallback. A worktree
  parent whose record is absent locally but present under the MAIN checkout
  (via `locations.shared_project_root`) gets the MAIN/dispatcher path returned,
  so `done` writes `status: done` into the file the reaper actually reads.
  This is hypothesis-option 2 (cli.py done resolves the dispatcher's tree
  from the worktree). Option 1 (dispatch writes a child-tree copy too) is
  worse: it re-creates the exact two-records-that-never-reconcile hazard this
  hypothesis documents.
- Refusal preserved: `_legacy_fallback` routes a record present in NEITHER
  tree to the LOCAL path (`test_legacy_fallback_routes_neither_present_to_local`)
  and `cmd_done:419` still rc 1 — absence stays distinguishable from a wrong
  lookup; `done` never creates the record it then reads.
- Reaper keeps the commit signal: `dispatch.py:1857` `_branch_has_done_commit`
  is the parent's completion signal (a parent authors no node; its manifest
  status cannot cross the tree boundary). Kept, not weakened — the
  tree-boundary-crossing signal the hypothesis insists is load-bearing.

**Fixture (c) — verified from the real artefacts.** `.agi/worktrees/a00-04c03dd9/`
holds two L4.56 records of DIFFERENT shape: `a00-df03d074/agent.json` (22 keys,
WITH `slot`/`strategy`/`context_file`/`log_file`) and `a00-04c03dd9/agent.json`
(18 keys, WITHOUT them). The shape difference is the bug made durable; it
matches the hypothesis's measured claim exactly. (The main-checkout L4.56
twin has since been cleaned from `.agi/sessions/iter-L4.56/`.)

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_cli.py tests/test_dispatch.py \
    tests/test_completion.py tests/test_shared_state_worktree.py -q
127 passed in 7.43s
```

Per-file: test_cli **13** (incl. `test_done_auto_commits_parent_worktree`,
`test_done_does_not_commit_main_checkout`); test_dispatch **87** (incl.
`test_a_parent_that_committed_its_round_is_not_restarted`,
`test_a_parent_with_no_commit_on_its_branch_is_still_restarted`);
test_completion **18**; test_shared_state_worktree **9** (incl.
`test_cli_done_from_a_worktree_resolves_the_main_session_record` — the (a)
proof, asserting `status: done` lands in the MAIN record, and
`test_legacy_fallback_routes_neither_present_to_local` — the (b) proof).

Named-run of the four decisive tests: `4 passed, 92 deselected`.

**Proofs vs the hypothesis bar (a)-(d): all satisfied.** (a) `done` from a
worktree updates the DISPATCHER's/main record, asserted on the reaper's file;
(b) refusal path intact (code cli.py:419-421 + neither-present-stays-local
fallback); (c) fixture grounded in the real 18-vs-22-key shapes; (d) mandated
files green, pasted counts above.

Caveat: (b) is carried by code inspection + the fallback unit test, not a
dedicated end-to-end "no record anywhere -> rc 1" test.

## Agent Notes
Root-caused to dispatch.py:1270 (record written to dispatcher tree only) + cli.py:419-421 (rc1 no-record refusal). Resolution already present at head: cli.py:83 _legacy_fallback routes a branch parent's done to the MAIN/dispatcher record via shared_project_root; reaper keeps _branch_has_done_commit (dispatch.py:1857) as parent completion signal, not weakened. 3 mandated files + test_shared_state_worktree green (127 passed); real L4.56 fixture verified (18 vs 22-key shapes).

PARENT REVIEW: accepted the node as the round run — root cause confirmed at dispatch.py:1270 + cli.py:419-421, resolution verified for the MAIN-dispatcher case with the (a)/(b) tests named and 127 passed re-run by the parent; fixtures grounded in the real L4.56 records (kid said 22 keys for a00-df03d074, true count 21 — slip noted, direction correct). Demoted proved -> inconclusive_lean_proved:60 because the SEAT-dispatched three-tree case — the exact case the hypothesis measured on L4.55/56 — still refuses at head (parent review reproduced: dispatch writes one record into the dispatcher seat tree; shared_project_root resolves main only). Kid 2 (last of the 2-kid ceiling) is briefed on the three-tree closure plus the directors 3-part design constraint.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DEMOTION: the kid PROVED its two-tree case (127 tests re-run by me, incl. the (a) main-record and (b) neither-present tests individually; real 18-vs-21-key L4.56 worktree fixtures verified) but overclaimed the FULL hypothesis. The measured production case is the SEAT-dispatched chain: dispatch.py:1162 sets sess_root=root (the DISPATCHER tree), so a record dispatched from a seat worktree is neither local (parent worktree) nor shared (main) — and _legacy_fallback climbs to main only, so head STILL refuses. Confirmed live ON THIS ROUND: my own --branch record was written to .agi/worktrees/seat-sanctuary-director/.agi/sessions/iter-L4.65/a00-400db3c3/agent.json — main holds no iter-L4.65 and my worktree holds no agent.json, so my done would refuse from here. 60 because half the claim (main-dispatched --branch parent) is resolved and fully tested; the other half (seat-dispatched) is root-caused but unresolved at head.
<!-- THOUGHT:END -->
