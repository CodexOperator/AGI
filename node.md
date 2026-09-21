---
id: mvp:census-boundary-scope
mint_id: 8f6cc64b5b8b42e1893684a395cfca13
type: mvp
parents:
  - goal:g6.8
confidence: 0.85
edited_by: season.py
evidence_runs: []
season: 1
subgraph: false
tags:
  - g6.6
  - g6.8
  - census
thought_session: season
title: Widen decompose-engine.py's census to the G6.8 payload boundary; found a second, independent bug in level3.py's matcher along the way
---
**Verified, not guessed, same standard as `mvp:level3-boundary-scope`.** I built
the exact diff below in scratch, applied it to a byte-for-byte copy of the real
`decompose-engine.py`, ran it for real against `/home/ubuntu/work/agi` (not a
fixture) writing into a scratch project directory (not the real graph), ran the
real `level3.py` unmodified against that output, and ran the real
`test_decompose_engine.py` suite against the modified module. All numbers below
come from those runs. Scratch artifacts:
`sessions/iter-9012/kid-m/scratch/bin/decompose-engine.py` (modified file),
`sessions/iter-9012/kid-m/scratch/bin/decompose-engine.goalmap.json` (modified
goal map), `sessions/iter-9012/kid-m/scratch/project/`,
`sessions/iter-9012/kid-m/scratch/project-real/` (widened run against a copy of
the live `nodes/idea/`), `sessions/iter-9012/kid-m/scratch/testrun2/` (pytest
run).

## Unit granularity, and why

**A census unit is "the smallest directory or named file that is one coherent
body of material a thought can attach to as a whole" — never a bare file
count, never a topic label.** Concretely, three rules, applied in this order:

1. **A directory that is itself subdivided into independent packages gets one
   unit per immediate child** (the existing `src_package` rule, generalized).
   `extensions/agi/tests/` fits this: `tests/graph_core/` is the test suite
   for one package, `tests/renderers/` for another — they are independent
   bodies of work that change independently, so five directories become five
   units: `tests-chain-engine`, `tests-embeddings`, `tests-graph-core`,
   `tests-renderers`, `tests-schema-registry`.
2. **A directory that is one coherent, non-subdivided body of material gets
   exactly one unit for the whole directory**, however many files it holds —
   `context/kits/` (6 files: cavekit specs) and `context/refs/` (19 files
   including the nested 16-file `zoom-roundtrip-ground-truth/` tree, picked up
   automatically by prefix matching without decompose-engine.py needing to
   know it exists) are each one unit, not one-per-file and not lumped with
   `context/impl/` or `context/plans/`, which are unrelated bodies of material
   in the same parent directory.
3. **A file whose meaning is independent of its neighbors, or that has no
   directory to itself, gets its own named unit** — the existing
   `NAMED_ENTRY_POINTS` convention, unchanged in kind, extended to cover
   `README.md`, `SKILL.md`, `agent-prompt.md`, and 14 more (full list below).

**Avoiding "too coarse" (one `idea:engine-misc` bucket):** every one of the 27
new units has a `unit_path` a reader can point at and say what it is without
qualification — "the cavekit specs", "the graph-core test suite", "the kid
brief". None of them is a grab-bag of unrelated material. The one unit that
comes closest to a catch-all, `idea:engine-tests` (13 files: `tests/__init__.py`
plus 12 flat `test_*.py` files), is still a real, nameable thing — "the test
suite for the bin/ command layer, plus shared pytest scaffolding" — not an
excuse bucket; see "extensions/agi/tests/" reasoning below for why it can't be
subdivided further without also fixing a separate defect in `level3.py`.

**Avoiding "too fine" (one unit per file):** the 51 files under
`extensions/agi/tests/` do not become 51 units, or even 12 units for the 12
flat test files — they become 6. The 29 files under `context/` do not become
29 units — they become 4. Where I *did* mint one unit per single file
(`README.md`, `TODO.md`, `HANDOFF.md`, …), each is independent of its
neighbors — `README.md` is not part of a `TODO.md` subsystem — so bundling
would be gluing unrelated things together, the coarse failure mode in reverse.
This is the existing `NAMED_ENTRY_POINTS` precedent (`driver.sh`,
`find-root.sh`, `cc-session-start.sh` are three files, three units, because
each is an independent surface), extended rather than reinvented.

**A unit should point at a goal, and not all of them do — named plainly, not
invented.** Where a unit is *explicitly* named by an active goal (`SKILL.md`
and `agent-prompt.md` are named verbatim in `goal:g6.6`'s text as "the
highest-leverage files … and the reason G6.6 exists") or shares a directory
with an already-goalmapped src package (`tests/graph_core/` inherits
`src/graph_core`'s `goal:g7`), the mapping is declared. Where no single
long-term commitment fits — `README.md` and `package.json` both describe the
*whole* project, not one commitment; `.gitignore` and `schema.sql` are
plumbing; the four `autoresearch.*` files are a superseded DB-backed
experiment (`autoresearch.ideas.md`'s own header: "Pruned 2026-04-30") — the
unit is left out of `decompose-engine.goalmap.json` on purpose and reported
`NO_GOAL`, exactly the existing, tested behavior for a unit nobody has
declared a mapping for. 15 of the 27 new units are `NO_GOAL` this way. See the
full table below for which is which and why.

## The units this mints

New `DIR_SUBSYSTEM_PREFIXES` (kind `src_package`, one unit per whole
directory — no further subdivision):

| unit id | unit_path | goal parent | files (measured) |
|---|---|---|---|
| `idea:engine-context-impl` | `context/impl` | *(none — cross-cutting impl log)* | 3 |
| `idea:engine-context-kits` | `context/kits` | *(none — cross-cutting kit specs)* | 6 |
| `idea:engine-context-plans` | `context/plans` | *(none — single planning doc)* | 1 |
| `idea:engine-context-refs` | `context/refs` | `goal:g2` (16 of 19 files are the zoom-roundtrip ground-truth set G2's falsifier cites) | 19 |

`extensions/agi/tests/` (kind `src_package`, `src/`-style: one unit per
immediate subdirectory, plus one catch-all for what's left directly under
`tests/`):

| unit id | unit_path | goal parent | files (measured) |
|---|---|---|---|
| `idea:engine-tests-chain-engine` | `extensions/agi/tests/chain_engine` | `goal:g3` (matches `src/chain_engine`) | 3 |
| `idea:engine-tests-embeddings` | `extensions/agi/tests/embeddings` | `goal:g2` (matches `src/embeddings`) | 4 |
| `idea:engine-tests-graph-core` | `extensions/agi/tests/graph_core` | `goal:g7` (matches `src/graph_core`) | 15 |
| `idea:engine-tests-renderers` | `extensions/agi/tests/renderers` | `goal:g9` (matches `src/renderers`) | 6 |
| `idea:engine-tests-schema-registry` | `extensions/agi/tests/schema_registry` | `goal:g5` (matches `src/schema_registry`) | 9 |
| `idea:engine-tests` | `extensions/agi/tests` (catch-all) | *(none — spans every goal in the bin/ layer, no single fit)* | 13 |

`tests/fixtures/` (13 files, deliberately **not** minted as a unit — see
"Prune safety" note below on why: it is out of the G6.8 payload boundary
entirely, so a unit for it would have zero possible children, forever).

New `NAMED_ENTRY_POINTS` (kind `entry_point`, one file = one unit, existing
convention extended — but see the level3.py caveat in "Dry-run result"):

| unit id | unit_path | goal parent |
|---|---|---|
| `idea:engine-agi-bridge-readme` | `extensions/agi-bridge/README.md` | `goal:g4` (same surface as `index.ts`) |
| `idea:engine-agent-prompt` | `extensions/agi/lib/agent-prompt.md` | `goal:g6.6` (named verbatim in G6.6) |
| `idea:engine-decompose-engine-goalmap` | `extensions/agi/bin/decompose-engine.goalmap.json` | `goal:g6.1` (same as `decompose-engine.py`) |
| `idea:engine-conftest` | `extensions/agi/conftest.py` | *(none — shared pytest fixture infra, no one goal)* |
| `idea:engine-skill-doc` | `skills/agi/SKILL.md` | `goal:g6.6` (named verbatim in G6.6) |
| `idea:engine-readme` | `README.md` | *(none — describes the whole project)* |
| `idea:engine-todo` | `TODO.md` | `goal:g7` (its own header: "archive of how each defect was fixed") |
| `idea:engine-handoff` | `HANDOFF.md` | `goal:g1.5` (its own header: "self-contained… assumes nothing exists locally") |
| `idea:engine-gitignore` | `.gitignore` | *(none — VCS plumbing)* |
| `idea:engine-package-json` | `package.json` | *(none — describes the whole project)* |
| `idea:engine-schema-sql` | `schema.sql` | *(none — superseded DB-experiment schema)* |
| `idea:engine-run-loop-sh` | `run-loop.sh` | *(none — legacy launcher, superseded by `driver.sh`)* |
| `idea:engine-start-sh` | `start.sh` | *(none — legacy launcher, superseded by `driver.sh`)* |
| `idea:engine-autoresearch-sh` | `autoresearch.sh` | *(none — superseded DB-experiment harness)* |
| `idea:engine-autoresearch-md` | `autoresearch.md` | *(none — superseded DB-experiment doc)* |
| `idea:engine-autoresearch-ideas` | `autoresearch.ideas.md` | *(none — its own header says "Pruned 2026-04-30")* |
| `idea:engine-autoresearch-config` | `autoresearch.config.json` | *(none — superseded DB-experiment config)* |

Total: **27 new units**, covering **96 files** (29 context + 50 tests-prefix +
17 named singles), verified by re-deriving `find_parent()` counts directly
(script output above). A 28th file, `extensions/agi/bin/payload_boundary.py`,
already gets a unit and a parent from the **unchanged** `bin_script` loop the
moment `decompose-engine.py` is next run at all — it just hasn't been, since
the file landed after the last real run. I additionally gave it a declared
goal (`goal:g6.8` — it *is* the G6.8 predicate) since I was already touching
the goal map and the mapping is not a guess.

## The change, as applicable code

### 1. `extensions/agi/bin/decompose-engine.py` — three sites

**Site A — constants block.** Insert two new prefix tables between the
existing `SRC_PREFIX`/`BIN_PREFIX` pair and `NAMED_ENTRY_POINTS`, and update
`NAMED_ENTRY_POINTS`'s own list and header comment.

Current:
```python
SRC_PREFIX = "extensions/agi/src/"
BIN_PREFIX = "extensions/agi/bin/"

# Single-file entry points named explicitly rather than discovered by a
# generic "every file in this dir" walk, because some of those directories
# also hold data files that are deliberately not units (e.g.
# extensions/agi/lib/agent-prompt.md — see engine-self-decomposition §1).
# Each entry is (rel_path from engine root, slug, kind). Presence is still
# checked against git ls-files: a removed entry point silently drops out.
NAMED_ENTRY_POINTS = [
    ("extensions/agi/driver.sh", "driver-sh", "entry_point"),
    ("extensions/agi/hooks/cc-session-start.sh", "cc-session-start", "entry_point"),
    ("extensions/agi/lib/find-root.sh", "find-root", "entry_point"),
    ("extensions/agi/scripts/migrate_to_sqlite.py", "migrate-to-sqlite", "entry_point"),
    ("extensions/agi-bridge/index.ts", "agi-bridge-index", "entry_point"),
]
```
Replacement:
```python
SRC_PREFIX = "extensions/agi/src/"
BIN_PREFIX = "extensions/agi/bin/"

# Non-code subsystem directories (G6.8 census widening — goal:g6.8,
# mvp:census-boundary-scope). level3.py's own scan widened to the G6.8
# payload boundary but this script's discovery did not move with it, leaving
# every file below parentless. Each of these directories becomes ONE unit —
# unlike SRC_PREFIX, which groups by the *next* path segment (one unit per
# immediate child package), these four are not further subdivided, because
# each already holds only a handful of files that are one coherent body of
# material (e.g. context/kits/ is one set of kit specs, not several) —
# subdividing further would be one-unit-per-file for a directory this small.
DIR_SUBSYSTEM_PREFIXES = [
    ("context/impl/", "context-impl"),
    ("context/kits/", "context-kits"),
    ("context/plans/", "context-plans"),
    ("context/refs/", "context-refs"),
]

# extensions/agi/tests/ gets the src/ treatment instead of the DIR_SUBSYSTEM
# treatment: one unit per immediate subdirectory (a tests/<pkg>/ directory is
# that package's test suite — the same "directory is a subsystem" logic
# SRC_PREFIX already applies, just rooted at tests/), plus one catch-all unit
# for whatever sits directly under tests/ and is not in a named subdirectory.
# Today the catch-all covers `tests/__init__.py` and twelve flat
# `test_*.py` files, each of which tests a *bin_script* unit — level3.py's
# find_parent() only exact-matches a bin_script, never by directory, so a
# flat test file can't nest under the script it tests the way tests/graph_core/
# nests under src/graph_core. Bundling those twelve under one "tests" unit
# instead of minting twelve near-empty units is the deliberate answer to the
# "too fine" failure mode — see mvp:census-boundary-scope.
# extensions/agi/conftest.py sits one level above this prefix (shared
# fixtures for every test, not any one subsystem's) and is censused
# separately, in NAMED_ENTRY_POINTS below.
TESTS_PREFIX = "extensions/agi/tests/"

# Single-file entry points named explicitly rather than discovered by a
# generic "every file in this dir" walk, because most directories that hold
# one of these also hold data files that should not automatically become
# their own unit merely by co-location (e.g. extensions/agi/lib/find-root.sh
# lives beside extensions/agi/lib/agent-prompt.md).
#
# `agent-prompt.md` was originally the worked example of a file that must
# never become a unit this way — see engine-self-decomposition §1 and the
# regression test that pinned it, test_data_file_next_to_an_entry_point_is_
# not_a_unit. That call predates goal:g6.6 / goal:g6.8, which later and
# explicitly named agent-prompt.md, alongside SKILL.md, as one of the two
# highest-leverage prose surfaces the census must cover — "the reason G6.6
# exists" (GOALS.md, verbatim). It is listed below for that reason now, as
# its own deliberate entry, not by loosening the directory walk — the
# property the old test actually protected (no naive "every file in this
# dir" enumeration) is unchanged: every entry here, including this one, is
# still an individually-decided tuple, never a directory listing. See
# mvp:census-boundary-scope in the graph repo for the fuller argument and the
# test-suite update this requires.
#
# Each entry is (rel_path from engine root, slug, kind). Presence is still
# checked against git ls-files: a removed entry point silently drops out.
NAMED_ENTRY_POINTS = [
    ("extensions/agi/driver.sh", "driver-sh", "entry_point"),
    ("extensions/agi/hooks/cc-session-start.sh", "cc-session-start", "entry_point"),
    ("extensions/agi/lib/find-root.sh", "find-root", "entry_point"),
    ("extensions/agi/scripts/migrate_to_sqlite.py", "migrate-to-sqlite", "entry_point"),
    ("extensions/agi-bridge/index.ts", "agi-bridge-index", "entry_point"),
    ("extensions/agi-bridge/README.md", "agi-bridge-readme", "entry_point"),
    ("extensions/agi/lib/agent-prompt.md", "agent-prompt", "entry_point"),
    ("extensions/agi/bin/decompose-engine.goalmap.json", "decompose-engine-goalmap", "entry_point"),
    ("extensions/agi/conftest.py", "conftest", "entry_point"),
    ("skills/agi/SKILL.md", "skill-doc", "entry_point"),
    ("README.md", "readme", "entry_point"),
    ("TODO.md", "todo", "entry_point"),
    ("HANDOFF.md", "handoff", "entry_point"),
    (".gitignore", "gitignore", "entry_point"),
    ("package.json", "package-json", "entry_point"),
    ("schema.sql", "schema-sql", "entry_point"),
    ("run-loop.sh", "run-loop-sh", "entry_point"),
    ("start.sh", "start-sh", "entry_point"),
    ("autoresearch.sh", "autoresearch-sh", "entry_point"),
    ("autoresearch.md", "autoresearch-md", "entry_point"),
    ("autoresearch.ideas.md", "autoresearch-ideas", "entry_point"),
    ("autoresearch.config.json", "autoresearch-config", "entry_point"),
]
```

**Site B — `discover_units()`, insert before the `bin/*.py` block.**

Current (the boundary point, unchanged text either side kept for anchoring):
```python
    # bin/*.py: direct children of bin/ only, not nested, not __pycache__.
    bin_files = sorted(
        f for f in files
        if f.startswith(BIN_PREFIX) and f.endswith(".py")
        and "/" not in f[len(BIN_PREFIX):]
    )
```
Replacement (new code inserted immediately above, `bin_files` block unchanged
below it):
```python
    # Directory-subsystem units (G6.8 widening): everything under each
    # prefix is one unit. Discovery only has to mint the unit; level3.py's
    # existing longest-prefix-wins find_parent() (unchanged) is what lets a
    # more specific prefix — e.g. a tests/ subdirectory below — win over a
    # broader one without this script needing to know about that resolution.
    for prefix, slug in DIR_SUBSYSTEM_PREFIXES:
        if any(f.startswith(prefix) for f in files):
            units.append({
                "rel_path": prefix.rstrip("/"),
                "slug": slug,
                "kind": "src_package",
                "doc_source": None,
            })

    # extensions/agi/tests/: one unit per immediate subdirectory, one
    # catch-all for whatever sits directly under tests/ itself.
    test_subdirs: set[str] = set()
    has_flat_test_file = False
    for f in files:
        if not f.startswith(TESTS_PREFIX):
            continue
        rest = f[len(TESTS_PREFIX):]
        if "/" in rest:
            test_subdirs.add(rest.split("/", 1)[0])
        else:
            has_flat_test_file = True
    for sub in sorted(test_subdirs):
        if sub == "fixtures":
            # Mirrors payload_boundary.is_test_fixture(): every file under
            # tests/fixtures/ is *out* of the G6.8 payload boundary (synthetic
            # input manufactured for a test harness to read, not a thought —
            # see mvp:payload-boundary-predicate). level3.py never emits a
            # node for any file in there, so a census unit for it would have
            # zero possible children forever. Not minted, on purpose.
            continue
        units.append({
            "rel_path": f"{TESTS_PREFIX}{sub}",
            "slug": f"tests-{sub.replace('_', '-')}",
            "kind": "src_package",
            "doc_source": None,
        })
    if test_subdirs or has_flat_test_file:
        units.append({
            "rel_path": TESTS_PREFIX.rstrip("/"),
            "slug": "tests",
            "kind": "src_package",
            "doc_source": None,
        })

    # bin/*.py: direct children of bin/ only, not nested, not __pycache__.
    bin_files = sorted(
        f for f in files
        if f.startswith(BIN_PREFIX) and f.endswith(".py")
        and "/" not in f[len(BIN_PREFIX):]
    )
```

**Site C — `main()`, the H0/H0i empty-scope guard.**

Current:
```python
        print(f"WARN: engine root {engine_root} is missing or unreadable "
              f"(not a git repo?) — no-op, nothing written or pruned",
              file=sys.stderr)
        return 0

    goal_map = load_goal_map(goal_map_path)
```
Replacement:
```python
        print(f"WARN: engine root {engine_root} is missing or unreadable "
              f"(not a git repo?) — no-op, nothing written or pruned",
              file=sys.stderr)
        return 0

    if not units:
        # H0/H0i guard, matching the one level3.py carries for the identical
        # shape of risk (see mvp:level3-boundary-scope). A real engine repo
        # is never structurally empty of src/ packages, bin/ scripts, and
        # named entry points all at once; a zero-length result here means
        # discovery resolved against the wrong tree, not that the census
        # genuinely has nothing to report. Fail loud and return before
        # written_paths/stale_generated are touched at all — a silent exit-0
        # here is the exact shape that cost this project 29k nodes twice.
        print(f"ERROR: discover_units returned zero units for engine root "
              f"{engine_root} — refusing to treat this as authoritative "
              f"scope; no-op, nothing written or pruned", file=sys.stderr)
        return 1

    goal_map = load_goal_map(goal_map_path)
```

### 2. `extensions/agi/bin/decompose-engine.goalmap.json` — extend `mappings`

Current (tail of the object):
```json
    "extensions/agi/bin/decompose-engine.py": "goal:g6.1",
    "extensions/agi/bin/level3.py": "goal:g2.1",
    "extensions/agi/bin/stitch.py": "goal:g6.1"
  }
}
```
Replacement:
```json
    "extensions/agi/bin/decompose-engine.py": "goal:g6.1",
    "extensions/agi/bin/level3.py": "goal:g2.1",
    "extensions/agi/bin/stitch.py": "goal:g6.1",
    "skills/agi/SKILL.md": "goal:g6.6",
    "extensions/agi/lib/agent-prompt.md": "goal:g6.6",
    "extensions/agi-bridge/README.md": "goal:g4",
    "extensions/agi/bin/decompose-engine.goalmap.json": "goal:g6.1",
    "HANDOFF.md": "goal:g1.5",
    "TODO.md": "goal:g7",
    "context/refs": "goal:g2",
    "extensions/agi/tests/chain_engine": "goal:g3",
    "extensions/agi/tests/embeddings": "goal:g2",
    "extensions/agi/tests/graph_core": "goal:g7",
    "extensions/agi/tests/renderers": "goal:g9",
    "extensions/agi/tests/schema_registry": "goal:g5",
    "extensions/agi/bin/payload_boundary.py": "goal:g6.8"
  }
}
```

Both files pass syntax checks (`ast.parse`, `json.load`) in scratch.

## Prune safety

**Argument.** `discover_units()` only ever *adds* new `if`/`for` blocks that
each independently `append` to `units`; nothing removes or shrinks the
existing `src_package`, `bin_script`, or `NAMED_ENTRY_POINTS` discovery paths,
and no existing `rel_path`/`slug` pair changes. The prune loop in `main()`
still computes `stale_generated` as "stamped `engine-decomp` and not in
`written_paths` this run" — since every previously-written unit is still
written this run (its discovery code is untouched), it can never appear in
`stale_generated` as a side effect of this change.

**New risk, and the guard for it (Site C above).** Before this change,
`discover_units()` returning `[]` (not `None`) was only theoretically
possible if a real engine repo somehow had zero `src/` packages, zero `bin/`
scripts, and zero named entry points simultaneously — `main()` had no explicit
guard for it because it hadn't needed one. Widening the discovery surface
doesn't change that risk's *shape*, but the project's own history (H0, H0b,
H0i, and `level3.py`'s freshly-added identical guard) is that every generator
touching `nodes/` should carry this guard regardless, rather than relying on
"can't happen in practice" — so I added the same one `level3.py` just got.
Verified directly: pointed `--engine-root` at a git repo containing one
untracked-by-any-rule file, `discover_units()` returned `[]`, and `main()`
printed `ERROR: discover_units returned zero units…` and exited 1 — 0 files
written, before touching `written_paths`.

**Verified empirically against the real corpus, not just argued.** Copied the
live `nodes/idea/` (43 files: 27 real `engine-decomp` nodes + 16 hand-authored
`domain-*`/other nodes) into a scratch project and ran the widened script
against it twice:
- Run 1: 55 nodes written (27 pre-existing + `payload-boundary` + 27 new),
  **0 pruned**, all 16 non-`engine-decomp` nodes present and untouched
  (verified: still 16 after, byte-identical filenames).
- Run 2 (idempotence): identical output, **0 pruned** again, node count
  unchanged.

## Dry-run result

Real numbers from `python3 decompose-engine.py --project
sessions/iter-9012/kid-m/scratch/project --engine-root /home/ubuntu/work/agi`
(full logs in that scratch dir):

- **units discovered: 55** (was 28) — `src_package: 16` (was 6), `bin_script:
  17` (unchanged), `entry_point: 22` (was 5)
- **with declared goal parent: 40** (was 27), **flagged NO_GOAL: 15** (was 1 —
  `payload_boundary.py`, now goalmapped too)
- **stale engine-decomp nodes pruned: 0**
- **STALE flags against pre-existing `idea:domain-*` nodes: 0** on the clean
  scratch project; **2** on the real-corpus copy (both are the *advisory*
  token-overlap heuristic matching slightly worse post-widening — it never
  mutates anything; confirmed the flagged files are untouched on disk)

**The number that matters, measured by re-running the unmodified `level3.py`
against this script's output — 102 → 23, not 102 → 0. Here is exactly why, and
it is a second, independent finding, not noise:**

`level3.py`'s `load_census_units()` filters to
`unit_kind not in ("src_package", "bin_script")` — **it silently excludes
`unit_kind == "entry_point"` from ever being matched as a parent.** This is
not something my change introduces or can fix by widening scope; it is a
pre-existing gap in `level3.py` itself, invisible until now because before
G6.8 widened `level3.py`'s own file scope, no in-scope file had ever needed an
`entry_point`-kind parent (`driver.sh`, `find-root.sh`, `cc-session-start.sh`,
`migrate_to_sqlite.py`, and `agi-bridge/index.ts` were all *already*
out-of-scope for `level3.py` before G6.8, for unrelated reasons — see
`level3.py`'s own now-superseded docstring). Verified directly: those five
files already have correct, goalmapped `idea:engine-*` census units *today*,
on the unmodified real repo — `decompose-engine.py`'s scope was never the
problem for them — and they are still in the level-3 `NO_PARENT` list because
`find_parent()` never sees their unit.

Measured, with my change applied and `level3.py` left completely untouched:

- **files scanned: 178, with census parent: 155, flagged NO_PARENT: 23**
- Of the 23: **22 are `entry_point`-kind units that exist, are correctly
  pathed, and are goalmapped where declared** (17 new + the 5 pre-existing
  ones named above) — blocked purely by `level3.py`'s matcher, not by
  anything in this change. **1 is `extensions/agi/src/__init__.py`**, the
  pre-existing, deliberate non-unit (unrelated to this task, matches
  `mvp:level3-boundary-scope`'s own precedent).
- All **79** `src_package`-kind new units (the 4 `context/*` + 6 `tests/*`
  units) resolve immediately, verified per-unit: `context-impl` 3,
  `context-kits` 6, `context-plans` 1, `context-refs` 19, `tests-chain-engine`
  3, `tests-embeddings` 4, `tests-graph-core` 15, `tests-renderers` 6,
  `tests-schema-registry` 9, `tests` (catch-all) 13 — sums to exactly 79.

**I verified the fix, but it is out of scope for this change and I did not
apply it** (my mandate is `decompose-engine.py`; I write one node, not two
engine files). In a throwaway copy of `level3.py` I changed exactly two
conditions —
`load_census_units()`'s kind filter to also accept `"entry_point"`, and
`find_parent()`'s `if u["unit_kind"] == "bin_script"` branch to
`if u["unit_kind"] in ("bin_script", "entry_point")` (an `entry_point` unit
needs the same exact-match semantics a `bin_script` unit does — a
directory-prefix match can never match a single file, which is why simply
adding the kind to the filter alone is not sufficient) — and re-ran: **178
files scanned, 177 with census parent, 1 flagged NO_PARENT** (the deliberate
`src/__init__.py` case, alone). This is a real, two-line, independently
verifiable fix; I am naming it precisely rather than either hiding the gap or
quietly stepping outside my assignment to apply it.

**Bottom line: applying only this node's change, 102 → 23. Applying this
node's change plus the named two-line `level3.py` fix, 102 → 1.**

## Tests affected

Baseline: `python3 -m pytest extensions/agi/tests/test_decompose_engine.py -q`
→ **18 passed** (confirmed before any change, run from the correct directory
depth so `test_default_engine_root_points_at_this_repo`'s path-depth
assertion is meaningful).

After applying the diff, unmodified: **16 passed, 2 failed** — both failures
are the `agent-prompt.md` reclassification, exactly as expected, nothing else
moved (`DIR_SUBSYSTEM_PREFIXES` and `TESTS_PREFIX` never match anything in
`test_decompose_engine.py`'s small synthetic `ENGINE_FILES` fixture, so that
code path is silent in this suite — it is only exercised by the real-repo run
above):

- `test_discovers_expected_units_with_kinds_and_scale` — its expected `ids`
  set needs `"idea:engine-agent-prompt"` added.
- `test_data_file_next_to_an_entry_point_is_not_a_unit` — its entire premise
  (agent-prompt.md must never become a unit) is superseded by `goal:g6.6` /
  `goal:g6.8`, which later and explicitly named it as required coverage. It
  needs replacing, not just patching — see below for exact replacement text,
  verified to restore full green (**19 passed** after applying).

Exact fixture + test changes (verified in
`sessions/iter-9012/kid-m/scratch/testrun2/`):

**`ENGINE_FILES` fixture** — current entry:
```python
    "extensions/agi/lib/agent-prompt.md":
        "# Not a code surface, must never become a unit.\n",
```
Replacement (content updated to match new reality, plus a new sibling fixture
file to keep covering the "no naive directory walk" property the original
test protected):
```python
    "extensions/agi/lib/agent-prompt.md":
        "# The kid brief. Named explicitly in NAMED_ENTRY_POINTS -- goal:g6.6.\n",
    "extensions/agi/lib/notes.md":
        "# Incidental notes file, never named -- must not become a unit merely "
        "by sitting beside find-root.sh / agent-prompt.md.\n",
```

**`test_discovers_expected_units_with_kinds_and_scale`** — the expected `ids`
set gains one entry:
```python
        "idea:engine-agi-bridge-index",
```
becomes
```python
        "idea:engine-agi-bridge-index", "idea:engine-agent-prompt",
```

**`test_data_file_next_to_an_entry_point_is_not_a_unit`** — current:
```python
def test_data_file_next_to_an_entry_point_is_not_a_unit(project, engine):
    run(project, engine)
    nodes = idea_nodes(project)
    assert not any("agent-prompt" in nid for nid in nodes)
```
Replacement (one test renamed/repurposed around the new sibling fixture, one
new test added asserting the new intent):
```python
def test_data_file_next_to_named_entry_points_is_not_a_unit(project, engine):
    """A file living beside a NAMED_ENTRY_POINTS entry is still not swept in
    by a generic directory walk -- discovery is always an explicit,
    individually-decided tuple, never "every file in this dir".

    agent-prompt.md was the original worked example of this rule (see
    engine-self-decomposition Section 1) until goal:g6.6/goal:g6.8 named it,
    alongside SKILL.md, as one of the two highest-leverage prose surfaces the
    census must cover -- so it graduated to a named entry of its own (see
    test below). notes.md takes over as the unnamed-sibling regression case.
    """
    run(project, engine)
    nodes = idea_nodes(project)
    assert not any("notes" in nid for nid in nodes)


def test_agent_prompt_is_a_named_entry_point(project, engine):
    """goal:g6.6/goal:g6.8 named agent-prompt.md, alongside SKILL.md, as one
    of the two highest-leverage prose surfaces the census must cover -- "the
    reason G6.6 exists" (GOALS.md, verbatim). It is a NAMED_ENTRY_POINTS entry
    like find-root.sh now, not swept in by a directory walk.
    """
    run(project, engine)
    _path, fm = idea_nodes(project)["idea:engine-agent-prompt"]
    assert fm["unit_kind"] == "entry_point"
    assert fm["unit_path"] == "extensions/agi/lib/agent-prompt.md"
```

No other test in `test_decompose_engine.py` needed a change — the other 16
pass unmodified both before and after.

`test_level3.py` and `test_stitch.py` are untouched by this change (I did not
modify `level3.py`) and were not re-run for this task; they were already
exercised by `mvp:level3-boundary-scope`.

## What still has no parent, and why that is correct

Of the 102 files this task set out to close:

- **1 — `extensions/agi/src/__init__.py`.** Deliberately not a unit;
  `discover_units()`'s own src_package loop explicitly skips a stray file
  directly in `src/`. Pre-existing, unrelated to this task, matches
  `mvp:level3-boundary-scope`'s own documented exception.
- **22 — every `entry_point`-kind unit, old and new alike.** Each of these
  has a real, correctly-pathed, (where declared) correctly-goalmapped census
  unit *right now*, on the unmodified real repo, after this change is
  applied. They remain in `level3.py`'s `NO_PARENT` list solely because
  `load_census_units()` filters out `unit_kind == "entry_point"` — a second,
  independent bug, fully diagnosed and fixed in a throwaway copy (see
  "Dry-run result"), but out of scope for this node to apply, since my
  mandate was `decompose-engine.py` and I write exactly one file. This is
  worth a `§B` row and a two-line follow-up in `level3.py`; I am not filing
  it myself since I have no spec-writing tool in this task, only naming it
  precisely enough that the parent or a future kid can act on it without
  re-deriving the diagnosis.

Every other file in the original 102 — 79 of them — has a parent it did not
have before, verified by direct re-derivation of `find_parent()`'s output
against the real repo, not estimated.