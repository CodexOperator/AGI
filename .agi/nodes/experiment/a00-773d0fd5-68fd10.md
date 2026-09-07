---
id: experiment:a00-773d0fd5-68fd10
mint_id: f28900c923f1428488457585fe97f0a6
type: experiment
parents:
  - hypothesis:l3-remote-control-desktop-disconnect
next_edges: []
confidence: 0.7
edited_by: a00-6ecbb009
evidence_runs:
  - experiment:a00-773d0fd5-68fd10
loop: hypothesis:l3-remote-control-desktop-disconnect@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 57c6377c85d53b21
season: 2
title: A00 773d0fd5 68fd10
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-773d0fd5-68fd10

## Experiment

Investigated the recorded 2026-09-07 remote-control desktop disconnect on the
prime (session `cse_013kQ65Xe7UBQdyoe9Tpchd8`, debug log
`.agi/sessions/belam-S1-L3-II.log`, transcript
`~/.claude/projects/-home-ubuntu-work-agi/567c990a-….jsonl`). Aim: name the
disconnect/reconnect failure signature (hypothesis item 4), determine whether
the CLI session survives a reconnect without a new session (items 1–3), and
check whether `rotate.py status` can show remote-control attachment (FIX SHAPE).

Method: read the debug log and the session `.jsonl` around the owner-reported
window (~13:45Z, confirmed by the owner's OBSERVED note; local time is UTC-3 so
13:45Z is the log clock). Ran `rotate.py status` to capture current behavior.

### Actual disconnect sequence (from `belam-S1-L3-II.log`, Z times)

- `13:44:21.151Z` — last `CCRClient: Heartbeat sent`. Heartbeats then stop
  silently: **the disconnect itself logs NO error line** — the heartbeat stream
  just ends.
- `13:45:26.678Z` — reconnect begins: `control_request subtype=initialize` →
  `Sent control_response … result=success`, then `get_context_usage`,
  `get_workspace_diff`.
- `13:46:01.628Z` — `control_request subtype=end_session` → `Sent
  control_response … result=error`.
- `13:46:01.805Z` — `[ERROR] CCRClient: Epoch mismatch (409, reason=session_not_active), shutting down`; `[remote-bridge] v2 transport closed (code=4090)`; `handleStateChange state=failed detail="this session was ended or archived from another device or app (code 4090)"`.
- `13:46:11.826Z` — `Hook cleanup: starting teardown …`; teardown complete.

### Same event, user-visible, in the `.jsonl` transcript

`567c990a….jsonl` line 1047, `type=system`, timestamp `2026-09-07T13:46:01.810Z`:

> `Remote Control disconnected — this session was ended or archived from another device or app (code 4090)`

(Matches the debug-log teardown to within 5 ms.)

### `rotate.py status` (current)

```
$ python3 extensions/agi/bin/rotate.py status
(no agi-master or belam tmux sessions)
```

`cmd_status` only lists tmux windows + activity age; it reads no debug log, so
it cannot show whether a seat's remote-control client is attached. The FIX
SHAPE item is unimplemented.

## Evidence

- **Disconnect signature (grep patterns).** The disconnect is NOT recorded in
  the message transcript as an error; it appears as a `system` message with the
  literal text `Remote Control disconnected — this session was ended or
  archived from another device or app (code 4090)`. Grep the `.jsonl` for
  `ended or archived` / `code 4090`; grep the `--debug-file` log for
  `Epoch mismatch` / `session_not_active` / `state=failed`. The earlier
  `SSETransport: Stream read error: The socket connection was closed
  unexpectedly` + auto-reconnect is a red herring — it is the worker/API event
  stream drooping and recovering on its own (observed 13:42Z and 17:04Z in
  other sessions), NOT the GUI disconnect.
- **Session survival is conditional, not guaranteed.** A disconnect alone does
  not tear the session (heartbeats just stop). But a reconnect from a client
  whose remote-control epoch no longer matches the server (app relaunch /
  different endpoint) sends `end_session`, gets `session_not_active`, and the
  CLI session is terminated with code 4090 and torn down. The machine-side
  prime (tmux window, dispatch loop, monitors) is a separate OS process and
  survives; the specific remote-control session object does not — a NEW session
  is required. This corrects the owner's 14:10 read ("the session itself was
  never interrupted"): the session WAS ended; the work continued only because a
  fresh CLI session ("restarted") re-derived the round from saved state.
- **Background work on teardown.** `Hook cleanup: starting teardown` +
  `CCR v2 internal event writer cleared` fire at 13:46:11Z, so in-flight turns
  in that session are cut at teardown. Whether an external Workflow/Monitor
  task survives depends on it being a separate process from the claude session;
  the master dispatch loop is, so rounds still fire.
- **Transcript still meterable.** The `.jsonl` persists after teardown;
  `rotate.py meter` reads the newest transcript regardless, so metering is
  unaffected.
- **Commands run:** `python3 extensions/agi/bin/rotate.py status` (above);
  `grep -o '.\{60\}ended or archived.\{80\}' …/567c990a….jsonl`;
  python json walk of the transcript to timestamp the `system` message.

## Verdict

The conjunctive claim splits on the evidence. "Prime keeps running (tmux,
monitors, dispatched rounds)" — CONFIRMED: the dispatch loop and tmux are a
separate process and survived. "Owner can reconnect … without a new session" —
DISPROVEN: the reconnect from a non-matching epoch client ended the session
(code 4090) and a new session was required. "Any state the disconnect breaks is
named, tested and repaired" — the broken state is now precisely NAMED (4090 /
Epoch mismatch), but the FIX SHAPE (rotate.py status attachment, QUICKSTART
reconnect doc) is not implemented. Because the load-bearing "reconnect without
a new session" sub-claim fails on direct log evidence, the overall claim leans
disproved — the practical goal (prime survives, work continues) holds, but via
a new session, not a resumed one.

## Agent Notes
Analyzed recorded 2026-09-07 disconnect in belam-S1-L3-II.log + 567c990a.jsonl. Prime survives (separate process) but reconnect with stale epoch ends CLI session (4090/Epoch mismatch) - new session required. Rotate status shows no attachment. Corrects owner's 'not interrupted' read.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-6ecbb009): accepted as written. Independently re-verified the artifact against raw evidence before accepting: belam-S1-L3-II.log L6633-6642 shows the exact sequence the kid reports (inbound end_session at 13:46:01Z, error response, Epoch mismatch 409 session_not_active, state=failed code 4090, Hook cleanup teardown 10s later), and the .jsonl system message "Remote Control disconnected — ended or archived (code 4090)" is present as quoted. The disproof is load-bearing and honest: the owner reconnecting from a stale-epoch client DID end the CLI session; survival of the prime is a separate-process property, not session resumption. This corrects the owner 14:10 note, which is exactly the kind of correction the hypothesis asked for. Verdict inconclusive_lean_disproved:70 kept rather than demoted: the "reconnect without a new session" sub-claim is disproved on direct log evidence, but the conjunctive claim also contains confirmed sub-claims and the repair half (rotate.py attachment display, QUICKSTART reconnect doc) is named but unimplemented, so 70 not higher. evidence_runs names this experiment itself, which is legitimate since the experiment IS the run. Weakness kept in caveats: single-incident sample, and "end_session came from the reconnecting client" is inferred from inbound ordering, not proven from the client side.
<!-- THOUGHT:END -->

## Agent Notes
Accepted kid experiment: log evidence shows GUI disconnect reconnect with stale epoch ended the CLI session (4090/Epoch mismatch, 13:46Z); prime survived as separate process; owner's 'session never interrupted' read corrected.
