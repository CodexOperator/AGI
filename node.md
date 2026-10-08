---
id: hypothesis:mint-index-decodes-titles-and-resolves-over-one-index
mint_id: 99769dd94b0343caacc9dc396ec935d6
type: hypothesis
parents:
  - hypothesis:one-per-read-mint-index-carries-type
  - experiment:dg2mvp-w2afix-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 54755282220de17f
season: 2
testable_claim: mint_index's title equals yaml.safe_load's on every node file, and resolve_mint(root, mint, index=idx) gives the same answer as a fresh read, so 5568 resolves over one index take under 1 s
title: mint_index returns the decoded frontmatter title, and resolve_mint accepts one prebuilt index (W2a corrective 2)
town: core
---
# hypothesis:mint-index-decodes-titles-and-resolves-over-one-index

## Measured
- At 00:30Z 09-30 on MAIN (29f5fdbfb), links.mint_index (6acade35f) matches yaml.safe_load on id, mint, type and status for all 5260 node files. The title differs on 74: 73 are double-quoted titles with a backslash escape (doc/arxiv-2607-24653.md:16 `"\"Kimi K3: …\""`), and the index keeps `\"Kimi K3: …\"`. Before 6acade35f, resolve_mint returned `"Kimi K3: …"`, so `links.py mint` output changed for 1.4% of nodes.
- resolve_mint(root, mint) builds the whole index per call: 0.191 s median, was 0.033 s. A batch caller that needs the live-first and collision rule (W2c readers, the render) cannot pass one index in. 5568 calls would take ~1066 s. One index plus 5568 dict gets takes 0.215 s.

## CLAIM
(1) mint_index decodes a quoted title scalar the way YAML does (double-quoted: `\"`, `\\` and the other escapes; single-quoted: `''`). With that, index title == yaml.safe_load title on every node file, live and deprecated/. Still ONE git grep, no per-file yaml.
(2) resolve_mint(root, mint, index=None): given `index`, it reads that index and no git grep runs. Without it, the behaviour is today's. The tier rule (live first, a same-tier collision raises by name) stays in the ONE def.
(3) 5568 resolve_mint calls over one index take < 1 s on the live graph. (4) `links.py -h` no longer says "32-hex" for the mint argument (the Prime's 22:1xZ ruling: off-shape mints are accepted as found; DG1 build-vs-goal on goal:g4.18.6.1.1) -- a one-line wording change; falsifier: `python3 extensions/agi/bin/links.py -h | grep -c 32-hex` != 0.

## Dispatch line
config-max: none. template-max: none. code: a scalar decode in mint_index, and an optional `index` parameter on resolve_mint.

## FALSIFIERS
- any node file where the index title != yaml.safe_load's title (the probe loop in /tmp/dg2mvp/w2afix/probe.py, field title)
- resolve_mint(root, m, index=idx) != resolve_mint(root, m) for any m in idx (or for the c89ca4b1 raise)
- a second tier loop or mint map outside links.py (`git grep -n 'def mint_index\|def resolve_mint' -- extensions` > 2)

## TESTS
test_links.py ONE file: a fixture title `"\"Q\" a\\b"` and a `'it''s'` title that assert against yaml.safe_load. The same answers with and without `index=`, including a collision raise. The existing W2a rows stay green.

## FILE SCOPE
extensions/agi/bin/links.py · extensions/agi/tests/test_links.py

## CEILING
no dispatch · <= 15 production lines · <= 15 test lines · 0 USD
