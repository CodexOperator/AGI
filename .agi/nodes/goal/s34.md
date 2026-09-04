---
id: goal:s34
mint_id: e00c348e0718409dbdb4aaa6a9c8cbf1
type: goal
parents: []
next_edges: []
edited_by: director
goal_id: S34
goal_kind: short-term
heading_level: 2
origin: goals-doc
scaffold_hash: 84788d877ae9eae0
status: active
thought_session: L1.12
title: "S34: Every hazard carried in a handoff is closed in the loop, not carried again"
---
# goal:s34

## Agent Notes
"Owner ask, 2026-09-04: fix ALL the bugs and hazards discovered in loop L1 that were carried in HANDOFF.md section 8 instead of fixed in the loop. The standing rule, now also in the agi skill: bugfixes, edge-case hardening, security fixes, optimization and hazard removals are done IN the loop, attached to the most relevant goal, tracked in the handoff so they close by the final iteration; anything structural gets its own short or medium-term goal and is banked for the owner. The carried list (HANDOFF section 8, rows 1 to 16): 1 provisioning.py ignores the OpenRouter workspace weekly budget; 2 dispatch.py mints an OpenRouter key for every CC kid; 3 _reap_one restarts on the CLI default model; 4 manifest.json says running after done; 5 write.py set string-typed values (fixed in wave 8, verify); 6 backward-mvp regex heuristic; 7 six demoted prior-director experiments; 8 commands.py verify runs smoke before grid-commit; 9 test_mint_refuses_to_hand_out_a_key_with_no_ttl is non-hermetic; 10 claude_code adapter lets parents write HANDOFF.md, CLAUDE.md, run dispatch.py and git; 11 briefs say experiments parent to goals but [experiment].md forbids it; 12 [verdict].md says contradicts, corpus uses contrasts; 13 two mermaid.py; 14 fantasia/agi clone runs the old grid.py; 15 briefing.py re-reads idea status from disk; 16 untracked nodes vanish across a wave. Each row closes with a fix plus a red-on-purpose test, or is moved to a named goal with a reason. Rows 3 and 4 belong to goal:g4.9."

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"Minted by the L1.08 director at the owner request; the table moves here from the handoff because GOALS.md is the tracker."
<!-- THOUGHT:END -->
