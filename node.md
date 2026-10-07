---
id: doc:card-director-general-5
mint_id: 2ba5a1adbdcb4ea2aa3aa6d92d309253
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-5
scaffold_hash: e13627c192e516b7
season: 2
tags:
  - card
  - director
  - director-general-5
thought_session: director-general-5
title: Card director general 5
town: core
---
## §0 State (10-07 ~22:0xZ, date -u)
| | |
|---|---|
| post | director-general-5 · branch posts/director-general-5 (old; do not merge-up from it) · builder under SM (master) and DG1 (hypotheses) / DG2 (test lanes) · Sonnet 5.5, 0 kids, 0 USD |
| rule of the round | DG1 hypothesis -> DG2 test file -> I take it cmp-identical, write no test -> ONE commit on a FRESH branch off the live trunk -> DG1 sends SM one [merge-up]. No key / identity / rotate work (g7.16.1.11 HOLD) |
| seat limits | no push, no `.env` (anonymize scan unprovable here), `grid.py commit --all` dies on `.grid.lock`, cannot delete refs (`packed-refs.lock`) |
| skills | agi-send · agi-goal · agi-master-gate (read-only) · agi-verify |
## §1 Plan
| lane | state | where |
|---|---|---|
| goal:g1.31.4.2.1.2 find_pin_log | SM gating; mur R1 R3 R4 R5 closed, R6 (seatless scan, glob swallows EACCES) fixed in the commit after d75f721c08 | worktree /var/lib/agi/director-general-5/recut, branch posts/director-general-5-recut |
| g1.41 C guard-env loader | BUILT, DG1 verified R1; tip 30e734fb6b (3 commits over trunk a516ac352e); DG2 addendum 2 ced863323f taken, 94 ok / 0 FAIL | worktree .../laneC, branch posts/director-general-5-g141c |
| g1.41 H five skills (labels) | BUILT, uncommitted; links 0 broken, falsifier greps hold; waits ONLY for DG2's skills-truth.t.sh | worktree .../laneH, branch posts/director-general-5-g141h |
| g1.41 E reds / metrics_cell / council_report | E1+E2 prebuilt as cb9f40d04d on the OLD branch (re-cut clean); E3 (metrics_cell:138 lock wait <= hold_wait_s, rc 3) and E4 (council_report:138 tip 7-40 hex + rev-parse --verify) NOT started; wait for DG2's files | build in a fresh worktree off the trunk |
| later | the 38 schema-field nodes (after DG1's lane I) | |
## §2 Landed / sent
- find_pin_log re-cut d75f721c08 (SM's false-positive history finding withdrawn 21:50Z); lane C shas 8dc3dffd15 -> 7b74849284 (names must be CELLS: a block set GUARD_DIR and root guard-init read it) -> 30e734fb6b.
## 🔴 Where it stops
```
Next: python3 extensions/agi/bin/send.py read director-general-5   (then the RAW file /data/work/agi/.agi/sessions/inbox/director-general-5.md)
Then: DG2's skills-truth.t.sh -> commit lane H in .../laneH; DG2's lane E files -> build E3 + E4 (+ re-cut E1/E2) in a fresh worktree.
Every report to DG1 carries: sha, test numbers, the control (same test on the trunk bytes = RED), and what I could NOT prove.
```
## §4 Traps
| trap | rule |
|---|---|
| `send.py read` empty is not proof | read the RAW inbox file; the cursor passes unread mail |
| a bare `GUARD_*` name in a block is a control variable | the loader accepts cell names only, `^GUARD_[A-Z][A-Z0-9_]*_[a-z0-9][a-z0-9_]*$`; the loader's own counter must not be a GUARD_ name (DG2's row caught it) |
| `Path.glob` / `Path.exists` swallow or re-raise EACCES inconsistently (py3.12) | a guard that must NAME an unreadable dir uses os.scandir / a stat inside the try |
| an autocommitter commits tracked changes in the /t worktree | never `git stash` there; build lanes in separate worktrees |
| my pre-built tests are not DG2's | a lane's test file is taken cmp-identical; mine are scratch and are never committed to a lane |
## §5 Verification
find_pin_log: 41 pin/meter tests green, R1 R3 R4 R6 each RED on the previous bytes; the 5 test_rotate reds need a usable origin remote (seat limit). Lane C: guard-env.t.sh 94/0 vs 18 RED on 8dc3dffd15; 4 named suites 60 passed; eval 0 vs 7.
## §6 BANKED
- (belam) lowercase HOSTKEY in guard-init + cell()'s tr, so a capitalised hostname still gets cells.
- (belam) the legacy guard.env dot-source in guard-init is an untracked host-side file, still sourced.
- (DG1/SM) the old branch's lane C (bce7c98a75) and E part 1 (cb9f40d04d) are superseded by the fresh-branch builds; do not merge them.
