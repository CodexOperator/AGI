---
id: experiment:durable-named-tmux-pane-hold-live-reproof
mint_id: d39c151129a447f8a655e24806b7c5c6
type: experiment
parents:
  - hypothesis:a00-814bac02-32024a
next_edges: []
confidence: 0.75
edited_by: a00-59a0ef02
evidence_runs:
  - experiment:durable-named-tmux-pane-hold-live-reproof
line_ceiling: 160
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 141
profile: balanced
rebrief_answer: proceed-with-160
rebrief_request: "Port of the prior-art seam landed and PROVED live (real tmux, same pane_id across pid churn) at 141 production lines -- the prior-art tmux_hold.py is ~113 lines by itself. Default ceiling 40 is 3.5x too small for the ordered port. Ask: raise ceiling to ~160 and merge the branch; otherwise direct a split (e.g. seam-only over two rounds)."
role: kid
scaffold_hash: fd09609a871f3bf4
season: 2
title: Durable named tmux pane hold, ported and reproved live on the DT.102 tip
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:durable-named-tmux-pane-hold-live-reproof

## Claim under test

On the DT.102 tip (`f655a6714`), a `grok-bot` restart can be made to
re-enter the SAME named tmux pane after the seat PROCESS is killed: the
immutable `#{pane_id}` survives pid churn, the pane is re-created exactly
once with `created=true` when it is genuinely gone, and another seat name
cannot take it. Opt-in seam declared in the adapter; no `grok` literal in
`dispatch.py` / `rotate.py`.

## What was built (current tip)

- **NEW** `extensions/agi/bin/adapters/tmux_hold.py` (113 lines): the seam.
  `enabled` / `pane_name` / `panes` (`-s` session-wide) / `start` (founds the
  pane with a throwaway shell, sets `remain-on-exit` on the pane, then
  `respawn-pane -k` the real argv) / `reattach` (`respawn-pane -k` on the
  immutable pane_id; if the pane is GONE, `start` once and stamp
  `created=true`). Session is the box cell `box.tmux_session`, read from the
  harness or back from the live config.
- **CHANGED** `extensions/agi/bin/adapters/grok_bot_adapter.py` (+28):
  `HOLD_PANE = True` declared in the adapter that owns the spawn shape;
  `hold_harness()` applies it unless the row states `tmux`/`pane` outright;
  `restart` routes through `tmux_hold.reattach` and stamps `agent_record["tmux"]
  = {"created": ..., "pane_id": ...}`.
- **CHANGED** `extensions/agi/tests/test_grok_bot_adapter.py` (tests only):
  the two direct-`Popen` tests now opt out with `tmux: False`; added
  `test_hold_harness_defaults_to_hold_and_honours_an_explicit_cell` and
  `test_restart_re_enters_the_named_pane_when_held`.

No edit to `dispatch.py` / `rotate.py`, and none was needed: the restart
call site already threads `rec["harness_spec"]` into `adapter.restart`, and
`hold_harness` supplies the cell an older record lacks (proved below).

## Headline evidence — LIVE tmux, real process death (raw)

Script: a real `tmux new-session`/`new-window`/`respawn-pane` run; assert the
SAME `#{pane_id}` before and after `kill -9` of the seat process.

```
== 1. START: found the pane on first spawn ==
start() -> 522634
$ tmux list-panes -s -t cand-814bac02 -F '#{window_name} #{pane_id} #{pane_pid}'
seat-cc1123d5d56b %0 522634
panes BEFORE: [('seat-cc1123d5d56b', '%0', '522634')]

== 2. KILL the seat PROCESS (pane survives via remain-on-exit) ==
$ kill -9 522634
$ tmux list-panes -s -t cand-814bac02 -F ...
seat-cc1123d5d56b %0 522634
panes AFTER kill: [('seat-cc1123d5d56b', '%0', '522634')]

== 3. RESTART -> reattach must re-enter the SAME pane id ==
reattach() -> 522647 created= {'created': False, 'pane_id': '%0'}
$ tmux list-panes -s -t cand-814bac02 -F ...
seat-cc1123d5d56b %0 522647
panes AFTER restart: [('seat-cc1123d5d56b', '%0', '522647')]
PROOF: pane_id %0 stable across pid 522634 -> 522647
```

Falsifier conjunct 1 **holds**: `%0` before, `%0` after; only the pid churned.

## Negative probes (`probes:`)

- **gate (pane genuinely gone).** `kill -9` then `kill-window -t %0`; the
  server tore down. `reattach(gone) -> 522676 created= {'created': True,
  'pane_id': '%0'}` — it re-created once and stamped `created=true`, rather
  than silently returning the old pane. Raw: `no server running on
  /tmp/tmux-1000/default` then a fresh `%0 522676`. The equal `%0` is the tmux
  SERVER counter resetting with the new server, not a stale return; the
  distinguishing signal is `created=true` + a new pane_pid.
- **seat isolation / auth.** `reattach(OTHER)` with a different agent name:
  `pane_name("a00-other-seat")` differs from `pane_name("a00-814bac02")`,
  `_pane(HOLD, other_name)` was `None`, and the other seat founded its OWN
  pane `%1` while the first seat's `%0` was untouched:
  `[('seat-cc1123d5d56b','%0','522676'), ('seat-7034d8f97091','%1','522694')]`.
- **hold gate.** `hold_harness({'adapter':'grok_bot'})['tmux'] is True`;
  explicit `{'tmux': False}` / `{'pane': False}` stays False (direct `Popen`).
- **wire (dispatch restart call site reaches the changed bytes).** Ran the
  REAL `dispatch._reap_one` restart branch against a temp project root and a
  spy adapter with a real dead pid and `harness_spec = {'adapter':
  'grok_bot','tmux':True,'tmux_session':'wire-probe-sess'}`. Raw:
  ```
  reap record: {'status': 'running', 'pid': 919191, 'restart_count': 1,
                'fail_reason': 'pid 522732 disappeared; restarted'}
  WIRE-1 PASS: dispatch restart call site delivered harness_spec:
    {'adapter': 'grok_bot', 'tmux': True, 'tmux_session': 'wire-probe-sess'}
  WIRE-2 PASS: the same harness routed to tmux_hold.reattach; Popen stub
    never saw it. pid= 555
  ```
  WIRE-2 replaced `grok.subprocess.Popen` with a raiser, so the direct path
  provably was NOT taken: the record threads to the hold, a stub never sees it.

## Repo suite (files changed / covering them)

`python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py
 extensions/agi/tests/test_adapters.py -q` -> **52 passed**. One pre-existing
 test failed first because the new default changed its path; it was corrected
 to opt out explicitly (`tmux: False`), and the hold default/path got its own
 tests — the assertion was the change working.

## Residues from the DT.43 MUR (parent order D)

- **write-log citation** and **dangling raw-capture path** belonged to two
  hypothesis nodes from an earlier tip; the raw captures here are PASTED into
  this body on purpose, so no gitignored `sessions/` path is cited.
- **tip-named-claim mismatch** is avoided: every claim above names the current
  tip `f655a6714` and was produced on it.
- The three residues are not reachable from this branch (they live on other
  branches), so they are BANKED, not faked closed.

## Rebrief / honest verdict

The ordered port is implemented and PROVED live on this tip, but it lands at
**141 production lines** against a **40-line ceiling** (2x = 80). Per the
brief I stopped at the ceiling checkpoint, set `production_lines` /`line_ceiling` / `rebrief_request`, and put this node at `pending` for the
parent's ceiling answer. Evidence is real; the verdict is withheld only
because the round is paused on the ceiling decision, not on the proof.

## Boundary honestly not crossed

First-spawn founding inside `dispatch._open_round` (prior-art branch
`a00-603fb228`) was NOT ported — it would add more over-ceiling lines and was
not needed for the falsifier as written (the pane can be founded by
`tmux_hold.start`/`reattach`, and every later restart re-enters it). Recorded
as banked, not as done.

## Agent Notes
Ported prior-art tmux_hold seam onto tip f655a6714 and PROVED live: real tmux same pane_id %0 across kill -9 and restart (created=false), pane-gone re-creates once with created=true, other seat cannot enter it; wire probe shows dispatch._reap_one restart threads harness_spec into tmux_hold.reattach while a Popen stub never sees it. 52 tests pass. STOPPED at ceiling checkpoint: 141 production lines vs ceiling 40 (2x=80); rebrief_request set on the experiment node asking for ~160.

Parent accepted with probes: same pane_id %0 across kill -9 (created=false); created=true when pane gone; seat isolation held; probe C names the banked first-spawn gap. verdict lean_proved:75, rebrief_answer proceed-with-160.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DT.102. Read the kid DIFF bytes, never its result file: tmux_hold.py (113 lines new), grok_bot_adapter.py (+28), test_grok_bot_adapter.py (+51/-1); no dispatch.py or rotate.py edit and no grok literal. Ran four parent negative probes on the kid bytes with real tmux -- A wire: start then kill -9 then reattach returned the SAME pane_id %0 with created=false; B gate: a genuinely gone pane re-creates once with created=true, never a stale id; D auth/isolation: two seat names map to two panes and one seat cannot enter another pane; C: the REAL dispatch first-spawn path founds no pane, so the first restart fabricates it. Judged inconclusive_lean_proved:75, not the kid pending: the reattach mechanism is proved, but the goal invariant one named pane per seat / no anonymous fire-and-forget does NOT hold from first spawn (honestly banked by the kid). Ceiling raised 40 to 160; the prior-art seam alone is 113 lines.
<!-- THOUGHT:END -->
