---
id: goal:g7.33.12
mint_id: 9c4cd1b695e3470dbb1d8fb323dffbe3
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.9
edited_by: director-engine
goal_id: G7.33.12
goal_kind: subgoal
origin: goals-doc
scaffold_hash: c2280d2ac5c17d0c
season: 2
seeds: []
status: complete
tags:
  - local-maxxing
  - engine
  - research-review
title: "G7.33.12: RESEARCH-REVIEW SEES EVERY PROPOSAL -- the refute stage never silently drops brainstormed hypotheses when propose-only mode never minted them"
town: core
---
# goal:g7.33.12

| | |
|---|---|
| goal | agi-research-review's REFUTE stage evaluates whatever the BRAINSTORM stage actually produced, minted (mint:true) or proposal-only (mint:false) -- the adversarial filter must never silently see an empty list when real proposals exist |
| origin | surfaced live by director-engine running rr-lm-qk-norm-model-wall-parent in propose-only mode: brainstorm proposed 3 hypotheses, refute read "No hypotheses were supplied by the brainstorm stage" -- the filter never ran on them · ordered as thought-master TMM.144 item 3 (00:54Z 09-25, the owner's priority call), landed same session |
| where | extensions/agi/workflows/agi-research-review.js:36 (REFUTE_TMPL, only ever templated `{hypotheses}`) and its call site (~line 53, `fill(REFUTE_TMPL, ...)`), plus the matching JSON manifest's refute stage prompt |
| done | REFUTE_TMPL now templates both `{hypotheses}` (minted, real ids) and `{proposed_hypotheses}` (proposal-only, no id) explicitly, and RETURN CONTRACT `ready_batch` entries carry a real id only when one exists, else the proposal's title -- so MODIFY knows whether to call write.py or just return a corrected title/claim · fill()'s array interpolation now JSON.stringifies instead of naive string-substitution (would have printed "[object Object]") · new test_research_review_refute_sees_proposals.py plus the two pre-existing research-review test files: 17 passed |
| who | director-engine, ordered by thought-master (TMM.144 item 3 / TMM.147 item 2) |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted retroactively (gen 13, director-engine) for code that already landed at 74fde134d8 (merge-up #12) -- the owner's 01:13:03Z line, relayed by thought-master (TMM.146/TMM.147) and independently corroborated verbatim on town:local-maxxing's board (.agi/nodes/town/local-maxxing.md): "research review bug can be prioritized at this time" is why this fix jumped the queue ahead of TMM.136 and round B goal:g7.33.10 the same session (the raw owner utterance itself was not found in director-engine's own session transcript, so this quote rests on two independent, byte-identical relays rather than the primary source directly). Nested under goal:g7.33 (ENGINE FIXES SURFACED BY THE TOWN) as a sub-sub goal per the owner's 16:24Z fixes-nesting rule, rather than under goal:g6.11 (a spawn/dispatch/kid-lifecycle TEST-coverage bucket unrelated to this workflow) -- g7.33 is the family this fix actually matches: surfaced by the town's live operation, fixed by director-engine, batched by thought-master, same shape as g7.33.9/g7.33.10/g7.33.11.
<!-- THOUGHT:END -->

## Agent Notes
director-engine (gen 13): retroactive goal for already-landed and tested code (74fde134d8, merge-up #12). No round dispatched -- nothing left to do.
