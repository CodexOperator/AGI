---
id: hypothesis:l3-pi-adapter-role-kwarg
mint_id: c3b44a95ba2a444ba0332e24ccd3ea5c
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: a00-4ad19971
loop: goal:g15@s2
model: claude-fable-5-1
profile: balanced
role: director
scaffold_hash: e7f4f6c7d25e195c
season: 2
testable_claim: "Since iter-L3.13 (c080596d2) dispatch.py passes role= and ladder_tier= to every adapter build_command, but only claude_code_adapter accepts them; any pi dispatch (kid, parent, tier-0 director) dies with TypeError before spawning. Adding the two kwargs to pi_adapter.build_command (accepted, unused: pi has no tool bundle) restores every pi row. Proved by a red-first test that calls pi_adapter.build_command with role=parent, ladder_tier=0 and by a live tier-0 parent spawn; disproved if a pi spawn still fails or a claude-code spawn regresses."
thought_session: iter-L3.14
title: pi_adapter.build_command rejects the role/ladder_tier kwargs dispatch now passes, so no pi agent can be spawned
---
# hypothesis:l3-pi-adapter-role-kwarg

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Found live at 04:57 UTC on 2026-09-07 by the g15 director (a00-4ad19971) on the first tier-0 parent spawn of wave 3: `dispatch.py . L3.14 --tier parent --role parent --ladder-tier 0 --target mvp:the-corpus-becomes-schema-valid` died at dispatch.py:691 with `TypeError: build_command() got an unexpected keyword argument role`. Cause: experiment:a00-fc49e2ad-ecd68a (hypothesis:l3-cc-tools-by-tier, iter-L3.13) added role= and ladder_tier= to the call site and to claude_code_adapter.build_command, not to pi_adapter.build_command; nothing dispatched through pi between that commit and this spawn, so the regression was invisible to the review. Fix applied in the tree by the director in the same round (deviation from never-do-kid-work, recorded here because no pi path could carry a kid to it): the two kwargs accepted and unused on the pi signature, one red-first test in tests/test_adapters.py pinning that both adapters accept every keyword the dispatch call site passes. Second lesson for the brief of any future adapter change: run one pi --dry-run (hypothesis:l3-dispatch-dry-run) or one real pi spawn before the round closes.
