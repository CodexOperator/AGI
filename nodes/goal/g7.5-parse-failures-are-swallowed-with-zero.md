---
confidence: 1.0
goal_id: G7.5
goal_kind: subgoal
id: "goal:g7.5"
mint_id: 116872160ca44aafadd6c8d1eab645a2
origin: goals-doc
parents:
  - goal:g7
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G7.5: Parse failures are swallowed with zero signal"
type: goal
---

`load_directory`'s `except Exception: continue` and `load_existing_nodes`'s
`except Exception: pass` both silently drop any file that raises while its
frontmatter is parsed. **No caller learns anything.**

On the live corpus this hides exactly one file:
`nodes/hypothesis/a00-1467544f-chain-600hop.md`, whose frontmatter carries a
stray `- "exp:a00-1467544f-chain-600hop"` list line between `id:` and
`parents:`, breaking YAML block-mapping parsing. That file is invisible to the
renderer, the metrics, the chain finder and the dashboard alike — the same
failure mode as G7.1 and G7.2, reached through a hard parse error instead of a
bad reference or an id collision.

Fix: both sites warn with the file path and the exception, following the
warn-by-default / strict-to-fail pattern G7.1 and G7.2 already established.
**Do not repair the malformed node.** Fixing the corpus is a separate,
deliberate decision — the G7.2 rule. This goal is about making the failure
visible, not about making it go away.
