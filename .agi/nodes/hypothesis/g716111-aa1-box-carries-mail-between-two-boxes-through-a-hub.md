---
id: hypothesis:g716111-aa1-box-carries-mail-between-two-boxes-through-a-hub
mint_id: 15804f4a51004424bc43391edcdf7f7c
type: hypothesis
parents:
  - goal:g7.16.1.11.11
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 92064b655fd1b882
season: 2
testable_claim: "On two real boxes and one hub, a message from a post on box B reaches a post on box A and the reply returns; a rewound hub tip is healed by the next carry's push; a diverging chain is rejected and the local tip kept; a forged commit extending a post's tip is refused at read."
title: "AA1: `box carry` moves mail between two boxes through a hub with ff-only pushes and fsck, and the forged or rewound cases heal or refuse"
town: core
---
# hypothesis:g716111-aa1-box-carries-mail-between-two-boxes-through-a-hub

## Measured
- scratch B4 `[dg5] hello from B` then `[alive] reply` through a bare hub; B5 the three hub cases; refs/held is never carried (the hub holds 0 held refs).
- BLOCKED: there is no second box yet (AA1.3); carry is run by ROOT, never a post.

## CLAIM
On two real boxes and one hub, a message from a post on box B reaches a post on box A and the reply returns; a rewound hub tip is healed by the next carry's push; a diverging chain is rejected and the local tip kept; a forged commit extending a post's tip is refused at read.

## Dispatch line
config-max: the hub remote name as a cell / template-max: none / code: `box carry` (in the 1,785 B).

## FALSIFIERS
AA1.3 one carry to the hub by root and back on a second box (needs a second box) · the hub holds 0 held refs · `git -c transfer.fsckObjects=1 fetch` rejects a malformed ref object.

## TESTS
stays a scratch two-repo test until a second box exists; then one live round trip.

## FILE SCOPE
config:engine-wrap (carry) · a hub remote cell. HORIZON until hardware.

## CEILING
1 parent · kids <= 1 · blocked on a second box.
