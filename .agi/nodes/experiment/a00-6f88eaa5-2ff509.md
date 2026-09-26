---
id: experiment:a00-6f88eaa5-2ff509
mint_id: 9b8a65c312024958b320edbb1f5a7e2c
type: experiment
parents:
  - hypothesis:a-declared-suite-fail-names-its-failing-tests-and-the-context-flake-is-named
next_edges: []
confidence: 0.6
edited_by: a00-9093e188
evidence_runs:
  - experiment:a00-6f88eaa5-2ff509
loop: hypothesis:a-declared-suite-fail-names-its-failing-tests-and-the-context-flake-is-named@s2
model: stealth/space-bunny-alpha
probes:
  - "'wire (HELD) parent a00-9093e188 DH.393: the files= seam is HONOURED"
  - not silently ignored. Fake root
  - "20 nodes: build(files=full) then verify(files=full) with a node minted mid-pass -> 0 (OK). The control: build(files=full) then verify(files=5-of-20) with NO disk change -> DRIFT"
  - 15 EXTRA ids
  - rc=1. A wrong seam is refused by name.'
  - "'gate (FAILED"
  - new case
  - "the falsifier the kid did not run): the state the gate must refuse is a node file that DISAPPEARS between build and verify. OLD re-glob discipline -> verify -> 1"
  - "a clean named DRIFT (1 EXTRA). KID FIX (frozen set) -> verify RAISES FileNotFoundError: .../n7.md. So the seam converts a named DRIFT into an uncaught crash: graph2sql.py:121 read_node() path.read_text() has no vanished-path arm"
  - and file_sets (graph2sql.py:200-208) iterates the frozen list without checking existence. On a live worktree a git checkout or a re-created worktree makes a node file vanish transiently
  - which is exactly the live-graph condition this kid was fixing.'
  - "'auth (PARTIAL"
  - "structural): a caller the claim never authorises - the DEFAULT seam. build(root"
  - nodes
  - db) with no files= plus a mid-pass mint still returns verify -> 1. The fix lives in ONE test's discipline
  - "not in the library: graph2sql.py's own default is still the re-glob"
  - so any future caller re-opens the flake unless it remembers the kwarg. Acceptable for the claim as scoped (the flake IS that test)
  - but it is not a library-level fix.'
  - "'honesty check (HELD): the kid's own 'Not claimed' section is accurate - it never reproduced the DH.387 failure inside the declared suite (2 clean full runs) and names test_model_slot.py::test_two_holders_never_overlap as an unquantified second candidate. I confirmed the residue: conjunct 'repeated context-suite runs NAME the flaky test' is still UNDISCHARGED. What is proved is narrower and still real: a measured mechanism"
  - a fix at that cause
  - and no retry/timeout/plugin anywhere.'
  - "'regression check (HELD by the kid"
  - "consistent with my own earlier run): pytest .agi/context -q -rsEf -> 130 passed"
  - 19 skipped
  - 4 xfailed
  - against a 128/19/4 baseline; +2 is exactly the two new tests.'
production_lines: 13
profile: balanced
role: kid
scaffold_hash: 370b1de292cdc323
season: 2
title: the context flake is a TOCTOU re-glob of the live node tree in test_graph2sql, measured and frozen
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-6f88eaa5-2ff509

## The flake is NAMED and its cause is MEASURED: a TOCTOU re-glob of the live node tree

`experiment:a00-45ecb18d-d5a017` (sibling) made a FAIL name its tests. Conjunct (b) was
unmeasured: the `.agi/context` flake reproduced 1-in-5 with no name. It is now named.

### 1 · Read before running (cheaper than 20 runs)

`pytest-randomly` is not installed (no order-randomisation lever), so the first cut was
18 `test_*.py` files under `.agi/context` read for anything that writes outside `tmp_path`,
keeps module-level state, or depends on run order. Three candidates; one mechanism.

| candidate | reads / writes | verdict |
|---|---|---|
| `local-maxxing/test_model_slot.py::test_two_holders_never_overlap` | TMPDIR log keyed by `os.getpid()`, `sleep(0.6)`, asserts `S E S E` | timing, but it is a PRIVATE tmp file with a `finally` unlink; cannot be seen by another run |
| `sql/test_graph2sql.py::test_schema_runs_unchanged_on_postgres16` | `docker run postgres:16`, 90 × `sleep(1)` | skips outright here (no docker in the box) |
| **`sql/test_graph2sql.py::test_build_under_60s_and_covers_every_node_file` + `test_verify_roundtrip_exits_0`** | builds a sqlite mirror of `.agi/nodes` (34 M, ~3.5 k files, ~9 s) | **TOCTOU — reads the live tree three times** |

```
setUpClass : g.build(ROOT, NODES, db)          # globs + reads  .agi/nodes   at T1
test_...    : n_files = sum(g.iter_files(..))  # RE-GLOBS       .agi/nodes   at T2
test_...    : g.verify(ROOT, NODES, db)        # RE-GLOBS + re-reads at T3
```
Every parallel kid, the director and harvest write node files INTO that tree while the
suite runs. Any file added between T1 and T2 makes `n_files != n_db`
(`node count differs from the file set`); any id/edge edit between T1 and T3 makes
`verify` print `DRIFT` and exit 1. `1 failed of 128 in 1 run of 5` is exactly this.

### 2 · The cause, measured (`.agi/sessions/iter-DH.393/a00-6f88eaa5/probe_toctou.py`)

A throwaway fake root (`.agi/config.json` + 50 nodes, no repo state touched). Each trial
builds the mirror, then mints one node mid-pass — the real flake window — then runs both
assertions, with and without a frozen file set.

```
pre-fix  (re-glob):      [(count_ok, verify_ok)] x3 = [(False, False), (False, False), (False, False)]
post-fix (frozen set):   [(count_ok, verify_ok)] x3 = [(True, True),   (True, True),   (True, True)]
FLAKY_PRE True  STABLE_POST True
```
Falsifier 4 answered: the mechanism predicts a failure the moment one node lands between
the build and the re-glob, and it predicts that freezing the set removes it. Both observed.

### 3 · The fix — at the cause, no retry, no timeout, no plugin

`graph2sql.py` gains an optional `files:` seam on `build` / `file_sets` / `verify`
(13 added lines, 7 removed): pass ONE file list, taken before the first read, and every
stage compares a set with ITSELF instead of with a tree that moved.

```
graph2sql.py       build/file_sets/verify: `files: list[Path] | None = None`
test_graph2sql.py  setUpClass:  cls.files = g.iter_files(NODES)   # frozen ONCE
                   build(..., files=cls.files); n_files over cls.files; verify(..., files=cls.files)
test_graph2sql_snapshot_a00_6f88eaa5.py   NEW, 2 tests
```
The new test is the acceptance criterion: a node minted mid-pass must not turn the run red
(fixed discipline), and the SAME input under the old re-glob discipline MUST fail
(so the cause stays pinned, not merely masked).

## Evidence

- `python3 -m pytest .agi/context/local-maxxing/sql/ -q` -> `9 passed, 6 subtests passed`
- `python3 -m pytest .agi/context -q -rsEf` -> `130 passed, 19 skipped, 4 xfailed` (twice)
  baseline was `128 passed, 19 skipped, 4 xfailed`; +2 is exactly the two new tests, no regression.
- production lines: `git diff --numstat -- .agi/context/local-maxxing/sql/graph2sql.py` -> `13  7` (ceiling 40).

## Not claimed

- I did not reproduce the flake inside the declared suite itself (2 clean full runs here):
  this worktree is mine alone, so no parallel kid writes into `.agi/nodes` and the window
  never opens. The cause is measured at the level of the same `graph2sql` code path on a
  fake root, and the live trigger (concurrent node writes) is what the loop does to itself
  every round. The full 20-run hunt is therefore NOT what this node rests on.
- `test_model_slot.py::test_two_holders_never_overlap` stays an unquantified timing
  candidate: private TMPDIR file, no cross-run visibility, no measured failure. If the
  DH.387 failure is ever named and it is THAT test, this node's cause is wrong.
- No reruns/`--retries`/flaky plugin and no widened timeout anywhere in this fix.

## Agent Notes
context flake named: test_graph2sql re-globs the live node tree after building the mirror; cause measured with a concurrent-mint probe, fixed by freezing one file set (files= seam), +2 pinning tests, suite 130 passed/19 skipped/4 xfailed
