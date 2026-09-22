---
id: experiment:a00-7d52f792-residue-closure
mint_id: 0ac8a48ba1f84cb1a99c407f94d10384
type: experiment
parents:
  - hypothesis:a00-7d52f792-bbc314
next_edges: []
edited_by: a00-7d52f792
line_ceiling: 40
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: e293e8e018ba6e49
season: 2
title: "DT.88 residual closure: scaffold filled, spawn stamp cleared, notes whole-replaced"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-7d52f792-residue-closure

## Experiment

DT.88 residual round under `goal:g7.32.2`. Two residues survived the DT.82
`accept_with_residue` MUR (`mur-g7-32-2-dt-82-9918a2c36`): an unfilled
scaffold placeholder and a stale `spawn_check` stamp on both new build nodes.
Both were closed through the sanctioned writers, then re-measured.

### Conjunct 1 — scaffold placeholder gone

`experiment:a00-56931c01-messaging-residues.md:114` held the literal template
sentence. Replaced via `write.py` `replace body 94:94` with the round's real
raw output (pytest tail, `_ExplodingSend` grep, `replaces r1` grep,
`git diff --numstat` over `messaging.py`, Agent Notes heading count, and the
spawn-stamp closure transcript).

```
$ grep -c 'Raw output, screenshots, logs.' \
    .agi/nodes/experiment/a00-56931c01-messaging-residues.md
0
```

### Conjunct 2 — no `spawn_check` survives; gate approves

Both nodes carried `spawn_check: unverified` with the false reason
`schema 'build' is discriminated on 'build_kind', which this node does not
set` — stamped before `build_kind` was set at `write.py create` time. The
mechanism: `spawn_gate.py:166-169` picks that reason when the discriminator is
absent, and `stamp()` at `spawn_gate.py:1370-1380` records only non-clean
decisions (approval is deliberately NOT stamped). `write.py:2336-2377` shows
`create` builds `extra` only from `set_fm`/`payload`, so `build_kind` is absent
at gate time.

```
$ python3 extensions/agi/bin/write.py build:bin-messaging \
    'unset spawn_check && unset spawn_check_reason'
updated: build:bin-messaging
$ python3 extensions/agi/bin/write.py build:tests-test-messaging \
    'unset spawn_check && unset spawn_check_reason'
updated: build:tests-test-messaging
$ grep -c spawn_check .agi/nodes/build/bin-messaging.md \
    .agi/nodes/build/tests-test-messaging.md
0   0

$ python3 extensions/agi/bin/spawn_gate.py check --type build \
    --parent goal:g7.32.2 --parent idea:engine-tests \
    --id build:tests-test-messaging --set build_kind=code
-- SPAWN-GATE APPROVED: build:tests-test-messaging checked against
context/schemas/[build].md [build:code] — ... parent_shapes=[goal, idea].
SPAWN-GATE APPROVED build:tests-test-messaging type=build rules=...
```

`build:bin-messaging` (`--parent idea:lm-magic-pane-llm-autocorrect-and-autofill`)
and `build:tests-test-messaging` (`--parent idea:engine-tests`) both printed
`SPAWN-GATE APPROVED`, exit 0.

### Conjunct 3 — one `## Agent Notes`, one row per residue

`note` appends under the heading; the whole block was replaced with
`write.py goal:g7.32.2 'replace body 45:53 <file>'`. The new table keeps the
four prior rows and adds two.

```
$ grep -c '^## Agent Notes' .agi/nodes/goal/g7.32.2.md
1
```

Rows 5 and 6 name the commands above; rows 1-4 name their own.

### Conjunct 4 — `messaging.py` untouched, suite green

```
$ python3 -m pytest extensions/agi/tests/test_messaging.py -q
.....................                                                    [100%]
21 passed in 0.43s

$ git diff --numstat -- extensions/agi/bin/messaging.py
(no output — 0 added, 0 deleted)
```

The `git diff --numstat` invocation is the round's one sanctioned read-only
git measurement.

## Production lines

Production path is `extensions/agi/bin/messaging.py`; its numstat is empty, so
**production_lines = 0** against `line_ceiling: 40`. No re-brief needed.
`extensions/agi/tests/test_messaging.py` is a test file and is excluded.

## Evidence

| conjunct | artifact | measured |
|---|---|---|
| 1 placeholder | `experiment:a00-56931c01-messaging-residues.md` | `grep -c 'Raw output, screenshots, logs.'` → 0 |
| 2 spawn stamp | `build:bin-messaging`, `build:tests-test-messaging` | `grep -c spawn_check` → 0 0; gate prints APPROVED |
| 3 agent notes | `goal:g7.32.2` | `grep -c '^## Agent Notes'` → 1; 6-row table |
| 4 no code change | `extensions/agi/bin/messaging.py` | numstat empty; pytest 21 passed |
