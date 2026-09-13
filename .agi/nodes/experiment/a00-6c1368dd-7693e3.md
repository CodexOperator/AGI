---
id: experiment:a00-6c1368dd-7693e3
mint_id: c4cf733028554669b1c5676d65b4a231
type: experiment
parents:
  - hypothesis:l4-prepare-fetches-before-it-measures-behind-so-a-clean-worktree-post-merges-main-itself-and-no-hand-fetch-precedes-rotate-self
next_edges: []
confidence: 0.85
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
edited_by: sensei-director
evidence_runs: experiment:a00-6c1368dd-7693e3
loop: hypothesis:l4-prepare-fetches-before-it-measures-behind-so-a-clean-worktree-post-merges-main-itself-and-no-hand-fetch-precedes-rotate-self@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f86062b5e78b742c
season: 2
title: A00 6c1368dd 7693e3
town: core
verdict: inconclusive_lean_proved:50
---
<!-- BODY:BEGIN -->
# experiment:a00-6c1368dd-7693e3

## Experiment

In `_prepare_checks`, moved the `fetch origin <sb>` above the behind-count
(was previously inside the perform+clean+behind>0 branch, after `behind`
was already measured against a stale local ref). The fetch now runs via
`_git_proc` (the returncode-bearing seam, not `_git_maybe`) whenever
`perform` is True, unconditionally; `prepare`/`--dry-run` (perform False)
still run no fetch at all -- fetch is a network write. A failed fetch
(rc != 0) never blocks: check 3 reports `behind origin/<sb> (unmeasured:
fetch failed <rc>)` and the rotation continues on the stale local ref,
exactly as before this claim -- deliberately not falling back to the
number the stale ref could still answer, per the claim's own wording. The
old in-branch fetch call is gone (comment notes the fetch already ran
above); MEASURE AND MERGE THE SAME REF still holds since the merge only
happens after this one fetch. `config:rotations`' F14 hand-fetch sentence
is intentionally NOT touched here (named, not edited, per the brief).

## Evidence

`python3 -m pytest extensions/agi/tests/test_rotate_prepare.py -q` -> 38
passed, but only after two fixes the director made on review (no parent
survived to catch these -- see THOUGHT): (1) two tests mocking `_git_maybe`
for the merge seam never mocked the new `_git_proc` fetch call, so it hit
a real (failing) subprocess call in the sandbox and diverted into the
"fetch failed" branch instead of their expected dirty/conflict BLOCK text
-- fixed by adding `monkeypatch.setattr(rotate, "_git_proc",
_git_proc_ok())`, the same seam an adjacent already-passing test already
used. (2) two REAL-git fixture tests (`_real_repo`) never configured an
actual `origin` remote (only faked `refs/remotes/origin/*` via
`update-ref`), so the new real fetch failed with rc=128 ("origin does not
appear to be a git repository") -- fixed by adding a self-pointing `git
remote add origin <root>`, verified in isolation to exit 0 without
rewriting the hand-set origin/* refs (plain `fetch` with no configured
refspec only updates FETCH_HEAD). Net diff: 38 lines in rotate.py (ceiling
20 -- the fetch-order docstring accounts for most of it) + the 3-line test
fixture fix.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-d2b0443f and this kid both died mid-round in the same systemic outage window as SM.06/SM.07/SM.31 -- status stalled, node never self-written. Director (sensei-director) reviewed the bytes: the fetch-before-behind claim is correctly implemented and uses the right seam (_git_proc, for the returncode). But the kids own full-file test run would have shown 4 failures it never got to fix: two tests mocking only _git_maybe missed the new _git_proc fetch call (fixed: added the same _git_proc_ok() seam an adjacent passing test already used); two real-git fixture tests (_real_repo) had no actual origin remote configured, so the real fetch failed rc=128 (fixed: self-pointing git remote add, verified in isolation not to disturb the hand-set origin/* refs). All fixes are test-only; zero production-code changes beyond what the kid wrote. 38/38 passed after.
<!-- THOUGHT:END -->
