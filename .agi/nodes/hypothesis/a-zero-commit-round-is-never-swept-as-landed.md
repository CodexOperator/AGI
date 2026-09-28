---
id: hypothesis:a-zero-commit-round-is-never-swept-as-landed
mint_id: 5b3e593cc9e14183a7bd5ec785eed21f
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
edited_by: director-engine
scaffold_hash: 7aa20d28c6686e3f
season: 2
testable_claim: a finished worktree whose branch has 0 commits past its cut point is refused by the heal sweep unless clean including its unhomed writes; merged 1+-commit rounds sweep as today
title: "A zero-commit round is never swept as landed (EG.9, TMM.313, assigned: director-engine)"
town: core
---
# hypothesis:a-zero-commit-round-is-never-swept-as-landed

## ROUND EG.9 (thought-master TMM.313 00:45Z 09-28, belam [decision] 00:4xZ: the heal-sweep 0-commit fix heads the queue with EG.1; the tmpfs GO waits on it being MERGED + 24 h without a memory crit)
Measured   DH.648 (00:0xZ 09-28): the heal sweep removed a FINISHED parent worktree whose loop branch carried 0 commits; the round's ordered in-scope node edit was left uncommitted and was recovered by hand from the kid worktree (867b44a8b). heal.py:1499 _sweep_finished_worktrees gate (2) is `merge-base --is-ancestor HEAD <base>` (heal.py:1600): a branch with ZERO commits past its cut point has HEAD == the cut point, which is always an ancestor of its base, so gate (2) reads it as landed; gate (3) filters every `.agi/sessions/` path out of `git status` (heal.py:1261 _sweep_dirty_paths) before judging dirt.
CLAIM      a finished round whose branch has zero commits past its cut point is never removed on the ancestry gate alone: the sweep refuses it by name (`[sweep] refused <id>: unmerged (0 commits)`) unless the tree is clean INCLUDING every path the round wrote outside its own homed session dir; a branch with >= 1 commit that is an ancestor of its base is swept exactly as today.
Dispatch line  config-max: any new knob (e.g. whether a clean 0-commit tree may be pruned) is a cell next to reaper.worktree_grace_min, never a literal · template-max: the new refusal reason sits in the same `[sweep] refused` line family as `unmerged (no HEAD)` · code: the gate predicate only
FIRST ACT  REPRODUCE before any code: a committed test that builds a worktree cut from a base with 0 commits and one uncommitted edit (one under .agi/nodes/, one under .agi/sessions/<iter>/), runs the sweep past grace with no live lease, and asserts the tree is NOT removed -- paste the RED run on the base first, then the fix, then GREEN.
FALSIFIERS the reproduction test passes on the unmodified base (then the mechanism above is wrong: name the real one from the bytes before touching code) · a merged, clean, >= 1-commit round is no longer swept (existing test_heal_sweep.py cases go red) · the fix passes `--force` anywhere or widens what the sweep removes
TESTS      test_heal_sweep.py + test_heal_worktree_refusal.py + test_heal.py + test_bin_help_smoke.py (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); never the whole suite
FILE SCOPE extensions/agi/bin/heal.py (the sweep gate and its helpers only) · extensions/agi/tests/test_heal_sweep.py · .agi/config.json (one reaper.* cell, only if a knob is needed) · the kid's own node
CEILING    HARD CAP: 1 kid · <= 20 production lines net · <= 60 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
BOUNDARY   hypothesis:clean-kid-worktrees-prune-and-dirty-ones-harvest-or-list (DH.655, its own loop branch) reworks the same sweep; do NOT pull its branch or its predicate -- fix the gate on the post-branch bytes; the director reconciles the two at merge.
ANON       no user name, home or repo path value, host, IP or hardware name; patterns write <user>
PARENT     paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit
