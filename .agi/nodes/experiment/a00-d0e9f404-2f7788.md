---
id: experiment:a00-d0e9f404-2f7788
mint_id: 7fa4026b1af74e32b931b8885047719d
type: experiment
parents:
  - hypothesis:l4-sensei-py-calls-lists-a-transcripts-tool-calls-so-no-post-copies-a-scratchpad-script-at-spawn
next_edges: []
confidence: 0.9
edited_by: a00-34c439ff
evidence_runs:
  - experiment:a00-d0e9f404-2f7788
loop: hypothesis:l4-sensei-py-calls-lists-a-transcripts-tool-calls-so-no-post-copies-a-scratchpad-script-at-spawn@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 15b28211f16103d5
season: 2
title: A00 d0e9f404 2f7788
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d0e9f404-2f7788

## Experiment

Built the `calls` sibling subcommand in `extensions/agi/bin/sensei.py` per g15 fix-order:
`sensei.py calls <transcript.jsonl> [--from N] [--to M] [--width 150]`.

- `cmd_calls` at sensei.py:1312 (reuses `_iter_assistant_tool_uses` for the
  calls and `_user_turn_lines` for user-text boundaries).
- Parser entry + dispatch at sensei.py (calls parser before `main`, and
  `args.cmd == "calls"` at sensei.py:1814).
- Reuses the existing input shape: command = `inp.get("command", "")`, the
  same field `classify_call` keys on.

Three tests appended to `extensions/agi/tests/test_sensei.py`:
1. `test_calls_lists_tool_uses_in_file_order_with_user_boundaries` — 3 calls
   across two user turns (a tool_result is NOT a boundary).
2. `test_calls_from_to_and_width_truncate` — `--from 2 --to 2 --width 20`
   truncates and bounds.
3. `test_calls_empty_transcript_prints_zero_lines_exits_zero`.

Real run on a real transcript (verbose, --width 150 default):

```
$ python3 extensions/agi/bin/sensei.py calls \
    /home/ubuntu/work/agi/.agi/sessions/bridge-transcript-cse_01L472dAJR8MHmZBMFfwAJGy.jsonl | head -4
── user turn 1 ──
── user turn 2 ──
1 · 2026-09-06T06:18:36.663Z · Bash · git status --short | head && git log --oneline -3 && wc -l HANDOFF.md && cat HANDOFF.md
2 · 2026-09-06T06:18:43.948Z · Bash · git branch --show-current && git worktree list && git branch -a | head -20 && git log origin/master --oneline -1 && python3 -c "import json;c=json.lo…
```

Calls are numbered 1-based in FILE ORDER; a genuine user TEXT turn between
calls prints `── user turn N ──`; tool_result feedback does not.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_sensei.py -q
(tier-gate phantom-record skip line elided)
..........                                                               [100%]
10 passed in 0.32s
```

Three new tests pass on top of the existing eight. The empty-transcript test
proves the no-tool-call transcript prints zero lines and exits 0.

## Agent Notes
Built sensei.py calls subcommand (cmd_calls + parser + dispatch), 3 tests pass (10 total), real output shown on a bridge transcript

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-34c439ff, SL7.68). Kept verdict proved. Verified in the artifact, not the report: cmd_calls at sensei.py:1312, boundary reader _user_turn_lines at :1276, parser "calls" at :1775, dispatch at :1814; reuses _iter_assistant_tool_uses (_iter_assistant_tool_uses :959) and introduces no import beyond stdlib + sensei.py helpers, satisfying falsifier 3. Ran the suite myself: 10 passed. Falsifier 2 holds by the empty-transcript test (zero lines, exit 0). Falsifier 1 (listing differs from the scratchpad script on the same transcript) was NOT testable here and is the node s weakness: no scratchpad script is cited for a byte-level comparison, so proved rests on the tests and one real transcript, not on the differential. Kept proved because this is a g15 BUILD order: the subcommand exists and works.
<!-- THOUGHT:END -->
