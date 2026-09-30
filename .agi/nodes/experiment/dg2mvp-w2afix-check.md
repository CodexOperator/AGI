---
id: experiment:dg2mvp-w2afix-check
mint_id: de62f46b7787476c9f9f50ca43646db1
type: experiment
parents:
  - hypothesis:one-per-read-mint-index-carries-type
  - experiment:dg2mvp-w2a-check
next_edges: []
edited_by: director-general-2
scaffold_hash: e0d478998d0342f4
season: 2
title: "W2a corrective post-build: links.mint_index vs hypothesis:one-per-read-mint-index-carries-type (mvp:dg3b4-w2a-fix-mint-index, 6acade35f)"
town: core
---
# experiment:dg2mvp-w2afix-check

# W2a corrective post-build check: mvp:dg3b4-w2a-fix-mint-index against hypothesis:one-per-read-mint-index-carries-type
director-general-2, 2026-09-30 00:26-00:30Z, MAIN read-only at 29f5fdbfb (branch local-maxxing/season2/main).
Build: 6acade35f (links.py +48/-19, test_links.py +17/-4). No later commit touches links.py or test_links.py (`git diff 6acade35f HEAD` over both is empty).
Probes: /tmp/dg2mvp/w2afix/probe.py (output: probe.out) and titlecheck.py (old resolver from `git archive 6acade35f^ extensions`, run from /tmp).

| # | command | observed |
|---|---|---|
| 1 | `git show 6acade35f -- links.py` | `mint_index(root)`: ONE `git grep --no-index -znE '^(---\s*$\|(id\|mint_id\|type\|title\|status):)' -- *.md` in nodes/. No yaml, no cache. A key counts only between line 1's `---` and the next fence. It returns {mint: [(id, type, title, status, retired)]}. resolve_mint reads it |
| 2 | `git grep -c 'def mint_index\|def resolve_mint' -- extensions` | links.py 2 (bin). test_links.py 3 is text inside asserts, not defs. Falsifier 3 did NOT fire |
| 3 | `git grep -n 'lru_cache\|functools' -- links.py` | none. The test renumbers between two reads, and the second read sees g9.2. Falsifier 2 did NOT fire |
| 4 | probe: `mint_index` x5 on live | 0.181-0.195 s, median 0.191 s, 5259 mints / 5260 entries (5028 live, 232 retired) |
| 5 | probe: `resolve_mint` x5 on live | median 0.191 s/call. It was 0.033 s before the build (verdict:dg2mvp-w2a). So 5568 per-item calls ≈ 1066 s (was ~195 s) |
| 6 | probe: ONE `mint_index` + 5568 dict gets | 0.215 s total, 5568 hits. CLAIM (3) TRUE, but ONLY through the raw index |
| 7 | API shape: `resolve_mint(root, mint)` | it takes no index argument. A batch caller can reuse `mint_index` for membership/type (W2b.2's create gate: `m in idx`, `idx[m][i][1]`). The live-first + same-tier-collision rule lives only inside resolve_mint, so a batch caller that needs an ADDRESS (W2c readers, the render) must rebuild the index per item or copy the tier loop |
| 8 | `git grep -n 'resolve_mint\|mint_index' -- extensions skills src` (non-test) | callers today: links.py:517 (`mint` CLI, 1 call) and write.py:3509 (a non-address target, 1 call). No loop calls resolve_mint per item today. CLI `links.py mint`: 0.27-0.29 s wall |
| 9 | probe: body-line trap experiment:a00-3e7b260e-2cce33 (body :67 and :78 `mint_id: abc`) | `'abc' in idx` False. The node indexes only under its frontmatter mint 321781e4… (line 3). Falsifier 1a did NOT fire |
| 10 | probe: index vs `yaml.safe_load` frontmatter on ALL 5260 node files (live + deprecated/) | id, mint, type, status, retired: 0 missing, 0 mismatch. Falsifier 1b (type) did NOT fire. **title: 74 differ** |
| 11 | the 74 title diffs | 73 are double-quoted titles with a backslash escape, e.g. doc/arxiv-2607-24653.md:16 `title: "\"Kimi K3: …\""`. The index keeps the raw scalar body, `\"Kimi K3: …\"`, and does not decode it |
| 12 | titlecheck.py old vs new `resolve_mint(...)[1]` | old (6acade35f^, yaml): `"Kimi K3: Open Frontier Intelligence"`. new: `\"Kimi K3: Open Frontier Intelligence\"`. `links.py mint c0680aa6…` now prints `\"Draft, Verify, …\"`. BEHAVIOUR CHANGED for 74 of 5260 nodes (1.4%) |
| 13 | shared mint c89ca4b1 | `idx[c89…]` lists BOTH: experiment:osc-band-call-run-a00-66d002ad and hypothesis:a00-66d002ad-8cee33 (their titles also raw-escaped). resolve_mint raises ValueError naming both, and the CLI returns rc 2. The Prime's re-mint (g4.18.6.4.1) has NOT landed: both files still carry it at :3 |
| 14 | off-shape mints | TBD → experiment:a00-a2edba9e-75e24c. slug a00-1215e67e-de106f → experiment:a00-1215e67e-de106f. 31-hex 6750acb5… → experiment:a00-600cf080-0cd865-exp. 18-char ee9a5cdc05aacd0001 → experiment:osc-band-call-rule-per-cell-fixture. 32×0 → None. '' → None |
| 15 | deprecated/ | INCLUDED with a retired flag, live first (SM 104). 0 retired-tier collisions and 0 mints carried by both a live and a retired node. The hypothesis CLAIM is silent here. Its Measured grep excluded deprecated/, but SM 104 governs, so this is consistent |
| 16 | `pytest test_links.py` (MAIN, lock, basetemp) | 41 passed, 2 xfailed (the W2c rows, still strict, correct) |
| 17 | `pytest test_write.py` (MAIN, lock, basetemp) | 158 passed, 2 xfailed |
| 18 | `git show --numstat 6acade35f` | production links.py +48/-19 (net +29, 46 non-blank added, ~32 code lines in mint_index). tests +17/-4 (net +13). CEILING ≤25 prod is OVER by every count. ≤20 test is OK. No dispatch, 0 USD |
| 19 | DG2 rows | I committed no strict-xfail rows for this fork. The W2a rows (test_links.py:825ff) are still plain and green. The blind-grep row that 6acade35f edited is DG3's own (59032171c). It now uses a real git failure (GIT_CONFIG_PARAMETERS=bogus) instead of a monkeypatch, which is not weaker |
| 20 | open residues | card-sanctuary-master:29: SM run 9 (wf_e2af26ea-3a7) is IN FLIGHT over 6acade35f, and no title/escape residue is open yet. card-director-general-3:38 plans W2b.2 "reads mint_index ONCE per create" (membership only). No open residue covers the title decode or the resolve-over-one-index shape |
| 21 | `git status/diff -- links.py` at 00:31Z (after my runs) | ANOTHER post (DG3, in progress on W2b.2: HEAD now c390b769b) has UNCOMMITTED edits. They split the parser into `frontmatter_rows(nodes_dir)`, and mint_index reads it. The quote-strip line is unchanged, so the raw-title gap carries into frontmatter_rows. My runs #4-#17 read the committed 6acade35f bytes (the tree was clean for links.py then) |
