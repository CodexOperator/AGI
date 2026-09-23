---
name: agent_session
derived_from: goal:g7.32.1 first ingest 2026-09-23 -- activated from the design doc (unbracketed sibling stays inactive)
fields:
  agent_id: {type: str}
  session_id: {type: str}
  started_at: {type: str}
  source_artifact: {type: str}
  turn_count: {type: int}
  tags: {type: list}
  title: {type: str}
  edited_by: {type: str}
  thought_session: {type: str}
validation:
  required: [id, type, mint_id, title, tags]
  types:
    tags: list
    turn_count: int
spawn:
  allowed_parents: [goal]
  min_parents: 1
  max_parents: 2
---

# agent_session

A recorded agent session, ingested from a harness artifact into the graph.
**This bracketed file is the ACTIVE copy**; the unbracketed
`agent_session.md` beside it is the design doc and stays inactive.

The pre-2026-09-23 design doc declared `run_id`, `source_files` and
`input_shape` required — three fields no session artifact carries. This
activation narrows `validation.required` to what a session actually has:
`id, type, mint_id, title, tags`. Everything else is optional provenance.

ID prefix: `agent_session:<slug>`. The slug is a deterministic function of the
session identity, so a second ingest of the same artifact resolves the same
node address instead of minting a duplicate.

Minted only by `extensions/agi/bin/ingest_grok_session.py`, through
`node_writer.write_node`. A parent `goal` names the goal the session served.
