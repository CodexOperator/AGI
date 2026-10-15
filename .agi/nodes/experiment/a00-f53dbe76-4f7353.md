---
id: experiment:a00-f53dbe76-4f7353
mint_id: 15319c54674e4497ae41704f4fd3bf14
type: experiment
parents:
  - hypothesis:l4-after-join-is-performed-live-by-a-running-watch-or-by-rotate-selfs-own-tail-when-no-watcher-runs
next_edges: []
confidence: 0.9
edited_by: a00-4125554d
evidence_runs:
  - experiment:a00-f53dbe76-4f7353
loop: hypothesis:l4-after-join-is-performed-live-by-a-running-watch-or-by-rotate-selfs-own-tail-when-no-watcher-runs@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0c060c5320eed4c5
season: 2
title: A00 f53dbe76 4f7353
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f53dbe76-4f7353

## What changed

Kid 2 of hypothesis:l4-after-join-is-performed-live-by-a-running-watch-or-by-
rotate-selfs-own-tail-when-no-watcher-runs closed the end-to-end gap the
parent held `proved` open on: the step (6.4) WIRING of kid 1's fix was
verified only by reading its seams. Two new tests in
extensions/agi/tests/test_rotate_handover.py drive the REAL `cmd_rotate_self`
on the fixture root (inline_reaper=false declared in the config — absent-code
reads True by default — plus NO / ALIVE heal-watch heartbeat) and read the
rotation RECORD, so `performer == "tail"` reaching the record is proven, not
assumed:

- **T4 `test_rotate_self_tail_performs_after_join_when_no_watch`** — no
  `sessions/reaper.watch.json`, `inline_reaper=false` => `_watch_alive` False
  => `_after_join_tail_should_perform` True => the tail runs after_join at
  (6.4). The record lands a NON-EMPTY `after_join` with `performer == "tail"`,
  legacy `performed_by == "tail"`, and a `results` key present (the
  never-`{}` guarantee).
- **T5 `test_rotate_self_tail_defers_when_watch_alive`** — `_live_watch_heartbeat`
  written first => `_watch_alive` True => tail DEFERS: `rec.get("after_join")
  is None` and the `(6.4) after_join deferred to the persistent service` line
  prints. The rotation itself still succeeds (rc 0).

Docstring repair (item 3): `_after_join_performer_armed`'s docstring ended
"Missing/broken config reads armed" while the code returns False on
`locations.config_path is None` and on a config parse exception. I chose to
rewrite the SENTENCE to match the CODE (not the code to the sentence): an
absent/unparsable config must not declare the box to own the confirm — the
one who actually owns it in that state is the rotate-self tail at step (6.4),
whose own readiness is decided THERE via `_after_join_tail_should_perform`.
Making the code `armed` on a broken config would have silently withheld the
tail's `deferred: after_join` teaching on a box that cannot read its own
config. The body comments already said this ("An absent cfg / dead / stale
watch reads NOT armed"); only the long sentence disagreed.

The end-to-end drive did NOT reveal a wiring defect — kid 1's `performer="tail"`
path lands intact. (6.4) prints the tail-performed line, the record carries the
key, and the alive-watch deferral short-circuits correctly.

## Evidence

```bash
# whole file green (45 tests, was 43 + T4/T5)
python3 -m pytest extensions/agi/tests/test_rotate_handover.py -q
# >> 45 passed in 16.73s

# the two new tests alone
python3 -m pytest extensions/agi/tests/test_rotate_handover.py \
    -k "tail_performs_after_join_when_no_watch or tail_defers_when_watch_alive" -q
# >> 2 passed, 43 deselected

# rotate.py was touched (docstring only) => the after_join service suite re-run
python3 -m pytest extensions/agi/tests/test_after_join_service.py -q
# >> 20 passed
```

T4 — the REAL rotate-self (6.4) print + the record the parent reads:

```
(6.4) after_join performed by rotate-self (own tail): 0 command(s) after a 0s delay;
      record appended: True, dm sent: True
rc 0
{
  "performer": "tail",
  "performed_by": "tail",
  "delay_s": 0,
  "results": [],
  "dm": "## AFTER_JOIN OUTPUT (the SERVICE ran the rotation's after_join for you; you ran nothing)\nThis is your SECOND input, delivered `after_join_delay_s` after spawn.\n\n..."
}
```

T5 — the alive-watch deferral (record carries NO after_join):

```
(6.4) after_join deferred to the persistent service
      (agent_dispatch.inline_reaper=false, watch alive)
after_join key in record: False
```

## Thought

Kid 2 of the round. T4/T5 pass; verdict `proved`. Broadest residual is naming
(6.4) the *deferral* relies on the record NOT carrying an `after_join` key at
all — the effect is asserted (deferral line printed + key absent) rather than
by reading a recorded decision field; that is exactly the tight claim. Kid 1's
`_after_join_tail_should_perform` proves the predicate; here the call site is
driven. Docstring/sentence disagreement resolved in the node direction the
code already enforced. No new nodes, no refactors, no after_join list entries.

<!-- THOUGHT:BEGIN -->
This node closes the wiring gap the parent held proved-open: it drives the
real cmd_rotate_self step (6.4) end-to-end (T4 no-watch => tail performs;
T5 alive-watch => tail defers) and reads the rotation record, not the helper
seams kid 1's tests exercised. Also repaired the _after_join_performer_armed
docstring, which said "missing/broken config reads armed" while the code
returns False — aligned the sentence to the code, because an unreadable config
must not be declared to own the confirm (the tail owns it in that state).
<!-- THOUGHT:END -->

## Agent Notes
E2E wiring proved: T4 drives real cmd_rotate_self (inline_reaper=false, no watch) => record carries after_join performer=tail + results; T5 (alive watch) => tail defers, no after_join key. 45 handover + 20 after_join-service tests green. Docstring aligned to code (unreadable config => not armed).

PARENT REVIEW (a00-4125554d, SL7.72): accepted, verdict proved. This is the node that turns the hypothesis into a checked claim: T4 (test_rotate_handover.py:1675) drives the REAL cmd_rotate_self with inline_reaper:false and no heartbeat, and reads the rotation RECORD for a non-empty after_join with performer/performed_by == "tail"; T5 (:1719) drives the same path with a fresh live-pid heartbeat and asserts the record carries NO after_join plus the printed deferral line. I re-ran test_rotate_handover.py + test_after_join_service.py: 65 passed. The docstring repair (rotate.py:9291-9297) is correct in the node direction the code already enforced. Residual accepted as stated in the kid caveat: T5 asserts deferral by absence + print, not by a recorded decision field; and the heartbeat-liveness pid is the same process, not a foreign live watch. Also unrecorded by either kid: heal.py:885 uses locations.sessions_dir (per-worktree) while rotate reads via _sessions_dir (shared via git_common_root) — same dir only while the unit roots at the main checkout.
