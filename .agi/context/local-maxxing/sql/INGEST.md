# INGEST.md — reading the graph as SQL instead of files

*git is the source of truth. `nodes.sqlite` is a derived, gitignored query
surface rebuilt from `.agi/nodes/**/*.md` by `graph2sql.py` (<= 60 s, ~14 s
measured on the A1 including the FTS index). Rebuild it whenever the graph
moves; never edit it by hand.*

## Build, check, ask

```bash
S=.agi/context/local-maxxing/sql
python3 $S/graph2sql.py build            # .agi/nodes/**/*.md -> $S/nodes.sqlite
python3 $S/graph2sql.py --verify         # set equality; exit 0 on match, 1 on drift
python3 $S/graph2sql.py query children_of goal:g14
python3 $S/graph2sql.py query nodes_by_type_verdict_town verdict proved core
python3 $S/graph2sql.py query evidence_runs_of experiment:a00-217797be-f1590a
python3 $S/graph2sql.py query notes_with_dates owner
python3 $S/graph2sql.py query retired_dangling_supersedes
python3 $S/graph2sql.py ddl              # print schema.sql (runs on Postgres 16)
```

`--verify` compares *sets*, both directions: every `id` and every
`(src,dst,kind)` edge in the files must be in the db and nothing else may be.
A failure prints up to 20 `MISSING`/`EXTRA` rows and exits 1.

## The tables

| table | one row per | columns that matter |
|---|---|---|
| `nodes` | node file with a frontmatter `id` | `id`, `mint_id`, `type`, `title`, `town`, `verdict`, `status`, `confidence`, `season`, `supersedes`, `retired`, `body`, `thought`, `agent_notes`, `note_dates`, `json` |
| `edges` | `(src,dst,kind)` from `parents` / `next_edges` / `evidence_runs` | `src`, `dst`, `kind` |
| `files` | every `.md` under `nodes/` | `path`, `mint_id`, `sha256` |

`json` holds every frontmatter key not promoted to a column. `retired=1` means
the file is under a `deprecated/` sibling **or** carries `status: deprecated`.
`thought` is the `THOUGHT:BEGIN…END` region; `agent_notes` is the
`## Agent Notes` section; `body` is the whole rest of the file. `note_dates`
is the comma-joined set of `YYYY-MM-DD` dates found in `agent_notes`, computed
at build time so `notes_with_dates` needs no full-text scan.

## File form vs db form — which to use

| question | file form | db form |
|---|---|---|
| what does *this* node say | `read .agi/nodes/<type>/<slug>.md` | `SELECT * FROM nodes WHERE id=?` |
| every node of a type/verdict/town | glob one dir, parse each | `SELECT … WHERE type=? AND verdict=? AND town=?` (indexed) |
| children of a goal | grep every file for `goal:<id>` | `SELECT src FROM edges WHERE kind='parents' AND dst=?` |
| who cites this run | grep `evidence_runs` | `SELECT src,dst FROM edges WHERE kind='evidence_runs' AND (src=? OR dst=?)` |
| a phrase in anyone's notes, with dates | grep -r + manual date scan | `query notes_with_dates <term>` (FTS5-indexed; returns id,title,note_dates; read `agent_notes` by id for the prose) |
| retired node with a dangling `supersedes` | five-file special case | `query retired_dangling_supersedes` |
| how many nodes / did the tree move | `find … | wc -l` | `SELECT count(*) FROM nodes` |
| write, edit, retire, version | **file form only** | never — the db is read-only in spirit; rebuild it |

**Rule of thumb:** reach for the db when the question is *across* nodes
(counts, joins, sets, full-text); reach for the file when the question is
*inside* one node or when you are changing anything. The db cannot answer
"which version introduced this line" — that is the grid (`grid.py`), and the
db cannot be edited back into the graph — that is `write.py`.

## What the mirror is not

- Not the source of truth. A node added since the last `build` is invisible.
- Not a writer. No INSERT/UPDATE path exists; the build drops and re-creates.
- Not versioned. The `.sqlite` file is gitignored; `git` and `refs/grid/*` hold
  history.
- Not a substitute for `zoom.py`/`brief.py`. It answers standing loop
  questions fast; it does not rank, route or render.

## Portability

`schema.sql` is the whole DDL and has no SQLite-isms (no `AUTOINCREMENT`, no
`PRAGMA`, no `WITHOUT ROWID`), so the same file creates the tables on
PostgreSQL 16 — verified in a throwaway `postgres:16` docker container by
`test_graph2sql.py`. The FTS5 index used for `notes_with_dates` is a SQLite
build-time extra and is **not** in `schema.sql`, so Postgres consumers fall
back to a `LIKE` scan (still well under 50 ms at 3.5 k rows). Neon or any
Postgres can carry the same tables; only the loader is SQLite-specific today.
