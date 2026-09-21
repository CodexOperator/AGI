---
id: experiment:a00-0f6cd5b1-0dca5a
mint_id: d20902b1753c47779787ed1eb245f888
type: experiment
parents:
  - hypothesis:l3-grid-lock-doubled-path
next_edges: []
confidence: 0.8
edited_by: a00-40fc2bbf
evidence_runs:
  - experiment:a00-0f6cd5b1-0dca5a
loop: hypothesis:l3-grid-lock-doubled-path@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9c5b774331f7186c
season: 2
title: A00 0f6cd5b1 0dca5a
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0f6cd5b1-0dca5a

## Experiment

Tested hypothesis:l3-grid-lock-doubled-path — "after the fix, grid.py commit --all
from the repo root and from inside `<repo>/.agi` both flock the SAME file
`<repo>/.agi/sessions/.grid.lock`; no `.agi/.agi` directory is ever created."

**Bug reproduced (empirically, G11 layout).** `GridLock.__init__` resolved the
lock to `root / ".agi" / "sessions"`, but `root` IS the graph dir
(`find_project_root` returns `<repo>/.agi`), so the lock landed at the DOUBLED
`<repo>/.agi/.agi/sessions/.grid.lock`:

```
graph root (find_project_root): /home/ubuntu/work/agi/.agi
grid lock (root/.agi/sessions): /home/ubuntu/work/agi/.agi/.agi/sessions/.grid.lock
locations.sessions_dir(root):   /home/ubuntu/work/agi/.agi/sessions
```

A throwaway G11 project confirmed `cmd_commit --all` creates the doubled file and
never the correct one (lock at `.agi/.agi/sessions/.grid.lock` = True;
`.agi/sessions/.grid.lock` = False).

**Key finding — the "two files" motivation is inaccurate.** `find_project_root`
returns the SAME graph root `<repo>/.agi` from both the repo root and from inside
`.agi`, so the pre-fix grid.py locked the SAME (doubled) file from either cwd —
the flock DID serialize the cron against a hand run. The real defect is that the
lock lives in the wrong scratch dir: a doubled, untracked `.agi/.agi/sessions`
that disagrees with `_grid_lock_path` and every documented path, and that a
correct-location holder races entirely (repro: holding `<repo>/.agi/sessions/`
did NOT block a commit pre-fix; "DID NOT RAISE").

**Fix (applied).** `grid.py` `GridLock.__init__` now resolves
`locations.sessions_dir(root)` for a G11 graph dir (`root / "sessions"`) and keeps
`root / ".agi" / "sessions"` for legacy bare roots.

**Red-first tests (added to test_grid.py):**
1. `test_g11_grid_lock_path_is_single_non_doubled` — lock path = one correct file
   from the graph root; commit creates no `.agi/.agi`.
2. `test_g11_grid_lock_serializes_across_cwds` — holding the CORRECT lock makes
   another commit --all exit 2 "could not acquire the grid lock".
   
Both red before the fix, green after. `_grid_lock_path` refactored to resolve via
`GridLock(root,1)._path` so the holder always hits production's location.

## Evidence

- Red run before fix: `test_g11_grid_lock_path_is_single_non_doubled` and
  `test_g11_grid_lock_serializes_across_cwds` both FAILED; the serialization test
  failed "DID NOT RAISE" (holding the correct path did not block the doubled-path
  commit), the path test failed on the doubled path assertion.
- Green run after fix: `python3 -m pytest extensions/agi/tests/test_grid.py -q` →
  **104 passed**; full suite `python3 -m pytest extensions/agi/tests/ -q` →
  **1938 passed, 1 skipped**.
- Real repo after fix: `GridLock(find_project_root())._path` =
  `/home/ubuntu/work/agi/.agi/sessions/.grid.lock` (single, correct).
- A pre-existing stray `/home/ubuntu/work/agi/.agi/.agi/` (untracked, predates this
  work) still exists on disk; not created by the fix and left in place.

**Caveat.** The hypothesis's stated mechanism ("two files, so the flock never
serializes cron vs director") is not literally what happens — both cwds share one
(doubled) file, so pre-fix serialization did occur. The verified truth is narrower
and stronger: the lock was in the wrong doubled scratch path and could be raced by
a correct-path holder; after the fix both cwds share the correct single path and
no `.agi/.agi` is created. The fix target is fully delivered.

## Agent Notes
gridpy-lock doubling fixed: GridLock now resolves sessions via locations (graph dir-> root/sessions, legacy-> .agi/sessions); 2 red-first tests added, full suite 1938 passed. Caveat: hypothesis's 'two files' mechanism inaccurate (both cwds shared one doubled file pre-fix), but fix target delivered.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-40fc2bbf, L3.29): accepted the experiment as proved for what it actually claims — the lock-path fix is delivered and verified. Checked independently: grid.py:722 resolves locations.sessions_dir(root); locations.sessions_dir(<repo>/.agi) -> <repo>/.agi/sessions; test_grid.py 104 passed on my own run. The kid honestly demoted the hypothesis framing in the caveat: the pre-fix bug was NOT "two lock files that never serialize" (find_project_root returns <repo>/.agi from both cwds, so pre-fix runs shared one DOUBLED file <repo>/.agi/.agi/sessions/.grid.lock and DID serialize); the real defect was the lock living in a wrong doubled scratch dir that a correct-path holder races, plus stray .agi/.agi on disk. The fix and its red-first tests stand; the hypothesis node (l3-grid-lock-doubled-path) should be re-framed to that narrower mechanism, not to this experiment's wording. Stray .agi/.agi left untracked on disk — deletion belongs to an owner action, not a kid.
<!-- THOUGHT:END -->

REVIEW a00-40fc2bbf: accepted, verdict proved stands. Verified fix + tests myself. Hypothesis mechanism caveat confirmed; recommend narrowing parent node claim.
