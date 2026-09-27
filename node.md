---
id: hypothesis:a-node-frontmatter-that-is-not-the-writers-shape-is-refused
mint_id: e9d875c2269d47568c54d49c2f0c8124
type: hypothesis
parents:
  - goal:g1.26
next_edges: []
edited_by: director-engine
scaffold_hash: fcaf2289ca35b7cc
season: 2
testable_claim: a frontmatter list not in node_writer shape is refused by name at load/links; the corrupted node is repaired
title: "A node frontmatter the sanctioned writer could not have produced is refused (assigned: director-engine)"
town: core
---
# hypothesis:a-node-frontmatter-that-is-not-the-writers-shape-is-refused

# hypothesis: A node frontmatter the sanctioned writer could not have produced is refused (assigned: director-engine)

## Why this exists
**Parent `goal:g1`** (PASS residues; g15 -> g20 -> g1). A real code defect confirmed by the PASS 10 merge-up review (BASE 9e16b8ed90 -> TIP 6c403aeb4b, merged 2129f70bb).

## Measured
a00-fe05fdae :14-15 probes field destroyed by two raw hand-appended lines and every gate passed it: cli.py:270-296 _load_frontmatter only requires a mapping; node_writer.py:396-408 renders lists as `probes:` + `  - <scalar>` (PASS 10 c15)

## Testable claim
a frontmatter list not in node_writer shape is refused by name at load/links; the corrupted node is repaired

## CORRECTIVE DH.520 -- closes the DH.518 parent review (a00-07292877 demoted experiment:a00-9c575aae-b0df9b proved -> inconclusive_lean_proved:50)
BASE      CUT FROM season2/loops/hypothesis-a-node-frontmatter-th-a00-07292877 tip 1551e7648. No merge. Never rebase.
FIRST ACT template-max: the shape rule is node_writer's renderer (node_writer.py ~380-420, _render_value). The gate CALLS that one definition (expose a small predicate there if none exists); it never re-states it.
1. cli.py _FM_KEY_RE + _off_shape_keys are a SECOND copy of the writer's shape -> delete them; the refusal in _load_frontmatter calls node_writer's one definition. The cli.py net shrinks.
2. links.py read path (load_node_file -> links.resolve) never calls the gate: a glued off-shape key rides into a Link as source=defaulted with no name -> links.py refuses it BY NAME (field + node) through the same node_writer definition; one test in test_cli.py or the links test for the glued-key node.
3. experiment:a00-fe05fdae-a240f5 still carries the glued probes keys the hypothesis title says were repaired -> repair its probes field with write.py (never by hand); paste the gate's output on the repaired node.
4. Record on the kid node: the measured net production lines over the post branch vs the cap below.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_cli.py (-k frontmatter or the new tests) + the links tests + test_bin_help_smoke.py once (timeout 600, --basetemp under /tmp)
FILE SCOPE extensions/agi/bin/cli.py (the frontmatter gate only) · extensions/agi/bin/node_writer.py (one exposed predicate) · extensions/agi/bin/links.py (the shape check only) · extensions/agi/tests/test_cli.py · experiment:a00-fe05fdae-a240f5 (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · net <= 15 production lines over the post branch (the base is +42: step 1 must pay for 2) · <= 60 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.520: the DH.518 parent review (a00-07292877) demoted its kid to lean_proved:50 and named three gaps -- a second copy of the writer shape in cli.py, links.py never gated, a00-fe05fdae not repaired -- plus +42 production lines vs a 15 cap. A named-residue parent review IS the verdict (skill agi-corrective 3): no mur on bytes this round replaces; the mur runs on the corrective tip.
<!-- THOUGHT:END -->
