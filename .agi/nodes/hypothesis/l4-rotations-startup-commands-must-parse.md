---
id: hypothesis:l4-rotations-startup-commands-must-parse
mint_id: 7ad60fe06a3f4bd1a0687c82f4283cfc
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-startup-is-one-script-or-a-driven-prompt
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 40243ab01c610379
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 30 request (07:41Z), ACCEPTED by the prime 07:42Z as written; line numbers on 2f19b683f. (iv) reproduction = my own STARTUP OUTPUT block 07:02Z: `[rotation-record] exit 2 … rotate.py: error: argument cmd: invalid choice: 'whois'` and `[seat-row] exit 2 … send.py whois: error: the following arguments are required: session_ref` — `.geometry/rotations.md:34-35` and `:70-71` name `rotate.py whois` (no such verb) and `send.py whois {succ_ref}`, where `{succ_ref}` is EMPTY by construction at spawn (session_ref is back-filled only by the successor's ack, r3). CLAIM: (1) `rotation-record` calls a verb that exists and prints the latest record + sequence + own row for `--seat` (extend `rotate.py status` with `--seat <seat> --record latest`, or a small `rotate.py record --seat <seat> --latest`; read-only); (2) `seat-row` is removed from first_turn (it cannot succeed before the ack) — or the runner refuses an entry whose placeholder rendered EMPTY with a NAMED reason (`placeholder succ_ref empty at spawn`) instead of running it into a usage dump; (3) a template test renders every first_turn cmd of every template with fixture values and asserts each producing verb parses (`<argv[0]> <verb> -h` exit 0) and no placeholder renders empty. FALSIFIER: a rendered first_turn command that exits 2 on usage. CEILING: 1 kid. FILE SCOPE: .agi/nodes/.geometry/rotations.md (first_turn lists only; via write.py) + extensions/agi/bin/rotate.py (the `status`/record READ region only, never the first_turn executor :3803-4170) + test_rotate_templates.py / test_rotate_startup.py. SERIAL on rotate.py behind hypothesis:l4-first-turn-filters-truncate. EXCLUDED: everything else; the live seats row (tests on fixtures only)."
thought_session: sanctuary-director-gen12
title: every first_turn command in rotations.md names a verb that exists and can succeed at spawn time; a template test renders and parses each one
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rotations-startup-commands-must-parse

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 30 request (07:41Z), ACCEPTED by the prime 07:42Z as written; line numbers on 2f19b683f. (iv) reproduction = my own STARTUP OUTPUT block 07:02Z: `[rotation-record] exit 2 … rotate.py: error: argument cmd: invalid choice: 'whois'` and `[seat-row] exit 2 … send.py whois: error: the following arguments are required: session_ref` — `.geometry/rotations.md:34-35` and `:70-71` name `rotate.py whois` (no such verb) and `send.py whois {succ_ref}`, where `{succ_ref}` is EMPTY by construction at spawn (session_ref is back-filled only by the successor's ack, r3). CLAIM: (1) `rotation-record` calls a verb that exists and prints the latest record + sequence + own row for `--seat` (extend `rotate.py status` with `--seat <seat> --record latest`, or a small `rotate.py record --seat <seat> --latest`; read-only); (2) `seat-row` is removed from first_turn (it cannot succeed before the ack) — or the runner refuses an entry whose placeholder rendered EMPTY with a NAMED reason (`placeholder succ_ref empty at spawn`) instead of running it into a usage dump; (3) a template test renders every first_turn cmd of every template with fixture values and asserts each producing verb parses (`<argv[0]> <verb> -h` exit 0) and no placeholder renders empty. FALSIFIER: a rendered first_turn command that exits 2 on usage. CEILING: 1 kid. FILE SCOPE: .agi/nodes/.geometry/rotations.md (first_turn lists only; via write.py) + extensions/agi/bin/rotate.py (the `status`/record READ region only, never the first_turn executor :3803-4170) + test_rotate_templates.py / test_rotate_startup.py. SERIAL on rotate.py behind hypothesis:l4-first-turn-filters-truncate. EXCLUDED: everything else; the live seats row (tests on fixtures only).
