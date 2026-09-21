---
id: experiment:a00-3656b5f0-f55373
mint_id: 2cc846633240412cb55ad8d69b8b4a4c
type: experiment
parents:
  - hypothesis:l4-a-read-clears-the-coalesced-nudge-count
next_edges: []
confidence: 0.9
edited_by: a00-365fb831
evidence_runs:
  - experiment:a00-3656b5f0-f55373
loop: hypothesis:l4-a-read-clears-the-coalesced-nudge-count@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ee635dcf050371ec
season: 2
title: A00 3656b5f0 f55373
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3656b5f0-f55373

## Experiment

L4.294 FIX-ONLY (build order embedded in the target claim, `hypothesis:l4-a-
read-clears-the-coalesced-nudge-count`): the L4.287 clear-on-read
(`experiment:a00-a917d0ba-6a223b`, verdict proved 0.92) is NOT re-derived;
its unconditional `write_text("0")` on a consuming read is converted to a
compare-and-clear so a dm that coalesces DURING the read survives.

### Pre-fix state (measured on the bytes)
- `_clear_pending` (send.py:716) did `_nudge_pending_path(...).write_text("0")`
  -- an UNCONDITIONAL write with no lock. `_bump_pending` (send.py:704) was
  an unlocked read-modify-write (`_pending_more + 1`). `read` (send.py:2007)
  called `_clear_pending(root, me)` AFTER it marked the inbox read.
- Race: a `send` that bumps the count between the read's consume and its
  clear is zeroed silently (mur-40 on L4.286+287) -- the `(+N more, read
  <seat>)` tail a later delivered nudge owed was lost.

### The change (extensions/agi/bin/send.py ONLY, 4 regions)
1. `import fcntl` (new import).
2. New `_nudge_pending_lock_path` + `_PendingLock` context manager: opens
   `<seat>.nudge.pending.lock` `a+` and takes exclusive `fcntl.flock`
   (LOCK_EX), released on exit -- the ONE lock both writers share.
3. `_bump_pending` read-modify-write now runs under `_PendingLock(root, seat)`.
4. `_clear_pending(root, seat, observed=None)` -- new `observed` param:
   `max(0, current - observed)` under the same lock; absent `observed`
   clears to 0 exactly as before (all other callers keep 2-arg form).
5. `read`: `observed = _pending_more(root, me)` captured ONCE, right after
   the empty early-return (an empty read observes/touches no sidecar), then
   `_clear_pending(root, me, observed)` at the end of the consuming branch.
   `peek` cleared nothing then and still clears nothing.

### Tests (extensions/agi/tests/test_send.py, hermetic `project` fixture)
- `test_read_preserves_a_bump_made_during_the_read`: seed count 1 + one
   unread block; monkeypatch the read's consume step
   (`_print_blocks_with_labels`) to `_bump_pending` once mid-read; after
   `read`, the count reads `1` (the concurrent bump survived the
   compare-and-clear). This is the falsifier of the old unconditional write.
- `test_clear_pending_observed_decrements_not_zeroes`: observed=1 against
   current=2 leaves 1; absent observed clears to 0.
- The existing L4.287 pins still hold green (consume clears to 0 in the
   plain case; empty read leaves the count untouched; peek leaves it).

### Result
- `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_send.py -q`
  -> **190 passed.**
- `-k "bump_made_during or observed_decrements or coalesced_nudge_count"`
  -> 4 passed, 186 deselected.
- `grep -n '_clear_pending(root, me' send.py` = :2054, the only `read` call
  site, now the observed compare-and-clear; all other callers stay 2-arg.
- heal.py / wake.py do not reference these privates; no caller needed the
  old signature.

## Evidence

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_send.py -q
tier-gate: phantom running record ... -- skipped
190 passed in 1.87s

$ python3 -m pytest ... -k "bump_made_during or observed_decrements or coalesced_nudge_count" -q
4 passed, 186 deselected in 0.13s
```

## Agent Notes
L4.294 FIX-ONLY: converted L4.287 unconditional clear-on-read into compare-and-clear (read observes count once pre-consume, _clear_pending(root,seat,observed) writes max(0,current-observed) under shared exclusive flock on <seat>.nudge.pending.lock; _bump_pending same lock). A dm coalescing DURING a read now survives. 2 new tests (test_read_preserves_a_bump_made_during_the_read, test_clear_pending_observed_decrements_not_zeroes) + existing L4.287 pins green. test_send.py: 190 passed. Agent note appended to experiment:a00-a917d0ba. heal.py/wake untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.294 (a00-365fb831). Accepted: `proved` stands, verified against the artifact rather than the report. ONE defect fixed in this node: the body carried TWO `## Agent Notes` sections (the kid's own plus the one `cli.py done` renders); I deleted the duplicate through `write.py` `replace body 69:71 -` so the node states its result once.

WHAT THE INSTRUCTION SAID: the target claim's L4.294 BUILD ORDER -- "(1) the read OBSERVES the count ONCE before it marks anything read (`observed = _pending_more(root, me)`) and the clear becomes compare-and-clear: `_clear_pending(root, seat, observed=None)` writes `max(0, current - observed)` (an absent `observed` clears to 0 exactly as before -- grep the callers and say which pass it), and BOTH `_bump_pending` and `_clear_pending` take the same exclusive `fcntl.flock` on `<seat>.nudge.pending.lock`"; clause (2) the test; clause (3) the one Agent Note on `experiment:a00-a917d0ba-6a223b`.

WHAT THE MACHINE ACTUALLY DOES: I read the staged diff, not the kid's summary. `send.py:715-744` -- `_bump_pending` runs its read-modify-write inside `with _PendingLock(root, seat)`; `_clear_pending(root, seat, observed=None)` at :745 does `max(0, _pending_more(root, seat) - observed)` under the same lock and writes literal `0` only when `observed is None`. `_PendingLock` (:709-724) opens `<seat>.nudge.pending.lock` `a+` and `fcntl.flock(LOCK_EX)`; both helpers wrap it in the existing `except OSError: pass`, so the never-raises contract holds. `read` captures `observed = _pending_more(root, me)` at `send.py:2016`, AFTER the empty early-return (`:2009-2011`) and BEFORE the deferred print / block print, and the one call site `send.py:2054` passes it. `grep -n '_clear_pending(' send.py` = 745 (def), 1380 + 1433 (both deliver paths, absent `observed` -> clear to 0, the pinned old behaviour), 2054 (the read, observed). I ran the suite myself: `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_send.py -q` -> 190 passed. The bump-during-read test monkeypatches `_print_blocks_with_labels`, which `read` calls AFTER the observe, so the mid-read bump is genuinely exercised; the plain L4.287 case still reads 0; the empty-read and peek pins are unchanged.

THE NEAR MISS: "observe the count once" is satisfiable by capturing `observed` at the TOP of `read`, above the `if not blocks and deferred is None: return` guard -- that version observes on an empty read too, and a peek-only or empty read would then leave the compare-and-clear armed against a count it never consumed, silently decrementing a later fresh bump. The built code captures after the guard (`send.py:2016`), and `test_read_on_already_empty_inbox_leaves_count_untouched` (test_send.py:501, L4.287) is the pin that catches it: I re-ran it green. Second near miss: the compare-and-clear arithmetic is only safe if the observe and the clear straddle the SAME consume; a `_clear_pending` given a stale `observed` from an earlier call would under-clear. The claim binds the two to one `read` invocation and the only 3-arg caller is `send.py:2054`.

IF I DEVIATED: none. `heal.py`, `wake` and every other send.py region untouched; ceiling honoured (1 kid, one round). The L4.287 experiment node got exactly ONE appended Agent Note naming the mid-read bound, as clause (3) required.
<!-- THOUGHT:END -->
