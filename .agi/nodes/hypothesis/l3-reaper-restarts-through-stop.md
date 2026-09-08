---
id: hypothesis:l3-reaper-restarts-through-stop
mint_id: feac00e527454989bf2bb713a9b7b441
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 0ba23401b81e37df
season: 2
testable_claim: "dispatch.py's inline reaper (_reap_one_impl) restarts an agent whenever its pid disappears and the reaper cannot see the node already complete, with no way to distinguish a deliberate kill from a crash -- so an agent killed as part of a declared owner stop is respawned and resumes spending. Reproduced live at least six times today: L3.42, L3.44 (main-tree kid a00-67a5c714, restarted as a00-67a5c714-r1 with iter=0 about sixty seconds after being killed), SD.01's first attempt (kid a00-762fcc70 restarted the same way), and others named in HANDOFF.md's stop-order sections, including one restart that surfaced hours after its agent's first death. Proved by adding a spawn_budget-level pause flag that both acquire() and the reaper's restart branch consult: with the flag set, killing an agent's pid must not produce a replacement pid within the reaper's poll window, and spawn_budget.acquire() must refuse admission outright for any new spawn. Disproved if a paused reaper still restarts a killed agent, or if setting the pause flag blocks a legitimate crash-driven restart from resuming once the flag is cleared."
title: L3 reaper restarts a killed agent through an active stop order
---
<!-- BODY:BEGIN -->
# hypothesis:l3-reaper-restarts-through-stop

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SANCTUARY-DIRECTOR, 2026-09-08. Survival mode (owner: only this seat is running; every other seat holds). Building directly, no dispatch -- the dispatch itself is the cost right now. DESIGN CHOSEN: a spawn_budget-level pause flag (file-anchored the same way budget_dir already resolves -- main checkout via locations.git_common_root + find_project_root, never the nearest .agi/, learning directly from today's worktree-pin hazard rather than repeating it in this fix) checked at exactly two chokepoints: spawn_budget.acquire() (refuses ANY new admission while paused, covering "no new dispatches" structurally rather than by every seat remembering a verbal instruction) and dispatch.py's _reap_one_impl restart branch (refuses to restart a dead agent while paused, covering "no auto-restart through a stop"). REJECTED ALTERNATIVE: per-kill cause detection (inspecting exit signal/waitpid to tell a deliberate SIGTERM from a crash). Rejected because the reaper is not reliably the OS-level parent of the pid it is polling (a fresh dispatch.py invocation reading a pid back out of agent.json cannot waitpid a process it did not itself fork), so signal-cause forensics would be unreliable across process boundaries -- exactly the kind of clever-but-fragile detection this loop has been burned by today. A global, explicitly-set pause flag requires no forensics and matches how stops are actually communicated in this system: as a broadcast to everyone, not a signal to one process. ADJACENT FINDING, fixed in the same pass because it is the same shape: pi_adapter.is_alive() still uses bare os.kill(pid,0), which reports a zombie as alive; claude_code_adapter.is_alive() and spawn_budget._pid_alive() were already fixed for exactly this (hypothesis:l3-cc-adapter-zombie-lease) and pi_adapter was never brought in line -- one truth (is a pid dead), two readers, and they disagreed. Brought pi_adapter.is_alive() to the same rule. NOT covered here, left for hypothesis:l3-killed-agent-restarts-unattributed (separate, already landed): making a LEGITIMATE restart attributable via -rN/iter inheritance -- that mechanism is correct and untouched; this fix only adds the gate in front of it.
<!-- THOUGHT:END -->
