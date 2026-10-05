---
id: hypothesis:grok-bot-restart-degrades-to-none
mint_id: 226d9df1102947ab9fdd6406d86352f4
type: hypothesis
parents:
  - goal:g7.25
next_edges: []
confidence: 0.8
edited_by: director-thought-2
model: grok-4.6
role: director
season: 2
tags:
  - grok-bot
  - adapter
  - encryption-town
testable_claim: "On encryption-town, grok_bot_adapter.restart returns None (does not raise, does not spawn) when the live bin cell is missing, and when both rendered_brief and context_file are empty with a resolving bin."
title: grok-bot restart degrades to None on missing bin and on empty prompt
town: core
---
# hypothesis:grok-bot-restart-degrades-to-none

## Measured
- Owner [owner] 04:48Z 10-05: thought-lane turn; do not implement mint; council chews zygote+mint.
- g7.25 still claimed. Live bin cell missing. `$GROK_BOT_BIN` unset. Dispatch dry-run PermissionError on MAIN `.env`.
- Adapter: `restart` rebuilds argv through `build_command`; OSError/ValueError → print + return None (g4.7). Empty prompt raises ValueError by name. Missing path-shaped bin raises FileNotFoundError by name.
- Prior: restart callable only (experiment:dt2-grok-bot-env-bin-1004). F4 of g7.25 is "restart is callable" — this leaf asks the degrade arm.

## CLAIM
C1. `restart(live row, rendered_brief='hello')` with unset `$GROK_BOT_BIN` returns `None`; does not raise; no child pid; no `output.log` in sess_dir.
C2. `restart(harness bin=grok-bot, rendered_brief=None, context_file='')` returns `None`; does not raise; no child.
Both → proved. Any raise, any pid, any billed spawn → disproved. Void: load of grok_bot fails.

## Dispatch line
config-max: none. template-max: none. code: none. Measurement only. Did not spawn a grok session.

## FALSIFIERS
- C1 or C2 raises through the caller → disproved
- C1 or C2 returns a pid → disproved
- a grok process appears in sess_dir → disproved
- load fails → void

## TESTS
No new test file. pytest absent this uid. Commands on the experiment node.

## FILE SCOPE
this hypothesis, its experiment, its verdict, g7.25 seeds/thought. Not `.agi/config.json`. Not `grok_bot_adapter.py`. Not mint/zygote nodes.

## CEILING
0 production lines, one builder, CPU, 0 USD. Wall cap 5 min. No billed grok spawn.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-thought-2 04:54Z 10-05 (date -u): owner wake thought-lane. Nested under claimed g7.25 rather than a second top. Did not implement mint/zygote (council chew). Near miss: dispatch --dry-run still hits MAIN .env PermissionError; this leaf is in-process python, no dispatch.
<!-- THOUGHT:END -->
