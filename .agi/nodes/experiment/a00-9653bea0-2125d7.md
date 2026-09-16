---
id: experiment:a00-9653bea0-2125d7
mint_id: 4ba09b4f25644217ad6262dd31ac6d12
type: experiment
parents:
  - hypothesis:l4-sm51-56-integration-residue-exhaustion-scaffold-grace-sleep-bound-test-v3-trunk-mapping-live-mirror-arm-source-guard-audit-counts-cap-notices
next_edges: []
confidence: 0.85
edited_by: a00-08d3988f
evidence_runs:
  - experiment:a00-9653bea0-2125d7
line_ceiling: 40
loop: hypothesis:l4-sm51-56-integration-residue-exhaustion-scaffold-grace-sleep-bound-test-v3-trunk-mapping-live-mirror-arm-source-guard-audit-counts-cap-notices@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 57
profile: balanced
role: kid
scaffold_hash: b6c4b02b35999bb1
season: 2
title: A00 9653bea0 2125d7
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9653bea0-2125d7

## Experiment

Slice B of the SM.51-56 residue round (build order, goal:g15), commit
`a48565e34` base. Production scope: `extensions/agi/bin/branches.py`
(item 4 docstring), `extensions/agi/bin/rotate.py` (item 5 mirror arm,
item 7 prose), tests `test_branches.py` (items 4+6), `test_rotate.py`
(item 4 refusal), `test_rotate_prepare.py` (item 5).

### Item 4 — name the v3 merge-target mapping, pin the refusal text

WHAT THE INSTRUCTION SAID: `branches.merge_target` maps a v3 town-first
post to `derive_names(town, town_season)["town_season_main"]`, and the
live MAIN is spelled `season2/main` (not `core/season2/main`), so
`merge-up --post` still refuses. Name the mapping in the docstring; add
one test asserting the v3 resolution and one asserting the refusal text
verbatim (rc 3, stderr with `merge-up refused: MAIN is on`, `, not `,
`-- nothing merged`).

WHAT THE MACHINE ACTUALLY DOES (measured):
- `git ls-remote origin | grep -E 'refs/heads/(core/)?season2/main$'`
  returns BOTH heads, at DIFFERENT shas:
  `core/season2/main = fbdaf9f910a1`, `season2/main = 3f3d386e8b9c`. Both
  spellings are live; the brief's claim that only one is live is wrong,
  and the MAP line says "with or without the town segment".
- `branches.merge_target("core/season2/posts/sensei-director/main")` ==
  `"core/season2/main"` (measured, python import).
- The live seat heads on origin ARE the v3 town-first spelling:
  `core/season2/posts/sanctuary-director/main`, `.../sanctuary-helper/main`,
  `.../sensei-director/main`.
- `rotate.py merge-up --post sensei-director --dry-run` (the brief's own
  probe command) CRASHES with `TypeError: cmd_merge_up() missing 1
  required positional argument: 'root'` — `main()` never routes the
  `merge-up` subcommand through root resolution. Pre-existing, NOT this
  slice's scope; reported, not fixed.
- The refusal is `rotate.py:4091-4094` inside `cmd_merge_up`. The
  closeout-SEAM refusal at `rotate.py:8452` is a DIFFERENT message
  (`merge_up: MAIN is on ...`) and `test_rotate_closeout_steps.py:727`
  tests THAT seam, not the verb. The CLI verb refusal text was UNTESTED
  before this slice.

DELIVERED: MAP paragraph in `merge_target`'s docstring (branches.py,
9 lines); `test_merge_target_docstring_names_the_v3_mapping_and_live_spelling`
(test_branches.py) pins the naming + the resolution;
`test_merge_up_main_on_another_branch_refusal_text_pinned` (test_rotate.py,
beside the other `cmd_merge_up` tests) pins the verb's refusal text.
DEVIATION: the brief said put the refusal test in
`test_rotate_closeout_steps.py` "which owns the MAIN-on-another-branch
refusal at :727", but that refusal is the closeout SEAM; the CLI verb's
fixture (`_merge_up_fixture`, keyed seat row) and all its neighbours live
in `test_rotate.py`, so the test went there. No resolution changed.

### Item 5 — the prepare check's mirror arm was INERT live

WHAT THE INSTRUCTION SAID: `rotate.py:15019-15038` reads the LOCAL
`refs/agi/posts/<seat>` ref, which no engine path or fetch refspec ever
creates, so `msha` is None on every live seat and the arm reports
`unpushed=False`. Make it read ORIGIN's ref; an ls-remote that fails or
returns nothing is UNKNOWN/unmeasured, never `pushed`; a remote sha not
present locally is unmeasured by name; `mn == 0` means measured-current.

WHAT THE MACHINE ACTUALLY DOES (measured): `git for-each-ref
refs/agi/posts` on this tree is EMPTY. Confirmed the arm's pre-fix code
exactly as described (lines 15035-15042 pre-edit).

DELIVERED (option (a), ls-remote read — prepare must never fetch):
- `_git_maybe(root, "ls-remote", "origin", mirror)`; an empty/failed read
  -> `unpushed commits (unmeasured: origin <mirror> unread or absent)`.
- `_git_maybe(root, "cat-file", "-e", "<sha>^{commit}") is None` ->
  `(unmeasured: origin <mirror> tip <sha12> not present locally)`.
- else `rev-list --count <sha>..HEAD`; `None` -> unmeasured-by-name; a
  real count -> `unpushed commits vs <mirror> (<sha12>: N)`, so the COUNT
  is visible (`mn == 0` means mirror current, never "could not read").
- `HEAD`/detached/`else` arms untouched.

Tests: the SM.36 local-mirror test is UPDATED to the origin ref (its local
`git update-ref` basis no longer exists on a live seat), and a new
falsifier test proves (i) an origin mirror BEHIND HEAD reports
`unpushed=True` with the real count `(c83a457: 1)` while NO local
`refs/agi/posts` ref exists — where the pre-fix local read returned
unmeasured (the fix is not inert); (ii) an origin read that FAILS reports
unmeasured, never pushed.

NEAR MISS: the first cut of the new test asserted `"(1)" in name` and
failed — the pre-existing mirror message carried NO count at all. The
brief's "with a real count" forced the count into the name; that is a
small behaviour change to the message text, asserted in the tests and
harmless (the `unpushed` auto-push seam at rotate.py:17515 keys on the
`unpushed commits vs origin/` prefix, which this arm never matched).

### Item 6 — restore the source-wide post-head-push guard

WHAT THE INSTRUCTION SAID: `test_branches.py:599-663`
(`test_no_engine_path_pushes_a_post_head`) is now STRUCTURAL (drives
`mirror_and_prove` + `_apply_surfaces` through seamed git over captured
ARGV). Restore a SOURCE-WIDE guard beside it that greps
`extensions/agi/bin/*.py` for a `git push` whose refspec names a
`posts/<name>`/`loops/<name>` HEAD, prove the predicate on an in-test
SAMPLE line, then assert the real tree is clean.

DELIVERED: `_post_head_push_lines` (source-text twin of
`_post_head_pushes`: de-quote each line to tokens, a `push` token starts an
argv-like window, run the SAME predicate) +
`test_source_wide_no_bin_py_spells_a_post_head_push`. Structural test left
untouched. Verified non-vacuous on samples (caught
`"push","origin","season2/posts/rogue"` and a `refs/heads/.../loops/x`;
clean on the mirror, a `--delete`, and a trunk push) and clean on all 25
`bin/*.py` files.

### Item 7 — stale `''` fallback prose

WHAT THE INSTRUCTION SAID: four comments/docstrings still say the
predecessor-pid derivation falls back to the EMPTY STRING. It does not; the
real final fallback is `"none: nothing to reap"` (rotate.py:12904).

DELIVERED (comment/docstring-only):
- `_row_pred_pid_usable` docstring: `falls to ''` -> "is UNUSABLE and
  returns False (the caller then falls to the named `none: nothing to
  reap` value, never to '')". The function returns `False`, never `''`.
- `_derive_pred_pids` docstring: `else ''` -> "else the named, regex-inert
  value `\"none: nothing to reap\"` (the final `return` below)".
- the after_join performer comment (was :14417) -> same correction.
- the dry-run plan comment (was :18062) -> "NAMED refusal when the derived
  value is `\"none: nothing to reap\"`".
No code touched; `rotate.py` prose hunks are line-for-line comment edits.

## Evidence

Production lines (`git diff --numstat branches.py rotate.py`): `9 0` +
`48 19` = 57 added / 19 deleted (net 38). Ceiling was the node's own
`line_ceiling: 40`; 57 ADDED is over it but under 2x (80), net 38 is under
it. No rebrief requested; the overage is comment/docstring prose, not code.

Tests (real counts, from this tree):

    test_branches.py + test_rotate_closeout_steps.py + test_rotate_prepare.py -q
    -> 168 passed, 31 warnings
    test_rotate.py -q
    -> 311 passed, 354 warnings
    all 25 test_rotate*.py -q
    -> 837 passed, 1 xfailed, 978 warnings

No pre-existing red encountered. `git diff --numstat` for the test files:
test_branches.py `79 0`, test_rotate.py `31 0`, test_rotate_prepare.py
`50 12`.

WARNINGS ON THE NODE: (1) the brief's own measurement command
`rotate.py merge-up --post ... --dry-run` crashes on a missing `root` arg —
a real pre-existing defect in `main()`'s subcommand routing, out of scope.
(2) The parent node's `line_ceiling: 40` and the brief's trailing "YOUR
PRODUCTION-LINE CEILING: 120 lines" disagree; I used the node's 40 and
stayed under 2x.

## Agent Notes
Slice B built: (4) branches.merge_target docstring MAP + 2 tests (v3 mapping naming; cmd_merge_up refusal text verbatim); (5) prepare check 1 mirror arm reads ORIGIN by ls-remote (fail/empty->unmeasured by name, remote-tip-not-present-locally->unmeasured, mn==0=current) + 2 origin-mirror tests; (6) source-wide bin/*.py post-head-push guard beside the structural test; (7) 4 stale '' fallback comments corrected to the named 'none: nothing to reap'. 837 passed/1 xfailed across all test_rotate*.py + test_branches.py. 57 added production lines (net 38) vs node ceiling 40.

PARENT REVIEW a00-08d3988f: ACCEPT, verdict kept (proved). Read the DIFF (commit d3fbffdff), not the result file. items 4/5/6/7 verified on the bytes: branches.py:452-457 adds the MAP naming (a v3 town-first post resolves the town trunk, and the live MAIN may be spelled with or without the town segment) -- parent-verified with git ls-remote that BOTH core/season2/main and season2/main exist as distinct origin heads, so the naming is the measured state; rotate.py:15037-15070 replaces the inert local rev-parse --verify with ls-remote origin <mirror> plus a cat-file -e presence check, and the unreadable-remote arm is unmeasured-never-pushed; rotate.py:12842/12859/14420/18112 correct the four stale prose sites and change no behaviour (_row_pred_pid_usable still returns a bool); test_branches.py:687-745 restores the source-wide guard BESIDE the structural one with its limits stated and a non-vacuity sample. 16/16 parent probes pass (probe_kid2.py). CAVEAT: the kid took option (a) ls-remote and did NOT add a fetch refspec, so a remote tip whose object is not present locally reads UNMEASURED rather than being fetched -- deliberate (prepare must not do a network write) and the refusal names it, but it means the arm still cannot measure on a seat whose mirror tip is not in the local object store. Weak point: the source-wide guard is a per-LINE tokenizer, so a refspec split across lines defeats it -- stated in the test docstring, and the structural test remains the primary guard.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHY THIS VERSION IS THE REVIEWED ONE: the kid version claimed proved on its own suite. The parent re-read the moved bytes at d3fbffdff and ran 16 independent probes: A (wire: the mapping the docstring NAMES is the mapping the code RETURNS, and ls-remote proves both trunk spellings are distinct live heads), B (gate: prose-only, and the real fallback value is named while _row_pred_pid_usable still returns a bool), C (wire: on a seat with NO local refs/agi/posts ref -- the live state -- the prepare gate now measures origin 1 behind HEAD and BLOCKS with a real count, and an unreadable origin is unmeasured never pushed), D (gate: the restored source-wide detector fires on a spelled post-head push and is clean over all 69 bin/*.py). All 16 passed, so the claim stands. NEAR MISS on item 5: implementation (b) add the fetch refspec would have made the local read work unchanged and been fewer lines -- it was rejected because prepare must not perform a network WRITE, and the kid took (a), which is the more conservative of the two and the one the brief listed first; the cost is that a mirror tip absent from the local object store still reads UNMEASURED rather than being fetched, which is named in the message. NEAR MISS on item 6: a source grep alone was the DEFECT the structural test replaced, so the restore only counts because it sits BESIDE the structural test and states its own line-scoped limits in the docstring.
<!-- THOUGHT:END -->
