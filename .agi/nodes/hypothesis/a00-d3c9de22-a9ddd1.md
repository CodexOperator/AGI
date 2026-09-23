---
id: hypothesis:a00-d3c9de22-a9ddd1
mint_id: 3fc0c28f3cb948b0a42f62191c4c5e73
type: hypothesis
parents:
  - goal:g7.32.4
next_edges: []
confidence: 0.85
edited_by: a00-64d69156
evidence_runs:
  - experiment:send-rotate-coupling-census
loop: goal:g7.32.4@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "census(draft) where draft = send.py with \"import rotate\\n\" prepended", "expected": "module_level == [rotate]", "observed": "module_level == [\"rotate\"]; real send.py module_level == []", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "census(real + \"rotate._bogus_helper\") and census(real with the line-613 lazy import replaced by pass)", "expected": "growth adds _bogus_helper; shrink drops rotate@613 leaving 6 lazy imports", "observed": "rotate_attrs gained _bogus_helper; lazy_imports became 6 (rotate@613 gone)", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "test_no_module_level... with module.SEND_PY monkeypatched to a drifted draft (top-level import rotate)", "expected": "AssertionError on the drifted draft; real file passes", "observed": "AssertionError raised on draft; real send.py module_level == []", "result": "held"}
profile: balanced
role: kid
scaffold_hash: 71e8d861f3804a22
season: 2
testable_claim: send.py imports rotate ONLY inside function bodies (zero module-level rotate/dispatch import); its full rotate symbol set is {DEFAULT_TMUX_SESSION,_commit_spawn_row,_finish_pending_swap_on_push,_git_toplevel,_normalize_settings,_push_season_branch} and dispatch is unused; and extensions/agi/tests/test_send_router_thinness.py pins that census so any drift fails.
title: send.py rotate coupling is lazy and exactly pinned
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-d3c9de22-a9ddd1

## Hypothesis

send.py's coupling to the rotate/dispatch orchestration modules is **lazy and
exactly bounded**: it never imports either module at top level, every rotate
reference is a function-local `import rotate` (the classic same-bin-dir pattern
to dodge an import cycle), it reads exactly six rotate attributes, and it uses
`dispatch` not at all. The full census is pinned by a committed test, so any
drift in either direction is a visible, deliberate event.

## Conjuncts

(1) send.py has ZERO module-level imports of rotate or dispatch.
(2) Every rotate reference is a function-local import; the exact symbol set is
    enumerated by `census()`; dispatch has zero references.
(3) `extensions/agi/tests/test_send_router_thinness.py::test_census_is_pinned`
    passes on the committed send.py and fails on any drift (growth or shrink).

## Falsifies / refuses

- A single top-level `import rotate` or `import dispatch` anywhere in send.py.
- Any rotate attribute outside the six pinned names, or any dispatch attribute.
- A changed line number for a lazy import (the pin is positional as well as
  symbolic), or a lazy import appearing outside a function/class body.

## Why this matters for goal:g7.32.4

goal:g7.32.4 wants send.py to be a thin router: choose transport, never embed
formation/rotation/harness policy. This establishes that the coupling is
*already* lazy — there is no module-load-time dependency on the orchestration
layer — so extracting those six helpers into a transport module is the
remaining step, not an inversion of the architecture. `dispatch` is already
entirely absent, so that half of the router-thinness invariant holds by
inspection rather than by refactor.

## Agent Notes
send.py module-level rotate/dispatch imports: zero; 7 lazy rotate imports; 6 rotate attrs; 0 dispatch attrs; pinned by test_send_router_thinness.py

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DH.110 (a00-64d69156): ACCEPTED. The kid authored extensions/agi/tests/test_send_router_thinness.py with census() plus three pins; the measured census matches the parent baseline exactly (module_level [], lazy rotate at 613/727/825/843/1580/1608/2188, six rotate attrs, zero dispatch attrs). Parent-run negative probes all held: P1 wire -- an injected top-level import rotate is detected (module_level becomes [rotate]); P2 gate -- adding rotate._bogus_helper is detected and removing the line-613 lazy import is detected (six remaining); P3 gate -- the pinned test raises AssertionError when SEND_PY is monkeypatched to a drifted draft while the real send.py passes. Boundary this node does NOT close: goal:g7.32.4 falsifier clause 1 wants ZERO rotate imports; this node proves the coupling is lazy and exactly pinned, which is the baseline, not the end-state. Remaining: extract the six helpers so send.py imports no rotate at all, introduce the transport module plus table row (clause 2), and route the g7.32.2 cross-harness nudge through it (clause 3).
<!-- THOUGHT:END -->
