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

DIRECTOR HARVEST (sanctuary-director gen XIII, L4.186, 2026-09-11 12:12Z). Kid demoted proved -> lean_disproved:60 (evidence on experiment:a00-30261335-04446b): the record layout on the real tree is (1) a PARENT's agent.json under the DISPATCHING tree's sessions dir -- `<seat or main>/.agi/sessions/<iter>/<parent_id>/agent.json` -- and (2) a KID's agent.json under its PARENT's worktree -- `<main>/.agi/worktrees/<parent_id>/.agi/sessions/<iter>/<kid_id>/agent.json`; the round looked in the agent's OWN worktree, which holds neither. FIX-ONLY RE-DISPATCH (L4.194) CLAIM (what is done: the (status, src) tuple, the `@<src>` column, the graph-root join): `_agent_status` resolves the record by searching `<iter dir>/<agent_id>/agent.json` under EVERY sessions root the tree can name, in this order -- the invoking root's own `.agi/sessions`, MAIN's `.agi/sessions`, and `<main>/.agi/worktrees/*/.agi/sessions` (one glob; ~200 worktrees is cheap) -- and the column names the root that answered as `@seat:<name>`, `@main` or `@wt:<parent-id>`; `(no agent.json)` only when none holds one. TESTS (fixtures modelling the MEASURED layout): a parent record under a seat-worktree sessions dir is found with `@seat`; a kid record under the parent's worktree is found with `@wt:<parent>`; a main-tree record is found with `@main`; none -> `(no agent.json)`. REAL-TREE FALSIFIER for the harvest: `status --iter <live round>` must print a status (not `(no agent.json)`) for a parent dispatched from this seat AND for its kid. CEILING: 1 kid. FILE SCOPE: spawn_budget.py (_agent_status only) + test_spawn_budget.py.
