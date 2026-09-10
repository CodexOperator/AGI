---
id: experiment:a00-1a7e6831-17f1b8
mint_id: 203683cdd09d42da824bfc62d7058e96
type: experiment
parents:
  - hypothesis:l4b17-success-metrics
next_edges: []
confidence: 0.6
edited_by: sanctuary-helper
evidence_runs:
  - experiment:a00-1a7e6831-17f1b8
loop: hypothesis:l4b17-success-metrics@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d2fd07f419a92da5
season: 2
thought_session: sanctuary-helper-05
title: A00 1a7e6831 17f1b8
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-1a7e6831-17f1b8

## Experiment

Survey to test `hypothesis:l4b17-success-metrics` (each of the Sanctuary Council's seven success metrics has ONE named source and ONE recorded place). New instrumentation, not a bug fix — tested current state as-is. Read each proposed data source; did NOT build `success_metrics.py` (one node = one iteration, per brief this is the discovery run).

Seven metrics and their named sources as of season 2, today:

1. **average tokens/turn** — source NONE. `.agi/sessions/write-log.jsonl` (1 line, keys: `mint_id,node_id,node_type,operation,parents,path,sha256,ts`) has no token field. No per-session manifest under `.agi/sessions/` carries token counts. ✗
2. **total hierarchy system tokens/hour** — source NONE. Same absence; spawn keys log USD spend only (`used=$` per key). ✗
3. **conclusive verdicts** — source PRESENT: `metrics.py` → `.agi/config.json` `.notebook.metrics` or the emitted METRIC stream. Live value: `decisive_verdicts=134`, `decisive_evidence_fraction=1.0`, `evidence_fraction=0.562`, `verdicts_asserting=546`, `verdicts_evidence_backed=307`. ✓ computable now.
4. **overview accuracy vs last season** — source PRESENT but not surfaced as one score: `season.py` judge + `season_names[1]=genesis`, `current_season=2`. Rollover judge data exists (`.agi/sessions/rotations/*`, `quorum/*`) but no normalized accuracy number is recorded per season. △
5. **subscription tokens per season** — source NONE. No subscription-token counter anywhere. Only spend-$ exists: provisioning key `used=$7.13/limit=$15.00`. ✗
6. **vision-adherence score** — source NONE. `season.py judge --against` exists but no derived vision-adherence number recorded. ✗
7. **OpenRouter/subscription spend ratio** — source PARTIAL. OpenRouter side real: provisioning `label=sk-or-v1-6c9…10b limit=$15.00 used=$7.13 remaining=$7.87`. Subscription-spend side absent. ♢

Commands run (all read-only): `provisioning.py status`, `spawn_budget.py status`, `metrics.py`, `season.py status`, `cat ladder.md`, `head write-log.jsonl`.

## Evidence

- `metrics.py`: `METRIC decisive_verdicts=134`, `decisive_evidence_fraction=1.0`, `evidence_fraction=0.562`, `verdicts_evidence_backed=307`, `verdicts_pending=143`, `primary_value=0.147` (outcome_coverage).
- `provisioning.py status`: `OPENROUTER_API_KEY used=$7.13 remaining=$7.87`; 13 engine keys visible; per-key `used=` USD only, no token counts. `available keys_visible=15 engine_minted=13`.
- `spawn_budget.py status`: `budget: 12/25 live`; 12 agents with `tier=parent/kid iter=L4.xx` — spawn tracking carries tier and iteration, no token numbers.
- `.agi/sessions/write-log.jsonl` = 1 line, fields `[mint_id, node_id, node_type, operation, parents, path, sha256, ts]` — no `tokens` key.
- `ladder.md`: `current_season: 2`; `season_names: {1: genesis}`.
- `season.py` subcommands: status/judge/rollover/retag/merge-up — judge records judgments, but no aggregated per-season accuracy score is materialized into one recorded place.

## Judgment

Of the seven, exactly ONE (conclusive verdicts) is today computed from one named source (`metrics.py`) and lands in the recorded METRIC stream. Two are partial (overview-accuracy has judging machinery but no normalized score; spend ratio has the OpenRouter side only). Four (tokens/turn, tokens/hour, subscription tokens/season, vision-adherence) have NO source and NO recorded place today. The hypothesis-as-current-state is satisfied for ~1 of 7 — mostly not yet true; the other six await the new instrumentation the brief describes (tokens via session/write-log enrichment, spend ratio via a recorded subscription-spend source, vision-adherence via a normalized season.py-derived score).

## Agent Notes
Surveyed all seven success metrics against live sources; only conclusive-verdicts has one source+place today, 2 partial, 4 absent. New instrumentation needed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Kid 1 ran the discovery half of the L4.25 brief and stopped before the build half. Its survey is sound and is the load-bearing evidence: 1/7 metrics sourced (conclusive verdicts via metrics.py), 2 partial (overview-accuracy, spend ratio), 4 absent (tokens/turn, tokens/hour, subscription tokens/season, vision-adherence). The lean_disproved:60 verdict overclaims in one direction: the hypothesis says each metric CAN get one named source and one recorded place, and the brief prescribes NEW instrumentation — current absence does not disprove buildability. Parent judgement: verdict stands as a statement about the current state, not the hypothesis; kid 2 inherits this survey and must attempt the build (success_metrics.py reading provisioning.py/spawn_budget.py/season.py/metrics.py sources), which is the actual test.
<!-- THOUGHT:END -->