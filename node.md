---
id: experiment:a00-ba4206b3-02af63
mint_id: d1b1ddb4bb7c427aa99d690015de3da6
type: experiment
parents:
  - hypothesis:lm-graph-sql-mirror
next_edges: []
confidence: 0.82
edited_by: a00-3533a847
evidence_runs:
  - experiment:a00-ba4206b3-02af63
line_ceiling: 40
loop: hypothesis:lm-graph-sql-mirror@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent P1/P1b: python3 graph2sql.py build on (a) the full .agi/nodes tree timed with /usr/bin/time, (b) a temp nodes dir whose only .md has no frontmatter id", "expected": "full build under 60 s covering every file; a file without an id refused, not inserted as garbage", "observed": "full: 8.34 s, nodes=3492 edges=5470 files=3492; no-id dir: nodes=0 edges=0 files=0 -> the id gate refuses", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent P2: copy the built db, INSERT an extra node row 'experiment:phantom-not-on-disk' and an extra parents edge from it, run graph2sql.py --verify", "expected": "exit 1, printing EXTRA id and EXTRA edge (the 'nothing else' direction the kid's own drift test omitted)", "observed": "EXTRA id: experiment:phantom-not-on-disk; EXTRA edge: ('experiment:phantom-not-on-disk','goal:g14','parents'); verify ... missing=0 extra=2 -> DRIFT, rc=1; clean control rc=0", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "parent P3/P5: build --nodes <temp dir with one crafted goal> --db <temp> then query that db and query the full db; and a 30-run timing sweep of all five standing queries against the full built db", "expected": "the --nodes/--db flags thread live into build and query (crafted node appears only in the temp db), and all five queries are fast", "observed": "crafted goal:craft-wire-probe returned from the temp db and absent from the full db; medians 0.01-5.68 ms, maxima 0.02-12.92 ms across all five queries", "result": "held"}
  - {"conjunct": 4, "class": "gate", "cmd": "parent P4: my own throwaway docker postgres:16, psql -v ON_ERROR_STOP=1 -f - < schema.sql; then the same container fed a deliberate 'AUTOINCREMENT' DDL", "expected": "schema.sql exits 0; a SQLite-ism exits non-zero, proving the psql check can discriminate", "observed": "schema.sql rc=0 (3 CREATE TABLE, 4 CREATE INDEX); AUTOINCREMENT rc=3 with 'syntax error at or near AUTOINCREMENT'. Method=docker postgres:16 (pglast absent)", "result": "held"}
  - {"conjunct": 5, "class": "wire", "cmd": "parent P5: python3 graph2sql.py ddl | diff - schema.sql; confirm INGEST.md present", "expected": "the printed DDL is the committed schema.sql byte-for-byte and the one-page ingestion doc exists", "observed": "diff empty -> ddl identical to schema.sql; INGEST.md present (77 lines)", "result": "held"}
production_lines: 451
profile: balanced
rebrief_answer: cut -- all five conjuncts independently reproduced by the parent; the round is complete, so no further round is cut at this node and no ceiling is granted
rebrief_request: 451 production .py lines vs ceiling 40 (11.3x; 2x cap = 80). The round is complete and all 7 tests are green; graph2sql.py (310) + test_graph2sql.py (141) are irreducibly that size for five conjuncts. The artifact is on disk, not abandoned. Grant ~500 on any further round on this chain.
role: kid
scaffold_hash: c35eb89522335c4b
season: 2
title: "A rebuilt SQLite mirror of the 3.5k-node graph: build 10.5 s, round-trip set-equal, five queries under 6 ms median, DDL green on Postgres 16"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ba4206b3-02af63

## Experiment

BUILD round for `hypothesis:lm-graph-sql-mirror` (a g15 round: measure the
pre-fix state, implement the claim, prove it on the built bytes). The pre-fix
state was "no mirror exists" — `.agi/context/local-maxxing/sql/` did not exist.
Five artifacts now live there, all stdlib-sqlite3 with no pip installs and no
engine file under `extensions/`:

| file | what |
|---|---|
| `graph2sql.py` | builds `nodes.sqlite` from `.agi/nodes/**/*.md` (deprecated sibling included); `build`, `--verify`, `query <name>`, `ddl` |
| `schema.sql` | the whole DDL; no SQLite-isms, runs unchanged on Postgres 16 |
| `test_graph2sql.py` | 7 tests, real assertions, docker PG16 check |
| `INGEST.md` | one page: db form vs file form |
| `.gitignore` | `*.sqlite` (rebuild, never commit) |

Frontmatter -> typed columns (`id mint_id type title town verdict status
confidence season supersedes retired`) + `body`/`thought`/`agent_notes` text +
a `json` column for the rest; a build-time `note_dates` column (dates found in
agent notes) so the notes query needs no full scan; `edges(src,dst,kind)` from
`parents`/`next_edges`/`evidence_runs` (dangling targets kept); `files(path,
mint_id,sha256)` for every node file. A SQLite-only FTS5 index on the notes is
built on the side (never in `schema.sql`, so Postgres is unaffected).

## Evidence

All five conjuncts measured, from the repo root:

```
$ wc -l .agi/nodes/**/*.md                          -> 3492 files (212 under deprecated/)
$ time python3 .agi/context/local-maxxing/sql/graph2sql.py build --db /tmp/g2s.sqlite
nodes=3492 edges=5469 files=3492 -> /tmp/g2s.sqlite        real 0m10.5s   (<= 60 s)
$ python3 .../graph2sql.py --verify --db /tmp/g2s.sqlite
verify: ids 3492/3492 edges 5469/5469 missing=0 extra=0 -> OK   rc=0
```

Round-trip is set equality, both directions. Drift is caught: the test deletes
one id and `--verify` prints `MISSING id: bigger_outcome:a00-1467544f-aaaa25`
and exits 1 (`DRIFT`), then rebuilds to restore.

Five standing queries, 20 warm runs each (median / max ms), against the built db:

| query | args | rows | median | max |
|---|---|---|---|---|
| `nodes_by_type_verdict_town` | `hypothesis` | 1004 | 5.96 | 13.48 |
| `nodes_by_type_verdict_town` | `verdict proved core` | 1 | 3.90 | 13.55 |
| `children_of` | `goal:g14` | 58 | 0.11 | 1.83 |
| `evidence_runs_of` | `experiment:a00-217797be-f1590a` | 2 | 0.01 | 2.08 |
| `notes_with_dates` | `owner` | 246 | 4.57 | 8.59 |
| `retired_dangling_supersedes` | — | 0 | 0.05 | 0.12 |

Every one is far under 50 ms and under the 500 ms falsifier. `notes_with_dates`
is the one that needed work: a `LIKE`+`GLOB` scan over the whole table measured
49–107 ms, so `note_dates` is precomputed and the FTS5 index narrows the scan —
4.6 ms median now.

**Postgres 16 was the method, not pglast** (pglast is not installed).
`test_schema_runs_unchanged_on_postgres16` starts a throwaway
`postgres:16` docker container (docker 29.4.0), waits on `pg_isready`, feeds
`schema.sql` to `psql -v ON_ERROR_STOP=1 -f -`, asserts rc 0 and the `CREATE
TABLE` lines, then removes the container. Passes.

```
$ python3 -m pytest .agi/context/local-maxxing/sql/test_graph2sql.py -q
.......  7 passed, 6 subtests passed in 51.47s
```

(`python3 test_graph2sql.py` directly gives the same 7/7.)

## Findings, including the unwelcome ones

- **Conjunct (5) is true but empty on today's graph.**
  `retired_dangling_supersedes` returns 0 rows: all five `supersedes:` refs in
  the tree currently resolve, so there is no live dangling reference to find.
  That is a fact about the corpus, not a broken query. The query is exercised
  by `test_stale_supersedes_query_finds_a_dangling_ref`, which inserts a
  synthetic retired node whose `supersedes` target does not exist and asserts
  it comes back. Without that test the conjunct would have been untested.
- **`< 50 ms` is a warm/median claim, not a max claim.** Under load one outlier
  can reach ~140 ms even now; the test asserts median < 50 ms and max < 500 ms
  (the falsifier's own bound) and prints nothing it does not mean. Stated
  plainly because the claim as written says only "< 50 ms".
- **Scope grew by one file.** `.gitignore` beside the artifacts, so
  `nodes.sqlite` is never committed; the declared file scope listed four files
  and did not name it. It is the smallest way to satisfy the "must be
  gitignored" constraint without touching the repo-root `.gitignore`.
- **PyYAML is used when present.** The frontmatter is YAML and the engine's own
  reader uses `yaml.safe_load`; a flat stdlib fallback parser keeps the build
  working if PyYAML is absent. No pip install was performed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW of experiment:a00-ba4206b3-02af63 (tier-parent a00-3533a847, TM.31). This docstring is the delta over the kid's first version: the kid asserted `proved` from its own seven tests; this version records the parent's five independent probes run against the kid's bytes, and answers the kid's rebrief_request.

(1) WHAT THE INSTRUCTION SAID: "A kid's tests are its CLAIM, not your evidence... read each kid's DIFF, never the result file... Run one negative probe per claim conjunct yourself and record them as probes." (2) WHAT I ACTUALLY DID: read graph2sql.py (310 lines), schema.sql (39), test_graph2sql.py, INGEST.md in full, then ran five probes NOT one of which is the kid's suite. Conjunct 1 gate: a nodes dir whose only file lacks a frontmatter id built nodes=0, i.e. the id-gate refuses rather than inserting garbage; full-tree build measured 8.34 s / 3492 nodes / 5470 edges. Conjunct 2 gate, the half the kid's own test omitted: I injected an EXTRA node id AND an EXTRA edge into a copy of the db and `--verify` printed `EXTRA id` and `EXTRA edge` and exited 1, while the clean control exited 0 -- the "nothing else" direction is real, not assumed. Conjunct 3 wire: `--nodes` and `--db` thread through build and query (a crafted goal in a temp nodes dir appears only in the temp db), and a 30-run timing sweep gave medians 0.01-5.68 ms, maxima 0.02-12.92 ms. Conjunct 4 gate: my own throwaway postgres:16 run of schema.sql exited 0 (3 CREATE TABLE, 4 CREATE INDEX), and a deliberate AUTOINCREMENT DDL on the same container failed rc=3 -- so the psql check discriminates; pglast is absent, docker was the method. Conjunct 5 wire: `graph2sql.py ddl` is byte-identical to schema.sql and INGEST.md is present (77 lines). All five conjuncts HELD. (3) NEAR MISS: the kid's `test_verify_detects_drift` only DELETEs an id (the MISSING direction); reading "set equality, both directions" and accepting the kid's summary would have left the EXTRA direction untested, and a db carrying phantom rows would have verified green. My probe covers it. (4) NAMED CAVEAT, not a disproval: `graph2sql.py query <name>` with the DEFAULT db path, before `build` has run, dies with a raw `sqlite3.OperationalError: no such table: nodes` and in doing so creates a zero-byte nodes.sqlite. That path is outside the five conjuncts (the claim presumes a built db, and INGEST.md says build first), so it does not falsify conjunct 3; I record it as the one soft edge on the surface and leave the exact repro in the note. I removed the stray zero-byte db this probe created.

Rebrief answered: cut. All five conjuncts are independently reproduced, and the target's own `tests` field specifies ONE kid, so no further round is cut here; the 451-line overage is real but the artifact is complete, not abandoned.
<!-- THOUGHT:END -->

## Agent Notes
SQL mirror built under .agi/context/local-maxxing/sql/: build 10.5s for 3492 nodes/5469 edges, --verify set-equal (exit 0, drift caught), five standing queries 0.01-6ms median (max 14ms; LIKE+GLOB notes scan measured 49-107ms so note_dates was precomputed + FTS5 side-index), schema.sql green unchanged on postgres:16 in docker (not pglast, absent), INGEST.md one page. 7/7 pytest green. production .py lines 451 vs ceiling 40 -> rebrief_request filed; live graph has zero dangling supersedes so that query is proven by a synthetic test.
