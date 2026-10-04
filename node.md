---
id: hypothesis:grok-bot-live-bin-exists
mint_id: fa92514b2d7545c4815e2972bd3893c4
type: hypothesis
parents:
  - goal:g7.25
next_edges: []
confidence: 0.4
edited_by: director-thought-2
model: grok-4.6
role: director
season: 2
tags:
  - grok-bot
  - adapter
  - encryption-town
testable_claim: "On encryption-town, grok-bot --help documents -p/--single and -m/--model; grok_bot_adapter.build_command emits that flag shape; and adapters.resolve_bin on the live harnesses.grok-bot row returns an existing executable path."
title: "Grok-bot live row bin is executable on encryption-town, and the stub argv is a documented grok-bot invocation"
town: core
---
# hypothesis:grok-bot-live-bin-exists

## Measured
- g7.25.1–.3 complete. Parent g7.25 still horizon, unassigned. This seat is a live grok-bot capsule on encryption-town (engine.v4).
- F1 `adapters.load("grok_bot")` succeeds; NAME grok-bot; REQUIRED names present (build_command, child_env, is_alive, restart, needs_credential).
- F2 `adapters.resolve(cfg, "grok-bot")` returns the live row (adapter grok_bot, bin `~/.npm-global/bin/grok-bot`, models kid grok-4-fast / parent grok-4).
- F3 `grep` dispatch.py for grok-bot|grok_bot = 0 hits.
- F4 is_alive(self pid) True; needs_credential False; restart callable. pytest absent on this uid; tests not re-run.
- `grok-bot --help` (same binary as `grok`): `-p, --single <PROMPT>` "Single-turn prompt. Prints the response to stdout and exits"; `-m, --model <MODEL>`.
- Adapter docstring still says the flag shape is a stub until `--help` is read (grok_bot_adapter.py build_command).

## CLAIM
C1. `grok-bot --help` documents `-p, --single <PROMPT>` and `-m, --model <MODEL>`.
C2. `build_command` with a resolving harness emits `<bin> --model <models[tier]> -p <prompt>` (the documented pair).
C3. `resolve_bin` on the live `harnesses.grok-bot` row returns a path that exists and is executable on this box.
Verdict. C1 AND C2 AND C3 -> proved: a dispatch spawn using the live row would start grok-bot with a documented argv. Any failure -> disproved. Void: grok-bot not on PATH, or load/resolve of the row itself fails.

## Dispatch line
config-max: the live `harnesses.grok-bot.bin` cell is the load-bearing path (g7.25.2). template-max: none. code: none this round (no adapter edit, no config write). Measurement only.

## FALSIFIERS
- `--help` lacks `-p/--single` or `-m/--model` -> C1 disproved
- `build_command` (with a resolving bin) emits a flag `--help` does not name -> C2 disproved
- `resolve_bin(live row)` raises or returns a non-existent path -> C3 disproved
- load or resolve of the row fails -> void

## TESTS
No new test file. Neighbourhood: extensions/agi/tests/test_grok_bot_adapter.py (existing; pytest absent this uid). Commands are the probes on the experiment node.

## FILE SCOPE
the hypothesis, experiment, and verdict nodes. Not `.agi/config.json`. Not `grok_bot_adapter.py`.

## CEILING
0 production lines, one builder, CPU, 0 USD. Wall cap 5 min. No spawn of a grok session beyond `--help` and a 4 s `-p` timeout.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-thought-2 16:50Z 10-04 (date -u): owner go, encryption-town only. Claimed unassigned g7.25. The practice-run children closed the REQUIRED surface; this hyp asks the remaining g7.25 target ("argv that starts one agent") against the live row on this box. Near miss: first --help head hid `-p`; full help names `-p, --single`. Did not take g7.30 (helper / land on main) and did not write the bin cell.
<!-- THOUGHT:END -->
