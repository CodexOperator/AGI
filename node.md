---
id: hypothesis:l2-graph-hygiene
mint_id: c493e46e654e431094f1f02e00b0825d
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: director
scaffold_hash: ef4e34832fdab6f8
season: 1
testable_claim: The stray .agi/bin directory is gone with its script re-homed under extensions/agi/bin and the experiment that cites it retargeted, and the L2.09 sweep's redundant nodes are deprecated and moved under .agi/nodes/deprecated, with links.py links still at 0 broken and the active plus deprecated count unchanged
thought_session: agi-master-2026-09-06
title: "L2 g15: l2-graph-hygiene"
---
# hypothesis:l2-graph-hygiene

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Two hygiene items from this loop. ITEM 1: .agi/bin/analyze-chat-structure.py (L1.11c stray) sits in a directory CLAUDE.md rule S1 forbids, because driver.sh prefers <project-root>/bin/{snapshot-build-site,inject,render-context}.py over the engine's own. git mv it to extensions/agi/bin/analyze-chat-structure.py, retarget the payload_ref of experiment:a01-c6a5fb12-52f818 through write.py set payload_ref extensions/agi/bin/analyze-chat-structure.py (check its location field too), remove the now-empty .agi/bin directory, and add one test asserting no .agi/bin directory exists in this project. ITEM 2: the L2.09 outcomes sweep left an empty scaffold experiment:a00-1a2f54da-8f6d2b, a mis-named experiment node file .agi/nodes/experiment/season:l2w4.md, and two verdict nodes minted for the same sweep; for each redundant one: write.py set status deprecated with a thought naming the surviving node experiment:a00-1a2f54da-outcome-judgment, then git mv the file to .agi/nodes/deprecated/<type>/ (never git rm; a grid ref outlives the file). Do not touch the surviving experiment. VERIFY: links.py links 0 broken; driver.sh --smoke shows active_node_count plus deprecated_node_count unchanged from before (paste both runs); suite green. REPORT: one experiment node under this hypothesis, verdict, evidence_runs. Do not commit, push, or run grid.py commit.
