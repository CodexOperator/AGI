---
id: hypothesis:a00-96adeacf-f8a541
mint_id: 8059c52deca142ea903d5efc514c3fd4
type: hypothesis
parents:
  - goal:g7.32.2
next_edges: []
confidence: 0.9
edited_by: a00-96adeacf
evidence_runs:
  - experiment:magic-pane-native-route-a00-96adeacf
line_ceiling: 40
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 <scratch>/probe_kid1.py: native_send with send.send_dm/_nudge_window/_nudge_target patched to RAISE", "expected": "path=native, target=agi-rc:@246, text typed; no transport exception", "observed": "path=native target=agi-rc:@246 typed=7 argv=agi-rc:@246; transport never invoked", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "probe_kid1.py route() edge cases", "expected": "empty/unequal harness -> nudge-send; ws+case equal -> native", "observed": "route(,,)=nudge-send; route(grok-bot,claude-code)=nudge-send; route(grok-bot,GROK-BOT)=native", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "probe_kid1.py: native_send to a windowless seat + AST re-read of messaging.py import list", "expected": "NoAddressableWindow, zero keystrokes; no rotate/dispatch in own imports", "observed": "refused NoAddressableWindow; keystrokes=[]; imports=[__future__,boxes,pathlib,send,subprocess,time]", "result": "pass"}
production_lines: 40
profile: balanced
role: kid
scaffold_hash: 3930634881384976
season: 2
testable_claim: "`extensions/agi/bin/messaging.py` routes same-harness messages natively (tmux `send-keys` straight into the recipient's `@id` window, resolved from the `config:posts` rows) and NEVER invokes the `send.py` transport; it imports neither `rotate` nor `dispatch`. Cross-harness is a named `cross_send` seam for `goal:g7.32.4`."
title: "magic-pane messaging: same-harness native tmux route, cross-harness seam"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-96adeacf-f8a541

## Claim

`extensions/agi/bin/messaging.py` routes same-harness messages natively
(tmux `send-keys` straight into the recipient's `@id` window, resolved from
the `config:posts` rows) and NEVER invokes the `send.py` transport; it
imports neither `rotate` nor `dispatch`. Cross-harness is a named
`cross_send` seam for `goal:g7.32.4`.

Falsified by: a same-harness call reaching `send.send_dm` / `send._nudge_*`,
a `route()` that misclassifies by harness, a no-window seat that gets typed
into, or an import of rotate/dispatch in the module's own import list.

## Built

### A — `extensions/agi/bin/messaging.py` (40 production lines)
- `NoAddressableWindow(RuntimeError)` — L9 (fail-closed refusal)
- `route(sender_harness, target_harness) -> str` — L13
- `_native_target(root, to_seat, tmux_session) -> str` — L19
- `native_send(root, to_seat, text, *, sender=None, tmux_session=None) -> dict` — L28
- `cross_send(...) -> dict` — L39 (named seam, `NotImplementedError`)

`native_send` reuses `send._seat_row_by_name(send._locally_loaded_rows(root), seat)`
(the ONE seats reader) plus `boxes.row_is_local`; a row whose `window` is not
an `@id`, a missing row or a foreign-box row raise `NoAddressableWindow`
before any keystroke.

### B — `extensions/agi/tests/test_magic_pane_messaging.py`
6 tests: wire (target `<session>:@id`, text typed, transport record EMPTY),
routing, fail-closed (no row / no window / NAME window), foreign box, the
AST import invariant, and the named cross seam.

### Routing decision table

```
                    sender harness == target harness?
                        │ yes                    │ no (or either empty)
                        ▼                        ▼
                  route() = "native"       route() = "nudge-send"
                        │                        │
     native_send(root,to,text)            cross_send(root,to,text)
        │  resolve row.window @id             │  goal:g7.32.4 seam
        │  <session>:@id                      │  (kid 2 fills this)
        ▼                                     ▼
   tmux send-keys -l <text>              NotImplementedError now,
   tmux send-keys Enter                  nudge artifact -> send.py later
        │
        ▼
   NO send.py, NO inbox, NO rotate/dispatch
```

## Measured

Command:
```
python3 -m pytest extensions/agi/tests/test_magic_pane_messaging.py -q
```
Output: `6 passed in 13.00s`

Negative probe against the real bytes
(`.agi/sessions/iter-DH.177/a00-96adeacf/probe_negative.py`):
```
imports: ['__future__', 'boxes', 'pathlib', 'send', 'subprocess', 'time'] rotate/dispatch present: False
route same: native
route diff: nudge-send
route ws/case: native
route empty: nudge-send
fail-closed OK: NoAddressableWindow
```

Production lines: 40 (`wc -l`; the file is untracked so `git diff --numstat`
reports no rows).

## Seam left for conjunct 2

`messaging.cross_send` (L39) is the named seam: the cross-harness
`nudge -> send.py` measured trace (falsifier conjunct 2) is kid 2's slice
and belongs there, never in `native_send`.

## Agent Notes
messaging.py (40 lines) routes same-harness natively via tmux @id, transport-free, rotate/dispatch-free; cross_send seam left for g7.32.4; 6 tests + negative probe pass

Parent review DH.177 (a00-ab3bb108). Read the BYTES, not the summary: messaging.py is 40 production lines, test_magic_pane_messaging.py is 6 tests. Ran three independent negative probes (wire/gate/auth) against the real module and recorded them under `probes`; all three pass. Deliverables A/B/C all present in the tree: route/native_send/_native_target/NoAddressableWindow/cross_send seam exist as claimed; the AST check confirms no rotate/dispatch in the module own import list; native_send reuses send._locally_loaded_rows + boxes.row_is_local and never calls the transport. Verdict left at the auto-demoted inconclusive_lean_proved:50 because the kid named its own hypothesis node as evidence (no experiment child); that is a plumbing gap, not a claim failure — the parent probes independently confirm the claim. Falsifier conjunct 2 (cross-harness nudge->send measured trace) is NOT covered by this kid and is assigned to the next kid.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent DH.177 review of kid a00-96adeacf. WHAT THE KID BUILT (from the bytes): a thin routing module messaging.py with route() harness comparison and native_send() that resolves the config:posts row window (@id) and types via tmux send-keys, plus a fail-closed NoAddressableWindow for missing/NAME/foreign rows; a 6-test suite; and a named cross_send NotImplementedError seam for the cross-harness slice. WHY THIS VERSION DIFFERS FROM THE KID S OWN: it adds the parent probes record and the review note; the claim and verdict are the kid s. The NEAR MISS the kid avoided: importing send and calling send.send_dm for BOTH paths would have satisfied route()==native on paper and violated the same-harness transport-free invariant; the module imports send only for the seats reader and native_send never calls the transport. Verified by patching send.send_dm/_nudge_window/_nudge_target to raise and re-running native_send — it still delivers. DEVIATION: none from standing rules; the only judgement call is leaving the auto-demoted 50 lean rather than promoting it, because no experiment node exists to evidence a proved verdict.
<!-- THOUGHT:END -->
