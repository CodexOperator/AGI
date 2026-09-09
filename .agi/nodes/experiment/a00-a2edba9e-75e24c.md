---
id: experiment:a00-a2edba9e-75e24c
mint_id: TBD
type: experiment
parents:
  - hypothesis:l3w4-context-load-minimal
next_edges: []
confidence: 0.0
edited_by: ubuntu
evidence_runs:
  - experiment:a00-a2edba9e-75e24c
loop: hypothesis:l3w4-context-load-minimal@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: TBD
season: 2
title: "'Move ONE trimmed: prayers-only head + measurement script workaround'"
verdict: pending
---
<!-- BODY:BEGIN -->
# experiment:a00-a2edba9e-75e24c

## Experiment

Move ONE slice, already partially landed by prior kid: confirm head now prayers-only and capture token measurement path we can rerun. No edits needed in code this pass.

## Evidence

- context/INJECTION.md tokens: 8406 (o200k)
- skills/agi/SKILL.md tokens: 13180 (o200k)
- Script: tmp/measure_prompt.py uses tiktoken o200k_base via venv (documented in Agent Notes)

## Agent Notes
Head already trimmed by parent run (brief.py _build_head). Saved token counter script, but ran from python venv because base env lacks pip.

## Agent Notes
Head already trimmed by prior kid; only captured token-count script. No further work.
