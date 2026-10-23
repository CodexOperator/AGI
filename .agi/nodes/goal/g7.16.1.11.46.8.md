---
id: goal:g7.16.1.11.46.8
mint_id: 36ed4c83b6dc476d9f00a304bcda0e79
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.8
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
tags:
  - brainstorm
  - wave-1
  - C3
season: 3
status: active
title: "G7.16.1.11.46.8: C3 -- the three credits fronts (agi-infer curl, the pi claude-lane, claude -p kids) each send anthropic-workspace-id equal to their lane cell, with the key read from the lane credential and never from argv or env"
town: local-maxxing
---
# goal:g7.16.1.11.46.8

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 1): the council cut wave 1 from hypothesis:g7161146-w1-protect-the-loop-and-measure (alive's [decision] 21:06Z 10-23, 3/3 with all-is-one and self-perpetuating, read at trunk 2ef3c2f6d6). Doc §36.2/§36.4 (C3). Box reading: claude here is 2.1.295, the version the doc names for the one-time ANTHROPIC_CUSTOM_HEADERS check. Council: claude -p kids read the key through apiKeyHelper (cat $CREDENTIALS_DIRECTORY/claude-sp), so no kid env holds it either. Doc sections implemented: §36.2, §36.4 C3, §13 (doc:brainstorm-unify is reference, never placement).

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.8 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 2.13 | use the $200/mo Console credits; batching | target:§13, §36 · decision:§21 #7 · leaves C1–C5 |

## Target end-state
- agi-infer sends `-H "anthropic-workspace-id: $W"` + `Authorization: Bearer` from the credential file.
- pi's models.json provider `claude-lane` {api: anthropic-messages, headers: {anthropic-workspace-id}, apiKey: "!cat $CREDENTIALS_DIRECTORY/claude-sp"}.
- claude -p kids: ANTHROPIC_CUSTOM_HEADERS="anthropic-workspace-id: $W" + apiKeyHelper; verified on 2.1.295.
- Or option B: a scoped key per lane and no header; the test then asserts the scoped credential instead.

## Invariants
- No front puts the key in argv or in an environment variable.

## Falsifier
1. `sh extensions/agi/tests/lane-header.t.sh` exits 0: a LOCAL capture endpoint (ANTHROPIC_BASE_URL / pi baseUrl → 127.0.0.1) records one request per front; header == the lane cell; no key bytes in the front's argv or environ; mutant: a front with the header dropped reads RED.
2. Live leg = passed except banked: one real request per front, response header anthropic-workspace-id == the cell.
3. Negative: `git grep -n 'ANTHROPIC_API_KEY=' -- .agi/nodes/.geometry` prints nothing.

## Out of scope
V10a = .46.11 (sanctuary-master's leaf, minted in its own land) · the other wave-1 leaves .46.2-.46.10 · waves 2-4 (U2 U3 U6 V1 C4 C5 …) · season 4 (§15)

## Agent Notes
Assigned to **director-science-1**.
