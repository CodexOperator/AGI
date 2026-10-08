---
id: config:workflows
mint_id: 7b5b36b813e2414e9cff438c94530fac
type: config
parents:
  - goal:g1.14
next_edges: []
default_harness: pi-free
edited_by: belam
locations: {}
scaffold_hash: ecc9a7f9f209d906
season: 2
spawn_check: unverified
spawn_check_reason: no active schema for type 'config'
thought_session: belam-S1-L4-VII
title: Workflow type registry and the prime-owned default harness
types:
  - {"name": "review", "harness": "pi-free", "stage_shapes": ["global-checks", "review:{target}"]}
  - {"name": "drafting", "harness": "pi-free", "stage_shapes": ["draft:{slug}", "critic"]}
  - {"name": "research", "harness": "pi-free", "stage_shapes": ["read", "refute:{lens}", "synthesize"]}
  - {"name": "route-probe", "harness": "pi-free", "stage_shapes": ["emit", "critic"]}
  - {"name": "plan-research", "harness": "pi-free", "stage_shapes": ["map", "draft", "judge", "verify", "synthesize"]}
  - {"name": "investigate-refute", "harness": "pi-free", "stage_shapes": ["investigate:{key}", "refute:{key}"]}
  - {"name": "merge-up-review", "harness": "pi-free", "stage_shapes": ["review:{key}", "verify:{key}"]}
  - {"name": "desktop-check", "harness": "pi-free", "stage_shapes": ["capture-and-read"]}
  - {"name": "trove-survey", "harness": "claude-code", "stage_shapes": ["read:{key}", "critique:{key}", "panel:{key}", "judge"]}
  - {"name": "recovery-survey", "harness": "pi-free", "stage_shapes": ["survey:{key}", "refute:{key}"]}
  - {"name": "g15-close-triage", "harness": "pi-free", "stage_shapes": ["triage:{key}", "refute:{key}"]}
workflows:
  - {"name": "review", "type": "review"}
  - {"name": "drafting", "type": "drafting"}
  - {"name": "deep-search", "type": "research"}
  - {"name": "l3w-route-probe", "type": "route-probe"}
  - {"name": "l4-plan-research", "type": "plan-research"}
  - {"name": "prime-open-questions", "type": "investigate-refute"}
  - {"name": "merge-up-review", "type": "merge-up-review"}
  - {"name": "desktop-check", "type": "desktop-check"}
  - {"name": "trove-survey", "type": "trove-survey"}
  - {"name": "recovery-survey", "type": "recovery-survey"}
  - {"name": "g15-close-triage", "type": "g15-close-triage"}
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
belam-S2-L5-XIII 13:0xZ 09-27, on thought-master [red] 06:42Z + 06:52Z (TMM.295) and the OWNER 13:0xZ (account drained, no funds to top up): default_harness pi -> pi-free and all 10 pi type rows -> pi-free (trove-survey stays claude-code: the subscription, not OpenRouter). (1) SAID: the ladder went zero_usd (431b8edc32), "every lane pi-free". (2) DOES: workflow.py resolves a run harness as explicit --harness, then workflows.<name>.harness, then the type row, then default_harness; every type row here said pi, and harnesses.pi.models is deepseek/deepseek-v4.1-flash (PAID), so every mur stage without an explicit --harness pi-free billed deepseek -- TM ledger: DE 74 pi / 2 pi-free, DT 22 / 6, no-post keys 73 / 70; ~12.8 USD to 0.606 USD left. (3) NEAR MISS: moving the ladder and the director brief to pi-free satisfies "every lane pi-free" in the words while this node, the one the resolver actually falls through to, still named the paid harness. (4) No rule deviated: this node is prime-owned (default_harness is the Prime default).
<!-- THOUGHT:END -->

## Agent Notes
OWNER 2026-09-11 01:5xZ (verbatim in doc:l4-owner-decisions): the merge review is registered in the config-based router and used through the unified workflow dispatch router. APPLIED by the Prime L4-VII: type merge-up-review (harness claude-code: the Prime reviews on its own subscription; pi is one --harness flag away) + workflow row merge-up-review, pair authored with workflow.py author (merge-up-review.json is the source, agi-merge-up-review.js derived). From merge-up 24 on the Prime runs `workflow.py run merge-up-review --args <json>` and never an inline script.

OWNER 2026-09-11 02:1xZ (verbatim in doc:l4-owner-decisions): have a workflow check screenshots of the desktop as needed, the tmux panes stay up. APPLIED by the Prime L4-VII: type + row desktop-check (harness claude-code: the Read tool renders the PNG), pair authored with workflow.py author; xfce4-screenshooter -f -s on DISPLAY=:1 proven (1920x1200 PNG); run by name: workflow.py run desktop-check --args {focus} then the Workflow tool on the registered scriptPath.
