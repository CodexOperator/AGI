---
id: goal:g7.16.1.11.46.11
mint_id: 350502b733dc4902a557a6fd932926f5
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.46.11
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
tags:
  - brainstorm
  - wave-1
  - V10a
season: 3
status: active
title: "G7.16.1.11.46.11: V10a -- the retired identity variable is named nowhere outside the history paths: AGI_POST is the one identity variable, its fallbacks are gone, and a strict standing test keeps it so"
town: local-maxxing
---
# goal:g7.16.1.11.46.11

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 (sanctuary-master 10-23): the brief's done-when names "seat_status.py retired"; the council (alive 21:3xZ, 3/3) moved that retire to the §34.5 census-cell leaf (wave 2), option B. Reason: seat_status.py is a LIVE reader (viewport.py imports it at 5 sites, fail-soft) and retiring it before the census cell exists drops the posts board from `viewport.py --live`; its file name is the word, which is V10b's, not this variable's. Placed, not promised: this node's Out of scope, and doc:card-belam §7 row 8.1 (open, target the census leaf). Graph text names the variable as `AGI_[retired]` (council: agreed, it keeps closed records true); 0 owner-verbatim bytes were rewritten. The history paths are four EXPLICIT paths (council), never a generic deprecated segment.
<!-- THOUGHT:END -->

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 1): V10 of doc:brainstorm-unify §35, the lexical half of "posts, never seats". belam's brief (hypothesis:g7161146-w1-protect-the-loop-and-measure) names it sanctuary-master's MECHANICAL leaf, not a council design. The council (alive's [decision] 21:05Z 10-23, 3/3) ruled its scope: V10a = the variable, with a STRICT negative test; V10b (the word sweep, the ~30 id renames, the closed-record exclusion) = wave 3, after V1, with the owner's word on the exclusion. Box readings (trunk 2ef3c2f6d6): 821 refs in 253 files; only 3 LIVE readers (geometry_config.resolved_seat_env's fallback, and the two SessionStart hook copies' `${AGI_POST:-${...}}`); both agi-post@ units already set AGI_POST=%i (engine-root.md :29, :70); no repo setter. One host leftover sits outside the repo: /opt/agi/bin/agi-sync, a stale root copy from 10-04 that prints the variable in a display header only (a host item for belam). belam: units and pieces reach live posts only at a boot pin move, so the live-readers check runs there, not before.

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; the lexical half only, the walk half is wave 3)
| 5.1 | posts, never seats; stand guard, never idle | target:§35 (V10 + the walk as idle state) |

## Target end-state
- AGI_POST is the one identity variable. geometry_config.resolved_seat_env() reads AGI_POST only (no fallback, no env notice), and the hooks read `${AGI_POST:-}`.
- Every test that set, scrubbed or asserted the retired variable is rewritten by hand. A negative row that only proved its absence is folded into the standing test, and each mutant still reads RED (post-env m3/m4 mutate to another variable; m5 is a helper that ignores AGI_POST).
- Graph text names it as `AGI_[retired]` (never `AGI_POST`, which would make a closed record state a falsehood); every changed frontmatter still parses.
- test_rotate_main_seat_rows.py and test_session_start_seat_pre_spawn.py are renamed (…_post_…), history untouched.
- extensions/agi/tests/test_no_retired_identity_variable.py is the standing test.

## Invariants
- The history paths are not rewritten: `.agi/nodes/deprecated/`, `extensions/agi/guard/deprecated/` (the three retired guard drop-ins), `.agi/sessions/rotations/`, `datasets/`; git history is the archive.
- No pattern exemption: the ONE escape is the test's committed ALLOW (path + sha256 of the exact line), for an owner-verbatim line only; it is empty today and a stale entry is red.

## Falsifier
1. `python3 -m pytest -q extensions/agi/tests/test_no_retired_identity_variable.py` exits 0. It scans tracked + untracked files with `git grep --untracked -F` for the name outside the four history paths, minus ALLOW.
2. Mutants: a planted untracked scratch file under extensions/ holding the variable set to x makes test 1 exit 1 (proved on the build, and as a row in the test on a scratch repo); the same under extensions/agi/bin/deprecated/ is RED too.
3. `git grep -c resolved_seat_env -- extensions/agi/bin/geometry_config.py` is >= 1, and its body reads AGI_POST only (post-env.t.sh p1 + m5).

## Out of scope
seat_status.py retire -> the §34.5 census-cell leaf (wave 2; council option B, card-belam §7 row 8.1) · V10b (the word "seat|seats|seating" everywhere, the ~30 node-id renames, the closed-record exclusion: wave 3, after V1, with the owner's word) · the walk half of §35 (wave 3) · /opt/agi/bin/agi-sync (a root host file; belam).

## Agent Notes
Assigned to **sanctuary-master**.
