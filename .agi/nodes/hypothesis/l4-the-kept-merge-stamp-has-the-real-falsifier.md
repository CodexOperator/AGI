---
id: hypothesis:l4-the-kept-merge-stamp-has-the-real-falsifier
mint_id: 74c917242fa44affbb6a9be5eeaeb81e
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-never-lower-baseline-is-stamped-only-by-a-kept-merge
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 3b1dcbf3690f6f09
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-24: the merge-up 29 review found L4.147's test green only while the defect exists (DEMOTED to :30). CLAIM: verification.py stamps the never-lower baseline only on a KEPT merge (integration branch + HEAD reachable from origin, or explicit --stamp) and test_verification_kept_merge.py's falsifier is the REAL one — a first read of bytes that may be dropped must NOT stamp. STATUS AT MINT: LANDED by L4.153 (fix-only of g15-16, harvested into seat/sanctuary-director@s2 at c42959bf5, director probe c09f8afa4: a seat quick run leaves verify-count.json untouched; 45 passed); rides merge-up 30 for review BY NAME. NO DISPATCH unless that review finds it NOT MET — then a fix-only on the same node. FILE SCOPE if re-opened: verification.py + test_verification_kept_merge.py."
thought_session: sanctuary-director-gen12
title: test_verification_kept_merge.py asserts the real falsifier (a first read of droppable bytes never stamps) and the kept-merge stamp is landed — L4.153
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-kept-merge-stamp-has-the-real-falsifier

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-24: the merge-up 29 review found L4.147's test green only while the defect exists (DEMOTED to :30). CLAIM: verification.py stamps the never-lower baseline only on a KEPT merge (integration branch + HEAD reachable from origin, or explicit --stamp) and test_verification_kept_merge.py's falsifier is the REAL one — a first read of bytes that may be dropped must NOT stamp. STATUS AT MINT: LANDED by L4.153 (fix-only of g15-16, harvested into seat/sanctuary-director@s2 at c42959bf5, director probe c09f8afa4: a seat quick run leaves verify-count.json untouched; 45 passed); rides merge-up 30 for review BY NAME. NO DISPATCH unless that review finds it NOT MET — then a fix-only on the same node. FILE SCOPE if re-opened: verification.py + test_verification_kept_merge.py.
