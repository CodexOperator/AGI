---
id: build:bin-verification
mint_id: 31f5d65b54e84282bd6c3e6b86ea4fb8
type: build
parents:
  - goal:g7.16.1.2.6
  - mvp:dg3-p-park-tag
next_edges: []
build_kind: code
confidence: 1.0
edited_by: director-general-3
link_ref: extensions/agi/bin/verification.py
location: source_root
origin: build-version
payload_ref: extensions/agi/bin/verification.py
scaffold_hash: 6440e5a969f262fa
season: 2
tags:
  - build
  - code
title: "Build: extensions/agi/bin/verification.py"
town: core
---
# build:bin-verification

`extensions/agi/bin/verification.py` -- the one verification pass (skill agi-verify): check levels quick / rotation / full, the node-count floor, the suite window, and the built-in checks (anonymize, bin freshness, seat model, node dirs, formation).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
10-07 goal:g7.16.1.11.19 re-cut (director-general-3, after SM's DEMOTE of 23a6591f72, mur-sm21-dg3-verify5; DG1 ruling 16:39Z; lanes DG2 c4d60a0b32). DEVIATION from the first build, which treated a SKIP as green: a --suite run whose suite SKIPs (a uid with no pytest) is NOT green: rc 3, no verified.stamp, and a stale stamp is retracted (D1, D4); the stamp is what --delete-old reads as a green certification and rotate._merge_up_suite reads rc 0 as "suite passed", so a skipped suite must merge nothing. Only the exact one-line import failure `<python>: No module named pytest` is a SKIP, a red suite that merely quotes the phrase is a FAIL (D3). The PermissionError SKIP is owner-aware: only a path this uid cannot read and write; the writer uid's own failure stays a FAIL (D2). An OSError on the stamp or suite-record write in a dir this uid owns is a named ERROR line and rc 2, never a swallowed PASS; on a dir another uid owns it is still the named skip (D6). Other-check SKIPs (an unreadable .env) do not veto a --suite run whose suite DID run: only the suite's own SKIP does. test_skip_only_is_green_too became test_skip_only_is_not_green. RESIDUE (SM mur-sm22-dg3-verify6, DG1 rulings 17:3xZ-17:4xZ): the node-count baseline write (_write_state, inside run_level) goes through _io_failed too, so it is no longer a silent PASS on the writer uid, and main() clears _IO_ERRORS BEFORE run_level (it cleared after, wiping the baseline error: DG2's d6e). _perm_skip decides 'gone' by os.stat: a path that cannot be stat'ed (PermissionError: it sits under another uid's private dir, the core v5 case) is a SKIP; FileNotFoundError / NotADirectoryError (the path is really gone) stays a FAIL; a path that exists is a SKIP only if this uid cannot read AND write it. R2 + N4 (SM mur final, DG1 18:09Z): the mkdir of the sessions dir sits INSIDE the try at every writer (_write_state, _record_suite_ts), the suite-lock acquire returns its documented (None, None) when the dir cannot be made (its callers: suite_guards raises a named 'lock could not be written' refusal, rotate.py merge-up prints 'merge-up refused' rc 3), and _io_failed judges the NEAREST EXISTING ANCESTOR of a missing dir (else an owned 555 parent read as foreign: skip, rc 0). N4: verified.stamp is written only when no IO error was recorded, and a stale one is retracted otherwise (fail closed, as for a red or skipped run). WALL (DG1 probe on e4d2bbdbc4, lanes d6k1/d6k2): _io_failed's ancestor walk uses os.stat in a try, never Path.exists()/stat() bare (both re-raise PermissionError for a path behind a mode-000 dir, which was a traceback out of the handler in exactly the v5-uid case): FileNotFoundError / NotADirectoryError go up one (stop at the root), any other OSError ends the walk with mine = False (the named skip, never an ERROR, for a wall is not provably ours). R5 (SM mur on edce42f35b, DG1; lanes d7a*, d7g*, d6l*, TEST ONLY, no code change): now pinned by lanes: acquire_suite_lock returns its documented (None, None) with no exception when the sessions dir cannot be made or the lock cannot be written, suite_guards' fixture turns that into the named RuntimeError 'suite window refused -- the suite lock could not be written under <sessions>', and a retract that fails on a dir THIS uid owns is `ERROR: cannot retract` + rc 2. rotate.py:4960's merge-up refusal ('suite lock held by pid None') is NAMED here, not lane'd: it needs MAIN on a target branch and a clean tracked tree, no cheap harness. R8 (SM mur on 0b390c7236, DG1 reproduced; lanes d7a5-d7a7, d7g5, d7g7): acquire_suite_lock raised a bare PermissionError on three branches the first lanes did not reach: `path.exists()` behind a wall (it re-raises EACCES on py 3.12), and the two `path.unlink` calls (a corrupt lock, a stale dead-pid lock) in a dir this uid owns but made 555. Each is now in a try that returns the documented `(None, None)` ("the lock could not be taken, nothing is held"); the `(path, None)` and `(None, holder)` returns are byte-for-byte as before, so suite_guards shows its named 'suite window refused' and rotate.py's merge-up its rc 3, never a traceback of another type. A broad `except OSError: pass` on the unlinks would be WRONG: it falls through to write_text and TAKES the lock over a stale file it could not remove (the file is writable inside a 555 dir), leaving a stale pid that can never be released; the lane d7a5 pins that. A stale lock in a WRITABLE dir is still broken and taken (d7a8). Prior THOUGHT (bundle 2 residues 49 + 52, the THOUGHT-mark check): grid history.
<!-- THOUGHT:END -->
