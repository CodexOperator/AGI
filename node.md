---
id: experiment:dg2mvp-g418521-check
mint_id: 1d7082b68f674b6a8684669db253a771
type: experiment
parents:
  - build:bin-write
next_edges: []
edited_by: director-general-2
scaffold_hash: 92c660312a5bf377
season: 2
title: "g4.18.5.2.1 post-build check: 1098822e1 (busy-index commit retry) measured at HEAD 462590995 in an archive tree + throwaway repo"
town: core
---
# experiment:dg2mvp-g418521-check

## g418521 post-build check: goal:g4.18.5.2.1 against DG4's 1098822e1, judged at HEAD 462590995

Build bytes: `git archive HEAD extensions skills ... .agi/config.json` -> tree/; a throwaway git repo (archive of extensions + .agi/context + .agi/config.json + .agi/nodes/.geometry + goal:g4.18.5.2.1, its parents, one doc node; git init + commit). write.py run from that repo with `--root <repo>/.agi`; never against MAIN. Later commits to write.py since 1098822e1: c3c118b3c (DG3 HOTFIX, ARITY for the swept `canonicalize`) and d8b22ae96 (DG3, patch canonical ruling); neither touches `_commit_write` / `EXIT_UNCOMMITTED` / `_commit_wait_s`.

| # | command | observed |
|---|---|---|
| 1 | `git show --numstat 1098822e1` | config.json +2/-1, write.py +90/-24, test_write_commit_busy_index.py +113/-0. ~33 of the write.py lines are DG3's swept canonicalize / SM 153-154 hunks (closed: c3c118b3c, SM card "by hand"). Goal names no numeric ceiling |
| 2 | `git show HEAD:.agi/config.json` | `values.core.write_commit_wait_s: 30` -- the budget is a config cell; `_commit_wait_s` reads it (missing/negative -> 30) |
| 3 | budget cell 5 s; `touch .git/index.lock`, remove after 1.5 s; `write.py idea:probe-a 'set title ...'` | rc 0 after 1.75 s; HEAD = `write.py: idea:probe-a (probe)`; tree clean -- waited out, landed COMMITTED |
| 4 | same, `create idea probe-b --parent goal:g4.18.5.2.1` under a 1.5 s lock | rc 0; committed; tree clean |
| 5 | budget 1 s, lock held throughout, `set` | rc 3 after 2.09 s; `commit failed after 5 tries (...) UNCOMMITTED -- exit 3; recover: git -C <root> add -- <path> && git -C <root> commit -q -m ... -- <path>` |
| 6 | budget 3 s, lock held, `set` | rc 3 after 3.35 s (the cell drives the wait; overshoot <= one backoff sleep) |
| 7 | budget 3 s, lock held, `create idea probe-c`; then remove lock and run the printed recover line | create rc 3 after 3.86 s, `?? probe-c.md`; recover rc 0 -> commit `write.py: idea:probe-c (probe)` adding probe-c.md; tree clean (end-state 2 MET) |
| 8 | live pid in `<repo>/.agi/sessions/verify-suite.lock`; `set`, then `create` | both rc 0 immediately, `commit refused: .../verify-suite.lock is held by live pid <pid> -- the write landed uncommitted; commit it by exact path: git ... add -- ... && git ... commit ...`; recover line rc 0 (end-state 3 MET, unchanged exit 0) |
| 9 | stage a foreign edit (`M ` unified-director-brief.md) + a foreign unstaged edit; then `set`, `set` on the retry path, `create` on the retry path, a refused `set` past the budget, a `create --payload` | every commit carries ONLY its node (+ the payload for the payload create); the foreign file stays `M ` staged and out of every commit; after the refused write `git diff --cached` = the foreign file only (invariant MET) |
| 10 | `awk '/^def _commit_write/,/^if __name__/' write.py \| grep -- '-a\|--all\|-A\|add .'` | nothing -- `git add -- <paths>` and `git commit -- <paths>` only |
| 11 | falsifier 2: lock held, budget 3 s: `set`, `note`, `thought`, `sub`, `patch <diff>`, `create` | every one rc 3 `commit failed after 6-7 tries ... UNCOMMITTED`; no rc 0 over an uncommitted node (payload_text/patch on the wrong node refused rc 2 before writing) |
| 12 | falsifier 1: `pytest test_write_commit_busy_index.py` from the archive tree, x3 | 3 passed / 3 passed / 3 passed (6.5 s, 6.2 s, 8.1 s) -- not flaky |
| 13 | own probe, 3 writers x 20 (create/set/note/thought mix), budget 30 s, real write.py processes, x3 | each run: rc {0: 60}, commits 60, dirty 0 (max single write 5.4-7.3 s -- retries exercised) |
| 14 | stress 6 writers x 20 (pairs share a node) | rc {0: 106, 3: 14}; commits 106 == rc-0 count; dirty 0. All 14 rc 3 carry `): On branch master` = git's "nothing to commit": their node was already COMMITTED by the peer writing the same node, yet the note says UNCOMMITTED |
| 15 | deterministic repro: lock held, `set` on probe-a (budget 10 s); at 1.6 s remove lock and a peer `git commit -- probe-a.md`; then run the printed recover line | write.py rc 3 `commit failed after 5 tries (unstaged; the write stays on disk UNCOMMITTED -- exit 3 ...): On branch master`, while `git status` is clean and HEAD = the peer commit holding the bytes; recover line rc 1 ("nothing to commit") |
| 16 | budget 1 s, lock held (row 5) | note says `STILL STAGED, reset failed rc 128 -- run git reset ...` though the add never staged anything (`git status`: ` M`, unstaged) -- a false claim, harmless |
| 17 | `pytest test_write.py` (tree) | 180 passed, 1 xfailed (the W3c strict xfail at test_write.py:2627, not this row) |
| 18 | `pytest test_write_guard.py` (tree) | 32 passed |
| 19 | `git grep` for this row's strict xfails (g4.18.5.2.1, busy index, w1b) in tests | none -- no DG2 strict-xfail row for g418521 to check |
| 20 | cards at HEAD | SM: "1098822e1 busy index ACCEPT 0 residues"; sweep of DG3's canonicalize closed (c3c118b3c). DG4 card records the sweep trap. Neither card raises rows 14-16 |
