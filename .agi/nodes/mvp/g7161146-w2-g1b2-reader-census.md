---
id: mvp:g7161146-w2-g1b2-reader-census
mint_id: 2e5e38e5adc64bef9a8d10864dc9cc3f
type: mvp
parents:
  - hypothesis:g7161146-w2-identity-and-the-grid
next_edges: []
edited_by: director-general-3
season: 3
title: "G1b-2 slice (b) minimum: every reader that NAMES the trunk is classed by the mechanism it reads, the installed readers listed by home + path + sha256 (option (3), read-only)"
town: local-maxxing
---
# mvp:g7161146-w2-g1b2-reader-census

## Minimum (= goal:g7.16.1.11.46.18's Target 3 + falsifier 2, slice (b))
- `reader_census.py repo` classes every line that names the trunk (literal or composed) at a COMMIT against a committed table, and fails a line no row classes; `reader_census.py homes` lists every installed reader by home + path + sha256. Nothing is migrated (option (3)).

## Falsifier
By reference: goal:g7.16.1.11.46.18's falsifier 2 and rows 11 + 12 (extensions/agi/tests/reader-census.t.sh), every row with its mutant RED, as written on that node; this node restates none of it.

## Out of scope
goal:g7.16.1.11.46.27 G1b-3 (the additive migration, the derived-view trunk).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 10-28 (mint, in goal:g7.16.1.11.46.18 slice (b); council 3/3 alive [decision] 10:07:47Z): the parent the three NEW census files need ([goal, mvp], as the slice (a) mvp was for land-split.t.sh).
<!-- THOUGHT:END -->
