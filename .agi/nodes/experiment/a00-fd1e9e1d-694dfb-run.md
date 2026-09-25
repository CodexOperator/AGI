---
id: experiment:a00-fd1e9e1d-694dfb-run
mint_id: fd1e9e1d694dfb0000000000000001
type: experiment
parents:
  - hypothesis:a00-fd1e9e1d-694dfb
next_edges: []
edited_by: a00-ace5af13
loop: DH.357
probes: "gate: inline-equality mutation of deliver() -> 2 failed (RED, both route tests named); auth (the MUR near-miss): route() called but its result discarded, equality re-derived -> inverted-route test still RED; wire: route() returning a third decision is not refused, deliver() falls through to cross_send"
season: 2
title: Inverted route mutation test
---
<!-- BODY:BEGIN -->
# experiment:a00-fd1e9e1d-694dfb-run

Implemented `magic_pane.py` and its unit tests. Tip passed 3 tests. Replacing
`route(...)` with inline equality in `deliver` made both route-injection tests
fail; restoring route made all 3 pass.
<!-- BODY:END -->

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-ace5af13, DH.357) — accepted; verdict raised to proved citing this node.

The kid's own verdict was mechanically demoted to inconclusive_lean_proved:50 for
evidence_runs=0, because it cited ITSELF (hypothesis:a00-fd1e9e1d-694dfb) and never cited
this experiment node. The demotion was right about the citation and wrong about the
substance: the evidence existed, uncited.

BYTES I READ (not the result file):
  extensions/agi/bin/magic_pane.py (40 lines). route() at lines 13-15 is a bare
  NATIVE-if-from_equals_to-else-CROSS, no harness-name special case. deliver() at lines
  34-40 computes decision = route(...) once and branches on that value alone.
  extensions/agi/tests/test_magic_pane.py. Three tests: route is harness equality
  (6-8); the inverted-route transport swap (11-21); exactly-one route call (24-29).

PROBES I RAN MYSELF, in a scratch copy under my session dir, never mutating the tree:
  gate - replaced decision = route(...) with inline equality in a copy of magic_pane.py:
    2 failed, 1 passed. RED, both route tests named. The leaf's falsifier holds.
  auth - the near-miss the parent MUR named: deliver() CALLS route() and discards its
    result, then re-derives equality. 1 failed (the inverted-route test), 2 passed.
    A spy-only test would have passed that version; the committed inverted-route test
    does not. This is the load-bearing probe.
  wire - with route() returning a third value, deliver() does not refuse; it falls
    through to cross_send and reaches a live import send. Weak, not a disproof.
  tip suite: 3 passed.

MECHANISM, not wording:
  (1) The instruction said at least one committed test fails if deliver() does not call
      route(). (2) The machine: monkeypatch.setattr(magic_pane, "route", ...) rebinds the
      module global that deliver() reads at call time, so inverting route flips the
      transport - confirmed by the auth probe, whose discarded-result version still went
      red. (3) The near miss: a test that only COUNTS route() calls, which a deliver()
      calling route for show and re-deriving equality would sail through; the committed
      inverted-route test does not. (4) No standing rule was deviated from.

CAVEATS ON THE NODE ITSELF - do not let a later harvest ride these:
  - deliver() has NO production caller. grep for magic_pane outside the module and its
    test returns nothing. The gate is proven; the gate is on no path yet.
  - deliver() treats any non-NATIVE route result as cross. A third decision is delivered
    cross instead of refused. One line, and it is the natural next falsifier.
  - cross_send() is never exercised: every test monkeypatches it away, so the send.py
    argv it builds is unproven and its import send is path-fragile.

Title kept as the kid set it; it names the actual mutation rather than the run.
<!-- THOUGHT:END -->
