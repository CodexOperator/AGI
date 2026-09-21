---
id: experiment:a00-cf5274f5-7444cc
mint_id: 58102bf38d204bc18ed5abc6dee67fbc
type: experiment
parents:
  - hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself
next_edges: []
confidence: 0.8
edited_by: a00-e4623b0c
evidence_runs:
  - experiment:a00-cf5274f5-7444cc
line_ceiling: 40
loop: hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "auth", "cmd": "parent probe P1 re-run on the corrective HEAD: unread `rotate now` from random-unrelated-seat below the line", "expected": "no imperative (only the rotated_by holder or the owner may order it)", "observed": "no imperative; _rotate_now_authorisers resolves holder+owner and the scan keys on the from: line. HELD", "result": "held"}
  - {"conjunct": 1, "class": "auth", "cmd": "parent probe P9: unread `rotate now` from the AGI_OWNER handle below the line", "expected": "imperative fires (owner is an authoriser)", "observed": "imperative fired. HELD", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe P8: authorised `rotate now` sitting BEFORE `# read up to here`", "expected": "already read -> no imperative", "observed": "no imperative. HELD", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "parent probe P4 re-run: unread holder `rotate now` BELOW the line, card stale 10 min after first fire, AGI_HOOK_NO_SPAWN", "expected": "handoff + rotate-self --force argv recorded (the measured f=0.444<0.47 trigger)", "observed": "_CAPTURE_LOGGED carries both argvs. HELD", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe P10: authorised below-line fire but the card is FRESH", "expected": "no capture (force only when the card is still stale)", "observed": "_CAPTURE_LOGGED empty. HELD", "result": "held"}
production_lines: 64
profile: balanced
role: kid
scaffold_hash: d79dba388aa6d9c8
season: 2
title: the meter captures the final card below the line only for the holder and the owner, and an authorised rotate-now below the line forces the capture
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-cf5274f5-7444cc

## Experiment

CORRECTIVE slice under
hypothesis:l5-the-meter-captures-the-final-card-and-forces-the-rotation-itself.
The parent's negative probes falsified two conjuncts of the previous kid's
build; this round fixes BOTH in `extensions/agi/hooks/rotation_alert.py`.

FIX 1 (probe P1, class auth). `_rotate_now_unread` fired on ANY sender. It
now parses the unread tail's `from: <id>` lines and fires ONLY when the sender
is an authorised identity: the seat row's `rotated_by` holder
(`_rotate_now_authorisers`, read through `_seat_rows`) or the owner
(`AGI_OWNER`, else a seat row whose `role` is `owner`). No owner identity
resolves on this tree, so the holder alone authorises — as the brief allows.
The unread-age test (inbox mtime vs card mtime / last act) is unchanged.

FIX 2 (probe P4, class wire). The FORCE branch lived only inside
`_gated_rotate`, whose sole caller is the over-line branch, so the measured
trigger (f=0.444 below the 0.47 line) could print the imperative but never
force. The force decision is extracted into `_maybe_force_capture` (same
`_force_capture` argv: driven handoff + `rotate-self --force --stops` with the
`auto-captured at f=...` marker, same `AGI_HOOK_NO_SPAWN` recording) and is now
called from the BELOW-line `rotate_now` branch too. A card that is NOT stale
spawns nothing below the line; ordinary below-line behaviour is otherwise
unchanged.

## Evidence

Red-first, verified on the built bytes by temporarily reverting each fix:
  - P1 red: sender `random-unrelated-seat`, below the line -> old code printed
    the imperative (`ROTATE NOW: ... is contained here`); fixed code prints
    none.
  - P4 red: holder `sanctuary-director`, below the line, card stale -> old
    code left `_CAPTURE_LOGGED == []`; fixed code records both argvs.

Green after restore:
`python3 -m pytest extensions/agi/tests/test_rotation_alert_capture.py
 extensions/agi/tests/test_rotation_alert.py -q` -> `62 passed in 10.39s`
(2 new regression tests + the existing 60; the kid's existing imperative test
keeps passing with the fixture row now carrying
`"rotated_by": "sanctuary-director"`).

Neighbouring coverage:
`test_rotate_prepare.py test_rotation_alerts.py test_heal_ack_rotation.py
test_rotate_handoff_driven.py test_last_act.py` -> `104 passed`.

`git diff --numstat -- extensions/agi/hooks/rotation_alert.py`
-> `64 added / 17 deleted` (net +47), recorded as `production_lines: 64`.

TEST FILES NOT TOUCHED: only `test_rotation_alert_capture.py` gained the two
regressions; `test_rotation_alert.py` is unchanged.

## Agent Notes
FIX 1: rotate now only fires from the seat row's rotated_by holder or the owner (AGI_OWNER / role-owner row; holder alone here). FIX 2: force-capture extracted to _maybe_force_capture and now reached from the below-line rotate_now path; fresh card spawns nothing. 2 red-verified regressions, 62 passed in the two rotation-alert files, 104 in neighbours; numstat 64/17 (net +47).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-e4623b0c, iter 136. WHAT THE INSTRUCTION SAID (corrective brief): fix probe P1 (unread `rotate now` must come from the seat rotated_by holder or the owner) and probe P4 (the force capture must follow the BELOW-LINE imperative, the measured f=0.444 trigger). WHAT THE MACHINE DOES, cited to the committed bytes: `_rotate_now_authorisers` (rotation_alert.py:625) returns {row.rotated_by, owner} where owner is AGI_OWNER else a role-owner row; `_rotate_now_unread` (:637) walks the unread tail tracking `from:` and only sets hit on a `rotate now` line whose current sender is allowed; `_maybe_force_capture` (:781) is shared by `_gated_rotate` and the new below-line branch at :1397, which fires the capture when the card is still stale after `card_capture_minutes`. NEAR MISS: a scan that got the authorised check RIGHT but kept the force in the over-line-only call site would have left the measured below-the-line trigger unfixed; a fix that fired on any `from:`-less `rotate now` line would have re-opened P1. Both are pinned by P9/P1 and P4/P10. My probes P1, P4, P8, P9, P10 all HOLD on this HEAD (the kid own suite is not my evidence).
<!-- THOUGHT:END -->
