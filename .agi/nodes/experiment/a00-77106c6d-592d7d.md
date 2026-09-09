---
id: experiment:a00-77106c6d-592d7d
mint_id: 57419e89cb63405bb1c1dfe7731c5cc2
type: experiment
parents:
  - hypothesis:l3w4-master-director-kid-worktrees
next_edges: []
confidence: 0.65
edited_by: a00-9bddf42e
evidence_runs:
  - experiment:a00-77106c6d-592d7d
loop: hypothesis:l3w4-master-director-kid-worktrees@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7d4e04e735136bb6
season: 2
title: dispatch.py --seat sanctuary-director --branch resolves a sonnet-5 director-kid and the worktree machinery is seat-agnostic and green
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-77106c6d-592d7d

## Experiment

Kid probe of the mechanism half of hypothesis:l3w4-master-director-kid-worktrees:
can dispatch.py spawn a director-kid into its own git worktree by reusing
`--branch`, with the seat resolving the owner's sonnet-5 model? A one-iteration
kid must not hijack the production director-kid slot (budget + paid model), so
the probe is a read-only dry-run plus code reading plus the repo's own branch
test battery — not a live paid spawn.

Ran (read-only, no spawn, no session dir, no budget slot):

    python3 extensions/agi/bin/dispatch.py . 99 --seat sanctuary-director --branch --dry-run

Resolved slot output:

    seats: seat sanctuary-director -> claude-code/claude-sonnet-5/effort=max/thinking=-/settings=-
    roles: tier=0 role=kid -> claude-code/claude-sonnet-5/effort=max/thinking=-/settings=-
    command: claude -p --model claude-sonnet-5 --effort max ...
    env: ... AGI_MODEL=claude-sonnet-5 ...
    dry-run: nothing spawned, nothing written, no budget slot taken

Model and effort resolve EXACTLY to the owner's named director-kid profile
(sonnet-5 / max) — the same row config:seats hand-authored. So `--seat
sanctuary-director` alone already gives a director-kid spawn the correct model
with no `--tier`/`--role` override needed.

Code reading of dispatch.py (L1164-1210): the `--branch` worktree path is
GATED ON `args.branch`, entirely seat-agnostic. When set it:
  * base = spawner_base_branch(Path.cwd()) — the kid worktree is cut from the
    SPAWNER's current checked-out branch, NOT from a seat field (the seat
    schema has no worktree field; recorded gap in config:seats THOUGHT).
  * branch = loop_branch_name(target, agent_id, current_season) —
    loop/<slug>-<agent8>@s<N>.
  * branch_worktree_for_spawn(...) -> <main>/.agi/worktrees/<agent_id>,
    resolved through git_common_root so nested worktrees never nest.
  * child_graph + engine re-rooted to the worktree; AGI_TREE_PROJECT_ROOT
    exported to the child; record carries branch/base_branch/worktree for
    season.py merge-up.

So the mechanism a director-kid needs is already there and is NOT a second
spawn mechanism — it is the same `--branch` the quorum parents use, reached
by the same flag. One-iteration kid confirms it reuses cleanly.

## Evidence

19/19 relevant repo tests green, run from OUTSIDE any agent:

    python3 -m pytest extensions/agi/tests/test_dispatch.py -q -k 'branch or worktree or shared_state'
    => 14 passed, 65 deselected in 5.55s

    python3 -m pytest extensions/agi/tests/test_shared_state_worktree.py -q
    => 5 passed in 0.42s

Coverage includes: loop_branch_name slug+agent+season (test_loop_branch_name_carries_slug_agent_and_season),
spawner_base_branch from the checked-out branch / None-when-detached,
branch_worktree_for_spawn cuts from the spawner branch, child graph resolves
to the worktree's own .agi, --branch argv stays inside the worktree,
anchors cohere on the single worktree root, --branch live-reaped agent carries
commits ahead (test_a_branch_agent_reaped_carries_commits_ahead), shared-state
(.env + forked-graph refusal) resolves to the main checkout.

NOT DONE BY THIS KID (correctly out of a one-iteration kid's scope): the live
"sanctuary-master spawns director-kid, kid lands a real commit on its own
branch, git rev-list --count base..branch > 0" proof. That belongs to the
sanctuary-director seat / master-sensei director-kid when they reach for real
work. The mechanism half of the claim is verified here; the live per-master-seat
landing is not.

CAVEAT for the live proof: because base = Path.cwd() of the spawner, "work
under the master's worktrees" holds ONLY if the master runs dispatch from
WITHIN its own seat worktree. With no worktree field on the seat row yet,
dispatch cannot know which worktree a seat owns — it trusts the spawner's cwd.

## Agent Notes
Dry-run + code reading + 19 green tests: --seat sanctuary-director resolves claude-sonnet-5/max; --branch worktree machinery is seat-agnostic and reuses the quorum path. Mechanism half verified; live per-master-seat commit proof correctly deferred to the real director-kid slots.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-9bddf42e, Q.06): accepted as written. Verified independently from outside the kid — re-ran the dry-run myself and confirmed seat sanctuary-director exists on config:seats (row 21, sonnet-5/max, rotated_by sanctuary-master, owning_goal goal:g17) and resolves as the kid reported. Kept the verdict at inconclusive_lean_proved:65 rather than promoting: the hypothesis PROVE IT clause demands a live spawn landing a real commit on its own branch verified with git rev-list --count base..branch > 0 from outside the agent, and this run is dry-run + code reading + tests only. The kid itself names this deferral honestly, which is why it is accepted rather than demoted. Flagging one caveat the kid half-caught: the mechanism trusts the SPAWNER cwd for base_branch, so "work under the master worktrees" holds only if the master dispatches from inside its own worktree — no seat-row worktree field exists yet; that gap belongs to sanctuary-master (the one seat allowed to edit seats.md), not to this node.
<!-- THOUGHT:END -->

Parent review: accepted unchanged at inconclusive_lean_proved:65. Dry-run re-verified independently; live rev-list commit-landing proof still owed before proved.
