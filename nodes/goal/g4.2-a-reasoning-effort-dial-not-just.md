---
confidence: 1.0
goal_id: G4.2
goal_kind: subgoal
id: "goal:g4.2"
mint_id: 1ff9cd74d05644f5ac1e8b9fadb3b24b
origin: goals-doc
parents:
  - goal:g4
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G4.2: A reasoning-effort dial, not just a model name"
type: goal
---

`cc_dispatch.kid_model` selects the model. **Nothing selects how hard it
thinks.** Asked for "sonnet 5 on max settings" the honest answer was that the
dispatch surface exposes model choice and not reasoning budget, so the request
had to be approximated by wording in the brief.

That is a real gap in L3's "fully configurable per tier" claim: a tier is
currently a model name and nothing else. Add effort/reasoning budget as a
per-tier config key alongside `kid_model` and `parent_model`, and make the
delegator tier configurable the same way.

Worth measuring rather than assuming: run the same brief at different efforts
and see whether node quality moves enough to justify the cost. This project's
own evidence says cheap tiers are fine for prose and catastrophic for contract
structure (0.792 vs 0.000) — effort may split the same way.
