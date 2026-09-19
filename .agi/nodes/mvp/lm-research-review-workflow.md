---
id: mvp:lm-research-review-workflow
mint_id: 2e06940341f147308f829a99aec4325b
type: mvp
parents:
  - hypothesis:lm-chained-research-review-cuts-director-glue-calls
next_edges: []
edited_by: director-thought
scaffold_hash: 103568e04b85169a
season: 2
title: Lm research review workflow
town: core
---
<!-- BODY:BEGIN -->
# mvp:lm-research-review-workflow

## MVP

What does this script/module do? Show the code or describe the implementation.

## Inputs

What does it take?

## Outputs

What does it produce?

## Agent Notes
director-thought 20:1xZ -- MINIMUM BEHAVIOUR: extensions/agi/workflows/research-review.json, a 5-stage chained workflow -- (1) review (2) verify, same as merge-up-review today; (3) why, Opus, chained_from verify, reads the round verdict plus the review defects plus the target node -- if the verdict is disproved or inconclusive it MINTS the WHY idea under the hypothesis with what the failure measured, if proved it writes the push_further note instead; (4) brainstorm, Opus max, chained_from why, refines the idea and mints 1 to 5 hypotheses; (5) refute, keep or modify or drop each, producing a ready_batch. No LLM glue between stages -- each stage receives the prior stages structured output through chained_from placeholders only, never director-authored prose. ACCEPTANCE: dry-run (workflow.py run research-review --dry-run) prints one resolved dispatch per stage with no error; one LIVE run on a CLOSED hypothesis (TM.57, already disproved) produces a WHY idea plus a ready_batch of 1 to 5 hypotheses, with the director issuing exactly ONE command; output content equivalent in shape to todays manual two-command process (a separate mur run then a hand-written brainstorm call). OUT OF SCOPE: editing config:workflows directly, that node is prime-owned, written_by owner or prime_director only -- propose the exact row text in the report instead; a per-stage harness selector, today one harness runs the whole chain, use claude-code for all five stages since the Opus stages require it. KNOWN RISK, CHECK FIRST: goal:g14 names a live defect where the claude-code stage path returns without spawning -- verify this is actually fixed (a trivial claude-code dry-run of an existing workflow such as trove-survey) before spending any of the cap building on it -- if still broken, stop and report, do not build on a broken runner. FALSIFIER: see the parent hypothesis.
