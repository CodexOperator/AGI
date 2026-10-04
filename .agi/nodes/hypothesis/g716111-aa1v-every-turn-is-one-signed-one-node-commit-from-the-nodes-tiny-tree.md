---
id: hypothesis:g716111-aa1v-every-turn-is-one-signed-one-node-commit-from-the-nodes-tiny-tree
mint_id: 5e20b10918194ec5b44bfa3cc3bbfd02
type: hypothesis
parents:
  - goal:g7.16.1.11.11
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 42f4e83a3b7ce0b9
season: 2
testable_claim: "On a live v5 turn with two node trees changed, `git log` on posts/<p> shows exactly two new commits, each signed (%G? = G), each named for its node (`<post>: <path>`), each changing exactly ONE node file under .agi/nodes plus only that node's payload_ref paths (V4); a turn with no edits makes no commit; a node whose tip changed since pull keeps the tip's version and the post's version goes to refs/archive/<p>/<mint> (`[moved]`, tree dropped, never overwritten); a raced CAS is reported, not retried."
title: "AA1.V: agi-turn makes ONE signed commit per changed node from the node's tiny tree onto posts/<p> (the box send primitive over a one-node tree), changing only that node file and its payload_ref paths"
town: core
---
# hypothesis:g716111-aa1v-every-turn-is-one-signed-one-node-commit-from-the-nodes-tiny-tree

## Measured
- doc:rse-aa1-boxes AA1.V (alive, posts/alive f62efcfcf; belam [decision] 00:25Z; split settled 00:2xZ): Owner 00:3xZ (via alive, AA1.V): "Couldn't the grid become the only commit surface instead ... Every turn is a GRID commit. ... The grid commit is a smaller total commit just a tiny worktree for a single node getting updated per turn as needed. Other node worktrees la get brought in and spawned dynamically as needed then purged."
- Today: agi-turn = `git add -A` + one whole-tree commit per turn in ~/t and it drops every unclaimed tree each turn; agi-wt drop copies the tree BACK into ~/t; agi-link guesses node <-> code from changed paths; the grid is a separate */5 cron (9,563 of 11,779 refs).
- Scratch 19/19 (G1-G9): two trees = 2 commits one node each, %G? = G, no edit = no commit, a tip moved by a merge = [moved] + refs/archive, `agi-wt new` lands on posts/alive, 0 refs/grid.
- Bytes: agi-turn 269 -> 1,074 B, agi-wt 688 -> 819 B, agi-link 358 B retires: net +578 B in the post pieces, EXPANSION, 0 B in the zygote (AA2 owns the 8 KB account).
- DOWN merges (two-parent commit-tree) are safe to land only with AA3.4 fix 4 (`diff-tree -r -c`): all-is-one 00:3xZ. One-node-per-commit is AA1's invariant to test, not land's.

## CLAIM
On a live v5 turn with two node trees changed, `git log` on posts/<p> shows exactly two new commits, each signed (%G? = G), each named for its node (`<post>: <path>`), each changing exactly ONE node file under .agi/nodes plus only that node's payload_ref paths (V4); a turn with no edits makes no commit; a node whose tip changed since pull keeps the tip's version and the post's version goes to refs/archive/<p>/<mint> (`[moved]`, tree dropped, never overwritten); a raced CAS is reported, not retried.

## Dispatch line
config-max: none new (agi-turn/agi-wt are post pieces in engine-post) / template-max: none / code: agi-turn (1,074 B) + agi-wt (819 B) expansion; agi-link retires.

## FALSIFIERS
AA1.V1 one live turn of a v5 post with two trees = two signed one-node commits on posts/<p>, `git log -1 --format=%s` names the node · AA1.V4 every commit agi-turn writes changes exactly ONE node file under .agi/nodes plus only that node's payload_ref paths (G3 on scratch) · a no-edit turn writes 0 commits · a tip-moved node is archived, never overwritten.

## TESTS
re-run the scratch G1-G9 (fix.sh + t.sh) on the BUILT bytes; one live turn as a v5 uid on a throwaway node.

## FILE SCOPE
engine-post pieces agi-turn + agi-wt + the retirement of agi-link; the briefs say 'edit in agi-wt pull's directory'. Never a post's real tip beyond one throwaway node.

## CEILING
1 parent · kids <= 2 · +578 B expansion, 0 B in the zygote · regular review. DEPENDS ON the principal form `<post>@agi` and the ring (goal:g7.16.1.11.12).
