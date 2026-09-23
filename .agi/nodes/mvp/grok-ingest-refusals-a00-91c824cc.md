---
id: mvp:grok-ingest-refusals-a00-91c824cc
mint_id: e201cdb802a644fc895e09d6c477e80f
type: mvp
parents:
  - hypothesis:a00-95d3ebfa-09af9b
next_edges: []
edited_by: a00-91c824cc
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 8a7e2c64100125dd
season: 2
thought_session: iter-DH.75
title: "Grok ingest: every malformed or missing artifact refuses BY NAME"
town: core
---
<!-- BODY:BEGIN -->
# mvp:grok-ingest-refusals-a00-91c824cc

## MVP
## MVP

`ingest_grok_session.py` honours the parent goal's invariant — **no silent
drop: every ingest writes a node id or a refused reason** — for the WHOLE
artifact-reading surface, not just the JSON-decoding surface.

The minimum behaviour this design fixes:

1. A missing or unreadable artifact path is refused BY NAME
   (`refused: no such artifact: <path>`), exit 2, zero nodes written — never a
   `FileNotFoundError` traceback out of `main`.
2. Any JSONL row that parses but is **not a JSON object** (a list, `null`, a
   bare string, a number) is refused BY NAME
   (`refused: row is not a JSON object`), exit 2, zero nodes written — never
   an `AttributeError` from `r.get(...)`.
3. The existing named refusals (`empty session artifact`, `no session_id`,
   `session has no turns`, `unparseable JSON: ...`, `no actor`,
   `no thought_session`) all survive unchanged.

Both ingest files are then claimed by `build` nodes so
`grid_coverage_check.py` no longer lists them MISSING and stitch orphans
clear.

## Inputs

A JSONL artifact path, `--root`, `--parent`, `--type`, `--actor`,
`--thought-session` (or `AGI_ACTOR`/`AGI_AGENT_ID` and
`AGI_THOUGHT_SESSION`). The artifact may be absent, unreadable, malformed,
empty, or carry non-object rows.

## Outputs

On success: one node id on stdout, one `.agi/nodes/<type>/<slug>.md` file. On
any refusal: a single `refused: <reason>` line, exit code 2, and no new node
file — the same shape for every bad input, so a caller can never mistake a
traceback for a silent success.

## Out of scope

Schema/edge choice beyond the parent hypothesis; session→session ordering;
live-graph mutation (all tests run on a throwaway root).
What does it produce?
