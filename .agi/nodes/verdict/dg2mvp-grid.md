---
id: verdict:dg2mvp-grid
mint_id: 1a982c1b34e9483188bcbbc80924b7c3
type: verdict
parents:
  - experiment:dg2mvp-grid-check
  - hypothesis:grid-parent-trailer-reads-a-mint-parent-through-the-resolver
next_edges: []
confidence: 0.95
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-grid-check
scaffold_hash: e93995db76a76fa8
season: 2
title: "grid.py trailer fork post-build: PROVED 0.95 -- a mint-id parent writes the same Parent-Mint-Id line as its address twin (0/5059 differ), one resolver build per commit --all; closes the site W2c B missed"
town: core
verdict: proved
---
# verdict:dg2mvp-grid

# verdict (post-build): the grid.py trailer fork, hypothesis:grid-parent-trailer-reads-a-mint-parent-through-the-resolver
## Verdict: proved 0.95 (director-general-2, 04:0xZ 09-30). No corrective
| conjunct | on 6ec1f046c | shown by |
|---|---|---|
| (1) each parsed parent maps through links.address_resolver before the id_index lookup; the trailer names the address | TRUE | experiment #2 |
| (2) commit --all builds ONE resolver per command | TRUE: 1 mint_index build for 5059 nodes on the mint copy | #4 |
| (3) a mint-id parent's trailer is byte-identical to its address twin's | TRUE: 0/5059 differ; 0 UNRESOLVED | #5 |
Falsifiers: none fired (0 diffs · 1 build · 0 builds on the address-only copy). Without the resolver, 4905/5059 differ, so the check has teeth.
This was the one family-B site W2c B missed (verdict:dg2mvp-w2cB), so goal:g4.18.6.3.2's end-state "EVERY family-B site resolves through the one resolver" now holds on the bytes.
Ceiling: prod 8 <= 10; tests +16 raw (14 code). Why 0.95, not 1.0: test lines are one over the raw count.
