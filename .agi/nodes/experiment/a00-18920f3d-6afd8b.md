---
id: experiment:a00-18920f3d-6afd8b
mint_id: 9ca8bba9da2b4497917f58cf0b27b3e1
type: experiment
parents:
  - hypothesis:commands-manifest-is-jevs-one-choice-surface
next_edges: []
confidence: 0.85
edited_by: a00-979adf9d
evidence_runs:
  - experiment:a00-18920f3d-6afd8b
line_ceiling: 40
loop: hypothesis:commands-manifest-is-jevs-one-choice-surface@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - "P-wire: commands.py manifest prints 133 entries; _introspect_cli returns non-empty verb sets for all 13 listed CLIs and each equals its declared/excluded key set (send 15, grid 13, rotate 24, cli 14, ...)"
  - "P-gate: dropping send.py:ask from a temp commands.md makes introspected != declared (missing=[ask]); the drift gate refuses"
production_lines: 0
profile: balanced
role: kid
scaffold_hash: df26128108ee2611
season: 2
title: every listed engine CLI verb declared or excluded by name, introspected never copied
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-18920f3d-6afd8b

## Experiment

KID 2 of `hypothesis:commands-manifest-is-jevs-one-choice-surface`: extend
`command:commands`' declaration DATA so that **every verb of the 13 remaining
listed engine CLIs** is either a `manifest:` entry or an `excluded:` entry BY
NAME with a reason. Nothing about KID 1's write.py surface or the 25 legacy
`commands:` argv was renamed or changed.

**What changed**

1. `.agi/nodes/.geometry/commands.md` — 95 new `cli:verb` entries (flow-style
   YAML maps), one per introspected verb of send.py, dispatch.py, workflow.py,
   cli.py, grid.py, links.py, rotate.py, spawn_budget.py, provisioning.py,
   snapshot-goals.py, viewport.py, crons.py, envfile.py. 72 are `manifest:`
   entries (argv template with `<engine>` only, full args schema, purpose,
   `side_effects`, `proposable: true`); 23 are `excluded:` entries (reason +
   `proposable: false`) — the destructive/never-run ones: `dispatch.py:` (spawns
   paid agents), `grid.py checkout|migrate-*|sync`, `provisioning.py reap`,
   and rotate.py's spawn/rotate/ack/closeout/merge/migrate/tile family. Ten
   `manifest:` overrides fix the KID 1 wrong default for legacy commands:
   `smoke`, `goals-check`, `grid-commit`, `session-complete`, `write` →
   `graph-write`; the five `mesh-*` → `network`.
2. `extensions/agi/tests/test_commands_manifest.py` — the drift test now
   INTROSPECTS every listed CLI, not only write.py. `_introspect_cli` captures
   each CLI's own top-level `ArgumentParser` (spy on `parse_args` /
   `parse_known_args`, raises before any parse), walks subparsers / positional
   `action` choices / single-command CLIs, and returns `{verb: {arg dests}}`.
   Two parametrised tests assert `introspected == manifest/excluded keys` per
   CLI and that every declared arg is still a real arg dest. A live
   no-absolute-path test was added.

**What was deliberately NOT touched**: `commands.py` needed no change — the
KID 1 `_entry`/`manifest` reader already handles arbitrary `manifest:`/
`excluded:` dicts, including flow-style ones, so production lines here = 0.

## Evidence

```
$ python3 extensions/agi/bin/commands.py --root . manifest | wc -l
... 133 entries total (38 before + 95 new)

$ per CLI (declared / excluded):
  send.py           15 /  0        grid.py            8 /  5
  dispatch.py        0 /  1        links.py           3 /  0
  workflow.py        8 /  0        rotate.py          8 / 16
  cli.py            14 /  0        spawn_budget.py    4 /  0
  provisioning.py    5 /  1        snapshot-goals.py  1 /  0
  viewport.py        1 /  0        crons.py           4 /  0
  envfile.py         1 /  0        ---- total 95 keys

$ commands.py manifest twice; cmp /tmp/a.json /tmp/b.json
byte-identical

$ python3 -m pytest extensions/agi/tests/test_commands_manifest.py \
      extensions/agi/tests/test_commands.py -q
65 passed, 7 skipped in 5.12s
```

**Gate probe (not vacuous).** Dropping `grid.py:checkout` from a temp copy of
`commands.md` and re-resolving gave `declared != introspected`, missing
`['checkout']` — the drift gate genuinely refuses a dropped verb.

## What the round did NOT cover

`propose` (Python, CLI and the graphweb GET /commands.json + POST /propose
endpoints) is still a later kid's conjunct; this round only completes the
DECLARATION DATA and the drift gate over it. The `side_effects` classification
is an authored judgement, documented in the THOUGHT block.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-979adf9d). Accepted for its slice; NOT the whole target. (1) INSTRUCTION: "a verb of a listed CLI that is neither declared nor excluded (a test introspects every parser)". (2) MACHINE: I imported the test module and called _introspect_cli for all 13 CLIs myself: send 15, dispatch 1, workflow 8, cli 14, grid 13, links 3, rotate 24, spawn_budget 4, provisioning 6, snapshot-goals 1, viewport 1, crons 4, envfile 1 -- every one NON-empty and EQUAL to its declared/excluded key set (133 manifest entries total, 25 proposable:false, grid-commit=graph-write, mesh-local-town=network). GATE PROBE: removing send.py:ask from a temp commands.md gave introspected!=declared, missing=[ask]. (3) NEAR MISS: a drift test that asserts only "every declared key maps to a real verb" would pass with the declaration half-missing; the equality assertion (introspected == declared, both missing and extra) is what closes it, and it is the version shipped. (4) NOTE: _LISTED_CLIS excludes write.py, so write.py args are pinned only for verb names, not arg dests -- acceptable because write.py has no argparse; its VERBS table is its parser.
<!-- THOUGHT:END -->

## Agent Notes
95 verbs of the 13 remaining listed CLIs now declared (72 manifest/proposable, 23 excluded with reason); drift test introspects each CLI's own argparse and passes 65/7 skipped; dropping a verb fails the gate (negative probe); 10 legacy side_effects overrides; commands.py unchanged
