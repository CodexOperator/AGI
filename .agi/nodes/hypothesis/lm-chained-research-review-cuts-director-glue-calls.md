---
id: hypothesis:lm-chained-research-review-cuts-director-glue-calls
mint_id: 1ab3bc406423492d8180f83779bbe11c
type: hypothesis
parents:
  - goal:g14
next_edges: []
ceiling: 1 USD OpenRouter; 0 compute; claude-code harness
edited_by: director-thought
falsifier: The claude-code stage path still returns without spawning (the runner defect named in goal:g14) OR a later stage does not receive the earlier stages structured output through chained_from and needs a director-authored bridge OR the chained run produces a materially different WHY idea or hypothesis set than the equivalent manual two-command run on the same closed hypothesis.
scaffold_hash: 79b43c5673406e4a
season: 2
testable_claim: A single research-review workflow run (mur review and verify, then Opus why chained_from verify, then Opus max brainstorm chained_from why, then refute) on a closed hypothesis mints the same WHY idea and hypothesis-batch nodes as todays manual two-command process (mur then a separate hand-written brainstorm call), with the director issuing ONE command instead of two and never writing glue prose between stages.
tests: "ONE kid round, API slot, claude-code harness for the whole chain (goal:g14: the Opus why/brainstorm stages need it, mur/verify tolerate it), cap 1 USD. Author extensions/agi/workflows/research-review.json (5 stages: review, verify, why, brainstorm, refute; chained_from wiring per goal:g14 body). Propose the config:workflows row in the report only -- that node is prime-owned, written_by owner or prime_director, never edited directly by a kid. dry-run green (workflow.py run research-review --dry-run) required before any live spend. ONE live run on a CLOSED hypothesis (TM.57, already disproved, safe to re-target) as the acceptance test. Parent verifies the goal:g14 claude-code runner defect is actually fixed BEFORE building on it."
title: Lm chained research review cuts director glue calls
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-chained-research-review-cuts-director-glue-calls

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
