---
id: build:lib-find-root.sh@v2
mint_id: 7d1096b9e7bb412dbeb37ab51860570a
type: build
parents:
  - goal:g8.2
build_kind: code
confidence: 0.85
edited_by: season.py
origin: build-version
payload_ref: extensions/agi/lib/find-root.sh
season: 1
status: deprecated
supersedes: build:lib-find-root.sh
tags:
  - build
  - build-version
  - g8.2
thought_session: season
title: "Level-3 v2: extensions/agi/lib/find-root.sh — descend into <project>/<name>-tree"
version: 2
---
**Deprecated 2026-08-27 — retired, not deleted (G2.10).** The reasoning that lived in this node was migrated verbatim into the `THOUGHT` region of `build:lib-find-root.sh`, the canonical node for `extensions/agi/lib/find-root.sh`. The `@v2` convention is retired: a version is a grid commit, not a second node file, and the `THOUGHT` region — which survives a regenerating scan since 2026-08-27 — is now where a build artifact's reasoning lives. This file, its mint id, its `supersedes:` edge and its grid ref stay in place as prior art; deleting them would orphan the ref and leave a dangling edge behind. Earlier versions of this body remain readable via `grid.py payload`/`log` on this node's ref.