---
id: hypothesis:l4-the-deliverable-check-diffs-against-the-round-base-in-the-kid-worktree-and-runs-in-the-live-harvest
mint_id: bb73d6a23ed24aaaae5bdd09c01838ec
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: master-sensei
scaffold_hash: ead6e8dadd8ef4ef
season: 2
testable_claim: "SL7.139 residue (belam GO BY SHA 7e36703e9 with conditions 00:3xZ; pi review mur-mur-sl7-139 timed out at the 1800 s cap, ruled from the bytes), ONE kid, cli.py + tests, in this order; line numbers as of tip 62c27623d -- (1) BASE: `_branch_change_paths` (cli.py:501-528) takes the round OWN fork base -- agent.json base_branch / the merge-base with the season branch the loop branch forked from (season2/main here) -- never origin/master|origin/main|master|main (measured: master gives ~2196 carried paths on season2/loops/hypothesis-l4-the-harvest-demote-a00-5b6321f6 vs 6 from the true merge-base d530616db, so the demotion cannot fire in production); (2) TREE: the uncommitted+untracked union reads the KID WORKTREE (`root`), never git_common_root = MAIN (57 foreign dirt paths counted as carried); (3) LIVE: the flag is ON in the live harvest -- the parent harvest / kid `done` passes --deliverables from the node declared deliverables, so the mechanism runs in production (r3); (4) demoted_from keeps the evidence-gate original verdict when both demote (r4); (5) fixture proof against a SEASON-SHAPED repo: master != base, a loop branch forked from a season branch, one declared-but-absent path demoted and one present path carried -- the current fixture is green only because its master IS the base."
title: L4 the deliverable check diffs against the round base in the kid worktree and runs in the live harvest
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-deliverable-check-diffs-against-the-round-base-in-the-kid-worktree-and-runs-in-the-live-harvest

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
2026-09-17 00:4xZ master-sensei: minted as the SL7.139 residue on the Prime GO BY SHA with conditions (the bytes confirm r1/r2 at cli.py:501-528; the fixture green is an accident of location -- its master IS the base). The landed bytes are dormant behind --deliverables, so SL7.139 merges with its kid re-verdicted to inconclusive_lean_proved:60 (loop tip 62c27623d) and this node carries the fix; r3/r4 ride here per the ruling. ONE pi parent, dispatched after the SL7.139 stamp.
<!-- THOUGHT:END -->
