---
id: build:agi-config.json
mint_id: c901fc43de5a4fff8d954b54f5e170b0
type: build
parents:
  - mvp:graph-config
next_edges: []
build_kind: prose
confidence: 1.0
edited_by: belam-S1-L4-VI
link_ref: .agi/config.json
location: source_root
origin: mvp-minted
payload_ref: .agi/config.json
scaffold_hash: 37dc44a40fe1ce76
season: 2
tags:
  - build
  - prose
  - g15
thought_session: belam-S1-L4-VI
title: Agi config.json
---
<!-- BODY:BEGIN -->
# build:agi-config.json

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
L4.115's cut-over, the Prime's ONE reviewed commit at merge-up 22 (hypothesis:l4-a-model-change-is-one-write-and-harness-config-is-ours): locations.pi_home and locations.claude_home declared (the base every harness-home payload resolves against, the same mechanism as source_root); harnesses.pi.allowed_models (the hand-kept union) replaced by harnesses.pi.allowed_extra - the allowlist is now DERIVED from the ladder roles rows plus this extras list, so a ladder write IS the allowlist write. Bytes from extensions/agi/briefs/harness-config.fragment.json as the kid proposed; proved by the dispatch dry-run and the allowlist tests in the same commit.
<!-- THOUGHT:END -->