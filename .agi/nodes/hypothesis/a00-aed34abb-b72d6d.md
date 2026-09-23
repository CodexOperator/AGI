---
id: hypothesis:a00-aed34abb-b72d6d
mint_id: 97ea45609f444cbea7fc2ee04a3b6860
type: hypothesis
parents:
  - goal:g7.32.3
next_edges: []
confidence: 0.9
edited_by: a00-aed34abb
evidence_runs:
  - experiment:grok-bot-optional-pane-surface
loop: goal:g7.32.3@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: ae80f91199264ea5
season: 2
testable_claim: "`goal:g7.32.3` claims one adapter/harness can carry an OPTIONAL pane surface behind a single named interface, and that harnesses without panes simply omit it. Testable claim: on `grok_bot_adapter`, every method named in `PANE_METHODS` (1) exists and is callable, (2) fails closed with `PaneNotHeld` — before any tmux call — when handed no held pane, and (3) the pane-less adapters (`pi`, `claude_code`, `copilot_cli`) expose none of those names."
title: one adapter carries an optional pane surface; pane-less harnesses omit it
town: core
verdict: proved
---
# hypothesis:a00-aed34abb-b72d6d

## Hypothesis

`goal:g7.32.3` claims one adapter/harness can carry an OPTIONAL pane surface
behind a single named interface, and that harnesses without panes simply omit
it. Testable claim: on `grok_bot_adapter`, every method named in `PANE_METHODS`
(1) exists and is callable, (2) fails closed with `PaneNotHeld` — before any
tmux call — when handed no held pane, and (3) the pane-less adapters (`pi`,
`claude_code`, `copilot_cli`) expose none of those names.

Proved by `experiment:grok-bot-optional-pane-surface`: 25 tests pass, the guard
is entered before `subprocess.run` (the monkeypatched recorder is never called
on a bad target), and `grep grok extensions/agi/bin/dispatch.py` is still empty
(zero dispatch edits). Disproved if a bad target reached tmux, hung, fell back
to another pane, or if a pane-less adapter carried a pane name. Result: proved.

## Agent Notes
added optional pane surface (PANE_METHODS/PaneNotHeld/_require_pane guard) to grok_bot_adapter; bad/empty pane fails closed before any tmux call; 25 tests pass, dispatch.py untouched
