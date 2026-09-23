---
id: hypothesis:a00-aed34abb-b72d6d
mint_id: 97ea45609f444cbea7fc2ee04a3b6860
type: hypothesis
parents:
  - goal:g7.32.3
next_edges: []
confidence: 0.9
edited_by: a00-da85626e
evidence_runs:
  - experiment:grok-bot-optional-pane-surface
loop: goal:g7.32.3@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 -c import adapters;m=adapters.load(grok_bot);assert all(callable(getattr(m,n)) for n in m.PANE_METHODS);assert not hasattr(m,pane_bogus)", "expected": "all 4 PANE_METHODS resolve callable; an unlisted name is absent", "observed": "4/4 callable; pane_bogus AttributeError", "result": "confirmed"}
  - {"conjunct": 2, "class": "gate", "cmd": "probe1.py: monkeypatch grok.subprocess.run=recorder then call every PANE_METHOD with None//0/False", "expected": "PaneNotHeld raised by name for every case and subprocess.run never reached", "observed": "12/12 PaneNotHeld; subprocess reached 0", "result": "refused by name"}
  - {"conjunct": 3, "class": "wire", "cmd": "list adapters/*grok* and *pane*adapter*; hasattr(pane name) on pi/claude_code/copilot_cli imports", "expected": "one grok module, no second pane adapter, pane-less harnesses expose none", "observed": "[grok_bot_adapter.py]; []; pi/claude_code/copilot_cli all []", "result": "one module"}
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-da85626e review of kid a00-aed34abb, target goal:g7.32.3. MECHANISM. WHAT THE INSTRUCTION SAID: "One negative probe per claim conjunct, run by YOU, recorded as probes ... A kid that passes its own tests and fails your probe is lean_disproved." WHAT THE MACHINE ACTUALLY DOES, cited to the changed bytes and to a probe I built and ran, not to the result file: extensions/agi/bin/adapters/grok_bot_adapter.py now carries PANE_METHODS, class PaneNotHeld, _require_pane, _tmux, and pane_present/pane_attach/pane_read/pane_send; my probe1.py ran three probes and all three HOLD. Probe A, wire, conjunct one: on a live import all four PANE_METHODS resolve callable and a name outside the tuple is absent. Probe B, gate, conjunct two: with grok.subprocess.run monkeypatched to a recorder, calling every method with None, empty string, 0 and False raised PaneNotHeld 12 of 12 times and the recorder was reached 0 times (no hang, no fallback pane). Probe C, wire, conjunct three: exactly one *grok* module grok_bot_adapter.py, zero *pane*adapter* modules, and pi/claude_code/copilot_cli expose none of the four names. THE NEAR MISS: a guard that checks only a module-global held-pane variable and otherwise falls back to a default pane would satisfy the words "fails closed" and lose the mechanism; this guard rejects on the argument itself before any tmux call, which is precisely why subprocess.run is provably never reached. DEVIATION/EDGE, recorded not hidden: with a non-existent pane NAME and tmux returning rc=1, pane_attach raises PaneNotHeld but pane_read returns an empty string and pane_send returns False, a soft fail rather than the named error. Hold validity is what the target explicitly leaves to goal:g7.31.1 ("methods wrap, do not re-own hold"), so this is a caveat, not a conjunct falsification. Verdict stands: the target falsifier is green on these bytes.
<!-- THOUGHT:END -->

parent a00-da85626e: 3/3 conjunct probes pass on the changed bytes; kid title real; deliverables (grok_bot_adapter.py, test_grok_bot_adapter.py) both carried; caveat: pane_read/pane_send soft-fail (empty/False) on a non-resolving pane name rather than raising PaneNotHeld — hold-validity is g7.31.1, so not a falsification
