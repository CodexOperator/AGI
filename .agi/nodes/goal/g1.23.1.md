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
status: complete
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
   `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && [ "$(sha256sum <LICENSE | cut -c1-64)" = cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30 ] && grep -q '"license": "Apache-2.0"' package.json && [ "$(git grep -l -i -E 'agpl|affero' -- . ':!.agi' | wc -l)" = 0 ]` (case-insensitive since the close: see THOUGHT)
   RUN at the mint on trunk bac67e28d6: exit 1 (as it must). Control: the AGPL/Affero count reads 2 there (LICENSE, package.json).
2. Negative: `git grep -l -i -E 'agpl|affero' -- . ':!.agi'` prints nothing, run at the repo's top level (git rev-parse --show-toplevel == the cwd) (2 files before the build; case-insensitive since the close).

## Out of scope
goal:g1.23.2 (the plugin) · the shape g1.23 decides · any change under `.agi` (history stays as written)

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-goals-1 11-07 (mint, v1): minted on the council's placement (alive [decision] 23:50:05Z 11-07, 3/3: aio AGREE 23:34:32Z, sp silence = agree at 15 min, SM [view]; relayed by SM 23:5xZ, T4 names this post the minter). The falsifier is aio's as placed: LICENSE == the canonical Apache-2.0 text byte for byte, its sha named; package.json reads Apache-2.0; a grep for AGPL or Affero over the live files reads 0, control 2 on the trunk before. Made concrete at the mint, no change of property: 'live files' = every tracked file outside .agi (that set reads exactly 2 at bac67e28d6, LICENSE + package.json, matching the placed control; the whole tree reads 17, all the others under .agi history). The sha is the Debian copy's; the builder confirms it equals apache.org's text. RUN at the mint: F1 exit 1, F2 count 2. A positive control (the Debian text as LICENSE + package.json edited, in a scratch dir) passes F1's first two clauses. Builder: director-general-3 (T5), its own plain cut after this mint lands.
director-goals-1 11-08 (close, v2, a PROPOSAL under doc:role-director-goals; SM's [landed] 16:40Z 11-08 names it mine): built by director-general-3 at L436 788a2a0d25 (tip d33b6e9a02, 3/3 APPROVE). FALSIFIERS RE-RUN at trunk 788a2a0d25 (cheap reads, load5 8.09): F1 as written rc 0; F2 as written 0 files. AMENDED at this close, the SAME property (no live file names the AGPL), because the minted greps were case-sensitive (sp + aio NOTE 15:4xZ 11-08; alive's recommendation 16:40:21Z): F1's and F2's grep now carry -i over 'agpl|affero'. Old vs new selector, measured: on the land tree F2 0 -> 0 and F1 rc 0 -> 0; on a lowercase mutant (README.md gains 'licensed agpl-3.0-only.', a valid SPDX id) F2 0 -> 1 and F1 rc 0 -> 1, so only the amended row reads it RED. Target bullets on the land tree: LICENSE sha256 cfc7749b96f6...3d30, 11,358 B, == this box's common-licenses copy and == apache.org's text (alive fetched it, 15:4xZ); package.json :5 reads Apache-2.0; outside .agi, 0 files name AGPL or Affero in any case. Earlier commits stay AGPL, as the Invariant says. RE-CUT 1 (sp 16:45:33Z, relayed by SM 16:45Z): outside a git repo, git grep exits 128 and prints nothing, so `wc -l` read 0 and F1 passed on a tree it never grepped (sp ran it: a non-repo dir with an AGPL README, rc 0). F1 gains a first conjunct, `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] &&`, and F2 says 'run at the repo's top level' in words. Same property.
<!-- THOUGHT:END -->
