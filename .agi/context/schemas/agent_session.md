---
name: agent_session
active: false
derived_from: not-derived -- zero agent_session nodes exist in the corpus
---

# agent_session — INACTIVE

> Bracketed filename = active schema in this directory tree. **This filename
> is not bracketed, so this schema is inactive** and is never auto-discovered
> (`schema_registry/active_set.py`, R2.2).

**Repair, 2026-08-25:** this file had no YAML frontmatter at all, so it did
not merely load as inactive — `load_schemas_from_dir` raised
`FrontmatterError: md file missing opening '---'` and recorded it in
`SchemaRegistry.errors` on every single load. It was a permanent parse error
sitting in the schemas directory, not a dormant schema. The frontmatter above
is the minimum that makes it load; the `fields:`/`validation:`/`spawn:` blocks
are deliberately absent because there are **zero `agent_session` nodes in the
corpus** and deriving a shape from a design document rather than from nodes is
exactly what produced `run_id`, `source_files` and `input_shape` — three
required fields no node has ever carried. The prose below is preserved
verbatim as the original design intent.

## Schema

```yaml
id: "session:<agent-id>-<timestamp>"    # unique per-run
type: agent_session
agent_id: string                          # which agent ran this session
iter: integer                             # iteration number
lifecycle_state: enum[spawning, active, handoff, terminated]
parent_session: string | null             # prior session that handed off
spawned_nodes: list[string]              # node IDs this session created
spawned_verdicts: list[string]            # verdict IDs attributed here
zoom_level: enum[big, small]              # what context level was used
verdict: enum[pending, proved, disproved, inconclusive_lean_proved, inconclusive_lean_disproved]
confidence: float[0.0-1.0]
tags: list[string]
relates_to: list[string]
status: enum[open, closed]
scale: enum[big, small]
last_touched_by: string                   # agent id that last modified
```

## Lifecycle State Machine

```
spawning → active → handoff → terminated
   ↑_________|       |
   (rollback)        └──→ spawning (if re-spawned)
```

## Validation Rules

- `lifecycle_state` transitions must follow the state machine above
- `spawned_nodes` must reference existing nodes (or be creatable)
- `agent_id` must match `/^[a-z0-9-]+$/`
- `iter` must be non-negative integer
- `confidence` must be 0.0-1.0 when `verdict != pending`

## Query Patterns

- Find all sessions by agent: filter `agent_id == "<id>"`
- Find sessions in iteration: filter `iter == N`
- Find active sessions: filter `lifecycle_state == "active"`
- Get handoff trail: follow `parent_session` edges
- Attribution query: which session spawned node X? → look up node's `last_touched_by`

## Relationship to Other Schemas

- **vs hypothesis**: hypothesis nodes are spawned by sessions; session records attribution
- **vs verdict**: verdicts are created by sessions; session tracks `spawned_verdicts`
- **vs idea**: ideas are domain anchors; sessions explore and extend them
