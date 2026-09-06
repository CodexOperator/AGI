---
id: hypothesis:l2w3-send
mint_id: 8bbe213273cc4b34b15d68f783233d0c
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: director
scaffold_hash: 0d5d68cd32e38fcc
testable_claim: One send verb carries a message from any role to any other through a per-recipient inbox file under sessions, and a recipient can read and clear its inbox with the same tool
thought_session: agi-master-2026-09-06
title: "L2 wave 3: l2w3-send"
---
# hypothesis:l2w3-send

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
FILE: extensions/agi/bin/send.py (new) plus tests; brief.py gains one sentence per tier saying to check the inbox at each seam. Section 2, Comms is one verb: same call for kid to parent, parent to director, director to director above, council. TRANSPORT: an append-only file .agi/sessions/inbox/<recipient>.md where recipient is an agent id (a00-xxxx), a role name (director, prime-director), or council; each message is one block with ts, from (agent id or role, from AGI_AGENT_ID or --from), to, and the text; send.py send <to> <text> appends and prints the path; send.py read <me> prints unread blocks and marks them read (a marker line, not deletion, so the record stays); send.py peek <me> prints without marking. Chat stays chat: a decision reached in messages becomes a co-authored idea node minted by the humans or directors involved, send.py does not mint nodes. Transport for CC sessions is not built here; note it as the next adapter. brief.py: kid brief gains one line, if you must escalate use send.py send <parent id> <question> then stop; parent brief gains, read your inbox with send.py read <your id> before each kid review; keep both to one sentence. VERIFY red-first: send then read returns the block once and peek still shows it; two senders interleave without loss; suite green. REPORT: one experiment node under this hypothesis, verdict on the testable claim, evidence_runs as a list of node ids (pass --evidence-runs to cli.py done), every verify command with its actual output in the body. Engine files are edited in place; a new engine file goes directly under extensions/agi/bin/. Suite via python3 extensions/agi/bin/commands.py run tests, green before you report; every new rule gets a test that was red first. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/season-ladder-and-morals-brief.md
