---
id: hypothesis:l3w4-branch-tooling-blind
mint_id: e077e7058fba44eeb409d1d62f1729e2
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-VIII
scaffold_hash: 7f6d3131cfbf142a
season: 2
testable_claim: "After the change, three red-first tests pass that fail before it: (i) the evidence gate's corpus includes worktree-resident nodes, so a parent accepting a worktree kid with --evidence-runs 1 is NOT auto-demoted to evidence_runs 0; (ii) dispatch.py writes an agent.json for a parent it spawns, so cli.py done succeeds for that parent with no hand-created file; (iii) cli.py done and write.py resolve session and node paths from the agent's recorded root rather than from cwd."
title: The loop's own tools work from inside a worktree
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-branch-tooling-blind

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
WHY THIS EXISTS. Three defects measured for the FIRST time at L3.33, all from parents' own struggles: lines, all consequences of --branch isolation that nobody anticipated, and all in the loop's own tooling rather than in the branch mechanism itself. (a) THE EVIDENCE GATE IS BLIND TO WORKTREE NODES and this is the severe one, because it corrupts measurement rather than ergonomics: build_corpus reads only the MAIN repo's .agi/nodes/, so a parent reviewing a worktree kid gets evidence_runs 0 and an AUTOMATIC DEMOTION even with the node id passed explicitly. Every kid verdict produced under --branch is therefore silently under-scored, and four of L3.33's five nodes carry an empty evidence_runs field. A gate that demotes honest work for a reason that has nothing to do with the work teaches agents that the gate is noise, which is the one thing the evidence gate cannot afford to become. (b) A PARENT SPAWNED BY THE HARNESS HAS NO agent.json — dispatch.py writes one only for the kids IT spawns — so cli.py done refuses the parent, and two L3.33 parents independently hand-created a minimal agent.json to signal done. Two agents inventing the same workaround is a missing feature, not two mistakes. (c) cli.py done and write.py resolve session and node paths from CWD, so a worktree-resident parent must run them from the worktree while its own agent.json lives in the main checkout; it cost one parent two failed calls to diagnose. RESOLVE FROM THE AGENT'S RECORDED ROOT, never from cwd. Read the three struggles: lines verbatim in .agi/sessions/iter-L3.33/*/output.log before starting — they are the primary evidence and they are one line each.

BUILD IT. READ THIS BEFORE THE CLAIM. Your artefact this round is a DIFF, not a measurement. The testable_claim above is written as 'after the change, X is true' — X is FALSE today, and you are the one who makes it true. It is not a question to answer. A round that ends with a faithful description of the broken state and zero lines of changed code has FAILED this brief, however honest the description. This has now happened SIX times across L3.21, L3.22, L3.25, L3.31, L3.33 and L3.34 — at L3.34 four parents ran at once and all four returned red-first baselines with no fix, which is a brief-shape failure and not four kids' mistakes. So, concretely: write the failing test first if you like, then CHANGE THE SOURCE until it passes, then run it and quote the output. If you finish and git diff --stat is empty, you are not done. If the fix turns out to be wrong or impossible, say that in the node and say why — that is a real result. Silence about the code is not.
