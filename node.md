---
id: build:bin-grid@v2
mint_id: 9faf50074bcc46dea5bad1bf3b981557
type: build
parents:
  - goal:g2.5
build_kind: code
confidence: 0.82
edited_by: season.py
origin: build-version
payload_ref: extensions/agi/bin/grid.py
season: 1
status: deprecated
supersedes: build:bin-grid
tags:
  - build
  - build-version
  - g2.5
thought_session: season
title: "Level-3 v2: extensions/agi/bin/grid.py — sanitize() becomes injective"
version: 2
---
**Deprecated 2026-08-27 — retired, not deleted (G2.10).** The reasoning that lived in this node was migrated verbatim into the `THOUGHT` region of `build:bin-grid`, the canonical node for `extensions/agi/bin/grid.py`. The `@v2` convention is retired: a version is a grid commit, not a second node file, and the `THOUGHT` region — which survives a regenerating scan since 2026-08-27 — is now where a build artifact's reasoning lives. This file, its mint id, its `supersedes:` edge and its grid ref stay in place as prior art; deleting them would orphan the ref and leave a dangling edge behind. Earlier versions of this body remain readable via `grid.py payload`/`log` on this node's ref.