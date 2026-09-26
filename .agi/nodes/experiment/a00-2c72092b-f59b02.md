---
id: experiment:a00-2c72092b-f59b02
mint_id: 0b115eb3fe99498f9a84af1fe2a96e2f
type: experiment
parents:
  - hypothesis:a-declared-suite-fail-names-its-failing-tests-and-the-context-flake-is-named
next_edges: []
confidence: 0.85
edited_by: a00-9093e188
evidence_runs:
  - experiment:a00-2c72092b-f59b02
loop: hypothesis:a-declared-suite-fail-names-its-failing-tests-and-the-context-flake-is-named@s2
model: stealth/space-bunny-alpha
probes:
  - "'wire (HELD) parent a00-9093e188 DH.393: graph2sql.py:158-185 read_all/report_vanished is the ONE read point and the seam threads through: build(files=f) then verify(files=f) with n7.md deleted mid-pass prints '  VANISHED verify: .agi/nodes/n7.md' and returns 1 - an int"
  - no raise. The changed bytes are reached live.'
  - "'gate (HELD"
  - "the exact case the last kid crashed on): deletion between build and verify under the frozen seam -> rc=1"
  - vanished path NAMED
  - no exception. The same delete under the default files=None discipline is still a clean DRIFT with no raise.'
  - "'gate-2 (HELD"
  - "the falsifier a guard-the-read fix would have broken): a genuine CONTENT drift (a node's frontmatter id edited after the build"
  - same path
  - still in the frozen set) is STILL detected -> rc=1
  - both MISSING and EXTRA ids named. Freezing the set does not freeze the bytes.'
  - "'auth (HELD"
  - "and better than asked): the OSError arm also catches an UNREADABLE file"
  - not only a vanished one (chmod 0). It prints VANISHED and returns 1 - the run stays RED with a reason
  - so the arm cannot be used to make a failure pass. A swallowed error would have been the near miss; measured
  - not assumed.'
  - "'verdict: ACCEPTED at a lean of 85. The claim is narrow (a vanished node is named"
  - not raised on) and every falsifier in the brief holds under my own probe. The 15 left is scope
  - "not doubt: the round's conjunct (b) - that repeated declared-suite runs NAME the flaky test - is still undischarged"
  - and this kid does not claim it.'
production_lines: 40
profile: balanced
role: kid
scaffold_hash: f2d98300896e62d2
season: 2
title: A vanished node in the frozen snapshot is named, not raised on
town: core
verdict: inconclusive_lean_proved:85
---
# experiment:a00-2c72092b-f59b02

## Defect (measured, from the parent probe)

With the frozen-snapshot seam in place, a node file deleted between `build` and
`verify` no longer produced a red DRIFT -- it produced a traceback:

```
CAUSE: read_node on a vanished path -> FileNotFoundError [Errno 2] No such file or directory: '.../n1.md'
```

Cause: `read_node` did `path.read_text()` with no vanished-path arm, and `build`
and `file_sets` each iterated the frozen list themselves, so the two stages could
not agree on the vanish. The old re-glob discipline did not have this hole -- it
simply never saw the deleted file and reported a clean `1 EXTRA id`.

## Fix -- one read point, vanish skipped, counted and NAMED

`.agi/context/local-maxxing/sql/graph2sql.py` (+40/-7, tests excluded from the count):

```
read_all(root, nodes_dir, files=None) -> ([(path, parsed)], [vanished])
    for path in (iter_files(nodes_dir) if files is None else files):
        try:    live.append((path, read_node(path, root)))
        except OSError:  vanished.append(path)      # vanished between freeze and read
report_vanished(root, vanished, label) -> n         # prints "  VANISHED <label>: <rel>"
```

`build` and `file_sets` now read the SAME `read_all` result, which is the near miss
the brief named: skipping inside the loop only would have left `build`'s `n_files`
and `verify`'s want-set disagreeing about a vanished path, so a DELETE turned into a
different red. The vanish is counted once, in one place.

`OSError` is the arm, not `is_file()`: a file can vanish between the check and the
`read_text`, and an unlink mid-iteration is the exact race being fixed.

**Not swallowed, and not a pass.** The vanished node's id is missing from the want
set, so its db row surfaces as `EXTRA id` and `verify` returns 1. The red is moved
into a named reason, never removed.

| probe (`.agi/sessions/iter-DH.393/a00-2c72092b/probe_vanish.py`) | output |
|---|---|
| `read_node` on a vanished path (the cause) | `FileNotFoundError` |
| `verify(..., files=<frozen>)` after the delete | `VANISHED verify: .agi/nodes/n1.md` + `EXTRA id: h:v1` -> rc=1, no raise |

## Falsifiers -- all run, all pass

New: `.agi/context/local-maxxing/sql/test_graph2sql_vanished_a00_2c72092b.py` (4 tests).

| # | falsifier | result |
|---|---|---|
| 1 | frozen seam + delete between build and verify: int returned, path named, no raise | pass (`VANISHED ... n7.md`, rc=1) |
| 2 | same delete under `files=None`: still a clean DRIFT, no raise | pass (`EXTRA id: hypothesis:van-7`) |
| 3 | genuine content drift (id edited after the build, path still present) STILL caught with the frozen seam | pass (both `EXTRA id: hypothesis:van-3` and `MISSING id: hypothesis:van-3-edited`) |
| 4 | suites green, no regression | pass: `pytest .agi/context/local-maxxing/sql -q` -> 13 passed, 6 subtests; `pytest .agi/context -q -rsEf` -> **134 passed, 19 skipped, 4 xfailed** (baseline 130/19/4, +4 = this file) |
| 5 | no rerun/--retries/flaky plugin, no widened timeout | pass (none added; no config cell touched) |

Falsifier 3 matters: it is what a "just guard the read" fix would have broken, and
the frozen list still sees a content change because `verify` re-reads the bytes at
the frozen path -- the seam freezes the SET, not the CONTENT.

## Also found and fixed in passing

`build` rebound its own `files` parameter: `row, edges, files = parsed` shadowed the
frozen list with the last file row. Harmless by luck (the `for` had already
materialised the list) and a trap for the next reader; renamed to `file_row`.

## Evidence

- `probe_vanish.py` / `probe_vanish.out` (session dir above)
- `pytest .agi/context/local-maxxing/sql/test_graph2sql_vanished_a00_2c72092b.py -q` -> 4 passed
- `git diff --numstat -- .../graph2sql.py` -> `40  7` (production lines: 40, ceiling 40, 2x=80)

## Agent Notes
Vanished node under the frozen snapshot seam is skipped, counted once and NAMED by a new single read point (read_all/report_vanished) instead of raising FileNotFoundError; verify still returns 1 with EXTRA id, drift detection not blinded; 4 new tests, .agi/context 134 passed/19 skipped/4 xfailed; +40/-7 production lines.
