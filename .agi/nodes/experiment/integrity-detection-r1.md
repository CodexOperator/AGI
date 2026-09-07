---
id: exp:integrity-detection-r1
mint_id: 98be4becff9543fd886605b5da0e85a2
type: experiment
parents:
  - goal:g7.1
confidence: 0.8
edited_by: season.py
evidence_runs: 1
season: 1
tags:
  - integrity
  - g7.1
  - g7.2
thought_session: season
title: Duplicate-id and dangling-parent detection
---
Closed both silent-integrity holes G7 named: G7.2 (duplicate ids hide files)
and G7.1 (dangling parent references go unchecked outside `goal:`). Both
fixes are detection-only — no node under `nodes/` was touched, merged, or
re-ided.

**G7.2 — `extensions/agi/src/graph_core/loader.py`, `load_directory`.** The
existing walk already does `if not g.has_node(id): add; else: <dropped
silently>`. Reused that exact branch point instead of adding a second pass:
the `else` now records `(id, kept_path, hidden_path)`, prints
`WARN: duplicate node id '<id>': kept <path>, hidden <path>` to stderr, and
appends to a local list. Added `strict: bool = False`; non-strict prints and
continues (loop never breaks), `strict=True` prints the same warnings then
raises a new `DuplicateIdError(GraphCoreError)` once the full pass
completes, so a strict caller sees every collision, not just the first hit.
The collected list is also exposed as `graph.duplicate_ids` on the returned
`Graph` — the function's `(Graph, list[LoadedNode])` return shape is
unchanged, so every caller that does `g, loaded = load_directory(...)`
(`render-context.py`, `metrics.py`, `dashboard.py`, `zoom.py`, `dispatch.py`,
`post_wire.py`) keeps working untouched.

**G7.1 — `extensions/agi/bin/snapshot-goals.py`.** `collect_parent_refs`
used to filter to `parents:` entries matching `^goal:`; the filter is gone,
so it now maps every referenced id (any prefix) to its referencing node ids.
The integrity loop in `main()` now checks every ref against
`known_ids = existing.keys() | goal_ids` instead of only goal ids against
`goal_ids`. `goal:`-prefixed dangling refs keep the exact original message
(`INTEGRITY: <path> references unknown goal '<id>'`) for backward
compatibility with the established contract; every other dangling ref gets
`INTEGRITY: <path> references unknown parent '<id>'`. Added one
classification on top: build a `rest_index` (id text after the first `:`) →
`[ids]` over `known_ids`; if a dangling ref's rest matches a *different*
prefix that does exist, it's a probable typo'd prefix and the message
becomes `... (possible prefix typo — did you mean '<id>'?)`, counted
separately from genuinely-missing refs. `--strict`/exit-0-by-default is
unchanged, now covers all refs, not just goals — same mechanism, wider
scope, no second mechanism invented.

**Measured against the real corpus** (`/home/ubuntu/work/agi-tree`):

- **Duplicate ids: 17 detected, 17 files hidden** — ran the patched
  `load_directory` read-only against `nodes/` (no writes, safe against the
  live corpus). Matches G7.2's own examples exactly:
  `app-purpose:graph-core` kept 276B / hid 575B;
  `bigger-outcome:graph-core-r1` kept 315B / hid 1,217B. 539 files loaded,
  17 hidden, 1 separate parse failure (below) — 539+17+1 = 557 total `.md`
  files under `nodes/`.
- **Dangling parent references: 88 detected — 22 prefix-mismatch (with a
  suggested id), 66 genuinely missing.** Measured by running
  `snapshot-goals.py --project <tmp copy of agi-tree>` (never the live
  corpus, per the no-writes-to-corpus rule) with and without `--strict`;
  `--strict` exits 1, default exits 0. Confirmed `hyp:`/`hypothesis:` is
  the dominant prefix-mismatch pattern G7.1 named, e.g.
  `hypothesis:chain-engine-r1-r1` → suggests `hyp:chain-engine-r1-r1`.

**Deviation worth flagging, found while measuring, not by reading code:**
an independent raw scan (plain regex + `yaml.safe_load` over every file,
bypassing `snapshot-goals.py`'s own node-loading entirely) finds **89**
dangling refs, not 88 — matching the count G7.1 itself cites. The missing
one is `t-090-bfsdfs-traversal-primitives.md → hyp:graph-core-r11`. Cause:
`load_existing_nodes()` in `snapshot-goals.py` — the function that builds
the `existing` dict the whole integrity check reads from — has its *own*,
separate silent duplicate-id collapse: `nodes[node_id] = {...}` in a plain
loop over `sorted(NODES_DIR.rglob("*.md"))`, so the *last*-sorted file with
a given id wins, opposite of `load_directory`'s first-wins. `task:t-090` is
one of the 17 duplicate ids above; its two files disagree on `parents:`, and
`load_existing_nodes()` silently keeps the wrong one (`...schema-as-file-
with.md`, sorts last) over the one with the dangling ref
(`...bfsdfs-traversal-primitives.md`, sorts first) — so that file's own
dangling parent reference never reaches the check at all. This is G7.2's
exact defect shape recurring in a second, independent loader, and it makes
G7.1's count quietly wrong by exactly the number of duplicate-id pairs whose
`parents:` differ. I did not fix it: `load_existing_nodes()` is not
`load_directory`, fixing it would mean building a second duplicate-detection
mechanism inside `snapshot-goals.py` (which G7.1 explicitly rules out —
"Do not invent a second mechanism"), and the two-file scope given here was
`load_directory` for G7.2. Flagged separately for a follow-up decision:
either point `load_existing_nodes()` at `load_directory` (one mechanism,
shared) or teach it the same first-wins-and-report behaviour independently.

**Second deviation, same category:** the parse failure above
(`nodes/hypothesis/a00-1467544f-chain-600hop.md`) has a `- "exp:..."` line
stray between `id:` and `parents:`, breaking YAML block-mapping parsing.
Both `load_directory` (`except Exception: continue`) and
`load_existing_nodes()` (`except Exception: pass`) swallow this with zero
signal — a third, distinct way for `nodes/` content to go invisible to every
tool, not covered by either G7.1 or G7.2's stated scope (duplicate ids /
dangling parents). Left as-is and flagged separately; fixing bare
except-and-continue parse-failure reporting is its own decision, not a
detection-scope extension of either assigned defect.

**Tests added:** `extensions/agi/tests/graph_core/test_loader.py` (new, 9
tests: no-op on no duplicates, first-sorted-file-still-wins, collision
recorded with correct kept/hidden paths, stderr warning format, default
mode never raises, strict raises `DuplicateIdError` with all collisions
attached, strict-with-no-duplicates is silent, 2-tuple return shape
preserved). `extensions/agi/tests/test_snapshot_goals.py` (+7 tests: non-goal
dangling ref warns and exits 0, fails under `--strict`, a known non-goal ref
is not flagged, prefix-mismatch reported with the correct suggestion using
the corpus's own `hyp:`/`hypothesis:` example, a genuinely-missing ref gets
no fabricated suggestion, the original `goal:` message wording is unchanged
byte-for-byte, and the stdout summary line splits prefix-mismatch from
missing correctly).

**Suite: 400 passed, 0 failed** (`cd /home/ubuntu/work/agi && python3 -m
pytest extensions/agi/tests -q`) — the pre-existing 384 plus the 16 added
here. No test outside the two owned files changed behaviour.

**Scope discipline:** did not touch `dashboard.py`'s own `find_duplicate_ids`
(a second, independent full-text scan for the same problem, already
present) — out of ownership, and `graph.duplicate_ids` now gives it a
cheaper path if a future change wants to use it instead. Did not delete,
merge, or re-id any of the 17 duplicate-id files or resolve any of the 88
dangling refs; both remain exactly as found on disk. Ran
`gitnexus_impact` on `load_directory` before editing (0 impacted, LOW —
the static call graph only sees the test files as callers; the `bin/*.py`
callers use dynamic `sys.path` imports GitNexus doesn't trace, so they were
checked by hand via grep instead) and `gitnexus_detect_changes` after
editing, which reported HIGH risk purely from line-number shift in a stale
index (symbols below the new class/import lines got flagged as "touched"
though their bodies are byte-identical) — not a real behavioural risk;
the green 400/400 suite is the actual signal.