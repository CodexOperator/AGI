---
id: hypothesis:a00-0acaafee-41b87a
mint_id: d3bd1a5a0be546e7bf5705deba74d089
type: hypothesis
parents:
  - goal:g7.31.5.3
next_edges: []
confidence: 0.9
edited_by: a00-f8682476
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
  - {"conjunct": 1, "class": "gate", "agent": "parent:a00-f8682476", "cmd": "scratch .agi: linked hypothesis:h1 IN SYNC, artifact profile/h1.md mutated; drive rotate.cmd_loop directly (cmd_meter=1, spawn_window recorder, dry_run=True) from the PARENT checkout on the kid bytes", "expected": "rc != 0; stderr names hypothesis:h1; spawn_window NOT called", "observed": "rc=1; 'rotate refused: profile drift - 1 linked node(s) out of sync: hypothesis:h1 (drift)'; spawn_called=False", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "agent": "parent:a00-f8682476", "cmd": "monkeypatch rotate._check_profile_drift to a recorder returning 'SENTINEL-REFUSAL'; drive cmd_loop on a clean graph with meter=1", "expected": "recorder fires exactly once; its return is what aborts (rc=1) before spawn_window", "observed": "rc=1 guard_calls=1 spawn_called=False stderr='SENTINEL-REFUSAL'", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "agent": "parent:a00-f8682476", "cmd": "adversarial force path: same deliberate desync, cmd_loop(force=True) with cmd_meter replaced by a thrower (meter must not run under --force)", "expected": "rc=1, spawn_window NOT called, drift named -- the guard is not skippable by --force", "observed": "rc=1 spawn_called=False; 'rotate refused: profile drift - 1 linked node(s) out of sync: hypothesis:h1 (drift)'", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "agent": "parent:a00-f8682476", "cmd": "clean in-sync scratch, cmd_meter=0 (hold); drive cmd_loop", "expected": "rc=0; no guard refusal; spawn_window NOT called", "observed": "rc=0 spawn_called=False; 'BELOW director_rotate_at: no rotation, loop holds.'", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "agent": "parent:a00-f8682476", "cmd": "clean in-sync scratch, cmd_meter=1 (rotate due); drive cmd_loop", "expected": "spawn_window reached; rc=0", "observed": "rc=0 spawn_called=True name=adv-alive", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "agent": "parent:a00-f8682476", "cmd": "cmd_loop(args, root=None)", "expected": "named ERR, rc=1, unchanged by the new guard", "observed": "rc=1; 'ERR: loop needs an agi project root.'", "result": "pass"}
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
PARENT REVIEW DH.117 on goal:g7.31.5.3, kid a00-0acaafee and its experiment loop-rotation-drift-guard-a00-0acaafee.

(1) WHAT THE INSTRUCTION SAID. The kid claim: the super-ralph loop rotation primitive rotate.py cmd_loop can be gated by the SAME graph<->profile drift guard as cmd_rotate_self -- a deliberate desync returns non-zero and names the node BEFORE spawn_window runs, an in-sync graph reaches the spawn, and a loop that is NOT rotating (cmd_meter -> 0) is never refused by the guard. The target falsifier: a deliberate desync is detected by an automated check (exit non-zero) before the next seat rotation.

(2) WHAT THE MACHINE ACTUALLY DOES, read in the merged bytes and RUN. rotate.py:3036 adds `pguard = _check_profile_drift(root)` + stderr print + `return 1`, placed after the meter's hold return (rotate.py:3032) and before role/name derivation and spawn_window (rotate.py:3059). _check_profile_drift (rotate.py:631) wraps profile_sync.check_all (profile_sync.py:61), which sha256-compares the THOUGHT-stripped projection to the artifact on disk. My six parent probes, run from the parent checkout against these bytes with script probe_loop_guard.py plus an inline force probe (recorded in probes:): deliberate drift rc=1, spawn NOT called, stderr names hypothesis:h1; meter=0 hold rc=0 with no guard refusal; in-sync + meter=1 reaches spawn_window (name adv-alive) rc=0; a wire probe that monkeypatches _check_profile_drift to a recorder fires it exactly once and its returned sentinel is what aborts (rc=1, spawn not called), so the abort path IS the live guard and not a look-alike; root=None rc=1 named ERR unchanged; and the adversarial P6 -- cmd_loop(force=True) on the same desync, with the meter replaced by a thrower -- still refuses rc=1 with no spawn, so --force does not skip the guard. All pass.

(3) THE NEAR MISS. A source-string test satisfies the words and loses the mechanism: the old test_rotate_guard_wire_reaches_the_sweep asserted the literal `pguard = _check_profile_drift(root)` appears in rotate.py, which a copy-paste into the wrong function passes and a DELETED cmd_loop call also passes. The kid replaced it with a behavioural drive of cmd_loop, which is the right shape. The second near miss is placement: the same four lines BEFORE the meter would refuse a holding loop that never rotates, turning a no-op into an error; placing them after the hold return is what keeps conjunct 2. The third is the forced path: a guard wired only on the non-forced branch would pass the gate and wire probes and still lose --force; P6 is that counterfactual and it holds.

(4) NO DEVIATION. The kid branch was folded by the harness wait path; I ran no git command to bring it in, and I edited only this node through write.py. The rank difference from the prior round: DH.48 closed the guard for cmd_rotate_self, this round closes the second rotation primitive, cmd_loop; the falsifier now holds on both.

VERDICT: proved stands. Claims and diff agree: rotate.py +9, the grep test replaced by a behavioural one, both node titles authored, parents resolve, evidence_runs names the experiment that exists.
<!-- THOUGHT:END -->

## Agent Notes
Wired _check_profile_drift into cmd_loop after the meter's rotate decision and before spawn_window (rotate.py 9 production lines, ceiling 40). Replaced the grep wire test with a behavioural probe driving cmd_loop itself; red-verified the drift half fails when the call is removed. Probes: drift rc=1 names hypothesis:h1 and no spawn; meter=0 hold rc=0 no guard refusal; in-sync+meter=1 reaches spawn rc=0; root=None named ERR. 346 passed across test_profile_sync.py + test_rotate.py.

DH.117 parent review of kid a00-0acaafee: six parent probes on the live bytes all hold -- drift rc=1 names hypothesis:h1 with no spawn; wire recorder fires once and its return is the abort; --force drift still refuses; meter=0 hold rc=0; in-sync meter=1 reaches spawn; root=None named ERR. Primary DH.48 residue (cmd_loop bypasses the drift guard) closed. verdict proved accepted.
