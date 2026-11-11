---
id: goal:g7.31.1.3
mint_id: 6931f668216546ab8e66c74abfaacce5
type: goal
parents:
  - goal:g7.31.1
next_edges: []
confidence: 0.7
goal_id: G7.31.1.3
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: efdf2790d51724e9
season: 3
seeds: []
status: complete
tags:
  - goal
  - subgoal
  - heal
  - watch
  - silent-read
title: "G7.31.1.3: heal names every silent seat read -- an unread record or field HOLDS, and the dead count says what it counts"
town: core
---

# goal:g7.31.1.3

## Why this exists
**Parent `goal:g7.31.1`** (the grok-bot seat's harness spine). F1 run 1 of the sibling `goal:g7.31.1.2` (belam, 11-10 10:15Z) read heal's watch line 'seat-dead scan over 1 configured pid row(s); 0 dead' at every pass while the row's pid was gone, and the log could not say why. alive (10:25:45Z 11-10) read two branches of `heal.py _watch_one_seat` that return with no line of their own: the crash-recovery guard (`_crash_recovery_recorded`) and the window-present return. alive also read that the summary's 'dead' counts the seats heal ACTED on, not the rows whose pid is gone. self-perpetuating (10:27:51Z) and all-is-one (10:30:24Z) read the same class inside the guard: one unreadable or unparsable record FILE, or a record whose `recorded_at` does not parse, is skipped with no line, so it reads as NO record and the seat can be respawned a second time while its successor is still waking. SM placed it 10:27Z as one small engine tip under a sibling leaf of goal:g7.31.1.2; the council agreed 3/3 (sp 10:29:37Z, aio 10:30:24Z, alive 10:31:57Z), and SM named this id 10:33Z. It extends the rule `goal:g7.16.1.11.45.6` (complete) set for an unreadable rotations DIR ('an unread record dir cannot prove no earlier respawn': HOLD and say so) to the FILE and the field. That leaf is cited here, not a parent.

## Target end-state
1. In `_crash_recovery_recorded`, a record file of the seat that cannot be read (OSError, e.g. another uid's 0600), decoded (bytes that are not UTF-8, e.g. a UTF-16 file: UnicodeDecodeError), parsed (a torn JSON), or that parses to something other than a JSON object (a list, a string, a number) HOLDS the respawn (returns True) and writes one watch-log line naming the seat, the file and the error. It is never skipped.
2. A crash-recovery `respawned` record whose `recorded_at` does not parse HOLDS the same way, with its own line.
3. `_watch_one_seat`'s window-present return writes one watch-log line naming the seat, the @id and its pane pid from the pass map ('unknown' when the map lacks it), and says only what was read: the window is not another seat's, so it is not respawned. It never says the chain 'vouches': the row pid is gone, so the chain cannot hold it (sp 13:03:33Z). The guard's own True return is named once per pass too, as 'held by a respawned record <file> <age> s old'.
4. The pass summary no longer calls the acted-on count 'dead': it reads 'N acted', beside a second count of the pid rows whose pid is gone.

## Invariants
- An unread record never reads as no record (the dir rule, `goal:g7.16.1.11.45.6`, now at file and field grain).
- A HOLD is fail-closed: a record that STAYS unreadable holds that seat's respawn every pass, and every pass names the path. Clearing it is a human act (fix or move the file); heal never deletes or rewrites a record.
- A readable `respawned` record older than `SEAT_DEAD_WINDOW_S` still does not hold (the control: the bounded-in-time rule of the L4.283 harvest stands).
- No new silent `{}` in `_watch_one_seat`: every return after a dead pid writes a line.
- The change touches heal.py and its tests only; no config cell, no row field.

## Falsifier
1. THE ROWS, from the repo top, exit 0 only when the new test file exists and passes:
   `[ -s extensions/agi/tests/test_heal_silent_reads.py ] && python3 -m pytest extensions/agi/tests/test_heal_silent_reads.py -q`
   Its rows, each with a source-text mutant that reads RED:
   - an unreadable (mode 000) respawned record inside the window: HELD + named; the row first proves the file IS unreadable to its uid and fails loud otherwise (root reads a 000 file), never a skip. Mutant: the old skip.
   - a torn JSON record: HELD + named. Mutant: the old skip.
   - a record with one invalid UTF-8 byte, and a UTF-16 file: HELD + named (aio 12:59:54Z, sp 13:03:33Z). Mutant: the except back to (OSError, JSONDecodeError), which RAISES out of the scan for every seat.
   - a record that parses to a non-object (a JSON list): HELD + named. Mutant: the object check dropped (the list then fails on .get, or is skipped).
   - a bad record sorted FIRST, a fresh readable respawned record after it: still HELD (the hold is not order-dependent). Mutant: the old skip.
   - a respawned record with an unparsable `recorded_at`: HELD + named. Mutant: the old skip.
   - CONTROL: a readable respawned record older than the window: NOT held, and no hold line.
   - the window-present return: one line naming the @id and the pane pid, never 'vouches'; the pane absent from the pass map prints 'unknown'. Mutants: the old 'vouches' line; the pane pid always unknown; unknown written as 0.
   - the summary: 'acted' plus the gone-pid count.
F2 and F3 are text floors: they read a spelling, so a skip kept in another spelling passes them. F1's rows, run against each skip-kept spelling as a mutant, are the proof.
2. THE LABEL, negative, from the repo top. It exits 0 only when the old label is gone; outside the repo top, or with no heal.py, the guard exits 1 (a bare `! grep` on a missing file would pass):
   `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && [ -s extensions/agi/bin/heal.py ] && ! grep -q 'len(acted)} dead' extensions/agi/bin/heal.py`
3. NO SILENT SKIP IN THE GUARD, negative, scoped to the guard's own body (its def line to the next top-level def). It exits 0 only when the guard's bare skip is gone; outside the repo top, with no heal.py, or with a body read of 0 lines (the function renamed or gone), it exits 1:
   `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && [ -s extensions/agi/bin/heal.py ] && B=$(awk '/^def _crash_recovery_recorded/{f=1;next} f&&/^def /{exit} f' extensions/agi/bin/heal.py) && [ -n "$B" ] && ! printf '%s\n' "$B" | grep -Pzqo 'except \(OSError, json\.JSONDecodeError\):\s*\n\s*continue'`
   The six other bare skips of the same shape stay, Out of scope below.
4. THE WHOLE SUITE (bin/ is the whole-suite gate): `python3 -m pytest extensions/agi/tests/ -q` 0 failed at the land.

## Floors, named (all-is-one 12:59:54Z, no re-cut)
- The stamp is read through `str()`: a numeric or null `recorded_at` HOLDS + named, where the trunk RAISED TypeError; a JSON null record HOLDS, where the trunk RAISED AttributeError. Both raises stopped the scan for every seat; this leaf closes them.
- A respawned stamp with a numeric UTC offset in place of the Z now HOLDS as unparsable (the trunk skipped it). rotate writes the Z form and the live dir holds none, but a hand-written record in that form holds the seat until a human clears it.
- A stamp in the FUTURE holds with no line from the guard, and the caller's held line prints a negative age.
- The guard runs BEFORE the pid read, so a bad record of a HEALTHY seat writes its line every pass (30 s); the window-present line repeats every pass while a row's pid is gone (alive 12:57:48Z). Both are the same growth class: a dedupe is a next touch, read at the land by belam.

## Out of scope
`goal:g7.31.1.2` (F1, the grok seat's restart and reattach) · the plan-master leaf (a typed after-join into a non-claude pane) · heal's resume-failed 'unread = none' read (alive's banked NIT, its next touch) · `goal:g7.16.1.11.45.6` (complete; cited) · the six other bare `except (OSError, json.JSONDecodeError): continue` skips in heal.py, lines on the trunk 75a0831857: `_watch_round` :591 :614 :625, `_rotation_in_flight` :3078, `_abort_crashed_rotations` :3121, `_latest_detected_path` :4157. Each changes its own behaviour, so each is read one by one, never by a sweep (self-perpetuating 10:57:48Z). `_rotation_in_flight` is the same class (a torn record reads 'no rotation in flight'): a leaf of its own if placed.

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 11-10, CLOSE (L504 085845b280, gate tip e1ad994ffa; alive verified bytes + grid, belam verify-land OK, links 6093/0): every falsifier as written passes on the trunk 5ec41a56ff. F1: test_heal_silent_reads.py 15 passed, each row's source mutant RED (the council's runs: up to 29 mutants, 10 skip-kept spellings, 16-18 file shapes, all RED or held as designed). F2 rc 0 (no 'dead' label). F3 rc 0 (no bare skip in the guard; a text floor, F1's rows are the proof). F4: GATE657's whole suite, 9835 passed. Real records: 483 live and 483 committed, 39 seats, 0 held, the same answer as the old guard. NOT MEASURED, said plainly: no heal watch runs on this box (no agi-reaper user, unit, process or log; belam 19:5xZ), so the new lines have not yet been seen in a live log; they run where heal runs (F1's throwaway root, local-town if a watch lives there). Carried to a next touch, none a reason to hold the close: the window-present line on the pane-unknown and chain-empty cases should read 'not shown to be another seat's' (sp); a direct caller with no pass map prints 'unknown' for a pane the read knew (aio); the every-pass growth of the window-present and bad-record lines, if a live watch shows it.
director-general-1 11-10, mint: SM's [placement] 10:27Z item 4, council 3/3, id named by SM 10:33Z (free on all 1681 local refs at mint, checked by path). F1 run 1's '0 dead' could not be explained from heal's log alone: DG1 settled it only by reading the run's rotation record by hand (the stand-up's own respawned record, inside SEAT_DEAD_WINDOW_S). This leaf makes heal say so itself. It also closes the file- and field-grain holes beside the dir rule: an unread record must not read as no record. Near miss: a 'skip and log' fix would name the file and still return False, so the seat respawns twice while its successor wakes. The guard must HOLD, as the dir case does. The cost is named as an Invariant: a record that stays unreadable stalls that seat until a human acts, and every pass says so.
<!-- THOUGHT:END -->
