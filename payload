---
name: agi-node-write
description: >
  OLD SETUP ONLY (a post whose row has engine.v 4 edits node files with plain Write/Edit
  and agi-turn commits; owner 10-01 23:3xZ). Read, edit or create ANY agi graph node through write.py (the old setup's node
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
  (mint_id is identity, the address may change); every write commits itself by exact path (`write.commit_message` in `.agi/config.json`); `the write landed uncommitted` (a held suite lock) prints the one commit-by-path line to run -- the grid cron versions what is committed, it is never the commit path.
- create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; recreate `.agi/context/kits/` or `plans/build-site.md`.
- hand-edit frontmatter (write.py owns it).
- let `active_node_count + deprecated_node_count` drop (skill `agi-verify`).
- start a `--body-file` with its own `# <id>` H1: `create` adds one, the node gets two (fix = `replace body 1:<L>`, L = the body length; there is no END keyword: `read body 1:END` refuses). Append = `replace body L:L <file>`, the file starting with line L.
  On a node WITH a THOUGHT block (since 6aedaa5a7): a range over a marker line refuses unless the file carries that ONE block whole, and the spliced body adds no block and no stray marker line -- so the whole-body fix keeps the block in its file, or replaces the lines around it and rewrites the reason with the `thought` verb; an Append whose L is the END marker line refuses (append above it).
- use the `thought` verb on a node whose body QUOTES a column-0 THOUGHT pair (plain or fenced): it rewrites the FIRST pair anywhere
  (node_writer.py `_THOUGHT_RE`), the quoted one included — `replace body` on the lines around both pairs instead: it lands
  as long as the splice adds no pair and no stray marker (SM 118).
