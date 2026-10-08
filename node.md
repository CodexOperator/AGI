---
id: experiment:a00-f0bd660c-c009b4
mint_id: 5b1b2b783d7244519e8141c50ab0c42e
type: experiment
parents:
  - hypothesis:l4b13-workflow-router
next_edges: []
confidence: 0.6
edited_by: a00-4781abca
evidence_runs:
  - experiment:a00-f0bd660c-c009b4
loop: hypothesis:l4b13-workflow-router@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3e79cd51cc056ae1
season: 2
title: A00 f0bd660c c009b4
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-f0bd660c-c009b4

## Experiment (L4.33 survey of hypothesis:l4b13-workflow-router)

Survey FIRST per the L4.22 brief — do not build a router blind. Findings,
then the gap, then verification. No code changed this experiment: the
implement/verify steps are budgeted as their own kids (KID CEILING 3), and
the pre-authored minimal tracking change is handed to the next kid.

### Finding 1 — ONE router exists and routes every registered workflow (PROVED)

`extensions/agi/bin/workflow.py` (801 lines) is a live, real router, not a
stub. 5 workflows are registered and all dispatch through it:

```
$ workflow.py list
NAME             SCRIPT                 STAGES  HARNESS
drafting         agi-brief-drafting.js 2      claude-code
deep-search      agi-deep-search.js   3      pi
l3w-route-probe  agi-l3w-route-probe.js 2      pi
l4-plan-research agi-l4-plan-research.js 5      pi
review           agi-round-review.js  2      pi

$ workflow.py validate
[registry] sound: every agi-*.js is named by a sibling manifest and every
manifest stage is implemented by its script
EXIT=0
```

A workflow started the Claude Code way resolves through the SAME router
(`workflow.py run review --harness claude-code --dry-run` → 2 stages,
`model=sonnet` — the claude-code subscription-alias namespace, which is
correct here). The pi harness resolves from `harnesses.pi.models` and refuses
cross-namespace aliases fail-closed. Both harness paths feed ONE
`RunView` event stream (`hypothesis:l3-workflow-surface-identical-across-harnesses`),
so "one router" holds for the workflow layer.

### Finding 2 — the parent/kid loop is NOT routed through workflow.py, and that is structural, not a gap

`workflow.py run dispatch` fails: `FileNotFoundError: no stage manifest
dispatch.json under ('extensions','agi','workflows')`. The parent/kid loop
(`driver.sh` → `dispatch.py --tier parent/--tier kid`) is the base driver the
router's own docstring is built on ("via dispatch.py kids when harness=pi" is
a summary line). workflow.py's pi harness spawns the headless `pi -p` binary
directly per stage; it never invokes dispatch.py. dispatch.py likewise never
invokes workflow.py. This confirms the owner's intended shape (l4-plan
A:320: "the parent is kinda the built-in driver for the workflow") — the
parent/kid loop is the substrate, not a registered entry. It is the right
structure; registering it as a `dispatch.json` workflow would be wrong.

### Finding 3 — RUN tracking does not exist; a CC-started run lands NO row in the graph (UNMET, the real gap)

The hypothesis's second conjunct — "a workflow started the Claude Code way
still lands a row in graph workflow-tracking" — is FALSE as-is. Verified with
a REAL (non-dry-run) CC-harness run:

```
$ workflow.py run review --harness claude-code
workflow review (harness=claude-code)
├─ [·] global-checks — model=sonnet script=agi-round-review.js
└─ [·] review — model=sonnet script=agi-round-review.js
[stage] global-checks resolved
[stage] review resolved
[summary] workflow=review stages=2 ok=0 failed=0
EXIT=0

sessions/nodes tree hash BEFORE and AFTER the run: IDENTICAL
→ NO run row landed anywhere in the graph
```

`run_workflow`'s claude-code path only resolves+describes through `RunView`
(stdout); the pi path spawns kids but likewise writes nothing. The only graph
presence a workflow has is its static build-node-per-definition
(`extensions/agi/workflows/<name>.json` + `agi-<name>.js`), never a run row.
No file matching any run-tracking pattern exists under `.agi/`.

### Verdict

- ONE-router half: **proved** — 5 live workflows, both harnesses, sound
  registry, through one router; parent/kid loop confirmed structural.
- CC-tracking half: **unmet** — zero graph trace per real run.
- The gap is exactly as the brief pre-authored: add minimal run tracking to
  `run_workflow` so a CC (and pi) `run` appends one row to the graph's
  session area (`.agi/sessions/workflows/<key>.jsonl`), reusing the existing
  `<project>/sessions/` pattern dispatch.py already writes — not a new
  subsystem. `--dry-run` writes nothing. Tracking must never fail a real run.

## Evidence

Above: `workflow.py list` / `validate` / CC-harness dry-run + real-run
outputs with exit codes; the before/after tree-hash showing no run row lands;
`FileNotFoundError` proving the parent/kid loop is unregistered.

`python3 -m pytest extensions/agi/tests/test_workflow.py -q` → **24 passed**
(0.22s), green baseline confirming review=2 stages / global-checks / claude-code
namespace contract this survey relies on.

Existing build node for the file the next kid will change:
`.agi/nodes/build/workflow.py.md` (new version → parents
`[build:workflow.py, goal:g15]`, never `[goal:g15]` alone).
<!-- BODY:END -->

## Agent Notes
Survey: ONE router proved (5 workflows, both harnesses, sound registry via list/validate); parent/kid loop is structural base driver not a gap; CC-tracking conjunct UNMET — a real CC run lands zero graph rows (tree-hash before/after identical). Gap pre-located for implement kid.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-4781abca): accepted as-is. Re-ran the checks myself — test_workflow.py green, list/validate sound, and the FileNotFoundError on `workflow.py run dispatch` is real, so the structural-substrate reading of the parent/kid loop stands. The survey did its job: it narrowed the claim instead of building blind, and the tree-hash before/after proof for Finding 3 is exactly the evidence the implement kid needed. evidence_runs self-citing is acceptable for an experiment (it IS the run).
<!-- THOUGHT:END -->
