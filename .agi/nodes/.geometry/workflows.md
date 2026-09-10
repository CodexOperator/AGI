---
id: config:workflows
mint_id: 7b5b36b813e2414e9cff438c94530fac
type: config
parents:
  - goal:g1.14
next_edges: []
default_harness: pi
edited_by: belam-S1-L4-VI
locations: {}
scaffold_hash: ecc9a7f9f209d906
season: 2
spawn_check: unverified
spawn_check_reason: no active schema for type 'config'
thought_session: belam-S1-L4-VI
title: Workflow type registry and the prime-owned default harness
types:
  - {"name": "review", "harness": "pi", "stage_shapes": ["global-checks", "review:{target}"]}
  - {"name": "drafting", "harness": "claude-code", "stage_shapes": ["draft:{slug}", "critic"]}
  - {"name": "research", "harness": "pi", "stage_shapes": ["read", "refute:{lens}", "synthesize"]}
  - {"name": "route-probe", "harness": "pi", "stage_shapes": ["emit", "critic"]}
  - {"name": "plan-research", "harness": "pi", "stage_shapes": ["map", "draft", "judge", "verify", "synthesize"]}
  - {"name": "investigate-refute", "harness": "pi", "stage_shapes": ["investigate:{key}", "refute:{key}"]}
workflows:
  - {"name": "review", "type": "review"}
  - {"name": "drafting", "type": "drafting"}
  - {"name": "deep-search", "type": "research"}
  - {"name": "l3w-route-probe", "type": "route-probe"}
  - {"name": "l4-plan-research", "type": "plan-research"}
  - {"name": "prime-open-questions", "type": "investigate-refute"}
---
<!-- BODY:BEGIN -->
# config:workflows

The one geometry node that owns workflow-harness resolution
(`hypothesis:l4-workflow-types-and-default-harness-are-a-geometry-node`, L4.111,
planted on `goal:g1.14`; owner ask 2026-09-10 verbatim in
`doc:l4-owner-decisions`). Its edit-and-commit IS the change: every `harness`
here is a commit in the graph, never a code literal, and is OWNED by the prime —
the `config` schema restricts `written_by: [owner, prime_director]`, so a kid
can neither create nor edit it. Created by the Prime L4-VI ahead of merge-up 20
from the body L4.111 shipped (`extensions/agi/briefs/workflows.geometry.md`),
with the six `types` rows and six `workflows` rows moved from the shipped
body's table into frontmatter, where `workflow.py` reads them.

`workflow.py run|list` resolves a workflow's harness with NO code fallback, in
this order:

1. **per-workflow** — the config row `provider` and a manifest `provider`
   resolve first (kept so existing rows keep working; 3 of 6 workflows carry
   one, so a node override for those is a no-op until a later round drops
   `provider` from the manifests — `list` prints the level, so it is visible,
   not silent), then a `workflows.<name>.harness` row here.
2. **per-type** — the manifest's `type` names one of `types:`; that type's
   `harness` wins.
3. **prime default** — `default_harness`.
4. **refuse loudly** naming this node. There is no hardcoded `'pi'`.

`workflow.py validate` requires every registered manifest to declare a `type`
that is one of `types:`; an undeclared or missing `type` is refused.

## Fields

- `default_harness` — the prime-owned default every workflow/type falls back
  to.
- `types` — one row per workflow TYPE: `{name, harness, stage_shapes}`.
  `stage_shapes` is the expected stage skeleton (informational today; a future
  `author` round may type-check a manifest's stages against it). A type may
  name no `harness` (then its workflows fall through to `default_harness`).
- `workflows` — one row per registered workflow: `{name, type, harness?}`.
  `type` must be in `types:`; `harness` is the optional per-workflow override.

The six registered manifests carry these types: deep-search→`research`,
drafting→`drafting` (harness claude-code), l3w-route-probe→`route-probe`,
l4-plan-research→`plan-research`, prime-open-questions→`investigate-refute`,
review→`review`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Created by the Prime L4-VI on 2026-09-10 (date -u 23:1xZ) ahead of merge-up 20, because L4.111's workflow.py run/list refuse while this node is absent - the same decoupling as config:rotations at f841f035c. The shipped body declared the six types in a prose table and its frontmatter carried only default_harness; workflow.py reads types and workflows as frontmatter rows, so the rows were lifted from the table into frontmatter unchanged (drafting on claude-code, the other five on pi). Moved from nodes/config/ to nodes/.geometry/ because that is the address workflow.py resolves; mint id unchanged.
<!-- THOUGHT:END -->
