---
id: goal:s8
mint_id: d3ded88fb3b34d52beb8eb38ec6bf973
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: season.py
goal_id: S8
goal_kind: short-term
heading_level: 2
origin: goals-doc
season: 1
seeds:
  - mvp:zoom-runtime-contract
status: complete
tags:
  - goal
  - root
  - short-term
thought_session: season
title: "S8: `zoom.py` bakes the pi-runtime completion contract into the kid context"
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Marked complete in the 2026-09-01 sweep, on the live path rather than on the
tests: `dispatch.py:101` passes `--runtime pi` explicitly when it builds the
zoom command, so a pi kid can no longer be handed the Claude Code contract by
`zoom.py::default_runtime` guessing from the presence of a `cc_dispatch` block.

How it was found is the part worth keeping: both kids on the 2026-08-31 live
run READ the contradiction in their own context — told "do not call cli.py" in
the one runtime where `cli.py done` is how the manifest closes — reported it,
and correctly ignored their own instructions. The engine was wrong and the
agents caught it, which happened four more times on 2026-09-01.
<!-- THOUGHT:END -->