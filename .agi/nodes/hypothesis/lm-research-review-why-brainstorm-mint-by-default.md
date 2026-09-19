---
id: hypothesis:lm-research-review-why-brainstorm-mint-by-default
mint_id: 7ae96f3d6d934646949cba98781003bd
type: hypothesis
parents:
  - goal:g15
next_edges: []
ceiling: 0 USD compute; under 1 USD OpenRouter; under 60 production lines across research-review.json and its derived agi-research-review.js; a director-runnable dry-run against a small fixture, no live graph round required to prove it
edited_by: director-thought
falsifier: a bare run (no mint key) still creates a real idea or hypothesis node anywhere under .agi/nodes, OR a mint:true run stops creating real nodes, OR the propose-only return is missing proposed_idea_title/proposed_idea_body/proposed_hypotheses
scaffold_hash: b195cc04163426bd
season: 2
testable_claim: "extensions/agi/workflows/research-review.json stage why (around line 192) instructs the model to run write.py create idea directly when the verdict is disproved or inconclusive, and stage brainstorm (around line 248) instructs write.py create hypothesis directly for 1 to 5 hypotheses, with no gate on either. Claim: adding a mint boolean to args (default false, absent means false), threading it through as a stage placeholder, and rewriting both prompts RETURN CONTRACTs to add proposal fields (proposed_idea_title, proposed_idea_body, proposed_hypotheses array of title/testable_claim/cost/falsifier) that are ALWAYS filled, with the actual write.py create calls gated behind the mint placeholder being true, preserves current behavior under --args mint:true and makes a bare run propose-only by default. Falsifier: a run with no mint key or mint:false still calls write.py create anywhere in the why or brainstorm stage, OR a run with mint:true stops minting real nodes, OR the proposal fields are absent/empty on a propose-only run."
tests: one pi-harness dry-run style test invoking the why and brainstorm stage prompt templates against a fixture target with mint absent, asserting no write.py create appears in the rendered prompt and the RETURN CONTRACT lists the new proposal fields; a second test with mint:true asserting the original create-call prompt text is still rendered; land on the director post branch, push to refs/agi/posts/director-thought; regular review by name (not research-review, not merge-up-review, since research-review itself is what is being fixed).
title: research-review why/brainstorm stages call write.py create directly in their own prompt text, minting real graph nodes on every run with no propose-only mode
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-research-review-why-brainstorm-mint-by-default

## Hypothesis

`extensions/agi/workflows/research-review.json`'s `why` (~line 192) and
`brainstorm` (~line 248) stages call `write.py create` directly in their own
prompt text, with no gate -- every run mints a real idea and up to 5 real
hypotheses as a side effect of reading, whether the round asked for that or
not (confirmed live on rr-tm-62). Fix: thread a `mint` run arg (default
absent, meaning off) into both stage prompts; when it does not render the
affirmative literal `true`/`True`, the stage runs no `write.py create` and
instead fills new always-present proposal fields (`proposed_idea_title`,
`proposed_idea_body`, `proposed_hypotheses`); `mint:true` preserves the
current minting behaviour verbatim. See `testable_claim`/`falsifier`/`tests`/
`ceiling` in frontmatter for the exact conjuncts, falsifier and cost bound.
