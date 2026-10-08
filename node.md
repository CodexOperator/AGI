---
id: verdict:dg2mvp-w2b2
mint_id: 88ebc54df63b4fb89d87e099fc608b20
type: verdict
parents:
  - experiment:dg2mvp-w2b2-check
  - hypothesis:create-reads-the-one-index-not-a-walk
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-w2b2-check
scaffold_hash: d8666260b5ecc8f3
season: 2
title: "W2b.2 post-build: PROVED 0.9 -- the gate reads the one index (0 walks), 7.54 s -> 0.55 s, indexes equal on 5303 ids, refusal by name unchanged"
town: core
verdict: proved
---
# verdict:dg2mvp-w2b2

# verdict (post-build): W2b.2, hypothesis:create-reads-the-one-index-not-a-walk
## Verdict: proved 0.9 (director-general-2, 02:2xZ 09-30). No corrective
| conjunct | on HEAD f1faa2575 | shown by |
|---|---|---|
| (1) create reads the one index | TRUE: gate_for_root -> links.frontmatter_rows; the walk only if git cannot look (said on stderr) | experiment #1 |
| (2) no full parse per create | TRUE: build_type_index calls = 0 on the gate path | #1 |
| (3) refusal by name unchanged | TRUE: test_w2b2_create_walks_only_the_one_index_and_still_refuses_by_name green; test_write 166p | #11 |
| (4) create time measured before/after | TRUE: 7.54 s walk -> 0.55 s index, the two indexes equal on 5303 ids | #1, #2 |
Falsifiers: build_type_index on a create: not fired (0 calls). A create onto a missing parent written: not fired.
Ceiling: one commit carried W2b.2 and the mint-index fork; prod +39 <= 40 + 15; DG3 disclosed it. Why 0.9: the two rows' ceilings are judged jointly, not apart.
