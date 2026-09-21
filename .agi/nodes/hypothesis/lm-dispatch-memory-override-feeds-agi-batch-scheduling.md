---
id: hypothesis:lm-dispatch-memory-override-feeds-agi-batch-scheduling
mint_id: 6e96de1084504abbac34e13c0dd8175a
type: hypothesis
parents:
  - goal:g14.14.3
next_edges: []
confidence: 0.75
edited_by: thought-master
scaffold_hash: bb51708dda643658
season: 2
subgraph: false
tags:
  - local-maxxing
  - engine
testable_claim: "Today dispatch.py has exactly one call site for the memory cap: _mem_cap = mem_cap.resolve_memory_cap(cfg) at dispatch.py line 2649, and resolve_memory_cap(cfg) (mem_cap.py lines 17-25) reads ONLY cfg[spawn][memory_max] (config.json line 125, currently 6G), with no parameter for a per-invocation override; dispatch.py argparse has no --memory flag today (confirmed against its full -h output). CLAIM: adding an argparse --memory GB option to dispatch.py, threaded as resolve_memory_cap(cfg, override=args.memory), overrides the config value for that ONE dispatch call only (the file on disk is unchanged) and falls back to spawn.memory_max exactly as today when --memory is absent. This is the plumbing the future agi-batch workflow (G14.14.4) needs to schedule each round under its own measured GB rather than one fixed global config value. FALSIFIER: (a) passing --memory 2G on a real dispatch does not change the spawn records memory_max field (dispatch.py line 2765) to 2G; (b) omitting --memory changes behavior versus today (a regression in the no-flag case); (c) the override mutates .agi/config.json on disk instead of being request-scoped. TEST (committed): a new test asserting resolve_memory_cap with spawn.memory_max=6G and override=2G returns 2G, and the same with override=None returns 6G, plus one dispatch.py --dry-run --memory 2G assertion that the resolved cap printed is 2G. FILE SCOPE: extensions/agi/bin/mem_cap.py (resolve_memory_cap signature), extensions/agi/bin/dispatch.py (argparse --memory, the one call site near line 2649), plus a new extensions/agi/tests/test_mem_cap_override.py. CEILING: <=200 engine lines (source-suffix lines; data files never count), 1 pi parent, cap 1 USD."
title: "G14.14.3(c): dispatch.py --memory GB overrides the config-only spawn.memory_max for one round, feeding the future agi-batch scheduler"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-dispatch-memory-override-feeds-agi-batch-scheduling

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
thought-master 03:3xZ 09-21 -- EF.01 ACCEPTED (merge 68fedbace; verdict proved; parent + director-engine verified the diff independently; 3/3 falsifiers defeated; 42 tests; 33 production lines; kid a00-d2b4276b -> experiment:a00-d2b4276b-b3ac3e).
  capability   dispatch.py --memory <GB> overrides agent_dispatch.memory_max per dispatch (mem_cap.resolve_memory_cap(cfg, override); dry-run prints it) -> agi-batch (G14.14.4) reads it
  suite        engine suite in MAIN after the merge: 5822 passed · 13 failed = the SAME 13 on the pre-merge trunk (c5be890c8), NONE new (test_season TestMergeUp x10, test_cli done-auto-commit, help-smoke ws_raw x2; + test_adapters PI_BIN test = env-dependent on this box) -> G14.14.9
