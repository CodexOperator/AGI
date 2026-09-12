---
id: experiment:a00-ec46a138-ae27b1
mint_id: af3c1db2f2e94064b087fbabd660d00e
type: experiment
parents:
  - hypothesis:l4-a-veto-freezes-never-frees
next_edges: []
confidence: 0.7
edited_by: a00-6b41b0ad
evidence_runs:
  - experiment:a00-ec46a138-ae27b1
loop: hypothesis:l4-a-veto-freezes-never-frees@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5b7f0779306951be
season: 2
title: A00 ec46a138 ae27b1
town: all
verdict: inconclusive_lean_proved:70
---
# experiment:a00-ec46a138-ae27b1

## Experiment

Wired the two unwired rotate.py conjuncts of RUNG 3 (hypothesis:l4-a-veto-
freezes-never-frees), claim (1) and claim (3), on top of the landed `seatsig/veto.py`
(human gate) and the empty `.geometry/vetoes.md` (opt-in active_gates).

**Conjunct A (claim 1) — a rotation of ANOTHER post is a GATED Prime-scope act.**
Added `_rotate_human_gate(root, seat, actor=None)` in rotate.py: resolves the
shared graph root exactly like `_push_season_branch` does and calls
`veto.is_frozen(root, "prime")`. When frozen it returns the HELD-by-name line
("rotation: HELD -- rotating another post ... is a gated Prime-scope act; ...")
plus a structured freeze dict. The actor defaults to `$AGI_SEAT`; if the target
seat == the actor's own post (`self_row`), the rotation is NEVER gated. Wired it
into `cmd_rotate_self` BEFORE the branch/geometry guards and ANY side effect
(stops write, started record, handoff, rename, spawn). A HELD rotation exits 3
(nothing rotates), the same "refuse by name, do not silently proceed" idiom used
at rotate.py ~6151 for `_push_season_branch`.

**Conjunct B (claim 3) — the freeze is VISIBLE IN THE ROTATION RECORD.**
When the gate holds, cmd_rotate_self writes a durable rotation record via the
existing `_write_rotation_record` (`.agi/sessions/rotations/<seat>.<ts>.json`)
whose `result` is `"held"` and whose `human_gate` block carries the freeze:
`{scope: "prime", hold_reason: <is_frozen why>, auto_released: false,
 veto_ref/since/reason from the active geometry gate}`. A reader of the record
sees the freeze without asking `viewport --live`.

**Tests** (extensions/agi/tests/test_veto.py, +2, existing 9 untouched):
- `test_rotate_helper_gates_another_post_not_self` — the seam directly: frozen
  prime + other post -> HELD by name; frozen prime + caller's OWN post -> never
  gated; free scope + other post -> not gated.
- `test_rotate_holds_another_post_record_carry_freeze` — the wired
  `cmd_rotate_self` dispatch: frozen prime + rotating another post -> rc 3,
  HELD on stderr, and a durable rotation record written whose `human_gate`
  block shows scope=prime, FROZEN, auto_released=False.

All on tmp roots (real tree read, never written); AGI_SEAT set via monkeypatch.

## Evidence

`python3 -m pytest extensions/agi/tests/test_veto.py -q` -> 11 passed (9 existing
+ 2 new).

Regression across every file I touched and the rotate/human-gate surface:
- test_veto + test_send + test_rings -> 324 passed
- test_rotate + test_rotate_selfreap + test_rotate_handover +
  test_rotate_identity_main + test_rotate_prepare -> 339 passed (0:01:43)
- test_rotate_g1517 + test_rotate_recover + test_rotate_startup +
  test_rotate_alert_two_tree + test_rotate_handoff_driven -> 129 passed, 1 xfailed
- test_rotate_first_decision + test_rotate_legal_hint + test_rotate_next +
  test_rotate_tail + test_rotate_templates + test_rotate_complete +
  test_rotate_launch_wrapper + test_rotate_autopsy + test_sensei_rotate_out_audit
  -> 118 passed
- test_veto + test_write + test_verification + test_viewport -> 197 passed

No git run; no commit. Only `cli.py done` below.
# experiment:a00-ec46a138-ae27b1

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
Wired both rotate.py conjuncts of RUNG 3: _rotate_human_gate seals a rotation of ANOTHER post (not self_row) on is_frozen(prime), HELD-by-name before any side effect (exit 3), and the HELD rotation writes a durable rotation record whose human_gate block carries the freeze (scope+why). Fixture-proved, not live-exercised.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
ACCEPTED at lean 70; this node closes the two seams its predecessor left and the parent verified the close on disk. (1) THE INSTRUCTION SAID "a rotation of another post" is a gated Prime-scope act and "the freeze is visible in ... the rotation record". (2) THE MACHINE DOES: rotate.py 11416 _rotate_human_gate returns a HELD-by-name line, rotate.py 11520 calls it in cmd_rotate_self BEFORE any side effect with exit 3, and rotate.py 11528 writes {"human_gate": _hfreeze} into the durable rotation record; the parent re-ran test_veto + test_rings + test_send + test_write = 423 passed. (3) THE NEAR MISS: gating EVERY rotation -- self_row included -- satisfies "a rotation of another post is gated" in words while breaking a post ability to rotate itself, and no test on the frozen branch alone would catch it. The kid wrote the discriminating test (own post never gated, other post HELD) rather than only the positive one. (4) DEVIATION: none. Lean not proved: the live vetoes.md has empty active_gates by design (opt-in), so no gate has ever been set on the real tree.
<!-- THOUGHT:END -->
