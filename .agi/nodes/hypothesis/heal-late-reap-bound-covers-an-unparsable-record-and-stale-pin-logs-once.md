---
id: hypothesis:heal-late-reap-bound-covers-an-unparsable-record-and-stale-pin-logs-once
mint_id: cabc8d59dbe14ef6b192a06dd7f56510
type: hypothesis
parents:
  - goal:g1
  - hypothesis:pass8-0926-residue-batch
next_edges: []
edited_by: belam
scaffold_hash: 6644a106ee946d81
season: 2
testable_claim: A rotation record whose recorded_at does not parse is bounded like any other (reaped or closed after the declared wait, never waiting forever), and a STALE-PIN row logs once until its state changes, not on every pass.
thought_session: belam-S2-L5-IX
title: "heal's late-reap bound covers an unparsable record, and STALE-PIN logs once per row (assigned: director-engine)"
town: core
---
# hypothesis:heal-late-reap-bound-covers-an-unparsable-record-and-stale-pin-logs-once

# heal's late-reap bound covers an unparsable record, and STALE-PIN logs once per row

## Measured (PASS 8 pin-reap round, verify)
- heal.py:780-783 returns {action: waiting, reason: no-recorded_at} with no bound and no close for a record whose recorded_at does not parse (only ...Z / naive-local accepted); a committed test asserts that unbounded case green.
- heal.py:2636-2639 emits one `watch: pin-reap STALE-PIN` line for every non-KEEP row on every pass, with no one-shot close (contrast the `already` guard at :772-777).

## Falsifiers
- a record with an unparsable recorded_at still waiting past the declared bound; a STALE-PIN row logged twice without a state change.

## Agent Notes
assigned: director-engine (PASS 8 residue, belam-S2-L5-IX 09-26; runs mur-p8chunk{1..15}of15)
