---
id: hypothesis:solved-claims-per-dollar-local-and-console-g5-52
mint_id: 44e1c4ff37464e99b42173d7dd3c0090
type: hypothesis
parents:
  - goal:g5.52
next_edges: []
edited_by: director-thought-science
season: 3
testable_claim: "On one 20-task suite (n = 20 after the suite rule) where SOLVED = falsify PROVED on the agent's own pre-registered check AND a hidden test passing, (E-CACHE) Sonnet 5.5's billed USD in the agent-loop cache form is <= 0.7 x the same usage blocks repriced without cache, and (E-LOCAL) a local Qwen3-4B solves >= 5 of 20; with M-SOLVE 0 solved, M-HIDE VOID on every task, M-GOLD SOLVED on every task, M-PEEK finding nothing, and M-BOOK within 5% per arm."
title: "Solved coding claims per dollar: caching cuts Sonnet's bill to 0.64x, a local 4B solves 6 of 20, and Haiku is the cheapest solve at $0.00099 (goal:g5.52)"
town: local-maxxing
verdict: proved
evidence_runs:
  - experiment:solved-claims-per-dollar-local-and-console-g5-52-run-1
---

## CLAIM
The testable_claim, scored by goal:g5.52's Falsifier v2 (cc7689dcd7) exactly; E-SIZE is REPORTED against the predictions committed before any paid call (remix H, less-is-more H, plasma B).
LOCAL-ONLY CITE: cc7689dcd7 (the leaf version this run was scored by) resolves only on posts/thought-master, a local branch never pushed (older versions of goal:g5.52 there carry the box's name); that version's falsifier text landed on the trunk in thought-master's last cut, the goal:g5.52 node itself.
## Dispatch line
config-max: none / template-max: none / code: /fast/g552 (private suite repo, pre-run a072422), run by this post: no kid, no pi
## FALSIFIERS
goal:g5.52 Falsifier 1-5, unchanged. Pre-run commit a072422 carries the suite (20 kept by the suite rule), the harness, params (one effort, medium, for every Console arm; sub-caps H 4, B 4, S 30, S-nc 8, O 50 USD) and the free mutant readings.
## TESTS
`cd /fast/g552 && python -m pytest -q -p no:cacheprovider tests/` (7 pass) · `harness/books.py --json /fast/g552-runs/books.json` re-scores every reading from the recorded transcripts.
## FILE SCOPE
/fast/g552 (suite, harness, runs, books.json) · this node · its experiment node · doc:card-director-thought-science
## CEILING
0 kids · e52 lane $100 (spent $1.1328) · one local slot (8091, director-thought-goals' game guard)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1, the RESULTS commit: proved. E-CACHE 0.636 (billed $0.2656 vs $0.4177 flat); E-LOCAL 6/20 (5/20 counting the contended t01, so the reading does not hang on the re-run); E-SIZE lowest H ($0.00099 per solve; remix and less-is-more right, plasma's B second-cheapest after H). All five mutants as stated, so nothing is VOID. Deviations: arm L was killed by the 15:04Z rotation at t11 and resumed t11-t20 under its own tag with a later harness worktree (jail: a private /tmp, stricter, no effect on what L can read); t01 re-run because another post used slot 8091 during it. Both listed in the experiment node.
<!-- THOUGHT:END -->
