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
OWNER 2026-09-10 ~22:2xZ (verbatim in doc:l4-owner-decisions): replace the glm parent model with deepseek/deepseek-v4.1-flash. 6da89f01e set agent_dispatch.model, a key the adapter reads only when no harnesses block exists (adapters/__init__.py); with a harnesses block the parent's model comes from the ladder roles row, then harnesses.pi.models.parent, and passes the harnesses.pi.allowed_models gate (dispatch.py). This version changes harnesses.pi.models.parent to the new id and adds the id to allowed_models; glm stays allowed so rounds already live keep their spawn model. The ladder rows changed in the same commit. Measured by the point gen VIII: the dry-run built command still printed glm after 6da89f01e.
<!-- THOUGHT:END -->