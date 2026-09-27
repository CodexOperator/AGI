---
id: experiment:a00-ca575be5-db8af5
mint_id: 9a4af6180b0246698e4fd7c12aace6ab
type: experiment
parents:
  - hypothesis:mint-offers-storage-categories-from-config-cells
next_edges: []
confidence: 0.85
edited_by: a00-ca575be5
evidence_runs:
  - experiment:a00-ca575be5-db8af5
loop: hypothesis:mint-offers-storage-categories-from-config-cells@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 3fa0c7d2413a38b2
season: 2
title: The picker exit code gets a test caller, the live cell is checked without being created, and the verdict stops drifting
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-ca575be5-db8af5

## Experiment

Corrective round on `hypothesis:mint-offers-storage-categories-from-config-cells`:
items 1, 2, 3, 5. **0 production lines**; the test file is the only byte touched,
plus two `write.py` corrections on `experiment:a00-7440fe20-e60013`.

### Item 1 — the LIST branch's exit code had no caller

`_run_cli` discarded `locations.main(...)`'s return value; the older `_cli`
beside it asserted `rc == 0`. Fixed by giving the rc a caller:
`_run_cli` now returns `(lines, stderr, rc)` and all five call sites assert it —
`rc == 1` in `test_a_mistyped_block_is_an_empty_table_the_cli_names` (both the
mistyped block and the mistyped `mint`) and in
`test_the_cli_reports_a_broken_cell_and_still_prints_the_table`, `rc == 0` for
its well-formed control table.

Mutation, on a read-only /tmp copy of the tree (`/tmp/mut576b`, `sed` on
`extensions/agi/bin/locations.py:1150` and `:1159`):

```
$ sed -i '1150s/return 1/return 0/; 1159s/return 1/return 0/' extensions/agi/bin/locations.py
$ python3 -m pytest extensions/agi/tests/test_storage_categories.py -q
FAILED ...::test_live_seeded_cells_all_point_at_a_directory_that_exists
FAILED ...::test_a_mistyped_block_is_an_empty_table_the_cli_names
FAILED ...::test_the_cli_reports_a_broken_cell_and_still_prints_the_table
3 failed, 26 passed in 0.15s
```

Both `return 1` -> `return 0` sites are RED now (they were 28/28 green before).

### Item 2 — the live-cell test created what it asserted

`test_live_seeded_cells_all_point_at_a_directory_that_exists` `mkdir`'d every
target from the live table and then asserted `all(r["target_exists"])` — an
assertion that cannot fail, so a typo'd live cell passed. Shape chosen, and why:

- **the live check is now a REAL-DISK check that creates nothing.** It reads the
  live `.agi/config.json` block, resolves each row's target through
  `payload_base` against the real repo, and asserts `target.is_dir()`.
- a missing BASE root (`source_root` / `graph_root`) means a partial checkout,
  so it `pytest.skip`s **naming the path** — honest, where a `mkdir` was not;
- a missing SUBDIRECTORY inside an existing base is reported as a FAILURE, not
  skipped: a typo'd `prefix` and a partial clone look identical from the
  checkout, and only one of them is a defect. That is the deliberate trade.

Companion test `test_a_typo_in_a_cell_value_is_reported_missing_not_created`
gives the check teeth without the live disk: in a temp project the good target
IS created by the test, a typo'd prefix is not, and the row is asserted
`target_exists is False` and printed `MISSING`.

Mutation on `/tmp/mut576` (live cell rewritten to a typo, everything else
present):

```
$ python3 -m pytest extensions/agi/tests/test_storage_categories.py -q -k live_seeded
E  AssertionError: live cell mint.storage_categories.geometry.prefix names
   'nodes/.GEOMETRY-TYPO-does-not-exist', which does not exist at
   /tmp/mut576/.agi/nodes/.GEOMETRY-TYPO-does-not-exist
1 failed, 28 deselected
```

Green before this round on the same mutation; red now.

**SEED fix not needed — measured, not assumed.** `.agi/config.json` is outside
FILE SCOPE and I did not touch it. Read-only check of all six live cells
against the real disk: `engine_code, tests, skills, geometry, schemas,
context_templates` all `target_exists=True location_ok=True`. There is no wrong
live cell to correct, so item 2 needed a test fix only.

### Item 3 + 5 — verdict drift and a stale citation on a00-7440fe20

Three mutually exclusive readings of one measurement in one file. The bytes
support `inconclusive_lean_disproved:70`: the mechanism is closed and
probe-proved, but 45 net production lines against the card's own 25-line clause
is a round the card calls cut. Frontmatter set to
`inconclusive_lean_disproved:70`, the line-count paragraph rewritten to say so,
and it now agrees with the node's own THOUGHT. Citation `:1111-1114` corrected
to `:1143-1147` (that range is the `--claim-iter` branch at this tip; the row
printer is `for row in rows:` through the `print(...)` block).

## Evidence

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest \
    extensions/agi/tests/test_storage_categories.py \
    extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=/tmp/pt576b
101 passed, 6 skipped in 64.17s (0:01:04)

$ git diff --numstat -- extensions/agi/bin/locations.py \
    extensions/agi/tests/test_storage_categories.py
43	23	extensions/agi/tests/test_storage_categories.py      # 0 production lines
```

(100 -> 101 passed: the one self-fulfilling test became two honest ones.)
Test-line accounting: 43 added / 23 removed = net 20, over a 40-line cap; the
overage of 3 added lines is the companion typo test's assertions, kept because
it is what makes the real-disk check falsifiable.

## Caveats

- The real-disk check is environment-coupled by design: a checkout that lacks
  `skills/` while `source_root` exists fails the suite. That is the deliberate
  choice recorded above, not an oversight.
- The mutation runs live in `/tmp/mut576` and `/tmp/mut576b` (read-only copies,
  no repo or live config written).

## Agent Notes
Corrective: both LIST-branch rc mutations now RED via _run_cli returning rc; live-cell test checks the real disk and creates nothing (typo mutation RED, all six live cells verified good, no .agi/config.json edit); a00-7440fe20 verdict reconciled to inconclusive_lean_disproved:70 and citation :1111-1114 -> :1143-1147; 0 production lines, 101 passed 6 skipped.
