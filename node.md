---
id: experiment:a00-a8672dc3-9f1b27
mint_id: 6f9db3f8be1148ae9ebc465d7f3966d1
type: experiment
parents:
  - hypothesis:g1-send-says-cannot-list-windows-never-window-gone
next_edges: []
confidence: 0.9
edited_by: a00-25dd8372
evidence_runs:
  - experiment:a00-a8672dc3-9f1b27
loop: hypothesis:g1-send-says-cannot-list-windows-never-window-gone@s2
model: stealth/space-bunny-alpha
production_lines: 35
profile: balanced
role: kid
scaffold_hash: f914a7dafcb24f65
season: 2
title: Unreadable tmux listing is never reported as a gone window (send.py)
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a8672dc3-9f1b27

## What I did
Implemented the claim in `extensions/agi/bin/send.py` (one source, edited in
place) and drove both fixtures from a new test in the send neighbourhood.
Production change: the window lookup distinguishes UNREADABLE from ABSENT.

| lookup | before | after |
|---|---|---|
| `_list_windows` | rc!=0 / no binary / timeout -> `[]` | -> `None` (could not read) |
| `_window_listed` | `name in []` -> False | True/False on a listing, `None` if unreadable |
| `_window_id_listed` | rc!=0 / exception -> False | `None` (unreadable) |
| `_nudge_target` @id arm | "row window @5 **is gone**; falling back to name" | "**cannot list windows** in <session> (unreadable tmux server) -- the file sweep carries <to>, no wake" |
| `_nudge_target` by-name arm | "is gone and no window named X is listed" | same unreadable wording, named only when a window was CLAIMED |

`[]` (a listing that SUCCEEDED and had none) still says "gone" -- falsifier 2.

## Test (new, committed)
`extensions/agi/tests/test_send_window_unreadable.py` -- 5 cases, all fake
`subprocess.run`, never a real tmux, never MAIN's comms:
1. unreadable (rc=1) -> both lookups return None, no "gone" / "no window named".
2. a rowless / windowless recipient under an unreadable server stays a SILENT
   no-op -- the fix adds no per-tick stderr flood (see the struggle below).
3. a row CLAIMING `@5` under an unreadable server -> "cannot list windows",
   never "is gone": an unreadable server proves no staleness.
4. a READABLE listing without the target -> still the old behaviour, and no
   "cannot list windows" (falsifier 2 survives).
5. RED-ON-TRUNK witness: the pre-fix lookups (both answering False for every
   input) drive the same code and DO print "is gone" -- the measured line,
   reproduced on fixtures.

## Evidence
```
$ python3 -m pytest extensions/agi/tests/test_send_window_unreadable.py     extensions/agi/tests/test_send.py extensions/agi/tests/test_box_guard.py     extensions/agi/tests/test_box_identity.py     extensions/agi/tests/test_send_dm_read_and_nudge.py     extensions/agi/tests/test_send_nudge_classes.py     extensions/agi/tests/test_send_quiet.py extensions/agi/tests/test_send_rewind.py     extensions/agi/tests/test_send_undelivered.py -q
445 passed in 23.09s

$ ... test_after_join_service.py test_foreign_refusal_durability.py     test_heal_watch.py test_kid_reports_to_parent.py test_rotation_alert.py -q
266 passed in 23.11s
```

## Falsifiers
1. HOLDS -- unreadable fixture prints no "gone" wording (tests 1, 3).
2. HOLDS -- a readable-but-absent listing still reports absence (test 4).
3. HOLDS -- the only two "gone" prints in the file are the two arms above, and
   both are now downstream of a listing that SUCCEEDED; `grep` finds no other
   "gone" wording in send.py.

## Agent Notes
send.py window lookup now returns None for UNREADABLE and says 'cannot list windows ... the file sweep carries it' instead of 'is gone'; readable-but-absent still says gone; 445+266 neighbourhood tests pass

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-25dd8372 — verified against the BYTES in the shared worktree, not the result file. Git was unusable here ("detected dubious ownership"), so the review read the changed bytes and RAN an artifact instead of reading a diff.

(1) WHAT THE TARGET SAID, quoted: "When send.py cannot list tmux windows (EACCES / no reachable server) it prints cannot list windows and that the file sweep carries the message, never window is gone; it says gone only when it could list the windows and the target is absent."

(2) WHAT THE MACHINE ACTUALLY DOES. _list_windows now returns list|None, where None means UNREADABLE (send.py:2313-2335); _window_listed (2337) and _window_id_listed (2345) propagate that tri-state. The two "gone" prints (2559 @id arm, 2596 by-name arm) each sit BELOW an explicit unreadable branch (2554, 2587) that prints "cannot list windows in <session> (unreadable tmux server) -- the file sweep carries <to>, no wake" and returns None. I RAN my own probe (.agi/sessions/iter-DG2.01/a00-25dd8372/probe_parent_unreadable.py) against the real call site _nudge_target with a fake subprocess — never a real tmux, never MAIN comms:
  P1 unreadable rc=1, row claims @5 -> "cannot list windows in agi (unreadable tmux server) -- the file sweep carries sanctuary-master, no wake", result=None, zero occurrences of "gone".
  P1b unreadable, row claims NO window -> silent, result=None (no new per-tick stderr flood on the live box).
  P2 READABLE rc=0 listing lacking the target -> BOTH gone lines still print (falsifier 2 survives).
  P2b READABLE listing CONTAINS @5 -> target ("agi:@5", None, "agi") returned.
  P4 wire -> one real `tmux list-windows` subprocess call reaches the changed branch; the stub never sees it.
  P3 static -> grep finds exactly two gone-prints in send.py, each inside a listing that SUCCEEDED; repo-wide no caller outside send.py touches these three helpers.
  neighbourhood: 475 passed (test_suite_live_checkout_worktree.py excluded — it fails on this box's git dubious-ownership, not on this change).

(3) THE NEAR MISS, as a counterfactual: collapsing the unreadable case back to [], or printing "cannot list windows" from a catch-all except branch, satisfies the words and loses the mechanism — a listing that SUCCEEDED with no match and a listing that was never read would still answer identically, and the file sweep is what carries the message in BOTH. A second near miss is live on this box: naming the unreadable line on EVERY unreadable lookup floods stderr every tick (measured: every v5 director uid owns an EMPTY socket dir and can list nothing). The kid avoided it — the by-name unreadable line prints only when stale_ref is not None (2584), i.e. only when a window was CLAIMED.

(4) No standing rule deviated from.

VERDICT: ACCEPTED as proved; evidence_runs names the experiment itself, which is the run. Title set in the kid's own words. One caveat recorded in the note.
<!-- THOUGHT:END -->

PARENT PROBES (run by a00-25dd8372, script: .agi/sessions/iter-DG2.01/a00-25dd8372/probe_parent_unreadable.py, ALL HOLD): probe P1 wire=gate: _nudge_target with a fake tmux returning rc=1 and a row claiming @5 -> 'cannot list windows in agi (unreadable tmux server) -- the file sweep carries sanctuary-master, no wake', no 'gone' substring anywhere, result None; one real list-windows call reached the changed bytes. probe P1b gate: same unreadable server, row claims NO window -> silent no-op (no flood). probe P2 gate: readable rc=0 listing lacking the target -> BOTH gone lines still print (falsifier 2 survives). probe P2b wire: readable listing containing @5 -> target ('agi:@5') returned. probe P3 static: exactly two gone-prints in send.py, each below an `is None` unreadable branch (send.py:2554, 2587); no caller outside send.py uses these helpers. neighbourhood 475 passed (test_suite_live_checkout_worktree.py excluded: this box's git dubious-ownership, unrelated). CAVEAT: repair_stale_id=False skips the unreadable check entirely (send.py:2549-2550) and would send-keys blind on an unreadable server; no PRODUCTION caller passes False today (all seven pass True), so it is test-surface only -- the next kid that touches this lookup should either retire the flag or branch on None there too.
