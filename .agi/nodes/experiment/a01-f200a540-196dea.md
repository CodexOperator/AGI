---
id: experiment:a01-f200a540-196dea
mint_id: d7a05d443a7f4a91b816445a1fe5af88
type: experiment
parents:
  - hypothesis:a00-7e85b581-3a07f5
next_edges: []
confidence: 0.55
evidence_runs:
  - experiment:a01-f200a540-196dea
scaffold_hash: c3694308d4b05c52
title: A01 f200a540 196dea — Shape 3 (pip/uv) invariants: only per-env version sharing survives
verdict: inconclusive_lean_proved:55
---
# experiment:a01-f200a540-196dea

## Experiment

Tested three invariants from hypothesis:a00-7e85b581-3a07f5 via code-path analysis and live tests against `/tmp/` cleanrooms (non-git mock `engine_root` + dummy project with `.agi/config.json`).

**Setup:**
- Mock engine root: `/tmp/non-git-dir/` — empty, no `.git/`, simulating pip site-packages
- Mock project root: `/tmp/test-pip-install/test-project/` — has `.agi/config.json`, no existing nodes
- Engine source: `/home/ubuntu/work/agi/extensions/agi/` (the real checkout, used as control)

**Invariant 1 (git ls-files in level3.py):**
- Test A: `payload_boundary.classify(Path('/tmp/non-git-dir'))` — raises `CalledProcessError: Command 'git -C /tmp/non-git-dir ls-files' returned non-zero exit status 128` (because `check=True`).
- Test B: `level3.py --project <project> --engine-root /tmp/non-git-dir` — gracefully catches the exception (line 310 `except Exception: return None`), prints `"WARN: engine root /tmp/non-git-dir is missing or unreadable (not a git repo?) — no-op, nothing written or pruned"`, exits 0.
- Test C: `driver.sh --smoke` from the mock project with the real engine — runs to completion, no crash. The smoke path does not invoke `level3.py` in a way that terminates the loop.

**Invariant 2 (find-root.sh resolution):**
- Test A: `cd /tmp/test-pip-install/test-project && source .../find-root.sh && find_project_root "$PWD"` — returns `/tmp/test-pip-install/test-project/.agi` (correct). Resolution works regardless of script location because it walks UP from `$PWD`, not from the script's own directory.

**Invariant 3 (per-project version independence):**
- Analysis, not a runnable test: pip/uv installs target one site-packages per Python environment. Two projects sharing the same environment always get the same engine version. Per-project pinning requires dedicated venvs, which are operationally equivalent to a clone with extra setup steps. The graph's `grid.py commit` and `refs/grid/*` versioning are per-repo, not per-install — so version independence is architectural, not handled by the package manager.

## Evidence

```
# Test A: payload_boundary.classify() on non-git dir
$ python3 -c "import payload_boundary; payload_boundary.classify(Path('/tmp/non-git-dir'))"
CalledProcessError: Command '['git', '-C', '/tmp/non-git-dir', 'ls-files']' 
returned non-zero exit status 128.

# Test B: level3.py gracefully handles non-git engine root
$ python3 level3.py --project /tmp/test-pip-install/test-project --engine-root /tmp/non-git-dir
WARN: engine root /tmp/non-git-dir is missing or unreadable (not a git repo?) —
no-op, nothing written or pruned

# Test C: driver.sh --smoke from mock project
$ bash driver.sh --smoke
PROJECT_ROOT=/tmp/test-pip-install/test-project/.agi
...iter L1.01...
no origin=goals-doc goal nodes — refusing to write an empty GOALS.md
(driver.sh completes without crash; level3.py's no-op does not stop the loop)

# Test D: find-root.sh resolves from PWD regardless of engine location
$ cd /tmp/test-pip-install/test-project && source .../find-root.sh && find_project_root "$PWD"
/tmp/test-pip-install/test-project/.agi
```

**Summary table:**
| Invariant | Claim | Actual | Verdict |
|-----------|-------|--------|---------|
| 1: git ls-files in level3.py | crashes discovery path | raises CalledProcessError in classify(); level3.py catches it and returns graceful no-op (exit 0) | Partially proved — fails but gracefully, not crash |
| 2: find-root.sh resolution | wrong root due to script location | walks up from PWD, works regardless of install path | Disproved — reasoning incorrect |
| 3: per-project version independence | machine-global install breaks forkability | per-env sharing is real; venvs mitigate but add overhead | Proved — architectural constraint


## Agent Notes
Tested 3 invariants for Shape3 (pip/uv install) vs forkability. Invariant1 (git ls-files in level3.py): payload_boundary.classify() raises CalledProcessError on non-git dir, but level3.py catches it (graceful no-op). Invariant2 (find-root.sh): DISPROVED — walks from PWD, works regardless of install path. Invariant3 (per-project version independence): PROVED — pip/uv per-env sharing is real, venvs add overhead. Overall: 2/3 invariants hold, leaning proved but invariant2 false alarm weakens claim.

<!-- THOUGHT:BEGIN -->
Parent review (a00-dcde66ac, iter 1065). The kid's verdict and confidence are
ACCEPTED unchanged at `inconclusive_lean_proved:55`; the only change is the
`evidence_runs` self-citation it omitted and a title that says something.

55 is the right number and the kid earned it by arguing against itself. Its
summary table marks invariant 2 DISPROVED -- "reasoning incorrect", the
hypothesis's own stated mechanism is false -- and its Agent Notes call that a
false alarm that weakens the parent claim, rather than burying it. Invariant 1
it downgrades to "fails but gracefully": `payload_boundary.classify()` really
does raise `CalledProcessError` on a non-git directory, but level3.py catches
it and no-ops at exit 0, so a broken discovery path is a warning line, not a
broken engine. That leaves invariant 3 as the only one standing, and a lean
barely over half is honest for one surviving barrier out of three.

Read against its sibling on the same hypothesis, experiment:a00-5e6608dd-c490af:
the two agree on invariants 1 and 2 from independently built cleanrooms, which
is worth more than either run alone, and split on invariant 3. This run treats
per-environment sharing as a real architectural constraint that venvs only trade
for clone-equivalent setup overhead; the sibling treats venvs as a solution and
called the whole hypothesis disproved. I demoted the sibling to 75 for that and
left this one alone -- the split is now legible in both nodes rather than
resolved by fiat in neither.

`evidence_runs` was absent. The verdict is a lean, so the gate did not require
it, but the tests in ## Evidence are this node's own and a reader should be able
to reach them by edge rather than by prose. An experiment may name itself.
<!-- THOUGHT:END -->
