---
id: experiment:schema-render-residue-heading-level-4
mint_id: 16b4166c769a41718a49470eaa22e03d
type: experiment
parents:
  - hypothesis:a00-18798b07-d9907a
next_edges: []
edited_by: a00-74167de8
line_ceiling: 40
loop: goal:g17.14@s2
model: deepseek/deepseek-v4.1-flash
probes: "gate-missing:rc=1 blocks by name; wire-wronglevel:heading_level 3 renders ### silently, not refused; wire-right:value 4 threads to ####; gate-final:rc=0 round-trip byte-identical"
production_lines: 9
profile: balanced
rebrief_answer: proceed with ceiling 40 - accepted as complete; the 219+/820- GOALS.md churn is the required re-render of a stale committed derived document, authored production is 9 lines, no new ceiling needed
rebrief_request: GOALS.md numstat churn 219+/820- is derived output from the required re-render of a stale committed document, not authored production; authored change is 9 lines, no new ceiling needed
role: kid
scaffold_hash: a5198d1b8194831b
season: 2
title: "heading_level 4 plus [goal] schema declaration: gate green, subgoals render ####"
town: core
---
<!-- BODY:BEGIN -->
# experiment:schema-render-residue-heading-level-4

## Run

Checkout `.agi/worktrees/a00-74167de8`, base `core/season2/main @ 18b3044cc`.

**PRE-fix** — the gate exits by hard error BEFORE any render or write (snapshot-goals.py:905-908):

```
$ python3 extensions/agi/bin/snapshot-goals.py --render --check
ERR: /data/work/agi/.agi/worktrees/a00-74167de8/.agi/nodes/goal/g17.14.1.md has no heading_level; run `snapshot-goals.py --from-doc` once to backfill it before rendering (goal:g6.9)
$ echo RC=$?
RC=1
```

No GOALS.md re-derivation happened before the fix; the byte-identical round trip is a POST-fix measurement.

**Fix A** — `heading_level: 4` on the three subgoals (their parent `goal:g17.14` is level 3, so subgoals are one deeper):

```
$ python3 extensions/agi/bin/write.py goal:g17.14.1 'set heading_level 4'
updated: goal:g17.14.1
$ python3 extensions/agi/bin/write.py goal:g17.14.2 'set heading_level 4'
updated: goal:g17.14.2
$ python3 extensions/agi/bin/write.py goal:g17.14.3 'set heading_level 4'
updated: goal:g17.14.3
```

**Fix B** — `.agi/context/schemas/[goal].md` now declares `heading_level` in `fields:`, adds it to `validation.required:`, and types it under `validation.types:` (`heading_level: int`).

**POST-fix** — re-derive GOALS.md, then check the round trip:

```
$ python3 extensions/agi/bin/snapshot-goals.py --render
rendered: 189 goal(s) + preamble -> /data/work/agi/.agi/worktrees/a00-74167de8/GOALS.md
$ python3 extensions/agi/bin/snapshot-goals.py --render --check
render --check: 189 goal(s) round-trip byte-identical
$ echo RC=$?
RC=0
```

**Schema scan** after widening the required list:

```
$ python3 extensions/agi/bin/links.py schema
schema: 192 node(s) missing a required field, 11 verdict-class disagreement(s), 0 outside-ref(s)
  goal              8   confidencex8, originx4, seedsx7, statusx1, tagsx7
```

The `goal` line is unchanged by the new required field — `heading_level` is not among the misses (all 193 `nodes/goal/*.md` carry it after Fix A), so the new requirement adds zero violations.

**Rendered wire:**

```
$ grep -n 'G17.14' GOALS.md
7512:### G17.14 — Grok Bot is a third-party harness adapter ... — status: active
7562:#### G17.14.1 — grok_bot_adapter.py REQUIRED surface ... — status: active
7570:#### G17.14.2 — harnesses.grok-bot config row only (no dispatch.py edit) — status: active
7578:#### G17.14.3 — mirror adapter interface tests for grok-bot — status: active
```

**Tests** (no engine code changed; the schema and derived doc are data):

```
$ <venv>/python -m pytest extensions/agi/tests/test_links.py extensions/agi/tests/test_snapshot_goals.py -q
108 passed, 47 warnings in 14.11s
```

## Probes

| Probe | Class | State handed to the tool | Observed |
|---|---|---|---|
| `gate-missing` | gate (must refuse) | scratch project `nodes/goal/g17.14.1.md` with the `heading_level:` line removed | rc=1, `ERR: .../g17.14.1.md has no heading_level` — blocks BY NAME, path in the message |
| `wire-wronglevel` | wire | scratch project `nodes/goal/g17.14.1.md` with `heading_level: 3` under the level-3 parent | rc=0 — NOT refused; renders `### G17.14.1`. The gate is a presence check, not a depth check. |
| `wire-right` | wire | the fixed tree | `#### G17.14.1/.2/.3` in GOALS.md; the value 4 threads to four hashes |
| `gate-final` | gate (must pass) | the fixed tree | rc=0, `189 goal(s) round-trip byte-identical` |

Scratch projects and captured outputs: `.agi/sessions/iter-DT.16/a00-18798b07/probe-missing/`, `probe-wronglevel/`, `probe-gate-missing.txt`, `probe-wire-wronglevel.txt`, `probe-wire-right.txt`, `probe-final-check.txt`.

## Result

`snapshot-goals.py` gates only on a missing `heading_level`; a missing field blocks by name, and the fixed tree passes. The three subgoals carry `heading_level: 4` and render `####`; the derived `GOALS.md` is byte-identical to a fresh render (rc=0); and the `[goal]` schema now declares the field it silently required, with no new required-field violations. The re-render also prunes stale GOALS.md sections with no backing node on this branch (`g1.legacy-direct`, `g20.legacy-direct`, `G1.18`, `G1.19`) — the committed document had been rendered on a tree that carried those nodes, so the pruning is the derived-file contract doing its job, not damage.

## Probes not covered (open)

The brief's second gate-class probe — a wrong depth (`3` under a level-3 parent) blocking by name — does **not** hold. The renderer has no hierarchy invariant; it renders whatever integer it finds. Closing that needs a depth check in `snapshot-goals.py` (or the schema) and is a follow-on node, not silently dropped here.

## Caveat

`links.py schema` reports a pre-existing 192 missing-required-field count across types (125 hypotheses missing `testable_claim`, etc.). That is unrelated to this change and untouched. The authored change is 9 lines (3 node frontmatter lines + 3 schema lines, each with a modified line above it); the large `GOALS.md` numstat churn is derived output, not authored production. See `rebrief_request`.

Raw output, screenshots, logs.
