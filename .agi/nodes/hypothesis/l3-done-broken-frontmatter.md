---
id: hypothesis:l3-done-broken-frontmatter
mint_id: 972759bccd1b4082986a2c656cf11b40
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-II
scaffold_hash: 82ce16c14c9237bd
season: 2
testable_claim: cli.py done validates the node's frontmatter before demoting anything, repairs a broken or missing --- block from the spawn manifest when the body is intact, refuses loudly with the exact defect otherwise, and the kid brief tells kids to edit below the closing --- only
title: L3 done broken frontmatter
---
# hypothesis:l3-done-broken-frontmatter

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OBSERVED L3.13 (kid a00-fc49e2ad, struggles line on experiment:a00-fc49e2ad-ecd68a): the kid's write tool overwrote the scaffolded node's frontmatter mid-run and broke the --- block; cli.py done first demoted proved to inconclusive and then could not parse the node at all; the kid restored the frontmatter by hand and re-ran done. A parse failure is not missing evidence, and the gate must not treat it as one. Related prior art: hypothesis:l2-done-doubled-frontmatter (L3.09: the writer absorbs a doubled block). FILES: extensions/agi/bin/cli.py (done path), extensions/agi/bin/node_writer.py (scaffold), extensions/agi/bin/brief.py (KID template only), extensions/agi/tests/test_cli*.py, test_brief.py. CHANGE: (1) cli.py done validates the frontmatter first: a missing or unterminated --- block, or one without id, type and parents, is repaired from the spawn manifest (the agent.json in the session dir carries node id, type, parent and scaffold_hash) when the body below is intact; otherwise done refuses with a non-zero exit, prints the exact defect and the repair command, and records NO demotion and NO verdict change; (2) the kid template says: edit below the closing --- only, never rewrite the frontmatter, set frontmatter fields with write.py set; (3) the scaffold writes a one-line HTML comment right after the closing --- marking where the body starts. Edits must be atomic (write each file whole, run its tests at once) because live advisors import brief.py when they spawn a director this same hour. VERIFY: red-first tests: broken block + intact body is repaired from the manifest and done proceeds with the verdict unchanged; a node with body damage is refused, exit non-zero, no demoted_from stamped; the assembled kid brief contains the below-the-frontmatter rule; suite green via python3 extensions/agi/bin/commands.py run tests. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output. Do not commit, push, or run grid.py commit. Another kid edits rotate.py this round; three live claude-code advisors are running under iter-L3.14 — report unexpected files, never touch them, never kill a process.
