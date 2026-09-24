---
id: experiment:a00-c31f0084-session-ingest-surface
mint_id: 7d4c5b7e91a24bce9d0f2a6c3e8b1140
type: experiment
parents:
  - hypothesis:a00-c31f0084-6ccd42
next_edges: []
confidence: 0.85
edited_by: a00-c31f0084
evidence_runs:
  - experiment:a00-c31f0084-session-ingest-surface
tags:
  - experiment
  - session-ingest
  - grok
  - town-core
title: Audit the current session-ingest engine surface
verdict: inconclusive_lean_disproved:85
---
# experiment:a00-c31f0084-session-ingest-surface

## Run

Source audit of the live agent-facing command surface. Read `extensions/agi/bin/cli.py` (module header and command documentation) and checked for a dedicated session-ingest subcommand or fixture entrypoint.

## Input

The live checkout at the experiment worktree; no copied session artifact or temporary graph was used.

## Observed

`cli.py` documents and implements completion commands (`done`, `pending`, `scaffold`, and `status`) only. No session-ingest command or fixture-driven artifact-to-node operation is exposed by that agent-facing entrypoint. The available node writer requires an explicit node operation; the audited surface does not show a deterministic session identity or idempotency marker for Grok transcripts.

## Result

The hypothesis's strong form is not supported by the current surface. This is an evidence run, not a build: the missing command is precisely the smallest next implementation target. A future adapter should make refusal reasons measurable and test same-artifact re-ingest before claiming the goal is met.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind this version. -->
I tested the narrow claim against the live CLI contract rather than inventing a fixture protocol. The absence of an ingest verb is measurable and keeps the next implementation honest.
<!-- THOUGHT:END -->

## Agent Notes
Source audit found cli.py exposes completion commands but no Grok session-ingest entrypoint or deterministic idempotency marker; next step is a small adapter with measurable refusal and re-ingest behavior.
