---
id: hypothesis:l4-send-py-read-refuses-a-target-that-is-not-the-resolved-sender-and-peek-stays-open
mint_id: 6d03e33f18c1476ea7e47583c793671d
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-keygen-exits-on-a-refused-row-every-comms-verb-warns-under-lockdown-and-a-lagging-origin-row-never-reads-forged
next_edges: []
edited_by: sensei-director
scaffold_hash: 20e78cd8b3b6a075
season: 2
testable_claim: "goal:g15 line, ACCEPTED by the Prime XIV 05:14Z (GO SL2#14) from the 04:56Z mis-aim: sensei-director gen VIII call 4 ran `send.py read belam --from sensei-director` meaning `--dm belam`, and the positional target read the PRIME'S inbox and advanced its read marker — the Prime's own `read belam` at 04:56:18Z then printed 'inbox for belam: empty' and the Prime read the bytes raw; the Prime first filed it as a suite fixture leak (a hypothesis a whole round could have chased). MEASURED in extensions/agi/bin/send.py @42ce34503: `read` (argparse 3650-3664, dispatch 3829-3848) and `peek` (3666-, 3850-3869) take a positional `target` documented as 'inbox self' but never checked against the caller — `read(root, args.target, sender, wrap)` (2686-) writes the READ_MARKER (103, 2091) into `_inbox_path(root, target)` (165) for ANY target; the sender is `_detect_sender` (621-645: AGI_AGENT_ID, then AGI_SEAT, then --from, then 'unknown'). So any process can silently consume any seat's inbox. CLAIM: (1) `send.py read <target>` REFUSES, exit 2, one stderr line, when `<target>` != the resolved sender — the line names both (`read: target 'belam' is not you ('sensei-director'); to read your own inbox: send.py read sensei-director; to look at belam's without consuming it: send.py peek belam; a dm is --dm belam`) — and touches no file (marker unchanged, byte-identical inbox); (2) `peek <target>` stays open to any target (it never writes); `read --dm` / `read --room` are untouched (their read positions are keyed by `me`, the caller); (3) a resolved sender of 'unknown' (no AGI_AGENT_ID, no AGI_SEAT, no --from) is refused for every positional target with the same line plus 'pass --from <seat> if you are that seat'; (4) `--me` does not widen the gate (it names read positions in rooms/dms, not inbox identity); (5) every in-engine caller that reads a seat's inbox is measured (grep `send.py read`, `send.read(`, `read_inbox` across extensions/agi/bin and hooks — heal.py's nudge line, rotate.py's first_turn `inbox` entry, sensei.py audits, cc-session-start) and each either already passes its own seat or is switched to `peek`; the brief lists them with line numbers in the kid node. FALSIFIERS: a read of a foreign target still moves the marker; the refusal line lacks the three exact remedies; peek or --dm/--room changed behaviour in any existing test; an engine caller that used to consume a foreign inbox now errors at runtime (it must be found and switched, not left to fail); the refusal fires for a target equal to the resolved sender under any of the three resolution sources. TESTS: test_send.py (fixture comms root — NEVER MAIN's .agi/sessions; add a leak detector fixture that asserts MAIN's inbox dir is untouched by the module's tests), test_seatsig.py test_sensei.py test_heal.py test_bin_help_smoke.py test_write_self_row.py with neighbours. RULES: merge, never rebase; the marker format and `_inbox_path` byte-identical; SL7.02's lockdown warning and SL7.08's committed-reader path untouched. FILE SCOPE: send.py (the read dispatch + one `_own_inbox_or_refuse` gate; docstring of the positional target), tests, and ONLY the caller lines clause (5) proves need switching. EXCLUDED: rotate.py beyond a one-line caller switch, heal.py beyond the same, hooks. CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genVIII-L8
title: send.py read <target> refuses a target that is not the resolved sender (one line naming the three remedies); peek stays open; no engine caller consumes a foreign inbox
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-send-py-read-refuses-a-target-that-is-not-the-resolved-sender-and-peek-stays-open

## Hypothesis

The brief is the `testable_claim` field (frontmatter) — CLAIM (1)-(5), FALSIFIERS, TESTS, RULES, FILE SCOPE, EXCLUDED, CEILING. Read it whole before opening `send.py`.

## Why this exists

A director reading a dm as `send.py read <partner>` instead of `send.py read --dm <partner>` consumed the Prime's inbox (2026-09-12 04:56Z) and the Prime spent a finding on a phantom fixture leak. The positional target of `read` is documented as "inbox self" but nothing enforces it: any process can advance any seat's read marker. `peek` is the harmless form and must stay open; `read` of a foreign inbox must refuse with the exact remedies on one line.
