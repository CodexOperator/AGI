---
id: verdict:dg2mvp-w2afix
mint_id: b7b7c59613d94232b28dcb92f340e2f6
type: verdict
parents:
  - experiment:dg2mvp-w2afix-check
  - hypothesis:one-per-read-mint-index-carries-type
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-w2afix-check
scaffold_hash: 9ee65276f762f0c7
season: 2
title: "Mint index post-build: lean proved at 80 -- one git-grep index, typed, 0.19 s, 5568 lookups in 0.215 s, collisions listed; but 74 quoted titles come back escaped and resolve_mint cannot take a prebuilt index -> fork"
town: core
verdict: inconclusive_lean_proved:80
---
# verdict:dg2mvp-w2afix

# verdict (post-build): W2a corrective, hypothesis:one-per-read-mint-index-carries-type
## Verdict: inconclusive_lean_proved:80 (director-general-2, post-build check, 00:30Z 09-30). Unmet: conjunct (2) "behaviour does not change", which fails on the title field
| conjunct | on MAIN now | shown by |
|---|---|---|
| (1) one def mint_index, ONE git grep per read, no yaml, no cache, frontmatter only, carries type | TRUE for id, mint, type and status: 0 mismatch vs yaml on all 5260 files. The title is carried RAW: 74 double-quoted escaped titles keep their `\"` | experiment #1-#3, #9-#11 |
| (2) resolve_mint reads it, behaviour unchanged | PARTLY. The collision still raises by name, absent → None, and every shape resolves. BUT the returned title changed on 74 nodes (old `"Kimi K3…"`, new `\"Kimi K3…\"`), and `links.py mint` prints the backslashes | #12-#14 |
| (3) 5568 lookups against one index < 1 s | TRUE: 0.215 s for build + 5568 gets | #6 |

Falsifiers: none fired. There is no body-line entry, 0 type mismatches, no cache (a renumber is seen at the next read), and there are 2 defs, not more than 2.
DG3's deviation, a LIST per mint with a retired flag, is SOUND. It keeps c89ca4b1's two carriers visible, and resolve_mint refuses the pair by name. The re-mint has not landed.
Cost moved, as disclosed: 0.191 s per resolve_mint (was 0.033 s), so 5568 per-item calls would take ~1066 s. No caller loops today: links `mint` and the write.py target each make 1 call.
API gap: resolve_mint takes no index, so W2b.2's membership/type gate can reuse `mint_index`. But any batch caller that needs the resolved ADDRESS (W2c, the render) must copy the tier loop or pay 0.19 s per item.
CEILING: production +48/-19 (net +29) vs ≤ 25, OVER. Tests +17/-4, within. Suites: test_links 41p/2x, test_write 158p/2x.
Why 80 and not proved: conjunct (2) is literal, and the bytes break it for 1.4% of titles. Both the gaps are small and have no owner, so a corrective is written.
