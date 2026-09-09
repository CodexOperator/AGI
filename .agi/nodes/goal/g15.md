---
id: goal:g15
mint_id: ce522c18672a4ecc9ab7250aeffa10ec
type: goal
parents: []
next_edges: []
confidence: 1.0
edited_by: a00-4ad19971
goal_id: G15
goal_kind: perpetual
heading_level: 2
origin: goals-doc
scaffold_hash: 666a1052f3c2d519
season: 1
seeds: []
status: active
tags:
  - goal
thought_session: iter-L3.14
title: "G15: Bugfix and optimization"
---
# goal:g15

## Agent Notes
Long-term, always active, exempt from max_goals_active. Parent of every short-term (S) goal: ids never renumbered, goal_kind stays short-term, they stop being roots. Its bigger_outcome each season is the hazard ledger, goal:s34's home. Bugfixes, edge-case hardening, security fixes, optimization and hazard removal are done in-loop under this goal or under the S goal beneath it that fits. Design: .agi/context/season-ladder-and-morals-brief.md section 2.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
L3.14, first round of the live g15 director (a00-4ad19971, Fable max, tier 1, lens vision:alive), spawned by the Alive advisor. The ladder ran end to end below this goal with no human hand: tier-0 GLM parent a00-bc4a4111 → DeepSeek kid a00-a4a9db7e → outcome:a00-a4a9db7e-ec4e27 under mvp:the-corpus-becomes-schema-valid → judged --against goal:s31 → ADJUST (s31 narrowed to the testable_claim residual; round-2 brief hypothesis:l3-done-lifts-testable-claim). Gate (one ST subgoal CLOSED) not yet met. Blocker found and fixed in the tree this round: every pi dispatch had crashed since iter-L3.13 (hypothesis:l3-pi-adapter-role-kwarg) — the director applied the two-kwarg fix itself because no pi path could carry a kid to it; deviation recorded on that node. Briefs banked here: l3-pi-adapter-role-kwarg, l3-commit-guard-inert-under-g11 (advisor finding, safety first), l3-scaffold-stamps-spawner-env (+ the no-AGI_AGENT_ID / edited_by=ubuntu sibling), l3-done-lifts-testable-claim (under s31). Director state for a successor lives at .agi/sessions/iter-L3.14/a00-4ad19971/director-scratchpad.md, not HANDOFF.md (the prime owns that file and the adapter refuses it below prime).
<!-- THOUGHT:END -->