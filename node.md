---
id: experiment:a00-ca0a163b-915416
mint_id: 987ccf8368134b01b50486bfc34e08ad
type: experiment
parents:
  - hypothesis:l4-quick-migrate-one-verb-moves-a-post-to-another-box-as-a-fresh-rotation-from-the-card-or-a-transcript-fork-over-the-git-messaging-layer
next_edges: []
confidence: 0.85
edited_by: a00-2a62c783
evidence_runs:
  - experiment:a00-ca0a163b-915416
line_ceiling: 120
loop: hypothesis:l4-quick-migrate-one-verb-moves-a-post-to-another-box-as-a-fresh-rotation-from-the-card-or-a-transcript-fork-over-the-git-messaging-layer@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "2 seating cells written under the schema-resolved actor, session cells as the post", "class": "wire", "cmd": "parent probe B: real cmd_migrate_receive -> real _write_identity_cells -> write.submit against a real posts.md + [config].md fixture; the identity writer is NOT mocked", "expected": "box/worktree land on the moved post row under sanctuary-master; window/pid land as the post", "observed": "rc 0; posts.md carries box boxB, worktrees/post-p, pid 4242; two writer lines printed", "result": "held"}
  - {"conjunct": "self_row stays untouched -- a post never re-seats itself (L4.110 ruling B)", "class": "auth", "cmd": "parent probe A: rotate._write_identity_cells(seat=p, actor=p, role=director, cells={box,worktree})", "expected": "REFUSED by name", "observed": "EditError: a seated role may update only its OWN row and only the declared fields; field box is not in the self-row fields", "result": "held"}
  - {"conjunct": "2 an absent grant names the skip and never aborts the tick", "class": "gate", "cmd": "parent probe C: the same receive with the sanctuary-master actor_rows entry REMOVED from [config].md", "expected": "SKIP by name, session cells still written, rc 0", "observed": "SKIP: no actor_rows grant covers box/worktree for p (the seating cells were not written); rc 0; pid 4242 written", "result": "held"}
  - {"conjunct": "3 residual robustness (out of the node declared scope, named not hidden)", "class": "gate", "cmd": "parent probe C2: actor_rows entry PRESENT but names an actor write.py does not admit (actor: nobody)", "expected": "fail-closed, but the tick should survive one bad record", "observed": "EditError propagates out of cmd_migrate_receive -- the identity writes sit outside the only try/except (which catches OSError only), so the whole receive tick aborts for every pending record", "result": "edge -- a broken-grant config aborts the tick; the absent-grant path is handled"}
production_lines: 79
profile: balanced
role: kid
scaffold_hash: 34fd2341106195f3
season: 2
title: "SM.123 slice 5: seating cells (box, worktree) written under the schema-declared master actor, session cells stay the post own self_row write"
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-ca0a163b-915416

## Experiment

SM.123 slice 5 -- implement the sanctuary-master gen-10 design call (option b)
on the quick-migrate TARGET side. Slice 4 delivered the receive tick, but its
ONE `_write_identity_cells(root, seat=post, actor=post, cells={box, worktree,
window, pid, ...})` call wrote the SEATING cells as the post itself.
`worktree` is in `write.SELF_ROW_PROTECTED` and NOT in `[config].md`'s
`self_row.fields`, so `_self_row_refusal` refused the whole write and
`write.submit` raised `EditError`; that call sits outside the receive tick's
`except OSError`, so the whole receive tick aborted (slice-4 VERIFY demote,
experiment:a00-ccab16ad-03d9b3). Every receive test mocked
`_write_identity_cells`, so nothing drove the real writer.

Built (production paths `extensions/agi/bin/rotate.py`,
`extensions/agi/bin/migrate_channel.py`; 79 changed lines, ceiling 120):

1. `rotate._migrate_seating_actor(root)` -- resolves the actor for the
   SEATING cells from `context/schemas/[config].md` `actor_rows`: the entry
   whose `list_key` equals the geometry resolver's list key (`posts`) and
   whose `fields` cover BOTH `box` and `worktree`. No post name literal in
   rotate.py; the schema stays the single place a grant changes.
2. `rotate.cmd_migrate_receive` splits the one write into two:
   SESSION cells (`window`, `pid`, `session_id`, `session_name`) stay the
   post's own `self_row` write (`actor=post`), and SEATING cells (`box`,
   `worktree`) go through `actor=<schema actor>` (sanctuary-master). An
   absent grant names the skip by line and writes no seating cell, never
   aborts the tick. `self_row.fields` and `SELF_ROW_PROTECTED` are unchanged.
3. `rotate._migrate_seat` resolves the worktree directory from the row's OWN
   `worktree` cell when it carries one (relative resolves against MAIN, the
   `_fd_seat_worktree` rule); the `.agi/worktrees/post-<seat>` convention is
   only the EMPTY-cell fallback, and the SAME spelling is written back.
4. `migrate_channel.verify_record` picks the legacy key order by the
   NORMALISED stage value (`str(stage).strip()`), matching `parse_record`'s
   read of a present-but-blank `stage: ""` as `request`. Before this a
   blank-stage legacy record parsed as request and then FAILED verification.

Tests (excluded from the production-line count):
`extensions/agi/tests/test_migrate_channel.py`
- `test_receive_writes_seating_cells_under_the_master_and_refuses_the_post`:
  the BINDING test. A real `.agi` graph root with the LIVE `[config].md` and
  a real `posts.md`; `_migrate_row`/`_migrate_seat` are the only mocks, so
  the real `_write_identity_cells -> write.submit` path runs. Asserts
  `box: boxB` and the worktree cell LAND on p's row under the master actor,
  AND that the SAME seating write as the post itself (`actor="p"`) raises
  `EditError` naming the own-row rule.
- `test_a_blank_stage_record_reads_as_request_and_verifies`.
- `test_seating_uses_the_rows_own_worktree_cell_when_set`.
- updated `test_receive_seats_once...` (session-only call on a bare root)
  and `test_receive_marks_the_moved_post_as_a_worktree_never_main` (asserts
  the seating call's actor is the master).

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_migrate_channel.py -q
30 passed, 2 warnings in 1.13s

$ python3 -m pytest extensions/agi/tests/test_write_actor_rows.py \
    extensions/agi/tests/test_rotate_identity_main.py \
    extensions/agi/tests/test_write_master_sensei.py -q
55 passed, 28 warnings in 10.76s

$ python3 -m pytest extensions/agi/tests/test_rotate_handover.py \
    extensions/agi/tests/test_post_rename.py -q
72 passed, 256 warnings in 36.75s

$ git diff --numstat -- extensions/agi/bin/rotate.py \
    extensions/agi/bin/migrate_channel.py
4	1	extensions/agi/bin/migrate_channel.py
67	7	extensions/agi/bin/rotate.py      # 79 changed, ceiling 120
```

THOUGHT: option (b) is taken literally -- the seating cells are the master's
row-list authority (the `actor_rows` grant already lists `box` and
`worktree`), while the post keeps its own session cells, so a post still
never re-seats itself (L4.110 ruling B) and neither `self_row.fields` nor
`SELF_ROW_PROTECTED` was widened. The grant actor is looked up by list_key +
required fields, never spelled in rotate.py.

## Agent Notes
Slice 5 built: seating cells (box, worktree) now written under the schema-declared actor_rows master via _migrate_seating_actor; session cells stay the post own self_row write; worktree from the row own cell; blank-stage verify fixed. Real-writer binding test (live [config].md + posts.md fixture) asserts the seating cells land under sanctuary-master and the same write as the post is refused by name. 30+55+72 tests green; 79 production lines vs 120 ceiling.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-2a62c783, iter 151): accepted, kid proved -> inconclusive_lean_proved:85. Headline mechanism verified by MY OWN probes on the committed bytes, not by the kids suite.

(1) THE INSTRUCTION SAID the receive tick must write the row identity cells "through the ONE writer" with seating cells (box, worktree) under the masters actor and SESSION cells as the post, with self_row untouched.
(2) THE MACHINE ACTUALLY DOES (probe B, myself, real writer, writer NOT mocked): cmd_migrate_receive on a real git repo + real posts.md + live [config].md lands box=boxB, worktrees/post-p and pid=4242 in posts.md, rc 0. Probe A (auth) re-run on the new bytes still REFUSES the same seating write as actor=p by name. Probe C (gate) with the actor_rows entry removed prints "no actor_rows grant covers box/worktree" and still writes the session cells, rc 0. All three held.
(3) NEAR MISS: driving the tick with the real writer is the only way to see the wall; the kid did keep the binding test real (test_receive_writes_seating_cells_under_the_master_and_refuses_the_post reads posts.md and re-raises as the post) -- verified in the diff.
(4) DEVIATION: I run a fourth probe (C2) the node does not claim: a grant PRESENT but naming an actor write.py does not admit raises EditError OUTSIDE the only try/except, aborting the whole tick. I recorded it as an edge probe rather than hiding it, and left the verdict at lean_proved because the absent-grant path the node DOES claim holds and the C2 state is a broken-schema config error, fail-closed. Named here so a later slice can wrap the identity writes in one catch if it wants the tick crash-free for that state too.
<!-- THOUGHT:END -->
