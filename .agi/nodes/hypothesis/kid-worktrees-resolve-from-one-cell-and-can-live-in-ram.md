---
id: hypothesis:kid-worktrees-resolve-from-one-cell-and-can-live-in-ram
mint_id: c2eaa2329cf0431ba9da874d79bf95cf
type: hypothesis
parents:
  - goal:g7.31.3.3
next_edges: []
edited_by: director-engine
scaffold_hash: 99f721ebee0a9eb8
season: 2
testable_claim: prune clean non-live kid worktrees; spawn reads paths.<town>.worktrees_root via locations.py (no literal at dispatch.py:754); guard.env GUARD_WORKTREE_TMPFS_<host>=4G mounted and charged to user@; post worktrees stay on disk; worktree prune on reboot
title: "Kid worktrees resolve from ONE config cell (paths.<town>.worktrees_root) and can live on a guard-owned 4G RAM disk; stale ones pruned first (assigned: director-engine)"
town: core
---
# hypothesis:kid-worktrees-resolve-from-one-cell-and-can-live-in-ram

# hypothesis: kid worktrees resolve from ONE config cell and can live on a guard-owned RAM disk (assigned: director-engine)

## Why this exists
**Parent `goal:g7.31.3.3`** (the spawn/rotate redesign): spawn is where a worktree is created. OWNER 2026-09-27 02:5xZ-03:1xZ to the Prime, verbatim: "if needed we could reduce pi latent count and reserve some ram for worktrees so we can batch the reads and writes for spawns and murs to and from ram. Dedicate a good couple gigs to it or maybe 4, what do you think?" · "Okay that sounds good as set up. Which config value are we editing later we will have to maintain it properly for all posts as part of the mint and send and rotate redesign goals."

## Measured (belam-S2-L5-XII, 03:0xZ 09-27)
- 210 worktrees; 190 kid checkouts at ~140 MB each (~27 GB on disk); `.git/objects` 145 MB.
- IO is READ-bound: Dirty 0.6 MB vs Cached 5 GB; io PSI some avg60 40-70 during PASS 10; every reviewer walk into `.agi/worktrees/` re-reads the 27 GB.
- The kid worktree root is a literal: `dispatch.py:754` `main / ".agi" / "worktrees" / agent_id`. `paths.local_maxxing` carries per-kid literals (`worktree_a00_2f819956`, `nodes_experiment_dir: .agi/worktrees/a00-d511add6/...`) because no root cell exists.
- Guard since 02:5xZ 09-27: docker budget 0, user@1000 high/max 12618/14021M, sshd reserve 1911M unchanged.

## Testable claim
1. PRUNE FIRST: every kid worktree that is clean AND not live (`spawn_budget.py status`) is removed with `git worktree remove` (its branch keeps every commit); post worktrees are never touched.
2. ONE CELL: `paths.<town>.worktrees_root` (default `.agi/worktrees`), resolved by `locations.py` and read by spawn (`dispatch.py:754`) -- no worktree path literal left in engine code; the per-kid `paths.local_maxxing.worktree_*` keys retire.
3. RAM LANE: `GUARD_WORKTREE_TMPFS_<host>` (4G) in guard.env; guard-init mounts it and subtracts it from user@'s budget like the docker budget; kid + loop (mur) worktrees point there; post worktrees stay on disk (cards and uncommitted edits must survive a power cut).
4. REBOOT: spawn/rotate/reap run `git worktree prune` when the RAM disk comes back empty.
5. EVICTION, BOTH LAYERS (owner 03:1xZ 09-27: 'update the reaper to also delete the worktrees automatically, or set up the RAM disk guard to do it for us for oldest inactive worktrees first for example? Or maybe both.'): the REAPER (agi-agi-reaper, git-aware) owns removal with the Prime's 03:1xZ predicate -- not live · idle >= reaper.worktree_idle_h · clean (no modified/untracked) · HEAD reachable from a branch · not referenced by config -- oldest-inactive first, `git worktree remove` never --force, bounded by reaper.worktree_keep_max; the RAM-DISK GUARD never runs git: at a high-water fill (80 pct) it triggers the reaper's eviction pass, at a hard-water (95 pct) spawn refuses a new worktree by name instead of deleting one. Reference implementation of the predicate: the Prime's one-shot prune of 03:2xZ 09-27 (commit message names the counts).

## Falsifier
1. `git grep -n '"worktrees"' -- extensions/agi/bin/*.py` = 0 path literals outside locations.py.
2. After the prune, `git worktree list | wc -l` <= live kids + posts + 5, and io PSI some avg60 during a PASS-sized load < 25.
3. A kid dispatched with `worktrees_root` = the tmpfs mount lands there, commits to its branch, and survives a `git worktree prune`.

## Agent Notes
2026-09-27 03:3xZ belam-S2-L5-XII ONE-SHOT PRUNE (owner 03:1xZ: 'Let's trim the worktrees yourself'), the conjunct-5 predicate by hand: 201 kid worktrees -> 52 removed (git worktree remove, never --force, 0 refused), /data avail 161827M -> 170620M (~8.8 GB), git worktree list 210 at 03:0xZ -> 170 at 03:3xZ (52 removed; ~12 spawned meanwhile). KEPT: 92 DIRTY (uncommitted/untracked kid NODE files: experiment, hypothesis, goal, build, 2x .agi/config.json) · 47 recent (< 6 h) · 9 live · 1 cwd-in-use; 15 de-base-* (DE's) + posts + prime-root untouched. FINDING for this round: the 92 dirty ones are UNHARVESTED kid output -- the reaper must harvest-or-deprecate uncommitted kid nodes (write.py adopt + commit, or a retire) BEFORE it may reclaim such a worktree; never --force. Decision log: /tmp/belam-pass10/wt-decisions.log (box-local).

## CORRECTIVE DH.529 -- closes mur-director-engine-18 DH.499-k1+k2+k3 (verify: accept_with_residue x3, config_max YES) -- slice 1 of 2: ONE cell
BASE      CUT FROM season2/loops/hypothesis-kid-worktrees-resolve-a00-42c4f9a2 tip 358a60839 (worktree de-h499). No merge. Never rebase.
SLICE 2 (NOT this round): the prune's ancestry gate + the dirty non-live kid sweep -> its own round, cut from this round's tip.
FIRST ACT config-max: the worktrees root is ONE cell. paths.core.worktrees_dir already exists and is authoritative (heal.py:194,198, _reap_worktrees_dir); the round added a SECOND name, paths.core.worktrees_root (.agi/config.json:235, read at locations.py:573).
1. Collapse to ONE name: locations.worktrees_root reads paths.<town>.worktrees_dir then paths.core.worktrees_dir (the claim says per-town), default .agi/worktrees; heal.py _reap_worktrees_dir calls locations.worktrees_root; drop the worktrees_root key from .agi/config.json (if the round commit gate refuses .agi/config.json, write the exact one-line diff on the kid node and the director lands it by name).
2. Route the 16 remaining literals through locations.worktrees_root -- cli.py:158,209,219,1305,3090,4565 · heal.py:464,1524,2253 · rotate.py:16986,16989,20878,20945,21115,21468 · verification.py:1366 -- and add ONE test: `git grep -n '"worktrees"' -- extensions/agi/bin/*.py` minus locations.py = 0, plus one test that a non-default cell moves the sweep's base (heal.py:1524) and the spawn path together.
3. Node wording (write.py): experiment:a00-011e4b8f-aa1da2 :17 rebrief_request and :123 say the cell is NOT in the branch (9ac4bcc2b landed it) and :36 points at a DIVERGENCE that is about other keys -> correct all three; experiment:a00-f7651b92-a75840 :42 measured '0 of 48 merged' against the post branch while _sweep_worktree_base resolves origin/season2/main -> re-measure against the engine's base, paste; experiment:a00-24f30600-a10da9 '169 of 181 prunable ~23.7 GB' is an UPPER bound (the unmerged gate passes 0 of 48) -> say so.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_locations.py test_heal*.py test_cli.py test_dispatch.py test_rotate*.py -k worktree test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp)
FILE SCOPE extensions/agi/bin/locations.py (worktrees_root) · cli.py · heal.py · rotate.py · verification.py (the 16 literal sites only) · .agi/config.json (the one key) · one new test file · experiment:a00-011e4b8f-aa1da2 · a00-f7651b92-a75840 · a00-24f30600-a10da9 (write.py) · the kid's own node. NEVER paths.local_maxxing.worktree_* (live readers in .agi/context/local-maxxing).
CEILING   HARD CAP: 2 kids (1: items 1-2 code, 2: item 3 nodes) · net <= 20 production lines (16 sites are one-token swaps) · <= 60 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

## ROUND DH.650 -- conjunct 3 (repo half) + 4 + 5 (spawn refusal): kid and loop worktrees on their own root (TMM.306: the first freed slot)
BASE      CUT FROM season2/loops/hypothesis-clean-kid-worktrees-p-a00-2a47eced tip 4cb4a8808 (branch de-base-650: the ONE-cell resolver locations.worktrees_root lives here). No merge. Never rebase.
FIRST ACT config-max: every value below is a CELL in .agi/config.json (paths.<town>.* / reaper.*), never a literal; code only for the resolver and the two triggers.
1. KID ROOT CELL: paths.<town>.kid_worktrees_dir (then paths.core.kid_worktrees_dir; absent = the worktrees_dir answer, so today's behaviour is byte-unchanged). locations.kid_worktrees_root(root, config, town) resolves it the way worktrees_root does. Spawn of a KID and of a LOOP (mur/review) worktree reads it; a POST worktree keeps worktrees_dir (cards and uncommitted edits must survive a power cut). One committed test pins all three (absent -> worktrees_dir; set -> the kid root; post -> never the kid root).
2. REBOOT (conjunct 4): when the kid root exists and holds no worktree dirs, spawn runs git worktree prune ONCE before it adds the new worktree, and names it in one line. Test in a tmp repo only.
3. HARD-WATER (conjunct 5, spawn half): reaper.kid_root_hardwater_pct (95): at or over it, spawn REFUSES the new kid worktree by name (the fill, the cell) instead of deleting anything. The guard's 80 pct high-water trigger is the guard's, not this round's.
OUTSIDE   the tmpfs itself (GUARD_WORKTREE_TMPFS in guard.env + the guard-init mount + the user@ budget subtraction) is the box keeper's, off-repo: NAME it on your node for the director, never touch it. NEVER mount, create a tmpfs, or run sudo; tmp_path only.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_locations.py test_dispatch.py + one new test file + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/locations.py · extensions/agi/bin/dispatch.py (the spawn site only) · .agi/config.json (the cells) · one new test file · the kid's own node
CEILING   HARD CAP: 2 kids (1: items 1-2, 2: item 3) · <= 30 production lines net over 4cb4a8808 · <= 60 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit AND every config/node edit on the loop branch before you exit (g7.33.19 row 13)

OWNER 16:2xZ 09-27 to belam, verbatim: "Sweet. Once that works DE can dial up concurrency and parallelism again as warranted. Then enable RAM disk when ready" -- the owner's GO for the RAM disk, AFTER the zero-usd mint fix works and DE's concurrency is back up. Sequence unchanged (belam card): claim 3 (tmpfs) merges up and is judged; guard.env GUARD_WORKTREE_TMPFS_belam_gpu=4G (backup first); guard-init.sh then --status green; only then paths.<town>.worktrees_root -> the mount; post worktrees + prime-root stay on disk; dirty kid worktrees harvested before any reclaim.

OWNER 17:0xZ 09-27 to belam, verbatim: "Yeah he's using the drain and harvest tools we just built to get those 92 or some worktrees cleaned up. I was wondering if we could add that tool and its use to the round harvest skill if there is one. Or if it's a part of a round start skill. Assuming it works good enough today and residues will get fixed alongside other things" -- the tool is heal.py sweep (hypothesis:clean-kid-worktrees-prune-and-dirty-ones-harvest-or-list, on its loop branch); belam [decision] 17:1xZ: DE adds its row to agi-dispatch §5 Orders and harvest in the SAME merge-up as the sweep code.

## CORRECTIVE DH.677 -- closes mur-director-engine-44 DH.650-k1 demote
BASE      CUT FROM season2/loops/hypothesis-kid-worktrees-resolve-a00-7e724480 tip b57ec4b90 (branch de-base-677; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. POST guard is dead code (dispatch.py:759 `tier == "post"`)
2. Over-reach: the unconditional else sends every non-post tier to the kid root (dispatch.py:759-760)
3. One reader, seventeen untouched consumers (locations.py:584) -- THIS round: NAME the 17 consumers on your node (file:line each) and add ONE test that fails if kid_worktrees_dir differs from worktrees_dir while any consumer still reads worktrees_dir; routing them is its OWN round (the director mints it), never here.
4. Hand-landed gate (.agi/config.json:238)
5. Node/bytes drift (hypothesis node names paths.<town>.worktrees_root)
6. Prune gate sits after the tier split and mislabels the post path
7. Prune note printed on a swallowed failure (dispatch.py:788)
8. THE TOWN CELL IS DEAD IN PRODUCTION, and it is green-tested. `git grep -n kid_worktrees_root` returns exactly one production hit, dispatch.py:760, which passes NO town argument; locations.kid_worktrees_root's town parameter (locations.py:585) is therefore never exercised outside test_kid_worktrees_root.py:44-48, so `paths.<town>.kid_worktrees_dir` -- the cell the order names FIRST -- can never be read, and a per-town RAM lane is impossible. Same 'green test pins a branch no production caller reaches' shape as the post guard, unflagged by the reader sweep.
9. SCOPE IS INVERTED, not merely over-broad: the only production caller of the changed function is workflow.py:2189-2194, a `--tier parent --branch` round stage; the order's authorised half (KID and LOOP/mur spawns reading the cell) has no production caller that reaches it, because the only other agent-tree creator in the tree, rotate.py:21468-21471, cuts post seats on worktrees_root directly. The test file's own docstring (test_kid_worktrees_root.py:5-7) asserts 'a set cell moves only KID and LOOP spawns' -- no line in the diff or the tests supports that sentence for parent/director.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_kid_worktrees_root.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/dispatch.py · extensions/agi/bin/locations.py · extensions/agi/bin/workflow.py · extensions/agi/tests/test_kid_worktrees_root.py · .agi/config.json · .agi/nodes/experiment/a00-42481a40-6d204c.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net (NET: this round should SHRINK the 55 added) over b57ec4b90 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.677: mur-director-engine-44 DH.650-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
