---
id: build:workflow.py
mint_id: f5c03734719848489854d3e7cdd39630
type: build
parents:
  - mvp:workflows-are-graph-payloads
next_edges: []
build_kind: code
confidence: 1.0
edited_by: a00-ee5d3690
link_ref: extensions/agi/bin/workflow.py
location: source_root
loop: hypothesis:l3w4-workflows-config-maxxed@s2
model: ~deepseek/deepseek-v4-flash-latest
origin: mvp-minted
payload_ref: extensions/agi/bin/workflow.py
profile: balanced
role: kid
scaffold_hash: de20b368238357c6
season: 2
spawn_check: unverified
spawn_check_reason: schema 'build' is discriminated on 'build_kind', which this node does not set
tags:
  - build
  - code
  - g17
thought_session: L3.27
title: Workflow.py
---
<!-- BODY:BEGIN -->
# build:workflow.py

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Authoring verb landed L4.105 (hypothesis:l4-workflow-authoring-is-a-harness-tool): workflow.py author <name> --stages <json|path|stdin> writes BOTH halves of a runnable pair in one action — <name>.json with real prompts AND agi-<name>.js generated FROM the manifest (manifest = source, script = derived). The generated script is a genuine Claude Code Workflow script (meta/phases/phase()/pipeline()/agent()), shaped exactly like the reference templates, so --harness claude-code renders in /workflows natively. Two-stage repeated workflows chain: stage[1].chained_from == stage[0].label + same repeat.of -> the pipeline(items, project, accumulate) form. On pi the chain is real too: a repeated stage with chained_from renders with the PRIOR stage validated return for the same repeat key merged into its prompt context (documented placeholder), carrying the finding across investigate->refute. register no longer lands <TODO> prompt skeletons (it could not author real prompts from labels) — it refuses and names author; validate now FLAGS <TODO> prompts as violations (strictly stronger invariant), so the registry itself can triage runnable from non-runnable. The two pre-existing register skeletons (l3w-route-probe, l4-plan-research) are now surfaced by validate awaiting an author rewrite — out of scope this round (files not in the round write-set).
<!-- THOUGHT:END -->