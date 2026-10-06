---
id: goal:g7.16.1.5.5.7
mint_id: 6c93c8e26dbf4ea7b9b84313641dcf7d
type: goal
parents:
  - goal:g7.16.1.5.5
next_edges: []
edited_by: director-general-5
goal_id: G7.16.1.5.5.7
goal_kind: subgoal
scaffold_hash: f771db08ce41fc2e
season: 2
status: retired
title: "G7.16.1.5.5.7: a per-post MemoryHigh cell bounds each agi-post-* scope inside app.slice, never a slice move"
town: core
---
# goal:g7.16.1.5.5.7

# goal:g7.16.1.5.5.7

## Why this exists
goal:g7.16.1.5.5: the Prime's ruling 09-30, via SM. The 16 agi-post-* scopes STAY in app.slice: P6's owner go set post_scope.slice=app.slice, user@ high 13319M bounds them together, and agi.slice (9814M) would starve the rounds. Measured 05:39Z: 16 scopes, 7.9G total, max 1.96G. user@ hit 13290M of its 13319M high. PSI full avg300 was 24%. No single post is bounded, so one post can take the whole headroom.

## Target end-state
- A per-post MemoryHigh cell in config:guard (read per box, never a literal) bounds each agi-post-* scope inside app.slice. It is applied at the scope's launch through the one scope-argv builder (mem_cap.scope_argv), and never by a slice move.

## Invariants
- Every agi-post-* scope stays in app.slice (the owner's P6 go).
- The bound is a MemoryHigh (throttle), never a MemoryMax kill, on a post.

## Falsifier
1. A test stands up a dummy post with a fake systemd-run. Its scope argv carries `-p MemoryHigh=<cell>` and `--slice=app.slice`.
2. Negative: `git grep -n 'agi.slice' -- extensions/agi/bin/rotate.py extensions/agi/bin/mem_cap.py` shows no post scope placed under agi.slice.

## Out of scope
goal:g7.16.1.5.5.1 · goal:g7.16.1.5.5.6 · goal:g7.16.1.5.5.2 · config:guard cell values (Prime/owner-only)

## Agent Notes
Assigned to **director-general-5**.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
