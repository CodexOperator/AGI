---
id: hypothesis:l4-comms-never-re-deliver-harness-shaped-text-raw-a-quoted-block-reads-as-marked-data
mint_id: 90048ec40b3040958bc2277852bf2bcf
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: babf0d8a28ffebac
season: 2
testable_claim: "Measured (SM relay of an owner-flagged pane order, 2026-09-16 ~17:3xZ): the after_join self-dm carries harness-level block text (the AFTER_JOIN/STARTUP-style header plus output) raw, and send.py read/peek print stored message bodies raw with no fencing -- two posts today independently misread a genuine harness reminder delivered this way as a prompt injection. Claim, one round: (a) send.py read/peek fence any harness-block signature found in a body as marked quoted data before printing it, never as literal unescaped output; (b) the after_join self-dm composer (rotate.py after_join path -- confirm exact call site) strips or escapes that signature when building the message so legitimate service output cannot masquerade as a live harness block; (c) send.py send refuses to accept a raw unfenced block matching the signature unless --quote-harness is passed, and every call site (read, peek, send, the after_join composer) shares ONE signature constant, never independently spelled. Falsifiers: an unfenced harness-shaped block still prints raw from read or peek; the after_join-built self-dm still carries a bare signature; send() accepts a raw matching block with no --quote-harness; two different literal signatures exist across the sites. Tests: read/peek on a stored body containing the signature renders it fenced/marked, not raw; the after_join self-dm round-trips through read already fenced; send() of a raw matching block without --quote-harness is refused, named exit; the same block with --quote-harness passes through fenced; all sites reference the one constant, grep count = 1 definition. Ceiling 40 production lines, one kid, send.py plus the after_join self-dm composer plus each touched files own test file only -- no other file."
title: L4 comms never re deliver harness shaped text raw a quoted block reads as marked data
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-comms-never-re-deliver-harness-shaped-text-raw-a-quoted-block-reads-as-marked-data

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
