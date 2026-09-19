---
id: hypothesis:l5-moral-one-loads-in-full-into-every-master-and-director-head-each-rotation
mint_id: 77613e107fe3489dbbc7f050e28018c0
type: hypothesis
parents:
  - goal:g17.1
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 6665f5d5671415b1
season: 2
testable_claim: "(1) MEASURED: the CONSTITUTION HEAD injected at spawn (config:rotations template -> brief.py head --tier <tier>) carries only the prayers section of moral:faith; the rest was moved to `brief.py readings --tier` on demand (hypothesis:l3w4-context-load-minimal). (2) brief.py head, for tier master and tier director (every master post, every director post, both towns), renders the FULL body of moral:faith (moral 1) byte-for-byte from the node at render time -- read from the graph, never a copy in code or template -- placed first in the head, followed by the four prayers exactly as today; the kid/parent/reviewer tiers keep today's head (prayers) unless the owner names them. (3) The rotation template needs no edit if it already calls brief.py head per tier; if a template line trims or caps the head (the 8000-byte facts cap or any readings trim), moral 1 is exempt from the cap and the cap applies after it. (4) TESTS (red-first, test_brief.py + test_rotate*.py): the rendered head for tier master and tier director contains moral:faith's body exactly (diff empty) and the prayers after it; tier kid unchanged; a moral:faith edit changes the next render with no code change; the spawn's STARTUP head (rotate-self dry render) shows it. NEVER edit moral:* -- read only. FILE SCOPE: extensions/agi/bin/brief.py (head tier rule), extensions/agi/tests/test_brief.py, and only if measured necessary the config:rotations template line that caps the head. CEILING 10 production lines."
title: "SM.138 (OWNER 04:3xZ 09-19 in the SM pane, verbatim: 'Add moral 1 as part of every master's and director's standard brief to be loaded in programmatically each rotation.'; goal:g17.1): brief.py head for the master and director tiers carries moral:faith (moral 1) IN FULL, byte-for-byte, above the four prayers, at every rotation -- never trimmed, never on-demand"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-moral-one-loads-in-full-into-every-master-and-director-head-each-rotation

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
