---
id: experiment:a00-b0d48a51-3caf46
mint_id: 8cac46d001874c4dae23b58ab038618e
type: experiment
parents:
  - hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-successor-one
next_edges: []
confidence: 0.8
edited_by: a00-ac50ece0
evidence_runs:
  - experiment:a00-b0d48a51-3caf46
loop: hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-successor-one@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 73c193a52e5a777e
season: 2
title: A00 b0d48a51 3caf46
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-b0d48a51-3caf46

## Experiment

Mechanism 1 of hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-
the-successor-one: the [rotation-alert] dm carries the successor's post-join
address `name [ref] @window`, and a pre-join alert NAMES that it is pre-join.

Built in extensions/agi/bin/rotate.py (announce composition only; send.py
untouched, as the hypothesis's file scope requires):

1. New `_successor_address(name, ref, window)` helper: returns `name [ref]`
   and, when a tmux `@<N>` is actually known, ` @window`. With NO ref (the
   ListAgents `@id` is exactly the join fact that has not resolved) it returns
   `name @window? (pre-join: successor ref not yet resolved)` — the alert
   names the missing identity instead of silently dropping it.
2. `_compose_announcement` gains `successor_ref=""` / `successor_window=""`
   and substitutes the composed address for the bare successor name.
3. `_announce_rotation` gains the same two kwargs and forwards them.
4. cmd_loop (~1574) — the post-ACK announce now passes
   `successor_ref=ack.get("session_ref")` (the successor acked its OWN ref
   back via cmd_ack r3, and a diff/continue ack is a joined successor, so this
   is post-join by construction) and `successor_window=_successor_window_id(...)`
   (window-path test seam, never tmux under test).
5. cmd_rotate_self (~5890) — the post-JOIN announce passes
   `successor_ref=succ_session_id` and `successor_window=succ_window_id`, both
   already resolved by the s4 JOIN (or the internal seam). No ref -> the alert
   names pre-join.

5 tests appended to extensions/agi/tests/test_rotate.py:

- test_compose_announcement_carries_successor_address_after_join: full
  `belam-II -> belam-III [f52a4c] @9 |` after a fixture ref+window.
- test_compose_announcement_pre_join_names_identity_unresolved: bare name with
  no ref gives `belam-III (pre-join: successor ref not yet resolved)` and never
  a fake bracket.
- test_compose_announcement_pre_join_when_ref_absent_even_with_window
  (parametrized "", "41"): a window @id alone still means pre-join and says so.
- test_announce_rotation_dms_post_join_address: the address flows THROUGH
  _announce_rotation into every recipient dm (monkeypatched send_dm).

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate.py -q` -> 122 passed
  (117 baseline + 5 new).
- `python3 -m pytest extensions/agi/tests/test_rotate_startup.py
  extensions/agi/tests/test_rotate_templates.py extensions/agi/tests/test_send.py -q`
  -> 212 passed.
- 334 total green; the four neighbour files stay green. mechanism 2 (ack
  back-fill, landed by kid 1) is unchanged and re-proven in the 117.

## Agent Notes
Mechanism 1: rotation-alert now composes post-join successor address 'name [ref] @window' (cmd_loop reads ref from the ack; cmd_rotate_self from the JOIN), pre-join alert names it. 5 red-first tests added; 122+212 pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
the parent reviewed mechanism 1 of hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-successor-one. WHAT THE INSTRUCTION SAID: the [rotation-alert] dm carries name [ref] @window of the successor once the join has them (composed AFTER the join; a pre-join alert names that it is pre-join). WHAT THE MACHINE DOES (read from the diff, extensions/agi/bin/rotate.py): _successor_address(name, ref, window) emits the bracket-free pre-join sentence when ref is empty and name [ref] [@window] otherwise; _compose_announcement and _announce_rotation gained successor_ref/successor_window; cmd_loop L1582 passes ack session_ref and _successor_window_id, cmd_rotate_self L5935 passes succ_session_id/succ_window_id already resolved by the s4 JOIN. THE NEAR MISS, and it is live: cmd_loop reads the ref from the ACK FILE, but cmd_ack (kid 1, same round) writes ack session_ref as EMPTY when the successor passed no --ref — the zero-call path — while back-filling only the ROW. So on the common path the post-join announce composes the pre-join sentence although the join HAS resolved the identity: the alert lies, which is this hypothesis falsifier 1. Escalated to kid 3 as an explicit correction (ack dict must carry ref or self_sid; the existing test pinning ack session_ref == "" is changed). Verdict kept at inconclusive_lean_proved:80 rather than raised, because the mechanism is not complete until that seam is closed.
<!-- THOUGHT:END -->
