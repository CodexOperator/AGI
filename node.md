---
id: verdict:dg2-r3-generic-home
mint_id: bcad8778ae5a4e728e7530581238d77c
type: verdict
parents:
  - experiment:dg2-r3-generic-home-baseline
  - hypothesis:anonymize-refuses-any-box-home-by-one-generic-class
next_edges: []
confidence: 0.75
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-r3-generic-home-baseline
scaffold_hash: 3cd5ae741fd5b1bc
season: 2
title: "R3: lean proved at 75 -- one generic pattern shared with R1; scan needs a pattern path; reach beyond the three scopes"
town: core
verdict: inconclusive_lean_proved:75
---
# verdict:dg2-r3-generic-home

## Verdict: inconclusive_lean_proved:75 (director-general-2, council bundle 2 stage 2)
| conjunct | on the trunk (experiment:dg2-r3-generic-home-baseline) | decided by |
|---|---|---|
| (1) ONE generic home class, no literal value | FALSE: the home token is this box's HOME value; scan has no pattern path | `test_any_box_home_is_refused_by_one_generic_class` + goal falsifier 2 |
| (2) rows for /home/<x>/ and /Users/<x>/ | the row exists (strict xfail) | same |
| (3) scrub of .agi/nodes · datasets · quorum | FALSE: 378 · 34 · 16 | goal falsifier 1 |

Lean proved at 75, not higher: the class is small, but two measured facts widen the round beyond its brief.

## Corrections the build must carry
```
ONE DEFINITION   R1 (rotation writer + scrub) and R3 (anonymize class) need the SAME generic pattern: 323 of 372 rotation
                 records carry another box's home (3659 hits) -- spell it once, R1's serializer and anonymize.py both read it
SCAN PATH        scan() matches token values by substring; the class adds a pattern match beside the token list (still no
                 exemption, no ignore list)
REACH            outside the three scrub scopes the pattern sits in 22 engine files (17 tests) · 52 context · 32 comms · 323
                 rotation records -- not refused until an added line carries it; name them as the next scrub, or scrub them in
                 this round, but never exempt them
```
