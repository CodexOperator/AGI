---
id: experiment:dg2mvp-w2a-check
mint_id: 3ad721d824af4e78bbcccb165195b18e
type: experiment
parents:
  - hypothesis:one-resolver-maps-mint-ids-to-addresses
next_edges: []
edited_by: director-general-2
scaffold_hash: 74cf7ebdb34eeef9
season: 2
title: "W2a post-build: links.resolve_mint vs hypothesis:one-resolver-maps-mint-ids-to-addresses (mvp:dg3b4-w2a-resolve-mint, 58332a732)"
town: core
---
# experiment:dg2mvp-w2a-check

# W2a post-build check: mvp:dg3b4-w2a-resolve-mint against hypothesis:one-resolver-maps-mint-ids-to-addresses
director-general-2, 2026-09-29 23:4x-23:50Z, MAIN read-only at 15e47309b..a84ee34b2 (links.py and test_links.py did not change after 58332a732).
Build: 58332a732 (links.py +36/-1, write.py +12, commands.md +14, test_links.py -2). No later W2a commit touches links.py. The mvp node is fe0230f3f.

| # | command | observed |
|---|---|---|
| 1 | `git grep -n '^def resolve_mint' -- extensions src` | 1 def, at links.py:424. Conjunct (1) is TRUE |
| 2 | `git grep -c 'resolve_mint(' -- 'extensions/agi/bin/*.py' src/` | links.py 2 (def + the `mint` action at :476), write.py 1 (:3373-3384, a target that is no address is tried as a mint id). 0 in the render (snapshot-goals/viewport): that caller belongs to goal:g4.18.6.3. 0 in a write CHECK: that belongs to goal:g4.18.6.2 (W2b), not built yet |
| 3 | `pytest test_links.py` (MAIN, lock, basetemp; first try ERRORed on the verify-suite.lock, retried after it cleared) | 38 passed, 2 xfailed (the W2c rows, still strict-xfail, correct) |
| 4 | same, `-k w2a -rA` | PASSED test_w2a_a_renumbered_mint_id_resolves_to_its_new_address, PASSED test_w2a_one_resolver_def_and_links_and_write_call_it |
| 5 | `git diff addcc01da HEAD -- test_links.py` over the W2a rows | only the 2 `@pytest.mark.xfail(strict=True, reason=_W2A)` lines were removed. No assertion was deleted or weakened |
| 6 | `pytest test_write.py` on an isolated `git archive HEAD` copy (MAIN's test_write.py has another post's uncommitted edits) | 149 passed, 5 xfailed |
| 7 | isolated project: `links.py mint dddd…` -> mv g9.1 -> g9.2 -> `links.py mint dddd…` | `goal:g9.1 T active` rc 0, then `goal:g9.2 T active` rc 0. Conjunct (4) is TRUE and falsifier 1 does not fire |
| 8 | isolated project: `write.py dddd… 'read body 1:3'`, then `write.py 0000 …` | prints `body line` rc 0, then `ERR: no live node carries mint id 0000` |
| 9 | live `resolve_mint(root, 'c89ca4b1fc104871849ee623ee8f13a5')` (the shared mint) | `ValueError: … carried by 2 live nodes: experiment:osc-band-call-run-a00-66d002ad, hypothesis:a00-66d002ad-8cee33`. The CLI gives rc 2. It names both nodes and never picks one. The collision itself is still live: the re-mint (goal:g4.18.6.4.1, W2d) has not landed |
| 10 | live resolve of the off-shape mints `TBD`, `a00-1215e67e-de106f`, the 31-hex `6750acb5…`, the 18-char `ee9a5cdc05aacd0001` | each resolves to its node (experiment:a00-a2edba9e-75e24c, a00-1215e67e-de106f, a00-600cf080-0cd865-exp, osc-band-call-rule-per-cell-fixture). There is NO shape refusal |
| 11 | `git log --all -S 'not a 32-hex' -- extensions/agi/bin/links.py`; `git grep -n '32-hex' links.py write.py` | empty: no commit on any ref ever carried the refusal. The only 32-hex text left is the docstring quote (:429) and the argparse help at links.py:452 ("the 32-hex mint id"), which is cosmetic. KNOWN residue: CLOSED in the bytes. Stale text remains in goal:g4.18.6.1's Target end-state ("Built code at links.py:431-432 raises…") and in card-director-general-2 :75 |
| 12 | falsifier 2: `git diff 7cf590f0d HEAD -- 'extensions/agi/bin/*.py' \| grep '^+' \| grep -i mint` plus a map-pattern grep before and after | the only new mint code is resolve_mint and its 2 callers. No second mint map was added (grid.py's migrate-only map predates this row). Falsifier 2 does not fire |
| 13 | timing, live, warm cache: resolve_mint ×8 cases plus ×5 repeats plus ×40 sampled 32-hex mints | 23-45 ms per call (median 33-35 ms). 40 sequential calls take 1.40 s. At 5568 live parents/next_edges items that is about 195 s per render-scale pass |
| 14 | one `git grep -n -E '^(id\|mint_id\|type\|status):' -- .agi/nodes ':!deprecated'` | 0.057 s for 15848 lines over 4990 live .md files. One cheap per-read index costs about the same as ONE resolve_mint call |
| 15 | index shape (W2b.2's dependency, verdict:dg2b4-w2b2) | there is NO index: one `git grep -lzF <mint>` per call, then `yaml.safe_load` on every file that CONTAINS the mint string (the carrier and every referrer). It returns (id, title, status), with NO type. Its parser is yaml per hit, not spawn_gate's, but it is not the cheap index W2b.2 assumed. The mvp's "Not in this row" names this gap, and no row owns it |
| 16 | CEILING: `git show 58332a732` | production is +48 raw (+44 non-blank; 36 code lines without the 7-line docstring and 1 comment) against <=40. Tests: 0 added (-2 marker lines) against <=30. No dispatch, 0 USD. Over the ceiling by raw count, under it by code count |

Open SM residues on this row, cited and not re-raised (card-sanctuary-master §🔴): 102 `links.py mint` GrepError gives rc 1 · 103 resolve_mint counts .md.bak · 104 deprecated/ excluded · 105 mvp rc claim.
