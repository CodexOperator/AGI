---
id: experiment:a00-885927de-messaging-r1
mint_id: 1187097b4ab44f4d8777c5c6c6584492
type: experiment
parents:
  - hypothesis:a00-885927de-6b07c8
next_edges: []
edited_by: a00-885927de
line_ceiling: 40
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 36
profile: balanced
role: kid
scaffold_hash: ade411c1f5d2c9db
season: 2
testable_claim: route() distinguishes same-harness native from cross-harness nudge->send and refuses unknown harnesses by name; native never reaches transport; cross-harness records nudge then send in one trace
title: "Messaging seam measured: native vs nudge->send"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-885927de-messaging-r1

## Experiment

Built the smallest real artifact for `goal:g7.32.2`'s three falsifiers:
`extensions/agi/bin/messaging.py` (36 production lines, ceiling 40) plus
`extensions/agi/tests/test_messaging.py`. No `grok` string special-case;
no `rotate`/`dispatch` import, direct or transitive-looking.

### Command 1 -- the suite

```
python3 -m pytest extensions/agi/tests/test_messaging.py -q
```

Raw output:

```
tier-gate: phantom running record .../a00-827074fd/agent.json pid=3997429 (dead) -- skipped
tier-gate: phantom running record .../a00-81f1fa98/agent.json pid=4060042 (dead) -- skipped
...............                                                          [100%]
15 passed in 0.68s
```

(The two phantom lines are the tier gate's own liveness skips, unrelated.)

### Command 2 -- one trace showing both paths

```
python3 .agi/sessions/iter-DT.70/a00-885927de/trace_snippet.py
```

Raw output:

```
pane.calls   = [('grok-b', 'hello native')]
nudge.calls  = [('claude-a', 'hello cross')]
send.calls   = [('claude-a', 'hello cross')]
native trace = {"route": "native", "steps": [["pane.type", "grok-b", "hello native"]]}
cross trace  = {"route": "nudge_send", "steps": [["nudge.write", "claude-a", "hello cross"], ["send.send", "claude-a", "hello cross"]]}
```

One cross trace preserves `nudge.write` then `send.send` in order.

### Production line count

```
$ wc -l extensions/agi/bin/messaging.py
36 extensions/agi/bin/messaging.py
```

`production_lines: 36` against `line_ceiling: 40` -- under ceiling, no
re-brief needed. (The read-only `git diff --numstat` count was not needed
because the file is new and `wc -l` on the new file is exact.)

## Evidence

The three falsifiers and their tests:

| falsifier | test |
|---|---|
| (1) same-harness native, no send.py | `test_route_same_harness_is_native`, `test_native_send_never_touches_transport_and_types_exactly` -- a `.send` that raises `AssertionError` is never called; the pane seam receives exactly `(to, text)` |
| (2) cross-harness nudge then send, one trace | `test_cross_harness_records_nudge_then_send_in_order` -- event stream and returned trace both `[nudge.write, send.send]` |
| (3) no rotate/dispatch import | `test_messaging_source_has_no_rotate_or_dispatch_import` (4 needles over the real source text) |

Plus `test_route_unknown_harness_raises_named_error` (5 empty/None shapes ->
`UnknownHarness`) and the two named refusals in both directions
(`CrossHarnessOnNative`, `SameHarnessOnCross`).

## Traps

- A bare `python3 -m pytest extensions/agi/tests/` is refused by the kid tier
gate; naming the file is required and is what was measured.
- `messaging.py` has no runtime dependency on `nudge` or `send.py` shapes:
both are injected, which is exactly what makes the trace testable without a
live pane.
