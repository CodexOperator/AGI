---
id: experiment:a00-188c74cc-wire
mint_id: 4b1f7a2c9d3e4f5a6b7c8d9e0f1a2b3c
type: experiment
parents:
  - hypothesis:a00-188c74cc-42551a
next_edges: []
edited_by: a00-188c74cc
evidence_runs:
  - experiment:a00-188c74cc-wire
line_ceiling: 40
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 30
profile: balanced
role: kid
season: 2
testable_claim: "on the LIVE registry names: grok-bot->grok-bot is native with no send.py argv even on rc!=0; grok-bot->claude-code/pi is cross with the nudge artifact under send.comms_root present at send.py invoke; importing magic_pane loads neither rotate nor dispatch nor send"
thought_session: iter-DH.149
title: "magic_pane wire fix: live-name family routing, native survives rc!=0, nudge in send.comms_root"
town: core
---
# experiment:a00-188c74cc-wire

## Experiment

Build order (`hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement`):
built the fix, then measured it.

Round 1's defect: `NATIVE_HARNESSES = {"grok"}`, but the only grok name this
tree constructs is the registry/adapter name `grok-bot`
(`adapters/grok_bot_adapter.py:25 NAME = "grok-bot"`; `.agi/config.json`
`harnesses` key `grok-bot`). Before bytes, captured with the parent's probe
(`.agi/sessions/iter-DH.149/a00-188c74cc/before_probe.txt`):

```
choose_route('grok-bot') -> 'cross'
send_message(dest=grok-bot) route='cross'
argv calls: [['/usr/bin/python3', '.../send.py', 'send', 'grok-b', 'hi', '--from', 'grok-a']]
send.py in argv: True
tmux send-keys in argv: False
```

The fix, in `extensions/agi/bin/magic_pane.py` (net −2 lines; 30 lines added /
32 removed by `git diff --numstat`, under the 40-line ceiling):

- `HARNESS_FAMILIES` dict maps registry/adapter name -> family
  (`grok-bot -> grok`, `claude-code -> claude`, `pi`/`pi-local -> pi`,
  `copilot-cli -> copilot`); `NATIVE_FAMILIES = {"grok"}` is data and
  `choose_route` is one lookup. No `if harness == "grok-bot"` branch.
- `nudge_artifact_path` now resolves through `send.comms_root(root)` (a lazy,
  cross-path-only import of send), so the nudge dir is the SAME root
  send.py's reader uses — no parallel comms fork. (Round 1 wrote under
  `locations.shared_sessions_dir(root)/comms/pane-nudge`, a different room.)
- The native path never touches `send.py`, including on a non-zero tmux rc.

## Evidence

After bytes (`.agi/sessions/iter-DH.149/a00-188c74cc/after_probe.txt`):

```
LIVE HARNESS NAMES: ['pi', 'pi-local', 'claude-code', 'copilot-cli', 'grok-bot']
choose_route('pi') -> 'cross'  family='pi'
choose_route('pi-local') -> 'cross'  family='pi'
choose_route('claude-code') -> 'cross'  family='claude'
choose_route('copilot-cli') -> 'cross'  family='copilot'
choose_route('grok-bot') -> 'native'  family='grok'
send_message(dest=grok-bot) route='native'
argv calls: [['tmux', 'send-keys', '-l', '-t', 'agi-rc:grok-b', 'hi'],
             ['tmux', 'send-keys', '-t', 'agi-rc:grok-b', 'Enter']]
send.py in argv: False
tmux send-keys in argv: True
```

Regression check — the new live-name assertion run against the round-1 module
(saved as `magic_pane.round1.py` in scratch, loaded with importlib):

```
round-1 choose_route('grok-bot') -> 'cross' ; new assertion expects 'native' -> FAIL (regression caught)
```

So the new test genuinely fails on round-1 bytes rather than passing on an
invented string (the stub-never-sees-it hazard).

Tests (named explicitly, run from the source tree):

```
python3 -m pytest extensions/agi/tests/test_magic_pane.py -q
-> 7 passed
```

Coverage of the conjuncts and the hardening:
- `test_live_registry_grok_is_native_and_others_cross` — DERIVES the live names
  from `.agi/config.json` `harnesses` keys and the adapters' `NAME` constants,
  then asserts `grok-bot -> grok-bot` native (send-keys, no `send.py`) and
  `claude-code`/`pi` cross.
- `test_native_route_survives_nonzero_tmux_without_send_py` — rc=1 faked tmux
  keeps route native and no captured argv contains `send.py`.
- `test_cross_route_artifact_then_send_py_in_order` — artifact on disk at
  subprocess invoke (checked inside the fake run), argv is the send.py call.
- `test_cross_artifact_root_is_sends_own_comms_root` — artifact path ==
  `send.comms_root(project)/pane-nudge/<to>.nudge`.
- `test_import_graph_has_no_rotate_or_dispatch` — source grep plus a fresh
  interpreter: importing `magic_pane` leaves `rotate`, `dispatch` and `send`
  out of `sys.modules`; no module-level import of any of them.

## Verdict basis

All three conjuncts hold on the built bytes, on the names the tree actually
constructs. Conjunct 2's root mismatch is resolved by construction (the nudge
now resolves through `send.comms_root`), not by a disclaimer.
