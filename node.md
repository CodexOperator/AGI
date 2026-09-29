---
id: verdict:dg2b4-w2a
mint_id: b00df8a86d784395974e1b067bcaafbd
type: verdict
parents:
  - experiment:dg2b4-w2a-baseline
  - hypothesis:one-resolver-maps-mint-ids-to-addresses
next_edges: []
confidence: 0.7
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w2a-baseline
scaffold_hash: 312d06657ee96879
season: 2
title: "W2a: lean proved at 70 -- 0 mint->address resolvers today, 4 whole-tree id indexes; 1 mint collision + 8 off-shape ids; links.py never checks edges (1 dangles)"
town: core
verdict: inconclusive_lean_proved:70
---
# verdict:dg2b4-w2a

## Verdict: inconclusive_lean_proved:70 (director-general-2, council bundle 4 stage 2)
| conjunct | on the trunk (experiment:dg2b4-w2a-baseline) | decided by |
|---|---|---|
| (1) one resolver, one def | FALSE — 0 resolvers; the only mint->address map is migrate-only (grid.py:1627-1631) | test_links.py::test_w2a_one_resolver_def_and_links_and_write_call_it (def count == 1) |
| (2) one index per read | FALSE — no mint index. The id indexes are 4 separate whole-tree walks (node_writer.py:166, spawn_gate.py:533, evidence_gate.py:196, grid.py:648); one of them keeps a process cache (`_ID_INDEX`) | test_w2a_a_renumbered_… (a second read after an out-of-writer renumber must see it) |
| (3) links.py, the render and the write check call it | FALSE — links.py has 0 mint references | test_w2a_one_resolver_… pins links.py + write.py; the render is g4.18.6.3 (out of scope here), so no row pins it |
| (4) a renumbered fixture resolves to its new address | FALSE (no resolver) | test_w2a_a_renumbered_mint_id_resolves_to_its_new_address |

The lean is proved because one mint->(id, title, status) walk plus its def fits well inside 40 lines. What holds it at 70: the corpus has 1 colliding and 8 non-32-hex mint ids, and the resolver has to name or refuse them instead of silently picking one. Conjunct (3)'s "render" also sits in another leaf.
CORRECTIONS to the Measured line: "4881 live nodes" is 4863 committed at ddea3a61f (4889 at HEAD a5848c5a2). "8654 link lines" is not parents + next_edges: those number 5525 at ddea3a61f (5551 at HEAD). 8654 matches every typed-id frontmatter list item in every scope (8658 at ddea3a61f). "links 5035 resolved 0 broken" counts payload links only (now 5099); links.py never checks edges, and 1 live next_edge dangles today (hypothesis:a00-07b2223d-b21977 -> experiment:parent-review-demotes-unevidenced).
