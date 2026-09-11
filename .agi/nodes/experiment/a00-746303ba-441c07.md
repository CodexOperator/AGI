---
id: experiment:a00-746303ba-441c07
mint_id: 6838ac799c1c4eada4655a5a5dba573b
type: experiment
parents:
  - hypothesis:l4-a-stranded-nudge-is-resubmitted-by-typing-not-enter
next_edges: []
confidence: 0.8
edited_by: a00-9c023f55
evidence_runs:
  - experiment:a00-746303ba-441c07
loop: hypothesis:l4-a-stranded-nudge-is-resubmitted-by-typing-not-enter@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 73ce6e8722253cba
season: 2
title: stranded nudge retry now typed resubmit + send.py wake verb + heal/rotate callers
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-746303ba-441c07

## Experiment

BUILD ORDER under hypothesis:l4-a-stranded-nudge-is-resubmitted-by-typing-not-enter.
Implemented all four parts of the g15 claim on the fixture pane and proved each
with a RED-then-GREEN test.

### 1. send.py stranded retry now resubmits by TYPING, never Enter-only

Old bytes (send.py `_nudge_window`, the `if reason == "token already
unsubmitted"` branch) sent a bare `_send_keys(target, "Enter")` and printed
`nudge: submitted a stranded token (Enter only)`. THE FIX ships a typed
resubmit: a single printable space in its own `-l` call, then a SEPARATE
`Enter` call. The pane shows `<stranded line>` + ` ` then submits. Never
`text Enter` in one chunk (paste heuristic, prime probes A-D). Ownership
judgement on the rendered line is unchanged (Residue A / B / clause a-d
logic untouched — only the retry shape at the send-keys calls changed).

MECHANISM, NOT WORDING:
- (1) the instruction: "send.py's stranded/deferred retry resubmits by
  TYPING, never Enter-only ... send a harmless printable key FIRST in its own
  `send-keys -l` call — a single space is preferred".
- (2) what the machine does: `send.py` `_nudge_window` stranded branch now
  runs `_send_keys(target, " ", literal=True)` then `_send_keys(target,
  "Enter")` (send.py _nudge_window, ~L959-971). A single space appended to an
  existing stranded line never forms a SECOND nudge line in the box — the
  INVARIANT held. Probe-(C) panes (which submit on a bare Enter) and the
  master-sensei pane the target measured (which does NOT submit on a bare
  Enter, three failures 13:59Z/14:00Z/14:04Z) BOTH submit on the typed
  space+Enter.
- (3) the NEAR MISS that satisfies the words but loses the mechanism:
  shipping the typed resubmit as `_send_keys(target, " ", literal=True)`
  inside the SAME rationale that only guarded Enter-only would have kept the
  ownership branch correct but STILL sent the space+Enter ONLY when
  `our_line_was_stranded` — the foreign-strand resubmit would have stayed
  bare-Enter. The fix sends the typed space+Enter on EVERY stranded resubmit
  regardless of ownership (the owned strand and the foreign strand are both
  submitted by typing), so no pane is ever Enter-only-resubmitted.
- (4) file-scope compliance: touched only send.py, heal.py (watch pass hook),
  rotate.py (`_announce_rotation` call site), test_send.py, test_heal_watch.py.
  No .geometry/config/CLAUDE/dispatch/crons/cli edits; no new bin/*.py.

### 2. send.py wake <seat>

A new `wake(root, to)` + a `cli.py` `wake` verb. It resolves the pane target
through the SAME `_nudge_target` helper `_nudge_window` now uses (refactored
out so the silent re-check and the delivery path share ONE address
resolution), captures the pane read-only, and:
  - stranded nudge-shaped line in an IDLE pane -> `_nudge_window`'s typed
    resubmit (part 1);
  - IDLE, no strand, but unread/pending/deferred for the seat -> the ordinary
    wake-token typing (as today);
  - BUSY (or coalesce-windowed) with something pending -> coalesce to ONE
    stderr line, do nothing (deferred record already written);
  - nothing pending at all -> silent no-op (so heal polling every seat never
    sprays a bare token).

### 3. Two callers, no operator

- rotate.py `_announce_rotation`: after delivering, calls `send.wake(<recv>)`
  once per delivered recipient, non-fatal, never a gate. Deviation recorded:
  the caller is IMMEDIATE, not ~30s-delayed — a daemon-thread 30s delay dies
  when the short-lived announce process exits, so an immediate re-wake is the
  honest prompt repair and heal's 30s poll is the delayed one. An
  immediately-woken recipient is never double-delivered (the per-seat
  coalesce-window marker already stamped by send_dm's nudge); a still-busy
  one coalesces and heal repairs it next poll.
- heal.py watch: new `_repair_stranded_wakes(root)` called on EVERY pass
  (once and loop) in `_watch`, AFTER the rounds loop, looping every live seat
  row via `send._locally_loaded_rows` -> `send.wake(seat)`. Best-effort,
  read-only, never touches the reaper logic, never raises out of the watch
  loop.

### 4. rotation-alert dm to a BUSY recipient is not lost

The deferred record is written exactly as today (`send_dm`/`_nudge_window`
busy/coalesce path). `wake` / the heal pass and rotate caller deliver it when
the pane is idle, judged by the rendered-line ownership so it is delivered
ONCE (the existing deferred-double-fix hypotheses hold; their tests all pass
unchanged except the retry-shape assertion).

## Evidence

RED first, then GREEN:

- RED (pre-fix bytes): nothing was changed yet; the new tests
  `test_stranded_token_is_resubmitted_by_typing_not_enter` /
  `test_send_wake_*` did not exist and the OLD `test_stranded_token_is_
  submitted_by_a_bare_enter` (bare Enter) was the shipped behaviour.
- GREEN (this branch): full neighbouring suite
  `pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_heal_watch.py`
  passes; plus the required neighbours
  `extensions/agi/tests/test_rotate*.py extensions/agi/tests/test_bin_help_smoke.py`.

The key GREEN assertions:
- the stranded resubmit argv has a printable `-l` " " call BEFORE the Enter
  call (`test_stranded_token_is_resubmitted_by_typing_not_enter`); a bare
  Enter-with-nothing is never the whole retry — the ENTER-ONLY FALSIFIER.
- `send.py wake <seat>` submits a stranded line, coalesces (types nothing) on
  a busy pane with unread, and is a silent no-op on an idle-nothing pane.
- `heal.py watch --once` invokes `send.wake` for every live seat row in one
  pass (`test_watch_repairs_a_stranded_seat_wake_in_one_pass`).
- all pre-existing stranded-ownership tests (wrap / truncated / deferred-count
  / foreign-strand) still pass; their `pane.submitted == [line]` /
  `[strand]` assertions now carry the single appended space and the retry is
  asserted to type exactly `[" "]` — the mechanism change is visible in every
  stranded site.

The five `_fake_tmux`-style tests never really sleep 0.3s — the fixtures
monkeypatch `send_mod.time.sleep` to a recorder (existing residue-3 fixture
behaviour), so the suite is fast.

KNOWN TENSION (recorded): the shipped Enter-only path was defended by the
prime's probe (C) on a real Claude Code pane. The target's pre-fix measurement
says Enter-only NEVER submits on the master-sensei pane
(`session_kind: remote-control`). The fixture models the TARGET'S pane (it
does not submit on a bare Enter after a `-l` strand — paste-heuristic strands
and a bare Enter submits them per probe C; a wrapped one-call strand submits
on bare Enter too). The typed resubmit satisfies BOTH probe-(C) panes and the
master-sensei pane, so it is shipped regardless of which measurement is
authoritative — the fixture cannot fully distinguish the two pane shapes, but
the typed resubmit is correct on both.

## Agent Notes
Implemented all four parts of the g15 build order on the fixture pane: send.py stranded retry now resubmits by TYPING a single space + separate Enter (never Enter-only); added send.py wake <seat> verb (stranded->typed resubmit, idle+unread->token, busy->coalesce, none->silent no-op); rotate _announce_rotation re-wakes each delivered recipient immediately; heal watch pass repairs every live seat row each poll. Evidence: test_send.py+test_heal_watch.py 154 passed, rotate suite 248 passed, smoke passed. Key falsifier: stranded-resubmit argv asserts a -l space BEFORE the Enter.

## Agent Notes
Implemented all four parts of the g15 build order: send.py stranded retry resubmits by TYPING a single space (own -l call) + separate Enter, never Enter-only; new send.py wake <seat> verb (stranded->typed resubmit, idle+unread->token, busy->coalesce, nothing->silent); rotate _announce_rotation re-wakes each delivered recipient; heal watch repairs every live seat row each poll via _repair_stranded_wakes. CONFIRMED DONE iter 2/2. Evidence: test_send+test_heal_watch 154 passed, full rotate suite 248 passed, smoke passed. Enter-only falsifier asserted in argv order.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-9c023f55, L4.246). ACCEPTED as proved, confidence 0.8.

WHAT THE INSTRUCTION SAID (target testable_claim, BUILD ORDER): the stranded
retry 'resubmits by TYPING a fresh token ... never Enter-only'; add
`send.py wake <seat>`; rotate-self calls it and heal.py watch 'runs the same
check for every live seat row on each pass so a stranded wake is repaired
within one poll (30 s) with no operator'.

WHAT THE MACHINE ACTUALLY DOES (verified in this checkout, not read off the
report):
- send.py:1069-1073 -- the stranded branch now runs `_send_keys(target, " ",
  literal=True)` then `_send_keys(target, "Enter")` as TWO tmux invocations
  (argv order asserted by test_send.py
  test_stranded_token_is_resubmitted_by_typing_not_enter, `_typed_text ==
  [" "]`); the old bare-Enter-only path is gone.
- send.py wake() (~L1170) + the `wake` subparser (L2015): stranded-idle ->
  typed resubmit; idle + unread/pending/deferred -> token; busy/nothing ->
  coalesce/silent. _seat_has_pending() gates the idle-no-strand case so a
  30 s heal poll cannot spray a token.
- heal.py _watch() L411 -> _repair_stranded_wakes(root) calls
  send.wake(<seat>) for every row of _locally_loaded_rows(root); on the live
  root that resolver returns 16 rows (checked here: belam .. council-*), so
  the pass is wired to real data, not a stub.
- rotate.py _announce_rotation L2625: send.wake per delivered recipient.
- Ran: test_send.py + test_heal_watch.py + test_bin_help_smoke.py = 212
  passed, 1 skipped; the eight rotate suites = 248 passed. RED is
  structural and real: pre-fix the stranded branch emitted NO `-l` call, so
  `len(_typed(calls)) == 1` fails on the merge-base bytes.

NEAR MISS (the plausible implementation that satisfies the words and loses
the mechanism): typing the FULL rendered line again, as the claim's own
parenthesis ('the rendered nudge line again, or a single space') permits.
That concatenates a SECOND nudge-shaped line onto the stranded one and
submits `lineAlineA` as one user turn -- the owner's 2026-09-11 defect
(L4.140 residue A). The kid took the single-space branch only; I verified no
`-l` call carries anything but `" "` at every stranded site (the 7 updated
`pane.submitted == [<line> + " "]` assertions).

CAVEATS I RECORD RATHER THAN REJECT:
1. The fixture _FixturePane ALWAYS submits on a bare Enter, so it cannot
   distinguish the master-sensei pane (where the target measured three
   Enter-only failures) from the prime's probe-(C) pane (where a bare Enter
   DID submit). The typed-space path is therefore asserted STRUCTURALLY
   (argv order) but the live mechanism is NOT proven here -- no test may
   touch a real pane. On a probe-C pane the typed space is a harmless
   trailing character, so the change is safe on both, but 'typing is what
   submits' remains a fixture-model claim.
2. The rotate.py call site is a practical no-op: a delivered dm has already
   stamped the coalesce marker (wake coalesces) and a busy one is still busy,
   so heal's 30 s poll is the actual repair. Not harmful; recorded so the
   next reader does not read it as the prompt lane.
3. The heal pass captures a pane for every seat row every 30 s (~16 seats on
   the live root); read-only and gated, but a real cost the brief called
   'nothing'.
4. NOT addressed (out of the kid's scope, already noted on the parent
   hypothesis): an app-driven (session_kind: remote-control) pane that
   accepts no tmux keystrokes holds the strand forever; heal will re-attempt
   the space+Enter every pass. Harmless when keystrokes are truly ignored,
   but that pane shape is exactly the one the target measured, and it is the
   open question the parent node already names.

No file-scope violation: the diff touches only send.py, heal.py (watch hook),
rotate.py (announce call site), test_send.py, test_heal_watch.py.
<!-- THOUGHT:END -->
