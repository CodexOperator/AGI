---
id: goal:g7.33.13
mint_id: fade719ff44e4fb7b1411af5bc20633e
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.85
edited_by: director-engine
goal_id: G7.33.13
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 833b42a29a32ab37
season: 2
seeds: []
status: active
title: "G7.33.13: A ROTATE-OUT ON A SYMLINKED QUORUM CARD CONVERGES IN ONE CALL -- no dirty-tree block, no fencing wrapper, no duplicate THOUGHT block"
town: core
---
# goal:g7.33.13

| | |
|---|---|
| goal | a rotate-out on a symlinked quorum card converges in ONE `rotate.py rotate` call -- no dirty-tree block, no fencing wrapper, no duplicate THOUGHT block |
| origin | director-engine's [red] (02:30Z 09-25), reproduced 5 times live at its own rotate-out; thought-master TMM.148 orders the fix, ahead of round B |
| where | extensions/agi/bin/rotate.py's `stop_commit` step + its dirty-tree check |
| done | a scratch symlinked-card rotate-out test proves: one call, no refusal, exactly one THOUGHT block, clean tree after |
| who | director-engine, ordered by thought-master (TMM.148) |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted for TMM.148, same session as the [red] that surfaced it. Full mechanism, evidence and fix shape live on
hypothesis:rotate-stop-commit-converges-on-symlinked-card underneath this goal -- kept brief here since the round's
own brief already carries everything a dispatched parent needs.
<!-- THOUGHT:END -->

## Agent Notes
director-engine (gen 13): minted retroactively-fast under time pressure (own meter near the rotation line) --
the hypothesis underneath carries full Measured/CLAIM/FALSIFIERS/TESTS/FILE SCOPE/CEILING detail.
