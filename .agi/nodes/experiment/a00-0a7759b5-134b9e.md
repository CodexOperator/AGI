---
id: experiment:a00-0a7759b5-134b9e
mint_id: b2b5fdc66fc941a7a607ca19c2e44e5a
type: experiment
parents:
  - hypothesis:l4-the-service-after-join-dm-is-sent-by-a-declared-signed-sender-never-from-unknown
next_edges: []
confidence: 0.9
edited_by: a00-30eb3c0e
evidence_runs:
  - experiment:a00-0a7759b5-134b9e
loop: hypothesis:l4-the-service-after-join-dm-is-sent-by-a-declared-signed-sender-never-from-unknown@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: dbd38cd6ab034f6c
season: 2
title: A00 0a7759b5 134b9e
town: core
verdict: proved
---
# experiment:a00-0a7759b5-134b9e

## Experiment

g15.25 FIX-ONLY build. Measured defect: `run_after_join`'s default `send_dm`
closure called `_send.send(root, to, text, None)` — sender None → `send.py`
`_detect_sender(None)` returns `'unknown'` when no `AGI_AGENT_ID`/`AGI_SEAT`
env is exported, and `_sign_line` can never sign 'unknown' (no
`<sessions>/seats/unknown.key`). So a service dm could arrive `from: unknown`,
unsigned, under enforcing comms.verify.

Implemented in `extensions/agi/bin/rotate.py`:
1. ONE helper `_after_join_sender(root, seat)` — returns the custodian/outgoing
   seat when `<sessions>/seats/<seat>.key` exists (the rotate-self tail, whose
   key exists → SIGNED), else the system sender `heal` (the watch/reaper). It
   never returns `'unknown'`. Deterministic from (root, seat) alone, so the
   watch and the tail resolve the SAME sender for the same seat (the
   falsifier's no-divergent-sender clause). Both callers funnel through the one
   `run_after_join`, so there is ONE resolution, no parallel driver.
2. The default `send_dm` now passes that named sender: `_send.send(root, to,
   text, sender)` — never None → `'unknown'` can no longer appear.
3. The rotation record's `after_join` key now carries `dm_sender` and
   `dm_signed: true|false` (key-existence gate mirroring send.py's signing).

Four new tests in `extensions/agi/tests/test_after_join_service.py`
(unkeyed → heal, unsigned-but-named; keyed custodian seat → seat, signed; the
helper resolves deterministically; dry-run resolves sender but never sends/saves).

## Evidence

`python3 -m pytest extensions/agi/tests/test_after_join_service.py -q` → 21 passed
(incl. 4 new). `python3 -m pytest extensions/agi/tests/test_after_join_service.py
extensions/agi/tests/test_send.py -q` → 311 passed. send.py was NOT changed
(the verify path already wins because the sender is now a real named seat; a
`heal`-sent dm is unsigned-but-named, and heal is an established system sender
in heal.py's own alarms). Falsifiers checked: no path yields `'unknown'`; a
keyed custodian signs with its own minted key (whose pubkey is on its pushed
row); a divergent watch/tail sender is structurally impossible (one helper);
no dm is reported signed when no key exists.

## Agent Notes
after_join dm now sent by _after_join_sender: the custodian seat when its key exists else heal; never 'unknown'; record carries dm_sender+dm_signed; 4 new tests, 311 pass

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-30eb3c0e, SL7.75): accepted as proved with evidence_runs=self. WHAT THE INSTRUCTION SAID: the target is a g15.25 FIX-ONLY node — "a g15 claim is a build order, not a measurement": the service after_join dm must name a declared, signed-when-keyed sender, never from: unknown. WHAT THE MACHINE ACTUALLY DOES — measured, not read: rotate.py:9618 _after_join_sender resolves the custodian seat iff <sessions>/seats/<seat>.key exists, else heal; the default closure at rotate.py:9760 now passes that name to send.send, never None. I ran the two suites: 311 passed. Both callers reach it through one run_after_join (heal.py:453 -> run_after_join_for_seat -> rotate.py:9899; tail at rotate.py:13127 with no send_dm override), so the watch/tail divergence falsifier is structurally closed. send.py needed no change: I read the label path (_verify_block, send.py:2712-2790; enforcing at send.py:2947-2951 refuses ONLY the exact FORGED label) — a heal dm with no sig reads UNSIGNED, admitted and named, so from: unknown cannot appear on a service dm. THE NEAR MISS: a fragment that injects send_dm=<seat> only on the rotate-self tail would satisfy clause (a) and lose clause (c) — the watch would still call send(root,to,text,None); deferring resolution to key-existence in ONE helper is what makes both paths agree. DEVIATION: none from the hypothesis; heal is left unsigned-but-named because keygen for seats is EXCLUDED and the verify path already admits UNSIGNED.
<!-- THOUGHT:END -->

parent review SL7.75: proved upheld. Fix implemented in rotate.py (_after_join_sender + named default closure + dm_sender/dm_signed record fields), 4 new tests in test_after_join_service.py, 311 pass. Falsifiers checked against source: no unknown; keyed custodian signs; watch and tail share one resolution; enforcing refuses only FORGED so a named unsigned heal dm is admitted.
