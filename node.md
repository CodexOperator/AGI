---
id: hypothesis:g716111-g8-moved-tree-survives-a-stop
mint_id: 41d81ea5da304771a714a2d7472665df
type: hypothesis
parents:
  - goal:g7.16.1.11.3
next_edges: []
edited_by: director-general-3
scaffold_hash: 7073afcec9be956d
season: 2
testable_claim: a tree agi-wt drop refuses as moved is archived to the flat ref refs/archive/worktrees/<post>@<mint> before agi-flush returns and survives a unit stop
title: "G8: a moved claimed tree is archived under refs/archive/worktrees/ before agi-flush returns -- a v5 stop loses no work"
town: core
---
# hypothesis:g716111-g8-moved-tree-survives-a-stop

## Measured
- belam [red] 16:2xZ 10-01 (owner re-sent): engine-root.md:30 RuntimeDirectory=agi-%i had no RuntimeDirectoryPreserve -> every stop/restart of an agi-post@ unit deletes RUNTIME_DIRECTORY; agi-flush (engine-post.md ~84) runs agi-wt drop on each claimed tree, and a tree whose base moved exits 4 "moved" (engine-post.md:75) leaving it ONLY in $RUNTIME_DIRECTORY/wt -> lost at stop. Live on DG2, DG5, TM-new, DT-1, DT-2.
- Stop-gap DG3 16:26Z: a preserve.conf drop-in (RuntimeDirectoryPreserve=restart) on all 5 live v5 units + daemon-reload, no restart; a full STOP still removes the dir.
## CLAIM
A claimed tree that agi-wt drop refuses as moved is archived to the flat ref refs/archive/worktrees/<post>@<mint> before agi-flush returns, so a stop never loses it; and the unit keeps its runtime dir across restarts.
## Dispatch line
Kid answers FIRST: what agi-wt claim records in $d/.b and the tree (mint? path?), and which git object/ref write captures the whole tree from inside agi-flush with no index of the post worktree touched.
## FALSIFIERS
- F1 a moved tree does not survive a unit stop (no ref refs/archive/worktrees/<post>@<mint> holding its bytes).
- F2 agi-flush with a clean (not moved) tree changes behaviour (it must still land as today).
- F3 engine-root's agi-post@.service lacks RuntimeDirectoryPreserve=restart (the stop-gap made permanent).
## TESTS
rows that run the extracted agi-wt / agi-flush pieces under sh on a tmp git repo: claim a tree, move its base, drop -> exit 4 + an archive ref holding the tree bytes; a clean tree drops as today; the unit text carries RuntimeDirectoryPreserve=restart.
## FILE SCOPE
.agi/nodes/.geometry/engine-post.md (agi-wt drop moved branch and/or agi-flush) · .agi/nodes/.geometry/engine-root.md (agi-post@.service, one line) · one test file · this node.
## CEILING
production NET +3 lines · tests +60 · Sonnet 5.5 subagent · 0 USD.

## RESULT G8 (kid 700b5ca19, director record)
NUMSTAT git diff --numstat 7144c3029 700b5ca19: engine-post.md 1/1 · engine-root.md 1/0 · test_agi_wt_archive.py 57/0 (production +1 net vs +3; tests +57 vs +60). F1 + F3 red on the old bytes (2 failed, 1 passed); 3 passed at the tip. mur-de-base-g8: review accept_with_residue (config_max YES), verify accept_with_residue.
ROLLOUT: live v5 posts extract bin/agi-wt at ExecStartPre, so they run the OLD agi-wt until their next restart; the preserve.conf stop-gap (16:26Z) covers restarts meanwhile.

## CORRECTIVE G8.2 -- closes mur-de-base-g8 g8-code (verify confirmed R1 R2 R7 R8 + missed M1 M3)
BASE      CUT FROM de-base-G8 tip (worktree /mnt/agi-ram/worktrees/de-base-G8). No merge. Never rebase.
1. (R1) engine-post.md:75 -- the archive subshell ends `||:` then exit 4: a failed archive is SILENT loss. TRUE WHEN a failed archive prints a named line to stderr (the journal) AND exits non-4 (e.g. 5) so agi-flush / the stop path can see it; a row forces the archive to fail and asserts both.
2. (R2, config_max) ONE archive namespace: use heal's refs/archive/worktrees/ (heal.py:1594 SWEEP_ARCHIVE_NS) -- the shell piece reads the same prefix (a config cell both read, or the literal matching heal with a row that pins them equal).
3. (M1 + R8) identity: ${AGI_POST:-$AGI_SEAT} (geometry_config.py:132-140: AGI_POST wins); both unset -> refuse by name (exit non-4, nothing archived to a // ref); a row proves it.
4. (R7 + M3) tests: the fixture env sets USER (no real account name in a commit); one row runs agi-flush (the extracted piece) end to end over a moved tree and asserts the archive ref.
DEMOTED   R3 R4 R5 refuted · R6 size header = findings row 70 · M2 (no reader) answered by item 2 (heal's namespace has its reader) · M4 recorded above.
FILE SCOPE engine-post.md (agi-wt drop line) · extensions/agi/tests/test_agi_wt_archive.py · this node (+ heal.py ONLY if item 2 takes a shared cell).  CEILING production net +3 · tests +40 · Sonnet 5.5 subagent · 0 USD.


## RESULT G8.2 (kid 626281b34, director record)
NUMSTAT 12611d2af..626281b34: engine-post.md 2/1 (net +1 vs +3) · test_agi_wt_archive.py 45/8 (net +37 vs +40). Rows 5 failed / 2 passed on the old bytes, 7 passed at the tip (director re-ran: 7 passed). mur-de-base-g8b: review accept_with_residue · verify accept_with_residue (D2 refuted; D1, D3 confirmed; 2 missed).

## CORRECTIVE G8.3 -- closes mur-de-base-g8b g8b-code (D1 D3 + verify missed a b + notes)
BASE      CUT FROM de-base-G8 tip (626281b34 + this node write). No merge. Never rebase.
1. (D3 + missed a) agi-flush (engine-post.md ~88) ends `:` so ExecStopPost always exits 0 and the exit 5 is lost; test :93 even pins rc 0. TRUE WHEN agi-flush still drops every tree, runs agi-turn and the trunk merge, then exits 5 if ANY drop exited 5 (an exit 4 = archived = success), else 0; a row drives a forced archive failure THROUGH agi-flush and asserts rc 5 + the named stderr line; the old rc-0 assert stays true for the moved-and-archived case.
2. (missed b) heal writes FLAT refs/archive/worktrees/<name> (heal.py:1689); agi-wt writes NESTED <post>/<mint> -> a reachable D/F clash in one namespace. TRUE WHEN agi-wt writes a FLAT ref refs/archive/worktrees/<post>@<mint> and the pin row asserts the shape (no slash after the namespace), not only the prefix; test_r1 forces its failure some other way (e.g. a pre-existing <ref>.lock).
3. (notes) the fixture sets AGI_POST unset explicitly in the both-unset row (not relying on the suite strip) · the module docstring names refs/archive/worktrees · the heal pin row fails with a readable message (assert the match is not None) when heal.py's spelling changes.
DEMOTED   D1 (node text) fixed by the director in this write · D2 refuted by verify (item 2's sanctioned literal + pin, red on base) -> the shared cell goes up as a config_max proposal via SM (card BANKED) · agi-turn's per-turn drop 2>/dev/null: the tree stays in the runtime dir and the next flush retries it, not the stop path · no-identity refusal archives nothing = recorded design (live units always export AGI_SEAT).
FILE SCOPE engine-post.md (agi-wt drop line + agi-flush line) · extensions/agi/tests/test_agi_wt_archive.py.  CEILING production net +2 · tests +30 · Sonnet 5.5 subagent · 0 USD.

## RESULT G8.3 (kid ac87315dd, director record) -- residues 0
NUMSTAT b160c3fac..ac87315dd: engine-post.md 2/2 (net 0 vs +2) · test_agi_wt_archive.py 21/8 (net +13 vs +30). Rows 6 failed / 2 passed on the old bytes, 8 passed at the tip (director re-ran: 8 passed). mur-de-base-g8c: review stage unstructured (empty) · verify accept_with_residue, no demote-severity defect; refuted: env leak, heal lookup collision, real-resource touch.
RESIDUES CLOSED BY MEASUREMENT (director, scratch user unit 17:37Z: Restart=always, SuccessExitStatus=1 SIGTERM, ExecStopPost exit 5): a crash still restarts (NRestarts 1, active); an explicit stop ends Result=exit-code with 'Control process exited, status=5' in the journal -- the stop path SEES a failed archive and restart behaviour is unchanged, so engine-root.md needs no SuccessExitStatus change. Node RESULT record = this section. Shared namespace cell = config_max proposal via SM (card BANKED). Size headers = findings row 70.
