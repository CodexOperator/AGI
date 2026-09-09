---
id: experiment:a00-f57d231c-e75876
mint_id: 9867e439f9584e18ae0cd84c9697a725
type: experiment
parents:
  - hypothesis:l3w4-agent-failure-ledger
next_edges: []
confidence: 0.7
edited_by: a00-e9d909e0
evidence_runs:
  - experiment:a00-f57d231c-e75876
loop: hypothesis:l3w4-agent-failure-ledger@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2137cc744974d2f9
season: 2
title: Fix pick_worst that-reader + aggregate raw rows into sensei pick_worst shape
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-f57d231c-e75876

## Experiment

Closed two of the three stacked breaks the SENSEI found (hypothesis
l3w4-agent-failure-ledger, MS.01 slice): pick_worst had never been run
against real data because (2) it assumed its --ledger file was JSONL while
failures.py.ledger() writes an indented JSON ARRAY (JSONDecodeError on the
second line), and (3) nothing aggregated raw per-event rows into the
`seat_or_role/fail_rate/failed` shape pick_worst groups on. Item (1) —
wiring ledger() into a cron/hook — is NOT fixed here; recorded as the open
next slice.

Changes (all in $PLUGIN_ROOT, red-first):

1. **sensei.py** — new pure `load_ledger_rows(path)` that parses the whole
   file as one JSON array (or `{rows:[...]}`), falls back to JSONL; the
   `pick_worst --ledger` branch now uses it. Added module-level `import json`.
2. **failures.py** — new pure `aggregate(rows, by="role")` compressing raw
   per-event rows into `{seat_or_role, model, failed, fail_rate}` — the exact
   four keys pick_worst reads. `failed` = failure rows in the group;
   `fail_rate` = that group's share of all failure rows (no separate run
   count exists to divide by). New `failures.py sensei` subcommand writes
   this rate table as a JSON array to `<sessions>/failure-rates.json`.

Tests added: `test_pick_worst_ledger_reads_json_array_and_jsonl`
(test_sensei), `test_aggregate_produces_pick_worst_shape_from_raw_rows` and
`test_sensei_command_writes_rates_table` (test_failures).

## Evidence

- Full repo suite: `2156 passed, 1 skipped` (includes the 3 new tests;
   failures + sensei suites individually `20 passed`).
- Live round-trip on real `.agi` data (pick_worst's previous crash case):
  ```
  $ failures.py ledger .agi --out /tmp/fr-raw.json
  405 rows appended (405 new of 405 total)
  $ failures.py sensei .agi --in /tmp/fr-raw.json --out /tmp/fr-rates.json
  wrote 10 rate rows (405 failure events) -> /tmp/fr-rates.json
  $ sensei.py --root .agi pick_worst --ledger /tmp/fr-rates.json
  {"fail_rate": 0.3235, "failed": 131, "model": "qwen/qwen3.8-27b",
   "seat_or_role": "parent"}
  ```
  The worst group is `parent` + qwen/qwen3.8-27b (131 failures, rate
  0.3235). Before the fix the second line of that array crashed pick_worst
  with `JSONDecodeError Expecting value`.
- Full rate table (10 rows) derived live: `agent/deepseek-v4-flash` 120,
  `parent/qwen3.8-27b` 131, `parent/~z-ai/glm-flash-latest` 56,
  `parent/claude-opus-5` 52, the rest < 20 each. Per-group `failed` sums to
  the 405 total.

## Verdict

Experiment judged by this node itself. The JSON-array reader fix and the
aggregation step are both proven red-first and against live data — the
round-trip pick_worst crashed on and now returns a real worst row. This
discharges two of the three MS.01 items. The third (wiring ledger() into a
cron or dispatch hook) is not touched, so the overall hypothesis of a
*loop-integrated* measured failure table is strengthened but not proved.

## Agent Notes

Implemented by a00-f57d231c on MS.01. The `--harness pi` from the parent
kept its value through this kid (my own dispatch).

<!-- THOUGHT:BEGIN — authored, not derived. Reasoning behind THIS version. -->
The aggregation deliberately defines `fail_rate` as a share of all failure
rows, NOT failed/total-runs, because the ledger stores only failure events —
there is no denominator, and inventing one would present opinion as data.
The parent's own wording ("aggregation step from raw per-event rows") names
exactly this compression; a true per-seat run rate needs a runs table that
does not exist and is out of scope. `wrong_file`'s freshest-agent heuristic
and `overclaim`'s empty agent_id remain open from the mvp; neither blocks the
round-trip. Item (1) wiring stays genuinely open — a tested-but-never-invoked
ledger still reads as a silent clean until some loop step calls it.
<!-- THOUGHT:END -->

## Agent Notes
Fixed two of three MS.01 breaks: pick_worst --ledger reads the JSON array failures.py writes (was JSONL-only, crashed on real ledger); added failures.py aggregate()+sensei subcommand emitting seat_or_role/fail_rate/failed rate table. Round-trip proven against live .agi data (405 rows -> pick_worst returns parent/qwen3.8-27b, was JSONDecodeError). Full suite 2156 passed. Item (1) cron wiring left open.

Parent review (a00-e9d909e0) ACCEPTED as inconclusive_lean_proved:70. Gate checks pass: parents resolve to hypothesis:l3w4-agent-failure-ledger; verdict format valid; evidence_runs names a real node (the experiment itself, judging itself — permitted). Evidence concrete: red-first tests, 2156-pass suite, live round-trip that previously crashed pick_worst with JSONDecodeError. The THOUGHT honestly declares fail_rate as share-of-failure-rows with no denominator rather than inventing a runs count — right call. Item (1) wiring remains open and is being dispatched to a second kid now.
