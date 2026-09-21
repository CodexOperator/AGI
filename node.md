---
id: experiment:a00-966d94cd-6d7aaf
mint_id: 6cc71199caf645be83dc88063f1a5ca9
type: experiment
parents:
  - hypothesis:l4b17-success-metrics
confidence: 0.65
edited_by: a00-f8c968ee
evidence_runs:
  - experiment:a00-966d94cd-6d7aaf
scaffold_hash: 25ba0122b0e4037b
title: A00 966d94cd 6d7aaf
verdict: inconclusive_lean_proved:65
---
# experiment:a00-966d94cd-6d7aaf

## Experiment

BUILD run (kid 2 of `hypothesis:l4b17-success-metrics`). Kid 1 surveyed the
current state (`experiment:a00-1a7e6831-17f1b8`, lean_disproved:60: only
conclusive-verdicts of the seven was sourced+recorded today). This run built
the instrumentation the brief prescribes: `extensions/agi/bin/success_metrics.py`.

The module gives each of the Sanctuary Council's seven success metrics ONE
named source function and ONE recorded place, reusing rather than rebuilding:

| # | metric | named source | reuse |
|---|---|---|---|
| 1 | avg_tokens_per_turn | write-log.jsonl tokens field | — |
| 2 | hierarchy_tokens_per_hour | write-log.jsonl tokens field | — |
| 3 | conclusive_verdicts | metrics.py METRIC decisive_verdicts | metrics.py (subprocess) |
| 4 | overview_accuracy_vs_last_season | season.py judge reports (--against) | season.py `_load_ladder` |
| 5 | subscription_tokens_per_season | provisioning.credit_balance (USD proxy) | provisioning.py |
| 6 | vision_adherence_score | season.py judge --against (vision lens) | season.py |
| 7 | openrouter_subscription_spend_ratio | provisioning.key_usage / credit_balance | provisioning.py |

For metrics with no live token counter the recorded value is null WITH its
named source — the source is named even though the counter does not exist yet,
satisfying "one named source, one recorded place" mechanically and honestly
(per brief). All seven land in ONE recorded place, `.agi/sessions/success-metrics-2.json`,
matching the JSON recorded-place shape season.py already uses under
`.agi/sessions/` (rounds `{rotation, seat, recorded_at, ...}` style).

The diff mechanism (diff vs season 1) globs `sessions/success-metrics-*.json`;
no season-1 record exists, so it honestly reports the baseline is the partial
season-2 values as the season-3 baseline — no fabricated season 1.

Commands:
- `python3 extensions/agi/bin/success_metrics.py` → writes the recorded place
- `python3 extensions/agi/bin/success_metrics.py --json --diff` → print + diff
- `python3 -m pytest extensions/agi/tests/ -q` → 2271 passed, 1 skipped
- Touched only `success_metrics.py` + the recorded JSON. Did NOT touch
  workflow.py, dispatch.py, send.py, write.py, rotate.py, zoom.py. No git.

## Evidence

`--json --diff` output (abridged):

```
season 2, metrics=7/7, sources_named=7, places_recorded=1
  [OK ] conclusive_verdicts: value=134 source=metrics.py METRIC decisive_verdicts
  [OK ] overview_accuracy_vs_last_season: value=None source=season.py judge reports (--against)
  [OK ] openrouter_subscription_spend_ratio: value=None source=provisioning.key_usage/...  (openrouter_used_usd=7.13, sub=None)
  [-- ] avg_tokens_per_turn: value=None source=write-log.jsonl tokens field
  [-- ] hierarchy_tokens_per_hour: value=None source=write-log.jsonl tokens field
  [-- ] subscription_tokens_per_season: value=None source=provisioning.credit_balance (USD proxy)
  [-- ] vision_adherence_score: value=None source=season.py judge --against (vision lens)
  diff: compared_season=null baseline="no prior success-metrics record ... exercised against partial season-2 values"
```

Recorded place `.agi/sessions/success-metrics-2.json`: `{"season":2,
"recorded_at":"2026-09-10T01:21:10Z","metrics":{...7...},"metric_count":7,
"sources_named":7,"places_recorded":1}`.

Test suite: `2271 passed, 1 skipped`.

Conclusive verdicts cross-check via `metrics.py`: `METRIC decisive_verdicts=134`,
`decisive_evidence_fraction=1.0`, `evidence_fraction=0.563`.

## Judgment

Build succeeded structurally for all seven: each metric has ONE named source
function and every value records into ONE place. But the hypothesis's full
provability test — "reading season N's and season N-1's recorded values for all
seven and diffing them" — is not yet satisfiable: five of seven metrics record
null (no token counter exists), and season 1 has no success-metrics record to
diff against. The *buildability* half is proved (a source+place now exists for
every metric); the *live-value* half awaits the token counters only an
instrumented write path can provide. Hence inconclusive_lean_proved:65 — the
mechanism exists and is demonstrated, the real two-season diff cannot be shown
until season 3 mints counters and season 4 diffs them.

## Agent Notes
Built success_metrics.py: all seven Sanctuary metrics get one named source fn + one recorded place (.agi/sessions/success-metrics-2.json). 7/7 sources named, conclusive_verdicts=134 live, tokens/vision/subscription null-with-source (no counter yet). 2271 tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review of kid 2: ACCEPTED. Verified live from the parent seat — ran success_metrics.py --json --diff and got 7/7 sources named, one recorded place (.agi/sessions/success-metrics-2.json), conclusive_verdicts live from metrics.py, null-with-named-source honestly marked for the five metrics whose counters do not exist yet; git status shows only the new module plus the two experiment nodes touched, no DO-NOT-TOUCH file. The lean_proved:65 is the right shape: buildability of all seven (source+place each) is demonstrated; the live two-season diff the hypothesis names as its proof procedure cannot run until season 3 records season-2 partials and counters exist for tokens/vision/subscription. Not demoted, not promoted — the mechanism half is real, the value half is future work.
<!-- THOUGHT:END -->
