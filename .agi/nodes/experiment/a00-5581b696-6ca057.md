---
id: experiment:a00-5581b696-6ca057
mint_id: 1dc77b21aaa44a73aa96076d5f7c4e39
type: experiment
parents:
  - hypothesis:l4-quick-migrate-one-verb-moves-a-post-to-another-box-as-a-fresh-rotation-from-the-card-or-a-transcript-fork-over-the-git-messaging-layer
next_edges: []
confidence: 0.9
edited_by: a00-d54a4d3b
evidence_runs:
  - experiment:a00-5581b696-6ca057
line_ceiling: 4
loop: hypothesis:l4-quick-migrate-one-verb-moves-a-post-to-another-box-as-a-fresh-rotation-from-the-card-or-a-transcript-fork-over-the-git-messaging-layer@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 6, "class": "gate", "cmd": "cmd_migrate_receive with _migrate_seating_actor->\"\" and seat_cells non-empty", "expected": "SKIP line, 0 acks, request byte-identical, no seated line", "observed": "probe1 ok=True rc=0 acks=0 record_unchanged=True skip=True seated_line=False", "result": "refused"}
  - {"conjunct": 6, "class": "gate", "cmd": "same call with a valid master grant (control)", "expected": "one ack, stage=seated, seated line present", "observed": "probe2 ok=True acks=1 stage=seated seated_line=True row_box=True", "result": "allowed"}
  - {"conjunct": 6, "class": "wire", "cmd": "master-grant path writes seating cells via _write_identity_cells", "expected": "actor == master, not p", "observed": "probe3 ok=True seating_calls=1 actor=sanctuary-master cells=[box,worktree]", "result": "allowed"}
  - {"conjunct": 6, "class": "auth", "cmd": "_write_identity_cells(seat=p, actor=p, cells={box,worktree})", "expected": "refused by name (post never re-seats itself)", "observed": "probe4 ok=True EditError may update only its OWN row", "result": "refused"}
  - {"conjunct": 6, "class": "gate", "by": "parent:a00-d54a4d3b", "cmd": "cmd_migrate_receive, _migrate_seating_actor->'' , seat_cells={box,worktree} (committed 129ca926d)", "expected": "SKIP printed, 0 acks, request byte-identical, no 'seated' line", "observed": "rc=0 acks=0 stages=[] seated_line=False skip=True req_unchanged=True", "result": "held"}
  - {"conjunct": 6, "class": "gate", "by": "parent:a00-d54a4d3b", "cmd": "CONTROL: same call with _migrate_seating_actor->'sanctuary-master'", "expected": "1 ack stage=seated, seating write actor=master, 'seated p on boxB'", "observed": "rc=0 acks=1 stages=['seated'] actor=sanctuary-master seated_line=True skip=False", "result": "held"}
  - {"conjunct": 6, "class": "wire", "by": "parent:a00-d54a4d3b", "cmd": "CONTROL: seat_cells empty (session cells only), no grant", "expected": "1 ack -- the gate fires only when seating cells exist", "observed": "rc=0 acks=1 stages=['seated'] seated_line=True skip=False", "result": "held"}
  - {"conjunct": 6, "class": "auth", "by": "parent:a00-d54a4d3b", "cmd": "rotate._write_identity_cells(seat='p', actor='p', cells={box,worktree}) against a real graph", "expected": "refused by name -- a post never re-seats itself", "observed": "EditError: a seated role may update only its OWN row ... field 'box' is not in the self-row fields", "result": "held"}
production_lines: 3
profile: balanced
role: kid
scaffold_hash: 85f7d4a5a43f0bb3
season: 2
testable_claim: a cmd_migrate_receive that cannot write the seating cells for want of an actor_rows grant writes NO seated ack and leaves the request record byte-identical
title: a receive with no seating grant writes no seated ack and leaves the request record as it was
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5581b696-6ca057

SM.123 slice 6 — the last unfinished conjunct of the quick-migrate chain.

## Experiment

Slice 5 split the receive-side identity writes: SESSION cells are the post's
own self_row write, SEATING cells (box, worktree) go through the schema-
resolved master actor. But when no `actor_rows` grant covers box/worktree the
code printed the SKIP line and then FELL THROUGH, writing a `stage: seated`
ack and printing `seated <post> on <me>` anyway — a receive that could not seat
claimed it had.

BUILT (g15 claim = behaviour to build, not to measure):

- `extensions/agi/bin/rotate.py:20740-20744` (`cmd_migrate_receive`): added
  `continue` after the SKIP print inside the `elif seat_cells:` branch, so no
  ack is written and no `seated` line prints.
- `extensions/agi/tests/test_migrate_channel.py:175-208`
  (`test_receive_seats_once_and_writes_the_cells_through_the_one_writer`):
  flipped to `_acks(fake) == []`, `"seated p on boxB" not in out`, and the
  request record read before/after is byte-identical. The SKIP line and the
  session-cell assertions (len(cell_calls)==1, actor `p`, pid 4242, no `box`
  cell) STAY. The test was NOT deleted.

Measured production lines: `git diff --numstat -- extensions/agi/bin/rotate.py`
= `3  0` (one `continue` + two comment lines), ceiling 4.

## Evidence

Suite: `python3 -m pytest extensions/agi/tests/test_migrate_channel.py -q`
-> `30 passed, 2 warnings in 0.91s` (after; before the flip it was also 30
passed — the change flips assertions inside one test, it does not add or
remove tests).

Own probes, run from `.agi/sessions/iter-153/a00-5581b696/probe_slice6.py`
against the built bytes:

```
[probe1 gate no-grant] ok=True rc=0 acks=0 record_unchanged=True session_cell_actor=p skip=True seated_line=False
[probe2 gate control] ok=True rc=0 acks=1 stage=seated seated_line=True row_box=True worktree_in_row=True
[probe3 wire] ok=True rc=0 seating_calls=1 actor=sanctuary-master master=sanctuary-master cells=['box', 'worktree']
[probe4 auth] ok=True msg="config nodes (config:posts): a seated role may update only its OWN row and only the declared fields; field 'worktree' is prime/owner-only on a seat row; a seated role may never write it. (L4.110 prime ruling B)"
```

- probe1 (gate): no grant, seat_cells non-empty -> SKIP printed, 0 acks,
  request record byte-identical, no `seated` line, session cells still written
  by the post itself.
- probe2 (gate control): the SAME call with a valid master grant -> one ack,
  `stage == seated`, `seated p on boxB` present, row carries box+worktree.
  Proves the ack was not killed everywhere.
- probe3 (wire): the master-grant path routes the seating write through
  `_write_identity_cells` with `actor == sanctuary-master`, not `p`.
- probe4 (auth): `_write_identity_cells(seat=p, actor=p, cells={box,worktree})`
  is still refused by name; untouched by this change.

Committed bytes: the diff above is in the working tree at
`extensions/agi/bin/rotate.py` (HEAD 33e2b631f); the loop owns the commit.

## Agent Notes
SM.123 slice 6: added continue in cmd_migrate_receive's no-grant branch (rotate.py:20744), so a receive that cannot write the seating cells writes NO seated ack and leaves the request record byte-identical; flipped the committed branch test to 0 acks + untouched row. rotate.py diff 3 lines, ceiling 4. test_migrate_channel.py 30 passed; test_rotate.py 328 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW BY PARENT a00-d54a4d3b (iter 153). (1) WHAT THE INSTRUCTION SAID: SLICE 6 -- "the absent-actor_rows-grant path in cmd_migrate_receive (rotate.py ~L20727-20736) must `continue` after its SKIP print -- a receive that could not write the seating cells writes NO seated ack and leaves the request record as it was; the committed test that asserts len(acks)==1 in that branch is flipped to assert 0 acks and an untouched row. CEILING: <=4 production lines." (2) WHAT THE MACHINE ACTUALLY DOES: I read the kid diff in commit 129ca926d -- rotate.py +3 lines at L20740-20744 (2 comment + `continue`), and test_migrate_channel.py:199-204 flipped to `_acks(fake) == []`, `"seated p on boxB" not in out`, `path.read_text() == text`. I ran my own probes against the COMMITTED tree (probe_slice6.py, scratch): A gate/no-grant -> rc 0, 0 acks, SKIP printed, request byte-identical, no seated line; B control/grant-present -> 1 ack stage=seated, seating write actor=sanctuary-master, "seated p on boxB" printed; C control/no seating cells -> 1 ack, not gated; D auth -> EditError "may update only its OWN row ... field box". 30 passed in test_migrate_channel.py, 328 passed in test_rotate.py on the same committed bytes. (3) THE NEAR MISS: a `continue` placed BEFORE the session-cell write would satisfy the words "no ack" and lose the mechanism -- the session cells (window/pid/session_id/session_name) are the post own self_row authority (L4.110 ruling B) and must still land; the kid placed it after the session write and my probe B/C confirm the happy paths keep acking, so the gate is not a global ack kill. (4) NO DEVIATION from a standing rule. ACCEPTED, no demotion.
<!-- THOUGHT:END -->

Parent review a00-d54a4d3b iter 153: ACCEPTED proved. Diff bytes match the SLICE 6 order exactly (rotate.py +3 at L20740-20744; test flipped at L199-204). 4 parent probes on the committed tree: no-grant -> 0 acks + request untouched; grant -> 1 ack + master actor; no-seating-cells -> 1 ack; post self-seat -> refused by name. Suite: test_migrate_channel.py 30 passed, test_rotate.py 328 passed.
