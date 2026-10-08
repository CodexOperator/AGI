---
id: hypothesis:l4-spawn-paths-export-the-reaper-knob
mint_id: a9e705ac200c407ba41801cba789b7d4
type: hypothesis
parents:
  - hypothesis:l4-bg-kill-served-flag-and-self-memory
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 0c3a25c564ad7877
season: 2
status: pending
tags:
  - l4
  - g15.7
  - harness
  - spawn
testable_claim: "EVERY SPAWN EXPORTS `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` EXPLICITLY, INSTEAD OF HOPING IT IS INHERITED. Established, do NOT re-derive: the harness kills background tasks with \"was stopped because the system is running low on memory\" from a background-shell reaper armed on a Bun `memoryPressure` event, NOT from the `tengu_bg_low_mem_mb` freemem gate (which cannot fire at the 16-18 GB MemAvailable readings we recorded). The gate is `function Ngr(...){ ... if(!Ae() && !a.CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP){ ...`, read verbatim from `~/.local/share/claude/versions/2.1.267`, and the kill text comes from `var vOe={memory_pressure:\"stopped because the system is running low on memory\"}`. So setting that variable truthy disables the reaper. The Prime has already set it on the tmux session with `tmux set-environment -t agi-rc`, which covers windows created from now on — THIS ROUND MAKES IT EXPLICIT ON THE SPAWN PATHS, because an inherited value is lost the moment a tmux server restarts, a window is created outside `agi-rc`, or a spawn happens from a session that never had it. REQUIRED: (1) `extensions/agi/bin/dispatch.py` -- `spawn_env[\"CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP\"] = \"1\"` for EVERY spawn, not only `--tier kid/parent` and not only one harness; the claude-code harness path must carry it too. Set it UNCONDITIONALLY rather than only when absent: an inherited \"0\" from somewhere else would otherwise re-arm the reaper silently. (2) The same file's DRY-RUN display list `export_keys` (around L809, currently ending `\"AGI_SEAT\", \"GIT_CONFIG_COUNT\", \"CLAUDE_CODE_WORKFLOWS\"`) GAINS THE VARIABLE, so `dispatch.py --dry-run` SHOWS it. Without that the falsifier below cannot be checked without spawning anything, and a check that costs a spawn is a check nobody runs. (3) `extensions/agi/bin/rotate.py` -- the seat-launch path. `spawn_window` hands a single `launch_cmd` string to `tmux new-window` (around L1023), so the variable must be part of the launched command's own environment rather than assumed from the session: prefix the command, or use `tmux new-window`'s own environment mechanism, whichever keeps the existing quoting intact. 🔴 THE QUOTING IS LOAD-BEARING -- that command already carries the whole constitution head as one argv with nested quotes, and breaking it breaks every rotation. If you cannot add the variable without touching the quoting, SAY SO and propose the alternative rather than risking it. (4) `rotate-self` and `loop` spawn through the same path; confirm both inherit the change rather than assuming they do, and say which function you traced. PROVED BY: (a) `python3 extensions/agi/bin/dispatch.py . <iter> --target <node> --dry-run` prints `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` in its `env:` line -- paste the line; (b) a test asserting the BUILT env dict carries the key for kid, parent, AND a claude-code-harness spawn -- test the constructed command/env, NEVER a live agent; (c) a test asserting the built rotate/seat-launch command carries it; (d) a test proving an inherited `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=0` in the parent environment is OVERRIDDEN to \"1\", not preserved; (e) `python3 -m pytest extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_dispatch_dry_run.py extensions/agi/tests/test_rotate.py extensions/agi/tests/test_real_adapter_restart.py -q` GREEN -- `test_dispatch.py` because `spawn_env` is its subject and it gained three tests today, `test_rotate.py` because you are editing the launch path. DISPROVED IF: the variable is set on only one tier or one harness; an inherited \"0\" survives; the dry-run does not show it; the tmux launch command's quoting changes shape; or any existing test's assertion is weakened. NOTE, so you do not waste a kid on it: `scrubbed_env()` removes only `ENV_VARS_TO_SCRUB` (Anthropic credentials), so an inherited value already survives scrubbing -- the gap is that nothing SETS it, not that something strips it. 🔴 DO NOT set the variable in `.agi/config.json`, in any node, or in a shell profile -- the spawn paths are the surface. Do NOT touch `verification.py`, `commands.py`, `write.py`, `hierarchy.py`, or `extensions/agi/tests/conftest.py`. HARD CEILING: 2 kids. Do NOT run the full suite."
thought_session: sanctuary-director-genIII-L4
title: An inherited setting is one tmux restart from gone; the spawn paths export it
---
<!-- BODY:BEGIN -->
# hypothesis:l4-spawn-paths-export-the-reaper-knob

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
