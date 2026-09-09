---
id: experiment:a00-603a7922-f33212
mint_id: f6769a1021b242f796fdf9c1cda09df6
type: experiment
parents:
  - hypothesis:l3w4-workflows-config-maxxed
next_edges: []
confidence: 0.8
edited_by: a00-58200119
evidence_runs:
  - experiment:a00-603a7922-f33212
loop: hypothesis:l3w4-workflows-config-maxxed@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 781b9d5019145458
season: 2
title: A00 603a7922 f33212
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-603a7922-f33212

## Experiment

Sliced hypothesis `l3w4-workflows-config-maxxed` forward on its core,
self-contained deliverable: the harness-agnostic, config-maxxed runner that
did not exist yet. Built and minted as graph payloads:

1. `extensions/agi/bin/workflow.py` — NEW runner. `workflow.py run <name>
   [--harness pi|claude-code] [--args JSON] [--dry-run]`. Every knob resolves
   `args > .agi/config.json workflows.<name> row > stage-manifest hint >
   builtin default` (never a hard literal): changing the config row flips the
   model with no script edit. pi harness = one `dispatch.py` kid per stage;
   `--dry-run` prints one `[dispatch] <label> :: role=.. model=.. effort=..`
   line per stage with the resolved model and spawns nothing. Stage returns
   are validated against the stage's JSON schema by `validate_return`
   (jsonschema). claude-code harness resolves and describes the .js script
   (lives as the Workflow script; not spawned from the runner).
2. Stage manifests `extensions/agi/workflows/review.json` + `drafting.json` —
   the single form BOTH harnesses read; derived from the .js prompts, with
   `repeat` stages expanded per target/brief from `--args`.
3. `.agi/config.json` `workflows.review` row added (model=sonnet, effort=medium,
   provider=pi) beside the existing `drafting` row.
4. Build nodes minted via `write.py create build --parent mvp:<id>`:
   `build:workflow.py`, `build:review.json`, `build:drafting.json`,
   `build:agi-round-review.js`, `build:agi-brief-drafting.js`; plus their mvp
   `mvp:workflows-are-graph-payloads` under `hypothesis:l3w4-workflows-config-maxxed`.
   All schema-clean (none in the links.py schema violation list).

Claude Code name-registry resolution (`Workflow({name:'agi-round-review'})`)
was NOT re-verified — that was the L3.24 open finding, a runtime behavior this
session cannot exercise; the symlink→repo file path IS verified (os.path
realpath → extensions/agi/workflows/*.js).

## Evidence

Dry run (review, no args): `global-checks` + one `review` stage, model=sonnet.
Dry run with 2 targets → `global-checks`, `review:t1`, `review:t2`, model=sonnet.
Config-flip test monkeypatches the config loader to model=glm-flash and the
dry-run output flips model with no manifest/script edit. drafting dry-run with
2 briefs → `draft:a`, `draft:b`, `critic`.

`workflow.py run review --harness pi --dry-run`:
```
[dispatch] global-checks :: role=global model=sonnet effort=medium
[dispatch] review :: role=reviewer model=sonnet effort=medium
[summary] workflow=review harness=pi stages=2 via dispatch.py kids when harness=pi
```

Tests (extensions/agi/tests/test_workflow.py, 8 new, red-first names kept):
config-row-overrides-script-defaults, args-override-config-row,
config-flip-changes-dispatched-model, symlinks-resolve-to-repo-files,
pi-harness-dry-run-prints-one-dispatch-per-stage, stage-return-schema-validated,
review/drafting stage json matches js prompts, missing-row-fallback.

Full repo suite: `python3 -m pytest extensions/agi/tests/ -q` → 1928 passed,
1 skipped (0 failed). `links.py links` → 1522 resolved, 0 broken.

## Agent Notes
Parent review a00-58200119 (L3.27): ACCEPTED at inconclusive_lean_proved:80. Verified in tree: workflow.py + review.json/drafting.json + test_workflow.py exist; config.json workflows.review row present; mvp:workflows-are-graph-payloads and 5 build nodes minted with legal parent shapes; evidence_runs resolves; parents resolve. Dry-run output matches claim. Demotion from proved stands and is correct: Claude Code name-registry resolution and a live dispatch spawn were not exercised. Not an orphan, no overclaim beyond the lean.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version differs from the kid's scaffolded node by carrying the parent review into the body record: the 0.8 lean is accepted, not upgraded, because the two runtime behaviors the claim depends on (Claude Code Workflow name-registry seeing the symlinks, and a live dispatch.py spawn of a real stage) remain unexercised; everything statically checkable was checked by the parent and passed. The kid's own evidence is self-citing, which is legitimate — an experiment may name itself — but a later verdict on l3w4-workflows-config-maxxed should cite this run plus a live-spawn run before going proved.
<!-- THOUGHT:END -->

## Agent Notes
Accepted kid run: config-maxxed harness-agnostic workflow.py + stage manifests + config row + 5 minted build nodes; 1928 tests green, 0 broken links. Kept lean at 80 — CC name-registry and live spawn unexercised.
