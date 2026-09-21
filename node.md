---
id: build:workflow.py
mint_id: f5c03734719848489854d3e7cdd39630
type: build
parents:
  - mvp:workflows-are-graph-payloads
next_edges: []
build_kind: code
confidence: 1.0
edited_by: a00-2b046d3e
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
<L4.111 a00-2b046d3e (experiment:a00-2b046d3e-35273a, hypothesis:l4-workflow-types-and-default-harness-are-a-geometry-node): the two hardcoded default-harness literals (old list_workflows:227, run_workflow:735) are gone, replaced by _resolve_default_harness reading nodes/.geometry/workflows.md in per-workflow > per-type > prime-default order, then refusing loudly NAMING the node (WorkflowsNodeError; main exits 2 cleanly). list gains a LEVEL column naming the source; run/list refuse when the node is absent (the pre-prime live state); validate refuses an undeclared or missing type when the node exists. The six live manifests gained a `type` (engine files, in scope). The live node is a config node written_by [owner, prime_director], so no kid can create it -- this round proves on a fixture root and ships the body at extensions/agi/briefs/workflows.geometry.md for the prime to land. Residual pre-existing <TODO> skeletons in l3w-route-probe.json and l4-plan-research.json are named, not fixed (authoring is a separate round). Near miss avoided: a code default kept for safety would satisfy the words and keep the literal the owner ordered gone.
<!-- THOUGHT:END -->