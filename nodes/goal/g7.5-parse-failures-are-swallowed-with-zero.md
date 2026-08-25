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

**This goal also owns one of G7.1's "dangling" references, which is not
dangling.** `nodes/experiment/a00-1467544f-chain-600hop.md` references
`hyp:a00-1467544f-chain-600hop`, and the integrity check reports it as an
unknown parent. **The target exists on disk, with exactly that id** — it is the
malformed file above, and it is absent from the loader's index only because
parsing it raised. So the reference is sound and the *index* is incomplete;
the reported defect is in the wrong place.

Left unfixed on 2026-08-25 for that reason. Repairing the stray list line would
clear the INTEGRITY line and simultaneously destroy the only live evidence this
goal has — the corpus stops demonstrating the defect the moment it is tidied.
**Repair it as part of landing the warn, never before**, and re-run G7.1's sweep
afterwards to confirm the reference resolves rather than disappears. Until then
the count of genuinely unresolvable references is **2**, not 3: this one is a
G7.5 symptom wearing a G7.1 costume.
