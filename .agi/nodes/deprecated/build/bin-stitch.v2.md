---
id: build:bin-stitch@v2
mint_id: 63c202d0c91a4ec4ade6734ec08af01f
type: build
parents:
  - goal:g6.3
build_kind: code
confidence: 0.85
edited_by: season.py
origin: build-version
payload_ref: extensions/agi/bin/stitch.py
season: 1
status: deprecated
supersedes: build:bin-stitch
tags:
  - build
  - build-version
  - g6.3
thought_session: season
title: "Level-3 v2: extensions/agi/bin/stitch.py — a version chain is not a duplicate payload_ref"
version: 2
---
**Deprecated 2026-08-27 — retired, not deleted (G2.10).** The reasoning that lived in this node was migrated verbatim into the `THOUGHT` region of `build:bin-stitch`, the canonical node for `extensions/agi/bin/stitch.py`. The `@v2` convention is retired: a version is a grid commit, not a second node file, and the `THOUGHT` region — which survives a regenerating scan since 2026-08-27 — is now where a build artifact's reasoning lives. This file, its mint id, its `supersedes:` edge and its grid ref stay in place as prior art; deleting them would orphan the ref and leave a dangling edge behind. Earlier versions of this body remain readable via `grid.py payload`/`log` on this node's ref.