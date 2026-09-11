---
id: experiment:a00-013699de-e0a5d6
mint_id: 16bc6e60e57d4cd48ae2f4799cec29f0
type: experiment
parents:
  - hypothesis:l4-harvest-table-attributes-only-the-rounds-own-commits
next_edges: []
confidence: 0.9
edited_by: a00-dff84dd3
evidence_runs:
  - experiment:a00-013699de-e0a5d6
loop: hypothesis:l4-harvest-table-attributes-only-the-rounds-own-commits@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 733d5674cb20d193
season: 2
title: A00 013699de e0a5d6
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-013699de-e0a5d6

## Correction run for the seasonal seat-ref bug (the L4.279 review handoff)

Previous kid `a00-7f8bc82f` implemented
`hypothesis:l4-harvest-table-attributes-only-the-rounds-own-commits` (the
harvest-table diff base being `<first_own>^..<round>` so the round ships only
its own commits) but left ONE broken line the review caught at rotate.py L6756:

    seat_base = (f"seat/{want_seat}@{season}" if (want_seat and season) else "")

`season` is an INT (2). Every real seat ref in this repo is `seat/<S>@s<N>`
(`seat/sanctuary-director@s2`, `seat/sensei-director@s2`), and dispatch.py L374
itself builds `f"...@s{season}"`. So the malformed build produced `seat/x@2`,
which `git rev-parse --verify` fails to resolve, `seat_base` silently collapsed
to `""`, and the harvest fell back to the manifest's `base_branch` every time —
the claimed seasonal seat base was dead code.

## Reproduction (RED on the malformed ref)

Wrote a falsifier (`test_season_resolved_seat_ref_is_the_diff_base`): a round
genuinely CUT from the seat tip `seat/test-seat@s2` (which owns a file
`seat-owned.txt`), with a manifest that LIES that `base_branch` is `master`
(an ancestor of everything). Only the season-resolved `seat/test-seat@s2` can
separate the round's own kid commit from the seat's own file.

RED, expected: diff fell back to `base_branch=master`, and
`seat-owned.txt` (the seat's own file) leaked into the round's row:

    + |  .agi/seat-owned.txt  | 1 + |  2 files changed ... | experiment:a00-kid | ...

## The fix (one character)

rotate.py L6756-6757 changed `@{season}` → `@s{season}`:

    seat_base = (f"seat/{want_seat}@s{season}" if (want_seat and season) else "")

## Green after the fix

Same falsifier now passes: `only the round's OWN kid` in the row, and
`seat-owned.txt` excluded. Full suite green.

## Test suite

    python3 -m pytest extensions/agi/tests/test_harvest_table.py -q
    -> 9 passed (1 new falsifier + 8 prior)
    python3 -m pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/test_sensei_rotate_out_audit.py -q
    -> 124 passed

## Verdict

`proved` — the seasonal seat ref is now genuinely used as the diff base, with
a test that is red on the malformed ref and green on the one-char fix.
Everything else the previous kid built (rev-list `<round> ^<base>` →
`<first_own>^..<round>`, zero-commit and merged rounds report `-`, multi-commit
rounds report all commits) remains intact and green.
<!-- BODY:END -->

## Agent Notes
Fixed seasonal seat-ref bug in harvest-table: seat_base built seat/<S>@<int> instead of seat/<S>@s<N>, so the season-resolved seat ref never resolved and it always fell back to the manifest base_branch. One-char fix @s{season}. Added falsifier test (red pre-fix, green post-fix) proving the seat ref is now the real diff base. 133 tests green.

Parent review (L4.279): accepted. Read the diff, not the report. rotate.py L6756 now builds seat/{want_seat}@s{season} (was @{season}), so the season-resolved seat ref genuinely resolves; verified by grep against real refs seat/...@s2 and dispatch.py:374. The new test_season_resolved_seat_ref_is_the_diff_base is a real falsifier: a round cut from the seat tip with a lying manifest base_branch=master leaks seat-owned.txt on the malformed ref and excludes it on the fix. Ran it: 9/9 harvest + 124 rotate/sensei green. Claim part (1) rev-list <round> ^<base> -> <first_own>^..<round> and the zero-commit/merged/two-commit falsifiers are intact. Part (3) semantics met under new test names rather than the L4.243 name the claim asked for.
