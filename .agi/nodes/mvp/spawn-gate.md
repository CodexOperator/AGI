---
id: mvp:spawn-gate
mint_id: 656e43bdaf164763aa347d5de0c37dd2
type: mvp
parents:
  - verdict:spawn-gate-lands-on-writer-path
next_edges: []
confidence: 0.85
edited_by: season.py
season: 1
source_files:
  - extensions/agi/bin/spawn_gate.py
  - extensions/agi/bin/cli.py
  - extensions/agi/bin/post_wire.py
  - extensions/agi/tests/test_spawn_gate.py
status: implemented
tags:
  - s17
  - schema
  - gate
tests_pass: true
thought_session: season
title: bin/spawn_gate.py — schema-declared spawn rules, enforced on the writer path
---
# mvp:spawn-gate

The code control S17 asked for. **The schema is data; this module is only the
enforcement.** Every per-type value lives in `context/schemas/`; nothing here
restates it.

## Files

| path | what |
|---|---|
| `extensions/agi/bin/spawn_gate.py` | new — the gate |
| `extensions/agi/bin/cli.py` | wired: `scaffold`, `done`'s fallback verdict node |
| `extensions/agi/bin/post_wire.py` | wired: verdict-node creation |
| `extensions/agi/tests/test_spawn_gate.py` | new — 37 tests |
| `context/schemas/*.md` | 7 new schemas, 6 repaired, 1 made loadable |

Payload edits are staged under `payloads/`; the graph is the source (G6.3).

## Inputs

- `context/schemas/[<type>].md` → `spawn:` block (flat, or discriminated).
- `context/schemas/[shape].md` → `parentless_types`, `max_parents_ceiling`.
- `context/schemas/[config].md` → `locations.nodes_root` (the one field read).
- The node corpus → id → type index, for resolving parent types.

## Outputs

`SpawnResult(status = approved | rejected | unverified | bypassed)`, and a
line on **every** one of them.

- **rejected** — names the rule, the schema file, the node and the fix.
  Writer paths turn it into exit 2; nothing is written, matching
  `evidence_gate`'s handling of a taxonomy violation.
- **approved** — names the schema file and every rule that passed, so
  "approved" and "not checked" are distinguishable without reading code.
  Deliberately leaves **no** frontmatter mark: a field on every node in the
  graph is noise. The terminal line is the feedback.
- **unverified** — fail-open. No schema, no `spawn:` block, a broken schema,
  or a parent id that resolves to nothing. Writes, warns, stamps
  `spawn_check: unverified` + reason.
- **bypassed** — `--no-spawn-gate`. Loud, stamps `spawn_gate: bypassed`.

## The design calls, and why

**No "demote".** `evidence_gate` has three outcomes because an overclaimed
verdict has an honest weaker form. A structural violation does not: you cannot
half-parent a node, and inventing the missing parent is forbidden (G7.1). So
the axis is decidable/undecidable — reject what is decidably wrong, warn on
what cannot be decided.

**The rule table has exactly one home.** Copying it into Python would recreate
the defect S17 names: the engine root is defined three times, and the two
Python definitions differ by one index because one counts from a directory and
the other from a file. `[shape].md` holds the *grammar*; the type files hold
the *values*; this module reads and never restates.

**A broken schema is refused, not obeyed.** `min_parents: 0` outside the
whitelist, or `max_parents` above the ceiling, makes the schema a load error
and its type falls back to `unverified`. That is what makes "exactly three may
be parentless" mechanical rather than prose, and it means raising a type's
budget takes two deliberate edits — the type file and `[shape].md`.

**Inactive schemas are never enforced.** Bracketed = active, per
`schema_registry/loader.py`. Un-bracketing a schema turns its rule off without
deleting it.

**Both spellings, zero renames.** `-` → `_` on both sides of every type
comparison, so `bigger-outcome` and `bigger_outcome` resolve to one rule and
the one real `app_purpose` → `bigger-outcome` edge validates. **Only the type
half** is canonicalised — `goal_kind: long-term` legitimately has a hyphen,
and rewriting it disabled the whole `[goal].md` schema until it was fixed.
`cli.py` now writes underscores and accepts hyphens as aliases; `dispatch.py`
still mints hyphens and is not owned here.

## Also fixed while in there

- `cli.py scaffold --parent` was a single **required** flag, so argparse — not
  the schema — decided every type had exactly one parent. It now repeats.
- `idea` and `task` were absent from `NODE_TYPES`: the tool whose job is
  creating nodes could not create the types with 71 and 91 of them. Added.
  `goal` and `level3` deliberately not added — both are derived, and a
  hand-scaffolded one is a stray the next loop run deletes.
- `cli.py done`'s fallback verdict node minted no `mint_id`, so every verdict
  it wrote was skipped by `grid.py commit --all` and silently had no version
  history (goal:s14). Surfaced by `[verdict].md` listing `mint_id` required.

## Verification

```
$ python3 -m pytest payloads/extensions/agi/tests/test_spawn_gate.py -q
37 passed in 1.07s
$ python3 -m pytest payloads/extensions/agi/tests/ -q
668 passed, 1 skipped in 26.58s
```

Both pre-registered falsifiers are tests, so they cannot silently regress.
`test_shipped_schemas_load_without_error` pins the two bugs the build itself
hit: a `---` banner inside frontmatter silently emptying `[shape].md`, and the
over-eager canonicalisation above.

## Not done

Coverage is 2 of ~6 writers — `dispatch.py` and the three generators are
ungated; see the verdict. The `validation:` engine
(`schema_registry/validation.py`) is still unwired, so `required`/`types`/
`regex` are declared and unenforced. `[config].md`'s other five locations are
documented, not collapsed.