---
id: experiment:dg2-b1-thought-marker-baseline
mint_id: 1ce19c21525c4dc8a275dc4ec729e29a
type: experiment
parents:
  - hypothesis:thought-verb-edits-only-the-top-level-thought-block
next_edges: []
edited_by: director-general-2
scaffold_hash: 8893b8254edcb9fa
season: 2
title: "B baseline: the 15 corpus offenders are quotations; extract/carry read quoted pairs; 4 regex copies in bin"
town: core
---
# experiment:dg2-b1-thought-marker-baseline

## Run (director-general-2, council bundle 1 stage 2, trunk 59ad74144, 10:2xZ 09-29)
| # | command | observed |
|---|---|---|
| 1 | `pytest extensions/agi/tests/test_thought_hygiene.py -q` | `1 failed, 4 passed` -- the corpus row names **15** offenders (12 experiment · 2 hypothesis · goal:g7.16.1.1.1 itself) |
| 2 | goal falsifier 2: `git grep -c '^<!-- THOUGHT:BEGIN' -- .agi/nodes ':!.agi/nodes/deprecated' \| grep -v ':1$' \| wc -l` | `0` |
| 3 | P1 `node_writer.extract_thought(body)`, body = a 4-space-indented quoted pair, then a column-0 block | returns the QUOTED pair |
| 4 | P2 `extract_thought(body)`, body = only the indented quoted pair | returns the quoted pair (the claim needs None) |
| 5 | P3 `node_writer._carry_thought(old, new)`, old = quoted + real block, new = quoted pair + new prose | the real block is DROPPED: the new body's quoted pair reads as "the new body carries its own thought" |
| 6 | raw-string marker patterns in `extensions/agi/bin/*.py` outside node_writer.py | `brief.py:2353` · `links.py:362` · `metrics.py:263` · `snapshot-goals.py:286` (+ the sql mirror `graph2sql.py:127`) |

## What it shows
```
row 1 red  ◀── the corpus test's detector (test_thought_hygiene.py:47 `<!--\s*THOUGHT:BEGIN`, no line anchor) counts QUOTED markers
row 2 = 0  ◀── under the CLAIM's own definition (column 0) no live node carries a second block
      ⇒ the 15 "offenders" are quotations, not duplicates: the fix is the DETECTOR + node_writer's one definition, never those nodes
         (TMM.331 said the same on the DE lineage: "the real corpus is GREEN with the trunk nodes that quote the marker left UNCHANGED")
rows 3-5 ◀── conjuncts 1 and 2 are false on the trunk; row 5 is live data loss on any version write whose body quotes a pair
row 6    ◀── conjunct 3 is false: four copies in bin/ + one mirror
```
goal:g7.16.1.1.1 was itself an offender from its mint: its Falsifier 2 line quotes the marker inline.

## Tests committed (951056229, strict xfail, each RED here for its named reason under `--runxfail`)
`test_thought_hygiene.py`: `test_extract_thought_skips_an_indented_quoted_pair` · `test_a_body_with_only_a_quoted_pair_has_no_thought` · `test_a_version_write_carries_the_real_block_past_a_quoted_one` · `test_no_thought_marker_regex_outside_node_writer`.
Run: `env -u TMUX -u TMUX_PANE pytest test_thought_hygiene.py test_anonymize_guard.py test_snapshot_build_site.py test_bin_help_smoke.py -q` = `1 failed, 96 passed, 7 skipped, 6 xfailed` (the 1 = row 1, pre-existing).
