---
id: config:workflows
type: config
parents:
  - goal:g1.14
default_harness: pi
edited_by: a00-2b046d3e
season: 2
status: active
tags:
  - geometry
  - config
  - structural
title: Workflow type registry and prime-owned default harness
---
<!-- BODY:BEGIN -->
# config:workflows

The one geometry node that owns workflow-harness resolution (hypothesis:
`l4-workflow-types-and-default-harness-are-a-geometry-node`, planted on
`goal:g1.14`). Its edit-and-commit IS the change: every `harness` here is a
commit in the graph, never a code literal, and is OWNED by the prime — the
schema `[config].md` already restricts `written_by: [owner, prime_director]`,
so a kid can neither create nor edit it.

`workflow.py run|list` resolves a workflow's default harness with NO code
fallback, reading this node in this order:

1. **per-workflow override** — a `workflows.<name>.harness` row; the config
   row `provider` and a manifest `provider` are the same per-workflow level
   and resolve first (kept so existing config rows keep working unchanged).
2. **per-type override** — the manifest's `type` names one of `types:`, and
   that type's `harness` wins.
3. **prime default** — `default_harness`.
4. **refuse loudly** — if none resolve, `workflow.py` names this node and
   refuses to invent a harness. There is no hardcoded `'pi'`.

`workflow.py validate` requires every registered manifest to declare a `type`
that is one of `types:`; an undeclared or missing `type` is refused.

## Fields

- `default_harness` — the prime-owned default every workflow/type falls back
  to. Only the prime's actor (owner / prime_director) may write it, enforced
  by the `config` schema's `written_by`.
- `types` — one row per workflow TYPE: `{name, harness, stage_shapes}`.
  `stage_shapes` is the expected stage skeleton of that type (informational
  today; a future `author` round may type-check a manifest's stages against
  it before landing). A type may name no `harness` (then its workflows fall
  through to `default_harness`).
- `workflows` — one row per registered workflow, keyed by registered name:
  `{name, type, harness?}`. `type` must be `types:`; `harness` is the
  optional per-workflow override.

## The six declared types

| type | harness | stage shapes |
|---|---|---|
| review | pi | `global-checks`, `review:{target}` |
| drafting | claude-code | `draft:{slug}`, `critic` |
| research | pi | `read`, `refute:{lens}`, `synthesize` |
| route-probe | pi | `emit`, `critic` |
| plan-research | pi | `map`, `draft`, `judge`, `verify`, `synthesize` |
| investigate-refute | pi | `investigate:{key}`, `refute:{key}` |

Every registered manifest carries a `type` naming one of the above
(deep-search→`research`, drafting→`drafting`, l3w-route-probe→`route-probe`,
l4-plan-research→`plan-research`, prime-open-questions→`investigate-refute`,
review→`review`), so `list` shows the resolved harness and the level it came
from for all six.

## Authored by a kid, landed by the prime

This file is a kid-authored SHIPPED BODY at `extensions/agi/briefs/`. A kid
is a `written_by`-excluded writer of `config` nodes, so the live node is
created by the prime at merge-up. The code (`workflow.py`) already reads the
live path `nodes/.geometry/workflows.md` and refuses loudly until it lands —
there is no code fallback in the gap, only a named missing node.