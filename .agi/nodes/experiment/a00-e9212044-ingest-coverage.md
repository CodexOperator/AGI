---
id: experiment:a00-e9212044-ingest-coverage
mint_id: fb83f8359dac4d4d9cb0408f08fca887
type: experiment
parents:
  - hypothesis:a00-e9212044-470a98
next_edges: []
confidence: 0.85
edited_by: a00-e9212044
evidence_runs: experiment:a00-e9212044-ingest-coverage
line_ceiling: 40
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 5407eebd0e740d1c
season: 2
testable_claim: The two tracked ingest engine files leave the grid-coverage MISSING list once their scoped build nodes are minted, and cli.py scope-check accepts the residue doc exactly when owned
title: Scoped mint of the two ingest build nodes plus the conjunct-2 scope-check test
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-e9212044-ingest-coverage

## Experiment

Run both residues of `goal:g7.32.1` on the live grid surface, in one pass,
from worktree `a00-fa4b19f2` at tip `0ef1219a7`.

**Step 1 — scoped mint (Residue A).** Ran `level3.mint_missing` against
EXACTLY the two paths (never the unscoped `--mint-missing-only` sweep, which
would have swept the pre-existing backlog). Command and output:

```
$ python3 .agi/sessions/iter-DT.86/a00-e9212044/mint_scoped.py
--mint-missing-only: 2 un-noded code file(s) of 2 tracked-code (2 boundary-admitted)
MINTED: build:bin-ingest-session (extensions/agi/bin/ingest_session.py, parent mvp:bin-modules)
MINTED: build:tests-test-ingest-session (extensions/agi/tests/test_ingest_session.py, parent mvp:tests)
level-3 nodes minted (mint-missing-only): 2
  skipped (id collision): 0
stale pruned (mint-missing-only): 0 — this mode is ADDITIVE ONLY
```

**Step 2 — coverage proof.** Same checker, before and after:

```
$ python3 extensions/agi/bin/grid_coverage_check.py --verbose 2>&1 | grep -E "ingest_session|test_ingest"
before: MISSING: extensions/agi/bin/ingest_session.py
        MISSING: extensions/agi/tests/test_ingest_session.py
after:  (no output)

totals:  before 205 -> after 203 tracked code file(s) OUTSIDE the grid
rc:      1 in both cases (the 203-file PRE-EXISTING backlog, not this round's)
```

**Step 3 — conjunct-2 test (Residue B).** Added
`test_residue_node_is_committable_exactly_when_owned` to
`extensions/agi/tests/test_ingest_session.py`; it drives the served
`cli.py scope-check` with the real residue path on stdin:

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_ingest_session.py -q -p no:cacheprovider
19 passed in 9.55s          # was 18 passed
```

## Evidence

- Minted ids resolve to real build nodes with the right anchors:
  `build:bin-ingest-session` -> `payload_ref: extensions/agi/bin/ingest_session.py`,
  `parents: [mvp:bin-modules]`; `build:tests-test-ingest-session` ->
  `payload_ref: extensions/agi/tests/test_ingest_session.py`, `parents: [mvp:tests]`.
- The MISSING grep prints NOTHING for either path after the mint; the total
drops 205 -> 203 and the residual 203 is the parent's §3d backlog.
- `--own` leg: `scope-check` rc=1 with no ownership, rc=0 with the residue
path named — both legs pinned by the new test.
- Production lines changed on the two given paths, test excluded: **0**
(`git diff --numstat` shows only the test file, +21/-1). Ceiling 40.

**Negative observation.** The dispatch brief asked to prove the mint with
`grid.py payload build:bin-ingest-session`. That verb reads from a grid ref,
and a freshly minted node has no ref until the loop runs
`grid.py commit --all`; it returns `ERR: no grid history ...` pre-commit by
construction. Recorded as a real limitation of the proof, not papered over.
