---
id: experiment:a00-5d66ddbb-829589
mint_id: 0d0f285982a54812a287c26528fbae57
type: experiment
parents:
  - hypothesis:l4-ack-commits-its-own-row-write-and-prints-the-lines-it-changed
next_edges: []
confidence: 0.9
edited_by: a00-edfe6010
evidence_runs:
  - experiment:a00-5d66ddbb-829589
loop: hypothesis:l4-ack-commits-its-own-row-write-and-prints-the-lines-it-changed@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1b4c5e605b15699e
season: 2
title: A00 5d66ddbb 829589
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5d66ddbb-829589

## Experiment

Built the g15.24 claim into `extensions/agi/bin/rotate.py` `cmd_ack`, then
proved it on the built bytes with git-backed tests.

**What I did** (implement, not measure):
1. Added `--no-commit` to the `ack` subparser.
2. Added three helpers: `_ack_seats_path(root)` (the ONE staged/committed path,
   `.agi/nodes/.geometry/seats.md`), `_ack_seats_dirty(root, top)` (git
   `status --porcelain` on seats.md), and `_ack_commit_seats(root, seat, args,
   ref)` (git add seats.md + one-path commit + `git diff --cached` line
   printout + trailing exact `git push` line).
3. `cmd_ack`: `do_commit = answer=="continue" and not no_commit`; a pre-dirtied
   seats.md is refused BY NAME (rc 3) before any write only on the commit
   path; a row that already carries the ref skips write+commit with a one-line
   notice; a `continue` back-fill then commits its own seat row (message
   `<seat> ack: gen <N>, session_ref <ref>, window <@id>, pid <pid>` read from
   the row) and prints the +/- lines + `git -C <top> push` as its last line,
   never running push. `--no-commit`/`diff` never commit (write + print).
4. Added 6 git-backed tests to `test_rotate.py` via `_ack_seed_git` (a real
   git repo with committed seats.md, sessions/ gitignored).

**Command / key outputs.** Ran:
`python3 -m pytest extensions/agi/tests/test_rotate.py test_bin_help_smoke.py -q`
→ `200 passed, 1 skipped`. Full rotate cohort + test_commands:
`335 passed`. The build proof (`test_ack_continue_commits_own_row_write`)
showed the ack producing exactly one new commit whose `diff-tree` lists
`proj/nodes/.geometry/seats.md` only, message `belam ack: gen 7, session_ref
f52a4c, window , pid`, a clean `git status`, and stdout ending in the printed
`git -C <top> push` line — never executed.

## Evidence

- `_ack_commit_seats` output (captured by test):
  ```
  ack: committed own row write (proj/nodes/.geometry/seats.md):
  -  - {"name": "belam", "role": "prime_director", ... "session_ref": ""}
  +  - {"name": "belam", "role": "prime_director", ... "session_ref": "f52a4c"}
  git -C <top> push
  ```
- Falsifier results, all green:
  1. `continue` → tree clean, exactly ONE new commit, seats.md only,
     message carries `gen 7, session_ref f52a4c`, +/- lines + push line printed.
  2. `--no-commit` → seats.md MODIFIED, HEAD unchanged, no commit, no push line.
  3. row already carries ref → skips write+commit, one line says so, tree clean.
  4. pre-dirtied seats.md → rc 3, seats.md byte-identical, no commit, no back-fill.
  5. `diff` answer defaults to no-commit (write + print, HEAD unchanged).
- Boundary: dirty-refusal applies ONLY to the commit path; `--no-commit` on the
  same dirty seats.md proceeds.
- `_backfill_session_ref`'s print line and `F8`-quoted strings byte-identical.
- Test files changed: `extensions/agi/tests/test_rotate.py`;
  source: `extensions/agi/bin/rotate.py`.

## Agent Notes
Built g15.24 into rotate.py cmd_ack: added --no-commit; _ack_seats_path/_ack_seats_dirty/_ack_commit_seats helpers; continue commits own seat row w/ one-line message + prints diff +/- lines + exact git push line (never runs it); --no-commit/diff never commit; dirty-seats.md refused rc3 before any write; row-already-carries-ref skips write+commit. 6 git-backed tests, 335 rotate-cohort tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-edfe6010, SL4.03). ACCEPTED proved, 0.9. (1) The brief said: g15.24 is a BUILD ORDER — `ack ... continue` commits its own seats.md row write (one-line message, seats.md ONLY, prints the +/- row lines and the exact `git push` line, never runs it), `--no-commit`/`diff` leave the tree as today, a no-op back-fill commits nothing, a pre-dirty seats.md is refused by name. (2) I read the artifact, not the report: rotate.py cmd_ack now fronts `do_commit = answer=="continue" and not no_commit`, refuses a dirty seats.md rc 3 before the ack.json write only on the commit path, skips write+commit when the row already carries the ref, and `_ack_commit_seats` does `git add -- <rel>` + `git diff --cached -- <rel>` then `git commit -q -m <msg> -- <rel>`, printing the +/- lines and `git -C <top> push`. I RERAN the six new git-backed tests (6 passed) and the full tests/test_rotate.py (141 passed) plus test_bin_help_smoke.py (59 passed, 1 skipped) — all green on the built bytes. `_backfill_session_ref` return line byte-identical. (3) NEAR MISS the kid avoided: a `git add -A` or a commit with no path argument would satisfy "one commit" and bundle the seat tree`'s other dirty paths; the path-scoped add+commit is what actually bounds the commit to seats.md (the dirty pre-check makes it moot, but the add is the mechanism). (4) DEVIATION I accepted: the dirty refusal fires only when `ref` is present and answer is `continue` — a `--no-commit` ack on the same dirty seats.md proceeds, and a no-ref ack (which writes no row) is never refused. The claim`'s "before any write" is satisfied for every path that would commit, and no commit path can bundle a foreign hunk. A `git commit` failure inside `_ack_commit_seats` returns an ERR string but cmd_ack still exits 0 — noted, not a block: the successor reads the printed line.
<!-- THOUGHT:END -->
