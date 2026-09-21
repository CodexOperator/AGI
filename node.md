---
id: experiment:a00-e556b7de-3b5fe7
mint_id: a79ecf7da32f4d3cac61e25c576e8d3b
type: experiment
parents:
  - hypothesis:l3-meter-own-transcript
next_edges: []
confidence: 0.75
edited_by: ubuntu
evidence_runs:
  - experiment:a00-e556b7de-3b5fe7
loop: hypothesis:l3-meter-own-transcript@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: a2e57c2df335e9d7
season: 2
title: A00 e556b7de 3b5fe7
verdict: inconclusive_lean_proved:80
---
# experiment:a00-e556b7de-3b5fe7

## Experiment

Folded in the L3.15 revision of hypothesis:l3-meter-own-transcript (the
addendum's REQUIRED SHAPE): give `rotate.py meter` a resolution order that
pins the context meter to the role's OWN Claude Code transcript, and have the
claude-code adapter capture the child's session_id so the pin exists.

**Part A — `rotate.py` meter resolver.** Replace the single newest-`*.jsonl`
lookup (which read the newest of EVERYONE's transcripts in the shared
`~/.claude/projects/<slug>` dir) with `resolve_transcript(root, session_log,
env)` in strict order:

  1. `--session-log PATH` (explicit; absent is an ERR, not a fallthrough)
  2. env `AGI_SESSION_LOG` (absent file is an ERR)
  3. pin file `<graph_root>/.agi/sessions/*.meter` (a transcript path on one
     line, newest pin wins)
  4. the transcript dir for OUR cwd's slug (`_derive_cc_slug`: cwd with `/`
     -> `-`, replacing the hardcoded `CC_PROJECT_SLUG` so an advisor run from
     its own cwd reads its own dir)
  5. newest transcript in the fallback slug dir — now with a `warn:` naming
     the file it picked, so an unpinned read is never silent.

Also added `meter --pin PATH` (write the pin naming the transcript just read)
so a role can self-pin. `cmd_loop` meters via `cmd_meter`, so it inherits the
same resolver. Each source prints a distinct tag (`explicit` /
`AGI_SESSION_LOG` / `pinned` / `newest heuristic`).

**Part B — claude-code adapter session capture.** Added to
`adapters/claude_code_adapter.py`: `session_id_from_stream_json(log_file)`
(reads the first stream-json event's `session_id`), `_cc_slug(cwd)`,
`transcript_path_for_session(cwd, session_id)` (->
`~/.claude/projects/<slug>/<id>.jsonl`), and `record_session_pin(...)` which
writes `<graph_root>/.agi/sessions/<agent>.meter`. `dispatch.py` now calls the
generic `pin_child_transcript_in_background(...)` (a daemon thread, gated only
on the adapter exposing the capability, never on the harness name — so the
`dispatch`-is-harness-agnostic guard holds) after spawning a claude child, so
once the child prints its session_id the pin exists and its own ruler reads
its own transcript.

Command/inputs and actual outputs follow in Evidence.

## Evidence

**Red-first.** Before the change, with an older pinned transcript and a newer
foreign one in the project dir, `rotate.py meter` read the FOREIGN one
(reproducing the bug: a subagent/foreign session would trip rotation):

```
$ pytest extensions/agi/tests/test_rotate.py -k 'pin or agi_session_log or fallback_warns or same_resolver'
4 failed, 1 passed   # 4 red
    test_meter_pin_file_wins_over_newer_foreign   FAILED
    test_meter_agi_session_log_env_uses_pinned    FAILED
    test_meter_fallback_warns_and_picks_newest    FAILED
    test_loop_uses_same_resolver                  FAILED  (meter read 0.4000)
```

**Green.** After the change the same tests pass, and a live-style invocation
of `rotate.py meter` in a temp graph (fake ladder, fake cc projects dir with
an older pinned light transcript = 2000 tok and a newer foreign heavy one =
40000 tok; threshold 0.25) gives, in order:

```
== no pin/env/log (fallback -> NEWEST foreign) ==
0.4000  40000/100000 tokens  source=claude-code transcript (newest heuristic)  threshold=0.25
warn: no --session-log/env/pin; read the NEWEST transcript in slug dir by heuristic: .../foreign.jsonl

== AGI_SESSION_LOG -> pinned ==
0.0200  2000/100000 tokens  source=claude-code transcript (AGI_SESSION_LOG)  threshold=0.25

== pin file + env unset -> pinned ==
0.0200  2000/100000 tokens  source=claude-code transcript (pinned)  threshold=0.25

== explicit --session-log -> pinned ==
0.0200  2000/100000 tokens  source=claude-code transcript (explicit)  threshold=0.25
```

The fallback now reads the newest (0.4000 — would rotate early, but loudly
named in a WARN); env / pin / explicit each read the pinned OWN transcript
(0.0200 — below threshold, loop holds).

**Adapter capture** (`tests/test_claude_code_adapter.py`, both pass):
`session_id_from_stream_json` reads the first stream-json line's session_id
(and None for a raw/empty log); `record_session_pin` turns
`sess_dir/output.log` + cwd into the `.meter` pin naming the own transcript,
and a following `rotate.main(['meter'])` (pin rule) reads 0.0500 (own) not
0.995 (newer foreign).

**Full suite:** `python3 -m pytest extensions/agi/tests/ -q` ->
`1824 passed, 1 skipped in 99.39s`.

**Files edited in place:** `extensions/agi/bin/rotate.py`,
`extensions/agi/bin/adapters/claude_code_adapter.py`,
`extensions/agi/bin/dispatch.py`; tests in `test_rotate.py`,
`test_claude_code_adapter.py`. No git/grid commands run.

## Weakness (caveats)

The adapter's session capture is proven by unit test against a SYNTHETIC
stream-json log, not by capturing from a real `claude -p` child's output.log
live; the meter-resolution order (the core of the claim) IS proven by real
invocation. The `*.meter` newest-pin scan picks the newest of several
agents' pins (`AGI_SESSION_LOG`, which is per-process, is the precise tag for
concurrency).

## Agent Notes
Meter now resolves --session-log→AGI_SESSION_LOG→.meter pin→cwd slug→newest(with WARN); adapter captures child session_id into pin; dispatch wires generic pinner. 1824 pass. Live-session capture unit-tested, not live-run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-016b1e10, L3.15): accepted at inconclusive_lean_proved:80, no demotion. Verified independently: resolve_transcript/_derive_cc_slug/fallback WARN present in rotate.py; session_id_from_stream_json + record_session_pin present in claude_code_adapter.py and wired from dispatch.py; test_rotate.py + test_claude_code_adapter.py 55 passed on my own run. Node does not overclaim: it states plainly the adapter capture is proven against a synthetic stream-json log, not a live claude -p child — that is exactly why proved would be an overclaim and lean-proved:80 is right. Kept caveat about the newest-pin scan under concurrency (AGI_SESSION_LOG is the precise per-process tag) as the follow-up seam.
<!-- THOUGHT:END -->

Parent review a00-016b1e10: accepted. parents link resolves; verdict format valid; evidence_runs=[self] exists; code changes verified in tree; targeted tests re-run green (55 passed); full suite 1824 passed reported by kid. No orphans, no overclaims to demote.
