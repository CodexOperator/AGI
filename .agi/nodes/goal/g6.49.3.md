---
id: goal:g6.49.3
mint_id: 969c91cda58e4e45ac61f0ad0e4eb635
type: goal
parents:
  - goal:g6.49
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G6.49.3
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 0b0ee000aaca385b
season: 2
seeds: []
status: complete
tags:
  - goal
  - subgoal
thought_session: reaper-triage-2026-09-25
title: "G6.49.3: an empty lease dir reads as nothing-is-live, so the sweep would delete a worktree out from under a running round"
town: core
---
<!-- BODY:BEGIN -->
# goal:g6.49.3

## Agent Notes
DEFECT: sweep condition (1) read liveness ONLY from the spawn-budget lease dir, by design -- the docstring says the lease dir is the liveness source, never ps by name. The design premise failed in practice. MEASURED on encryption-town 2026-09-25: .agi/sessions/.spawn-budget held no leases at all (kept-live=0 on every pass) while 11 worktrees held running processes -- tmux seats, bash shells, and THREE mid workflow.py run merge-up-review (MUR 231, 232, 234, each with a live viewport.py). The only reason nothing was lost is that conditions (2)-(5) refused all 622 trees for unrelated reasons; a tree that was merged, clean and past grace would have been removed out from under a live round. This is latent data loss, not a performance defect, and it was found by accident while clearing the worktrees by hand. FIX: a backstop under the lease dir, never a replacement. _live_worktrees_by_cwd reads /proc/<pid>/cwd and open descriptors -- an exact kernel fact about this box, not the ps name match condition (1) rightly rules out -- and unions the result into live_ids. It can only ever keep MORE trees, never fewer. The pass logs a named line when it fires. VERIFIED after restart: 7 leaseless tree(s) held live by a running process, kept-live=6 where the lease dir alone reported 0.
