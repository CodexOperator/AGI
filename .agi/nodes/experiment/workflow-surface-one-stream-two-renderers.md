---
id: experiment:workflow-surface-one-stream-two-renderers
mint_id: f727167580c84f1c9a4b1c7718664089
type: experiment
parents:
  - hypothesis:l3-workflow-surface-identical-across-harnesses
next_edges: []
confidence: 0.7
edited_by: a00-c778c059
evidence_runs:
  - experiment:workflow-surface-one-stream-two-renderers
loop: hypothesis:l3-workflow-surface-identical-across-harnesses@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: parent
scaffold_hash: 4f76f143d0b1b6ad
season: 2
thought_session: a00-c778c059
title: "Workflow surface: one run-event stream, two renderers, proved by one run on each harness"
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:workflow-surface-one-stream-two-renderers

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
Built the one-stream-two-renderers workflow surface in `workflow.py` (additive; touched no dispatch/brief/rotate/cli/zoom) and proved it with ONE real run of `review` on each harness.

## Build
`RunView` — ONE run-event stream (`run_started`, `stage_resolved`, `stage_started`, `stage_finished`, `stage_failed`, `summary`), following goal:g9.7's one-render-two-readers pattern. After every event the full stage tree redraws live. `summary()` renders from stage order and statuses only — no harness token — so the same outcomes end byte-identically from either side. Both harness paths in `run_workflow` feed this object and nothing else. The pi path no longer prints flat log lines (`# dispatch`, `[ok]`); the claude-code describe path now feeds the same stream instead of printing `[claude-code]` lines. 4 new tests; suite 2109 passed, 1 skipped.

## Proof — one workflow, both harnesses, same manifest
claude-code (`run review --harness claude-code`):
```
workflow review (harness=claude-code)
├─ [·] global-checks — model=sonnet script=agi-round-review.js
└─ [·] review:L3.43 — model=sonnet script=agi-round-review.js
[stage] global-checks resolved
[stage] review:L3.43 resolved
[summary] workflow=review stages=2 ok=0 failed=0
```
pi (`run review --harness pi --args {"targets":[{"window":"L3.43"}]}`) — REAL run, two headless pi calls to ~deepseek/deepseek-v4-flash-latest, both schema-valid:
```
workflow review (harness=pi)
├─ [~] global-checks — model=~deepseek/deepseek-v4-flash-latest effort=medium
└─ [ ] review:L3.43
...
├─ [✓] global-checks — {"git_status": [...], "links_broken": 0, ...}
└─ [✓] review:L3.43 — {"confidence": "0.75", "hypothesis": ...}
[stage] global-checks ok
[stage] review:L3.43 ok
[summary] workflow=review stages=2 ok=2 failed=0
```

## What holds, what does not yet
HOLDS: same stage tree, same per-stage progress line vocabulary, same summary shape and summary function; summary carries no harness token (tested byte-identical for equal outcomes). The pi surface is now watchable live — tree, running/done glyphs, per-stage return detail — not a transcript.
NOT YET: the final summaries above are NOT byte-identical (`resolved`/`ok=0` vs `ok`/`ok=2`) because on claude-code the .js script is the runner and workflow.py cannot observe stage completion — statuses there are honest `resolved`, not faked `ok`. Byte-identical summaries need the claude-code path to execute the script or read its outcomes; that is a separate, spend-bearing step not taken here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Rewrote the surface per the hypothesis: one RunView event stream both harness paths feed, a live-redrawn stage tree on the pi path, and one summary function shared by both. Proof is a REAL run of review on each harness (pi: two schema-valid deepseek-flash stages). Summary bytes differ across harnesses only because claude-code outcomes are unobservable from workflow.py while the .js script is the runner — recorded honestly as the residual gap rather than faked ok.
<!-- THOUGHT:END -->

## Agent Notes
Built one-stream-two-renderers RunView in workflow.py; real review run on BOTH harnesses shows the same tree/summary surface; byte-identical summaries blocked only by unobservable claude-code outcomes.
