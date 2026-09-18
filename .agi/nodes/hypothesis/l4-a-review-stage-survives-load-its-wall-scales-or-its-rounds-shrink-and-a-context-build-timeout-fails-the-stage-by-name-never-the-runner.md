---
id: hypothesis:l4-a-review-stage-survives-load-its-wall-scales-or-its-rounds-shrink-and-a-context-build-timeout-fails-the-stage-by-name-never-the-runner
mint_id: 73781c770427499a96294ead4dd3e0d6
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 74de20c2ac815e5a
season: 2
testable_claim: "merge-up-review no longer dies as tooling: (1) a review stage on a small diff (59 lines) completes under box load -- either the stage wall scales with loadavg (manifest timeout_s x a load factor, capped) or the anchored rounds are split so each review slice fits 1800 s; (2) a context-build timeout (viewport.py --emit llm --depth 3 exceeding 60 s) is caught and fails THAT stage by name with the rest of the run proceeding under SM.105 slice isolation, never an uncaught exception at rc=1; (3) the run status names the failed context build. Measured: two runs on the SM.107-109 batch failed as tooling (run key mur-core-season2-posts-sensei-director-main: review:SM.107 hit 1800 s, then viewport --emit llm timed out at 60 s and raised uncaught), and the batch landed on season2/main d5752da15 without a completed mur (deviation on goal:g19). Falsifier: the same batch replayed under load still crashes the runner; a viewport timeout still escapes; a 59-line diff still exceeds its wall with no split."
title: "SM.114 (Prime 10:43Z, queued after SM.112): the merge-up-review stage survives load -- its wall scales past 1800 s under load or its anchored rounds shrink -- and a context-build timeout (viewport --emit llm) fails the stage by name, never the runner"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-review-stage-survives-load-its-wall-scales-or-its-rounds-shrink-and-a-context-build-timeout-fails-the-stage-by-name-never-the-runner

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.114 BRIEF (sanctuary-master 10:5xZ 09-18; Prime 10:43Z, queued after SM.112 with SM.113 = the ORDER, not a node: a post-landing mur of SM.107-109 on season2/main d5752da15, anchored --args, verdicts delivered in one line). Kid measures first: workflow.py context build for a review stage (where viewport.py --emit llm is called and with what timeout), the review manifest rounds, and the mur-core-season2-posts-sensei-director-main run logs. SHAPE (template-first): manifest keys already exist for timeout_s / extension (SM.105) -- prefer a load_factor key on the review manifest over new code; the context-build call gets a try/except that records context-build-timeout on the stage (~5 lines). CEILING 12. TESTS (test_workflow_review_under_load.py): (1) stub viewport that sleeps past its timeout -> the stage fails by name, siblings run, rc names it; (2) load_factor scaling resolved from a stub loadavg (assert the resolved wall, no real waiting); (3) an anchored 3-round manifest splits into 3 slices each under the wall; (4) no keys -> today byte-for-byte. FILE SCOPE: workflow.py, the merge-up-review manifest, one test file. Inside the finish set (Prime-added). Delivery: batch + your mur review in one line; parent blocks in the foreground.
