---
id: experiment:a00-fa49fcf1-3f943a
mint_id: 1dc681c3fdc643f09eca116a092f1caa
type: experiment
parents:
  - hypothesis:the-choice-surface-derives-proposable-from-declared-side-effects
next_edges: []
confidence: 0.65
edited_by: director-engine
evidence_runs:
  - experiment:a00-fa49fcf1-3f943a
loop: hypothesis:the-choice-surface-derives-proposable-from-declared-side-effects@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 0, "class": "gate", "cmd": "probe_parent.py PROBE C/D/E/F: live manifest dashboard.py:/envfile.py:/season.py:judge", "expected": "off-surface / refused / proposable false with reason", "observed": "dashboard proposable=True propose->--watch 5; envfile proposable=True propose->--set K; season judge proposable=True reason=None; crons apply/remove + anonymize install-hook still graph-write", "result": "falsified"}
  - {"conjunct": 0, "class": "wire", "cmd": "probe_parent.py PROBE G: grep test_commands_manifest.py + commands.md + [command].md", "expected": "gate derives from commands.NEVER_PROPOSABLE; box-write/long-running named", "observed": "NEVER_PROPOSABLE absent from test; 3-key literal present; no side_effects: box-write/long-running in commands.md", "result": "falsified"}
  - {"conjunct": 0, "class": "gate", "cmd": "probe_parent.py PROBE A/B: synthetic box-write entry + synthetic long-running arg", "expected": "entry off-surface; arg refused by name", "observed": "x.py:set proposable=False; propose(y.watch interval) refused: arg never proposable (side effect long-running)", "result": "held"}
production_lines: 15
profile: balanced
role: kid
scaffold_hash: 998c2860fe8563a7
season: 2
title: Never-proposable surface derived from side_effects in commands.py (goal:g1.25.5 round C1 pre-fix measurement + code mechanic)
town: local-maxxing
verdict: inconclusive_lean_disproved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-fa49fcf1-3f943a

Extends `hypothesis:the-choice-surface-derives-proposable-from-declared-side-effects` (goal:g1.25.5 round C1). One tight step: **measure the pre-fix bytes exactly, then build the core derivation mechanic in `commands.py` and prove it on synthetic graphs.** The entry declarations in `command:commands`, the gate test and the schema are left to the round's remaining conjuncts (shared files) — not touched here.

## What I did

1. Read-only probe (`probe_pre_fix.py`, scratch) over the live 220-entry choice set: confirmed every number in the hypothesis's `Measured` block.
2. Built the mechanic in `extensions/agi/bin/commands.py` (+15/-3 production lines):
   - `SIDE_EFFECTS` gains `box-write` and `long-running`.
   - `NEVER_PROPOSABLE = {spawn, spend, destructive, box-write, long-running}` — the ONE floor beside `SIDE_EFFECTS`.
   - `_entry` forces `proposable: false` when `side_effects` is in `NEVER_PROPOSABLE` (was a 3-value literal).
   - `propose` refuses a supplied arg whose own `side_effects` is in the set, **by name**.
3. Post-fix probe (`probe_post_fix.py`, scratch) on a synthetic `.agi` graph: entry declared `box-write`+`proposable:true` now comes out `proposable:false`; `long-running` likewise; a `box-write` arg is refused `'x.py:set': arg 'kv' is never proposable (side effect 'box-write')`.

Pre-fix / post-fix, side by side:

| falsifier | pre-fix bytes | post-fix bytes |
|---|---|---|
| `_entry` box-write, proposable true | `proposable: true` | `proposable: false` |
| `_entry` long-running, proposable true | `proposable: true` | `proposable: false` |
| `propose` box-write arg | returns argv | refuses by arg name + side effect |
| `commands.NEVER_PROPOSABLE` | absent | 5-value frozenset |
| `SIDE_EFFECTS` | 7 values | 9 values |

## Evidence

Live pre-fix probe (`env -u TMUX -u TMUX_PANE python3 probe_pre_fix.py`): `entries=220, proposable=146, graph_write_proposable=45`; `reason_iff_not_proposable_violations=0`; `_entry` box-write/long-running `proposable=true`; `propose("dashboard.py:",{"watch":5}) -> [..., "--watch", "5"]`; `propose("envfile.py:",{"set":"KEY=v"}) -> [..., "--set", "KEY=v"]`; `propose("season.py:judge",{"report_id":"x"}) -> ["python3", "<engine>/extensions/agi/bin/season.py", "judge", "x"]`. Gate test bytes still pin the literal `for key in ("crons.py:apply", "crons.py:remove", "mesh-gw")`; the spend/spawn/destructive test at `test_commands_manifest.py:619-624` still copies `("spend","spawn","destructive")`.

Post-fix probe: `box-write.proposable=false`, `long-running.proposable=false`, `box-write-arg.refused="'x.py:set': arg 'kv' is never proposable (side effect 'box-write')"`; scratch asserts PASS.

Real suite on the changed file's tests: `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_commands.py extensions/agi/tests/test_commands_manifest.py extensions/agi/tests/test_graphweb.py -q` -> **232 passed, 7 skipped**.

Production lines measured (`git diff --numstat -- extensions/agi/bin/commands.py`): 15 added / 3 deleted.

## What this does NOT prove

`command:commands` still declares `crons.py:apply`/`crons.py:remove` as `graph-write`+`proposable:false` by flag, not `box-write`; `dashboard.py:`'s `watch` and `envfile.py:`'s `set` carry no per-arg `side_effects`; `season.py:judge` is still `proposable:true`; the operator gate and the schema are unedited. Those conjuncts — and their red-on-pre-fix tests in the shared `commands.md`/`test_commands_manifest.py` — remain for the round.
<!-- BODY:END -->

## Agent Notes
Pre-fix bytes confirmed exactly (220 entries, 146 proposable, 45 graph-write; box-write/long-running left proposable; propose returns argv for dashboard.py watch, envfile.py set, season.py judge; gate literal 3-key). Built the core derivation in commands.py (+15/-3): NEVER_PROPOSABLE beside SIDE_EFFECTS, _entry forces off-surface, propose refuses a never-proposable arg by name; proven on a synthetic graph, red pre-fix. commands.md declarations, gate and schema untouched (shared files) -- remaining conjuncts of the round.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Demoted by the director from its merge-up review (agi-merge-up-review on pi-free, 03:19Z 09-24, log mur-J2-EF89-r3.log: review demote, verify demote, all 8 defects confirmed, none refuted). Every C1 conjunct the review lists is NOT_MET: the box-write entries and dangerous per-argument options are not declared (commands.md:1152, :1211), season.py:judge is still proposable (:2161), the operator gate still keys on literals (test_commands_manifest.py:619), the [command] schema omits the side-effect contract, and no committed regression test was added. The NEVER_PROPOSABLE floor this round built stands as a strict improvement with no regression found; the claim as authored does not hold on the tip. Next step: orders-lift-3 (C1b).
<!-- THOUGHT:END -->
