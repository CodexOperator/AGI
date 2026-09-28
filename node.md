---
id: goal:g1.28
mint_id: 98ec9d18de3e4263abde2d48b0f5df0d
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 0.7
edited_by: belam
goal_id: G1.28
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 51e944e91f17ece5
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - residue
title: "G1.28: PASS 12 residues -- 5 engine defects (write-path schema gate, stdlib spawn fence, heal worktree literal, gate source round-committable, the unmerged seat wrap) + the node/doc batch (assigned: director-engine)"
town: core
---
# goal:g1.28

## Why this exists
goal:g1: PASS 12 (OWNER 00:0xZ 09-28: DE merged up its whole post branch, TM landed it, the Prime passes over it) reviewed the trunk @72d8d565ce against BASE 707d8dbbea on pi-free, 0 USD: 25 rounds (21 hypothesis rounds over 18 hypotheses + 4 engine-delta over 45 files), 13 chunks + 6 serial retries. Verdicts: 23 accept_with_residue, 2 demote, 0 RED; merged into season2/main at 774e0b912. The verify stages upheld 153 residue items; 5 are engine defects, the rest node or doc text.

## Target end-state
- Every write path through write.py (create, the Edit API path, node_writer.update_node callers) runs the same schema gate as the set verb, and a seat-row write failure is loud.
- The suite spawn fence covers every stdlib spawn leaf (os.popen, os.spawn*), not only subprocess.
- heal.py resolves a seat worktree path from the config cell, never a literal.
- A round's done commit can never sweep the gate's own source file.
- hypothesis:a00-955a27ff-64bc5a either carries the seat wrap it claims (rotate.py) with a test that never reaches a real systemd unit, or its verdict is withdrawn.
- Every node-text residue in the batch is fixed at its cited line or answered on its node.

## Invariants
- A residue is closed by a reviewed round, never by a note.
- No fix reaches a real systemd unit, tmux server or crontab from a test.

## Falsifier
1. Each child hypothesis's named tests pass on the trunk, and `git grep -n "_FENCED_SPAWN_LEAVES" extensions/agi/bin/suite_guards.py` shows os.popen in the tuple.
2. Negative: `write.py create` of a node with an out-of-regex field is refused (exit != 0), as `set` is.

## Out of scope
goal:g1.27 (PASS 11 residues) · goal:g1.26 (PASS 10 residues) · goal:g4.18.1 (the one mint route redesign).

## Agent Notes
Assigned to **director-engine**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 12 step 6 (skill agi-merge-pass): the residue leaf, shaped like goal:g1.27. origin + seeds + heading_level set after create -- the create call omitted them, and snapshot-goals.py --render skipped the node (393 goals before and after); g1.27 carries origin goals-doc + heading_level 3.
<!-- THOUGHT:END -->
