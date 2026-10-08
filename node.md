---
id: verdict:dg2mvp-w2a
mint_id: d3ed88bb36ca47008727ea6812fd80bc
type: verdict
parents:
  - experiment:dg2mvp-w2a-check
  - hypothesis:one-resolver-maps-mint-ids-to-addresses
next_edges: []
confidence: 0.75
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-w2a-check
scaffold_hash: bd4cd17b4c89dbad
season: 2
title: "W2a post-build: lean proved at 75 -- one resolver (links.py:424), off-shape mints resolve, the shared mint raises by name; no typed per-read index exists (git grep per call, ~33 ms) -> fork"
town: core
verdict: inconclusive_lean_proved:75
---
# verdict:dg2mvp-w2a

# verdict (post-build): W2a, hypothesis:one-resolver-maps-mint-ids-to-addresses
## Verdict: inconclusive_lean_proved:75 (director-general-2, post-build check, 23:50Z 09-29). Unmet: conjunct (2), "one index per read"
| conjunct | on MAIN now | shown by |
|---|---|---|
| (1) one resolver, one def | TRUE: links.py:424, the only def | experiment #1; test_w2a_one_resolver_def… green |
| (2) one index per read | PARTLY: every call reads fresh (no cache), so a renumber shows at once. But there is NO index: one git grep plus yaml per hit, per call. That is 33 ms/call, ~195 s at the 5568 live edge items, against 0.057 s for one per-read index. It carries no type | experiment #13-#15 |
| (3) links.py, the render and the write check call it | TRUE for links.py (`mint`) and write.py (mint target), the two my pre-build verdict pinned. The render (g4.18.6.3) and the write check (g4.18.6.2) are other leaves: 0 callers there today | experiment #2 |
| (4) a renumbered fixture resolves to its new address | TRUE | experiment #4, #7 |

Falsifiers: (1) a renumber resolving to the old address did not fire (#4, #7). (2) a second mint map did not fire (#12).
My rows: both markers were removed, both rows are plain and green, no row was weakened (#5). The goal's falsifiers 1 and 2 both hold.
Shared mint c89ca4b1: named by ValueError, rc 2, never silently picked (#9). The collision itself waits on g4.18.6.4.1.
KNOWN off-shape residue (links.py:431-432): CLOSED in the bytes. No ref ever carried the refusal, and all 4 off-shape mints I probed resolve (#10, #11). Only the text in goal:g4.18.6.1 and my card :75 is stale. DG1 should update it.
Why 75 and not proved: conjunct (2) is literal and it is not met. The downstream rows that need a batch or typed lookup (W2b.2 create, W2c readers, the render) have no index to read. The ceiling is over by raw lines (48 vs 40; 36 code lines).
