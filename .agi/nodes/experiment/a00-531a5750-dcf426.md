---
id: experiment:a00-531a5750-dcf426
mint_id: 32e681ef0e9c46838ab4689fa816fb7f
type: experiment
parents:
  - hypothesis:the-last-engine-clis-join-the-choice-surface
next_edges: []
confidence: 0.9
edited_by: a00-e65928ba
evidence_runs:
  - experiment:a00-531a5750-dcf426
loop: hypothesis:the-last-engine-clis-join-the-choice-surface@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - "auth: commands.propose refused by name with reason for backfill-mint-ids.py:, decompose-engine.py:, derive-commands.py:, failures.py:ledger, failures.py:sensei, glitch_master.py:format-record, graphweb.py:serve, inject.py: (all \"not proposable: <reason>\")"
  - "gate: introspected verb set == manifest+excluded set for all 12 (failures 3 verbs, frontier 1, glitch 1, graphweb 1, others 1); manifest suite 143 passed"
  - "wire: the 6 proposable read verbs (briefing, dashboard, drift_check, frontier.py:list, grid_coverage_check, failures.py:rates) returned an argv through propose; the 8 excluded keys carry proposable=false and a non-empty reason"
production_lines: 32
profile: balanced
role: kid
scaffold_hash: 3ef2a3938548acdd
season: 2
title: "CLI GROUP D: the last 12 plain-main CLIs declared, coverage green"
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-531a5750-dcf426

## Experiment

CLI GROUP D — the last 12 engine CLIs whose parser is a plain module-level
`main`. The EF.54 kid 1 harness (`_drive_module`, spy-based introspection)
already captures them, so this round is DATA plus one `_LISTED_CLIS` append.
No CLI was imported or run for its verbs: `_introspect_cli` reads each CLI's
own argparse at test time.

```
input   12 CLIs, 14 verbs total, dests+choices read off each argparse
step 1   append GROUP D to _LISTED_CLIS (new block, never folded)
step 2   declare read verbs in `manifest:` (6), side-effect verbs in
         `excluded:` by name with a reason (8)
step 3   add placement deviations: positional roots + `--in` / `--iter`
output  143 passed manifest suite; 124 passed / 12 skipped CLI+web+help suite
```

| CLI | verb | declared | side_effects | proposable |
|---|---|---|---|---|
| briefing.py | `''` | manifest | read | true |
| dashboard.py | `''` | manifest | read | true |
| drift_check.py | `''` | manifest | read | true |
| frontier.py | list | manifest | read | true |
| grid_coverage_check.py | `''` | manifest | read | true |
| failures.py | rates | manifest | read | true |
| backfill-mint-ids.py | `''` | excluded | graph-write | false |
| decompose-engine.py | `''` | excluded | graph-write | false |
| derive-commands.py | `''` | excluded | graph-write | false |
| failures.py | ledger | excluded | graph-write | false |
| failures.py | sensei | excluded | graph-write | false |
| glitch_master.py | format-record | excluded | graph-write | false |
| graphweb.py | serve | excluded | spawn | false |
| inject.py | `''` | excluded | graph-write | false |

Placement deviations added (the rest resolve from the `{defaults: true}`
convention): `briefing.py:.root`, `frontier.py:list.cmd`, the three
`failures.py:*.root` positionals, the three `failures.py:*.in_path` -> `--in`,
`glitch_master.py:format-record.iter_data` -> `--iter`,
`inject.py:.nodes_dir` positional.

## Evidence

Probes run (all from the worktree root):

```
python3 -m pytest extensions/agi/tests/test_commands_manifest.py -q
  -> 143 passed in 64.65s
python3 -m pytest extensions/agi/tests/test_commands.py \
    extensions/agi/tests/test_graphweb.py \
    extensions/agi/tests/test_bin_help_smoke.py -q
  -> 124 passed, 12 skipped in 13.28s
```

Gate: `test_every_listed_cli_verb_is_declared_or_excluded` compares the 14
introspected verbs against the manifest+excluded keys for all 12 CLIs --
`missing=[]`, `extra=[]`. Wire: `test_declared_args_are_still_accepted_by_the_cli`
and `test_declared_placement_matches_each_cli_introspected_at_test_time`
re-introspect at test time; `test_every_proposable_entry_accepts_a_full_supply_of_its_args`
and `..._lands_every_supplied_value_or_refuses_by_name` drive `propose` over
every proposable entry. Auth: `test_propose_never_imports_a_cli_or_touches_argparse`
and `test_no_spend_spawn_or_destructive_entry_is_proposable` -- propose
imports no CLI and the `spawn` entry (`graphweb.py:serve`) is non-proposable.

`commands.manifest('.agi')` renders 203 entries, two renders byte-identical;
no absolute path or box value appears.

## Measurement

`git diff --numstat -- .agi/nodes/.geometry/commands.md` -> `32 0`.
Production lines 32, below the 40 ceiling and far below the 2x stop.

## Agent Notes
CLI GROUP D: 12 plain-main CLIs, 14 verbs declared/excluded in command:commands, placement deviations added, _LISTED_CLIS appended; manifest suite 143 passed, CLI+web+help suite 124 passed/12 skipped; propose imports/executes nothing

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review EF.54 (a00-e65928ba) ACCEPT proved. (1) The brief said "your slice is 12 CLIs whose parser is a plain module-level main ... your work is DATA plus the _LISTED_CLIS append". (2) The diff carries it: 6 manifest read verbs + 8 excluded graph-write/spawn verbs in commands.md, 10 placement overrides (positional roots, --in, --iter), and one appended _LISTED_CLIS block of 12. My probes reproduce it: 8 non-proposable verbs refused by name with reason, 6 proposable return argv, introspected==declared for all 12, manifest suite 143 passed. (3) Near miss: marking failures.py:ledger or graphweb.py:serve proposable because their verbs are "just reads" -- ledger has --write-node and serve binds a port; both are excluded, which is the safe call. (4) No deviation; the kid excluded derive-commands/decompose-engine/inject as graph-write, which is the closest taxonomy cell for a repo/graph writer.
<!-- THOUGHT:END -->
