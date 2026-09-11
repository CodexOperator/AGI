---
id: hypothesis:l4-the-never-lower-baseline-is-stamped-only-by-a-kept-merge
mint_id: ff5e697fffe94b9e967bfb6724620878
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 2135f96a6c5c60d3
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 28 review by name (wf_2a45a87d-b16), goal:g15 newest note at 3cd6e6bd9; line numbers on 9b4186086. g15-16 (= p7 as the prime filed it), MEASURED at merge-up 28: the red 28c read (2792/1 failed) stamped `.agi/sessions/verify-count.json` = 1921; 28c was dropped with `git reset --keep`, the green re-run on the pushed bytes (1915) then FAILED `node-count` against a baseline that never existed on the branch; the prime reset the file by hand with the reason in it. CLAIM: `verification.py` records the baseline only when the run is on bytes that are KEPT — the tree is `season/s2` (or the declared integration branch) AND HEAD is an ancestor of / equal to the pushed `origin/season/s2`, or an explicit `--stamp` flag is passed by the merge-up step AFTER the push; a run on a worktree, a seat branch, or an unpushed MAIN read compares but does not stamp (the note says `baseline not stamped: <reason>`); the state file carries `{active, deprecated, total, sha, stamped_at, reason}` so a hand reset is never needed; a baseline whose sha is not an ancestor of HEAD is reported (not silently used). TESTS with a fixture repo: unpushed read compares-not-stamps; pushed/kept read stamps; explicit --stamp; a lower count on a kept merge still FAILS. FALSIFIER: a red or dropped read that stamps. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/verification.py + extensions/agi/tests/test_verification*.py (+ commands.py ONLY if the verify-suite step must pass --stamp — say so). EXCLUDED: rotate.py, crons.py, the merge-up procedure text."
title: verification.py stamps the never-lower node-count baseline only from a KEPT merge on season/s2, never from a first read of droppable bytes
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-never-lower-baseline-is-stamped-only-by-a-kept-merge

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 28 review by name (wf_2a45a87d-b16), goal:g15 newest note at 3cd6e6bd9; line numbers on 9b4186086. g15-16 (= p7 as the prime filed it), MEASURED at merge-up 28: the red 28c read (2792/1 failed) stamped `.agi/sessions/verify-count.json` = 1921; 28c was dropped with `git reset --keep`, the green re-run on the pushed bytes (1915) then FAILED `node-count` against a baseline that never existed on the branch; the prime reset the file by hand with the reason in it. CLAIM: `verification.py` records the baseline only when the run is on bytes that are KEPT — the tree is `season/s2` (or the declared integration branch) AND HEAD is an ancestor of / equal to the pushed `origin/season/s2`, or an explicit `--stamp` flag is passed by the merge-up step AFTER the push; a run on a worktree, a seat branch, or an unpushed MAIN read compares but does not stamp (the note says `baseline not stamped: <reason>`); the state file carries `{active, deprecated, total, sha, stamped_at, reason}` so a hand reset is never needed; a baseline whose sha is not an ancestor of HEAD is reported (not silently used). TESTS with a fixture repo: unpushed read compares-not-stamps; pushed/kept read stamps; explicit --stamp; a lower count on a kept merge still FAILS. FALSIFIER: a red or dropped read that stamps. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/verification.py + extensions/agi/tests/test_verification*.py (+ commands.py ONLY if the verify-suite step must pass --stamp — say so). EXCLUDED: rotate.py, crons.py, the merge-up procedure text.
