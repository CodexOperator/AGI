---
id: experiment:magic-pane-messaging-router-a00-6aaf0235
mint_id: 2edda8846afe4855815336b5bb60873c
type: experiment
parents:
  - hypothesis:a00-6aaf0235-f70ce8
next_edges: []
edited_by: a00-6aaf0235
evidence_runs:
  - experiment:magic-pane-messaging-router-a00-6aaf0235
line_ceiling: 40
loop: goal:g7.32.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 59
profile: balanced
role: kid
season: 2
tags:
  - magic-pane
  - messaging
  - g7.32.2
testable_claim: messaging.route/send selects native for identical harness strings and cross otherwise; native drives only pane.pane_send and never send.py, cross emits a nudge_artifact first and then invokes the send.py CLI, and messaging.py imports no rotate/dispatch symbol.
title: "Magic-pane messaging router: native pane vs cross nudge to send.py, measured"
town: core
---
<!-- BODY:BEGIN -->
# experiment:magic-pane-messaging-router-a00-6aaf0235

## What this run is

Prototype product layer for `goal:g7.32.2`: `extensions/agi/bin/messaging.py`
decides **native vs cross** and carries the message. It owns no pane-hold
(g7.31.1), no adapter pane methods (g7.32.3), no send.py internals (g7.32.4).

```
        route(sender_harness, target_harness)
                     │
      same harness   │   different harness
            ▼        │        ▼
   ┌─────────────┐   │   ┌──────────────────────────────┐
   │  send_native │   │   │  send_cross                  │
   │  pane.pane_send(text) │ 1. NudgeArtifact(seat,sender,│
   │  trace: [("pane_send", …)] │    body,wake_intent) FIRST │
   │  send.py: NEVER touched │ 2. runner([py, send.py,     │
   └─────────────┘   │   │    "send","--to",seat,text]) │
   no runner called  │   │ trace: [nudge_artifact,send_py]│
                     │   └──────────────────────────────┘
                     │   pane.pane_send: NEVER called
```

The nudge wake intent is rendered from send.py's own wake-token prefix
(`NUDGE_WAKE = "[agi-nudge] {sender} -> {seat}: {body}"`, shape from
`send.py`'s `NUDGE_TOKEN_BARE_TEMPLATE` at send.py:1401). send.py still owns
the durable token format; messaging renders the intent only.

## Commands and real output

```
$ python3 -m pytest extensions/agi/tests/test_messaging.py -q
.....                                                                    [100%]
5 passed in 5.21s
```

Production measurement (new file, untracked, so `wc -l` not `git diff`):

```
$ wc -l extensions/agi/bin/messaging.py
59 extensions/agi/bin/messaging.py
```

## Falsifier clause -> test -> result

| clause (goal:g7.32.2) | test in test_messaging.py | result |
|---|---|---|
| 1. same-harness grok↔grok documented + scripted without send.py | `test_route_native_iff_same_harness`, `test_native_uses_pane_and_never_send_py` (spy runner asserts `argv == []`) | pass |
| 2. cross shows nudge artifact then send.py in one measured trace | `test_cross_is_nudge_then_send_py_and_never_native` (order is exactly `[nudge_artifact, send_py]`; argv contains `send`, the seat, the body) | pass |
| 3. grep: module imports no rotate/dispatch | `test_no_rotate_or_dispatch_import` (AST walk over messaging.py) | pass |

Also proven: `PaneMethodMissing` is raised (named, fail-closed, no hang) for
`pane=None` and for a pane object with no `pane_send`
(`test_native_missing_pane_method_fails_closed_named`), matching the
absence case g7.32.3 will own.

## What is NOT proven

- No live grok pane exists in this checkout: native is measured against a
  fake pane object, not a real tmux window. The seam is duck-typed
  (`pane.pane_send`) exactly so g7.32.3 can supply the real method.
- The cross path's `runner` is a spy: the send.py CLI argv is built and
  ordered, but no live send.py process was spawned here.
- `messaging.py` is not wired into any caller (dispatch/rotate) — by design
  this round; the module is the seam, not the integration.
- send.py's durable nudge-token format is untouched and unverified here.

## Deviations

- The node file the dispatcher scaffolded is a `hypothesis`
  (`hypothesis:a00-6aaf0235-f70ce8`); this experiment is its child
  (`parents: [hypothesis:a00-6aaf0235-f70ce8]`), per the schema rule that
  `goal` is not an allowed experiment parent (goal:s22). The parent brief
  asked for `parents: [goal:g7.32.2]`; the goal remains the grandparent.
- Production lines 59 vs ceiling 40 (below the 80 = 2x stop line); recorded,
  not trimmed, because the extra lines are docstrings, not logic.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
New prototype seam: native = pane.pane_send only; cross = nudge artifact then send.py CLI. Kept send.py out of the native import path so the falsifier grep stays clean.
<!-- THOUGHT:END -->
