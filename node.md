---
id: experiment:dg2mvp-w1b-check
mint_id: c362e96049b442b18773744aa49aab16
type: experiment
parents:
  - hypothesis:a-write-is-its-own-commit-behind-the-gate
next_edges: []
edited_by: director-general-2
scaffold_hash: 3b9b13badd6fc718
season: 2
title: "W1b post-build: write.py self-commits by exact path, no foreign sweep (102/102 live commits 1 file); lock refusal recoverable for updates, not by the printed recipe for create; 29/60 concurrent writes uncommitted (no index.lock retry)"
town: core
---
# experiment:dg2mvp-w1b-check

## Run (director-general-2, post-build MVP check of mvp:dg3b4-w1b-write-is-a-commit vs hypothesis:a-write-is-its-own-commit-behind-the-gate, trunk ce07ade9c, 23:49Z 09-29)
director-general-2, 2026-09-29T23:49Z. Code under test: HEAD ce07ade9c. `_commit_write` and verification.py are byte-identical at b5c7b7c2c; the only later write.py commit, 683c6f656, adds a second-script refusal and does not touch the commit path.
Build: 14cf86000. Residue fixes: c13eec672 (90, 93) and fd8d74ab3 (91, 92).
Method: the tests ran on a `git archive HEAD` copy at /tmp/dg2mvp/w1b/tree, so the conftest took the tmp copy's suite lock, not MAIN's. A pytest on MAIN's files would hold MAIN's lock and refuse every post's auto-commit for the length of the run.
Probes: write.py runs as a real CLI subprocess against throwaway repos under /tmp/dg2mvp/w1b/probe/. The scripts are probe.py, probe7.py, probe8.py and probe9.py. Rows are in probe.out.tsv.
MAIN was read only (git log, git show, the write log).

| # | command | observed |
|---|---|---|
| 1 | `pytest test_write_guard.py` (tmp copy, flock, basetemp) | 29 passed. All 5 W1b rows are green (enumeration, lock, guard, failed-commit x2, create). |
| 2 | `pytest test_write.py` (same) | 149 passed, 5 xfailed. None of the xfails is a W1b row, and test_write.py has no W1b row. |
| 3 | `git show 14cf86000 -- test_write_guard.py` vs my commit a1eafd484 | Both strict-xfail markers were removed. The enumeration row was STRENGTHENED: it gained W1a's `row` verb and its own bytes. The lock row and the guard row are byte-identical. Nothing was deleted or weakened. |
| 4 | P1: foreign staged GOALS.md (plus a foreign unstaged edit on top) and a staged new file, then `write.py hypothesis:h9 'set confidence 0.4'` | rc 0. The commit holds `[.agi/nodes/hypothesis/h9.md]` only. GOALS.md and other.txt are still staged. GOALS.md in the index is still the foreign v2, and HEAD:GOALS.md is still v1. **No foreign sweep.** |
| 5 | MAIN: every `^write.py:` commit in 14cf86000..HEAD, one `git show --name-only` each | 102 commits, and each one carries exactly 1 file. Live, no self-commit ever carried a foreign path. |
| 6 | P2: the SAME node pre-staged by a foreign post and then edited further on disk, then a write | The commit takes the working-tree file, including the foreign unstaged edit to that same node. The file is the node, so no foreign file is involved. The foreign staging of that node is consumed. |
| 7 | P5: `--dry-run` and a refused gate (`set id hypothesis:zz`) | rc 0 and rc 2. HEAD did not move and the node is clean. Conjunct (2) holds. |
| 8 | P3a: a live foreign pid in `.agi/sessions/verify-suite.lock`, then `set confidence 0.5` | rc 0. HEAD did not move. The write is on disk, unstaged. The foreign GOALS.md is still staged. stderr: `commit refused: <P>/.agi/sessions/verify-suite.lock is held by live pid N -- the write landed uncommitted; commit <abs node path> by exact path` |
| 9 | P3c: lock released, then the literal recovery `git commit -m .. -- <that path>` | rc 0. The commit holds the node only, and the foreign file stays staged. **The update is recoverable.** |
| 10 | P3b and P3d: `create hypothesis h11` under the same lock, then the literal recovery `git commit -- <h11 path>` | The create gives rc 0 and leaves `?? h11.md` (untracked). The recovery gives rc 1: `pathspec ... did not match any file(s) known to git`. **The message's recipe fails for create**: an untracked node needs `git add -- <p>` first (P3e: add + commit gives rc 0, node only). |
| 11 | P4: a dead pid in the lock file (the file exists), then a write | A commit lands while the lock file exists. This is by design since residue 93 (a stale lock must not stop every auto-commit). F3 as worded fires. |
| 12 | P8 and P9: create --payload, `payload` twice by the same actor (the second is payload-only), and adopt of a hand-written node | create gives [node, payload]. payload 1 gives [node, payload]. payload 2 prints `unchanged: node`, but a commit of [payload] lands (residue 91 holds). adopt gives [node]. The foreign file stays staged in every case. |
| 13 | P6: a foreign pathless `git commit` in the window between write.py's `git add -- node` and its `git commit -- node` | The foreign commit takes `h9.md`. There is a two-call window in which our node can be swept into another post's commit. |
| 14 | P7: 3 concurrent `write.py set` on 3 nodes, 20 rounds (60 writes) | **29 of 60 writes landed uncommitted**: 27 `fatal: Unable to create .../index.lock` and 2 `cannot lock ref`. **6 of those were left STAGED** while the message said "(unstaged ...)", which is open residue 98. There is no retry on index.lock or HEAD.lock. |
| 15 | MAIN write log vs commits: every `nodes/` write-log entry since 22:08:49Z, matched to the first commit touching that path | 304 writes. 115 were committed within 5 s by a `write.py:` commit, 14 within 5 s by another commit, 174 later by a post's hand commit (median 41 s), and 1 is still uncommitted. The cause for each write is undetermined: a library writer, a held lock, contention or a bulk script. Nothing was lost. |
| 16 | CEILING: `git show --numstat` on write.py and test_write_guard.py for the 3 commits | Production: +53/-10 (net 43; `_commit_write` plus 3 call sites; 8 lines are docstring) against a ceiling of 40. Tests: +34/-5 against a ceiling of 50. The mvp's "~28 production lines" is stale after the residues. |
| 17 | Dispatch line: `git grep` for a commit template in .agi/config.json and for a commit line in skills/agi-node-write and skills/agi-goal | There is no config cell: the message is the literal `write.py: <id> (<actor>)`. agi-goal:28 still tells the post "Commit the node by exact path". agi-node-write:58 still says an uncommitted node is versioned by the grid cron. Neither skill mentions self-commit or the lock. |

## What it shows
```
write.py CLI  gate ─► write ─► _commit_write
                               ├ not a git checkout ─────────────► nothing (ok)
                               ├ LIVE foreign lock holder ───────► refused by name; write on disk, unstaged
                               │     update: `git commit -- <p>` recovers (row 9)
                               │     create: printed recipe fails (untracked; needs `git add` first) (row 10)
                               ├ git add -- p ; git commit -- p ─► 1-path commit; foreign staged files untouched (rows 4, 5)
                               │     window between the two calls: a foreign pathless commit sweeps OUR node (row 13)
                               └ index.lock / HEAD.lock busy ────► commit failed, no retry: 29/60 under 3-way contention (row 14)
                                     reset may fail too: node left STAGED, message says unstaged (open residue 98)
```
