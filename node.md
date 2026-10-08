---
id: goal:g1.41.1
mint_id: 2294208501054da1b091416dd3b9ccb3
type: goal
parents:
  - goal:g1.41
next_edges: []
confidence: 0.5
edited_by: director-general-1
goal_id: G1.41.1
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
scaffold_hash: 899f49cb1825989f
season: 2
seeds:
  - goal:g1.41
status: horizon
tags:
  - g1.41
  - root
  - vstore
title: "G1.41.1: the other root readers of the pinned trunk (box-carry, agi-land, agi-gate) read it through a verified store like A1b -- horizon, after A1b lands"
town: core
---
# goal:g1.41.1

## Why this exists
goal:g1.41: belam ruled (03:44Z 10-08) that A1b (hypothesis:g141-a1b-root-reads-the-pinned-trunk-only-through-a-store-it...) closes the three root reads of agi-boot, agi-project and the baked agi-project.service, and that the OTHER root readers of the same agi-writable object store are ONE follow-up leaf, horizon, not that round. This is that leaf.

## Target end-state
- Every other root-run reader of the pinned trunk reads it through a verified store (A1b's agi-vstore, its own store path per unit so a path-fired run never removes a store another is reading), not through MAIN's objects: box-carry's matrix read at the pin (agi-carry@.service and --fetch), agi-land and agi-gate where they run as root.
- Each such unit gains the same two lines as agi-boot.service (ExecStartPre=agi-vstore, GIT_DIR=its own store), and a forged pinned object makes it refuse (rc non-zero, nothing carried, landed or gated).

## Invariants
- Fail-closed on a corrupt object, as A1 and A1b. No new carry.env cell. The vstore file stays root-installed and is never read from the trunk.

## Falsifier
1. For each reader: a lane in the shape of A1b's agi-vstore.t.sh (a forged loose blob, tree or commit in a scratch MAIN, a real unit text) is RED on the trunk and green once the unit carries the two lines; `sh extensions/agi/tests/box-carry.t.sh` stays 0 FAIL.
2. Negative: `git grep -n -E 'git -C \$O|git show \$AGI_TRUNK' -- .agi/nodes/.geometry/engine-root.md` lists no root-run read of the pin outside the verified store, EXCEPT the post-uid ExecStartPre line of agi-post@.service (`git -C $O branch` / `worktree add`, engine-root.md:37), which runs as the post's own uid and reads MAIN by design: exclude it by name, or the grep matches it forever.

## Out of scope
A1b itself (the verifier and the boot / agi-project units) · the host act that installs the vstore file and refreshes the pin (belam's) · the box-carry --fetch hub path.

## Agent Notes
Assigned to **director-general-1**.
