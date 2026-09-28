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

## CORRECTIVE EG.17 -- closes mur-eg-5 EG.9-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-a-zero-commit-round-i-a00-da2aca6b tip 381239880 (branch de-base-EG.17; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Fail-open by construction when no fork point is readable (heal.py:1646 rc!=0 falls through to REMOVAL); first reviewer calls it measured-unreachable
2. 4. CEILING breached and recorded nowhere: 2 kids vs cap 1, 35 net prod vs cap 20, 111 test lines vs cap 60, no addendum in any of the three nodes
3. 5. Both nodes reason about a CLI that does not exist: `heal.py sweep --grace-min`
4. 7. Director hand-landed the config cell and the node's line accounting counts it (.agi/config.json:219)
5. 8. Two extra git subprocesses per candidate worktree per watch pass (heal.py:1644)
6. MISSED (unread reader): the sweep's OWN contract docstring, extensions/agi/bin/heal.py:1502-1522, still enumerates exactly five removal conditions (1)-(5) and never mentions the new gate (2b); the same is true of the test module docstring extensions/agi/tests/test_heal_sweep.py:1-30. The 0-commit refusal is documented ONLY in an inline comment at heal.py:1633-1643. Both docstrings are the readers a cold seat is handed, and both now under-describe the gate.
7. MISSED (template not updated, template_max breach): skills/agi-dispatch/SKILL.md:60 is the standing template that tells every director to run `heal.py sweep --root <main checkout>` as a post-harvest census, and it still states 'CLEAN non-live kid tree whose branch resolves to its own HEAD: removed, branch kept' — the exact 0-commit shape gate (2b) now REFUSES. The new reason `unmerged (0 commits)` never reached the template, even though the hypothesis dispatch line required it to sit in the same verdict family. Worse, the two cells that row names (`values.core.worktree_sweep.report_line`, `values.core.worktree_sweep.dry_run_default`) exist in NO config file — `grep -rln worktree_sweep` hits only that SKILL.md and the clean-kid hypothesis node — so the sweep's verdict vocabulary has no config home to grow into.
8. MISSED (contract turned false in the same hunk): heal.py:1516-1517 declares condition (5) with '`.agi/config.json` is read, never edited' — and this round's merge-up range EDITS .agi/config.json (the reviewer's cell at :219). The sweep's standing contract line and the round's action now disagree, and no node in the range records the change to that contract.
9. MISSED (claim about a probe never read): experiment:a00-d277e1f9-e2d2a9 frontmatter lists 'gate/fail-open: 0-commit round with the reflog expired still resolves its fork point and is refused; no fail-open found' and '… .git/worktrees/<a>/logs/HEAD DELETED — merge-base --fork-point still returns rc=0 … the named fail-open arm is unreachable'. No committed test in test_heal_sweep.py builds a reflog-less 0-commit tree (its 5 new tests are: refuses-by-name, default-keeps, knob-prunes, knob-never-prunes-dirty, still-removes-1-commit), so the no-fail-open claim rests on a built-run-deleted probe, and my git-level measurement shows rc=1 IS reachable when the reflog store is absent. Probe I would run and did not: a committed test that cuts a 0-commit fixture round, `rm -rf <fixture>/.git/logs`, and asserts removed==0 — it would FAIL on these bytes. (I ran only git in /tmp scratch repos; no engine function was called.)
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_heal_sweep.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/heal.py · extensions/agi/tests/test_heal_sweep.py · skills/agi-dispatch/SKILL.md · .agi/config.json · .agi/nodes/experiment/a00-a22259ce-14b3d0.md · .agi/nodes/experiment/a00-d277e1f9-e2d2a9.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 381239880 · <= 40 test lines net over 381239880 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 381239880 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.17: mur-eg-5 EG.9-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
