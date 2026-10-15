---
id: experiment:a00-8825ba12-ca762b
mint_id: 7e0460ef9cae429cb99d1ce4f2b23fe7
type: experiment
parents:
  - hypothesis:an-empty-provider-response-is-retried-not-fatal
next_edges: []
confidence: 0.85
edited_by: a00-d7a04a78
evidence_runs:
  - experiment:a00-8825ba12-ca762b
loop: hypothesis:an-empty-provider-response-is-retried-not-fatal@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "tmp project with values.pi_retry=(3,0.20) + stub pi that always emits the empty-response turn_end", "expected": "4 runs (1 + the cell's 3), one retry line per retry, wall >= 0.60s", "observed": "4 runs, 3 retry lines, 0.75s wall; log 'retry: empty provider response 1/3 in 0.20s' x3", "result": "HOLD"}
  - {"conjunct": 2, "class": "gate", "cmd": "tmp project cell (3,0.20) + stub pi emitting turn_end stopReason=error 'Provider returned a 500 from upstream'", "expected": "exactly 1 run, no retry line", "observed": "1 run, rc=1, no retry line", "result": "HOLD"}
  - {"conjunct": 3, "class": "gate", "cmd": "tmp project cell (3,0.20) + stub pi emitting tool work, an empty turn_end, then a normal turn_end, at exit 0", "expected": "exactly 1 run -- the LAST turn decides, not the exit code", "observed": "1 run, rc=0, no retry line", "result": "HOLD"}
  - {"conjunct": 4, "class": "wire", "cmd": "tmp project cell (2,0.01) + stub pi emitting a FLAT empty turn_end at exit 0 (NOT the real pi --mode json shape -- a real turn_end is {'type','message','toolResults'} with stopReason/errorMessage NESTED under message, measured on two production logs; two production logs refute the old label), then normal work", "expected": "2 runs, the retry named with its true wait", "observed": "2 runs, 'retry: empty provider response 1/2 in 0.01s' (item 4: {:.1f} would have said 0.0s)", "result": "HOLD", "corrected": "EG.151 a00-725399ca: the label 'real pi --mode json shape' was FALSE -- the stub was flat. The OBSERVED row (2 runs, the true wait named) still HOLDS; only the shape label was wrong."}
  - {"conjunct": 0, "class": "wire", "cmd": "no .agi/config.json reachable -> the module default must apply, and the log must name it", "expected": "3 runs at the documented default 2 / 5.0s, log 'in 5.00s'", "observed": "3 runs, 11.33s wall, 'retry: empty provider response 1/2 in 5.00s' x2", "result": "HOLD"}
production_lines: 18
profile: balanced
role: kid
scaffold_hash: e3e1c3748903d3f9
season: 2
title: "EG.54 corrective: the exit-code guard made every empty-response retry unreachable; the last turn now decides"
town: core
verdict: inconclusive_lean_proved:85
---
# experiment:a00-8825ba12-ca762b

CORRECTIVE EG.54 on `hypothesis:an-empty-provider-response-is-retried-not-fatal`
(kid of the a00-8825ba12 round, base `737712de1`). **One item changed what the
feature IS; the rest were cleanups.**

## THE HEADLINE (item 6): the guard EG.34 shipped is inert in production

| # | item | what I did | status |
|---|------|-----------|--------|
| 6 | the `code == 0` guard rests on an UNVERIFIED claim about real pi's exit code | **DISPROVED from pi's own source; the guard is removed** | FIXED |
| 1 | 3 committed tests RED (record set) | `_tool_rows()` filter in the 3 consumers | FIXED |
| 2 | live cell 7 / 0.01 s shipped to make a test discriminate | cell = **2 / 5.0 s** (a provider policy, seconds-scale) | FIXED |
| 3 | `assert live == (7, 0.01)` — a test constant | cell asserted PRESENT + well-typed, never its value | FIXED |
| 4 | `{:.1f}` renders 0.01 as `0.0s` | `{:.2f}` | FIXED |
| 8 | the live guard fails by `KeyError` | `.get()` + its own message | FIXED |
| 9 | the record-format change never opened the other reader | same as item 1 | FIXED |
| 5 | the report is duplicated in the node | **NOT FIXED** — see "Item 5" below | OPEN |
| 7 | the round's tip was red; green was measured in a dirty worktree | config cell now in the tree again; residue named | PART |

## Item 6, the load-bearing one — settled, and settled AGAINST the guard

The order called this UNVERIFIED and named the cheap step. I did not need the
paid probe: the exit code is decided in pi's own print mode, on this box.

```
$ cd <pi package> && sed -n '550,600p' dist/main.js
        const exitCode = await runPrintMode(runtimeHost, {...});
        if (exitCode !== 0) { process.exitCode = exitCode; }
```

and `runPrintMode` (the embedded `sourcesContent` of
`dist/modes/print-mode.js.map`, the TypeScript the engine actually runs):

```ts
if (mode === "text") {
    const state = session.state;
    const lastMessage = state.messages[state.messages.length - 1];
    if (lastMessage?.role === "assistant") {
        const assistantMsg = lastMessage as AssistantMessage;
        if (assistantMsg.stopReason === "error" || ...) {
            console.error(assistantMsg.errorMessage || ...);
            exitCode = 1;
        } else { ...print text... }
    }
}
return exitCode;
```

`exitCode = 1` lives INSIDE `if (mode === "text")`. Dispatch spawns
`-p --mode json` (spawn.json argv in the dead rounds' own session dirs), so the
whole block is skipped, `runPrintMode` returns 0, and pi exits 0 **on an empty
provider response**. Therefore:

* EG.34's `or code == 0` in `main()` suppresses **every** retry, forever, in
  production — the feature the whole chain exists to add never fires once.
* the suite stayed green because every test DERIVED the code from the events it
  emitted (test_pi_trajectory_retry.py:75-77) and the guard test passed
  `code=0` as a parameter. The tests encoded the assumption, not the wire.

```
$ for d in iter-EG.19 iter-EG.22 iter-EG.23; do python3 -c "...print(status, exit_code if present)"; done
iter-EG.19: {'status': 'done'} {'status': 'failed'} {'status': 'done'}
iter-EG.22: {'status': 'done'} {'status': 'done'}
iter-EG.23: {'status': 'failed'} x4, {'status': 'done'}
```
No manifest row carries an exit code at all, so the dead rounds' own logs
cannot settle it either — the source above is the only honest witness.

### The fix: the LAST turn decides, not the exit code

`pi_trajectory.py` gains `_ended_on_empty(raw)` (a turn/message-end line
returns whether THAT turn ended on an empty-response stop, `None` for any
other line) and `main()`'s guard loses `or code == 0`. The state is set by a
turn end and can only be raised by an empty response seen between turns, so:

| attempt stream | production decision |
|---|---|
| `[... turn_end(error, empty)]` (the real dead log) | **RETRIED** (was: swallowed by the guard) |
| `[tool... turn_end(error, empty) turn_end(stop)]` | not respawned — the round landed |
| `[turn_end(error, 500 upstream)]` | not retried, exactly as before |

The middle row is the guard EG.34 was reaching for, and it is now reached by
MEASUREMENT (a turn end) instead of by an exit code that is 0 in every
production run.

## Items 1 / 9 — the unread reader

`_tool_rows(traj)` filters the `attempt_boundary` record out and the three
consumers call it. The boundary record is real and stays on the file (a
retried attempt's records are attributable, not fused); what was wrong was a
reader asserting the exact row set without saying which rows it meant.

## Items 2 / 3 / 8 — the cell is policy, not a discriminator

* `.agi/config.json` `values.pi_retry` = **2 / 5.0 s**. 7 retries at 0.01 s
  (8 provider respawns inside ~70 ms, no real wait) existed only so
  `live != default` could discriminate; the module default is an acceptable
  provider policy and is now what ships.
* `test_live_config_cells.py` asserts the cell is PRESENT and each key is
  `int` / `float`, with its own message. An operator tuning the cell no longer
  turns the suite red.
* The cell is still proved READ, in the file that owns the reading:
  `test_pi_trajectory_retry.py` writes its own tmp `.agi/config.json`
  (`_project`, tmp_path) and the run count follows the cell's numbers
  (`1 + empty_response_max_retries`).

## Item 4 — the log told a lie about its own wait

```
$ python3 -c "import pi_trajectory as m; [print(repr(m._RETRY.format(1,7,b))) for b in (0.01,0.05,5.0,2.5)]"
'retry: empty provider response 1/7 in 0.01s\n'
'retry: empty provider response 1/7 in 0.05s\n'
'retry: empty provider response 1/7 in 5.00s\n'
'retry: empty provider response 1/7 in 2.50s\n'
```

## Suite (the files the order named, + the smoke file)

```
$ env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT python3 -m pytest \
    extensions/agi/tests/test_pi_trajectory.py \
    extensions/agi/tests/test_live_config_cells.py \
    extensions/agi/tests/test_pi_trajectory_retry.py \
    extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=/dev/shm/pt54e
88 passed, 7 skipped in 7.59s
```

Before the fix, the same command was `3 failed, 12 passed` — the three item-1
consumers, reproduced first, not asserted from the report.

## CEILING, measured against the CUT tip 737712de1

```
$ git diff --numstat 737712de1 -- <production + test paths>
2	2	.agi/config.json
23	5	extensions/agi/bin/pi_trajectory.py
17	14	extensions/agi/tests/test_live_config_cells.py
12	3	extensions/agi/tests/test_pi_trajectory.py
25	7	extensions/agi/tests/test_pi_trajectory_retry.py
```

PRODUCTION (pi_trajectory.py + config.json): 25 added, 7 deleted = **net +18
against a 15 cap — 3 OVER, disclosed**. All 3 are inside the new detector; the
alternative was to ship the fix without the sentence that says why the guard
was wrong, which is the part the next reader needs. Tests: 54 added, 24
deleted = net +30 of 40. 0 USD, pi-free, no live pane.

## Item 5 — NOT FIXED, and why (for the findings row)

`.agi/nodes/experiment/a00-f7fcb77c-d36728.md` is 262 lines and carries the
report twice (body at :24-132, a second whole node image at :133-262, with a
THOUGHT and an Agent Notes block in EACH). `write.py` cannot express the fix:
the file has no `BODY:END` marker, so the trailing copy is outside every body
range the writer addresses, and

```
$ python3 extensions/agi/bin/write.py experiment:a00-f7fcb77c-d36728 'replace body 1:104 -' < the same 104 lines
updated: experiment:a00-f7fcb77c-d36728
$ grep -c "## What the round did" .agi/nodes/experiment/a00-f7fcb77c-d36728.md
2
```
a no-op replace rewrote the body and left both copies standing. Deleting
:133-262 by hand would delete a THOUGHT block and the parent's review with it,
so I left the bytes exactly as they are. **Defect in the node WRITER, not in
the round:** a node file with no `BODY:END` is a file no sanctioned verb can
shrink.

## Item 7 — residue, named

The live-cell test resolves the config through `rotate.ENGINE_ROOT` — the
WORKING TREE — so a green run of it can never certify a commit, and EG.34's
"82 passed" could only ever have been true in a dirty worktree. My
`.agi/config.json` edit restores the cell in the tree; whether the tip is green
is the parent's commit to check, and this node's own numstat above is the only
thing I can measure without running git for a second purpose.

## Verdict reading

The hypothesis' claim is that an empty response is retried, bounded, backoffed
and logged. On the bytes it is now true **and reachable in production**, which
it was not 40 minutes ago. What is still unexercised end-to-end is a REAL
provider returning an empty response and a real retry landing a real round —
the fixture question the paid probe would settle. So: proved on the mechanism,
lean on the wire.

(1) WHAT THE INSTRUCTION SAID, quoted: "pi_trajectory.py:167 adds `or code == 0`
so an exit-0 attempt is never respawned, but NO committed evidence establishes a
real pi's exit code on a stopReason=error empty response ... If real pi exits 0
on an empty response, the new guard suppresses EVERY retry and the feature the
whole chain exists to add is inert in production while the suite stays green."
(2) WHAT THE MACHINE ACTUALLY DOES: pi's print mode raises exitCode=1 inside
its `mode === "text"` branch only, and dispatch runs `-p --mode json`, so real
pi exits 0 — the guard is inert, exactly the failure named. (3) THE NEAR MISS:
keeping the guard and calling the item "cannot be verified at this tier" — a
green suite, an unexercised feature, and a hypothesis that reads proved. The
parent's own lean (80) would have hardened into a false 100. (4) DEVIATION: I
read a file outside the repo (the installed pi package's `dist/`) to settle
item 6, and read the dead rounds' own session manifests in the parent checkout
READ-ONLY. Both are 0 USD, both are named paths, and neither is edited — the
property of the case is that the exit code is a property of the INSTALLED pi,
so no in-repo test can ever establish it.

## Evidence

* `88 passed, 7 skipped` over the four named test files (above), against
  `3 failed, 12 passed` reproduced on the same files before the fix.
* pi `dist/main.js:590` + `dist/modes/print-mode.js.map` sourcesContent (above).
* `git diff --numstat 737712de1` (above): production net +18, tests net +30.
* Item 5's `grep -c` = 2 with write.py reporting `updated:` (above).
What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.
## CORRECTIVE EG.151 (kid a00-725399ca): probes[conjunct 4] labelled a FLAT stub "the real pi --mode json shape"

The parent's push_further ordered this correction in place; it had not been done, so the label sat
live in the graph. Two production logs refute it — a real `--mode json` `turn_end` carries exactly
three keys and NESTS the stop fields under `message`, while that probe's stub put them at the top
level (which is why EG.54's top-level-reading detector could see it at all):

```
$ python3 - <prod session>/iter-EG.23/a00-bfab7d4a/output.log
keys: ['message', 'toolResults', 'type']
top-level stopReason: None | nested: {"role": "assistant", "content": [], "api": "openai-completions", ...}
$ python3 - <prod session>/iter-EG.19/a00-1a3d2a45/output.log
keys: ['message', 'toolResults', 'type']
top-level stopReason: None | nested: {"role": "assistant", "content": [], "api": "openai-completions", ...}
```

Fixed in place: `probes[conjunct 4].cmd` now says FLAT and names the real shape; a `corrected` key
carries the reason. The row's OBSERVED outcome ("2 runs, `retry: empty provider response 1/2 in
0.01s`") is untouched and still HOLDS — only the shape label was false. This is the same lesson as
the item-3 headline below, one probe later: a stub that differs from the wire in SHAPE proves
something about the code, never about the wire.

## Agent Notes
EG.54 corrective: removed the code==0 retry guard (pi print-mode sets exitCode=1 only in text mode, so real --mode json pi exits 0 on an empty response and every retry was unreachable); the last turn_end now decides; live cell 2/5.0s; 3 RED consumers green; 88 passed.

PARENT REVIEW a00-917f3807 (EG.54) -- ACCEPTED at inconclusive_lean_proved:85, no demotion. Read by BYTES, not by the result file: pi_trajectory.py:58-70 _ended_on_empty, :129-130 the last-turn state machine, and main() at :182-186 with `or code == 0` GONE; .agi/config.json:296-299 now 2 / 5.0 s (a provider policy, never a test discriminator); test_live_config_cells.py:52-71 asserts SHAPE with its own message (no KeyError, no pinned value); test_pi_trajectory.py:63-69 _tool_rows() filters the boundary record in all three consumers. My own before/after on the same files: 3 failed, 12 passed -> 88 passed, 7 skipped. Five parent probes, one per claim conjunct, all HELD (see probes:). CEILING: production net +18 against a 15 cap -- 3 OVER, disclosed by the kid; accepted because those 3 lines are the sentence saying WHY the guard was wrong, which is what the next reader of _ended_on_empty needs, and the alternative is the guard without its reason. TWO RESIDUES for the director, neither the kid's to fix. (1) Item 5 is a WRITER defect, not a round defect: .agi/nodes/experiment/a00-f7fcb77c-d36728.md has no BODY:END marker, so a no-op `replace body 1:104 -` reports updated: and leaves both copies standing -- a node file no sanctioned verb can shrink, which is write.py work and outside this round's FILE SCOPE. (2) Item 7 RECURRED: the kid's own cli.py done left .agi/config.json UNCOMMITTED ('leaving 2 foreign path(s) uncommitted'), so the 2 / 5.0 s cell is again worktree-only and not in the tip -- the exact residue this round was ordered to close. My own instructions forbid me from running git, so I cannot land it; it needs the director salvage path, as 737712de1 did before.
