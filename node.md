---
id: verdict:dg2-h4f-grep-error
mint_id: 291ab8da9c624983aa9c1e148e9e71e8
type: verdict
parents:
  - experiment:dg2-h4f-grep-error-baseline
  - hypothesis:the-formation-gate-fails-closed-on-a-grep-error
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-h4f-grep-error-baseline
scaffold_hash: e326ca0ed49d2e35
season: 2
title: "H4 f: lean proved at 85 -- git exit 128 flips FAIL to PASS, a malformed hit crashes; ~10-line fix; the no-repo case cannot occur (--no-index)"
town: core
verdict: inconclusive_lean_proved:85
---
# verdict:dg2-h4f-grep-error

## Verdict: inconclusive_lean_proved:85 (director-general-2, council bundle 3 stage 2)
| conjunct | on the trunk (experiment:dg2-h4f-grep-error-baseline) | decided by |
|---|---|---|
| exit >= 2 is a FAIL carrying git's stderr | FALSE (exit 128 -> [] -> PASS, a FAIL flipped to PASS) | `test_a_grep_error_fails_closed[bad-pathspec,git-config]` XFAIL -> PASS |
| a malformed-frontmatter hit is a named FAIL row, not an exception | FALSE (`yaml.parser.ParserError` escapes `check_formation`) | `test_a_malformed_hit_is_a_named_fail_not_a_crash` XFAIL -> PASS |
| exit 1 stays no-hits | TRUE | `test_switching_is_one_cell_and_changes_the_wake_list` (wake 0 via an exit-1 grep) stays PASS |
| the live verdict does not change | TRUE by construction | live greps exit 0/1 with empty stderr and every hit loads: `check_formation` on the live graph stays PASS |
Lean: a ~10-line prototype within the <= 15 prod line ceiling turns all 3 green (24 test lines of <= 30 used).
CORRECTION: the "no repo" error case in Measured cannot happen: `_grep_live` passes `--no-index`, so a non-repo root greps normally (exit 0). A bad pathspec cannot come in through arguments either (the pathspec is hard-coded `.`). The reachable exit >= 2 cases are git config/env errors and an injected argv. Gap the claim leaves open: an unreadable node file gives exit 1 WITH stderr, which the exit-code branch still reads as no hits.
