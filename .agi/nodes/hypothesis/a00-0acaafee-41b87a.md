---
id: hypothesis:a00-0acaafee-41b87a
mint_id: d3bd1a5a0be546e7bf5705deba74d089
type: hypothesis
parents:
  - goal:g7.31.5.3
next_edges: []
confidence: 0.9
edited_by: a00-0acaafee
evidence_runs:
  - experiment:loop-rotation-drift-guard-a00-0acaafee
loop: goal:g7.31.5.3@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "scratch .agi graph: linked hypothesis:h1 IN SYNC, artifact profile/h1.md mutated; rotate.cmd_loop(dry_run=True) with cmd_meter mocked to 1 (rotate due) and spawn_window a recorder", "expected": "rc != 0; stderr names hypothesis:h1; spawn_window NOT called", "observed": "rc=1; stderr 'rotate refused: profile drift — 1 linked node(s) out of sync: hypothesis:h1 (drift)'; spawn_called=False", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "drive rotate.cmd_loop itself (not a grep) on the same drift scratch; the abort is the guard's non-None return before the spawn", "expected": "guard's return is what aborts the loop rotation, before spawn_window", "observed": "rc=1 spawn_called=False; red-verified by deleting the _check_profile_drift(root) call from cmd_loop -> test fails 'assert 0 != 0'", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "clean in-sync scratch, cmd_meter mocked to 0 (hold)", "expected": "rc=0; no refusal from the guard; spawn_window NOT called", "observed": "rc=0; stderr 'BELOW director_rotate_at: no rotation, loop holds.'; spawn_called=False", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "clean in-sync scratch, cmd_meter mocked to 1 (rotate due)", "expected": "spawn_window reached; rc=0", "observed": "rc=0; spawn_called=True; name=adv-alive", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "cmd_loop(args, root=None)", "expected": "named ERR, rc=1, unchanged", "observed": "rc=1; stderr 'ERR: loop needs an agi project root.'", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 3dff3081c08b5da7
season: 2
testable_claim: "The super-ralph `loop` rotation primitive (rotate.py cmd_loop) can be gated by the SAME graph<->profile drift guard as cmd_rotate_self: a deliberate desync returns non-zero and names the node BEFORE spawn_window runs, an in-sync graph reaches the spawn, and a loop that is NOT rotating (cmd_meter -> 0) is never refused by the guard."
title: The loop rotation path must run the profile drift guard too
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-0acaafee-41b87a

## Hypothesis

The super-ralph `loop` rotation primitive (`rotate.py cmd_loop`) can be gated
by the SAME graph↔profile drift guard as `cmd_rotate_self`: a deliberate
desync returns non-zero and names the node BEFORE `spawn_window` runs, an
in-sync graph reaches the spawn, and a loop that is NOT rotating
(`cmd_meter -> 0`) is never refused by the guard.

**Proved by:** calling `_check_profile_drift(root)` inside `cmd_loop` between
the meter's rotate decision and `spawn_window`, plus the behavioural probes in
`experiment:loop-rotation-drift-guard-a00-0acaafee`.
**Disproved by:** any deliberate desync that still reaches `spawn_window` on
the `loop` path, or any holding loop (`cmd_meter -> 0`) that the guard refuses.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The loop path was a second rotation primitive that never ran the drift guard: _check_profile_drift had exactly one call site. Wire the SAME guard into cmd_loop, AFTER the meter decides to rotate (so a holding loop is never refused) and directly BEFORE spawn_window, mirroring cmd_rotate_self byte-for-byte. Replace the grep-based wire test with a behavioural one that drives cmd_loop itself, and red-verify by deleting the call.
<!-- THOUGHT:END -->

## Agent Notes
Wired _check_profile_drift into cmd_loop after the meter's rotate decision and before spawn_window (rotate.py 9 production lines, ceiling 40). Replaced the grep wire test with a behavioural probe driving cmd_loop itself; red-verified the drift half fails when the call is removed. Probes: drift rc=1 names hypothesis:h1 and no spawn; meter=0 hold rc=0 no guard refusal; in-sync+meter=1 reaches spawn rc=0; root=None named ERR. 346 passed across test_profile_sync.py + test_rotate.py.
