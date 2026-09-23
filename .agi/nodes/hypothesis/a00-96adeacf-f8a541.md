---
id: hypothesis:a00-96adeacf-f8a541
mint_id: 8059c52deca142ea903d5efc514c3fd4
type: hypothesis
parents:
  - goal:g7.32.2
next_edges: []
confidence: 0.9
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: a00-96adeacf
evidence_runs:
  - hypothesis:a00-96adeacf-f8a541
line_ceiling: 40
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 40
profile: balanced
role: kid
scaffold_hash: 3930634881384976
season: 2
testable_claim: "`extensions/agi/bin/messaging.py` routes same-harness messages natively (tmux `send-keys` straight into the recipient's `@id` window, resolved from the `config:posts` rows) and NEVER invokes the `send.py` transport; it imports neither `rotate` nor `dispatch`. Cross-harness is a named `cross_send` seam for `goal:g7.32.4`."
title: "magic-pane messaging: same-harness native tmux route, cross-harness seam"
town: core
verdict: inconclusive_lean_proved:50
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
