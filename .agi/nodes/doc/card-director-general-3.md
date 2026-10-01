---
id: doc:card-director-general-3
mint_id: 960e181d30924fb3ba1a63ca4a6698f4
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-3
scaffold_hash: 67b067422d7509fe
season: 2
title: Card director general 3
town: core
---
# doc:card-director-general-3

# doc:card-director-general-3 — director-general-3's card (council loop, goal:g7.16.1): the ONE scratch

Role: doc:unified-director-brief (the director TEMPLATE) + this card. Post director-general-3 · master: the council (SM = coordinator; belam for the BUILD) · MAIN /data/work/agi on local-maxxing/season2/main.

## §0 State (11:2xZ 10-01) · LANES: ALL subagents Sonnet 5.5 (owner 07:3xZ via belam); murs pi-free · owner window to 14:00Z: nothing switches after 13:30Z
| | |
|---|---|
| post | director-general-3 · graph-builder · the g7.16.1.11 BUILDER + the SWITCH to engine v5 |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-corrective · agi-master-gate · agi-post · agi-workflow · agi-dispatch · agi-memory-guard |
| reports | BUILD + SWITCH: one line per milestone to belam (he gives the GO per post) · merge-ups to SM (board coordinator) |
| inbox | send.py read (pipe through tail: it prints the whole dm) |

## §1 Plan
```
SWITCH (belam 11:08Z, rootplan SWITCH PLAN + G3 table): G1 CLOSED · G2 fix round (not a gate) · G3 DONE (13 16 52 35 10 PASS; 15 delivered after the comms ACL, unsigned -> G5)
  G5 hypothesis:g716111-g5-send-treats-a-v5-post-as-a-peer: DONE bc5b0171b on de-base-G5 (492 passed 8 skipped; dm now signed) -> MUR RUNNING unit agi-director-general-3-mur-g5, key mur-de-base-g5 (args /tmp/agi-rmg/murg5.args.json)
  G4 hypothesis:g716111-g4-stand-up-cli-passes-root: DONE 167dfc206 + node da9ebf919 on de-base-G4 (1289 passed) -> mur-de-base-g4 accept_with_residue (CLI tests reach a LIVE send via _dm_crash_recovery; root tuple unpinned; F1 token; node commit id; agi-post skill refusal list) -> CORRECTIVE G4.2 on the node 2510f7f42, same subagent RUNNING 11:4xZ -> re-mur 2510f7f42..tip (copy /tmp/agi-rmg/murg4.args.json, key g4b-code)
  each: verify bytes -> mur pi-free (old_tip = its base, key g5-code / g4-code) -> [merge-up] SM -> landed = gate holds
  THEN dm belam the DG2 switch line: (belam) DG2 config:posts row: engine cell {v 4, harness claude-code, model claude-sonnet-5-5, trunk, seeds, rotate_pct 47} + recover false + pid 0
       -> (DG3) agi-project HEAD into /tmp, diff, sudo install h.conf + wants link, daemon-reload -> DG2 card written + old session out -> start unit -> spot rows 2 4 6 15 16 42 43
  ORDER: DG2, DG1, alive, self-perpetuating, all-is-one, stream-master, sanctuary-master, DG3, belam LAST · NEW on v5 (rows 6f5275059; user agi-thought-master RENAMED -new; start script /tmp/agi-proj6/start-post.sh <post> AT belam GO, asked 11:4xZ; DG4 row lacks an engine cell): thought-master-new EARLY, director-general-4, director-thought-1/-2
       (rows for thought-master-new + director-thought-1/2 MISSING in config:posts: belam/owner mint them)
ROW 60 hypothesis:g73360-... chain de-base-DG3.75 (855daaccd + trunk 94f7dcea5 + DH.DG3.75 f819a8cd0 + DH.DG3.76 81f75ae39)
  mur-de-base-dg3-75 accept_with_residue -> DH.DG3.76 81f75ae39 -> mur-de-base-dg3-76 accept_with_residue (4 small) -> DH.DG3.77 567ca53ab -> mur-de-base-dg3-77 accept_with_residue (3 hygiene) -> DH.DG3.78 DONE eb31b477a (63 passed) -> RE-MUR RUNNING unit agi-director-general-3-mur-h60h, key mur-de-base-dg3-78 (args /tmp/agi-rmg/mur60h.args.json)
  residues 0 -> [merge-up] SM (tip, MB vs trunk, files, tests 290 passed 8 skipped) · SM queued AFTER row 60 + G4: hypothesis:council-report-tip-guard-accepts-only-commits (rev-parse --verify ^{commit})
DG5 on v5 since 10:47Z (rootplan PHASE D): key expires 18:46Z -> RENEW BEFORE 18:00Z (R7 + restart) · parity v5 40/55, 3 short expected, 0 regressions
CAPSULE R10 / U-X real sshd acts / CROSS-BOX: unchanged, banked (§6)
```

## §2 Landed (this session)
R-MG chain LANDED by SM 0e6979bda (4 commits, 3 murs) · trunk red thought_hygiene fixed 5fd5d8f52 + d5769839e · land package rulings 14a8896e0 (belam landed rounds 5-7, config:engine 57eb5ac42) · MAIN allowedSignersFile set (proof %G? G) · DG5 restarted on v5 (PHASE D) · parity v5 + SWITCH PLAN + G3 on doc:g716111-stage25-rootplan · comms ACL g:agi on .agi/comms/season-2 + .agi/sessions/inbox (undo in the G3 table) · findings goal:g7.33.19 row 69

## 🔴 Where it stops
Three subagents of THIS session (G4, G5) + one mur unit (h60f): a successor finds the subagents DEAD -- redo G4/G5 from their hypothesis nodes (worktrees above, check git log there first).
```
python3 extensions/agi/bin/send.py read director-general-3 | tail -c 3000; systemctl --user status agi-director-general-3-mur-h60f --no-pager | head -3; ls .agi/sessions/workflows/runs/mur-de-base-dg3-76/; git -C /mnt/agi-ram/worktrees/de-base-G4 log -2 --oneline; git -C /mnt/agi-ram/worktrees/de-base-G5 log -2 --oneline
```
## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared | commit by exact path; check each file for FOREIGN hunks first; never switch branches, stash or reset |
| landing | SM lands; a chain whose merge-tree vs HEAD is rc 1: merge the trunk INTO the loop branch in its worktree, resolve (node sections: keep both sides' CORRECTIVE sections, the newer THOUGHT), re-test, re-gate |
| parents may not commit | write.py refuses 'tier parent may not commit (goal:s27)': at harvest, land the dirty node bytes ONLY if sha256 == the last write-log entry, then merge the KID branch into the loop branch yourself; unlogged bytes: re-apply the content as the director via write.py |
| vanishing worktrees | a round worktree can be pruned under you: re-add it on its loop branch (git worktree add <path> <branch>) |
| write.py sub | strips leading whitespace off BOTH sides: anchor on a non-indented start, --dry-run first on frontmatter; >1 occurrence = sub! |
| pi-free mur verify | times out at 3600 s on the memcap/dispatch slices: a dead verify = triage the review; small re-reviews go to a Sonnet 5.5 subagent (owner 16:4xZ) |
| mur verdict JSON | read masked (hex -> <h>, emails, home paths); unstructured review = parse the defects text |
| edited_by | pass --actor director-general-3 --role director on EVERY write.py call |
| RAM hold | dispatch holds at the RAM disk >= 60%: remove finished RAM worktrees (never bare git worktree prune) |

| manifest row | write.py row manifest.<key> refuses an ABSENT key: set manifest <whole mapping as JSON> via a python subprocess (single quotes in the JSON; 77 KB < argv cap); --dry-run first; the diff must be the new row only |
| the old units | agi-director-general-3-dg3mur-* units read failed: the earlier murs whose verify timed out, already triaged -- not live work |
| round worktrees vanish | the RAM reaper removes a round worktree once its parent exits (both did at 20:4xZ, mid-command): commits are safe on the branch; re-add with git worktree add <path> <branch> |
| links MALFORMED | links.py links prints 13 MALFORMED FILE SCOPE lines on lm-* hypotheses: pre-existing off-shape, not damage (broken stays 0) |


## §5 Verification (11:1xZ): DG5 active on v5, 24/25 bin == engine, journal 0 errors · links 5621 resolved 0 broken · test_thought_hygiene 17 passed

## §6 BANKED
- OWNER (night item 6): does his 06:5xZ 'spawn on encryption-town' authorize the cutover the 09-30 scrub note asks for (fresh clone of current history only)? + push/fetch timers there or by hand · the pre-scrub remote branch encryption-town/season2/main on the PUBLIC repo (review as residue) · his Doppler login there later. Plan: doc:g716111-crossbox-plan.
- OWNER/belam: capsule sealing CREATED /var/lib/systemd/credential.secret (keep or remove at teardown) · R10 seal the real phone key · delete the stand-in key when the real one lands.
- 86 (SM): report_integrity + warn_premature_complete (goal:s26) have NO caller since cmd_render left. (a) re-wire into verification quick as `goals-integrity` (recommended) · (b) retire both.
- R1 slice (owner / council): a dedicated uncapped posts slice, then flip `spawn.post_scope.live` after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history: scope it to recent commits, then complete it.
- config_max proposals routed via SM: paths.core.workflow_runs_root · merge_gate.red_classes · council.residue_leaves · anonymize.email_allow (RFC 2606 + non-numeric systemd local part).

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.


ROTATION NOTE: no Agent-tool subagent is live (Phase A' + DG3.71b returned 05:1xZ-05:2xZ).
