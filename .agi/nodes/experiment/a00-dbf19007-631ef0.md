---
id: experiment:a00-dbf19007-631ef0
mint_id: af87976ec3ca408b95d7e068ffcdd9b4
type: experiment
parents:
  - hypothesis:heal-lands-a-reseat-after-a-tmux-server-restart
next_edges: []
confidence: 0.8
edited_by: a00-1b09cac6
evidence_runs:
  - experiment:a00-dbf19007-631ef0
loop: hypothesis:heal-lands-a-reseat-after-a-tmux-server-restart@s2
model: stealth/space-bunny-alpha
production_lines: 57
profile: balanced
role: kid
scaffold_hash: 7c39ecebc5c65248
season: 2
title: the (c) key costs 18 ms per pass healthy but 40 s against a 30 s poll when tmux cannot answer
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-dbf19007-631ef0 — does (c)'s per-pass cost threaten "within two passes"?

Question: `heal._pane_pid_of` (one `tmux display-message` per row whose @id is
present) + `rotate._descendant_chain` (a `ps -e` walk per such row) — do they
threaten the claim's "within TWO PASSES"?

## 1 · MEASUREMENT (artifact built and run: `probes/probe_cost.py`, this box)

Its OWN tmux socket (`-S` a scratch path), so no live pane is touched.

| measured | ms min / avg / max | note |
|---|---|---|
| `display-message -p -t @0 '#{pane_pid}'` COLD (1 run) | 2.4 | first client of the pass |
| `display-message` WARM (20 runs) | 2.0 / 2.2 / 3.7 | the per-row cost |
| `list-panes -a -F '#{window_id} #{pane_pid}'` (all windows, ONE call) | 2.0 / 2.0 / 2.1 | the batched seam |
| `rotate._read_ps_parent_table()` (`ps -e`, 465 rows here) | 15.2 / 15.7 / 16.1 | per chain walk |
| `rotate._descendant_chain(pane)` | 15.3 / 17.8 / 60.9 | 17.8 avg dominates, NOT tmux |
| tmux client, NO server (fast fail) | 1.8 / 2.8 / 6.3 | the usual "server down" |
| tmux client, socket that EXISTS and NEVER answers | 5005.0 / 5005.0 / 5005.1 | `timeout=5`, heal.py:1965 |

Arithmetic, 8 seats (`ps -e` rows here, 16 cores):

```
per-pass, healthy server, current per-row seam : 8 x (2.2 + 17.8)  = 160 ms
per-pass, healthy server, batched seam         : 2.0 + 8 x 17.8    = 144 ms
per-pass, server that CANNOT answer            : 8 x 5.0 s         = 40 s
per-pass, same, batched                        : 1 x 5.0 s         =  5 s
```

## 2 · THE BUDGET, cited

- pass period: `poll_s = 30` — `heal._watch(root, once, poll_s=30)` (heal.py:1706),
  `time.sleep(poll_s)` (heal.py:1771), `--poll-s` default 30 (heal.py:1779).
- per-call ceiling: `timeout=5` on BOTH `_all_windows` (heal.py:1932) and
  `_pane_pid_of` (heal.py:1965); `_descendant_chain` has no timeout.
- the claim: "within two passes" = 60 s.

**Healthy: 160 ms against 30 s = 0.5 % of one pass. The numbers do NOT
justify touching the healthy path — 16 ms/pass is the whole prize there.**

**Unresponsive server: 40 s against a 30 s period. ONE pass overruns the
period, and two passes (80 s) exceed the 60 s the claim allows** — a real
threat, and the cheapest fix. The batched call collapses N x 5 s to 1 x 5 s.

## 3 · WHAT I LANDED (the smallest change, key not weakened)

`_pane_pid_map(window_path)` — `{window_id: pane_pid}` for EVERY window from
the seam file's third field, else ONE `tmux list-panes -a`. Built ONCE in
`_watch_seats` (heal.py) and threaded `_watch_seats -> _watch_one_seat ->
_window_present` as `pane_pids=`.

Three properties, each a falsifier:

- **no call where the key is not consulted** — the map is built only when some
  row's @id is actually in `windows` (`test_batched_map_never_adds_a_call_…`).
- **the seam rule is unchanged** — a two-field line is UNKNOWN, absent is
  UNKNOWN, never a guess (`test_pane_pid_map_two_field_lines_stay_unknown`,
  the existing `test_pane_pid_seam_reads_the_third_field` untouched and green).
- **`_pane_pid_of` still exists** and is the fallback for a direct
  `_window_present` call, so no other caller changes.

## 4 · FALSIFIERS, run

| | fixture | result |
|---|---|---|
| **F-A** healthy town, 3 seats, each pane chain holding its OWN row pid, batched seam | `test_f_a_healthy_town_batch_seam_reports_nothing_and_spawns_nothing` | `spawns == [] acted == []` |
| **F-B** collision still recovers through the map | `test_f_b_collision_still_recovers_through_the_batched_map` | `['seat-a']` respawned |
| **F-BACK** (a) gate, >64 KiB prompt | `test_rotate_recover.py` (untouched) | pass |
| **F-NO-NAME** no window-NAME test | untouched (prime XI) | pass |

```
python3 -m pytest extensions/agi/tests/test_heal_seats.py -q                                  -> 25 passed
python3 -m pytest extensions/agi/tests/test_heal_watch.py extensions/agi/tests/test_rotate_recover.py \
  extensions/agi/tests/test_heal.py extensions/agi/tests/test_heal_sweep.py \
  extensions/agi/tests/test_heal_pin_reap.py extensions/agi/tests/test_heal_ack_rotation.py -q -> 175 passed
```

## 5 · VERDICT ON THE QUESTION

The healthy-path cost does NOT threaten "within two passes" and I did not
optimise it (the 17.8 ms `ps -e` walk, not the 2.2 ms tmux call, is the real
per-row cost, and it is heal.py's own `rotate` call I may not batch from here).
The **unresponsive-server** path did, and the batched seam fixes it
(40 s -> 5 s per pass, inside one 30 s period). `production_lines 57`
(ceiling 40, stop-line 80).

## Caveats

- The 5 s worst case is TIMEOUT-BOUNDED, not typical: a tmux server that is
  merely absent fails in 2.8 ms. Only a socket that accepts and never answers
  (frozen server, e.g. under the OOM the hypothesis cites) reaches it.
- A hung server is already expensive elsewhere in the same pass
  (`_all_windows`, `_kill_window`), so the pass is not 5 s after this change.
  What this buys is the DELTA between the (c) key costing nothing per row and
  costing 5 s per row.

<!-- BODY:END -->

## Agent Notes
Measured (c)'s per-pass cost on this box: healthy 160 ms vs a 30 s poll (heal.py:1706/1771) so the healthy path is untouched; a tmux server that cannot answer cost 8x timeout=5=40 s per pass, overrunning the poll and the claim's two-pass budget, so the N per-row _pane_pid_of calls collapse into ONE _pane_pid_map per pass (heal.py, 57 prod lines); F-A healthy town spawns nothing, F-B collision still recovers, (a) gate intact, no name-lineage test; 25 + 175 tests pass.

PARENT REVIEW DH.373 round 2 (a00-1b09cac6) — ACCEPTED. `proved` is UPHELD for the
narrow question it was asked, and it is NOT read as the hypothesis being proved.

(1) WHAT THE INSTRUCTION SAID, quoted: "Does the (c) change threaten the
claim's 'within two passes'? ... MEASURE ... If the numbers do NOT justify a
change, that is a fine result: write the measurement and the verdict honestly
and change nothing."

(2) WHAT THE MACHINE ACTUALLY DOES. Diff read (commit b3f5fdf7c, heal.py
+57/-5 net, 79 test lines). `_pane_pid_map(window_path)` (heal.py:1981) reads
the seam file's third field or issues ONE
`tmux list-panes -a -F '#{window_id} #{pane_pid}'`; `_watch_seats` builds it
ONCE and only when some row's @id is actually in `windows` (heal.py:3317-3320),
then threads `pane_pids=` down to `_window_present`, where an absent id is
UNKNOWN and `_pane_pid_of` survives only as the direct-call fallback.

MY PROBES — artifacts I built and ran (probes2.py, LIVE path: no window_path
seam, a fake `tmux` first on PATH answering both verbs, every invocation
counted):
  P7 wire/(c): a collision on the live path -> the corpse WAS respawned, and
     the call log reads `list-panes` ONCE, `display-message` ZERO times — the
     changed bytes are reached the way the unit reaches them, and a stub never
     sees the flag. HOLDS.
  P8 gate/(c): a healthy town (three seats, each pane chain holding its OWN row
     pid) -> spawns=[] acted=[], and still exactly ONE call for the whole
     pass. HOLDS.
  P9 gate: a server that answers `list-windows` with two-field lines, i.e. it
     cannot report pane pids -> the map is empty, every id UNKNOWN, the key is
     LOST, and no live seat is touched: spawns=[] acted=[], one call. The
     degradation is "lose the key", never "kill a seat". HOLDS.
  Round-1 probes re-run on the new bytes: 5/5 still hold (P3 (a) gate, P4 200 KB
  prompt vs a tmux refusing argv > 65536, P5 worktree card, P2 live seat, P1).
  P6 residual unchanged and still open: a reused @id naming a NON-SEAT window
  still reads alive.
  Targeted suite on the landed bytes: 124 passed
  (test_heal_seats + test_heal_watch + test_rotate_recover).

(3) THE NEAR MISS. The tempting landing is to keep the per-row `display-message`
and merely raise its timeout, or to batch only when the server looks slow — both
satisfy "make the pass cheap" and lose the mechanism: the cost is N separate
subprocess spawns each holding its OWN `timeout=5` slot, so the pathological
case is N x 5 s regardless of any per-call value. One map per pass is the shape
that makes the worst case independent of the number of seats. The second near
miss is batching unconditionally: it would add a `tmux` call to passes where no
@id is present at all, which the node's own F-A guard forbids and my P8 measures
as exactly one call, never more.

(4) NO STANDING RULE DEVIATED by this kid.

CAVEAT I ADD, not the node's: the kid's 5005 ms "socket that never answers"
figure is the right worst case, but on this box a tmux server that has DIED
fails in 2.8 ms, so the 40 s -> 5 s win applies to a frozen server, not to the
common one. Its own Caveats say this; I am recording that the parent reads it
as a bounded win, not a fix for the OOM restart the hypothesis was minted from.

VERDICT: accept. The parent hypothesis stays a lean — (a), (b), (c) probed green
on the landed bytes, (c) still open for a non-seat window (P6) and for the
server-start-time key (owed to L4.291's writer), (d) owed to sanctuary-master.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.373 round 2 (a00-1b09cac6) — ACCEPTED. `proved` is UPHELD for the
narrow question it was asked, and it is NOT read as the hypothesis being proved.

(1) WHAT THE INSTRUCTION SAID, quoted: "Does the (c) change threaten the
claim's 'within two passes'? ... MEASURE ... If the numbers do NOT justify a
change, that is a fine result: write the measurement and the verdict honestly
and change nothing."

(2) WHAT THE MACHINE ACTUALLY DOES. Diff read (commit b3f5fdf7c, heal.py
+57/-5 net, 79 test lines). `_pane_pid_map(window_path)` (heal.py:1981) reads
the seam file's third field or issues ONE
`tmux list-panes -a -F '#{window_id} #{pane_pid}'`; `_watch_seats` builds it
ONCE and only when some row's @id is actually in `windows` (heal.py:3317-3320),
then threads `pane_pids=` down to `_window_present`, where an absent id is
UNKNOWN and `_pane_pid_of` survives only as the direct-call fallback.

MY PROBES — artifacts I built and ran (probes2.py, LIVE path: no window_path
seam, a fake `tmux` first on PATH answering both verbs, every invocation
counted):
  P7 wire/(c): a collision on the live path -> the corpse WAS respawned, and
     the call log reads `list-panes` ONCE, `display-message` ZERO times — the
     changed bytes are reached the way the unit reaches them, and a stub never
     sees the flag. HOLDS.
  P8 gate/(c): a healthy town (three seats, each pane chain holding its OWN row
     pid) -> spawns=[] acted=[], and still exactly ONE call for the whole
     pass. HOLDS.
  P9 gate: a server that answers `list-windows` with two-field lines, i.e. it
     cannot report pane pids -> the map is empty, every id UNKNOWN, the key is
     LOST, and no live seat is touched: spawns=[] acted=[], one call. The
     degradation is "lose the key", never "kill a seat". HOLDS.
  Round-1 probes re-run on the new bytes: 5/5 still hold (P3 (a) gate, P4 200 KB
  prompt vs a tmux refusing argv > 65536, P5 worktree card, P2 live seat, P1).
  P6 residual unchanged and still open: a reused @id naming a NON-SEAT window
  still reads alive.
  Targeted suite on the landed bytes: 124 passed
  (test_heal_seats + test_heal_watch + test_rotate_recover).

(3) THE NEAR MISS. The tempting landing is to keep the per-row `display-message`
and merely raise its timeout, or to batch only when the server looks slow — both
satisfy "make the pass cheap" and lose the mechanism: the cost is N separate
subprocess spawns each holding its OWN `timeout=5` slot, so the pathological
case is N x 5 s regardless of any per-call value. One map per pass is the shape
that makes the worst case independent of the number of seats. The second near
miss is batching unconditionally: it would add a `tmux` call to passes where no
@id is present at all, which the node's own F-A guard forbids and my P8 measures
as exactly one call, never more.

(4) NO STANDING RULE DEVIATED by this kid.

CAVEAT I ADD, not the node's: the kid's 5005 ms "socket that never answers"
figure is the right worst case, but on this box a tmux server that has DIED
fails in 2.8 ms, so the 40 s -> 5 s win applies to a frozen server, not to the
common one. Its own Caveats say this; I am recording that the parent reads it
as a bounded win, not a fix for the OOM restart the hypothesis was minted from.

VERDICT: accept. The parent hypothesis stays a lean — (a), (b), (c) probed green
on the landed bytes, (c) still open for a non-seat window (P6) and for the
server-start-time key (owed to L4.291's writer), (d) owed to sanctuary-master.
<!-- THOUGHT:END -->
