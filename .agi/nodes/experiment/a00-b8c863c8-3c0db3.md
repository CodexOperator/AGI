---
id: experiment:a00-b8c863c8-3c0db3
mint_id: 0214a689c3e94f698e3bed2241d11289
type: experiment
parents:
  - hypothesis:l4-sensei-audits-agree-on-session-keyed-acks-and-top-level-session-records
next_edges: []
confidence: 0.95
edited_by: a00-35f28094
evidence_runs:
  - experiment:a00-b8c863c8-3c0db3
loop: hypothesis:l4-sensei-audits-agree-on-session-keyed-acks-and-top-level-session-records@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "independent parent fixture: rotate_out_audit over a predecessor Read of seats/<seat>.ack.<sid8>.json; then mock rotate._ack_session_id -> \"\" and rerun the SAME bytes", "expected": "(b) when the identity threads from the call site; the same Read falls to (d) when the identity is stubbed empty (helper-only threading fails)", "observed": "cats=['b'] then cats=['d'] on the stubbed run", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "_record_matches_session on {session_id: A} -> True; on {handover.join: A} -> True; on {session_id: A, handover.join: B} matching B -> True (join wins); on {session_id: A} vs C -> False; end-to-end row=A with only session-B record on disk", "expected": "top level and join both match, join wins, no over-match, and the end-to-end case exits 2 naming A's session with calls==[]", "observed": "True/True/True/False; wake_audit code=2, calls=[], stderr names session 'aaaaaaaa'", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "classify_call on Bash: cat seats/<seat>.ack.deadbeef.json; cat seats/<seat>.ack.json; cat reports/summary.json; cat seats/<seat>.ack.dead.json", "expected": "b; b; d; d -- the keyed spell and the legacy spell are (b), an unrelated .json and a non-8-char .ack.<token> stay (d)", "observed": "b; b; d; d", "result": "pass"}
  - {"conjunct": 4, "class": "auth", "cmd": "grep the committed tests for test_only_another_sessions_record_refuses_by_name (P1) and test_prime_row_with_session_id_stays_on_latest_and_legacy_ack (P3); check no /tmp code dependency", "expected": "both tests present in test_sensei_wake_audit.py; /tmp/probe_sl7124_parent.py named only as provenance in comments, never imported/opened", "observed": "both present; no import/open of the probe; 109 passed on the three named files", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 318ecb7d69f59164
season: 2
title: A00 b8c863c8 3c0db3
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b8c863c8-3c0db3

**Verdict: `proved`** — four conjuncts of
`hypothesis:l4-sensei-audits-agree-on-session-keyed-acks-and-top-level-session-records`
BUILT (not merely reproduced), all on the live bytes of this worktree's
`extensions/agi/bin/sensei.py`.

## Experiment

Measured the PRE-FIX state, implemented the three code conjuncts, then proved
the built bytes with positive tests plus targeted negative probes. Files
touched (only these three, all inside the permitted set):

- `extensions/agi/bin/sensei.py`
- `extensions/agi/tests/test_sensei_wake_audit.py`
- `extensions/agi/tests/test_sensei_rotate_out_audit.py`

### Pre-fix measurement (the defect, confirmed before touching bytes)

```
C3 cat seats/x.ack.deadbeef.json -> False     (should be b)
C3 legacy .ack.json             -> True
C3 unrelated .json              -> False
C2 record session_id top-level only -> False  (should be True)
C2 record session_id under handover.join -> True
C1 rotate_out_audit hand_paths   -> no session_id (wake_audit threads it)
```

### C1 — `rotate_out_audit` threads the session id (FIXED)

- New bytes: `sensei.py:1628-1629`
  ```
  session_id = rotate._ack_session_id(root, seat)
  hand_paths = _hand_read_paths(entries, facts_list, seat, session_id)
  ```
  The same identity `wake_audit` derives at `sensei.py:1199`. The one-wrapper
  invariant at `classify_tool_use` now holds for a session-keyed ack Read.
- Test: `test_rotate_out_threads_the_session_id_like_wake_audit`
  (`tests/test_sensei_rotate_out_audit.py`) — a non-prime seat row carrying a
  `session_id`, a `seats/<seat>.ack.<sid8>.json` file, and a `Read` of that
  ack in the predecessor transcript: asserts `(b)` in rotate-out, `(b)` in
  wake, and identical `(cat, label)` in both.
- **Wire negative probe (run, passed):** spying on `_hand_read_paths` shows
  `rotate='deadbeef-…' wake='deadbeef-…'` (equal). Simulating a call site that
  does NOT thread it (a pre-fix-shaped wrapper dropping the 4th arg) makes the
  SAME Read classify `['d']` — so the test fails on a helper that is tested
  directly but never threaded from the call site.

### C2 — `_record_matches_session` reads the record TOP level (FIXED)

- New bytes: `sensei.py:595-623`. Reads `rec.get("session_id")` first, then
  `handover.join.session_id` wins when present — `rotate._record_join`'s order
  (`rotate.py:6365-6377`), so `rotate.py:4702-4703`'s top-level write for a
  FIRST-SEATING record resolves. 8-char prefix rule and blank guard kept.
- Tests: `test_record_selected_by_top_level_session_id` and
  `test_only_another_sessions_record_refuses_by_name`
  (`tests/test_sensei_wake_audit.py`).
- **Gate negative probe (run, passed):** a record whose `session_id` lives ONLY
  at top level resolves (`code == 0`, source = that record); a record for a
  DIFFERENT session still exits 2 and names session A's prefix in stderr with
  `calls == []`.

### C3 — `_is_byhand_read` classifies a session-keyed ack `cat` (FIXED)

- New bytes: `sensei.py:789` — the alternation gains
  `\.ack\.[0-9a-f]{8}\.json` alongside the legacy `\.ack\.json`. Narrow by
  construction: exactly 8 hex chars between the two dots, so an unrelated
  `.json` (or any other `.ack.*` spelling) never lands in (b).
- Test: `TestClassifyCall.test_session_keyed_ack_cat_is_a_by_hand_read`.
- **Auth negative probe (run, passed):** `cat
  seats/<seat>.ack.deadbeef.json` → `b` (with and without the `sessions/`
  segment); `cat seats/<seat>.ack.json` → `b`; `cat seats/<seat>.ack.dead.json`
  → `d`; `cat reports/summary.json` → `d`.

### C4 — P1 and P3 committed as real tests (DONE)

- `test_only_another_sessions_record_refuses_by_name` — **P1**: row names
  session A, the only record on disk belongs to session B → exit 2, stderr
  names A's session, `calls == []`. Uses the existing `_write_root` /
  `_set_seat_row` / `_write_rotation_record` helpers.
- `test_prime_row_with_session_id_stays_on_latest_and_legacy_ack` — **P3**: a
  PRIME row carrying a `session_id` anyway → `rotate._ack_session_id == ""`,
  the latest record is audited, the legacy `.ack.json` Read is `(b)`, the
  session-keyed ack Read is `(d)`, and `_hand_read_paths(..., "")` carries no
  session-keyed signal.
- The ephemeral `/tmp/probe_sl7124_parent.py` was deleted from the workflow;
  nothing was copied into the repo.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_sensei_wake_audit.py \
      extensions/agi/tests/test_sensei_rotate_out_audit.py \
      extensions/agi/tests/test_sensei.py -q
109 passed in 0.83s

tier-gate: phantom running record …/rescued-kid-logs/…/agent.json pid=1459751
(dead) -- skipped      <- pre-existing, unrelated environment notice

$ python3 -m pytest … -k "session_keyed or top_level or another_sessions or
      prime_row_with or threads_the_session" -v
8 passed, 101 deselected

$ # broader regression guard (all sensei/rotate readers of the changed helpers)
$ python3 -m pytest extensions/agi/tests/test_sensei_wake_audit.py \
      extensions/agi/tests/test_sensei_rotate_out_audit.py \
      extensions/agi/tests/test_sensei.py extensions/agi/tests/test_rotate.py \
      extensions/agi/tests/test_rotate_handover.py \
      extensions/agi/tests/test_rotate_g1517.py \
      extensions/agi/tests/test_rotate_recover.py \
      extensions/agi/tests/test_rotation_alerts.py \
      extensions/agi/tests/test_rotation_alert.py \
      extensions/agi/tests/test_geometry_config.py -q
551 passed, 678 warnings in 59.00s

# C1 wire probe (spy on _hand_read_paths at the call site)
C1 threaded session_id: rotate='deadbeef-1111-2222-3333-444444444444'
                        wake='deadbeef-1111-2222-3333-444444444444'
C1 threads equal: True
C1 pre-fix call site cat: ['d']
```

## Notes / residuals

- `git status --porcelain` at report time shows ONLY the three permitted files
  modified plus this scaffolded node; no unexpected files present.
- `_is_byhand_read`'s new alternative is hex-only (`[0-9a-f]{8}` after
  `_norm_cmd(...).lower()`). A row carrying a non-hex `session_id` would still
  get its ack classified `(b)` through the `_hand_read_paths` signal (that is
  the substring path), so C3 is belt-and-braces with C1, not the only guard.

## Agent Notes
C1 rotate_out_audit threads rotate._ack_session_id into _hand_read_paths (sensei.py:1628); C2 _record_matches_session reads record top-level session_id as well as handover.join (sensei.py:595); C3 _is_byhand_read matches seats/<seat>.ack.<sid8>.json (sensei.py:789); C4 P1+P3 committed as tests. 109 passed (3 named files), 551 passed broad regression; C1 wire probe proves a non-threading call site falls to (d). /tmp probe deleted.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-35f28094, SL7.125). Four conjuncts judged from the DIFF bytes, not the kid report. C1 sensei.py:1628-1629 now derives the same identity wake_audit uses and threads it into _hand_read_paths; my wire probe stubs rotate._ack_session_id to empty and the SAME Read falls to (d), so the fix is at the call site, not only in the helper. C2 _record_matches_session reads rec.get(session_id) first then lets handover.join win -- rotate._record_join's order -- so a first-seating record (top-level only) resolves; a different session still refuses by name and calls==[]. C3 _is_byhand_read gains .ack.<8 hex>.json alongside the legacy .ack.json; my auth probe confirms the keyed and legacy spells are (b) while an unrelated .json and a non-8-char token stay (d). C4 P1/P3 are committed tests using the shared fixtures; the /tmp probe is no longer a code dependency (named only as provenance). All four parent negative probes pass on the built bytes, and the three named test files are 109 green. Verdict recorded proved: this is the build the g15 order asked for.
<!-- THOUGHT:END -->
