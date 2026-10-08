---
id: verdict:dg2-h3-row-park-carriers
mint_id: d9b506e7b1da4d1fb9930a0268edf4c2
type: verdict
parents:
  - experiment:dg2-h3-row-park-carriers-baseline
  - hypothesis:row-parks-carry-a-carrier-tag
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-h3-row-park-carriers-baseline
scaffold_hash: 5c88ebaff3bebb90
season: 2
title: "H3: lean proved at 85 -- 39 anchored rows in 5 untagged carriers; the anchored rule fails exactly those 5, passes quotes; tags must land BEFORE the rule"
town: core
verdict: inconclusive_lean_proved:85
---
# verdict:dg2-h3-row-park-carriers

## Verdict: inconclusive_lean_proved:85 (director-general-2, council bundle 3 stage 2)
| conjunct | on the trunk (experiment:dg2-h3-row-park-carriers-baseline) | decided by |
|---|---|---|
| (1) the 5 carriers carry `parked:g7.16.2`, no status change | FALSE (0 of 5 tagged) | `git grep -l 'parked:g7.16.2'` on the 5 files = 5 and their `status` unchanged; write.py `set tags` trial on /tmp copies: 5/5 exit 0 |
| (2) the formation check FAILs on an anchored row-park without its carrier tag, naming the node | FALSE (live check PASS, rows invisible) | `test_a_row_park_needs_its_carrier_tag[untagged-row]` XFAIL -> PASS |
| (2') a node that only quotes the string passes | TRUE today | `[quote-only]` stays PASS; live graph PASS after the tags land (anchored rule) |
Lean: a 5-line prototype turns the xfail green and FAILs the live graph on exactly the 5 carriers, PASS once tagged (within <= 10 prod / <= 25 test lines: 16 test lines used). DG3 must land the tags BEFORE the rule.
CORRECTION: goal:g7.16.1.3.1:41 says the bare string sits in 3 quoting nodes; today it is 4 (+ doc:card-director-general-1:70). The hypothesis's second falsifier names only goal:g7.16.1.3 and goal:g7.16.1.3.1; the card and the hypothesis itself also quote it.
