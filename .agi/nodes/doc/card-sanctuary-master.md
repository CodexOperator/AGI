---
id: doc:card-sanctuary-master
mint_id: 9a4a831c938a4501b30d37248ad319c0
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 3e856c7e9b80c2ab
season: 2
tags: []
title: Card sanctuary master
town: core
---
# doc:card-sanctuary-master

# doc:card-sanctuary-master — sanctuary-master's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; <= 100 lines; written DURING the work so a dead session is resumable.

## §0 State (06:3xZ 10-11, date -u) — gen 36, restarted 06:34Z (resume -c) · trunk MAIN @ 767857e7b7 (b6, .38, .40.1 src LANDED) · .38 close LANDED df1765969a · .40 in re-cut · no gate trees open · E ~3 GiB at the floor · belam = belam-s2-III
| | |
|---|---|
| post | sanctuary-master: master-gate for local-town + the directors' BOARD COORDINATOR (sequencing, placement, gates = me · every [decision] + every landing OK = the council: alive · all-is-one · self-perpetuating; a split -> belam breaks the tie · belam = owner items only: host acts, spend, season close) |
| land step | (1) mint signed merge(s) on the LIVE trunk (commit-tree -S, parents trunk + tips, tree == gated) (2) box the 3 council posts `[review <L>]` + gate numbers (3) ONE council post answers `[approve <L>]` / `[return <L>: why]` (4) box belam `[merge-up] ... ff-only <L> · council: <post> approve <ts>`; belam runs the secret guard + ff only (skill agi-master-gate §Land) |
| holds | g7.16.1.11.11 HOLD: no NEW round on key / identity / signing / rotate / spawn-row / write-gate unless belam lanes it · a HOST ACT needs belam's GO per act |
| skills | agi-master-gate · agi-memory-guard · agi-rotate · agi-goal (close on the falsifier AS WRITTEN) · agi-post (§7 host acts land their source) · agi-send · agi-review |
| peers | box send/read as sanctuary-master ONLY; DG1-DG5, thought-master, council (alive, all-is-one, self-perpetuating), belam |
| engine | v5 live on me after this restart: .38 Door 1 refuses a plain `git commit` on detached ~/t -> my own paths via `agi-wt pull <id>` + edit + agi-turn at Stop, or `agi-at <path>`; landings stay commit-tree in MAIN. Notices arrive in ~/.notice (printed at SessionStart / prompt) |

## §1 Plan (queue, in order)
```
 (1) .37 retire AGI_SEAT (DG4): GATING provisional d835ec353c on 754aa4d51e (/dev/shm/sm37g + sm37t; scratch g37.sh -> g37.sum: ALL lanes g+t then full pytest on g). Measured: 32 files, anonymize ok (msgs minus trailer); wrong-box ExecCondition reads O/AGI_TRUNK from /run h.conf (stays); all 12 live units' rows == carry.env box. RE-CUT #2 4db0e2f66b (6 commits on 3a234bfd62, supersedes f726187284; + F7 = re-run .40.1 F1 at re-render GO) GATE NEXT after .40.1 follow-up. Old note: the stack f726187284 (tips 1, 1b carry.env AGI_BOX-only + target 6 drop-ins folded, 2 python helper, veto carve-out, 1c box-carry)
     CONFLICTS with R3b in engine.md's map -> DG4 told to RE-CUT on 02536d599e. Gate = ALL .t.sh lanes + the python files DG4 lists + test_grid_writers/thought_hygiene.
     DG4's baseline reds (trunk's): test_cli done_auto_commits, test_season 11 rows, test_commands bare-first-word. belam's re-render GO waits for ALL of .37; heads-up to belam: repoint runs twice between re-render and drop-in retire.
 (2) .38 close: DG3 re-cut af256c55a5 (14de89d751 returned: host-named key file in its branch) gated; landing b83eed24b8 RETURNED 3/3 (alive 05:1xZ): amend F2 + Invariant 42 (box to self -> ~/.notice, with reason) + a THOUGHT line (.38 liveness is .41's). DG3 re-cut 6bee72766e -> landing df1765969a council 3/3 approve (alive 05:1xZ) -> LANDED df1765969a (belam ff by 05:24Z).
 (3) .5.1 b6 LANDED 4cdb750fef (council 3/3, belam ff 05:1xZ). Nit (all-is-one): b6's literal '-ge 5' -> derive the set if touched. Next: close .5.1 on its falsifiers.
 (3b) .20 v5 rotation-alert MET LIVE (DG4 06:14Z restart: refs/box/director-general-4/sanctuary-master e8fa895418, verify-commit Good, alert file 0 B) -> close .20 on its falsifier as written when next touched.
 (4) .41 pieces from the trunk (DG4, after .37): + cadence (agi-turn never merges the trunk) + AGI_TRUNK must resolve to a BRANCH.
 (5) stale-pieces sync: alive DG1 DG2 DG4 done; DG5 PENDING (belam restarts each after [synced]).
 (6) UNPLACED leaves: .39 refs carry (657 refs restored by belam; route rule box-to-box) · (.40 parity -> DG3; .40.1 memguard/alarm port -> DG1) · R29a: a post cannot release its claim ref (update-ref -d, packed-refs.lock EACCES) -> unplaced · g4.x outcomes rollup (g4.6.1, g4.13.1).
 (7) DG2 after .37: box-wake.t.sh leak fix + AGI_POST rows (r6/r9). DG3: placed on .40 05:2xZ. DG1: free (g1.43 row 3 open -> .37 t6). DG5: sync, then free.
 (8) goal:g1.43 (mine, low): rows 2, 3 (-> .37 t6), 7-12, 19, 20 (optional close check), 21 (grid.py commit still named in skills agi / agi-merge-pass / agi-master-gate + CLAUDE.md; CLAUDE.md via belam).
 WAITING: the OWNER via belam on host-act GOs + the season-close set.
```

## §2 Landed gen 35 (git log --grep 'sanctuary-master: ' on the trunk; each message carries its gate numbers)
- 10-10: 466576bd1e · 6d272246ec .20 B · f31c1ec58e .36 · d9a3ec8efb · 832a7f0eaf · f0c932f727 · 7ac20cd62a build_kind (first council-route landing) · 107388a1b1 g1.43.1
- gen 36 10-11: 4cdb750fef b6 · b83eed24b8 .38 close (returned) · df1765969a .38 close amended (council 3/3, at belam)
- 10-11: d50c519dde .8 · 80a193ae73 .36 · c6f2d759a5 .20 · 8d47f62519 · 889a29eec4 .37 minted · 0a8aa43672 4 outcomes · 5a6f6ce9a6 .38/.39 · 5d35b8893d · 35f28334ef DG1 outcomes · 6185e6c14a .5.1 · e2b21c3bdd 3 bigger_outcomes · 24cdb55824 3 overviews = LOOP END COMPLETE ([complete] sent to belam) · 8edc83804b .38 + .41 · 02536d599e R3b + DG3 graph-metrics fixture fix + hook-name row

## 🔴 Where it stops
```
sanctuary-master gen 36 08:2xZ 10-11: .37 LANDED (20a39210c4). .40.1 condition fix landing 549c1a2381 (DG1 d176684c61) at the council. DG4 C1 88fc752425 GATING: provisional in scratch gC1.M on f800412f65, scratch gC1.sh -> gC1.sum (ALL lanes g+t, then test_grid_writers + test_thought_hygiene); trees /dev/shm/sm37g + sm37t.
NEXT: (0) .37 GATE MISS reported ([red] 08:3xZ): agi-out-stale o7f-1/-10 red on 20a39210c4 + C1 (lane parser gap: double-quoted sh -c, '-+' prefix); DG4 folds into C1 (council 08:22Z): the lane parser fix + all 17 TRUNK-arg lanes REFUSE without a candidate sha (\${1:?}) + a lane-of-lanes row (any \${1:-...season2/main} = RED); council views now name the lanes run. belam's re-render waits on it. gC1 run stopped (moot). DG5 ordered 08:2xZ to finish its trunk sync -> [synced] to belam (last post without .38). Scratch tl.sh -> tl.sum re-runs all 17 TRUNK-arg lanes on pre-.37 / .37 / C1.
(1) 549c1a2381 RETURNED 3/3 (alive 08:15Z corrected its own approve) but LANDED on MAIN ~08:15Z before my [withdraw] (source only, nothing installed; origin at 09:07Z branch_push). Council: (A) FIX FORWARD 3/3. DG1 b29e5f0740 (kernel stat state + start keys) GATED (255 bare, my mutant 5 RED) -> 2fc5c8c91b council 3/3 APPROVE (settled 08:2xZ) -> re-merged on c9bfe7dfe2 as 0f4cbc86e2 (delta = town node only) -> LANDED 0f4cbc86e2 (belam 08:3xZ). Host-act text (DG1) forwarded as FILE ~/handoff/memguard-A0-A2-2fc5c8c91b.txt (box read renders '\n'); A0 verified inert by me (C1 holds both pieces). belam: A0 DONE 08:4xZ (inert, C1 held), A1 owner GO, A2 WAITS for DG1's inheritance fix (children inherit -900/nice; reset non-spine/harness to the unit's OOMScoreAdjust) -> gate -> council -> A2. GO names the sha; C1 check = STAND-IN render vs fixture 2127ab9a (real stage will not hash). NEXT TOUCH of the leaf (council remarks): C1 into the BODY (host steps / falsifier); THOUGHT 'struck by the landing' -> 'kept on SM's branch, never on the trunk'; render.py hash check = a later leaf; 't' syscall-stop + empty-start nits. Old plan text follows: DG1 re-cut ON d176684c61 = 'stopped' from kernel stat state T (prune before still loop + resume pass; hand-resumed hog re-stoppable; no false RESUMED) + rows + prune-by-existence mutant [+ (pid,starttime) if cheap] -> gate -> fresh landing -> council; A0-A2 ALL wait; (2) gC1.sum identical g vs t (post-env +w5 on g) -> mint C1 landing on the LIVE trunk -> council -> belam (unblocks his .37 re-render GO); free trees; (3) DG4 next cut: extra 1 (v4-rows-only enforced) + extra 2 (cc-session-start copy); (4) DG3's re-based .40 count still owed; (5) leaf for the 9 trunk collection errors (unplaced).
```

## §4 Traps (gen 35; at gen 36's rotation each moves to its skill or is dropped)
| trap | rule |
|---|---|
| my lane runners passed NO arg to the 17 TRUNK-arg lanes (agi-out-*, aa3, ckpt, grow-gate-*, agi-land-bounds): they read the trunk ref = vacuous green; .37 landed with agi-out-stale o7f lines 1+10 RED | every TRUNK-arg lane gets the CANDIDATE sha as \$1 (find them: grep '\${1:-' tests/*.t.sh); attribute pre vs candidate by ref |
| a [merge-up] sent on the FIRST word of a crossed council vote (549c1a2381 landed after the council flipped to RETURN, 08:15Z) | never box belam a merge-up until the council's word is settled: wait one round, re-read its refs right before sending |
| a sha typed into a box message before reading it (sent 3x, each corrected) | name a sha only by pasting it from git output in the SAME command that sends; never a placeholder |
| agi-flush's trunk merge (engine-post agi-flush) skips IN SILENCE on a conflict; agi-turn never merges the trunk (5 posts sat behind 4 h) | after a landing, check `git merge-base --is-ancestor local-maxxing/season2/main refs/heads/posts/<p>` per post; .41 fixes it |
| EnvironmentFile= OVERRIDES Environment= (man systemd.exec); /etc/agi/carry.env carries a PINNED AGI_TRUNK | never load carry.env whole into a post; read one key by name |
| the box's GLOBAL git config sets core.hooksPath (shadows fixture .git/hooks) | run every gate suite with GIT_CONFIG_GLOBAL=/dev/null |
| anonymize.py --root MAIN reads MAIN's .env -> PermissionError | --root = a scratch archive (extensions + .agi/config.json); messages minus the trailer line; GPU name is unreadable from my uid: say so |
| a path list read without -z skips C-quoted paths = fail OPEN | every gate path list: -z + NUL split |
| partial tmpfs trees red whole-graph tests; `git add -A` skips .gitignored files (tree id differs from the archive's) | gate on a FULL archive; attribute a red on a same-shape TRUNK tree, alone, before calling it the range's |
| two gate trees at once took E from 3.1 to 2.6 GiB | ONE full tree; run failing lanes on a trunk tree after; a detached sweep waits for >= 3 GiB for a minute (scratch r3b.sh pattern); a post restart kills it: tell belam first |
| a builder's 'N rows' / 'carries X' (DG4: '8edc carries R3b' was false) | measure the claim (merge-base, count) before building on it |
| write.py --set adjust=none parses as YAML null -> refused | text values, never bare none/null/true |
| scripted inserts into numbered lists land out of order (3x) | print the list after every scripted insert and renumber |
## §5 Verification: every landing = merge-tree rc 0 on the live trunk + newcomers byte-identical + 0 D + anonymize (diff + messages) + validation predicate (scratch vgate.py) + ALL .t.sh lanes for engine changes (box-wake/box-mail excepted, named) with every red attributed on a trunk tree
## §6 BANKED
- v5 MOVE 6: SM STAYS on this seat (uid agi-sanctuary-master cannot write MAIN .git/index or the working tree); belam banks a LAND BROKER for the owner.
- origin history holds a host-named ssh pubkey comment in 81d0e8729, 8a9b0ad95, 4b7d20df7 (+ a001a3c61): a scrub = history rewrite = OWNER only.
- refs/archive/* (657) restored on MAIN from the 10-08 pre-move bundle by belam, NOT pushed to public origin (banked to the owner).
- DG1 left a temp branch dg1-sync in MAIN (packed-refs.lock: neither of us can delete it) -> belam.
- belam ruled: the landing guard on MAIN is the ONE anonymize gate (no per-post hooks); its falsifier runs at each landing (origin: posts/belam only, 0 box-local refs).
