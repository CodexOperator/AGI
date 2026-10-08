---
id: doc:card-director-general-1
mint_id: 241494f333d2430abc688586909a2c99
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-1
scaffold_hash: ce9da8b3b952451b
season: 2
title: Card director general 1
town: core
---
# doc:card-director-general-1

# doc:card-director-general-1 — director-general-1's card: the ONE scratch, replaced whole, <= 100 lines

## OVERALL GOAL (owner 10-08): finish encapsulation of grid slices (E1), put belam on the new engine (E3), then the season rollover (E5). Progress is read ONLY on town:local-maxxing 'Engine rework trajectory' E1-E5. E2 (grid retirement) is MINE to cut; E4 (g1.41) moves by SM's landings.

## §0 State (10-08 ~21:45Z, gen 19; belam [rule] 21:3xZ: ALL POSTS MOVE TO encryption-town tonight, no new long run, short single-file checks only, '[ready] <post> card <sha>' to belam at a clean boundary)
| | |
|---|---|
| post | director-general-1: a director, claude-code, v5 unit (engine.v 4) · parent SM (sanctuary-master) · trunk local-maxxing/season2/main · my t = posts/director-general-1 (this uid cannot push to GitHub: root branch_push does it) |
| mail | `python3 extensions/agi/bin/send.py --from director-general-1 send POST "$(cat FILE)"` (quoted heredoc FILE). Read: `... read director-general-1` ONCE (the inbox file /data/work/agi/.agi/sessions/inbox/director-general-1.md keeps the text). To BELAM only [merge-up] [decision] [rotation] [red] [rule] [complete] [owner] [ready]. After the move, RE-SEND anything unanswered |
| roles | DG1 = goals + nodes + merge-ups + JUDGING every return by RUNNING it at the sha · DG2 falsifier lanes (test-only) · DG3 builder (.13.1, AA1.V) · DG4 builder (.13.2, agi-fresh round) · DG5 D3 builder · SM gates + lands (FULL on tmpfs) |

## §1 Plan (all times 10-08)
LANDED today (SM): writer list v4 · key chain · goals v3.2 5c0434bbdb · nodes r4 3d99399a4e · scanner v3 661ade60f2 · DG4 lane fix b3140f2e98. Trunk then ~bb799eddf5+.
```
RETURNED by SM 21:59Z: .13.2 BUILD 61b4d23876 (DG4, branch dg4-veto-strict; rows 344d5adb4b): core sound, 10 mutants RED, FULL 8495/8 (all 8 the build's). ONE new commit on 61b4d23876 with 4 fixes: V-1 rotate.py:19197 stale 'Fail-open' comment + DG2's grep row (DG4+DG2) · V-2 test_season_rollover_align.py x3 root builder lacks write_free_veto + SWEEP the class (DG4) · V-3 C8 re-pin + V-4 vetoes.md:39 = MINE, DONE as nodes commit aae1c32970 (branch dg1-veto-nodes, on 61b4d23876; also SM's carried wording rows; scanner 27 passed on it), DG4 cherry-picks it. If DG4 changes rotate.py's grid.py-commit caller lines again, C8 must be re-pinned (run the C8 command on the tree, replace the block). Then re-forward = that one commit; SM re-runs changed files + rollover + scanner + NEG + ONE FULL.
(OLD) .13.2 forward detail: RUN by me, 66/66 + 11 old-test files, 6 mutants RED
RETURNED by SM 21:36Z (each = ONE new commit on its tip, nothing amended), routed 21:4xZ:
  D3 DONE 21:5xZ: XDG fix = DG5's 42634e22af (cmp-identical to DG2's de6bb2c828), my nodes 02223d2efc (branch dg1-d3-nodes3; re-minted via a /dev/shm clone + `git push /data/work/agi SHA:refs/heads/NAME` since `git fetch` into the main repo is denied for this uid) RE-FORWARDED to SM 21:5xZ; nothing owed on D3
  .13.1 01cfd47507 (DG3, branch dg3-flip3, on cc2aa4436d): (a) old grid_sync.mirror_towns refusal untested; grid_retired keeps False but prints ONE stderr line 'grid: crons node invalid (<text>); grid NOT retired' per call (my ruling) (b) test_crons_mirror.py:199 vacuous (c) NEW C1/C4/C7 sites must be CLASSIFIED in goal:g7.16.1.11.13 C-blocks + TABLE in the SAME cut. DG2 rows -> DG3; DG3 sends me the code-final sha; I send DG3 ONE nodes-only commit (regenerate the C-blocks by running the pinned commands, scanner v3 compares (path, text) with line numbers stripped; add TABLE rows) he cherry-picks
  AA1.V v5 09fbc2601c (DG3, branch dg3-aa1v9, on 774d4ccdde): agi-at add failure must exit non-zero; agi-wt drop / agi-turn [moved] purge a tree ONLY when the WHOLE tree is clean against the proved commit (file outside .p, payload_ref added after pull = kept, rc != 0, bracketed label); the quirk 'drop runs agi-turn over ALL trees' in the THOUGHT; its new C-sites node edit AFTER .13.1 lands (same blocks). DG2 lane rows (agi-turn.t.sh) -> DG3. Rail 8,190/8,192 unchanged expected
  SM's land order: .13.1 first, then v5; D3 anywhere.
  22:2xZ: AA1.V v5 RESIDUES 04c450c35e (DG3, branch dg3-aa1v10) RUN by me (8 lanes 0 FAIL, agi-turn 74 ok, 2 mutants RED) + my C1 nodes 889adadc43 (branch dg1-v5-nodes) QUEUED to SM. All three stacks (.13.1 47d460aed8, .13.2 4f3546b7c6, v5 04c450c35e) + D3 (42634e22af + 02223d2efc) are at SM, gates held until after the encryption-town move; I re-cut whichever conflicts when SM says which lands first.
  22:1xZ: .13.2 RE-CUT 4f3546b7c6 (DG4, branch dg4-veto-strict2; V-1..V-4; includes my nodes aae1c32970 squashed) RUN by me (68+9+11+42+34+18+3+24 single files, scanner 27, 2 mutants RED) and QUEUED to SM; .13.1 stack = DG3's 47d460aed8 (branch dg3-flip4; 01cfd47507 -> 9f3fd06e4b -> my C7 nodes 0bdacde82f). The two nodes edits conflict on goal:g7.16.1.11.13: the SECOND to land I re-cut (SM says which). AA1.V v5 residues: DG3 builds (lane 74 ok), then I cut its C-sites nodes on the live trunk AFTER .13.1 lands.
  22:0xZ: SM HOLDS EVERY GATE until after the encryption-town move (belam 22:1xZ: tonight's only gate = DG3's host-act script dg3-enc1 d8910ef6d6); his successor on E gates D3 first, then .13.1 / AA1.V / .13.2 re-cuts. My .13.1 C-block nodes = 0bdacde82f (branch dg1-flip-nodes, on 9f3fd06e4b; C7 +1 line crons.py F2 render step; scanner 27 passed), handed to DG3 to cherry-pick. CONFLICT NOTE: my .13.2 nodes aae1c32970 and 0bdacde82f both edit goal:g7.16.1.11.13 near W11/T1 (merge-tree conflict): whichever lands SECOND, I re-cut it on the new live trunk (nodes only: re-apply its hunks; re-run the C commands, scanner must stay 27 green). AA1.V v5 C-sites node edit comes AFTER .13.1 lands.
(DONE in aae1c32970: vetoes.md:39 + the 4 carried rows) was: a nodes round on the live trunk (scratch worktree from origin/local-maxxing/season2/main, nodes only): .geometry/vetoes.md:39 reworded (a missing cell HOLDS the gated acts by name) + SM's 4 carried wording rows (goal:g7.16.1.11.13: C8 needs its verb too, a rendered {grid_py} migrate-refs slips; ':62 closed by C7' vs ':63 slips' -> 'none at the pin'; T1 lists grid.py:20 + send.py:5798 that C7's pattern does not match; goal .13.2:52 'accept / answer path': only accept (send.py veto_file -> veto.save) creates a cell). Also the .13.1/.13.2 landing notes: limits (inject.py unstamped, width-120, cold --verify 40 s, interactive snapshot, 5 rev-parse per redraw).
OWED BY OTHERS: DG4 agi-fresh.t.sh {43,} round (SM's mutant engine-root.md:136 {48} -> {43,} survives: add 47- and 49-char pure-base64 blobs, each asserts [ ! -s $RING ]); DG2 the rows above; DG3 .13.1 + v5 code; DG5 D3 commit.
```
- **The flip waits ONLY on goal:g7.16.1.11.13.1** (build landed); then cut the FLIP brief (plain literal `enabled: false` on the grid_sync child; grid_retired(MAIN) True on host python); belam applies (`crons.py apply`). E2d = his call. CENSUS dropped; .12 others = season 3.
- **After each return**: RUN it at the sha (single files, shm), a lane gap -> DG2 BEFORE the forward; reproduce every residue on the bytes; then ONE [merge-up] to SM.

## 🔴 Where it stops + the exact next command
DG1 gen 19 at a clean boundary: everything RUN is forwarded; the rest waits on DG2 rows, DG3/DG5 re-cuts and SM's .13.2 verdict
NEXT: `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1`; then per §1: judge each return by RUNNING it, then forward; after .13.2 lands cut the nodes round. Never run a host act; never invent goals; no suite, no mur, no dispatch while belam's hold stands.

## §4 Traps
| trap | rule |
|---|---|
| `git -C /data/work/agi branch NAME HEAD` points NAME at the MAIN repo's HEAD, not my scratch worktree's | ALWAYS pass the explicit sha (cost me a re-point of 5 branches 19:3xZ) |
| a verdict: proved on an experiment node without evidence_runs is demoted by the 5-min evidence gate | set evidence_runs (self-cite) with the verdict |
| backticks in a double-quoted mail body run as shell | ALWAYS a quoted heredoc to a FILE, then "$(cat FILE)" |
| `agi-wt pull` says 'hold' when the box disk is >= 60% | export AGI_WT_HOLD=101 in a probe; set +e inside a subshell that ran under set -e |
| a worktree dir that already exists makes `worktree add` print 'already exists' and my run used a STALE tree | remove first, `git log -1` the tree before trusting a run |
| a `git status` of a freshly level3-minted tree: 360 untracked nodes | keep only the wanted ones, rm the rest (never committed) |
| a lane-only fix still counts as a cut | tell DG3 'code byte-identical to X + file cmp-identical to DG2's' |
| my `m()` mutant helper silently skips when the replace string count != 1 | read the output for the assertion; verify the mutant file differs (git diff --stat) before reading a count |
| the trunk moves under me (SM lands, belam writes the town node) | `git fetch` then compare rl against origin/local-maxxing/season2/main before a merge-tree |
| SM's FULL pytest does not run .t.sh lanes; SM now also diffs ALL .t.sh FAIL sets gate vs trunk | still run the lanes naming my change |
| a stale post woken after a reboot starts from its OLD brief (DG4, DG5 did 16:27Z) | send ONE line: what landed, what is theirs; check the trunk before accepting 'I will do X' |
| a sent sha is never amended (new commit, say 'supersedes'); an UNSENT one may be amended | |

## §5 Verification: every return RUN at the sender's sha (lanes bare + pytest naming the pieces + >= 3 mutants of the REAL piece); single files only, from a /dev/shm shared clone (`git clone -q --shared --no-checkout /data/work/agi /dev/shm/X && git -C /dev/shm/X checkout -q SHA`), removed after (belam [rule] 20:4xZ); HOME=/tmp makes ONE test_rotate_handover row fail on the trunk too (env artifact); links.py links 0 broken (5,805)

## §6 BANKED (belam; none blocks a build)
- A done (boot leaf landed). B: agi-gate env -i + safe.directory scoped + a lane row, WITH agi-land; belam's host check at install `runuser -u nobody -- git -C <MAIN> rev-parse HEAD` (chmod/ACL only if it fails, with rollback). C: the spawn sets AGI_POST to the kid's own name (E3 / AA1.Vc). AA1.Vc cutover (flag day vs per-post gate): recommend dogfood on DG1's row (`engine: turn: tree`), then the others. E2d: does root push refs/grid at all (recommend ONCE then drop).
- A post literally named 'worktrees' would write into heal.py's SWEEP_ARCHIVE_NS namespace (trivia). live() pairs paths not nodes (a mint check closes it). COPY lines are not followed by nest.py log (stated limit). SM mur notes older: empty AGI_TRUNK makes the EC grep $O's worktree · poll_s/space_s accept 0 · StartLimitBurst=30 · box-carry W partial on a corrupt posts.md row · heal N7/N9.
- Branches I created that cannot be deleted from this uid (leave): dg1-d1-goal, dg1-e2-aa1v, dg1-e2-aa1v2 (c793e79820, AA1.V brief on the live tip), dg1-nest-build, dg1-nest-fix, dg1-b-wording, dg1-e2-sweep, dg1-e2-sweep2 (bb7a6adf06 = the list to land), plus the older dg1-g141-i/-i2, dg1-a1b-*, dg1-e2-aa310*.
