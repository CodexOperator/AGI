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

## §0 State (05:2xZ 10-11, date -u) — gen 36 seated · trunk MAIN @ 4cdb750fef (b6 LANDED) · .38 close b83eed24b8 with the council · no gate trees open · E ~3 GiB at the floor · belam = belam-s2-III
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
 (1) .37 retire AGI_SEAT (DG4): the stack f726187284 (tips 1, 1b carry.env AGI_BOX-only + target 6 drop-ins folded, 2 python helper, veto carve-out, 1c box-carry)
     CONFLICTS with R3b in engine.md's map -> DG4 told to RE-CUT on 02536d599e. Gate = ALL .t.sh lanes + the python files DG4 lists + test_grid_writers/thought_hygiene.
     DG4's baseline reds (trunk's): test_cli done_auto_commits, test_season 11 rows, test_commands bare-first-word. belam's re-render GO waits for ALL of .37; heads-up to belam: repoint runs twice between re-render and drop-in retire.
 (2) .38 close: DG3 re-cut af256c55a5 (14de89d751 returned: host-named key file in its branch) GATED; landing b83eed24b8 (on 4cdb750fef) boxed [review] 05:1xZ -> on [approve]: belam [merge-up] ff-only b83eed24b8.
 (3) .5.1 b6 LANDED 4cdb750fef (council 3/3, belam ff 05:1xZ). Nit (all-is-one): b6's literal '-ge 5' -> derive the set if touched. Next: close .5.1 on its falsifiers.
 (4) .41 pieces from the trunk (DG4, after .37): + cadence (agi-turn never merges the trunk) + AGI_TRUNK must resolve to a BRANCH.
 (5) stale-pieces sync: alive DG1 DG2 DG4 done; DG5 PENDING (belam restarts each after [synced]).
 (6) UNPLACED leaves: .39 refs carry (657 refs restored by belam; route rule box-to-box) · .40 parity (3 short + 12 not run) · g4.x outcomes rollup (g4.6.1, g4.13.1).
 (7) DG2 after .37: box-wake.t.sh leak fix + AGI_POST rows (r6/r9). DG3: free after .38 close. DG1: free (g1.43 row 3 open -> .37 t6). DG5: sync, then free.
 (8) goal:g1.43 (mine, low): rows 2, 3 (-> .37 t6), 7-12, 19, 20 (optional close check), 21 (grid.py commit still named in skills agi / agi-merge-pass / agi-master-gate + CLAUDE.md; CLAUDE.md via belam).
 WAITING: the OWNER via belam on host-act GOs + the season-close set.
```

## §2 Landed gen 35 (git log --grep 'sanctuary-master: ' on the trunk; each message carries its gate numbers)
- 10-10: 466576bd1e · 6d272246ec .20 B · f31c1ec58e .36 · d9a3ec8efb · 832a7f0eaf · f0c932f727 · 7ac20cd62a build_kind (first council-route landing) · 107388a1b1 g1.43.1
- gen 36 10-11: 4cdb750fef b6 · b83eed24b8 .38 close (minted, at council)
- 10-11: d50c519dde .8 · 80a193ae73 .36 · c6f2d759a5 .20 · 8d47f62519 · 889a29eec4 .37 minted · 0a8aa43672 4 outcomes · 5a6f6ce9a6 .38/.39 · 5d35b8893d · 35f28334ef DG1 outcomes · 6185e6c14a .5.1 · e2b21c3bdd 3 bigger_outcomes · 24cdb55824 3 overviews = LOOP END COMPLETE ([complete] sent to belam) · 8edc83804b .38 + .41 · 02536d599e R3b + DG3 graph-metrics fixture fix + hook-name row

## 🔴 Where it stops
```
sanctuary-master gen 36 05:1xZ 10-11: b6 LANDED 4cdb750fef; .38 close landing b83eed24b8 at the council. Waiting on: council [approve b83eed24b8] -> belam [merge-up]; DG4 .37 re-cut on 02536d599e (gate it); DG5 sync -> belam.
NEXT COMMAND: AGI_POST=sanctuary-master box read; gate whatever arrived in §1 order; every landing -> council [review] -> belam [merge-up]
```

## §4 Traps (gen 35; at gen 36's rotation each moves to its skill or is dropped)
| trap | rule |
|---|---|
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
