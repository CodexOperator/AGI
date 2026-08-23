---
confidence: 1.0
goal_id: S8
goal_kind: short-term
id: "goal:s8"
origin: goals-doc
seeds: []
status: active
tags:
  - goal
  - root
  - short-term
title: "S8: `zoom.py` bakes the pi-runtime completion contract into the kid context"
type: goal
---

When using the script to inject context, eventually zoom.py fires and inserts the
reference for each kid on how to mark the completion of their task. It currently
inserts a pi-runtime reference for completion, rather than being properly runtime-
agnostic.

Fix: make zoom.py or whatever upstream file be runtime aware and offer the proper
completion contract or have this be set during install.

**Corroborated 2026-08-23 by the iter-9006..9008 run, which hit it three times.**
The generated kid context ends with a `cli.py done` block, so every CC-dispatch
kid was handed a completion contract that `skills/agi/SKILL.md` explicitly
forbids for its role ("do not commit, and do not call `cli.py done`"). All six
spawn prompts had to carry an out-of-band override telling the kid to ignore its
own context file. `exp:noncode-surface-census` independently found the same
contradiction one layer up, between `agent-prompt.md` rules 5–6 and SKILL.md's
kid contract.

That makes this a three-way disagreement — `agent-prompt.md`, `zoom.py`'s emitted
block, and `SKILL.md` — about one procedure, with no file deferring to another.
Note the shape: it is the same defect **G6.6** exists to catch, and G6.6's own
verdict says the currently-prescribed remedy would not have caught it, because
all three are internally self-consistent and only disagree with each other.
Patching at dispatch time, as this run did, is the workaround, not the fix.
