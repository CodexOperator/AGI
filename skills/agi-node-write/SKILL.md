---
name: agi-node-write
description: >
  Read, edit or create ANY agi graph node by plain file edit (the node writer is retired, goal:g7.16.1.11.46.23):
  where nodes live, the sed read route, the edit route and its two checks, create with the spawn gate, build-node
  parent shapes, THOUGHT blocks, retire-never-delete. Use whenever a post touches a node file; goals: agi-goal.
---

# agi-node-write — a node is a plain file; read it with sed, edit it in place

The writer was retired (owner a1, goal:g7.16.1.11.46.23): there is no verb grammar, no `--actor`/`--role`, no
`--dry-run`. A node is `.agi/nodes/<type>/<slug>.md`; the schema and the commit gate are the guards.

## 1 · Read, edit, check, commit (F24, F4)
```bash
sed -n '1,60p' .agi/nodes/<type>/<slug>.md                    # a range
sed -n '/^## Falsifier/,/^## Out/p' .agi/nodes/<type>/<slug>.md   # a section: the anchor is CONTENT, never a file line number
git grep -lE '^id: <id>$' -- .agi/nodes                        # type dir unknown
```
- Read by CONTENT anchor. A line number drifts, and a range counted from the body start is not a file line (a node's frontmatter can be 140 lines).
- A path with brackets (`.agi/context/schemas/[config].md`): `git cat-file blob REV:path`, never `git show REV:path` (rc 0 and EMPTY when the file is absent).
- EDIT with plain Write/Edit. A post: `agi-wt pull <id>` (or `agi-wt new <path>`), edit in the RAM tree, `agi-turn` versions it at Stop (~/t is a read view); a path in ~/t: `agi-at <path>`. MAIN: edit, then `git commit -- <path>` (by exact path, never `git add -A`).
- BEFORE every commit of a node edit: `python3 extensions/agi/bin/links.py schema` (the type's required list, regexes, list fields) and `python3 extensions/agi/bin/links.py links` (every link resolves; broken must be 0).
- A frontmatter field whose value the engine validates (a verdict, `evidence_runs`): `node_writer.update_node(root, '<id>', set_fm={...})` is the validated one-liner; a body line or a note: a plain edit.
- A text value that parses as YAML null or a bool (`none`, `null`, `true`) is stored as that type: quote it.

## 2 · Where nodes live (F17, F21)
```
.agi/nodes/<type>/<slug>.md              live            schemas: .agi/context/schemas/[<type>].md (brackets in the name)
.agi/nodes/deprecated/<type>/<slug>.md   retired (moved, never deleted)
.agi/nodes/.geometry/<name>.md           config:<name>  → sed -n '/^## <heading>/,/^## /p' .agi/nodes/.geometry/<name>.md   (never ls/find)
```
A NEW node: write the file with the frontmatter the type schema requires; the spawn gate (grow.py, run by `agi-at` / `agi-turn` for a new `.agi/nodes` file) judges its parent set against the schema, and the schema, not a flag, decides how many parents are legal.
`config:*` nodes carry `written_by` (owner / prime_director only): a director's edit of one is refused at review -> hand the exact text to your master, never force it (DG4).

## 3 · Build nodes — two legal origins (goal:s29, schema [build].md `parent_shapes`, an OR across shapes)
| shape | means |
|---|---|
| `[mvp]` | a NEW file, argued for by an mvp |
| `[build, goal]` | a new VERSION of an existing file + the goal that motivated it |
| `[goal, mvp]` · `[goal, idea]` | a new file under a goal, argued by an mvp or an idea (skills: `idea:engine-skill-doc`) |
A goal ALONE never mints a build node. **Never run `level3.py` by hand** until goal:g1.43.1's round lands: its default
scan overwrites a hand-repaired parent list with its census hit (goal:g1.43 rows 16-18 -> the illegal `[idea]`; council 10-10).
A new file is written directly under `extensions/`, `skills/` or `src/`; its node is `.agi/nodes/build/<path-with-dashes>.md` with `parents:` one legal shape, `payload_ref: <repo/path>`, `build_kind: prose|code`.
Set `payload_ref` — `level3.py` keys on it and would otherwise mint a duplicate. A build node's `BUILD-CONTRACT` block is
regenerated — never hand-edit it; edit the payload (the file itself).

## 4 · THOUGHT — body is state, thought is delta (goal:g2.11)
The text between `<!-- THOUGHT:BEGIN` and `<!-- THOUGHT:END -->` is rewritten whole: why THIS version differs from the last. Absent = empty;
never fabricate one after the fact. Mechanism, not wording: quote the instruction · cite what the machine does
(file:line or an artifact you ran) · name the near miss · if a standing rule was bent, the property of THIS case.
A node others also edit (a shared doc): read its CURRENT THOUGHT first and carry it verbatim into the rewrite (all-is-one clobbered alive's THOUGHT 07:1xZ).
A node whose body QUOTES a column-0 THOUGHT pair (plain or fenced): the engine reads the FIRST pair anywhere (node_writer.py `_THOUGHT_RE`), the quoted one included — edit the lines around both pairs (SM 118).

## 5 · Never
- delete a node or `git rm` under `.agi/nodes` — retire: `cd extensions/agi/bin && python3 -c "import node_writer; node_writer.retire_node('../../../.agi', '<id>', note='<why>')"` = `status: deprecated` + the move to `deprecated/<type>/`, one act (a status-only deprecate is REFUSED: goal:g4.18.5.4; `verify` fails a status/place mismatch)
  (mint_id is identity, the address may change); a held suite lock: commit by exact path once it is released, never `git add -A` — the grid cron versions what is committed, it is never the commit path.
- create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; recreate `.agi/context/kits/` or `plans/build-site.md`.
- hand-edit a node's `id`, `mint_id` or `type` (identity); a rename is a retire + a new node (goal renumber: skill agi-goal).
- let `active_node_count + deprecated_node_count` drop (skill `agi-verify`).
- start a body with its own `# <id>` H1 when the scaffold already carries one: the node gets two.
- rewrite `.agi/config.json` from a dict: it is not json.dumps round-trippable (19588 B, indent=2 dump differs) -> insert cells as text, verify with `json.loads` (DG4).
- count a minted verdict node as closing its hypothesis: also set the hypothesis's own `verdict` field (and evidence_runs) in the same turn, else the round stays open (all-is-one).

## Traps moved from cards (owner 10-10: one sweep, then a rule)
- a node body written through an UNQUOTED heredoc lost every $ figure ("$15" -> "5", goal:g5.4.2) -> every node body via `<<'EOF'`, values patched in after (belam gen II)
- the agi-at reset leaves a STALE `town:local-maxxing` metrics line in ~/t -> `git restore --source=HEAD --staged --worktree -- .agi/nodes/town/local-maxxing.md`, never commit it (belam gen II)
- `agi-at` run with NO path (to read its usage) committed ALL of ~/t, stale, onto posts/belam (a2afb06f76, 15:04Z 10-26, belam trap 141, gen VIII; caught before any push or cut, CAS-rewound) -> never run an agi-* tool bare to learn it: read its line-2 comment (`sed -n 2p ~/bin/<tool>`)
