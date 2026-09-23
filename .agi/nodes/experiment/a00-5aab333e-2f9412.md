---
id: experiment:a00-5aab333e-2f9412
mint_id: a4e646c2e428422abe49f5532c43e8aa
type: experiment
parents:
  - hypothesis:the-last-engine-clis-join-the-choice-surface
next_edges: []
confidence: 0.92
edited_by: a00-e65928ba
evidence_runs:
  - experiment:a00-5aab333e-2f9412
loop: hypothesis:the-last-engine-clis-join-the-choice-surface@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - "auth: commands.propose(root, boxes.py: | mem_cap.py: | ws_raw.py: | pi_trajectory.py:) refused by name -- \"not proposable: <reason>\"; branches.py: returned its argv"
  - "gate: introspected verb set == manifest+excluded set for all 11 (spawn_gate 2 verbs, others 1); render_manifest byte-identical twice; no token starts with /; no home/root/box label"
  - "wire: the 5 __main__-only CLIs failed parser capture on the base (probe35: boxes.py req=True -> fell to req=False); after _drive_module(as_main=True) _introspect_cli returns real dests (branches names, completion root+node_id)"
production_lines: 29
profile: balanced
role: kid
scaffold_hash: 01c1bc16d11b7bba
season: 2
title: EF.54 harness captures the 11 parser-outside-main engine CLIs
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5aab333e-2f9412

## Experiment

Extend the manifest introspection HARNESS so the 11 engine CLIs whose parser
lives outside a plain module-level `main()` are captured, then declare their
verbs in `command:commands` so all 70 engine CLIs are covered.

Probe (parent table) had 11 uncovered CLIs. Measured shape, re-read from each
file's OWN argparse:

| CLI | where the parser lives | introspected verbs |
|---|---|---|
| boxes.py, mem_cap.py, migrate_channel.py | `__main__` block, bare parser | `''` (no args) |
| branches.py | `__main__` block | `''` (positional `names`) |
| completion.py | `main` defined INSIDE `__main__` | `''` (`root`, `node_id`) |
| geometry_config.py | `_main(argv)` | `''` (`root`) |
| spawn_gate.py | `_cli(argv)` | `check`, `rules` |
| towns.py | `_main(argv)` | `''` (`root`, `tuples`) |
| ws_raw.py | `_parse_args` is HAND-ROLLED argv | parserless |
| pi_edit_forgiveness.py, pi_trajectory.py | manual argv | parserless |

Deviation from the parent table: `ws_raw.py` is genuinely parserless (its
`_parse_args` scans argv by hand; the `async` is only its `main`), so it joins
`_PARSERLESS_CLIS` rather than the parser path.

Harness: one new `_drive_module(path, modname, as_main)` in
`test_commands_manifest.py` used by BOTH `_introspect_cli` and
`_cli_arg_specs`. It runs the module once normally (drives `main`/`_cli`/
`_main`/`_parse_args` under the spy), and, only if no parser was captured,
re-execs with `__name__ == "__main__"`. Plain `exec` is used because
`SourceFileLoader.exec_module` refuses a module whose `__name__` differs from
the loader's (`ImportError: loader for X cannot handle __main__`). The spy
still raises before parse, so no verb runs.

Declaration: 6 proposable read verbs (`branches.py:`, `completion.py:`,
`geometry_config.py:`, `spawn_gate.py:check`, `spawn_gate.py:rules`,
`towns.py:`) + 5 excluded by name with a reason (`boxes.py:`, `mem_cap.py:`,
`migrate_channel.py:` bare-parser libraries; `ws_raw.py:` relay;
`pi_edit_forgiveness.py:`, `pi_trajectory.py:` manual argv). Placement
overrides: `branches.py:.names` and `towns.py:.root` positional;
`spawn_gate.py:check` `--id`/`--set`/`--season-parent`; `parents` reuses the
existing global `--parent`.

## Evidence

Scratch probe `.agi/sessions/iter-EF.54/a00-5aab333e/probe.py` printed the
expected verb/dest set for all 11 (and `{'': set()}` for the 3 parserless).

```
boxes.py {'': set()}          branches.py {'': {'names'}}
completion.py {'': {'root','node_id'}}   mem_cap.py {'': set()}
migrate_channel.py {'': set()}   geometry_config.py {'': {'root'}}
spawn_gate.py {'check': {node_type,parents,node_id,root,sets,
                         no_spawn_gate,season_parents,current_season},
               'rules': {'root'}}
towns.py {'': {'root','tuples'}}
ws_raw.py / pi_edit_forgiveness.py / pi_trajectory.py  PARSERLESS
```

Tests (the two files named in the brief, plus the cover set):

```
python3 -m pytest extensions/agi/tests/test_commands_manifest.py -q
  -> 119 passed
python3 -m pytest extensions/agi/tests/test_commands.py \
  extensions/agi/tests/test_graphweb.py \
  extensions/agi/tests/test_bin_help_smoke.py -q
  -> 124 passed, 12 skipped
```

Production lines (`git diff --numstat`, test file excluded):
`.agi/nodes/.geometry/commands.md` 29 added, 0 removed — under the 40 ceiling.
The test-file edit (80+/32-) is excluded by the brief.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review EF.54 (a00-e65928ba) ACCEPT proved. (1) The brief said "follow EF.45 exactly ... the drift test introspects argparse at TEST time" and named 11 parser-outside-main CLIs. (2) The diff carries exactly what machine does: `_drive_module` in test_commands_manifest.py is shared by `_introspect_cli` and `_cli_arg_specs`; `exec` with `__name__="__main__"` (not SourceFileLoader, which refuses a name mismatch) fires the guarded block under the parse_args spy; commands.md gains 6 manifest + 6 excluded keys with placement overrides. My probes reproduce it: 4 non-proposable verbs refused by name with reason, branches.py: returns argv, introspected==declared for all 11, manifest byte-identical, no abs/box token. (3) Near miss: declaring boxes/mem_cap/migrate_channel as proposable single-verb entries reading their bare `--help` parser -- satisfies "every verb declared" and loses the safety that they do no work; the kid excluded them by name instead. (4) Deviations accepted: parent table called ws_raw async, kid measured `_parse_args` as hand-rolled -> parserless, which is honest; kid also extended `_cli_arg_specs` unprompted because the placement test would otherwise fail -- correct, the brief under-named the two introspectors.
<!-- THOUGHT:END -->

## Agent Notes
Extended _drive_module in test_commands_manifest.py to capture parsers under __main__, _cli/_main, and async; declared the 11 parser-outside-main CLIs (6 proposable read verbs, 5 excluded by name); 119+124 tests pass; 29 production lines.
