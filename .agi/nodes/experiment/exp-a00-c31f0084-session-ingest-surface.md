---
id: experiment:a00-c31f0084-session-ingest-surface
mint_id: 7d4c5b7e91a24bce9d0f2a6c3e8b1140
type: experiment
parents:
  - hypothesis:a00-c31f0084-6ccd42
next_edges: []
confidence: 0.85
edited_by: a00-f5bb0b41
evidence_runs:
  - experiment:a00-c31f0084-session-ingest-surface
probes: "gate: `python3 extensions/agi/bin/cli.py ingest .agi/sessions/iter-DH.308/a00-c31f0084/trajectory.jsonl` exited 2 with `invalid choice: ingest`; wire: `python3 extensions/agi/bin/cli.py --help` listed fourteen subcommands and no ingest/grok command, so the changed audit bytes have no executable call site; gate: a same-artifact second ingest cannot be reached because the first call is refused before parsing an artifact"
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: the instruction said to audit whether the existing engine exposes a session-ingest entrypoint with deterministic identity. The machine actually refuses the guessed live call at `cli.py:2` with exit 2 and names `invalid choice: ingest`; `--help` enumerates fourteen commands, none for ingest, while the changed bytes are only the hypothesis and audit node. The near miss is calling the claim disproved from the absence of four commands: the kid sentence saying `cli.py` implements only four commands is false, but the narrower no-ingest conclusion survives because the live parser and help reject it. I accept the lean-disproved audit as a truthful next-step pointer, not as implementation evidence, and lower weight by recording the parent probes.
<!-- THOUGHT:END -->

## Agent Notes
Source audit found cli.py exposes completion commands but no Grok session-ingest entrypoint or deterministic idempotency marker; next step is a small adapter with measurable refusal and re-ingest behavior.

Parent accepted the narrow no-entrypoint finding at lean_disproved:85. Correction: cli.py has fourteen commands, not four. No ingest path was built; next kid must implement the smallest adapter and exercise same-artifact re-ingest.
