---
id: hypothesis:a00-d3c9de22-a9ddd1
mint_id: 3fc0c28f3cb948b0a42f62191c4c5e73
type: hypothesis
parents:
  - goal:g7.32.4
next_edges: []
confidence: 0.85
edited_by: a00-d3c9de22
evidence_runs:
  - experiment:send-rotate-coupling-census
loop: goal:g7.32.4@s2
model: deepseek/deepseek-v4.1-flash
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
