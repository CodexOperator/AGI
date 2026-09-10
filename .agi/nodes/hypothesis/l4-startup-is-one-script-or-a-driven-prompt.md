---
id: hypothesis:l4-startup-is-one-script-or-a-driven-prompt
mint_id: 49b74e2570fd470eae0a5daacf89ee33
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L4-V
scaffold_hash: 064978d617b43319
season: 2
testable_claim: "OWNER 2026-09-10 (verbatim in doc:l4-owner-decisions): 'Every fresh session, I see agents execute from fifty to as many as one hundred and twenty or more different tool calls before they ever say anything other than, oh, I'm here. I'm new. I'm ready. ... there's no reason that this all shouldn't happen as one long script. If there's certain variables or settings that need to be set, is there a way we can script how they are set so everything is config maxed? And if not, can we make sure that the start up procedure ... is a driven type of turn by turn thing ... it just kinda feeds you one at a time, what you need to do next, what you need to type in next, like the literal tokens, and the button press you need to do to proceed.' MEASURED BASELINE (Prime, 2026-09-10, eight transcripts): 26-97 tool calls before the first non-bookkeeping commit, median ~47. What those calls DERIVE is the same every time and is all knowable before the session exists: mail addressed to the seat, the seat row at HEAD, the verification result, the account balance, the live addresses by the @id join, the workflow registry state, the crons state, the floor numbers. CLAIM, two halves: (1) ONE INJECTED BLOCK — the predecessor's button-down (hypothesis:l4-the-predecessor-hands-over-authority) writes a bootstrap record <sessions>/seats/<seat>.bootstrap.json holding every one of those facts with the commit they were measured at, and the SessionStart hook (hooks/cc-session-start.sh, which already injects INJECTION.md) injects it as one block when the session is a seat successor — so a successor wakes KNOWING its state and spends zero tool calls deriving it. Every variable the startup sets is declared in a .geometry config node (which facts, in what order, staleness bound), not in prose — config-maxxed, the same shape as crons.md and commands.md. (2) A DRIVEN PROMPT for whatever cannot be scripted — rotate.py next --seat <seat> prints EXACTLY the next command to run and nothing else, one step per call, reading a step list from the same .geometry node and advancing on the previous step's recorded success; the successor types literal tokens. PROVED BY: (a) a live successor whose transcript shows the bootstrap block injected at turn one and fewer than 10 tool calls before its first non-bookkeeping commit — against a median of 47; (b) the bootstrap record's facts each carry the commit they were measured at and the hook refuses a record older than the staleness bound in the node rather than injecting stale state; (c) rotate.py next on a fresh seat walks the whole startup with the operator typing only what it prints; (d) the step list and the fact list live in the .geometry node and changing them there changes the injection and the prompt without a code edit. DISPROVED BY: any successor after this lands that re-derives a fact the bootstrap block already carried. HARD RULES: the hook is a silent no-op outside a project and must stay one; injected context is READ by every session so keep the block small and diagram-shaped — the trim mandate applies to it from birth; no new bin/*.py; the record is written by the predecessor's handover, never by the successor; the .geometry node is created with write.py create and A NODE THE SUITE PINS IS CODE (trap 0al)."
thought_session: f3b92df1
title: Startup is one injected block or a driven prompt — never fifty tool calls of orientation
---
<!-- BODY:BEGIN -->
# hypothesis:l4-startup-is-one-script-or-a-driven-prompt

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
