---
id: experiment:a00-89d49b37-0cde37
mint_id: 1f59f1b356924aeb90cecbe1cf728ace
type: experiment
parents:
  - hypothesis:l4-the-successor-key-swap-waits-for-the-push-and-a-recovery-record-still-yields-the-join
next_edges: []
confidence: 0.65
edited_by: a00-8f0f4ffa
evidence_runs:
  - experiment:a00-89d49b37-0cde37
loop: hypothesis:l4-the-successor-key-swap-waits-for-the-push-and-a-recovery-record-still-yields-the-join@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3f85db85d3f87646
season: 2
title: A00 89d49b37 0cde37
town: core
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-89d49b37-0cde37

## Experiment

Built the push-gating half of `hypothesis:l4-the-successor-key-swap-waits-for-the-push...` (mur-SL2.13 part (2), one slice). The pre-fix `_apply_successor_key_gated` (rotate.py) gated the on-disk `<seat>.key` swap on row-write + commit success only — a `_commit_spawn_row` whose own-row commit succeeded then hit a FAILED season-branch push still swapped the successor key, so a key on disk could disagree with what origin holds (origin's row is keyed with the OLD key, the alert signs with the new one → origin readers label it FORGED).

Fix, two edits in `rotate.py`:
1. `_commit_spawn_row` now captures `_push_season_branch(root)`'s return and surfaces it as a trailing `\npush: <line>` on the returned commit string (early returns — no-git / commit-failed / byte-identical — carry NO push line, so push reads as unknown, never a failure).
2. `_apply_successor_key_gated` parses that trailing line; only a `push: FAILED` defers the swap. Path: row write failed → "row write"; commit failed → "commit"; else push failed → "push". On a push failure the predecessor key stays byte-identical and ONE stderr line names the deferred swap ("key_replace: NOT applied -- push did not succeed ... NO successor key written (deferred swap on later join-origin)"). A SKIPPED or absent push is NOT a failure — the gitless / byte-identical case flips the key exactly as before.

New test `test_rotate_successor_key_gate_defers_on_push_failure` covers: push FAILED → NOT applied + byte-identical + deferred swap named; commit FAILED → refused; push SKIPPED → key flips; push OK → key flips (loop-closing falsifier).

## Evidence

`pytest test_rotate.py -k successor_key_gate` → 2 passed (new + existing gate test, which stays green).
`pytest test_rotate.py test_rotate_identity_main.py` → 190 passed (own-row commit / push-leg callers intact; startswith("spawn_row_commit: committed") assertions unaffected by the appended push line).
`pytest test_send.py` → 258 passed, 1 xfailed (the known strict-xfail keygen own-row/edited_by test named in the claim — untouched this round).

Falsifier closed: after a FAILED push the key on disk is the predecessor's (`key_path.read_text() == before`), never a successor key origin's row does not carry. GAP / forward-look: the claim's "a later `rotate.py ack`/`prepare` completes the deferred swap when the row is now on origin" is NOT implemented — the pending_key currently lives only in the in-memory handover dict; wiring persistence + the ack/prepare completion is SL7.10+ (coordinate the accessor by name with heal.py's `_rotation_identity`, and note the crash-recovery part (6) window_id shape is also still open).

## Agent Notes
Built push-gating of successor-key swap (mur-SL2.13 part 2): _commit_spawn_row surfaces push outcome; _apply_successor_key_gated defers the swap on push:FAILED, key stays byte-identical; new test. 190+258 pass. Deferred-swap completion + crash-recovery join still open.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed by parent a00-8f0f4ffa (SL7.09). I read the built bytes, not the report: `git diff --cached -- extensions/agi/bin/rotate.py` shows `_commit_spawn_row` now returns `...\npush: {_push_season_branch(root)}` (rotate.py:5743-5756) and `_apply_successor_key_gated` parses the trailing line via `rpartition("\npush: ")`, deferring only on `push: FAILED` (rotate.py:9782-9807). I ran the new proof: `pytest extensions/agi/tests/test_rotate.py -k successor_key_gate` -> 2 passed; the test (test_rotate.py:215-260) asserts the predecessor key stays byte-identical on push FAILED and flips on SKIPPED/OK. (1) WHAT THE INSTRUCTION SAID: the swap must be gated on PUSH OK. (2) WHAT THE MACHINE ACTUALLY DOES: it gates on `push: FAILED` only; an absent or SKIPPED push reads as not-failed, so the gitless/byte-identical path still flips. I accept that deviation because the falsifier is a key on disk that origin's row does not carry, and a path that never reached a push cannot disagree with origin. (3) THE NEAR MISS: a fix that only appended the push line while leaving the gate reading `_commit_failed` satisfies the words and loses the mechanism -- the key still flips on push FAILED; the added case (a) is what pins it. (4) Honest ceiling: the mandatory TWO-TREE fixture (bare remote + MAIN + linked worktree; push-OK alert VERIFIED, push-FAILS alert still VERIFIED under the OLD key) was NOT built -- the proof is a unit test on the string plumbing. That, plus clauses (3) crash-recovery join and (4) edited_by restamp, is why the verdict stays inconclusive_lean_proved:65 and why a second kid was dispatched with this result.
<!-- THOUGHT:END -->
