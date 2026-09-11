---
id: experiment:a00-e1e56b9b-ec05cd
mint_id: 130d9bcc68bf4b6d89fdd0f8e7b511ac
type: experiment
parents:
  - hypothesis:l4-a-join-matches-the-delimited-window-token-and-keep-both-is-tested
next_edges: []
confidence: 0.92
edited_by: a00-e7441bfe
evidence_runs:
  - experiment:a00-e1e56b9b-ec05cd
loop: hypothesis:l4-a-join-matches-the-delimited-window-token-and-keep-both-is-tested@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 40fa7c659604fdd4
season: 2
title: A00 e1e56b9b ec05cd
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e1e56b9b-ec05cd

## Experiment

BUILD ORDER (goal:g15) — build both clauses, don't just measure them. The target node names `test_rotate_ack.py`, which does NOT exist (record corrected: the ack tests live in `test_rotate_handover.py`, `test_rotate.py`, `test_rotate_g1517.py`). Work landed in `extensions/agi/bin/rotate.py` + `extensions/agi/tests/test_rotate_handover.py`.

### Clause A — `_join_successor` matches the @id as a DELIMITED token

Pre-fix `rotate.py:5722` did `if token not in raw: continue` — a bare SUBSTRING test over the raw JSON, so window `@30` joined the registry file of `@302`/`@308`. Since L4.288 the ack writes pid/session_id/pin BEHIND that join, so a wrong join wrote a foreign session's identity into the seat's row.

Fix: moved `json.loads` BEFORE the match and replaced the substring test with a delimited-token match over the PARSED JSON. New helper `_registry_matches_window_id(data, window_id)`: the @id digits must be followed by a NON-id character (`.`, quote, comma, brace, whitespace, or end of value) — tmux stores the window as `@<id>.%<pane>`, so `@30` matches `view:@30.%0` but NOT `view:@302.%0`. A non-numeric window id falls back to a whole-cell equality match. No bare substring anywhere.

Fixture (test_rotate_handover.py `test_join_matches_window_id_as_delimited_token`): two registry files `@30` and `@302`.

### Clause B — KEEP-BOTH ref-equal-but-identity-differs branch has a test

At `rotate.py` cmd_ack: when the ref EQUALS the row's `session_ref` but an identity cell (pid) DIFFERS, `already` must be False and the write must still happen. This branch was UNTESTED.

Fix: no code change — added the missing test `test_ack_keep_both_ref_equal_identity_differs_writes_pid` on a TEMP git fixture (never the live seats row): row already carries `session_ref=r1` but a STALE pid 999999 + blanked session_id (window @77); a registry whose content matches @77 with LIVE pid 4242. First ack rewrites pid to 4242 and prints +/- lines; a second identical ack prints `already`.

## Evidence

Verification (205 passed, 0 failed):

    env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_rotate_handover.py extensions/agi/tests/test_rotate_tail.py extensions/agi/tests/test_rotate.py extensions/agi/tests/test_rotate_identity_main.py -q
    # 205 passed in 42.44s

Two join lines (Clause A fixture):

    JOIN30: joined by @30 in registry file 10001.json
    JOIN302: joined by @302 in registry file 10002.json
    MISS: registry file for @999 not found in .../registry within the bounded join poll

Clause B — FIRST ack (ref equal but pid differs -> write, NOT already):

    back-filled session_ref=r1, session_id=abc-def-123, pid=4242 into own row (source: ack, joined by @77)
    ack: committed own row write (nodes/.geometry/seats.md):
    +edited_by: adv-s
    -  - {"name": "adv-s", ... "session_ref": "r1", "session_id": "", "window": "@77", "pid": 999999}
    +  - {"name": "adv-s", ... "session_ref": "r1", "session_id": "abc-def-123", "window": "@77", "pid": 4242}
    git -C <tmp> push

Clause B — SECOND identical ack (nothing differs -> `already`):

    ack: adv-s row already carries session_ref=r1 — nothing to back-fill or commit

## Agent Notes
Clause A: _join_successor now matches @id as delimited token over parsed JSON (no bare substring) - @30 joins @30 only, @302 joins @302 only, miss named. Clause B: added missing test for KEEP-BOTH ref-equal-but-identity-differs - pid rewritten + +- lines on first ack, already on second. Full rotate suite 205 passed. test_rotate_ack.py does not exist; ack tests live in handover/rotate/g1517.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-e7441bfe, L4.295) — ACCEPTED proved, confidence 0.9.

WHAT THE INSTRUCTION SAID: the target node says "[A] the join matches the window token as a DELIMITED value ... never a bare substring" and "[B] one test on a temp fixture ... seeds a row with the same ref and a stale pid, runs the ack, and asserts the pid is rewritten, the +/- lines print, and a second identical ack prints already".

WHAT THE MACHINE ACTUALLY DOES (artifact read + run, not appearance): I read the diff at extensions/agi/bin/rotate.py:5697-5765 — json.loads now runs BEFORE the match and the bare substring test is replaced by _registry_matches_window_id(data, token), a regex @<digits>(?![0-9A-Za-z_]) over parsed scalar VALUES. I ran the helper directly against the real registry shape measured at /home/ubuntu/.claude/sessions/1847231.json (tmux = "view-master-sensei:@305.%305"): @30 vs @302 -> False, @30 vs "v:@30.%30" -> True, @30 vs "v:@1030.%1030" -> False, nested/list scalars -> True, empty dict (JSON parse failure) -> False (fails closed, which the old substring test did not). I reproduced the kid suite myself: 205 passed in 43.11s across test_rotate_handover + test_rotate_tail + test_rotate + test_rotate_identity_main. The kid's two fixtures assert exactly what clause B demands: first ack rewrites pid 999999->4242 with +/- lines and no "already"; second identical ack prints "row already carries session_ref=r1 -- nothing to back-fill or commit" and does not commit.

THE NEAR MISS: a fix that keeps the raw pre-check and only ADDS the parsed comparison afterwards satisfies the words "where a raw pre-check is kept for speed" and still loses clause A — the raw substring would match @302 first in sorted glob order, and a file whose JSON fails to parse would fall into the data = {} branch and still be accepted by the parsed test as an empty dict if the comparison were written as a raw fallback. The kid did it the other way — parse first, no raw check — which is the stronger read; noted as a deviation in the SAFE direction, not an overclaim.

CAVEATS I am carrying forward, none of which change the verdict: (1) clause B exercises pid + blanked session_id but NOT pin; the target text names "pid/session_id/pin" as the differing cells and the meter pin is the one cell still unasserted in the ref-equal branch. (2) The regex is stricter than the target's minimum ("token followed by a JSON delimiter: quote, comma, brace, whitespace") — it also rejects a following LETTER/underscore, correct for tmux numeric ids but it would silently stop matching if a registry ever stored @30a. (3) The kid correctly corrected the record: test_rotate_ack.py named in the target does not exist; ack tests live in test_rotate_handover.py / test_rotate.py / test_rotate_g1517.py.

NOT RE-DERIVED, as instructed: _write_identity_cells, _shared_graph_root, _successor_row_write, _backfill_session_ref, _ack_seats_dirty and the spawn write are untouched by this diff.
<!-- THOUGHT:END -->

PARENT REVIEW L4.295 (a00-e7441bfe): ACCEPTED proved at 0.9. Clause A verified by running _registry_matches_window_id against the live registry shape and by reproducing 205 passed; clause B test present and both halves (write-on-diff, already-on-second) asserted on a temp git fixture. Evidence: experiment:a00-e1e56b9b-ec05cd. Owed as small fix-onlys, none blocking: pin-cell coverage in the ref-equal branch; the regex rejects a trailing letter where tmux ids are numeric.
