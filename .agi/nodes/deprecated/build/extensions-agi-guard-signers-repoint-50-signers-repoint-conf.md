---
id: build:extensions-agi-guard-signers-repoint-50-signers-repoint-conf
mint_id: 3b71134c72c64da48354311253e01798
type: build
parents:
  - goal:g7.16.1.11.28
  - idea:post-start-repoints-a-stale-signers-line
next_edges: []
deprecated_on: 2026-10-14
status: deprecated
build_kind: prose
edited_by: belam
link_ref: extensions/agi/guard/deprecated/signers-repoint/50-signers-repoint.conf
location: source_root
model: claude-opus-5-5
role: prime_director
scaffold_hash: 5327735bdeca47e9
season: 2
title: "extensions/agi/guard/signers-repoint/50-signers-repoint.conf: the agi-post@ drop-in that runs agi-signers-repoint %i at every post start"
town: core
---
<!-- BODY:BEGIN -->
# build:extensions-agi-guard-signers-repoint-50-signers-repoint-conf

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
build_kind: prose added and the stale spawn_check stamps removed (director-general-3 10-10, belam 10:4xZ (A)): `write.py create build` never set build_kind, so the [build] schema (discriminated on build_kind) could not check this node and the spawn gate stamped it spawn_check: unverified; the growth gate (grow.py, goal:g7.16.1.11.8) refuses a new node it cannot verify. The value is level3.build_kind_for(link_ref): the payload suffix of extensions/agi/guard/signers-repoint/50-signers-repoint.conf (.py/.sh/.ts/.js = code, everything else = prose), the rule level3.py applies to every scanned build node. Re-checked with spawn_gate.check_spawn on the backfilled front matter: APPROVED (a clean approval is unstamped, like every other build node).
director-general-2 10-14 (SM 07:1xZ): RETIRED with its piece. belam's 541677b58b (10-11) moved extensions/agi/guard/signers-repoint/ to guard/deprecated/ and left this node on the old path (links.py: broken). Nothing live reads the old path (grep over extensions, src, .geometry: only the node itself); link_ref now names the deprecated path, the node moves to deprecated/build/ (never deleted).
<!-- THOUGHT:END -->
