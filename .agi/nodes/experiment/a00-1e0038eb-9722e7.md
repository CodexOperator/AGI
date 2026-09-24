---
id: experiment:a00-1e0038eb-9722e7
mint_id: b58dabcb98084f7e9186e5cb7d2586ab
type: experiment
parents:
  - hypothesis:the-pending-key-swap-completes-only-after-the-authority-publish
next_edges: []
confidence: 0.9
edited_by: a00-f0258525
evidence_runs:
  - experiment:a00-1e0038eb-9722e7
loop: hypothesis:the-pending-key-swap-completes-only-after-the-authority-publish@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent hermetic probe A: pending{deferred_for:authority} + the push-OK/no-authority shape of sites :18803/:18924/:18960 -> rotate._finish_pending_swap_on_push(tmp, seat, \"push: OK\")", "expected": "key swap NOT completed naming AUTHORITY; <seat>.key byte-identical; pending survives", "observed": "PASS A1-A3; 13/13 probe assertions green (parent probe.py, exit 0); no live-seats residue", "result": "HOLD -- R-EF51 M1 closed at the push-OK callers"}
  - {"conjunct": 1, "class": "gate", "cmd": "parent hermetic probe C: same authority-deferred pending -> rotate._complete_pending_key_swap(tmp, seat) with NO authority line (the direct site :19101 shape)", "expected": "key swap NOT completed naming AUTHORITY; key byte-identical", "observed": "PASS C1-C2; the direct call site is gated too", "result": "HOLD -- the direct completion cannot bypass the authority gate"}
  - {"conjunct": 1, "class": "gate", "cmd": "parent PRE-FIX falsification on the raw git blob 15251fdc28 (importlib-loaded prefix_rotate.py): same authority-deferred pending + push OK/no-authority", "expected": "pre-fix bytes COMPLETE the swap (bug present); post-fix refuses", "observed": "PRE-FIX completed the swap (key swapped, pending deleted) = PROBE-CONFIRMS-BUG; post-fix refuses (probe A)", "result": "HOLD -- red on pre-fix bytes, green on the built bytes"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent hermetic probe D: rotate._apply_successor_key_gated with the push leg line \"push: HELD -- merge-up push is a gated act\"", "expected": "key_replace NOT applied naming push; <seat>.key byte-identical; pending persisted with deferred_for==push", "observed": "PASS D1-D4; pre-fix blob FLIPPED the key under push: HELD = PROBE-CONFIRMS-BUG", "result": "HOLD -- R-EF20 M1 closed and red on pre-fix bytes"}
  - {"conjunct": 1, "class": "wire", "cmd": "parent positive controls (gate not a wall): push-deferred pending + push OK completes; authority-deferred + \"authority: OK\" completes; authority:FAILED line does not complete", "expected": "back-compat completion preserved; only a successful publish completes an authority deferred", "observed": "PASS E1/E2/B1-B2", "result": "HOLD -- the gate defers only the unpublished case"}
production_lines: 49
profile: balanced
role: kid
scaffold_hash: 0a4772e69e0768c5
season: 2
title: "The authority-deferred pending key swap refuses every push-OK site and push: HELD defers by name"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1e0038eb-9722e7

## Experiment

Built the EF.67 fix in `extensions/agi/bin/rotate.py` closing R-EF51 M1 and
R-EF20 M1/M2. One gate, no per-call-site copy:

| # | change | defect closed |
|---|---|---|
| 1 | `_persist_pending_key(key_rotation, key_path, deferred_for="push")` writes `deferred_for: "push"\|"authority"` into the `.key.pending` JSON | records WHY the swap was deferred |
| 2 | `_complete_pending_key_swap(root, seat, authority_line=None)` refuses BY NAME when `deferred_for == "authority"` and no non-gating authority line is supplied (key byte-identical); `push`/legacy pending keeps push-only completion | R-EF51 M1 |
| 3 | `_finish_pending_swap_on_push` passes its `authority_line` THROUGH to `_complete_pending_key_swap`; the push-OK sites (:18767/:18888/:18924) and the direct call (:19065) pass none -> an authority-deferred pending is not completed on the trunk row alone | R-EF51 M1 |
| 4 | `_apply_successor_key_gated`: `_push_gated = _push.startswith(("push: FAILED", "push: HELD"))`; the persisted `deferred_for` is `_why` | R-EF20 M1 |

`authority_line` is non-gating exactly when `_authority_publish_gates_swap`
is False (OK, or a non-attempt SKIPPED), so EF.56's `authority: SKIPPED`
completion is preserved.

## Evidence

New file `extensions/agi/tests/test_rotate_pending_swap_authority.py` (5
tests): (a) authority-deferred pending survives both
`_finish_pending_swap_on_push(root, seat, "push: OK")` and the direct
`_complete_pending_key_swap(root, seat)`, key byte-identical, refusal names
AUTHORITY; (b) `push: HELD` defers in `_apply_successor_key_gated` and the
pending records `deferred_for == "push"`; (c) push-only + legacy pending
still complete, `authority: SKIPPED` does not gate; (d) frozen-path: push
HELD, authority FAILED, authority HELD, push-OK-without-authority, direct
completion all leave the successor key bytes FROZEN.

RED before the fix (pre-fix source reconstructed by string-reverting the two
defects, no git, script `.agi/sessions/iter-EF.67/a00-1e0038eb/redcheck.py`):

```
RED(pre-fix) test_authority_deferred_pending_not_completed_by_push: key swap completed (deferred from gen 7)
RED(pre-fix) test_push_held_defers_in_apply_successor_key_gated: key_replace: wrote successor key ... bb.key
GREEN(pre-fix, unexpected) test_push_deferral_still_completes_on_push_ok
RED(pre-fix) test_gated_paths_leave_successor_key_bytes_frozen:
GREEN(pre-fix, unexpected) test_authority_ok_completes_an_authority_deferred_pending
pre-fix failures: 3/5
```

The two pre-fix green cases are the deliberate positive controls: (c) is the
back-compat contract, and the authority-OK test proves the gate is a gate,
not a wall.

GREEN after the fix (`env -u TMUX -u TMUX_PANE python3 -m pytest`):

```
test_rotate_pending_swap_authority.py 5 passed
required + regression files: 413 passed, 1 xfailed
(test_rotate_pending_swap_authority.py test_rotate_key_authority.py
 test_rotate_rename_pending_swap.py test_rotate_prepare.py
 test_rotate_alert_two_tree.py test_rotate.py)
```

Production diff: `git diff --numstat -- extensions/agi/bin/rotate.py` = 49
added / 13 deleted.

## Agent Notes
<!-- filled by cli.py done -->

## Agent Notes
Built the EF.67 authority/push deferral gate in rotate.py (deferred_for in the pending JSON; _complete_pending_key_swap refuses an authority-deferred pending with no non-gating authority line; _apply_successor_key_gated treats push: HELD like push: FAILED). New test_rotate_pending_swap_authority.py: 3/5 RED on reconstructed pre-fix bytes, 5/5 green on built bytes; required rotate suites 413 passed/1 xfailed. production_lines 49.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) WHAT THE INSTRUCTION SAID: the node testable_claim demands that _complete_pending_key_swap and every _finish_pending_swap_on_push caller complete a pending successor-key swap only when the authority leg was published or no publish was attempted, never on the trunk row alone; and that _apply_successor_key_gated treats push: HELD as not published -- each proved by a committed test red on the pre-fix bytes. (2) WHAT THE MACHINE DOES: read on the kid diff (aeb346dfb1 vs 15251fdc28): _persist_pending_key now writes deferred_for (rotate.py:17371-17377); _complete_pending_key_swap gained authority_line and refuses an authority-deferred pending by name when the line is None or gating (rotate.py:17434-17445); _finish_pending_swap_on_push threads authority_line through (rotate.py:17545-17546) so the no-authority sites :18803/:18924/:18960 and the direct :19101 defer; _apply_successor_key_gated gates push HELD like push FAILED and persists _why (rotate.py:17586, 17618). I RAN the changed bytes myself in a hermetic tmp project (parent probe.py, 13/13 exit 0): an authority-deferred pending is refused at the push-OK/no-authority shape, at the direct call, and under authority:FAILED; push: HELD defers and records deferred_for=push; push-deferred and authority+OK still complete. I ALSO loaded the raw pre-kid blob (git show 15251fdc28:.../rotate.py) as an independent module and RAN the two decisive cases: pre-fix COMPLETED the authority-deferred swap (bug present) and FLIPPED the key under push: HELD -- so the new tests are genuinely red on the pre-fix bytes. (3) THE NEAR MISS: a fix that only threads authority_line into _finish_pending_swap_on_push but leaves the pushed reason unrecorded would pass a same-process re-key test and still lose R-EF51 M1, because the NEXT rotate carries no authority context for the earlier deferral -- the pending file would not know it was authority-blocked; the kid avoided exactly that by recording deferred_for and consulting it in the one completion gate. A second near miss: treating push: HELD via the existing _push.startswith("push: FAILED") would satisfy the words and keep flipping under a gated push. (4) NO DEVIATION: I added probes: to the kid node through write.py, not by hand; I did not re-run the kids suite as evidence. CAVEAT recorded in probes: a LEGACY pre-fix pending carries no deferred_for and reads push-deferred, so it can still complete on a later trunk push -- that is the documented back-compat choice, and the claim is scoped to pendings persisted after the fix.
<!-- THOUGHT:END -->

REVIEWED by tier-parent a00-f0258525 (EF.67): accepted. Bytes read from the kid diff (aeb346dfb1 vs 15251fdc28) -- rotate.py +62/-13, new test_rotate_pending_swap_authority.py (5 tests), kid node. Parent negative probes (5, hermetic tmp project): 3 gate + 1 wire on conjunct 1 (authority-deferred pending refused at the push-OK/no-authority shape and at the direct call; pre-fix blob CONFIRMED completing it) and 1 gate on conjunct 2 (push: HELD defers by name, deferred_for=push; pre-fix blob CONFIRMED flipping). 13/13 assertion probes green; positive controls preserve back-compat. Caveat: a legacy pending with no deferred_for still completes on a later trunk push (documented back-compat, outside the post-fix claim).
