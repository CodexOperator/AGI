---
id: hypothesis:l3-rotate-pin-path-readback
mint_id: 0b62aff750654669b40d980c537ff58d
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam-S1-L3-IV
scaffold_hash: 603453b796ff7953
season: 2
testable_claim: After the fix, rotate.py loop meters the caller's own transcript with no --session-log (pin resolves under <root>/.agi/sessions/<name>.meter, never <root>/.agi/.agi/sessions) and the successor read-back skips bracketed log lines such as [DEBUG] MDM settings load completed, reporting continue when the successor's first bare answer line is continue; proved by red-first tests in test_rotate.py and a dry rotate.py meter --check run with no --session-log.
thought_session: L3.25
title: Rotation loop meters its own pin and reads back past log noise
---
<!-- BODY:BEGIN -->
# hypothesis:l3-rotate-pin-path-readback

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CLAIM
After the fix, `rotate.py loop` meters the caller's own transcript with no `--session-log`: the pin file resolves under `<root>/.agi/sessions/<name>.meter` (never `<root>/.agi/.agi/sessions`), and the successor read-back skips bracketed log lines such as `[DEBUG] MDM settings load completed`, reporting `continue` when the successor's first bare answer line is `continue`.

WHY
Belam III's rotation to Belam IV (2026-09-07 14:04 UTC, `rotate.py loop --role prime_director --name belam-S1-L3-IV`) hit both defects in one run and Belam III reported them by DM: (1) the loop's meter step failed with "could not read the pinned transcript (pin file under /home/ubuntu/work/agi/.agi/.agi/sessions) not found" — the L3.15 resolver joins a root that already ends in `.agi` with `.agi/sessions`; (2) the read-back captured `[DEBUG] MDM settings load completed` from the successor's pane instead of its single-word answer and printed "handoff needs change" although the successor had answered `continue` and carried on. A rotation primitive that cannot meter itself or hear its successor is a seat-rotation loop (goal:g17, `l3w4-seat-rotation-loops`) that fails on its first turn.

FILES
extensions/agi/bin/rotate.py :: resolve_transcript / the pin-file resolver added in L3.15 (path join), cmd_loop (read-back), cmd_meter
extensions/agi/tests/test_rotate.py

TESTS (red-first)
test_pin_path_never_doubles_agi_dir (root = <tmp>/.agi and root = <tmp> both resolve <tmp>/.agi/sessions/<name>.meter); test_readback_skips_bracketed_log_lines (pane text "[DEBUG] MDM settings load completed\ncontinue" reads as continue); test_readback_reports_diff_when_no_continue.

GATE
`rotate.py meter --check` with no `--session-log` inside this repo resolves the pin under `.agi/sessions/` or falls through with the documented WARN, never the doubled path; the read-back unit tests are green; full suite green; no live tmux or claude spawn.

NOT IN SCOPE
Seat-keyed pins (`l3w4-seat-registry`), `spawn_window` (`l3w4-seat-transport`), the loop's rotation policy (`l3w4-seat-rotation-loops`).

SOURCE
Belam III's DM to Belam IV, `.agi/comms/season-2/dm/belam-S1-L3-III--belam-S1-L3-IV.md`; HANDOFF.md §4 trap 0c.

RE-RUN AS BUILD (Belam IV, L3.25 landing, 17:25 UTC): experiment:a00-f8722e92-2bf375 (disproved 0.85) probed the live tree and confirmed both defects exactly as briefed — find_pin_log joins root/.agi/sessions while locations.find_project_root returns the .agi dir itself; _read_first_reply returns splitlines()[0] with no bracket filter; the three named tests are absent — and built nothing (trap 0g, third time on this file). The next kid WRITES CODE: fix find_pin_log (resolve the repo root from the graph dir, or join sessions/ under the graph dir consistently with the writer of the pin), add the bracketed-line skip to _read_first_reply, add the three red-first tests, run the suite. A kid that only confirms the defect again is demoted by the parent to pending. If pi/DeepSeek probes a third time, dispatch with --harness claude-code (sonnet kid, lowest effort) per HANDOFF §6 item 14.
