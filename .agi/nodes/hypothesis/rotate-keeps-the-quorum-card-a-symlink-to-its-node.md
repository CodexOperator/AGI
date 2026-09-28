---
id: hypothesis:rotate-keeps-the-quorum-card-a-symlink-to-its-node
mint_id: 201918b4852c4cbd9833ce151c87ac37
type: hypothesis
parents:
  - goal:g6.38
next_edges: []
edited_by: belam
scaffold_hash: f4323886599f982e
season: 2
testable_claim: After rotate-self on a post whose .agi/sessions/quorum/<post>.md is a symlink to its card node, the working tree and HEAD both hold that path as a symlink resolving to the node (git ls-tree mode 120000) and the node file holds the handoff bytes the stop commit wrote; the successor wake needs no ln -sfn and no commit (card trap 10).
thought_session: belam-S2-L5-XI
title: "rotate keeps a symlinked quorum card a symlink: the stop commit versions the node bytes and leaves the link, so no successor re-links by hand (assigned: director-engine)"
town: core
---
# hypothesis:rotate-keeps-the-quorum-card-a-symlink-to-its-node

assigned: director-engine. Forwarded by belam-S2-L5-X on the OWNER's go (00:07Z 09-27, "go ahead and send it forward to your successor"); minted by belam-S2-L5-XI.

## Measured (belam-S2-L5-XI, local-town, 23:1xZ 09-26 + 00:2xZ 09-27)
- `rotate.py` flattens the card symlink on purpose: `_flatten_card_symlink` (def rotate.py:18177) is called at rotate.py:8290 ("a symlinked card is a graph NODE"), :8515, :18125, :18172, :18258 and :19158, and nothing re-links it afterwards.
- So every successor re-links by hand (the Prime's card trap 10): gen 10 at c2724f841 (17:43Z 09-26), gen 11 at 1cf8c1313 (23:1xZ 09-26). At gen 11's wake the flat quorum file was byte-identical to `.agi/nodes/doc/card-belam.md`, so the re-link lost nothing.
- Cost: one `ln -sfn` + one exact-path commit per rotation, against goal:g6.38's "the successor one". Risk (unmeasured): a successor that writes the flat copy before re-linking splits the card in two.

## The fix (the predecessor's two options; director-engine picks)
1. the stop commit versions the node file's bytes without replacing the working-tree symlink; or
2. rotate re-links right after the stop commit, in the same run.

## Test
A rotate-self fixture with a symlinked quorum card: after the stop commit, `readlink` still resolves to the node, `git ls-tree HEAD` shows mode 120000 at the quorum path, and the node file holds the handoff bytes the stop commit wrote.
