---
id: hypothesis:council-report-reads-the-mur-args-shape-per-round
mint_id: 1941743eda374dd3bf79892bb9a70d64
type: hypothesis
parents:
  - experiment:dg2mvp-g716103-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 2144ad5b228e560d
season: 2
testable_claim: with a rounds[] args file of two rounds, council_report.py add writes each round its own old..new and routes each round residues to the owner resolved from that round hypothesis; an unmatched label or unknown tip is rc 2, never a ?..? row
title: council_report.py add reads the mur args file per round (old_tip, new_tip, hypothesis owner), never a flat per-run dict that writes ?..? and routes every residue to the default leaf
town: core
---
# hypothesis:council-report-reads-the-mur-args-shape-per-round

## Measured
- g716103 post-build, tmp clone: council_report.py add with the mur args shape ({rounds:[{key,hypothesis,parent: <agent id>,old_tip,new_tip,files}]}) writes `?..?` rows over the correct ones and routes all 19 residues to the default leaf (owner director-engine); with the flat {parent: goal, old, new, subject} it works (2 rows, 19 on the owner leaf, idempotent).
- council_report.py reads args.get("old"/"new"/"parent"/"subject") once per RUN; a run labels several rounds with ONE old..new and ONE owner.

## CLAIM
`council_report.py add --run K --args F` accepts the mur args file ({rounds:[...]}) : each label of run K matches a round (key == label or key a prefix of it; no match = rc 2 naming the label), takes old_tip..new_tip from that round, and resolves the owner from that round's hypothesis -> its parent goal title `(assigned: <post>)`, else the post at the end of new_tip's commit subject (git log -1), else director-engine. A row whose old or new is unknown is refused (rc 2 naming the label), never written as `?..?`. The flat shape stays accepted.

## Dispatch line
config-max: none / template-max: none / code: council_report.py add (args reader + per-round owner resolve), one test file.

## FALSIFIERS
- F1: a fixture run with 2 labels and a rounds[] args file of 2 rounds with different old_tip/new_tip and different hypotheses -> the 2 report rows carry their OWN old..new, and each owner leaf gets its OWN residues = else false.
- F2: a rounds[] args with no round matching a label -> not rc 2 naming the label = false; any row containing `?..?` written = false.
- F3: the flat shape (the existing tests) goes red = false.

## TESTS
test_council_report.py: three rows (F1-F3), tmp project + tmp git repo, one file per run, never the live graph.

## FILE SCOPE
extensions/agi/bin/council_report.py · extensions/agi/tests/test_council_report.py

## CEILING
1 kid · council_report.py NET <= +25 production lines · tests NET <= +40 · 0 USD · SAFETY: never run `add` on the live graph; never set council.residue_leaves (the Prime's cell).
