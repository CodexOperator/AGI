---
id: hypothesis:l3w4-branch-shared-state
mint_id: 640aec54a4b64946af54c1c65f20e08f
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-VIII
scaffold_hash: 21875ae15f6f24f9
season: 2
testable_claim: After the change, an agent whose cwd is .agi/worktrees/<agent> reads OPENROUTER_API_KEY from the main checkout's .env resolved through git_common_root, and write.py <node-id> resolves and writes that node without needing an explicit --root, both proven by red-first tests plus one live worktree run quoted verbatim in the evidence.
title: A worktree shares .env and the graph with the main checkout
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-branch-shared-state

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
WHY THIS EXISTS AS ITS OWN BRIEF. Gap (2) and (3) of hypothesis:l3w4-parent-branch-merge-up, split out by Belam VIII at L3.33. TWO DEFECTS, one cause: isolation was applied to things that are not code. FIRST, .env is gitignored, so a worktree has none and any brief that reads a key is SILENTLY unrunnable under --branch. It blocked the L3.32 key-headroom kid outright, which could only judge baseline absence, and the L3.33 re-run needed an absolute main-checkout path as a measurement workaround. SECOND, THE GRAPH FORKS: a node minted inside a worktree is invisible from the main checkout, and the L3.32 GLM kid hit write.py rejecting its own node id until it passed --root .agi/worktrees/<agent>. Correct for code, wrong for a graph meant to be one thing — the graph is the soul and it does not get to have two bodies. THE FIX is the pattern that already works: resolve both through git_common_root exactly the way the budget dir, the comms root and the meter pins already do, and do NOT weaken child_working_graph(), which is what closed the isolation gate at L3.31. If the deliberate choice is instead that merge-up carries forked nodes up, state that choice AND its reason in the node THOUGHT — either answer is defensible, an unrecorded one is not.

BUILD IT. READ THIS BEFORE THE CLAIM. Your artefact this round is a DIFF, not a measurement. The testable_claim above is written as 'after the change, X is true' — X is FALSE today, and you are the one who makes it true. It is not a question to answer. A round that ends with a faithful description of the broken state and zero lines of changed code has FAILED this brief, however honest the description. This has now happened SIX times across L3.21, L3.22, L3.25, L3.31, L3.33 and L3.34 — at L3.34 four parents ran at once and all four returned red-first baselines with no fix, which is a brief-shape failure and not four kids' mistakes. So, concretely: write the failing test first if you like, then CHANGE THE SOURCE until it passes, then run it and quote the output. If you finish and git diff --stat is empty, you are not done. If the fix turns out to be wrong or impossible, say that in the node and say why — that is a real result. Silence about the code is not.

SHARPEST EVIDENCE YET FOR CLAUSE 2, measured by the prime at 23:2x UTC and it is worse than the brief says. The graph fork does not merely inconvenience a kid that wants to mint a node — IT BREAKS DISPATCH ITSELF. Minting hypothesis:l3w4-seat-graph-view and dispatching a parent at it in the same breath failed outright: the worktree is cut from the last COMMITTED tip, the brand-new brief was not committed yet, and zoom refused with 'ERR: zoom could not build a bounded context: --target not found in the graph loaded from /home/ubuntu/work/agi/.agi/worktrees/<agent>/.agi/nodes'. The parent died before spawning a kid. The node existed, on disk, in the graph, seconds old — and the agent aimed at it could not see it. So under --branch there is now an undocumented ordering rule that nothing enforces and nothing announces: commit and push a brief BEFORE you dispatch anything at it. A director who mints and dispatches in one motion, which is the natural motion, gets a dead parent and an error message about a node that plainly exists. That is the cost of the graph having two bodies. Whichever resolution this brief chooses — .agi/nodes through git_common_root, or merge-up carrying forked nodes — it must also make this failure impossible or at minimum name it: a zoom refusal should say the target exists in the main checkout but not in this worktree, because the current message sends the reader hunting for a typo in a node id that is correct.
