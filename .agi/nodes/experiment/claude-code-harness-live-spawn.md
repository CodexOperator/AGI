---
id: experiment:claude-code-harness-live-spawn
mint_id: 38f020b7b4da41c493cb7b3fea5b223f
type: experiment
parents:
  - hypothesis:a01-391172f1-7157cf
next_edges: []
confidence: 0.9
edited_by: parent agent (Claude Fable 5.1) implementing goal:g4.6
evidence_runs:
  - hypothesis:a00-9bcc560d-7dd08c
  - hypothesis:a01-391172f1-7157cf
scaffold_hash: 191d3ed93b8fe7f5
tags:
  - experiment
  - harness
  - claude-code
testable_claim: dispatch.py --harness claude-code --tier kid spawns a real claude -p process per slot that reads its zoom context, fills its scaffolded node under .agi/nodes/, runs cli.py done, exits, and returns its spawn_budget lease -- with dispatch.py unedited
thought_session: 2447cd96-1371-4b5a-b4c4-655b1e19b44b
title: Claude code harness live spawn
verdict: proved
---
# experiment:claude-code-harness-live-spawn

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
Implemented extensions/agi/bin/adapters/claude_code_adapter.py (goal:g4.6; the week the pi harness went dark on the OpenRouter weekly budget). build_command spells the whole brief -- zoom context, tier brief, skill prompt -- as ONE file per agent (`<sess>/system-prompt.md`) passed once via `--append-system-prompt-file`, because a one-turn probe on 2026-09-03 showed repeated `--append-system-prompt` is last-wins (two flags "codename ALPHA" / "colour BLUE" answered `UNKNOWN/blue`). The closing line is fenced behind `--` because `--tools`/`--allowedTools`/`--add-dir` are variadic and swallow a trailing positional prompt. Tools are a closed list with no Agent (`--tools` + the same list in `--allowedTools`); git write verbs are refused via `--disallowedTools Bash(git commit:*)` etc. (probe: `git commit` DENIED and recorded in permission_denials, the following echo still ran); `--strict-mcp-config` so a kid does not inherit the director MCP servers; `--add-dir <repo root>` because the child cwd is `.agi/`; `--output-format stream-json --verbose` so a killed agent still leaves a log. child_env hands back the ANTHROPIC_*/CLAUDE_CODE_*/CLAUDECODE names the shared pi scrub removes (the subscription IS the sanctioned path here) and never hands down OPENROUTER_PROVISIONING_KEY from any source. model_args: models[tier] -> --model, missing tier is a KeyError, never a fallback. is_alive and restart implemented like pi. dispatch.py NOT edited. LIVE RUN 2026-09-03 21:47: `dispatch.py /home/ubuntu/work/agi 1036 --harness claude-code --tier kid --target goal:g4.6 --level small` with spawn.parallel=2 spawned pids 3820742 and 3823446 (`claude -p --model claude-sonnet-5 ...`, cwd /home/ubuntu/work/agi/.agi, 6 tools, mcp=[]); both read their context, wrote their scaffolded nodes (hypothesis:a00-9bcc560d-7dd08c, USD 0.35; hypothesis:a01-391172f1-7157cf, 13 turns, USD 0.26), ran `cli.py done`, and exited; spawn_budget live_count went 2 -> 0; permission_denials 0. Session artefacts: .agi/sessions/iter-1036/<agent>/{context.md,system-prompt.md,output.log,agent.json}. Tests: tests/test_claude_code_adapter.py (22, fixture-based); reintroducing the pi spelling turned test_every_brief_segment_lands_in_one_system_prompt_file red with `AssertionError: last-wins: segments would be lost`; full suite after the last edit: 1452 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1, minted by the parent that wrote the adapter. Parent is hypothesis:a01-391172f1-7157cf rather than goal:g4.6 as the brief asked: [experiment].md removed `goal` from allowed_parents on 2026-09-01 (goal:s22) and the spawn gate would have refused; a01 is the CC kid own claim about this adapter, so the run that spawned it is literally the experiment executing it. `proved` is scoped to what was measured -- a Claude Code kid spawns through the shared path, writes its node, exits, and returns its lease -- not to the quality of the kid nodes (both verdicts are inconclusive_lean_proved; a00 reported a bare-integer evidence_runs and was resolved to zero). Left open, deliberately outside this file domain: dispatch mints an OpenRouter credential for a CC kid that never uses it; manifest.json still says running after agent.json says done (pre-existing); kids inherit the user hooks, and extensions/agi/hooks/cc-session-start.sh is mode 644 so every kid logs a permission-denied SessionStart hook error; _reap_one passes harness={} to restart, so a restarted kid runs on the CLI default model for pi and CC alike.
<!-- THOUGHT:END -->
