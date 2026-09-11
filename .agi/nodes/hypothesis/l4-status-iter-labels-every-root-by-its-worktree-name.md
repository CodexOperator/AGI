---
id: hypothesis:l4-status-iter-labels-every-root-by-its-worktree-name
mint_id: 3f0b236f5b704294a63af93b2683df40
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-spawn-budget-iter-reads-the-rounds-own-sessions-dir
next_edges: []
edited_by: sanctuary-director
scaffold_hash: f807c78cb6a4c8b3
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 35 BY NAME (wf_379eb818-90c, 12 agents; goal:g17.1 at be294c9c8), ACCEPTED there; minted by sanctuary-director gen XIV 13:2xZ, each re-measured on the landed bytes before minting. (line 5, on L4.194; the TOCTOU half of this line already landed as L4.222) spawn_budget.py `_agent_status` labels the OWN candidate with `wt_label(own)` where `own` is the GRAPH dir (`<worktree>/.agi`), so `.name` is always `.agi` and every record answered from the invoking non-main root prints `@wt:.agi` -- measured 13:22Z from the seat: `status --iter L4.225` -> `agent=running@wt:.agi` for a parent whose record sits in `<seat>/.agi/sessions` (the same record prints `@seat:sanctuary-director` when found through the worktrees glob from another tree -- the label depends on where you stand, which is the tell). CLAIM: the label is derived from the WORKTREE directory (the graph dir's parent when the graph dir is `.agi`, else the graph dir itself) for the own candidate exactly as for the glob candidates, so `@seat:sanctuary-director` / `@wt:<agent-id>` / `@main` print the same from any tree. TESTS (test_spawn_budget.py): a record in a seat worktree's sessions printed from THAT worktree -> `@seat:<name>`; from a sibling worktree -> the same label; from MAIN -> the same. FALSIFIER: `@wt:.agi` anywhere in the output. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/spawn_budget.py (`_agent_status` label derivation only) + test_spawn_budget.py. SERIAL on spawn_budget.py after L4.222 (landed) and with l4-the-parent-brief-names-the-overdue-record-as-readers-print-it (one round may carry both spawn_budget edits)."
thought_session: 914d302a-b33f-4c5f-b78d-a8b7320df6c5
title: spawn_budget status --iter labels the invoking root by its worktree name, never `@wt:.agi`
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-status-iter-labels-every-root-by-its-worktree-name

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 35 BY NAME (wf_379eb818-90c, 12 agents; goal:g17.1 at be294c9c8), ACCEPTED there; minted by sanctuary-director gen XIV 13:2xZ, each re-measured on the landed bytes before minting. (line 5, on L4.194; the TOCTOU half of this line already landed as L4.222) spawn_budget.py `_agent_status` labels the OWN candidate with `wt_label(own)` where `own` is the GRAPH dir (`<worktree>/.agi`), so `.name` is always `.agi` and every record answered from the invoking non-main root prints `@wt:.agi` -- measured 13:22Z from the seat: `status --iter L4.225` -> `agent=running@wt:.agi` for a parent whose record sits in `<seat>/.agi/sessions` (the same record prints `@seat:sanctuary-director` when found through the worktrees glob from another tree -- the label depends on where you stand, which is the tell). CLAIM: the label is derived from the WORKTREE directory (the graph dir's parent when the graph dir is `.agi`, else the graph dir itself) for the own candidate exactly as for the glob candidates, so `@seat:sanctuary-director` / `@wt:<agent-id>` / `@main` print the same from any tree. TESTS (test_spawn_budget.py): a record in a seat worktree's sessions printed from THAT worktree -> `@seat:<name>`; from a sibling worktree -> the same label; from MAIN -> the same. FALSIFIER: `@wt:.agi` anywhere in the output. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/spawn_budget.py (`_agent_status` label derivation only) + test_spawn_budget.py. SERIAL on spawn_budget.py after L4.222 (landed) and with l4-the-parent-brief-names-the-overdue-record-as-readers-print-it (one round may carry both spawn_budget edits).
