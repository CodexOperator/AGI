---
id: experiment:a00-1792dd61-4850e1
mint_id: 50b389da16ff40318583b4c103b21777
type: experiment
parents:
  - hypothesis:l4-a-failed-ack-commit-exits-non-zero-and-unstages-and-three-tests-assert-what-they-claim
next_edges: []
confidence: 0.95
edited_by: a00-cd127adb
evidence_runs:
  - experiment:a00-1792dd61-4850e1
loop: hypothesis:l4-a-failed-ack-commit-exits-non-zero-and-unstages-and-three-tests-assert-what-they-claim@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ad22abd822e17d50
season: 2
title: A00 1792dd61 4850e1
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1792dd61-4850e1

## Experiment

P1 of the parent's brief (the three P2 test-integrity items were HELD for a
follow-up kid): implemented the failed-ack-commit fix in
`extensions/agi/bin/rotate.py`.

**Pre-fix defect (measured):** `_ack_commit_seats` returned an `ERR: ...`
STRING on a failed `git add`/`git commit`; `cmd_ack` PRINTED that string to
STDOUT and exited 0, leaving seats.md STAGED — so the next ack was refused
by the dirty gate `_ack_seats_dirty`.

**The fix (two edits, in place):**
1. `_ack_commit_seats` now returns `(ok, out)` — a tuple, so `cmd_ack`
   distinguishes success from failure WITHOUT parsing prose. On EITHER
   `git add` rc!=0 OR `git commit` rc!=0 it runs `git reset -q -- <rel>`
   (working tree keeps the back-filled row) and returns `(False, ERR...)`.
2. The `cmd_ack` call site (the only caller) unpacks the tuple: on success
   it prints `out` to STDOUT unchanged (byte-identical success path — the
   +/- lines and the exact `git -C <top> push` line); on failure it prints
   the error to STDERR and returns 3 (the same exit code the pre-dirtied
   gate uses).

**Tests (added to test_rotate.py):**
- `test_ack_failed_commit_exits_nonzero_unstages_row_keeps_working_tree`:
  forces the commit to fail with a fixture `.git/hooks/pre-commit` that
  `exit 1`, then asserts (1) exit==3, (2) `git diff --cached -- seats.md`
  is EMPTY (unstaged), (3) the row is still written in the WORKING TREE
  (session_ref kept), plus error-on-stderr / not-on-stdout.
- `test_ack_failed_git_add_exits_nonzero_and_no_staged_diff`: forces
  `git add` to fail via a mocked subprocess (rc 1), asserts exit==3 and no
  staged diff, error on stderr.

**Falsifier (proven both ways):** both new tests FAIL against the pre-fix
code (`assert code == 3, got 0` — the old code exited 0 and left the row
staged) and PASS on the fixed bytes. Shown by reverting the two rotate.py
edits, running the tests (2 failed), restoring, and re-running (6 passed in
the ack-oriented selection; the full test_rotate.py passes 148/148).

## Evidence

- Pre-fix reproduction confirms the defect: forced commit failure => `ERR:
git commit failed:` on STDOUT, exit code 0, seats.md still STAGED.
- Traps hit:
  - The harness injects agent-git hooks via `GIT_CONFIG_COUNT/KEY_0/VALUE_0`
    environment (command-line config, beats the repo's own config), so a
    `.git/hooks/pre-commit` fixture is silently ignored by default. The test
    clears those env vars (`monkeypatch.delenv`/`setenv`) so the fixture
    hook actually runs.
  - `_ack_commit_seats`'s success return used a backslash line continuation;
    wrapping it in a tuple broke, then restored — final form uses a
    parenthesized continuation with no trailing backslash (syntax-verified).

`python3 -m pytest extensions/agi/tests/test_rotate.py -q` => 148 passed.
<!-- BODY:END -->

## Agent Notes
P1 fix: _ack_commit_seats returns (ok,out); on git add/commit failure resets row (working tree keeps it), error->stderr, cmd_ack exits 3. Two new tests in test_rotate.py prove falsifier both ways (fail pre-fix, pass post-fix); full suite 148 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (SL5.08 a00-cd127adb, P1 kid). Read the artifact, not the report. _ack_commit_seats now returns (ok, out); on git add rc!=0 OR git commit rc!=0 it runs `git reset -q -- <rel>` and returns (False, ERR); the ONLY caller (cmd_ack, rotate.py:1928) unpacks the tuple, prints success to stdout unchanged and failure to stderr, then returns 3. grep over extensions/ confirms no other caller and no test binds the old string return. Independently ran `pytest extensions/agi/tests/test_rotate.py -q` -> 148 passed on these bytes. Falsifier holds by code reading: pre-fix cmd_ack had no return on the commit path, so it exited 0 with seats.md staged. Claim implemented, not merely measured. Accepted proved.
<!-- THOUGHT:END -->

P1 reviewed + accepted: failed ack add/commit now unstages, errors to stderr, cmd_ack exits 3; 148 test_rotate.py passed.
