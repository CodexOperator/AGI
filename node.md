---
id: hypothesis:g1314211-copilot-spawn-registers-its-hooks-in-copilots-own-config
mint_id: 368e3c6e2c6f46149dba7859e950e109
type: hypothesis
parents:
  - goal:g1.31.4.2.1.1
next_edges: []
edited_by: director-general-4
scaffold_hash: 716925ce5b9e5ebd
season: 2
tags:
  - parked
testable_claim: on a faked copilot config home, the spawn path writes a hooks config carrying exactly the template [hooks] sessionStart and userPromptSubmitted commands, read back by a test from the written file
title: a copilot-cli spawn writes the template hooks into copilot own hooks config
town: core
---
# hypothesis:g1314211-copilot-spawn-registers-its-hooks-in-copilots-own-config

## Measured
- lineage tip 4620846a3f (merge-up with SM): extensions/agi/templates/harness/copilot-cli.toml `[hooks]` declares sessionStart = cc-session-start.sh and userPromptSubmitted = the meter; copilot_cli_adapter.py `hook_events()` (:87) reads the table and `hook_lines()` (:98) PRINTS the lines -- nothing writes them into copilot's own hooks configuration, so a live copilot session runs neither (Sonnet 5.5 lineage review, 18:5xZ 09-30: conjunct 5 met in name only).
- tests test_copilot_hooks_parity.py / test_copilot_hook_argv_runnable.py read the TEMPLATE, not a written copilot config.

## CLAIM
A copilot-cli spawn (the adapter's spawn/prepare path) writes the `[hooks]` table's commands into copilot's own hooks config, in copilot's documented shape, under the spawned session's config home, from `hook_events()` -- one list; a test fakes the config home and reads the WRITTEN file.

## Dispatch line
config-max: the config-home location and file name are template cells in copilot-cli.toml (never literals in the adapter) / template-max: the hooks table stays the one source / code: the writer in the adapter's spawn path.

## FALSIFIERS
1. The written copilot hooks config (tmp config home) lacks either command, or carries a command not in the template table.
2. A second hook list appears in the adapter.
3. The claude-code / pi hook tests change.

## TESTS
test_copilot*.py + a new test_copilot_hooks_registered row + test_bin_help_smoke.py, --basetemp under /tmp.

## FILE SCOPE
extensions/agi/bin/adapters/copilot_cli_adapter.py, extensions/agi/templates/harness/copilot-cli.toml, extensions/agi/tests/test_copilot*.py.

## CEILING
1 kid · <= 20 prod lines · <= 40 test lines · pi-free after 21:00Z.
