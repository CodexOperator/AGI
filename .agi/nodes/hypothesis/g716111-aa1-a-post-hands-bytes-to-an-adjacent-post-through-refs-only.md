---
id: hypothesis:g716111-aa1-a-post-hands-bytes-to-an-adjacent-post-through-refs-only
mint_id: 050617d6a9824c3e8bb745c0e0a7c8d6
type: hypothesis
parents:
  - goal:g7.16.1.11.11
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 1feb199298d5c70b
season: 2
testable_claim: "On the real shared .git, a v4 post (agi-alive uid) receives a message sent from an adjacent post: `box n` counts it, `box read` prints it and moves refs/held/alive/<from>, the next `box n` is 0, and no file under .agi/sessions/inbox is written by either side; the box script is <= 1,800 B."
title: "AA1: a v4 post sends and reads mail through refs/box refs only, with no inbox-file write and no read marker"
town: core
---
# hypothesis:g716111-aa1-a-post-hands-bytes-to-an-adjacent-post-through-refs-only

## Measured
- doc:rse-aa1-boxes (posts/alive 0a58624a1): scratch B1 belam->alive `n, read, n` = 1, `[belam] order 1`, 0; B2 two sends + the reader dies + a fresh process reads = both, in order; 25/25 PASS on scratch (two repos = two boxes, a bare hub, throwaway ed25519 keys).
- Live today (alive, 23:3xZ): send.py read printed belam's order then PermissionError writing the marker; the inbox files are belam:belam 664; the shared .git refs/ + objects/ + logs/ carry ACL group:agi rwx with the same default ACL, so a post can create and move a ref.
- DEPENDS ON: the principal form `<post>@agi` and the root-owned ring (goal:g7.16.1.11.12), else every verify-commit says No principal matched.

## CLAIM
On the real shared .git, a v4 post (agi-alive uid) receives a message sent from an adjacent post: `box n` counts it, `box read` prints it and moves refs/held/alive/<from>, the next `box n` is 0, and no file under .agi/sessions/inbox is written by either side; the box script is <= 1,800 B.

## Dispatch line
config-max: the matrix rows `post in box/*/<p> box` + `post out box/<p>/* box` in config:engine (~+110 B) + ONE map line (~+70 B) / template-max: none / code: the `box` script in config:engine-wrap (expansion) + agi-run's wake line (211 -> 142 B).

## FALSIFIERS
AA1.1 belam -> alive on the live shared .git, read by the agi-alive uid, held moves, the next `box n` = 0 · AA1.5 no .agi/sessions/inbox write by a v4 post (git grep over the box script and the wake line = 0 hits) · the box script is <= 1,800 B.

## TESTS
scratch re-run of B1-B8 (t.sh + fix.sh from the AA1 scratchpad) green on the BUILT bytes; one live lane as the agi-alive uid; the send neighbourhood of the old setup stays green.

## FILE SCOPE
config:engine-wrap (box + agi-run wake line) · config:engine (the two matrix rows + the map line) · the AA1 doc. Never send.py (old setup keeps it), never a live ref of another post.

## CEILING
1 parent · kids <= 2 (Sonnet 5.5) · config:engine stays <= 8,192 B after the rows · 0 B in the zygote · regular review.
