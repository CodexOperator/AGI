---
id: hypothesis:l4-the-predecessor-hands-over-authority
mint_id: 772e7eca6ce94f8987aa2cc3f1a4b294
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L4-V
scaffold_hash: 151068ed8ca96772
season: 2
testable_claim: "OWNER 2026-09-10 (verbatim in doc:l4-owner-decisions): 'whenever the rotation happens, the new successor must manually claim the pin and their authority before everybody or anybody acknowledges them. And really, that should be something the predecessor does to the successor. The predecessor first gives up its authority to the successor, and then the predecessor makes sure that everything else is buttoned down as the successor is already taking over.' TODAY'S ORDER, measured: the predecessor writes the handoff, spawns, and exits its work; the successor then claims its own pin (rotate.py meter --pin), reads the whole handoff to answer a gate that names the predecessor as live, verifies its own seat row, re-runs the verification the predecessor just ran, and only then works. BASELINE across the last eight prime/seat transcripts on this box (measured by the Prime, 2026-09-10): 26 to 97 tool calls before the first non-bookkeeping commit, median ~47; 88 to 182 tool calls per session; the seat row is the ONE piece already done the owner's way (L4-IV wrote L4-V's from the join before L4-V acted). CLAIM: rotate.py gains a handover verb the PREDECESSOR runs as one script, in this order: (1) spawn the successor's window; (2) join its @id to its session ref and transcript path (the join already exists in rotate.py loop); (3) WRITE THE SUCCESSOR'S AUTHORITY — its config:seats session_ref, its pin file pointing at ITS transcript, and its identity into the handoff header / agents-live / this-session / card so the ROTATION CONTINUATION gate is 'continue' BY CONSTRUCTION; (4) release the predecessor's own authority — its seats session_ref cleared or marked retired in the same write; (5) THEN button down — final commit, grid commit --all, push, and the verification run — while the successor is already working, and write the verification result where the successor's bootstrap reads it (see hypothesis:l4-startup-is-one-script-or-a-driven-prompt). The successor's first act is rotate.py ack (round 4); it claims nothing. PROVED BY: (a) one live rotation of any seat where the successor's transcript shows ZERO tool calls spent on pin, seat row, or handoff identity, and its first commit is work; (b) config:seats at HEAD names the successor before the successor's first tool call, verifiable by timestamps; (c) the gate answer is 'continue' and the handoff already names the successor when it reads it; (d) the predecessor's button-down verification is the one the successor reads, not re-runs. DISPROVED BY: any successor after this lands that runs rotate.py meter --pin on itself, writes its own seats row, or edits its own identity into the handoff. HARD RULES: rotate.py is build:bin-rotate, edited through write.py; identity is SUPPLIED never inferred (the join, not the newest transcript); authority is verified against the graph — the successor's row must be at HEAD and pushed before the successor acts; no new bin/*.py (test_bin_help_smoke); the ack channel from round 4 is the successor's first act and this round must not duplicate it."
thought_session: f3b92df1
title: The predecessor hands authority TO the successor, then buttons down — the successor wakes already authorized
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-predecessor-hands-over-authority

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
