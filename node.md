---
id: experiment:a00-9e86d914-cd3906
mint_id: f8b3c17094c044999770314341da2d8d
type: experiment
parents:
  - hypothesis:l4-code-head-is-persisted-on-the-after-join-record-and-the-heal-watch-guards-execv-and-re-execs-only-on-a-changed-head-with-a-clean-tree
next_edges: []
confidence: 0.8
edited_by: a00-83915d4a
evidence_runs:
  - experiment:a00-9e86d914-cd3906
loop: hypothesis:l4-code-head-is-persisted-on-the-after-join-record-and-the-heal-watch-guards-execv-and-re-execs-only-on-a-changed-head-with-a-clean-tree@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 76754b7fdc38ccb0
season: 2
title: A00 9e86d914 cd3906
town: core
verdict: proved
---
# experiment:a00-9e86d914-cd3906

FIX-ONLY build (goal:g15.25 SL7.105 residue (b), parent hypothesis): measure the pre-fix state, IMPLEMENT the claim, prove it on the built bytes. Pre-fix measurements confirmed three of the four claim clauses were NOT met even though the SL7.89 re-exec seam existed:

- `rotate.run_after_join_for_seat` stamped `code_head` only on the RETURNED result dict (rotate.py:12136) and the skipped dict (:12050) — the PERSISTED `after_join` block written to disk at rotate.py:11827 carried NO code_head. Claim (1) part 1 unmet.
- heal.py:475 `after_join performed for <seat> ...` log line named record/dm but NOT code_head. Claim (1) part 2 unmet.
- `_check_code_change` compared the FULL identity (head + heal.py/rotate.py mtime+size), so a file-only ``touch`` (HEAD unchanged, clean tree) still re-exec'd — obsolete code the process no longer runs. `_reexec` called `os.execv` with NO OSError guard; a missing interpreter / EACCES / ENOMEM would propagate and END the watch loop. Claims (2) and (3) unmet.

## Fix land (built bytes)

- rotate.py: added `"code_head": _code_head(root)` to the written `rec["after_join"]` block (same pathspec-committed write as the results). `_code_head` is best-effort, never raises, empty on non-repo.
- heal.py performed line: `... dm sent: <sent>, code_head=<sha|?>`.
- heal.py `_check_code_change`: re-exec now fires ONLY when `fresh["head"] != identity["head"]` AND the tree is clean; a changed-HEAD dirty tree still logs ``waiting (dirty)``; execv wrapped in `try/except OSError` -> logged by name + errno ('re-exec error (<Name>, errno N): continuing on running bytes'), fresh identity adopted so the next attempt waits for the NEXT clean-tree HEAD change (no retry storm). Rule stated in the docstring.

## Proof (tests, named files)

`test_after_join_service.py test_record_after_join_block_persists_code_head` (with `rotate._code_head` -> 'c0debeef'): `saved["after_join"]["code_head"] == "c0debeef"` — on-disk block names the bytes.
`test_heal_watch.py test_watch_performed_line_names_code_head`: the performed line carries `code_head=c0debeef`.
`test_heal_watch.py test_watch_reexec_oserror_is_caught_loop_continues`: `_reexec` raising `OSError(13,...)` -> log `re-exec error (PermissionError, errno 13): continuing on running bytes`, exactly ONE error line, fresh identity returned (no retry storm), no raise.
`test_heal_watch.py test_watch_unchanged_head_never_reexecs`: changed mtime/size with UNCHANGED HEAD + clean tree -> `_reexec` NOT called, no re-exec log.
Existing `test_watch_code_change_clean_tree_reexecs_once` (changed HEAD + clean -> exec) kept green unchanged.

Suite: `pytest test_heal_watch.py test_after_join_service.py` = 111 passed; `test_heal.py test_heal_seats.py test_heal_ack_rotation.py test_heal_pin_reap.py test_heal_sweep.py` = 75 passed. Ceiling respected (src delta ~28 lines; 5 net new tests, 4 of them added this pass).

## Caveats / weaknesses

code_head is captured on the result AFTER `run_after_join` returns but the PERSISTED write happens INSIDE run_after_join via `_code_head(root)` — the two read HEAD at slightly different instants (a HEAD move in between stamps different shas on the returned dict vs the record). Cosmetic; both are honest HEAD reads. The performed-line test mocks the whole `run_after_join_for_seat` rather than a live rotate path, so it proves the heal log line format, not the live stamping (that is covered by the result-carrying test + the persist test separately).

## Agent Notes
FIX-ONLY build done: code_head persisted into record after_join block + named on performed line; execv OSError caught/logged with errno, loop continues; re-exec gated on CHANGED HEAD + clean tree (file-only never execs). 4 new tests; heal+after_join nbsa 111+75 green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, independently verified on the built bytes. (1) INSTRUCTION: the target hypothesis said code_head is NOT persisted on the record and os.execv is UNGUARDED and a file-only change still execs; (2) MEASURED: pre-fix, rotate.py:11827 rec['after_join'] had no code_head key (only the returned dict at :12136 did); heal.py:475 performed line carried no code_head; _check_code_change compared the FULL identity dict so touch-only with clean tree exec'd; _reexec called os.execv unguarded. Post-fix I read the bytes: rotate.py:11840 now writes 'code_head': _code_head(root) INTO that same block; heal.py:477 prints code_head=<sha|?>; heal.py:1008-1024 compares head-only first and wraps _reexec in try/except OSError logging type+errno and returning fresh identity. I ran the 6 named tests (all pass) and both full files: 111 passed. Accept proved. (3) NEAR MISS: a test that mocked run_after_join_for_seat and asserted a code_head key on the RETURN dict would satisfy claim (1)'s wording while missing the persistence — the kid's persist test reads the on-disk JSON instead, which is the discriminating form. (4) no deviation from a standing rule. Caveats accepted as cosmetic: the persisted read and the returned read are two _code_head calls at different instants.
<!-- THOUGHT:END -->
