---
id: goal:g1.23.1
mint_id: c1aed7d4c9144e608326d93aa1bc6d25
type: goal
parents:
  - goal:g1.23
next_edges: []
confidence: 0.5
goal_id: G1.23.1
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 3c80059e1476fb54
season: 3
seeds: []
status: active
tags: []
title: "G1.23.1: agi is licensed Apache-2.0: LICENSE is the canonical text byte for byte, package.json says Apache-2.0, no live file names AGPL"
town: core
---

# goal:g1.23.1

## Why this exists
goal:g1.23 (decide the distribution shape: drop-in clone, skill package, or install): every shape it weighs ships with a license, and the owner chose that license on 11-07 (below). Measured on trunk bac67e28d6: `LICENSE` is the GNU AFFERO GENERAL PUBLIC LICENSE v3, `package.json` line 5 reads `"license": "AGPL-3.0-only"`, and those two are the only files outside `.agi` that name AGPL or Affero. The license does not choose g1.23's shape, so g1.23 stays horizon; this leaf is the part of it the owner decided (council placement: alive [decision] 23:25:38Z + 23:50:05Z 11-07, 3/3).

## OWNER 2026-11-07 20:42:45Z (c:be72d519c116), verbatim
From belam's [owner] 20:47:15Z 11-07 (box commit 86a44591bf on refs/box/belam/sanctuary-master), item 1, the owner's words in quotes:
"Cool lets go with Apache for it then and get it queued up."
belam's reading, marked MINE in that message: "= agi moves from AGPL-3.0 to Apache-2.0. MINE: one leaf + one RULES-free land: LICENSE replaced whole by the Apache-2.0 text, every license mention in the tree (README, QUICKSTART, any package metadata) read and changed in the same commit; all authors are ours (owner, our posts, Copilot bot), so the owner can relicense; earlier copies keep AGPL. Queue it after what is in flight."

## Target end-state
- `LICENSE` at the repo root is the canonical Apache License 2.0 text, byte for byte: sha256 cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30, 11,358 B (read from /usr/share/common-licenses/Apache-2.0 on this box; the builder confirms it equals https://www.apache.org/licenses/LICENSE-2.0.txt and names both shas in the build commit).
- `package.json` reads `"license": "Apache-2.0"`.
- No live file names AGPL or Affero. Live = every tracked file outside `.agi`; the graph's history under `.agi` keeps its past mentions, as earlier copies keep AGPL.

## Invariants
- Earlier commits stay AGPL as they were; nothing rewrites history.
- One build commit changes the license everywhere at once (no tree where LICENSE and package.json disagree).

## Falsifier
1. Exits 0 only when done, run from the repo root:
   `[ "$(sha256sum <LICENSE | cut -c1-64)" = cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30 ] && grep -q '"license": "Apache-2.0"' package.json && [ "$(git grep -l -E 'AGPL|Affero' -- . ':!.agi' | wc -l)" = 0 ]`
   RUN at the mint on trunk bac67e28d6: exit 1 (as it must). Control: the AGPL/Affero count reads 2 there (LICENSE, package.json).
2. Negative: `git grep -l -E 'AGPL|Affero' -- . ':!.agi'` prints nothing (2 files before the build).

## Out of scope
goal:g1.23.2 (the plugin) · the shape g1.23 decides · any change under `.agi` (history stays as written)

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-goals-1 11-07 (mint, v1): minted on the council's placement (alive [decision] 23:50:05Z 11-07, 3/3: aio AGREE 23:34:32Z, sp silence = agree at 15 min, SM [view]; relayed by SM 23:5xZ, T4 names this post the minter). The falsifier is aio's as placed: LICENSE == the canonical Apache-2.0 text byte for byte, its sha named; package.json reads Apache-2.0; a grep for AGPL or Affero over the live files reads 0, control 2 on the trunk before. Made concrete at the mint, no change of property: 'live files' = every tracked file outside .agi (that set reads exactly 2 at bac67e28d6, LICENSE + package.json, matching the placed control; the whole tree reads 17, all the others under .agi history). The sha is the Debian copy's; the builder confirms it equals apache.org's text. RUN at the mint: F1 exit 1, F2 count 2. A positive control (the Debian text as LICENSE + package.json edited, in a scratch dir) passes F1's first two clauses. Builder: director-general-3 (T5), its own plain cut after this mint lands.
<!-- THOUGHT:END -->
