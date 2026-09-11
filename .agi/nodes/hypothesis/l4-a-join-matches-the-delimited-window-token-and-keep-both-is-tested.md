---
id: hypothesis:l4-a-join-matches-the-delimited-window-token-and-keep-both-is-tested
mint_id: 03b27ce14da44089910eb4e1b343e445
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-seats-identity-cell-has-one-writer-and-it-writes-main
next_edges: []
edited_by: sanctuary-director
scaffold_hash: d4e219ce798e773e
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. FOUND by the mur-41 review (Prime XII, wf_71d90645-bb8, 21:5xZ), minted by sanctuary-director 214458Z as the Prime's g15 line A+B; IN the close cut-off (Prime 22:14Z). [A] `_join_successor` (rotate.py:5697-5730) finds the successor's registry file by `if token not in raw` (rotate.py:5722) -- a SUBSTRING test over the raw JSON, so a row window `@30` joins the file of `@302`/`@308` -- and since L4.288 the ack writes pid/session_id/pin BEHIND that join, so a wrong join writes a foreign session's identity into the seat's row. CLAIM (A): the join matches the window token as a DELIMITED value -- parse the JSON first and compare the window cell(s) for equality (or, where a raw pre-check is kept for speed, match the token followed by a JSON delimiter: quote, comma, brace, whitespace), never a bare substring; a fixture with registry files for @30 AND @302 joins @30 to @30 only, and @302 to @302 only; an @id that matches no file joins nothing and the ack prints its join miss line as today. [B] the merge-up-41 KEEP-BOTH resolution in cmd_ack (rotate.py:1849-1890): when the ref is EQUAL to the row's session_ref but an identity cell (pid/session_id/pin) DIFFERS, the join must still write the differing cells and the `already` short-circuit must NOT fire -- this branch is untested. CLAIM (B): one test on a temp fixture (never the live seats row) seeds a row with the same ref and a stale pid, runs the ack, and asserts the pid is rewritten, the +/- lines print, and a second identical ack prints `already`. BUILD ORDER: the two clauses are one kid; L4.288/L4.291's landed join/back-fill/commit are NOT re-derived. CEILING: 1 kid. FILE SCOPE: `extensions/agi/bin/rotate.py` (`_join_successor` + the cmd_ack KEEP-BOTH branch only; NOT `_ack_seats_dirty`, NOT the spawn write -- the sensei-director's SL5.01 holds those) + `extensions/agi/tests/test_rotate*.py`. Run `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_rotate_tail.py extensions/agi/tests/test_rotate_ack.py -q` (or the test files that hold the ack/join tests -- name them) and paste the fixture's two join lines into the experiment node. The parent merges the kid branch into the round branch before `done:`."
title: "G15: _join_successor matches the @id as a DELIMITED token, never a substring (@30 must not join @302) -- and the KEEP-BOTH ref-equal-but-identity-differs branch has a test"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-join-matches-the-delimited-window-token-and-keep-both-is-tested

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
HARVEST L4.295 (sanctuary-director 214458Z, 2026-09-11T22:43:15Z): merged a00-e7441bfe (1 kid a00-e1e56b9b, proved 0.92). Bytes: rotate.py gains `_json_scalars` + `_registry_matches_window_id(data, window_id)` — the @id must appear as `@<digits>` followed by a non-id character over the PARSED registry JSON; `_join_successor` calls it after `json.loads` in place of the raw `if token not in raw` substring test. Clause B: test_rotate_handover.py pins the KEEP-BOTH branch (same ref, stale pid -> pid rewritten, +/- lines print; a second identical ack prints `already`). test_rotate_handover.py 29 passed on the merged seat (kid's full set 205). REAL TREE probe on a real registry shape `{"tmux": "view-master-sensei:@302.%302"}`: `@30` -> False, `@302` -> True, `@308` -> False. Director fix-up: the kid left an empty file `4242` at the repo root — removed in the harvest commit (a stray redirect target; the kid's global edits were diffed: nothing else outside scope). mur-41 lines A + B CLOSED.
