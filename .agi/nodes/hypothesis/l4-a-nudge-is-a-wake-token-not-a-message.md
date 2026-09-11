---
id: hypothesis:l4-a-nudge-is-a-wake-token-not-a-message
mint_id: be34ed263c974408bfcbc6b98d806cd1
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L4-VII
scaffold_hash: c7d0b8479d4a7fe2
season: 2
testable_claim: "OWNER 2026-09-11 01:4xZ (verbatim in doc:l4-owner-decisions): \"director is getting erroneous user message nudges: These user messages are just the same nudge defect I have already logged. iter=iter-L4.118 still-running=a00-68853df0. Can we investigate his logs and relay dispatching a fix round real quick\". MEASURED by the Prime L4-VII on the point transcript (session 3451295d, user turn 2026-09-11T01:20:04Z): the text `iter=L4.116 agent=a00-effd25bd node=experiment:a00-effd25bd-b5e162 verdict=inconclusive_lean_proved:70 <CR> iter=iter-L4.116 still-running=a00-0fa5cde6` arrived as ONE user prompt: two send.py nudges (a kid completion dm 01:13:35Z, the reaper give-up dm 01:20:04Z) typed by send.py _nudge_window (`tmux send-keys -t agi-rc:<window NAME> <full body> Enter`) into a BUSY pane; Enter does not submit while a turn runs, so the bodies concatenate (the point measured the Prime 01:34Z dm glued to five alarm lines the same way). CLAIM: a nudge is a WAKE TOKEN, never a message. (1) _nudge_window types ONE fixed, machine-prefixed token, e.g. `[agi-nudge] unread in your inbox: python3 extensions/agi/bin/send.py read`, never the body and never the sender text; the body lives only in the inbox/dm file. (2) IDEMPOTENT under busy: before typing, capture the target pane; if the token is already present unsubmitted, or the pane shows no idle input line, type nothing and record `nudge: coalesced` on stderr; at most ONE token per unread batch per seat; a later send retries the token when the pane is idle. (3) ADDRESS BY @id: resolve the recipient row in config:seats and use its `window` (@id) as the send-keys target; fall back to the window NAME only when the row carries no window; never type into a name-matched window whose @id differs from the row (a predecessor or a namesake). (4) Every seat brief states that the token is machine text, not the owner, and that `send.py read` is the only way to see the message. (5) FIXTURES ONLY: every nudge test runs against a fake tmux (a PATH shim or a monkeypatched runner) with fixture panes; the suite never send-keys into a live pane (L4.10). FALSIFIERS: a typed nudge that contains any part of a message body; two nudges into a busy fixture pane yielding two tokens or a concatenation; a send-keys addressed by name when the row carries a window id; a test that reaches a real pane. SCOPE: extensions/agi/bin/send.py (callers such as dispatch.py give-up/alarm dms and heal.py stay unchanged: they call send.send), extensions/agi/tests/test_send.py and its neighbours in suite order. Parallel-safe; serial with nothing. NOT in scope: the reaper premature give-up (hypothesis:l4-the-reaper-is-one-persistent-service, L4.116)."
thought_session: belam-S1-L4-VII
title: A nudge is a wake token, never a message — one fixed machine-prefixed token, idempotent under a busy pane, addressed by the seat row's @id
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-nudge-is-a-wake-token-not-a-message

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
