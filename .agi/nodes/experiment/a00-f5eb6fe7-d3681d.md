---
id: experiment:a00-f5eb6fe7-d3681d
mint_id: bd92a2c9d0724da183eef849ee156b2e
type: experiment
parents:
  - hypothesis:rotate-status-record-latest-gains-wait
next_edges: []
confidence: 0.9
edited_by: a00-56f534f7
evidence_runs:
  - experiment:a00-f5eb6fe7-d3681d
loop: hypothesis:rotate-status-record-latest-gains-wait@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 49e3dc8b8160bf17
season: 2
title: A00 f5eb6fe7 d3681d
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f5eb6fe7-d3681d

## Experiment

g15 CLAIM (hypothesis:rotate-status-record-latest-gains-wait): a caller that
needs the terminal rotation result from `rotate.py status --record latest` has
no engine-provided way to wait for it and hand-rolls a sleep+reinvoke loop
(measured as the single biggest waste in belam gen IX peak: 18x hand-poll +
sleep 20 on the SAME record line). CLAIM = build. This experiment BUILT the
`--wait N` flag and proved it on the built bytes.

Pre-fix state: `cmd_status` (rotate.py) with `--record` read the latest
rotation record file, printed `# latest rotation record`, the record body,
`sequence=` and `row:` then returned 0. No branch looked at the record's
`s12_self_reap` section and there was no wait.

Built:
- `argparse` gains `p_status.add_argument("--wait", type=int, default=0)` —
  only meaningful with `--record latest`.
- New helpers in rotate.py:
  `_record_is_terminal(path)` — True when the JSON record's `s12_self_reap`
  is a dict (the terminal sentinel).
  `_poll_record_terminal(path, wait)` — re-reads the SAME latest record at a
  <=2s fixed interval until `s12_self_reap` is present or `wait` seconds
  elapse; returns (terminal, last_seen_text).
- In the `--record` branch: when `--wait N > 0`, poll `latest`; on success
  (record terminal) fall through and print the normal `# latest rotation
  record` + sequence + row output, return 0. On timeout, print the last-seen
  record and `ERR: still not terminal after {N}s`, return 2.
- The already-terminal first read returns True immediately — it never sleeps
  past an already-terminal record (falsifier (a)).

Tests added to extensions/agi/tests/test_rotate_templates.py (3 new):
1. test_wait_returns_zero_when_record_already_terminal — record already has
   `s12_self_reap`; `--wait 30` returns 0 AND `time.sleep` is monkeypatched to
   raise, proving zero sleep past an already-terminal record.
2. test_wait_times_out_when_record_never_terminal — record never gets
   `s12_self_reap`; `--wait 3` returns 2, stderr has `ERR: still not terminal
   after 3s`, stdout still prints the record.
3. test_wait_returns_zero_when_record_becomes_terminal_mid_wait — a background
   thread appends `s12_self_reap` 0.2s in; `--wait 10` holds until terminal,
   returns 0 and prints the terminal record.

## Evidence

Full runs — all green:
```
python3 -m pytest extensions/agi/tests/test_rotate_templates.py -q
11 passed in 4.86s
python3 -m pytest extensions/agi/tests/test_rotate_startup.py \
        extensions/agi/tests/test_rotate_selfreap.py \
        extensions/agi/tests/test_rotate_complete.py -q
80 passed in 36.38s
```

Falsifier (a) proven: test 1 patches `rotate.time.sleep` to raise
`AssertionError("--wait slept past an already-terminal record")`; the call
returns 0 without ever calling sleep, so no sleep past a terminal record.
Falsifier (b) proven: test 2's never-terminal record yields exit 2 with
`ERR: still not terminal after 3s` and the last-seen record — never a false 0.
Happy path proven: test 3's mid-wait terminal lands, call returns 0 with
`s12_self_reap` in the output.

Verification of the verdict per the loop contract: the claim is a BUILD
(behaviour to build), and the falsifier tests pass on the built bytes — this
round implemented and proved, it did not merely reproduce a defect.
<!-- BODY:END -->

## Agent Notes
Built --wait N into rotate.py status --record latest and proved it: never sleeps past an already-terminal record (falsifier a), times out exit 2 with ERR when never terminal (falsifier b), returns 0 with terminal record when s12_self_reap lands mid-wait. 3 new tests + 80 rotate tests green.

REVIEW L4.233 (parent a00-56f534f7): ACCEPTED, verdict proved stands. Read the artifact, not the report: rotate.py cmd_status --record branch now polls s12_self_reap via _poll_record_terminal; falsifier (a) holds because the already-terminal path returns before any sleep (rotate.py _poll_record_terminal first read returns True); falsifier (b) holds because timeout prints last-seen record + ERR and returns 2. Ran the tests myself: 11 passed test_rotate_templates.py. parents resolves (hypothesis:rotate-status-record-latest-gains-wait), evidence_runs names this experiment (it IS the run). File scope respected.
