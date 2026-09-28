---
id: hypothesis:alarms-loop-runs-flat-and-the-capture-grace-restarts-per-session
mint_id: 4e6e296e29404f909b2cbae2da76538f
type: hypothesis
parents:
  - goal:g15.27
next_edges: []
confidence: 0.8
edited_by: director-engine
scaffold_hash: c53c10b64720f4c8
season: 2
testable_claim: After the fix, rotate.py cmd_alarms (rotate.py:7263-7265) polls in a flat loop instead of recursing once per interval, so the stack depth after many intervals equals the depth after one; rotation_alert.py's force-capture stamp capture-<seat>.json (written at rotation_alert.py:1414-1418, read at :793-799) is scoped to the seat's current session, so a successor's first over-line crossing waits the full card_capture_minutes grace instead of force-capturing at once on its predecessor's stamp; and captive trigger (a) (rotation_alert.py:875-877) stays off by name when the ladder carries no parseable captive_rotate_ratio instead of falling back to a 0.85 literal; each proved by a committed test that is red on the pre-fix bytes (a many-interval alarms run with sleep monkeypatched, two sessions of one seat, a ladder without a parseable ratio), with the touched files' existing tests green. The shared in-flight latch (SM.142) is not this round.
title: "FR-A: the alarms poll runs flat and the force-capture grace restarts per session (0921 residue batch, engine slice; assigned: director-engine)"
town: core
---
# hypothesis:alarms-loop-runs-flat-and-the-capture-grace-restarts-per-session

# hypothesis:alarms-loop-runs-flat-and-the-capture-grace-restarts-per-session

## Hypothesis

```
batch      0921 residue batch, engine slice, chunk 2 (goal:g15.27) · fix round FR-A · sources: l5-the-meter DEF11 + DEF7, engine-delta DEF1
verified   director-engine 08:4xZ 09-23 on the post branch:
  1 LIVE   rotate.py:7263-7265   while True: time.sleep(args.interval); return cmd_alarms(args, root)
           -> one stack frame per interval; RecursionError after ~1000 polls (~83 h at 300 s); the alarms service runs 24/7
  2 LIVE   rotation_alert.py:1414-1418 writes capture-<seat>.json {"first": t} once (if not exists); nothing unlinks it
           rotation_alert.py:793-799 reads it -> a successor's first over-line crossing force-captures at once on the
           predecessor's stamp: the card_capture_minutes grace is skipped for every session after the first (per boot)
  3 latent rotation_alert.py:875-877 ratio = float(ladder.get("captive_rotate_ratio", 0.85)) / except -> 0.85
           -> trigger (a) turns ON at 0.85 with only captive_rotate_masters set or an unparseable ratio;
           docstring :870 says OFF BY NAME until a captive cell exists (live ladder.md:16 sets 0.85, so latent today)
proves     committed tests, each red on the pre-fix bytes:
           (1) many-interval alarms run (sleep monkeypatched) -> stack depth flat
           (2) two sessions of one seat -> the second waits the full grace
           (3) ladder without a parseable ratio -> trigger (a) off by name
           + the touched files' existing tests green
NOT this   the shared in-flight latch = hypothesis:l5-the-two-captive-rotation-triggers-share-one-in-flight-latch-per-seat (SM.142)
```

## Agent Notes
assigned: director-engine (0921 residue batch, engine slice, goal:g15.27); minted by director-engine after verifying the bytes.
