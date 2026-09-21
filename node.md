---
id: experiment:a00-72878506-1ba032
mint_id: 3252de2795ff437eaa576430b97f8157
type: experiment
parents:
  - hypothesis:l4-send-py-read-refuses-a-target-that-is-not-the-resolved-sender-and-peek-stays-open
next_edges: []
confidence: 0.8
edited_by: a00-0bec02e3
evidence_runs:
  - experiment:a00-72878506-1ba032
loop: hypothesis:l4-send-py-read-refuses-a-target-that-is-not-the-resolved-sender-and-peek-stays-open@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0e338cdb988a9e1f
season: 2
title: A00 72878506 1ba032
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-72878506-1ba032

## Experiment

BUILT the g15 claim (`hypothesis:l4-send-py-read-refuses-a-target-that-is-not-the-resolved-sender-and-peek-stays-open`) on `send.py` @42ce34503 (post-fix bytes).

**Pre-fix measure.** The dispatch (send.py 3829-3848) took the positional `target` of `read` and fed it straight to `read(root, args.target, sender, wrap)` -> `_inbox_path(root, target)` -> `READ_MARKER` written for ANY target. No check against the caller. `_detect_sender` (AGI_AGENT_ID -> AGI_SEAT -> --from -> `unknown`) never entered the decision.

**Change.** Added `_own_inbox_or_refuse(target, me)` wired into the `read` dispatch immediately before `read(...)`:
```python
resolved = _detect_sender(sender)
if not _own_inbox_or_refuse(args.target, resolved):
    return 2
read(root, args.target, sender, wrap=wrap)
```
The gate returns True only when `target == me and me != "unknown"`; otherwise it prints ONE stderr line naming both plus the three exact remedies (and the `--from <seat>` hint when the sender resolved to `unknown`), returning exit 2 BEFORE `read(...)` runs, so NO file is touched. `peek` never consults the gate. `--dm`/`--room` return earlier (un-gated, keyed by `me`). `--me` is never the gate input - the gate keys on `_detect_sender(sender)`, so `--me` cannot widen it.

**Clause (5) survey.** grep `send.py read` / `read_inbox` / `send.read(` across `extensions/agi/bin` and `hooks`: no engine caller invokes a consuming positional `read` on a foreign inbox. mail_alert uses non-writing `_scan_messages`/`_read_conv` (peek-equivalent); the `{seat}` command templates resolve to the caller's own seat; all other hits are help text, comments or the tests' own fixtures. No caller needed switching to `peek`.

**Tests.** 6 new in `test_send.py` (leak-guarded: each dispatch test `chdir`s into a fresh tmp project so the suite can never read the real checkout's `.agi/sessions`):
- `test_read_refuses_a_target_that_is_not_you` - rc 2, ONE stderr line naming both, both remedies present, marker + inbox bytes unchanged.
- `test_read_your_own_inbox_still_works` - rc 0, consumed (gate does not fire on the true self).
- `test_peek_stays_open_to_any_target` - foreign peek rc 0, prints body, marker untouched.
- `test_read_dm_and_room_untouched` - `--dm` partner still reads (un-gated).
- `test_read_unknown_sender_refused_with_from_hint` - unknown resolves, refused, `--from <seat>` hint present.
- `test_read_refuses_unknown_even_for_unknown_target` - `read unknown` by a senderless process refused (forces the `me != "unknown"` branch).

## Evidence

`python3 -m pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_seatsig.py extensions/agi/tests/test_sensei.py extensions/agi/tests/test_heal.py extensions/agi/tests/test_bin_help_smoke.py extensions/agi/tests/test_write_self_row.py -q` -> **371 passed, 3 skipped**. New-gate subset `-k "refuses or own_inbox or stays_open or dm_and_room or unknown"` -> 24 passed. No engine caller needed a `peek` switch (clause 5 verified by survey).

THOUGHT: the gate keys on `_detect_sender(sender)` because that is inbox identity; `args.me` names room/dm read positions and must not widen the gate (claim 4). The `me != "unknown"` disjunct makes claim 3 airtight: a senderless process can never consume even an inbox literally named `unknown`.

## Agent Notes
Built read position gate _own_inbox_or_refuse (refuse foreign positional read rc2, one line naming both+3 remedies; peek/--dm/--room/--me untouched; unknown sender refused always incl target 'unknown'); 6 leak-guarded tests; 371 passed incl neighbors; clause5 survey: no engine caller consumes foreign inbox, none needed peek switch.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-0bec02e3, SL7.13): accepted proved. I read the artifact, not the report: `_own_inbox_or_refuse` sits above read() and the positional branch gates on `_detect_sender(sender)` (never args.me), returning exit 2 with ONE stderr line and the three exact remedies, plus the --from hint when me==unknown; peek/--dm/--room are untouched. I re-ran the named suite myself on this tree: 371 passed, 3 skipped. The gate fires only for target != me, and `me != "unknown"` makes claim 3 airtight. GAP I found and re-cut to kid 2: the brief demanded a leak-detector fixture asserting MAIN .agi/sessions/inbox untouched, and this round delivered only per-test chdir. That is now built by experiment:a00-71afa7e6-dfd131.
<!-- THOUGHT:END -->
