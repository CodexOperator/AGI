---
id: hypothesis:node-type-schemas-name-a-thought-reader-that-exists
mint_id: 92a0c5efe8cd41738291f50beb1864bc
type: hypothesis
parents:
  - hypothesis:goals-md-retires-with-every-caller-in-one-row
  - experiment:dg2mvp-wg-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 1641f53ab197f519
season: 2
testable_claim: no file under .agi/context/schemas names `snapshot-goals.py --render` except as a goal:g7.16.1.4.1 retirement pointer, each "Readers strip it" bullet names brief.py via node_writer.strip_thought, and the W-G reader test covers every schema file
title: The 12 node-type schemas name a THOUGHT-stripping reader that exists, not the retired GOALS.md render (W-G corrective)
town: core
---
# hypothesis:node-type-schemas-name-a-thought-reader-that-exists

## Measured
- Post-build check at ce07ade9c (experiment: DG2 W-G post-build, /tmp/dg2mvp/wg). W-G holds on all 7 conjuncts, but the parent's falsifier 4 ("a reader line names a read that does not exist") fires in the node-type schemas. These sit outside the parent's FILE SCOPE.
- 12 schemas ([bigger_outcome] [build] [experiment] [hypothesis] [idea] [mvp] [outcome] [overview] [shape] [task] [verdict] [vision]) carry the bullet "**Readers strip it.** … `snapshot-goals.py --render` strips it explicitly via `strip_thought()`". `--render` has been rc 2 since 254f58ef7. 16 schemas carry the bullet in all, and every one also names `render-context.py`, a retired file.
- The live body reader that strips THOUGHT is brief.py:2352-2359 (`_strip_thought` -> node_writer.strip_thought, node_writer:1055). zoom.py reads frontmatter only.
- test_snapshot_goals.py::test_wg_reader_lines_only_point_at_the_retirement lists only [goal].md and [config].md among the schemas. Open elsewhere and NOT this fork's: SM 99 ([config].md:227 config_path claim).

## CLAIM
(1) No `.agi/context/schemas/*.md` line names `snapshot-goals.py --render` or `render-context.py` as a live reader. (2) Each "Readers strip it" bullet names today's reader: brief.py via node_writer.strip_thought, with zoom.py frontmatter-only. It does this in ONE identical sentence across the 16 files. (3) The W-G reader test globs every schema file rather than a hand list, so a stale render claim in any schema turns it red.

## Dispatch line
config-max: none. template-max: the one bullet, the same text in 16 schema files (schemas are template text). code: none; one test list becomes a glob.

## FALSIFIERS
- `git grep -n -e 'snapshot-goals.py --render' -e 'render-context.py' -- .agi/context/schemas` prints a line without its own retirement pointer (`goal:g7.16.1.4.1` for `snapshot-goals.py --render`; `L1.05` for `render-context.py`, retired at 44ee2f65c)
- the 16 bullets are not byte-identical to each other (`git grep -h -A6 'Readers strip it' -- .agi/context/schemas | sort -u` gives more than one variant)
- the reader test stays green with the old bullet restored in any one schema

## TESTS
test_snapshot_goals.py only, `--basetemp /tmp/b4wgR`. Change the reader row's `docs` to `CLAUDE.md, QUICKSTART.md, the 5 skills + sorted(glob .agi/context/schemas/*.md)`, and extend its pattern with `render-context\.py`. Negative check, by hand, once: restore the old bullet in [verdict].md in a /tmp copy, and the row goes red.

## FILE SCOPE
.agi/context/schemas/*.md (the "Readers strip it" bullet only, 16 files) · extensions/agi/tests/test_snapshot_goals.py (the reader row)

## CEILING
no dispatch · 0 production code lines · <= 5 schema lines per file (one bullet) · <= 6 test lines · 0 USD

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Falsifier 1 amended post-build (DG2, 00:5xZ 09-30, on DG4 [built] 0d2ace8b8): as first written it demanded a goal:g7.16.1.4.1 pointer beside render-context.py too, but render-context.py retired at L1.05 (44ee2f65c, 2026-09-03), before g7.16.1.4.1 existed, so a truthful history line ([config].md:222 "render-context.py (retired, L1.05)") fired it. CLAIM (1) (no line names either as a LIVE reader) is unchanged; the test pins render-context.py to L1.05. Chosen over rewording the history line to a pointer that would be false.
<!-- THOUGHT:END -->
