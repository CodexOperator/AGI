---
id: hypothesis:l3w4-seat-rotation-loops
mint_id: 75eb63960ff947eabc3594bb117c4365
type: hypothesis
parents:
  - goal:g17
next_edges: []
edited_by: belam-S1-L3-VIII
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

LIVE DEFECT FOUND AT BELAM VII's OWN ROTATION, 2026-09-07 21:56 UTC, and it is the most dangerous one in this brief's area because it fails silently toward losing the ladder. rotate.py loop --role prime_director --name belam-S1-L3-VIII --model claude-opus-5 --effort max --force --session-log <own transcript> printed 'successor replied (handoff needs change):' followed by the PRIME'S OWN transcript line - a mode event carrying the prime's own sessionId, not the successor's - and then printed 'rotate prime_director --> successor belam-S1-L3-VIII' as if it had worked. tmux list-windows showed belam windows for II through VII and NOTHING for VIII. No successor existed. A prime that believed that line would have emitted its closing prayer and exited, leaving the ladder with no prime at all and a handoff nobody was reading. rotate.py spawn --name belam-S1-L3-VIII --model claude-opus-5 --effort max then worked on the first try and the successor was confirmed by tmux capture-pane loading the agi skill. TWO TANGLED BUGS, both live: first, --session-log X is used for BOTH the meter and the successor read-back (trap 0l), so the read-back opens the caller's own transcript and finds whatever the caller just wrote; second, and worse, loop accepts that as a confirmed reply and RETURNS SUCCESS WITHOUT EVER CHECKING THAT A WINDOW EXISTS. The second bug is independent of the first and is the one to fix first: loop must assert the successor's tmux window is present and answering before it returns, and it must fail loudly when it is not. The read-back must additionally never be pointed at the caller's own transcript - give it the successor's pin or the window, never --session-log. This is the same read-side family as the stale-continue hazard this brief already fixed with a read-before-write cursor, which suggests the cursor fix is necessary but not sufficient: a cursor cannot help when the file being read is the wrong file entirely.

RE-RUN AS BUILD (Belam VIII, L3.33). L3.31 landed the build at lean-proved:80 — alarms and rotate-self are real and 7 named tests are green — but it is proved only hermetically through --window-path fixtures and NO live tmux rotation has ever been observed. Two further defects were then measured live at L3.32 and both are in this brief's territory. FIRST, THE MOST DANGEROUS DEFECT OF THE SESSION, because it fails silently in the direction of LOSING THE LADDER: rotate.py loop --role prime_director --name belam-S1-L3-VIII --model claude-opus-5 --effort max --force --session-log <own transcript> REPORTED A SUCCESSFUL ROTATION AND SPAWNED NO TMUX WINDOW (Belam VII, 21:56 UTC). It printed 'successor replied (handoff needs change):' followed by the PRIME'S OWN transcript line (a mode record carrying the caller's sessionId), then 'rotate prime_director --> successor belam-S1-L3-VIII', while tmux list-windows showed windows for II through VII and nothing for VIII. rotate.py spawn with the same flags worked first try. A prime that trusted that line would have exited and left no successor at all. Two tangled bugs, both live. (a) --session-log X is used for BOTH the meter and the successor read-back, so the read-back reads the CALLER'S transcript and any line in it can be mistaken for the successor's reply. The successor read-back must resolve its own path independently and REFUSE loudly if that path equals the caller's session log. (b) loop returns success without ever asserting the successor's window exists. It must assert the tmux window is present AND that the reply was written after the spawn timestamp (that is what L3.31's read-before-write cursor is for), and exit non-zero with a named message otherwise. SECOND, THE LIVE PROOF THIS BRIEF STILL OWES: a real successor spawned into real tmux under a reused plain name, answering continue, with the predecessor's window handled — the piece the owner asked after in HANDOFF section 6 item 32, because without rotate-self a director-kid cannot outlive its own context. A throwaway successor is fine and is the precedent (L3.01b): rotate.py spawn --name <throwaway> --model claude-haiku-4-5-20251001 --effort low, told to answer continue and stop; confirm by tmux capture-pane -pt agi-rc:<name> | tail, record the pane text verbatim as evidence, and kill ONLY the throwaway window. Never kill a belam-* window. GATE: the two fixes green under red-first tests, plus one live pane capture showing a successor that answered.
