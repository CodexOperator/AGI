---
id: experiment:a00-f0f7f404-aceba1
mint_id: ddb578660de64090aa6ed1302c907cdc
type: experiment
parents:
  - hypothesis:l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded
next_edges: []
confidence: 0.85
edited_by: a00-baa8e365
evidence_runs:
  - experiment:a00-f0f7f404-aceba1
line_ceiling: 24
loop: hypothesis:l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "tmp graph, 4 pairs, through links._schema_report and `links.py schema --root`", "expected": "equal silent; :N-only silent; real flip one line and counted; named demotion silent", "observed": "one line (v-flip) and summary \"1 verdict-class disagreement(s)\"; wrong-class demoted_from still reported; proved-vs-disproved flip at the same :N still reported", "result": "holds"}
  - {"conjunct": 2, "class": "gate", "cmd": "probe_core_count.py re-derives pairs from raw frontmatter without importing links._verdict_class_disagreements", "expected": "51 classed, 11 disagree; live CLI reports 11", "observed": "51 classed / 11 disagree with deprecated included or excluded; live `links.py schema` prints exactly 11 lines", "result": "holds"}
  - {"conjunct": 3, "class": "gate", "cmd": "read [verdict].md validation.required; run schema on a verdict with no reviewed_by", "expected": "reviewed_by in fields only; absent stays valid", "observed": "fields has reviewed_by: {type: str}; required unchanged; node without it not flagged", "result": "holds"}
  - {"conjunct": 4, "class": "wire", "cmd": "subprocess `links.py schema --root <tmp>`; then _schema_report(fix=True) over byte-snapshotted nodes", "expected": "exit 0; check prints live; --fix writes nothing", "observed": "rc=0 and the line printed; every node byte-identical after --fix; rc still 0", "result": "holds"}
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
Corrected in place under C item of hypothesis:mur-0921-engine-residues-dispositioned-and-corrected (EF.23, agent a00-baa8e365).
C item `exp aceba1` probe-shape: the `probes:` field was probes were a quoted `= [...]` scalar, which cli._parse_probes reads as None, while [experiment].md:18 wants a YAML LIST. It is now a real list, every probe string preserved verbatim. No verdict or lean field was touched.
<!-- THOUGHT:END -->

PARENT REVIEW a00-d36fced1 (iter 148) -- ACCEPTED proved. Read the bytes (links.py _verdict_class_disagreements + _schema_report summary, [verdict].md reviewed_by field, test_links_verdict_class.py) and ran one negative probe per conjunct myself; all four in `probes:` hold. Independent recount from raw frontmatter: 51 classed, 11 disagree, matching the check on its first live run. rebrief_request answered proceed-with-24 (exactly 2x, load-bearing dedupe + deprecated-tree read explained), line_ceiling set to 24.
