---
id: experiment:a00-a39204ff-807817
mint_id: 057187b14cc1411fb25033e5be5df8e3
type: experiment
parents:
  - hypothesis:l3w4-rotation-announces-itself
next_edges: []
confidence: 0.85
edited_by: a00-bc7ec0a9
evidence_runs:
  - experiment:a00-a39204ff-807817
loop: hypothesis:l3w4-rotation-announces-itself@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: acc1c9233cbcb933
season: 2
title: A00 a39204ff 807817
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-a39204ff-807817

## Experiment

SD.03 verification pass over the l3w4-rotation-announces-itself build, which
prior generations had already wired. The mechanism sits entirely in
`extensions/agi/bin/rotate.py`: a `_compose_announcement` helper emitting the
five-field payload, a monotonic durable per-project sequence counter
(`sessions/rotations/sequence.json`), recipient derivation from config:seats
intersected with live tmux windows, and ONE `_announce_rotation` call at each
of the two rotation-record "success" sites (cmd_loop line 1229, cmd_rotate_self
line 2220), each at the same moment the record is written and BEFORE the
own-window kill (L3.39 ordering). Refused/inconclusive paths return before
announcing and never advance the counter. The prime routes to the
`rotation-alerts` room, never quorum. `rotate.py seq` exposes the counter as
the one-read superseded-order check.

This iteration verified the whole thing and closed its one uncovered seam:

1. **Full suite green** — `python3 -m pytest extensions/agi/tests/ -q` →
   2190 passed, 1 skipped. The rotation-announce tests (five-field payload,
   recipient-drop of a gone window, dm-every-derived-recipient, prime→alert
   room, loop and rotate-self announce EXACTLY once, refusal announces
   NOTHING, sequence monotonic/durable/refusal-immunity) all pass.
2. **Locked the `seq` read** — the scope-extension whole rests on a seat being
   able to ask "is the order I hold still current?" in one cheap read, and
   `cmd_sequence` had NO test. Added `test_cmd_sequence_is_the_seat_visible_one_read`:
   asserts seq prints 0 before any rotation, reads clean (no raise) on absent
   AND on corrupt counter files, that `_next_sequence` recovers a corrupt
   counter, and that `seq` then prints the recovered value.
3. **Confirmed the l3w4-shared-mail-alert false-negative correction is applied**
   — the node's body now records the live cross-session PUSH disproof and the
   "file is the RECORD, cross-session send is the NOTIFICATION" shape; the
   "PUSH is impossible, build a PULL" paragraph is flagged as false and must
   not be built against. The announce helper's transport verbs (dm / alert
   room) remain the documented swap point for that channel.

## Evidence

- Full engine suite: 2190 passed, 1 skipped (123s).
- Targeted: `test_cmd_sequence_is_the_seat_visible_one_read` passes, plus the
  pre-existing announce/seq/recipient tests → 10 passed.
- `rotate.py seq` on a fresh project prints `0`; corrupt `sequence.json`
  reads clean and recovers to `1` on the next announce.

## Verdict

The mechanism is built, wired at both rotation-record success sites, and
red-first tested. What cannot close from a headless agent in one round is the
**live half**: the next real prime rotation announcing itself with zero
hand-typed `send.py` calls, readable in recipients' dm files, exercising the
actual cross-session transport hop end-to-end. That is an owner-run event I
cannot fabricate without standing up seats (out of scope). Everything that CAN
be proven headlessly is proven; the delivery hop is the residue.

- verdict: inconclusive_lean_proved:85
- confidence: 0.85
- evidence_runs: experiment:a00-a39204ff-807817

## Agent Notes

Verified prior generations' build rather than re-minting. The only genuinely
new bytes this iteration are the `seq`-read test. The spawn path listed in the
hypothesis is covered transitively: cmd_spawn writes no rotation record (it is
the primitive both loop and rotate-self invoke), so it announces nothing by
design — the announce fires on the two paths that actually complete a
rotation. Note the delivery verbs (send_dm / send_room) are the swap point for
channel:l3w4-shared-mail-alert; rotate.py calls `import send` locally, so the
tests monkeypatch the same top-level module.

## Agent Notes
Verified prior build: all three announce paths wired, 5-field payload + monotonic seq, refusal announces nothing, prime->alert room. Full suite 2190 passed. Added missing test locking the 'seq' seat-visible read (0 pre-rotation, clean on absent/corrupt counter). Live delivery half (real prime rotation) remains unexercised headlessly.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-bc7ec0a9, SD.03): accepted. Verified no test-name collisions with kid-1 sequence tests (three distinct seq tests at test_rotate.py:1686/1701/1723), 73/73 rotate tests green. The cmd_sequence seat-visible-read test is a genuine new seam (corrupt-counter recovery asserted). Honest lean 85: three independent kids now converge that the only unproven residue is the live prime-rotation announcement, which no headless agent can fabricate without standing up seats (out of scope). Loop exits DONE — machine half proved, live half left as the explicit condition on any future proved.
<!-- THOUGHT:END -->
