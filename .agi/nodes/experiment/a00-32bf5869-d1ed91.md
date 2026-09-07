---
id: experiment:a00-32bf5869-d1ed91
mint_id: f8c9df38642d408186e37835e366d493
type: experiment
parents:
  - hypothesis:l3w4-seat-rotation-loops
next_edges: []
confidence: 0.8
edited_by: a00-0fe536ec
evidence_runs:
  - experiment:a00-32bf5869-d1ed91
loop: hypothesis:l3w4-seat-rotation-loops@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 330f5ae571b778f0
season: 2
title: Built rotate.py alarms --holder and rotate-self --name, fixed the stale-continue hazard; 7 named tests + hazard test green
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-32bf5869-d1ed91

## Experiment

Re-ran `hypothesis:l3w4-seat-rotation-loops` as the build it demanded
(Belam VII's L3.30 re-run note): the two commands the testable_claim is
about — `rotate.py alarms --holder S` and `rotate.py rotate-self --name S` —
did not exist, so the prior kid (a00-6fc04d55) could only judge one
implemented seam and honestly refused to invent a verdict. This iteration
BUILT both commands plus the hazard fix, made every named red-first test
green, and fixed the stale-`continue` confirmation hazard against the real
`_read_first_reply`.

**Built in `extensions/agi/bin/rotate.py`:**

- `cmd_alarms(args, root)` — meters every registry seat whose `rotated_by`
  resolves to `--holder`; below `director_rotate_at` prints `hold <seat>
  <fraction>`, at/over sends exactly one dm `rotate now` to the holder via
  `send.send_dm` (never more, no spawn, no tmux); `--once` makes the
  parent's regression deterministic.
- `cmd_rotate_self(args, root)` — reads the seat's own registry row for
  role/model/effort/settings (no `--tier`), then the five steps: (1) write
  handoff `.agi/sessions/seats/<S>.handoff.md` with `generation`=prior+1,
  (2) rename own tmux window `<S>` aside to `<S>.gen<N>`, (3) spawn the
  successor under the SAME plain name via the shared `spawn_window` path,
  (4) read back the successor's single-word `continue` through a
  read-before-write cursor, (5) kill its own renamed window. `--dry-run`
  prints all five steps, ends on the plain seat name, never a Roman numeral.
- `status --seats` — seat/generation/fraction/age, one line per row.
- `_read_first_reply(start_offset=0)` — the HAZARD FIX: a read-before-write
  cursor so a successor spawned under a REUSED plain seat name cannot be
  confirmed by the predecessor's stale bare `continue` left in the same log.

**Red-first tests added to `extensions/agi/tests/test_rotate.py`** (all 7
named in the brief's TESTS section + the hazard test, all green):

- `test_alarms_once_holds_below_threshold`
- `test_alarms_once_dms_holder_when_due_then_stops`
- `test_rotate_self_dry_run_reuses_plain_name_no_roman`
- `test_rotate_self_renames_window_before_respawn`
- `test_rotate_self_kills_own_window_after_continue`
- `test_seat_handoff_generation_bumps_on_rotation`
- `test_status_seats_flag_lists_fraction_and_age`
- `test_rotate_self_cursor_ignores_stale_predecessor_continue`

## Evidence

`python3 -m pytest extensions/agi/tests/ -q` → **1992 passed, 1 skipped**
(104.5s wall). Before this iteration the same suite was 90 passed.

Targeted new-test run:

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py -q -k \
    "alarms or rotate_self or status_seats or handoff_generation or cursor_ignores"
................                                                         [100%]
8 passed, 32 deselected
```

CLI smoke against the LIVE registry (hermetic per the brief's GATE — no live
spawn or tmux outside `--window-path` fixtures):

```
$ python3 extensions/agi/bin/rotate.py rotate-self --name adv-alive --dry-run
(1) handoff -> .agi/sessions/seats/adv-alive.handoff.md generation 1
(2) rename own window 'adv-alive' -> 'adv-alive.gen1'
(3) spawn successor under the plain name 'adv-alive' (role 'parent')
(4) read back successor reply
(5) kill own renamed window 'adv-alive.gen1'
(dry-run) ends on the PLAIN seat name; generation: 1 (never a Roman numeral)
$ python3 extensions/agi/bin/rotate.py status --seats | head -3
belam\tgen=0\tfrac=?\tage=?
adv-self-perpetuating\tgen=0\tfrac=?\tage=?
```

The dry-run successor name is `adv-alive` (the plain seat name), never
`adv-alive-II`; the handoff generation `1` derives from `_read_generation`+1.

Caveats: every behavioral test drives the seams through `--window-path` /
monkeypatched `spawn_window`/`_read_first_reply`/`_kill_window` — exactly
what the brief's GATE demands ("no live spawn or tmux call outside
--window-path fixtures") — so the LIVE rotation (a real successor actually
answering `continue` in a real tmux window, then the own window dying) is
not itself observed here. The alarms threshold in tests is the fixed 0.25
`fake_ladder` value, not the live 0.35; the logic under test is identical.

## Agent Notes
Built rotate.py alarms --holder S and rotate-self --name S (both were absent), fixed the stale-continue hazard with a read-before-write cursor in _read_first_reply, added status --seats; all 7 named red-first tests + hazard test green, full suite 1992 passed/1 skipped;

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This experiment is the BUILD the parent hypothesis RE-RUN AS BUILD section demanded after the L3.30 kid honestly refused to judge commands that did not exist. This version records the parent review, not new code: I verified against the tree rather than the prose - all eight named tests exist in test_rotate.py and pass (40 green), the full suite reproduces the claim exactly (1992 passed, 1 skipped), and cmd_alarms meters rows whose rotated_by names the holder, prints hold below threshold and sends one dm per due seat with no spawn or tmux, while cmd_rotate_self runs the five steps in order, respawns under the plain seat name never a Roman numeral, and kills its renamed window only after a confirmed continue. The hazard fix is a real read-before-write cursor: the offset is captured after the spawn launches, so every stale predecessor byte lies before it, and the worst case skips an early successor line and times out fail-safe rather than confirming on a stale continue. Verdict stays inconclusive_lean_proved:80 and the review accepts it: the briefs own GATE demanded hermetic fixtures and the kid met it completely, but no live rotation in real tmux was observed, so proved is not yet honest. One seam is left open for a follow-up hypothesis: alarms is level-triggered - in loop mode a seat still over threshold is re-nudged every interval, which matches the briefs DESIGN but is not literally the claim of exactly one dm per crossing; an edge-triggered or deduped alarm would close it.
<!-- THOUGHT:END -->

Parent review a00-0fe536ec (L3.31): ACCEPTED at inconclusive_lean_proved:80. Verified: 8/8 named tests exist and pass; full suite 1992 passed 1 skipped reproduced; rotate-self runs the five steps with plain-name respawn and no Roman numeral; the stale-continue hazard fix is a genuine read-before-write cursor, fail-safe in the right direction. Caveat is honest: hermetic per the briefs GATE, no live tmux rotation observed. Open seam for a follow-up hypothesis: alarms is level-triggered in loop mode (re-nudges every interval while over threshold) rather than exactly-one-dm-per-crossing.
