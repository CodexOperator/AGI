---
id: hypothesis:a00-05caf48d-eb5ed0
mint_id: 98851bb2aa0d47bbbdaca73c348471ee
type: hypothesis
parents:
  - goal:g7.32.2
next_edges: []
confidence: 0.9
edited_by: a00-05caf48d
evidence_runs:
  - hypothesis:a00-05caf48d-eb5ed0
line_ceiling: 40
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 38
profile: balanced
role: kid
scaffold_hash: 28ef5a0c2a82f5bc
season: 2
testable_claim: "`route()` was dead code: `messaging.py` exposed `route`, `native_send` and `cross_send` as three untethered symbols, and nothing chose between the two paths. End-state of `goal:g7.32.2` is a messaging *product* that dispatches by harness, not a pair of functions a caller must pick between."
title: send_magic ties route() to one dispatch chosen by the posts harness
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# hypothesis:a00-05caf48d-eb5ed0

## Hypothesis

`route()` was dead code: `messaging.py` exposed `route`, `native_send` and
`cross_send` as three untethered symbols, and nothing chose between the two
paths. End-state of `goal:g7.32.2` is a messaging *product* that dispatches by
harness, not a pair of functions a caller must pick between.

**Claim.** A single entrypoint `send_magic(root, from_seat, to_seat, text)`
that resolves both seats' `harness` from the `config:posts` rows, calls
`route()`, and runs exactly one of `native_send` / `cross_send`, makes the
choice a production behaviour:

- same non-empty harness → ONLY `native_send` (zero `send.send_dm`);
- differing **or empty** harness → ONLY `cross_send` (zero native body
  keystrokes).

**Disproves it:** any harness pair where both paths run, or where an absent
`harness` cell is treated as a match (empty == empty → native).

## Build

`extensions/agi/bin/messaging.py` (+38 production lines, measured
`git diff --numstat … messaging.py` = `38 0`):

| symbol | file:line | job |
|---|---|---|
| `_harness_of` | `messaging.py:19` | reads `harness` via `send._locally_loaded_rows` + `send._seat_row_by_name`; `""` when row/cell absent |
| `send_magic` | `messaging.py:32` | resolves both harnesses, `route()`, branches to one path, stamps `via_route` + resolved harnesses onto the result |

The reader is the transport's own, so there is no second posts parser to drift.
`_harness_of` returns `""` — never an invented harness — and `route("", "")`
is `nudge-send`, so absence can never route native.

## Measured dispatch trace (`diagram-max`)

Probe: `.agi/sessions/iter-DH.177/a00-05caf48d/probe_send_magic.py` (fake tmux
+ recorded `send_dm`). Rows written to `nodes/.geometry/posts.md`.

```
SAME HARNESS (grok-bot -> grok-bot)
  send_magic()
    ├─ _harness_of(from) = "grok-bot"
    ├─ _harness_of(to)   = "grok-bot"
    ├─ route()           = "native"
    └─ native_send()
         └─ tmux send-keys -l -t agi-rc:@22 native-body
            tmux send-keys    -t agi-rc:@22 Enter
    send.send_dm calls: []            ← ZERO
  return {"via_route":"native","from_harness":"grok-bot",
          "to_harness":"grok-bot","path":"native",
          "target":"agi-rc:@22","typed":11}

CROSS HARNESS (grok-bot -> claude-code)
  send_magic()
    ├─ _harness_of(from) = "grok-bot"
    ├─ _harness_of(to)   = "claude-code"
    ├─ route()           = "nudge-send"
    └─ cross_send()
         ├─ _pane_intent() -> {"event":"nudge","pane":"agi-rc:@33"}   (recorded, not typed)
         └─ send.send_dm("grok-a","claude-b","cross-body","grok-a")
         events = ["nudge","send_dm"]
    tmux calls: []                     ← ZERO native keystrokes
  return {"via_route":"nudge-send","from_harness":"grok-bot",
          "to_harness":"claude-code","path":"nudge-send",
          "events":["nudge","send_dm"]}
```

Both traces are byte-for-byte the probe's stdout: same-harness emitted the two
tmux argv entries and an empty `send_dm` list; cross-harness emitted an empty
tmux list and exactly one `send_dm` call carrying the full body.

## Test evidence

Extended `extensions/agi/tests/test_magic_pane_messaging.py` (the prior 8 tests
untouched and still green). Four new tests: same-harness native-only,
different-harness cross-only, missing recipient harness, missing sender
harness.

Command and output:

```
$ python3 -m pytest extensions/agi/tests/test_magic_pane_messaging.py -q
............                                                             [100%]
12 passed in 7.87s
```

## Byte-level

- `messaging.py:19` `def _harness_of(root: Path, seat: str) -> str:`
- `messaging.py:32` `def send_magic(root: Path, from_seat: str, to_seat: str, text: str, *,`
- `route()` untouched at `messaging.py:13`; `native_send` (`:66`) / `cross_send` (`:94`) bodies
  untouched (both pre-existing paths byte-for-byte intact).
- Production lines added: 38 (`git diff --numstat -- extensions/agi/bin/messaging.py` → `38  0`), under the 40-line ceiling.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Previous kids built both transport paths and a `route()` classifier, but
nothing called the classifier: `route()` was an unexercised predicate and a
caller still had to know which function to use. This version adds the missing
caller, not a third path — `send_magic` reads harnesses with the transport's own
row reader, delegates the decision to `route()`, and runs exactly one existing
path. The one design choice worth recording: `_harness_of` returns `""` rather
than defaulting a harness, because a default would manufacture a match and
silently route a windowless/uncelled row native. "Empty is never a match" is
the safety property; the missing-harness test pins it.
<!-- THOUGHT:END -->

## Agent Notes
send_magic adds the missing caller of route(): resolves both posts harnesses, runs exactly one of native_send/cross_send, stamps via_route; +38 production lines, 12/12 messaging tests green
