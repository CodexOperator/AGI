---
name: agi-node-write
description: >
  Read, edit or create ANY agi graph node through write.py (the only sanctioned node
  writer): the verb grammar, create with the spawn gate, build nodes and their two legal
  parent shapes, config:* nodes, THOUGHT blocks, deprecate-never-delete. Use whenever a
  post touches a node file, a payload, a card or a config:* node. For goals use agi-goal.
---

# agi-node-write — every node operation is a write.py call

Source of truth: `python3 extensions/agi/bin/write.py -h` — its epilog renders the verb table from `VERBS`
and is drift-guarded, so read it there, not here. This skill carries what `-h` cannot.

## 1 · Grammar (F24, F4)
```bash
python3 extensions/agi/bin/write.py <node-id> '<verb> <args> && <verb> <args>' --actor <post> --role <role> [--dry-run]
python3 extensions/agi/bin/write.py create <type> <slug> --parent <id> [--parent <id>] [--set k=v] [--payload PATH] [--body-file PATH]
```
- ONE single-quoted script; units joined by ` && `; a literal verb-led `&&` in prose = `\&&`.
- `read body N:M` / `read payload N:M` — the range is REQUIRED. Read in pieces; never cat a big node.
- `replace body N:M <file>` is STANDALONE: never in one script with `note`, `thought`, `body_patch`.
- `sub <old> => <new>` is literal. `--dry-run` shows the edit and writes nothing.
- `set` is schema-gated (goal:g7.33.10): an invented field, an out-of-regex value, a raw string into a list field → refused.
- `--no-spawn-gate` / `--no-evidence-gate` = NEVER: it stamps the node unreviewed.

## 2 · Where nodes live (F17, F21)
```
.agi/nodes/<type>/<slug>.md              live            schemas: .agi/context/schemas/[<type>].md (brackets in the name)
.agi/nodes/deprecated/<type>/<slug>.md   retired (moved, never deleted)
.agi/nodes/.geometry/<name>.md           config:<name>  → write.py config:<name> 'read body N:M'   (never ls/find)
```
`write.py create <type> <slug> --parent <id>` runs the spawn gate against the schema; the schema, not argparse,
decides how many parents are legal.

## 3 · Build nodes — two legal origins (goal:s29, schema [build].md `parent_shapes`, an OR across shapes)
| shape | means |
|---|---|
| `[mvp]` | a NEW file, argued for by an mvp |
| `[build, goal]` | a new VERSION of an existing file + the goal that motivated it |
| `[goal, mvp]` · `[goal, idea]` | a new file under a goal, argued by an mvp or an idea (skills: `idea:engine-skill-doc`) |
A goal ALONE never mints a build node. New file + node in one call:
```bash
write.py create build <path-with-dashes> --parent goal:<id> --parent idea:<id> --payload <repo/path> \
  --set payload_ref=<repo/path> --set build_kind=prose|code --body-file <body.md> --actor <post> --role <role>
```
`--payload` creates the file if absent (never overwrites) and records `link_ref`; set `payload_ref` too —
`level3.py` keys on it and would otherwise mint a duplicate. A build node's `BUILD-CONTRACT` block is
regenerated — never hand-edit it; edit the payload (`patch -`, `replace payload N:M <file>`, or the file itself).

## 4 · THOUGHT — body is state, thought is delta (goal:g2.11)
`thought <text>` rewrites the authored region whole: why THIS version differs from the last. Absent = empty;
never fabricate one after the fact. Mechanism, not wording: quote the instruction · cite what the machine does
(file:line or an artifact you ran) · name the near miss · if a standing rule was bent, the property of THIS case.

## 5 · Never
- delete a node or `git rm` under `.agi/nodes` — retire: `set status deprecated` + move to `deprecated/<type>/`
  (mint_id is identity, the address may change); a fresh uncommitted node gets versioned by the grid cron within minutes (trap 3).
- create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; recreate `.agi/context/kits/` or `plans/build-site.md`.
- hand-edit `GOALS.md` (derived) or frontmatter (write.py owns it).
- let `active_node_count + deprecated_node_count` drop (skill `agi-verify`).
