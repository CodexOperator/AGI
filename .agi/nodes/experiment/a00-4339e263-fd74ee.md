---
id: experiment:a00-4339e263-fd74ee
mint_id: 3870f4f7613a45978cfa2f94d0015e64
type: experiment
parents:
  - hypothesis:an-empty-provider-response-is-retried-not-fatal
next_edges: []
confidence: 0.85
edited_by: director-engine
evidence_runs:
  - experiment:a00-4339e263-fd74ee
loop: hypothesis:an-empty-provider-response-is-retried-not-fatal@s2
model: stealth/space-bunny-alpha
production_lines: 6
profile: balanced
role: kid
scaffold_hash: 5813110d6c4e06b5
season: 2
title: "\"CORRECTIVE EG.141: only a turn_end decides the round — a toolResult message_end no longer masks an empty stop\""
town: core
verdict: inconclusive_lean_proved:85
---
# experiment:a00-4339e263-fd74ee — CORRECTIVE EG.141: only a turn_end may decide the round

## What I did

Base: the cut tip `dab7b02c5` (the nested-shape fix is COMMITTED there — the hypothesis node's
"the +30/-5 and +50 sit uncommitted" item was FALSE, corrected in place). One production change,
one test, and the node-text corrections the order named.

## The code claim (order item 3): a toolResult's message_end can MASK an empty turn_end

`_ended_on_empty` keyed on `("turn_end", "message_end")`, so ANY message_end answered the
last-turn question. A toolResult's message_end carries no stop fields, so it answered **False**
and overwrote the `empty=True` an earlier empty `turn_end` had set: on a stream that ORDERS a
toolResult's message_end AFTER the empty turn_end, the empty LAST turn would have gone
unretried and the round would have died on exactly the failure this chain exists to prevent.
**LATENT, not live** — no production log shows that ordering (measured; see "CORRECTIVE EG.151"
below): a strict NARROWING of the trigger that removes a hazard no round has hit.

```
$ grep -n 'turn_end",' -B2 -A6 extensions/agi/bin/pi_trajectory.py     # BEFORE
        if not isinstance(ev, dict) or ev.get("type") not in ("turn_end",
                                                              "message_end"):
$ grep -n 'turn_end")$' -B6 -A4 extensions/agi/bin/pi_trajectory.py     # AFTER
        if not isinstance(ev, dict) or ev.get("type") != "turn_end":
```

Keyed on `turn_end` and nothing else. A `message_end` that DOES carry an empty stop is still
caught, by `_is_empty_response`, which raises the flag between turns — so the trigger is not
narrowed, only moved to the right event.

## RED first, on the TIP'S OWN bytes

The wrapper was copied to `<session dir>/redrig_head/bin/` (a `bin/` tree, so `locations.py`
resolves and the config loads — the mistake the earlier rig made), and the committed test file
pointed at it with `AGI_TRAJ_WRAPPER`:

```
$ env -u TMUX -u TMUX_PANE AGI_TRAJ_WRAPPER=<scratch>/redrig_head/bin/pi_trajectory.py \
    python3 -m pytest extensions/agi/tests/test_pi_trajectory_retry.py -q -k toolresult
E       AssertionError: a toolResult message_end never masks an empty turn_end:
            ['run'] / '{"type": "turn_end", "toolResults": [], "message": {"role": "assistant",
            "stopReason": "error", "errorMessage": "Provider returned an empty response"}}\n
            {"type": "message_end", "message": {"role": "toolResult", ...}}\n'
E       assert ['run'] == ['run', 'run']
1 failed, 11 deselected in 0.21s
```

One run, no retry line: the empty response was fatal. The test asserts the RETRY, not a
literal: `runs == ["run", "run"]` plus the named retry line.

## GREEN on the built bytes

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest \
    extensions/agi/tests/test_pi_trajectory_retry.py \
    extensions/agi/tests/test_pi_trajectory.py \
    extensions/agi/tests/test_live_config_cells.py \
    extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=/dev/shm/pt141a
92 passed, 7 skipped in 7.38s
```

## The stale RED-rig headline (order item 8), re-run

`experiment:a00-b9e8e8d9-6211b4` pasted `3 failed, 8 passed`. That third failure was the rig
artifact the node itself names: its scratch wrapper sat OUTSIDE `bin/`, could not import
`locations.py`, and fell back to the module defaults instead of the test's own cell. Re-run
with the wrapper inside a `bin/` tree (a scratch reconstruction of the pre-nesting, top-level-only
detectors), on today's file:

```
3 failed, 9 passed in 1.10s
```

Two nested REDs (the claim that round made) + the masking test added here (a real RED on the
tip), with `test_the_bound_...` GREEN. On that round's own 11-test file the same rig is
`2 failed, 9 passed` — exactly what the order said.

## Ceiling, measured against the cut tip `dab7b02c5`

```
$ git diff --numstat dab7b02c5 -- <production + test paths>
10	4	extensions/agi/bin/pi_trajectory.py
23	0	extensions/agi/tests/test_pi_trajectory_retry.py
```

PRODUCTION net **+6** (cap 15 by the order's CEILING, 20 by the governing line,
`experiment:a00-b9e8e8d9-6211b4:129`); TESTS net **+23** (cap 40). 0 USD, pi-free, no live
pane, stub pi only.

## The node-text items, and what each one turned out to be on the bytes

| order item | what I did | status |
|---|---|---|
| 1 push_further "(3) sit uncommitted" | the tip is CLEAN at `dab7b02c5`; item rewritten to the residue that is real | FIXED |
| 2 stale near-miss (b) + FOR THE NEXT ROUND on `a00-b9e8e8d9` | both rewritten, each with what EG.141 actually closed | FIXED |
| 3 code: `turn_end` only + the masking test | RED→GREEN above | FIXED |
| 4/7 four contradictory ceilings | ONE governing ceiling section on the hypothesis node: **20 production / 40 test** (`a00-b9e8e8d9:129`), every other number labelled a RECORD | FIXED |
| 5 false "8 runs = 1 + 7" and "7 / 0.01" | `git show dab7b02c5:.agi/config.json` 296-298 reads **2 / 5.0**; both rows corrected, output pasted | FIXED |
| 6 "the live test pins (7, 0.01)" | read `test_live_config_cells.py:52-70`: it asserts SHAPE, never VALUE, and says so in its own docstring; corrected | FIXED |
| 8 stale RED-rig headline | re-run above; headline replaced in place, the stale line kept as a marked record | FIXED |

Item 7's fourth row (`a00-b9e8e8d9:110`, "ceiling 40, test file excluded") is a
contradiction inside that node's own body and is labelled a record in its own (4) paragraph;
the line itself was outside this round's assigned edit on that node.


## What this proves, and what it does not

It proves the last-turn decision is now keyed on the only event that ends a turn. The FIXTURE is
not the measured shape — its message_end-after-turn_end ordering is the reverse of the wire
(below) — so the proof is of a strict narrowing on a synthetic order, not of a failure that
happened. It does NOT prove a live provider returns and the retry lands a real round: every run
in this chain is a stub, so the hypothesis stays a lean.

## CORRECTIVE EG.151 (kid a00-725399ca): the fixture order is the REVERSE of the wire, so this is a latent-shape fix

The order is right about the test: `test_pi_trajectory_retry.py:225` emits
`[NESTED_TURN_EMPTY, TOOLRESULT_END]` — an empty `turn_end` FOLLOWED BY a toolResult
`message_end` — while this chain's own hypothesis says every toolResult `message_end` PRECEDES
its own `turn_end`. I measured that on a live `--mode json` session log, first-hand:

```
$ python3 - <prod session>/iter-EG.19/a00-3c15c94c/output.log   # 38 turn_end events
turn_end count: 38
toolResult message_end count: 39
toolResult message_end followed (next ending event) by another message_end: 2
...followed by turn_end: 37
seq[24:34]: [('tool_execution_end',...), ('message_start','toolResult'),
             ('message_end','toolResult'), ('tool_execution_end',...),
             ('message_start','toolResult'), ('message_end','toolResult'),
             ('turn_end','assistant',2), ('turn_start',...), ('message_start','assistant',...), ...]
```

39 of 39 toolResult `message_end`s land BEFORE the `turn_end` that carries their `toolResults`
(2 are followed by another `message_end`, still before the `turn_end`). So:

| what this round claimed | what the bytes and logs support |
|---|---|
| "the empty LAST turn went unretried and the round died" | would have, on that ordering; no production log emits it — a latent hazard, not a live failure |
| proved (mechanism) | DEMOTED to inconclusive_lean_proved:85 (the frontmatter verdict, EG.175) -- a strict NARROWING; the RED on the pre-fix bytes is real, the SHAPE is synthetic |

The code change itself is correct and is kept; only the framing is corrected — here, in the test
docstring at the same claim, and in the "fixture whose shape is the measured one" sentence above.
The trigger is not narrowed: a `message_end` that DOES carry an empty stop is still caught by
`_is_empty_response` between turns.
## ANON

No user name, home path, repo path value, host or IP appears above; the session scratch dir
is referred to by its config-free label `<session dir>` / `<scr>`.
Raw output, screenshots, logs.

## Agent Notes
CORRECTIVE EG.141: _ended_on_empty now keys on turn_end ONLY (+6 net production, +23 net test vs dab7b02c5); a toolResult message_end can no longer mask an empty turn_end - RED 1 run on the tip's bytes, GREEN 2 runs after; 92 passed, 7 skipped (the EG.141 harvest file set, NOT the whole suite); six node-text items corrected in place (false 8-run/7-0.01 config rows, the (7,0.01) value-pin claim, four ceilings reconciled to ONE governing 20/40, the stale RED-rig headline re-run to 3 failed 9 passed).

EG.175 (a00-d7a04a78): frontmatter verdict moved proved -> inconclusive_lean_proved:85, confidence 0.9 -> 0.85. The body calls its fixture a synthetic order no production log shows (latent, not live), so the narrowing stands as correct code but no longer carries a proved label.
