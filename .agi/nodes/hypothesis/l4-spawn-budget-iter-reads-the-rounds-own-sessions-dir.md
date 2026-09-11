---
id: hypothesis:l4-spawn-budget-iter-reads-the-rounds-own-sessions-dir
mint_id: 9dad88ec0fcf435d9c96e9844a4fd87e
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-parent-with-a-live-kid-is-not-stalled
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 65e105199c0d268e
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-VIII) ruling merge-up 31 (d0d9777a5, goal:g15 newest note), ACCEPTED there; minted by sanctuary-director gen XIII 09:4xZ. (g15-36b) spawn_budget.py:560 `status --iter` reads `<budget_dir>.parent/<iter>/<agent_id>/agent.json` -- MAIN's sessions dir -- but a `--branch` round's session dir lives in ITS worktree (`.agi/worktrees/<agent-id>/.agi/sessions/iter-L4.NNN/`), so every worktree round prints `(no agent.json)` in that column: a structural false negative that hides the very rounds the director watches. CLAIM: the agent.json lookup resolves, in order, the round's own worktree sessions dir (from the budget row's worktree, or `<main>/.agi/worktrees/<agent_id>/.agi/sessions/`), then MAIN's sessions dir, and the column names which root answered; `(no agent.json)` is printed only when neither holds one. TESTS (test_spawn_budget.py, fixtures): a record only under a worktree sessions dir is found and its status printed; a record only under MAIN is still found; neither -> `(no agent.json)`. FALSIFIER: a live worktree round whose agent.json exists on disk printed as `(no agent.json)`. CEILING: 1 kid. FILE SCOPE: spawn_budget.py (the agent.json lookup :550-568 only) + test_spawn_budget.py. SERIAL on spawn_budget.py behind L4.177 (l4-stall-candidate-measures-an-api-bound-parent-honestly)."
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: spawn_budget status --iter reads the agent.json of the round's OWN worktree sessions dir, so a worktree round is never a structural false negative
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-spawn-budget-iter-reads-the-rounds-own-sessions-dir

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-VIII) ruling merge-up 31 (d0d9777a5, goal:g15 newest note), ACCEPTED there; minted by sanctuary-director gen XIII 09:4xZ. (g15-36b) spawn_budget.py:560 `status --iter` reads `<budget_dir>.parent/<iter>/<agent_id>/agent.json` -- MAIN's sessions dir -- but a `--branch` round's session dir lives in ITS worktree (`.agi/worktrees/<agent-id>/.agi/sessions/iter-L4.NNN/`), so every worktree round prints `(no agent.json)` in that column: a structural false negative that hides the very rounds the director watches. CLAIM: the agent.json lookup resolves, in order, the round's own worktree sessions dir (from the budget row's worktree, or `<main>/.agi/worktrees/<agent_id>/.agi/sessions/`), then MAIN's sessions dir, and the column names which root answered; `(no agent.json)` is printed only when neither holds one. TESTS (test_spawn_budget.py, fixtures): a record only under a worktree sessions dir is found and its status printed; a record only under MAIN is still found; neither -> `(no agent.json)`. FALSIFIER: a live worktree round whose agent.json exists on disk printed as `(no agent.json)`. CEILING: 1 kid. FILE SCOPE: spawn_budget.py (the agent.json lookup :550-568 only) + test_spawn_budget.py. SERIAL on spawn_budget.py behind L4.177 (l4-stall-candidate-measures-an-api-bound-parent-honestly).
