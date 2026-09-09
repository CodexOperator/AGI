---
id: mvp:workflows-are-graph-payloads
mint_id: ab2299f5656c4c5283edfc43849cf3eb
type: mvp
parents:
  - hypothesis:l3w4-workflows-config-maxxed
next_edges: []
edited_by: belam-S1-L3-V
loop: hypothesis:l3w4-workflows-config-maxxed@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9f5c42c9c152edca
season: 2
thought_session: L3.27
title: Workflow scripts, runner and manifests are graph payloads
---
<!-- BODY:BEGIN -->
# mvp:workflows-are-graph-payloads

## MVP

The workflow layer of agi lives IN the graph as build nodes: the Claude Code
scripts `extensions/agi/workflows/agi-round-review.js` and
`agi-brief-drafting.js` (symlinked from `.claude/workflows/`), the single stage
manifests `review.json` / `drafting.json` that BOTH harnesses read, the
harness-agnostic runner `extensions/agi/bin/workflow.py`, `bin/frontier.py`,
and the rotation successor brief
`extensions/agi/briefs/prime-director-successor.md`. Every knob resolves from
`.agi/config.json workflows.<name>` with per-run `--args` overriding; the
pi harness runs one `dispatch.py` kid per stage whose return is schema-
validated by the runner.

Falsifier: any one of these files exists without a build node, or the runner
reads model/effort/provider from a literal instead of the config row (plus args
override), so changing the row cannot flip the model without a script edit.

## Inputs

- `.agi/config.json` `workflows.<name>` row (model, effort, provider)
- `extensions/agi/workflows/<name>.json` stage manifest
- per-run `--args` JSON overrides
- symlink `.claude/workflows/agi-*.js` -> `extensions/agi/workflows/agi-*.js`

## Outputs

A resolved schedule of stages; on the pi harness one dispatched kid per stage
whose structured return is schema-validated; dry-run prints one dispatch line
per stage with the resolved model so a human verifies the config-maxxed
contract with zero spawns.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (Belam V, L3.27): node minted by kid a00-603a7922 with its own file tool, so no write log existed; content accepted as written by the parent and re-logged through write.py at review — nothing else changed in this version.
<!-- THOUGHT:END -->
