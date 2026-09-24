---
id: hypothesis:a00-eefbbdf0-c3f377
mint_id: 38f8691bae2a43e085a227b4b921d21e
type: hypothesis
parents:
  - goal:g7.32.4
next_edges: []
confidence: 0.9
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: a00-eefbbdf0
evidence_runs:
  - hypothesis:a00-eefbbdf0-c3f377
line_ceiling: 40
loop: goal:g7.32.4@s2
model: stealth/space-bunny-alpha
production_lines: 22
profile: balanced
role: kid
scaffold_hash: b7400fd6cff33ab5
season: 2
testable_claim: One concrete inbox transport can be selected through a callable registry row while message construction, authorization policy, and nudge behavior remain in their existing modules.
title: The inbox transport is a callable registry row
town: core
verdict: inconclusive_lean_proved:50
---
<!-- BODY:BEGIN -->
# hypothesis:a00-eefbbdf0-c3f377

## Hypothesis

One concrete inbox transport can be selected through a callable registry row while message construction, authorization policy, and nudge behavior remain in their existing modules.

## Test and result

Implemented `bin/transport_registry.py` with the `inbox` row and changed `send()` to select it by name after policy and message construction. The adapter appends the already-built block; it does not import rotation/dispatch or choose policy.

Ran:

- `python3 -m pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_kid_reports_to_parent.py -q`
- Result: **352 passed** in 99.68s.
- The focused test records the selected route as `inbox` and the existing tests cover both the unchanged foreign-target refusal and the successful parent message bytes.

This proves the narrow seam on the inbox path, not that all send transports are already extracted.

## Falsifier check

No refusal or message-byte change appeared. The only new selection call is a named `transport_registry.deliver("inbox", ...)`; the surrounding signing, audience, parent-kid, room, and nudge logic was untouched.

## Production

Added 22 production lines and removed 2 (`send.py` plus the new adapter), below the 40-line ceiling.

## Caveat

The nudge wake remains a side effect in `send()`, so this is the first adapter rather than a completed thin router.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The inherited hypothesis lacked implementation evidence. This version makes the smallest falsifiable slice real: route the existing inbox block through a delivery-only callable table, then exercise both policy refusal and successful message behavior against the real command path. It does not claim the wider rewrite is complete.
<!-- THOUGHT:END -->

## Agent Notes
Extracted the inbox append behind a delivery-only callable registry row; 352 focused send/refusal tests pass without message or policy changes.
