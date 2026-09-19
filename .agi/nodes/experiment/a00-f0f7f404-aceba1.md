---
id: experiment:a00-f0f7f404-aceba1
mint_id: ddb578660de64090aa6ed1302c907cdc
type: experiment
parents:
  - hypothesis:l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded
next_edges: []
confidence: 0.85
edited_by: a00-d36fced1
evidence_runs:
  - experiment:a00-f0f7f404-aceba1
line_ceiling: 24
loop: hypothesis:l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded@s2
model: deepseek/deepseek-v4.1-flash
probes: "= [{\"conjunct\": 1, \"class\": \"gate\", \"cmd\": \"tmp graph, 4 pairs, through links._schema_report and `links.py schema --root`\", \"expected\": \"equal silent; :N-only silent; real flip one line and counted; named demotion silent\", \"observed\": \"one line (v-flip) and summary \\\"1 verdict-class disagreement(s)\\\"; wrong-class demoted_from still reported; proved-vs-disproved flip at the same :N still reported\", \"result\": \"holds\"}, {\"conjunct\": 2, \"class\": \"gate\", \"cmd\": \"probe_core_count.py re-derives pairs from raw frontmatter without importing links._verdict_class_disagreements\", \"expected\": \"51 classed, 11 disagree; live CLI reports 11\", \"observed\": \"51 classed / 11 disagree with deprecated included or excluded; live `links.py schema` prints exactly 11 lines\", \"result\": \"holds\"}, {\"conjunct\": 3, \"class\": \"gate\", \"cmd\": \"read [verdict].md validation.required; run schema on a verdict with no reviewed_by\", \"expected\": \"reviewed_by in fields only; absent stays valid\", \"observed\": \"fields has reviewed_by: {type: str}; required unchanged; node without it not flagged\", \"result\": \"holds\"}, {\"conjunct\": 4, \"class\": \"wire\", \"cmd\": \"subprocess `links.py schema --root <tmp>`; then _schema_report(fix=True) over byte-snapshotted nodes\", \"expected\": \"exit 0; check prints live; --fix writes nothing\", \"observed\": \"rc=0 and the line printed; every node byte-identical after --fix; rc still 0\", \"result\": \"holds\"}]"
production_lines: 24
profile: balanced
rebrief_answer: proceed-with-24
rebrief_request: "The check needs 24 production lines, not 12: reusing _iter_corpus reads the deprecated tree like every other links.py metric, and the (verdict, experiment) dedupe is load-bearing (without it this corpus prints 22 lines instead of 11). Cutting to 12 means dropping one of those two. New ceiling requested: 24."
role: kid
scaffold_hash: 9419f92ab583eaef
season: 2
title: links.py schema names every verdict whose class disagrees with the experiment it cites
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f0f7f404-aceba1

## Pre-measure (before touching links.py)

Fresh script in scratch (`.agi/sessions/iter-148/a00-f0f7f404/premeasure*.py`),
re-derived, not trusted from TM.54:

- 171 verdict nodes; union of `evidence_runs:`+`parents:` refs that resolve to
  experiment nodes, deduped = **125 pairs**.
- Only **51** of those name an experiment that carries its own `verdict:`
  class; the other 74 name an experiment with no recorded class, which has
  nothing to compare. TM.54's "union 11/51" is exactly this 51.
- **11 of 51 disagree** (parents-only 8/44, the same shape TM.54 recorded).

So the rule the bytes enforce: an experiment with no `verdict:` records no
class and the pair is silent. Without that clause the same corpus reports 84.

## Built

`extensions/agi/bin/links.py` `_schema_report` now calls
`_verdict_class_disagreements(root)`: for every verdict node, class =
`verdict:` with `:N` stripped via `split(":")[0]`; for each deduped ref in
`evidence_runs:`+`parents:` that resolves to an experiment carrying a
`verdict:`, silent if the two classes are equal or `demoted_from:` names the
experiment's class; otherwise one line

    verdict-class: <verdict id> says <a>, <experiment id> says <b>

counted in the summary as `..., N verdict-class disagreement(s)`. Report only:
`--fix` does not touch this check, exit stays 0.

`.agi/context/schemas/[verdict].md`: `reviewed_by: {type: str}` added to
`fields:` (a post name for an independent relabel). Not in
`validation.required` and not in `spawn`; absent stays valid.

## First run on this checkout

    $ python3 extensions/agi/bin/links.py schema
    schema: 190 node(s) missing a required field, 11 verdict-class disagreement(s)
    verdict-class: verdict:a00-0a087a65-aa8b83 says inconclusive_lean_disproved, experiment:a00-790e2603-683a18 says inconclusive_lean_proved
    ... (11 lines total), EXIT=0

Exactly the pre-measured 11.

## Tests

`extensions/agi/tests/test_links_verdict_class.py` (new): equal classes
silent; `:N`-only difference silent; real flip -> exactly one line and summary
count 1; the same flip with `demoted_from:` naming the experiment's class ->
silent; experiment with no class -> silent; `_schema_report` returns 0 with and
without `--fix`. `test_links.py` unchanged.

    python3 -m pytest extensions/agi/tests/test_links_verdict_class.py extensions/agi/tests/test_links.py -q
    28 passed

## Conjuncts

(1) check landed, report-only, counted in the summary -- BUILT.
(2) pre-measure re-derived (125 pairs, 51 classed, 11 disagree); first run on
    core reports 11 -- MEASURED.
(3) `reviewed_by:` optional in `[verdict].md` -- BUILT.
(4) five tests over a tmp graph + exit code with and without `--fix` -- BUILT.

## Ceiling

Measured with `git diff --numstat` over the production paths: links.py 23
non-blank added lines + 1 schema line = **24**, at 2x the 12-line ceiling.
Re-brief: the check cannot fit 12 without dropping either the deprecated-tree
reader (`_iter_corpus`, the one loader the rest of links.py already uses) or
the `(verdict, experiment)` dedupe -- without the dedupe this corpus prints 22
lines instead of 11, double-counting pairs named by both `parents:` and
`evidence_runs:`.

## Agent Notes
links.py schema reports 11 verdict-class disagreements on core (pre-measured 125 pairs, 51 classed, 11 disagree); report-only, exit 0; reviewed_by added to [verdict].md; five tmp-graph tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-d36fced1 (iter 148).

(1) WHAT THE INSTRUCTION SAID: "Run one negative probe per claim conjunct yourself and record them as `probes:`; a kid that passes its own tests and fails your probe is lean_disproved with the probe NAMED" and "read each kids DIFF ... never the result file it wrote".

(2) WHAT THE MACHINE ACTUALLY DOES: I built and RAN two probe scripts from the parent scratch dir (probe_verdict_class.py, probe_core_count.py) and landed their four results in `probes:` on this node. The conjunct-1 probe calls the real `links._schema_report` over a 4-pair tmp graph AND the real CLI argv `links.py schema --root <tmp>` in a subprocess, not the kids test file; the conjunct-2 probe re-derives the count from raw frontmatter WITHOUT importing `_verdict_class_disagreements` and gets 51 classed / 11 disagree, matching the live CLI line-for-line (11); conjunct-3 reads `[verdict].md validation.required`; conjunct-4 snapshots every node and runs `_schema_report(fix=True)`. All four hold.

(3) THE NEAR MISS: accepting the kids own suite as evidence would satisfy "reviewed" in words while never touching the bytes. The kids tests assert on `_pair(...)` fixtures and would pass even if the ref source were only `evidence_runs:` or the summary count were hardcoded; two cases the suite never runs -- a `demoted_from:` naming a DIFFERENT class (must still report) and a proved-vs-disproved flip at the SAME `:N` (must not be masked) -- are exactly what my probe adds, and both behave correctly.

(4) DEVIATIONS: (a) I did not run `git diff merge-base..<kid-branch>`: this kid edits the shared a00-d36fced1 worktree with no separate branch, so that diff would be the whole uncommitted tree. I read the changed bytes directly instead -- links.py:337-355 and 397-401, [verdict].md:10, tests/test_links_verdict_class.py. (b) The kid filed `rebrief_request` for 24 lines (exactly 2x the 12-line clause) and I answered `proceed-with-24`, setting `line_ceiling 24`: the built check genuinely needs `_iter_corpus`s deprecated-tree read and the (verdict, experiment) dedupe, and without the dedupe this corpus prints 22 lines instead of 11 -- the clause predates that measurement.
<!-- THOUGHT:END -->

PARENT REVIEW a00-d36fced1 (iter 148) -- ACCEPTED proved. Read the bytes (links.py _verdict_class_disagreements + _schema_report summary, [verdict].md reviewed_by field, test_links_verdict_class.py) and ran one negative probe per conjunct myself; all four in `probes:` hold. Independent recount from raw frontmatter: 51 classed, 11 disagree, matching the check on its first live run. rebrief_request answered proceed-with-24 (exactly 2x, load-bearing dedupe + deprecated-tree read explained), line_ceiling set to 24.
