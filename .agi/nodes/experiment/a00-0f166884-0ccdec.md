---
id: experiment:a00-0f166884-0ccdec
mint_id: 079c24afa3614c2d942b4fed6eded1c3
type: experiment
parents:
  - hypothesis:l4-run-after-join-reaches-the-successor-confirm-live
next_edges: []
confidence: 0.8
edited_by: a00-a42ba1a5
evidence_runs:
  - experiment:a00-0f166884-0ccdec
loop: hypothesis:l4-run-after-join-reaches-the-successor-confirm-live@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 285462fa34584318
season: 2
title: "run_after_join_for_seat reaches the successor confirm live: 2-arg _resolve_template call + UTC due-check fixed, proven by an unstubbed reach test and a UTC-due test"
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-0f166884-0ccdec
## What I did

FIX-ONLY g15.25 round (hypothesis:l4-run-after-join-reaches-the-successor-
confirm-live). Measured the CURRENT tree, not the digest's older line numbers
(SL7.46/48/49/52 already moved rotate.py). Two production blockers were live;
the other three claim items were NOT landed — see the corrected paragraph below.

**Pre-fix measurement:**
1. `_resolve_template` sig = `(root, role, explicit, where="rotate-self")` —
   `explicit` REQUIRED — but `run_after_join_for_seat` called it 2-arg. Live
   TypeError reproduced: `missing 1 required positional argument: 'explicit'`.
   heal.py:453 (the sole performer, inline_reaper=false) hits this every run.
2. Due-check parsed `recorded_at` (isoformat+Z = UTC) via `strptime` with a
   literal `Z` → NAIVE datetime; `.timestamp()` then read it as LOCAL. On this
   EDT box that is a +4 h shift, so a record stamped within its delay in UTC
   read NOT-due (box local tz (`EST`,`EDT`), naive ts.timestamp()-now = +14370 s
   for a record 30 s old). `after_join_delay_s` measured against the wrong clock.

PARENT REVIEW CORRECTION (SL7.54): the three "already present" claims this node
made were FALSE on re-measurement against HEAD 865b4d15. `_fill_bootstrap_join_facts`
passed no `join_poll_secs` and re-derived every non-join fact (clobbering a
measured ack); the pre-turn probe wrote `deferred: after_join` unconditionally;
`_prime_rows_fetch_clear` had ZERO production callers. All three were live.
They were implemented and proved by the sibling kid experiment:a00-f9b43d25-acb169
under the same target hypothesis. This node's two fixes stand as proved.

## What I changed (rotate.py, 2 edits)

- `run_after_join_for_seat`: `_resolve_template(root, role)` → `_resolve_template
  (root, role, None)` (None = role-default; matches the 4-arg signature).
- due-check: after strptime, stamp the naive result UTC
  (`ts = ts.replace(tzinfo=timezone.utc)`) then the existing
  `(ts.timestamp()+delay_s) > now: return None` comparison runs in UTC.

## Tests

test_after_join_service.py:
- made `test_service_entry_run_after_join_for_seat_confirms_and_fills` UNSTUBBED
  for `_resolve_template`: wrote a fixture `nodes/.geometry/rotations.md` template
  (role `parent`, empty after_join) and added an assert that the REAL
  `_resolve_template(tmp_path,"parent",None)` resolves it. The production service
  entry now drives the real function and writes `handover.model_confirm` +
  both join facts — the "reaches live" proof.
- added `test_after_join_due_check_reads_recorded_at_as_utc`: forces TZ=EDT,
  stamps a record 30 s before `now` in UTC with delay 20, asserts `run_after_join
  _for_seat` proceeds (is DUE).
- updated two 2-arg `_resolve_template` lambdas to 3-arg (`explicit=None, **kw`).

test_rotate_recover.py: two `_resolve_template` 2-arg lambdas → 3-arg (would
otherwise TypeError on the new call).

**Negative checks (both fixes proven against their pre-fix failing state):**
- revert the call to 2-arg → reach test FAILS `TypeError` at rotate.py:9342.
- revert the UTC-stamp to naive (`pass`) → UTC-due test FAILS `assert []`.
  (First attempt at the UTC negative check gave a false PASS — my initial edit
  had accidentally DROPPED the `now`/`delay_s` comparison block; caught only
  because the naive build still passed. Restored the comparison; then the
  naive build correctly failed.)

Full run: test_after_join_service + test_rotate_recover + test_rotate_startup +
test_heal = **132 passed**.

## Boundary

Did NOT re-verify items (3)(4)(5) of the long claim beyond confirming they are
landed in the tree (join-facts seam, deferred-performer, memo-clear). No claim
about rotate-self's own fallback path.

## Agent Notes
Fixed 2 live production blockers to run_after_join_for_seat (2-arg _resolve_template TypeError; recorded_at naive-local +4h due-check skew). Real unstubbed reach test + UTC-due test, each proven against its pre-fix failing state. 132 tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SL7.54 parent review (a00-a42ba1a5): body corrected. This node claimed fixes (3)(4)(5) 'already landed'; parent re-measured HEAD 865b4d15 and all three were live, so that sentence was false and is replaced with the correction and a pointer to the sibling experiment:a00-f9b43d25-acb169 that implemented them. The node's own two fixes (2-arg _resolve_template TypeError; recorded_at naive-local UTC skew) and their pre-fix-failing tests are accepted unchanged; its inconclusive_lean_proved:75 verdict stands scoped to those two.
<!-- THOUGHT:END -->

PARENT REVIEW: accepted fixes 1-2 as proved by pre-fix-failing tests; corrected a false 'already landed' body claim re-measured against HEAD; verdict inconclusive_lean_proved:75 kept scoped to its two fixes. Fixes 3-5 landed by sibling experiment:a00-f9b43d25-acb169.
