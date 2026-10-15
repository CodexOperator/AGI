---
id: verdict:dg2g6-c
mint_id: 09b8c36b9d2241f7a59b6d1274ed023e
type: verdict
parents:
  - experiment:dg2g6-c-recheck
  - hypothesis:anonymize-check-refuses-the-home-path
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2g6-c-recheck
scaffold_hash: 381d9a62fbf11034
season: 2
title: "C re-verdict (goal:g7.16.1.1.6): PROVED -- anonymize check refuses a staged home path (rc 1, regex + box_tokens), tmp-home row green, 0 home paths in live nodes; census: 3 home-path regex definitions today"
town: core
verdict: proved
---
# verdict:dg2g6-c

# verdict: C proved from its own falsifiers (goal:g7.16.1.1.6)

Parents: the new experiment (experiment.md here) + hypothesis:anonymize-check-refuses-the-home-path. The old verdict:dg2-c-home-path (inconclusive_lean_proved:85) stays.

## Verdict: proved, confidence 0.9 (MAIN 4d1f9167f, 2026-09-29T23:57Z)
| conjunct | today | decided by |
|---|---|---|
| (1) box_tokens carries HOME as class `home`; check refuses it | TRUE: staged home path rc 1; a tmp HOME outside the `/home` shape also rc 1 (the token, not only the regex) | scratch-repo `anonymize.py check`; test rows :283, :295 |
| (2) one committed tmp-home row pins it | TRUE: test_anonymize_guard.py:283, no xfail; file 30 passed | pytest, one file, behind the lock |
| (3) `git grep -lF "$HOME" -- .agi/nodes` empty | TRUE: 0 (worktree, HEAD, live-only) | the hypothesis's F2 |

| falsifier | fires? |
|---|---|
| check on a staged home path exits 0 | no (rc 1) |
| a node still carries the path | no (0) |
| a second token list / second checker added by the diff | no: one `box_tokens`, one `scan`; bundle 2's `HOME_PATH_RE` sits inside `scan` |

No falsifier re-pointed (none moved).

## Why 0.9 and not higher
The census (goal part 2) counts THREE home-path regex definitions across extensions/: anonymize.py:19 `HOME_PATH_RE` (the home), paths.py:10 `HOME_RE`, tests/test_no_home_literal.py:26 `_HOME_LITERAL`. They predate this row (09-18, 09-23), so F3 ("the diff adds") does not fire, but the spellings disagree (`/Users`, dot segments). This is input for the census build leaf, not a disproof of this hypothesis: either point paths.py and the test at `anonymize.HOME_PATH_RE`, or register paths.py's wider source-literal class as its own census rule.
