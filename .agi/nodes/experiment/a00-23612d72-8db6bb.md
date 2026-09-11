---
id: experiment:a00-23612d72-8db6bb
mint_id: 28be56257af74b01bc4974a4819bfcdc
type: experiment
parents:
  - hypothesis:l4-a-failed-ack-commit-exits-non-zero-and-unstages-and-three-tests-assert-what-they-claim
next_edges: []
confidence: 0.9
edited_by: a00-cd127adb
evidence_runs:
  - experiment:a00-23612d72-8db6bb
loop: hypothesis:l4-a-failed-ack-commit-exits-non-zero-and-unstages-and-three-tests-assert-what-they-claim@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7b82f060552168f4
season: 2
title: A00 23612d72 8db6bb
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-23612d72-8db6bb

## Experiment

P2 TEST-INTEGRITY round on the FAILED-ACK subtree (parent hypothesis). The
P1 kid already fixed rotate.py's `_ack_commit_seats` and added its two tests
(DO NOT touch rotate.py / test_rotate.py). This kid owned the THREE P2 items,
both entirely inside `extensions/agi/tests/test_send.py` and
`test_sensei_rotate_out_audit.py` -- no source file changed.

### P2a -- restored the lost assert (test_send.py `test_wake_no_target_outcome`)
Row built `calls = _fake_tmux_pane(...)` and never used it -- the
`assert not any(c[:2] == ["tmux","send-keys"] ...)` had been displaced by the
SL3.07 rearrangement. Re-added it under the test (grep confirmed no stray
displaced copy sat at the tail of a neighbour elsewhere): a no-target wake now
proves both `no-target` outcome AND zero typing.

### P2b -- new test for the `(no rendered box)` COALESCE path
`test_dm_coalesces_no_rendered_box_and_defers_the_body`: `send_dm` to a seat
whose `_fake_tmux` capture is NON-BLANK, box-less (`\u276f` absent), footer-less
(`esc to interrupt` absent) asserts ZERO `tmux send-keys`, stderr contains
`nudge: coalesced (no rendered box)`, and the body is DEFERRED
(`_read_deferred(project/.agi, seat) == {"sender":..., "body":...}`).
Hermetic: `_registry_status` forced to None, so the capture fake decides.

### P2c -- the busy fixture no longer discards the stranded token
`_FixturePane.capture()` with `busy=True` returned the static
`claude_pane_busy.txt` and threw `self.input` away. Now the busy capture keeps
the fixture's constant leader/separator/footer but renders the typed `self.input`
(wide-wrapped, same as the idle path) as the box body -- with an EMPTY input it
is byte-for-byte the committed fixture (so the three busy tests with no typed
line stay identical). `test_stranded_token_in_a_busy_pane_gets_no_enter` now
ASSERTS `_nudge_token_head(_OLD_TOKEN)` is in the capture AND that busy still
wins (no send-keys). (send.py checks `esc to interrupt` in the region BEFORE
stranding, so the busy branch still fires with a stranded line in the box.)

### P2d -- the registry default no longer reads $HOME
`test_rotate_out_registry_dir_is_honoured`'s first call passed `registry_dir=None`,
which stats the REAL `~/.claude/sessions/999999.json`. Routed the "default dir
does not see the fixture file" half through a fixture: `monkeypatch.setattr(rotate,
"REGISTRY_DEFAULT_DIR", str(tmp_path / "not-the-registry"))`, so the first call
is hermetic AND still asserts the fixture `reg` file is invisible under the
default. Second call (`registry_dir=str(reg)`) unchanged.

## Evidence

`python3 -m pytest extensions/agi/tests/test_send.py
extensions/agi/tests/test_sensei_rotate_out_audit.py -q`
-> **226 passed in 2.98s** (whole two-file run, green on the changed bytes).

Focused re-run of the touched/named tests
(`-k "stranded_token_in_a_busy_pane_gets_no_enter or wake_busy or
wake_verb_busy or dm_coalesces_no_rendered_box or wake_no_target or
busy_logs_deferred"`) -> **6 passed**.

## Agent Notes
P2 test-integrity: restored no-target send-keys assert, added (no rendered box) COALESCE test, busy fixture now holds the stranded token, registry default routed off $HOME -- 226 tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (SL5.08 a00-cd127adb, P2 kid). Read the diffs. P2a: the lost send-keys assert is restored UNDER test_wake_no_target_outcome with the `calls` it already built. P2b: new test_dm_coalesces_no_rendered_box_and_defers_the_body asserts zero send-keys, the `coalesced (no rendered box)` stderr line, and `_read_deferred` carrying the body. P2c: _FixturePane busy capture now renders self.input into the box (empty input still byte-identical to claude_pane_busy.txt) and test_stranded_token_in_a_busy_pane_gets_no_enter asserts the token head is IN the capture and busy still wins. P2d: REGISTRY_DEFAULT_DIR monkeypatched to a tmp path so the default-dir half no longer stats $HOME. No source file touched. Independently ran test_send.py + test_sensei_rotate_out_audit.py + test_rotate.py -> 374 passed. Accepted proved.
<!-- THOUGHT:END -->

P2 reviewed + accepted: no-target assert restored, no-rendered-box coalesce test added, busy fixture now retains the stranded token, registry default off $HOME; 374 passed across the three files.
