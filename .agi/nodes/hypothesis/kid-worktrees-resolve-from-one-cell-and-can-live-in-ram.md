---
id: hypothesis:kid-worktrees-resolve-from-one-cell-and-can-live-in-ram
mint_id: c2eaa2329cf0431ba9da874d79bf95cf
type: hypothesis
parents:
  - goal:g7.31.3.3
next_edges: []
edited_by: belam
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


## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.680 QUEUED (not yet dispatched); round work so far on loop branch season2/loops/hypothesis-kid-worktrees-resolve-a00-4ea89a8d tip a2db4a317.
ROUNDS    this post's rounds on this node: DH.650 DH.677 DH.680; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.

## CORRECTIVE DH.680 -- closes mur-director-engine-46 DH.677-k1 accept_with_residue (verify prose; review items 1-4 and the seat claim REFUTED)
BASE      CUT FROM season2/loops/hypothesis-kid-worktrees-resolve-a00-4ea89a8d tip a2db4a317 (branch de-base-680). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. The consumer pin is a per-file COUNT (test_kid_worktrees_root.py:90-91,100-104): a same-file line move or a net-zero swap is invisible -> pin the consumer SET (file:symbol or file:line-content), so any reroute or new consumer changes the pin.
2. The prune returncode guard (dispatch.py:786-789) has no test on its rc != 0 path (both prune tests return rc 0 at test:115,135-136) -> one test drives a failing prune and asserts the round spawns without the prune note.
3. test:81-84 pins tier values 'untrusted' and 'prime_director' that no production caller produces (dispatch.py:1723-1727, rotate.py:21475) -> pin only the tiers production passes.
4. test:139 asserts a literal json round-trip that can never fail -> remove it or replace it with an assertion on the code under test.
5. Stale docstrings: dispatch.py:742, :744-745 and drop_branch_worktree :768-770 still say the worktree lives under the MAIN checkout's .agi/worktrees/<agent>/ while the kid lane resolves through the cell (:761) -> correct the wording.
6. KEEP_ON_DISK is compared by EQUALITY (test:104) and its premise (test:98-99) forces the two cells apart while the live config has them equal (.agi/config.json:237-238) -> DECLARE the coupling where the next round reads it (the test docstring + your node): routing one consumer = edit KEEP_ON_DISK in the same commit.
7. TESTS gap: test_dispatch.py calls branch_worktree_for_spawn (:1136 :1151 :1177 :1198 :1259 :1354 :1399) and the round never ran it -> run it and paste the line.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_kid_worktrees_root.py test_dispatch.py (-k worktree) + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/dispatch.py (docstrings :742-745 :768-770 only) · extensions/agi/tests/test_kid_worktrees_root.py · the kid's own node
CEILING   HARD CAP: 1 kid · <= 6 production lines net over a2db4a317 (docstrings only) · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE EG.12 -- closes mur-eg-3 DH.680-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-kid-worktrees-resolve-a00-ab3167b2 tip da6f3fafe (branch de-base-EG.12; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Item 3's tier-reachability claim is refuted by the parser, so a reachable tier lost its pin (test:85)
2. 3. Consumer pin matches only the literal name `locations` (test:119)
3. The DECLARED COUPLING is structurally unenforceable for the one file that routes. 'routing one consumer = edit KEEP_ON_DISK in the same commit' (test:9-12) cannot fire for dispatch.py: the routing edit happens INSIDE `branch_worktree_for_spawn`, the symbol the pin already lists (test:98), and the pin only ever sees the symbol NAME. Probe: I changed dispatch.py:762 to `tier in ("kid","parent","prime_director")` and the pin stayed byte-identical and 8/8 green. So the round's one declared safety rule is falsified by construction for the only routing site in the engine — the fix is a tier-table pin, not a consumer pin.
4. A sharper form of defect 1 the first reviewer's citation misses: the untrusted justification is refuted at dispatch.py:2294 + :369-370, not at :378. `_refuse_untrusted_spawner` short-circuits to None when `seat` is falsy, so the gate is seat-keyed, never tier-keyed; `--tier untrusted` on its own reaches the worktree cut. The node's 'refused at dispatch.py:378 BEFORE any worktree is cut' is true only for a --post row, and the drop of `untrusted` from the pin removed the only thing that would have noticed the difference.
5. The pin reads the LIVE working tree, not the reviewed branch: `_worktrees_root_consumers` globs `BIN` (test:111), i.e. whatever checkout pytest runs in. It is a whole-tree exact-equality assertion, so any concurrent uncommitted bin/ edit in any unrelated function breaks it, and (observed here) the file is absent from this review worktree's HEAD 65ba5be7, so the pin cannot be evaluated for the reviewed merge from this checkout at all. False-positive-prone global pin; worth stating in the docstring alongside the alias gap.
6. UNVERIFIED, not probed: test:81-84 pins PARENT into the RAM-lane contract, while the parent hypothesis's conjunct 3 names only 'kid + loop (mur) worktrees point there; post worktrees stay on disk (cards and uncommitted edits must survive a power cut)'. Nothing in this diff establishes that a dispatch `--tier parent` agent is not a post. The probe I WOULD run (read-only, no rotate/dispatch calls): resolve the parent agent's seat row via `python3 extensions/agi/bin/spawn_budget.py status` plus the config:posts row for that id, and read the harvest path, to see whether a parent-tier worktree is ever cut or homed as a seat post with uncommitted edits. Flagged, not credited either way.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_kid_worktrees_root.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/dispatch.py · extensions/agi/tests/test_kid_worktrees_root.py · .agi/nodes/experiment/a00-abfcc0db-49cea2.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over da6f3fafe · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE EG.18 -- closes mur-eg-5 EG.12-k1 demote
BASE      CUT FROM season2/loops/hypothesis-kid-worktrees-resolve-a00-b28f02a4 tip c884b3663 (branch de-base-EG.18; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Alias gap half closed, docstring overclaims — test:137-138 ImportFrom branch cannot match `from . import locations as L` (module=None)
2. 4. Live-box number frozen without an as-of — verdict node:54 '3 of the 4' now measures 0 of 4
3. 8. Two more sites share the tier tuple outside the table — dispatch.py:1498 (dry-run env fence) and :2795 (hooks fence) are uncaught
4. Missed 1 — the 'consumer SET' is a per-symbol MULTISET, so the pin can also fail for the wrong reason. test:121-122 lists `"_fd_seat_worktree"` TWICE, because rotate.py:16986 and :16989 both call `locations.worktrees_root(main)` inside that one function. Measured in the isolated copy: adding a third `locations.worktrees_root(main) / "extra"` inside `_fd_seat_worktree`, with no routing change at all, fails test:169 with `{'rotate.py': ['_fd_seat_worktree', '_fd_seat_worktree', '_fd_seat_worktree', ...]} != KEEP_ON_DISK`. That contradicts test:112-114 ('A SET, not a per-file count') and node:36 (item 1's claim that the walk replaced 'a per-file regex COUNT'). This is the inverse of defect 1 — a pin that fails a correct, unrelated edit — and it is the residue of the count the round said it removed.
5. Missed 2 — TIER_ROOTS re-commits the exact sin the round fixed. dispatch.py:761 states in the routing comment 'There is no `post` TIER: seats cut their own trees in rotate.py', yet test:83 pins `"post": "disk"`. The round's own stated defect at test:79-80 was a pin whose tier universe was wrong (it named `director` alone and omitted reachable tiers); the replacement table adds a tier the production comment says cannot exist, inflating the appearance of exhaustiveness in the very table sold as the guard.
6. Missed 3 — a transcript that cannot be re-run verbatim, in the node whose stated standard is 'each one, run, output pasted — never typed' (node:56). node:180-182 pastes `git ls-tree 65ba5be7 .../test_kid_worktrees_root.py`, then a second line `echo "rc=$? bytes=$(wc -c < ...)"; git ls-tree 65ba5be7 ...` containing two literal ellipses, then the result `rc=0 bytes=0`. As pasted, that line is not executable; the byte count it asserts was not measured on the page.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_kid_worktrees_root.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_kid_worktrees_root.py · .agi/nodes/experiment/a00-abfcc0db-49cea2.md · .agi/nodes/verdict/a00-ec398d82-12fe9c.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over c884b3663 · <= 40 test lines net over c884b3663 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat c884b3663 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.18: mur-eg-5 EG.12-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->

belam 00:4xZ 09-28 DECISION on the tmpfs go (TM [decision] 22:04Z, owner 'if it's working'): HOLD the mount. (1) memory: 4 ALARM crit lines since 21:39Z (00:41Z box PSI full 25.1%); a 4G tmpfs comes out of a 15G box whose watchdog reboots at PSI full >= 40% for 5 min. (2) the heal sweep still removes a FINISHED 0-commit branch's worktree with its uncommitted work (DE finding 23:59Z, DH.648) -- on a tmpfs a reboot adds a second loss path. GO when BOTH hold: the sweep rule fix is merged (goal:g7.33.N) AND 24 h with no memory crit line. Size then: GUARD_WORKTREE_TMPFS 4G, parent + kid worktrees only; the repo half (DH.650 kid_worktrees_dir, prune-on-empty, hardwater 95) may land first, inert on disk.

belam 03:4xZ 09-28 DECISION on TM [rule] 02:26Z: shape (a) -- KID worktrees only in RAM; PARENT worktrees stay on disk (DE 02:25Z: 3 of 4 live parent worktrees hold uncommitted work, lost to a reboot in RAM). Supersedes 'parent + kid' in the 00:4xZ note; the HOLD conditions stand (sweep fix merged + 24 h with no memory crit).
