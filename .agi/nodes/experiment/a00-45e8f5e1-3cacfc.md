---
id: experiment:a00-45e8f5e1-3cacfc
mint_id: 3a8fc5f0075c4551b876f269d77df072
type: experiment
parents:
  - hypothesis:pin-reap-never-names-a-live-session-and-a-reap-leaves-no-stale-app-session
next_edges: []
confidence: 0.88
edited_by: a00-5aaa03c7
evidence_runs:
  - experiment:a00-45e8f5e1-3cacfc
loop: hypothesis:pin-reap-never-names-a-live-session-and-a-reap-leaves-no-stale-app-session@s2
model: stealth/space-bunny-alpha
production_lines: 45
profile: balanced
role: kid
scaffold_hash: c96dad27325ed796
season: 2
title: A live current seat session with a stale pin gets STALE-PIN, never REAP
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-45e8f5e1-3cacfc

## Conjunct (1) — a stale pin on a LIVE current session yields STALE-PIN, never REAP

Built in `extensions/agi/bin/heal.py` + `extensions/agi/tests/test_heal_pin_reap.py`.

| seam | what it is / where |
|---|---|
| `pid_alive` | the EXISTING liveness seam, injected by `_pin_reap_pass` and now forwarded into `_judge_leases(..., pid_alive=)`; default `_pid_alive` (heal.py:3150). `None` seam -> `_pid_alive` (real), so production behaviour is real liveness, tests are fake. |
| `registry_dir` | untouched — sessions still come from `_seat_sessions` only. |
| `window_path` | untouched — windows still come from `_all_windows` only. |
| `reaper` | untouched. |

### The two helpers (heal.py, just above `_judge_leases`)

```
_is_seat_current(row, s)  ->  row's OWN identity cell names THIS session
_is_alive(s, pid_is_alive) ->  ALIVE through the seam, FAIL CLOSED
```

`_is_seat_current` compares the session against the row's `session_id`, `pid`
or `window` cell (the identity cells a rotation writes into `posts.md`); it
returns False when the row names none of them.

**Where the current-session check reads its truth:**
`extensions/agi/bin/heal.py:2256` `_is_seat_current(row, s)` — the `row` dict
is the one `_pin_reap_pass` passes into `_judge_leases(..., rows, ...)` from
`_rotate._load_seats(root)` -> `geometry_config.load_rows` ->
`.agi/nodes/.geometry/posts.md`. The branch that calls it is
`extensions/agi/bin/heal.py:2355` (the `elif` immediately above
`verdict = "REAP"`).

### The branch (evaluated AFTER BELAM-UNPINNED, BEFORE the REAP fallthrough)

```python
elif _is_seat_current(row, s) and _is_alive(s, pid_is_alive):
    verdict = "STALE-PIN"
    reason = "stale pin for the seat's current session"
```

### Why STALE-PIN can never arm (read, not assumed)

`_pin_reap_pass` arms ONLY on `verdict == "REAP"`, in the single guard
`if j["verdict"] != "REAP" or not armed: continue` — so a STALE-PIN row
`continue`s before `_pin_reap_arm` and before the injected `reaper` seam, and
before the dm. I read that guard and did NOT need to add a second one; the
no-arm property is by construction. `test_stale_pin_never_arms_under_armed_mode`
runs the whole pass in `mode="armed"` with a reaper that records any call and
proves `called == [] and acted == []`.

### The watch-log line (item 3)

`_pin_reap_pass` ALREADY logs one line per non-KEEP verdict immediately above
the arm guard, carrying seat + sid + pid + window + reason; a STALE-PIN row
therefore produces exactly ONE such line per pass
(`watch: pin-reap STALE-PIN: seat=... sid=... pid=... window=... (stale pin
for the seat's current session)`). I did not add a second per-row line.
I DID extend the ONE existing per-pass summary line's verdict tuple with
`STALE-PIN`, so the counter shows it. **Bounding:** not bounded beyond the
pass cadence — the summary + per-row line are one pair per pass, exactly as for
PROTECTED/IN-FLIGHT/BELAM-UNPINNED today, and `_watch` already runs the pass
on its own interval. A seat stuck in STALE-PIN therefore repeats one line per
pass, like every other non-KEEP verdict; if that ever floods, the fix is a
`_watch_log` dedupe, which is not this kid's file.

### The three cases (tests)

| case | fixture | verdict |
|---|---|---|
| live pid, stale pin, pid == row's current session | `seat-live`, registry pid 9501, row `{session_id: sid, pid: 9501, window: @101}` | `STALE-PIN`, reason `stale pin for the seat's current session` |
| live pid, stale pin, NOT the row's current session (orphan) | `seat-orph`, row names `ffff-other` / pid 999999 / window `@424242` | `REAP` (unchanged — no blanket amnesty) |
| dead pid, row names it as current | `seat-deadc`, `pid_alive=False` | `REAP` (unchanged) |

Plus `test_stale_pin_never_arms_under_armed_mode` (pass-level).

### The falsifier I RAN (would have shown the branch absent)

I copied the edited `heal.py` into the scratch dir, deleted ONLY the
`elif _is_seat_current(...)` / `verdict = "STALE-PIN"` / `reason = ...` trio
(168 chars) -> `heal_nobranch.py`, and ran the same test file against it:

```
FAILED falsifier_test.py::test_live_current_session_with_stale_pin_is_stale_pin
      At index 0 diff: 'REAP' != 'STALE-PIN'
FAILED falsifier_test.py::test_stale_pin_never_arms_under_armed_mode
2 failed, 2 passed, 21 deselected
```

That is the pre-fix defect reproduced on the bytes: a LIVE current session with
a stale pin is `REAP`, and under `armed` the reaper IS handed the live seat.
The orphan and dead-pid tests pass on BOTH copies, which is the "not a blanket
amnesty / unchanged" half of the claim.

### Suite

```
python3 -m pytest extensions/agi/tests/test_heal_pin_reap.py -q          -> 25 passed
python3 -m pytest extensions/agi/tests/test_heal.py \
  extensions/agi/tests/test_heal_seats.py extensions/agi/tests/test_heal_watch.py \
  extensions/agi/tests/test_heal_sweep.py -q                             -> 134 passed
```

### Near-miss avoided

I nearly made STALE-PIN fire on "row carries a `session_id` cell at all" plus
"pid alive" without comparing the cell to THIS session — that would have made
every live session on an identified seat a STALE-PIN (the exact amnesty the
hypothesis forbids). The `str(...)` strip/compare on all three cells and the
"row names none -> False" guard is what keeps case 2 (orphan) at REAP.

### No new config cell

None needed, and NONE written. `reaper.pin_reap` stays untouched and unset in
the shipped `.agi/config.json` (dry-run). No real pane, pid, unit, crontab or
`~/.claude/sessions` was read or written; no test touched the live config.

### Files touched

- `extensions/agi/bin/heal.py` — 2 helpers + the one branch + the
  `pid_alive` keyword + the pass's forward + the summary-line verdict tuple.
- `extensions/agi/tests/test_heal_pin_reap.py` — 4 new tests, `_judge`'s
  helper gained a `pid_alive` passthrough.

## Agent Notes
STALE-PIN branch in _judge_leases (heal.py:2256 helpers, :2355 branch) plus 4 tests; falsified on branch-stripped bytes

PARENT REVIEW DH.368 (a00-5aaa03c7): ACCEPTED for conjunct (1). Read the bytes, not the node. heal.py:2256 _is_seat_current (session_id/pid/window identity cells, blank cell -> False), :2273 _is_alive (FAIL CLOSED), :2355 the elif ahead of verdict="REAP", :2286 the pid_alive kwarg, :2451 the summary tuple. Arm guard read at :2465 (if j["verdict"] != "REAP" or not armed: continue) -- a STALE-PIN row cannot reach _pin_reap_arm.

probes: (auth) a live pid whose seat row names NO identity cell, and one naming a DIFFERENT session/pid/window -> both still REAP, so STALE-PIN is not a blanket amnesty [PASS]. (gate) mode=armed with a recording reaper over a stale-pin current session + a true orphan: the reaper is handed the ORPHAN only, so the refusal is real and not vacuous [PASS]. (wire) the pid_alive seam flipping True/False flips STALE-PIN->REAP through _pin_reap_pass, so the flag reaches the changed bytes and a stub never sees it [PASS]. (wire, real geometry bytes) the live posts.md stream-master row -- window @5, pid 145738, session_id 55b374ac -- is recognised by _is_seat_current, so the branch has real input, not only fixture cells [PASS]. (gate, over-breadth, NOT a disproof) a session with a DIFFERENT session_id and pid that merely SHARES the row window cell also earns STALE-PIN; a pane id is reusable, so the amnesty is wider than the CURRENT session. Fails safe (non-arming), but the width is recorded for the next round.

Probe file (parent-run, not the kid suite): /data/work/agi/.agi/worktrees/post-director-engine/.agi/sessions/iter-DH.368/a00-5aaa03c7/probe_parent_1.py -> 5 passed. Note the fixture shape cost me two turns: the seats file is nodes/.geometry/seats.md with a `seats:` key (not posts.md) and a registry file needs sessionId plus a tmux cell "agi:@N.%N" -- without both the pass lists nothing and reads as a green run with zero judgements.
