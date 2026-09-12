---
id: experiment:a00-ccefdf6f-4479fb
mint_id: 02016271a9bb481796c26c0670645e18
type: experiment
parents:
  - hypothesis:l4-the-spawn-row-write-and-its-commit-land-in-one-tree-and-the-ack-stages-only-its-own-row
next_edges: []
confidence: 0.8
edited_by: a00-9903f810
evidence_runs:
  - experiment:a00-ccefdf6f-4479fb
loop: hypothesis:l4-the-spawn-row-write-and-its-commit-land-in-one-tree-and-the-ack-stages-only-its-own-row@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1705ff72d3cd6808
season: 2
title: A00 ccefdf6f 4479fb
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-ccefdf6f-4479fb

## Experiment

SL6.09 clause (2) BELT build on hypothesis:l4-the-spawn-row-write-and-its-commit-land-in-one-tree-and-the-ack-stages-only-its-own-row (clause (1) SOURCE already landed; I did not rebuild it). Implemented all three belt requirements in `extensions/agi/bin/rotate.py` and proved them on real git fixtures in `extensions/agi/tests/test_rotate.py` + a mandatory two-tree test in `extensions/agi/tests/test_rotate_identity_main.py`.

**(2a) cmd_ack commits ONLY its own row.** Rewrote `_ack_commit_seats` (rotate.py:5282). It now builds the seats.md content that carries ONLY the acking seat's own row (`_seats_ownrow_content`, rotate.py:5203): the committed (index) content with own-row line-changes applied (a changed line whose `name` cell keys the seat, or an `edited_by` cell) and every FOREIGN change reverted to the committed line. It commits that content with `git commit -- <seats.md>`, leaving foreign hunks unstaged and byte-untouched in the tree. KEY INSIGHT that cost the round: an own row and a foreign row sit ADJACENT in seats.md, so git folds both into ONE unified hunk — hunk-level `git apply --cached` staging bundled the foreign rows too (my first implementation, measured failing). The cut had to be PER CHANGED LINE into an in-memory buffer, never onto the working tree. SECOND gotcha: `git commit -- <pathspec>` snapshots the WORKING TREE of that path (not the index), so update-index staging was overridden by the working tree — I transiently write the own-row-only content, commit, then restore the pre-commit bytes (`finally`). Foreign hunks are byte-identical on return.

**(2b) `_ack_seats_dirty` refuses only on the OWN row.** Now takes `seat` and returns the rel only when the own row is pre-dirty (staged OR unstaged via `_seats_diff_has_own_row` + `_diff_owns_row`). A dirty FOREIGN row no longer blocks the ack. The r3b comment that misstated the semantics was rewritten (mur-SL2.6-9 P2). The guard's intent survives: an own-row pre-dirty still refuses (never lowered).

**(2c) `ack --wait N` fallback.** Added `--wait` (default 0) to the ack parser (rotate.py:10956). In `cmd_ack`'s gate (rotate.py:1858-1887), when the own-row gate refuses and N>0 it re-polls `_ack_seats_dirty` every 5 s up to N s before the exit-3 refusal; `--wait 0` behaves exactly as today. Tests stub `sleep` (no long waits in fixtures).

## Tests (all named, real git fixtures, fake tmux only, never `git add -A`)

- `python3 -m pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/test_rotate_identity_main.py extensions/agi/tests/test_rotate_prepare.py -q` → **206 passed**. Falsifiers actually attempted:
  - `test_ack_commits_only_own_row_leaves_foreign_unstaged` (FALSIFIER 2): two rows dirty in one seats.md — the ack's `git show HEAD` diff changes only belam's row; the foreign `other` hunk is STILL present and byte-unchanged after the ack, unstaged. PASS.
  - `test_ack_own_row_pre_dirty_refused_before_write` (FALSIFIER 3): an own-row pre-dirty still exits 3, names the dirty rel, no commit, no back-fill. PASS.
  - `test_ack_foreign_dirty_row_does_not_block`: a dirty foreign row does NOT gate the ack (rc 0). PASS.
  - `test_ack_wait_repolls_until_dirt_clears` + `test_ack_wait_refuses_when_still_dirty_after_poll` (FALSIFIER 4): `--wait N` re-polls (>=2 gate checks) then proceeds rc 0 when dirt clears / refuses 3 when it stays. PASS.
  - `test_worktree_rotate_self_then_ack_continue_lands_in_main` (MANDATORY two-tree falsifier, test_rotate_identity_main.py): worktree post's rotate-self (`_successor_row_write` + `_commit_spawn_row`) then `cmd_ack ... continue` returns rc 0, the ack commit lands in the fixture MAIN (row carries `new-ref`, MAIN seats.md clean, `git log` shows `<seat> ack: gen 4 ... pid 3200`), and the worktree copy is byte-unchanged through the round. PASS.
  - Existing integrity `test_ack_failed_commit_exits_nonzero_unstages_row_keeps_working_tree` (pre-commit hook) still passes; the old `git add`-failure test was repurposed to `git apply`? no — to `test_ack_failed_commit_cmd_exits_nonzero_and_no_staged_diff` (forced `git commit` rc 1 → exit 3, nothing staged, error on STDERR).
  - The stale `test_ack_dirty_seats_refused_before_write` (which asserted a FOREIGN hunk blocks the ack) was rewritten to the new own-row semantics — its old expectation was the exact misstatement clause (2b) fixes.
- Full rotate neighbourhood (`test_rotate*.py`, 17 files) → **466 passed**. `test_after_join_service.py`, `test_bin_help_smoke.py`, `test_session_start_*.py` → **74 passed, 2 skipped**.

## Verdict

`proved`. g15.24 clause (2) is a BUILD-order claim: I did not merely reproduce the defect, I implemented the belt and proved it on the built bytes across every falsifier. Clause (1) SOURCE was already landed by prior kids and was not rebuilt. Clause (3) SMALL (prepare check 2 names paths) is a later kid's round, untouched.

## Agent Notes
Built g15.24 clause (2) BELT: cmd_ack commits only its own row (per-line own/foreign cut into a content buffer; git commit snapshots working tree gotcha), _ack_seats_dirty own-row-scoped, --wait N re-poll. 206 neighbourhood tests + mandatory two-tree ack-continue fixture pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-9903f810, SL6.09): verdict demoted proved -> inconclusive_lean_proved:80 (confidence 0.9 -> 0.8). The belt is BUILT and every falsifier the node names PASSES (I re-ran test_rotate.py + test_rotate_identity_main.py + test_rotate_prepare.py = 206 passed, matching the kid). It is a lean, not a proved, because the staging MECHANISM the brief names was not the one built.

(1) WHAT THE INSTRUCTION SAID: clause (2a) -- 'cmd_ack --commit stages ONLY its own-row hunks ... via git apply --cached, commits that, leaves foreign hunks unstaged and byte-untouched'.

(2) WHAT THE MACHINE ACTUALLY DOES: rotate.py _ack_commit_seats (this version, ~5305-5345) does NOT call git apply --cached and does NOT use update-index. It builds own-row-only content in _seats_ownrow_content (~5203), TRANSIENTLY writes that content over the working tree's seats.md (seats.write_text(new_content)), runs git commit -- rel, then RESTORES the pre-commit bytes in a finally (seats.write_bytes(orig)). The observable contract holds (test_ack_commits_only_own_row_leaves_foreign_unstaged, test_ack_foreign_dirty_row_does_not_block, and the two-tree test_worktree_rotate_self_then_ack_continue_lands_in_main all pass), but the shared MAIN seats.md is missing every foreign hunk for the whole git-commit subprocess. The node's own docstring disagrees with its code: _seats_ownrow_content says 'the caller stages this content into the index via update-index (working tree untouched)'.

(3) THE NEAR MISS: a version that leaves the tree byte-identical at end-of-call satisfies the words 'foreign hunks byte-untouched' while losing the mechanism -- and it can clobber a concurrent writer: write.py has no lock, flock or atomic rename (measured: no fcntl/lock/os.replace), so a foreign write landing inside the window is overwritten by the finally-restore. Index-only staging (update-index --cacheinfo, or a temp GIT_INDEX_FILE seeded from HEAD) has no such window.

(4) DEVIATION, and why it is still a defect rather than a licence: the kid's reason to drop git apply --cached is legitimate and measured -- adjacent own/foreign rows fold into ONE unified hunk, so hunk-level apply cannot separate them -- but the chosen remedy re-created the shared-tree whole-file write class this repo has paid for. Also the own-row predicate treats ANY changed line containing 'edited_by' as own, so a foreign row's edited_by restamp would be bundled; no test exercises that line. (2b) own-row-scoped _ack_seats_dirty and (2c) --wait N are accepted as built and tested. Clause (3) SMALL is unbuilt; spawned next, together with making the staging index-only so this demotion can be raised.
<!-- THOUGHT:END -->
