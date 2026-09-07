---
id: hypothesis:l3w4-seat-rotation-loops
mint_id: 75eb63960ff947eabc3594bb117c4365
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-VII
scaffold_hash: a60602af9b37d566
season: 2
testable_claim: rotate.py alarms --holder S sends exactly one dm to a seat only when that seat's pin crosses director_rotate_at (0.35), and rotate.py rotate-self --name S then writes the seat's handoff with an incremented generation, renames its own tmux window, spawns its successor under the identical plain seat name (never a Roman numeral), reads back the successor's single-word continue, and kills its own renamed window before returning.
thought_session: 7af11157
title: L3w4 seat rotation loops
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-seat-rotation-loops

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

Every non-prime seat rotates itself at `director_rotate_at` (0.35) once nudged, not by self-polling: `rotate.py alarms --holder S` meters each seat whose row names `S` as `rotated_by`, and when due sends one dm "rotate now" — nothing more. The nudged seat runs `rotate.py rotate-self --name <seat>`: writes its handoff, renames its own window aside, spawns its successor under the SAME plain name, reads back `continue`, kills its renamed window. `generation:` lives in the handoff; only the prime keeps a Roman numeral.

## WHY

Owner (1): "perpetual rotation loops … without the Roman numeral convention"; "setting alarms … talking to each one when it's time"; "They keep him respawned by helping track parts of the handoff … doing the rotation together"; "Each layer lasts longer and longer in theory." Gloss "Seat lifecycle": advisors rotate the directors, the quorum rotates the liaison.

## FILES

extensions/agi/bin/rotate.py :: cmd_loop, _successor_command, _launch_window, _read_first_reply, _check_branch_guard, cmd_status
extensions/agi/bin/send.py :: send_dm
extensions/agi/bin/brief.py :: successor_prompt
extensions/agi/briefs/seat-successor.md — NEW
.agi/nodes/.geometry/ladder.md :: director_rotate_at
.agi/nodes/.geometry/seats.md :: rotated_by, handoff_file, pin_ref — NEW (l3w4-seat-registry)
extensions/agi/tests/test_rotate.py, test_send.py
skills/agi/SKILL.md :: Seasons, "Rotation:" paragraph

## DESIGN

- `alarms --holder S [--once] [--interval 300] [--window-path P]`: meters rows whose `rotated_by` resolves to `S`; below `pin_ref`'s threshold prints `hold <seat> <fraction>`; at/over, one `send_dm(croot, S, seat, "rotate now")` — live once `l3w4-seat-transport` lands, a plain dm today.
- `rotate-self --name S [--force] [--timeout 600] [--dry-run]`: reads S's own row for role/model/effort/settings, no `--tier`. (1) writes `.agi/sessions/seats/<S>.handoff.md` (`seat`, `generation`=prior+1, `rotated_at`, `predecessor_session`); (2) renames its own window (no `-t`) to `<S>.gen<N>`, freeing the plain name; (3) spawns the successor under it via `_successor_command`, body `seat-successor.md`; (4) `_read_first_reply` on its log, `cmd_loop`'s own `continue` contract; (5) confirmed, `tmux kill-window`s its renamed pane.
- `cmd_status --seats`: seat/generation/fraction/age, one line per row — "each layer lasts longer" is read there, never enforced.
- Belam (owner text ambiguous; proposal): `loop --role prime_director` stays self-metered. "Together" = `alarms --holder <advisor>` also reads his pin, posts the fraction to room `tier3-quorum`, so advisors keep their `HANDOFF.md` slice current — non-blocking.

## TESTS (red-first, test_rotate.py)

`test_alarms_once_holds_below_threshold`; `test_alarms_once_dms_holder_when_due_then_stops`; `test_rotate_self_dry_run_reuses_plain_name_no_roman`; `test_rotate_self_renames_window_before_respawn`; `test_rotate_self_kills_own_window_after_continue`; `test_seat_handoff_generation_bumps_on_rotation`; `test_status_seats_flag_lists_fraction_and_age`.

## GATE

`rotate-self --name adv-alive --dry-run` prints all five steps, ends on window `adv-alive` (never `adv-alive-II`), `generation: N+1`; `alarms --holder belam --once` on a fake pin at 0.40 sends one dm, spawns nothing; suite green via `commands.py run tests`; no live spawn or tmux call outside `--window-path` fixtures.

## NOT IN SCOPE

Registry rows, `rotated_by` resolution (`l3w4-seat-registry`); tmux nudge, any `spawn_window` extraction (`l3w4-seat-transport`); liaison duty text (`l3w4-liaison-seat`); quorum vote mechanics, audience routing, owner 4 (`l3w4-quorum-reviews`); seat-status graph render, `goal:g16` (`l3w4-telemetry-seat-status`).

## SOURCE

`.agi/context/l3-command-ladder-brief.md`, "Owner text 2026-09-07 (04:40–06:40 UTC, to Belam II after rotation)": owner verbatim (1); Director gloss, "Seat lifecycle."

ADDENDUM (Belam IV, 2026-09-07 14:55 UTC, measured): after rotating to Belam IV at 14:05 UTC, the predecessor Belam III kept acting for 40 minutes — recorded owner text, edited nodes and committed 439d1ef55 with git add -A at 14:45 UTC, sweeping the successor's in-flight round (L3.23 kid edits, uncommitted briefs, HANDOFF.md) into a commit the successor never reviewed. Two primes writing the same tree is the failure this loop must close: once the successor has answered, the predecessor's seat becomes inbox-only — no commits, no node writes, no HANDOFF edits; owner text that arrives late is relayed by DM to the live seat, which records it. Make that a mechanical property of the loop (the rotate step revokes the predecessor's git verbs via the adapter tool list or ends its session after the read-back), and a red-first test that a rotated-out seat's write is refused.

RE-RUN AS BUILD (Belam VII, after L3.30). The kid a00-6fc04d55 returned inconclusive_lean_disproved:60 and its caveat says why in one line: the commands this brief's claim names do not exist, so it could judge only the one seam that was implemented, and it proved the hazard on a FABRICATED log rather than a live run. That is trap 0g in its other form - a brief whose gate cites commands that were never built cannot be proved by anyone, and an honest kid correctly refuses to pretend. Rewrite the testable_claim as the FIX's proof condition against commands that EXIST after the change, name the seam it must add rather than the seam it may inspect, and require the hazard to be reproduced against a real rotation rather than a hand-written log. This brief matters more than its verdict suggests: it is the piece the owner asked after directly in HANDOFF section 6 item 32 - the loop that lets a perpetual director-kid run its own goal's parent and kid loops by itself - so it gets a slot in the next round either way. HARNESS DEFECT the same kid hit, worth its own fix and a failures.py row: its struggles line reads that write.py takes set FIELD VALUE as ONE script argument, write.py <id> "set FIELD VALUE", and NOT as the space-separated tokens the kid's rendered brief showed it. The kid brief template is teaching every kid the wrong calling convention for the one command they are all required to use. Fix it in brief.py's kid template when brief.py is free - it was being edited by live kids during this round and must not be touched mid-flight.

EXACT TARGET FOR THE RE-RUN (Belam VII, from the L3.30 review, wf_7fb7a17d-9ae). The reviewer found ZERO overclaims and called the lean-disproved:60 proportionate - one seam tested hermetically against a claim that asked for a live rotation loop - so read this as a scoping failure of the brief, not a failure of the kid. What does not exist and must be built: rotate.py alarms --holder S and rotate.py rotate-self --name S, the two commands the testable_claim is actually about, are absent from the tree entirely. None of the seven red-first tests this brief's own TESTS section names exist: test_alarms_once_holds_below_threshold, test_alarms_once_dms_holder_when_due_then_stops, test_rotate_self_dry_run_reuses_plain_name_no_roman, test_rotate_self_renames_window_before_respawn, test_rotate_self_kills_own_window_after_continue, test_seat_handoff_generation_bumps_on_rotation, test_status_seats_flag_lists_fraction_and_age. Build the commands, then those seven names go green. The HAZARD half is now independently reproduced against the real rotate.py _read_first_reply and _is_log_noise rather than a synthetic fixture, so treat it as established and FIX it: a new generation must not be confirmable by a predecessor's stale bare continue left in a reused plain-name log. The fix named but unbuilt is a read-before-write cursor or a log truncation at spawn so the read-back can only see lines written after the successor started. Prerequisite the brief itself defers: seats.md needs rotated_by, handoff_file and pin_ref for alarms to know whom to hold and whom to DM - that belongs to l3w4-seat-registry and must land first or be carried into this slice deliberately. This is the seat loop the owner asked after in item 32: without rotate-self a director-kid cannot keep itself alive across its own context limit, and everything else in the perpetual-seat design assumes it.
