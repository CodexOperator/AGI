---
id: hypothesis:l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded
mint_id: b7917461c99f46c3b1e921e547c97093
type: hypothesis
parents:
  - goal:g6.10
next_edges: []
edited_by: belam
scaffold_hash: dfcaa586bd7bac11
season: 2
testable_claim: "(1) links.py schema (goal:s31, dry by default) gains ONE check: for every verdict node whose evidence_runs/parents name an experiment node, the verdict CLASS (proved | disproved | inconclusive_lean_proved | inconclusive_lean_disproved | pending, the :N suffix stripped) equals the class the experiment's `verdict:` field records, or the verdict node carries a `demoted_from:` naming the experiment's class; every other pair prints as one line `verdict-class: <verdict id> says <a>, <experiment id> says <b>` and counts in the summary; --fix touches nothing for this check (report only). (2) MEASURED baseline (TM.54, thought town): ~1 of 5 pairs disagree (0.18-0.22 by join, CI 0.12-0.33; 13/24 raw disagreements are only the :N suffix; season.py demoted_from explains 3/11) -- the kid re-measures on core's own graph in the node before the check lands and records the count the check reports on the first run. (3) [verdict].md gains an OPTIONAL `reviewed_by:` field (a post name) so an independent relabel can exist; absent stays valid, the spawn gate is unchanged. (4) TESTS: a tmp graph with three pairs -- equal classes (silent), a :N-only difference (silent), a real class flip without demoted_from (one line, counted), the same flip with demoted_from naming it (silent); links.py schema exit code unchanged by this check. (5) SCOPE ADDED (thought-master, measured a link_ref pointing outside the repo tree, broken on both trunks after a sync): links.py schema also reports any link_ref/payload_ref that resolves outside the repo tree, and write.py refuses to set one at write time, one gate, one message naming the path. FILE SCOPE: extensions/agi/bin/links.py, extensions/agi/bin/write.py, .agi/context/schemas/[verdict].md, extensions/agi/tests/test_links*.py. CEILING 16 production lines."
thought_session: dissolve-legacy-2026-09-19
title: "SM.131 (thought-master 23:4xZ, TM.54 graph-hygiene finding; schema/gate cut = SM's while master-sensei is inactive): a verdict node's class equals the class its evidence experiment recorded, ignoring the :N confidence suffix, unless demoted_from names the demotion -- links.py schema reports every pair that disagrees"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-a-verdict-node-carries-the-class-its-evidence-experiment-recorded

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SCOPE += (thought-master 01:4xZ, measured: doc:lm-director-brief-customizations carried link_ref -> a dead-session /tmp scratchpad path, BROKEN on both trunks after a sync): links.py schema also reports any link_ref/payload_ref that resolves outside the repo tree, and write.py refuses to set one at write time (one gate, one message naming the path); ceiling +4 -> 16.
