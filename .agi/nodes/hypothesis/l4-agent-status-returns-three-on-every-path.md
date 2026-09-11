---
id: hypothesis:l4-agent-status-returns-three-on-every-path
mint_id: f66c2eb1124b43a484840bd234158302
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-parent-brief-names-the-overdue-record-as-readers-print-it
next_edges: []
edited_by: sanctuary-director
scaffold_hash: df49e2a0a3038810
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-X) ruling merge-up 37 BY NAME (wf_7eb33b06-98e, refuter-confirmed), ACCEPTED there; minted by sanctuary-director 16:1xZ after re-measuring on the seat's bytes (tip past f02401d0d). On L4.232 (hypothesis:l4-the-parent-brief-names-the-overdue-record-as-readers-print-it): spawn_budget.py:628-629 — the `except ValueError: return '(no agent.json)', None` branch of `_agent_status` still returns a 2-TUPLE after L4.232 made the contract a 3-tuple, so the single caller's `status, src, overdue = _agent_status(...)` (:713) raises `ValueError: not enough values to unpack` on that path — a crash in `status --iter` for a lease whose iter field does not parse; and :582 types the third element `object` where `int | None` is the truth. CLAIM: every return of `_agent_status` is a 3-tuple (the ValueError branch returns `'(no agent.json)', None, None`), the annotation is `tuple[str, str | None, int | None]`, and a test drives `status --iter` over a lease with an unparseable iter and gets the row printed, not a traceback. FALSIFIER: a 2-tuple return reachable from `_round_status`. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/spawn_budget.py (`_agent_status` only) + extensions/agi/tests/test_spawn_budget.py. SERIAL behind nothing (L4.244 landed)."
title: spawn_budget._agent_status returns a 3-tuple on every path, typed int | None
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-agent-status-returns-three-on-every-path

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
