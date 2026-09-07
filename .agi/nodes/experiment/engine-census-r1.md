---
id: exp:engine-census-r1
mint_id: ceedcf5c28df4448be9f96455578300d
type: experiment
parents:
  - hyp:engine-census-generated
confidence: 0.8
edited_by: season.py
evidence_runs: 1
season: 1
tags:
  - engine
  - l19
thought_session: season
title: Engine census generator, first run
---
**Built:** `extensions/agi/bin/decompose-engine.py`, plus a declared-mapping
side file `extensions/agi/bin/decompose-engine.goalmap.json` (checked in,
currently `{"mappings": {}}`) and 18 tests in
`extensions/agi/tests/test_decompose_engine.py`.

Seeds units from `git -C <engine root> ls-files` (never GitNexus, never a live
`os.walk` — grouping the tracked-file list by path prefix is the "directory
walk"), classifying by fixed rule: every top-level dir under
`extensions/agi/src/` with a tracked file is a `src_package`; every tracked
`.py` directly under `extensions/agi/bin/` is a `bin_script`; five named
single-file paths (`driver.sh`, `hooks/cc-session-start.sh`,
`lib/find-root.sh`, `scripts/migrate_to_sqlite.py`,
`extensions/agi-bridge/index.ts`) are `entry_point`s, present only if
`git ls-files` still lists them. Docstrings/headers are extracted with `ast`
for `.py`, a leading `#`-comment block for `.sh`, a leading `/** */` block for
`.ts`; a surface with none gets "No module docstring or header comment was
found for this surface" rather than an invented sentence.

`write_frontmatter` is imported by file path from `snapshot-goals.py` and
called unmodified with `preserve=existing_fm` — not re-implemented, per H0i.
Pruning is scoped to `origin: engine-decomp` only; a missing or non-git engine
root returns before touching the filesystem at all (verified by test, not just
by reading the code).

**Run 1 — dry-run**, `--project /home/ubuntu/work/agi-tree`:

```
units discovered: 23
  bin_script: 12
  entry_point: 5
  src_package: 6
nodes would write: 23
  with declared goal parent: 0
  flagged NO_GOAL (parentless): 23
stale engine-decomp nodes would prune: 0
STALE flags against pre-existing idea:domain-* nodes: 4
```

**Run 2 — for real**, same project. Wrote 23 files under `nodes/idea/`
(`engine-agi-algos.md` … `engine-zoom.md`). Same counts as the dry run.
`git status --short -- nodes/` went from 1 untracked file (another agent's
`nodes/hypothesis/level3-node-anatomy.md`, left alone) to 24.

**Run 3 — re-run, unchanged engine**, to check the falsifier directly. Copied
`nodes/idea/` to a scratch dir first, ran again, `diff -rq` against the copy:
**zero differences, all 23 files byte-identical.** `git status --short --
nodes/` still reports the same 24 untracked paths — no new file, no deleted
file. `git diff --stat -- nodes/` is empty, but that check is weak here on its
own: these are untracked paths and plain `git diff` never shows untracked
files regardless of whether content changed, so the `diff -rq` byte comparison
is the load-bearing check, not the git-diff instruction as literally stated.
Worth recording as a gap in the brief's own verification instruction, not in
the script.

**Against the pre-registered numbers:**

| Pre-registered | Measured | Match |
|---|---|---|
| 23 units | 23 (6 src, 12 bin, 5 entry) | yes |
| 0 units with a goal parent | 0 (23/23 `NO_GOAL`) | yes |
| second run byte-identical | confirmed via `diff -rq` | yes |

All three hold. The two hard falsifiers (non-empty second-run diff; a rename
not retired same-run) were not triggered — the engine did not change between
runs 2 and 3, so the rename case is untested by this run and stays open for a
future one. The 79%-of-generated-ideas-have-a-child statistical falsifier
needs 20 iterations and cannot be read yet; recorded here only as the number
to check later, not as evidence either way.

**Deviations and surprises, reported honestly:**

- **The unit -> goal mapping table is empty, on purpose, and that is the
  correct first-run outcome, not a shortcut.** No mapping exists anywhere in
  this repo — not even the 5 alive hand-written `domain-*` nodes carry
  `parents:` — so declaring one myself would have been exactly the guess the
  brief forbids. All 23 generated nodes are parentless and flagged `NO_GOAL`.
  This is a real gap, not a cosmetic one: it means none of this run's nodes
  feed `outcome_coverage` today. Filling `decompose-engine.goalmap.json` is
  follow-up work for a human or a verdict, not something this script should
  have decided.
- **The STALE heuristic missed one of the two nodes the parent idea called
  unambiguous.** `idea:domain-environment-indexers` — named directly in
  `idea:engine-self-decomposition` as a module that no longer exists — was
  **not** flagged. Its tokens (`environment`, `indexers`) false-matched
  `agi-bridge-index`'s token `index` via substring containment (`"index" in
  "indexers"`). The other unambiguous one, `domain-exporters`, was flagged
  correctly. This is a real miss in the heuristic, not a rounding error: a
  human trusting the `STALE:` output alone would not catch this one. Recorded
  as a known limitation rather than silently patched around, since the
  heuristic is explicitly advisory and the brief asks for judgement calls to
  be surfaced, not resolved by the generator.
- **`DEFAULT_ENGINE_ROOT` was wrong by one directory level on the first
  attempt** (`BIN_DIR.parents[3]` resolved to `/home/ubuntu/work` instead of
  the repo root, because `BIN_DIR` is already `.../extensions/agi/bin`, not
  the file itself). Caught immediately by running the dry-run against the
  real repo — it printed the missing-engine-root no-op message instead of a
  count. Fixed to `parents[2]` and pinned with a dedicated test
  (`test_default_engine_root_points_at_this_repo`) so a future refactor of the
  file's location trips a test instead of silently pointing outside the repo.
  Every test written before that point had passed anyway, because every test
  passes `--engine-root` explicitly and never exercises the default — worth
  naming as a gap in the test suite's own coverage, not just in the script.
- No sqlite persistence path was wired in (`snapshot-goals.py`'s
  `_upsert_node_to_db`), because `agi-tree`'s config has no `persistence` key
  and the filesystem write is what this project reads. Left out rather than
  added untested.

**Test suite:** 18 new tests in `test_decompose_engine.py`, all passing. Full
engine suite: `324 passed, 1 failed` — the failure is the pre-existing
`test_field_set_is_exactly_six` (an unrelated `Node` dataclass field-count
assertion, failing before this work started), exactly the one known failure
this task was told to expect.