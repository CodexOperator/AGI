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

## §0 State (12:4xZ 10-01) · LANES: ALL subagents Sonnet 5.5 (owner 07:3xZ via belam); murs pi-free · owner window to 14:00Z: nothing switches after 13:30Z
| | |
|---|---|
| post | director-general-3 · graph-builder · the g7.16.1.11 BUILDER + the SWITCH to engine v5 |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-corrective · agi-master-gate · agi-post · agi-workflow · agi-dispatch · agi-memory-guard |
| reports | BUILD + SWITCH: one line per milestone to belam (he gives the GO per post) · merge-ups to SM (board coordinator) |
| inbox | send.py read (WHOLE, never through tail: tail hides blocks for good) |

## §1 Plan
```
belam 13:00Z [decision]: (1) TM-new = lane A (research loop; old TM on STANDBY) (2) G6 + G5.3 land BEFORE any move, via SM after their murs
  (3) DG4 STOPPED 13:00Z for memory relief (wants link kept; restarts only on belam's word, with an assignment, owner's morning)
  (4) NO MOVES TONIGHT: owner's morning, from DG2, gate between each, old session STOPPED before the new one starts (5) gate miss noted
v5 UP: TM-new (oomd-killed ~12:57Z, self-restarted, resumes -c) · DT-1 · DT-2 · DG5 · DG4 stopped
G5 hypothesis:g716111-g5-send-treats-a-v5-post-as-a-peer: G5.3 DONE cfa9b3e27 (items 1-5) · send neighbourhood on tip 497 passed 8 skipped
  -> mur-de-base-g5c accept_with_residue (R1 R3 M1 M2 confirmed; R2 demoted by design; R4 claim fixed) -> G5.4 WRITTEN on node 88d82457c (4 items: line-24 stat, foreign wording, heal repair gate, boxless pin) -> G5.4 DONE 7dad3b4d4 (prod +6, tests +40, 3 red on old, 500 passed) -> mur-de-base-g5d accept_with_residue (R1 = my own slip: set testable_claim=a made a NEW key -- FIXED unset+set; R2-R6 + M1 M2 M4) -> G5.5 on node c4adbd38a, Sonnet subagent LIVE -> verify bytes -> re-mur 7dad3b4d4..tip (copy murg5d args, key g5e-code) -> [merge-up] SM with findings rows: write.py set accepts an invented key (testable_claim=a) · (NNNN B) headers drift -> residues 0 -> [merge-up] SM
G6 hypothesis:g716111-g6-projection-carries-agi-box: DONE 016ba8f26 on de-base-G6 (AGI_BOX in the agi-project jq; red on old; agi-gate 0)
  -> mur-de-base-g6 accept_with_residue (verify refuted R1-R4; missed M1 one-box fixture) -> G6.2 DONE a3fdc5090 (mutation red pasted) -> mur-de-base-g6b review accept, verify node-prose residues CLOSED in-loop 94b5a735d..5a31a9cf7 -> [merge-up] DELIVERED to SM 13:24Z (tip 5a31a9cf7, MB 6b536b730, 9 passed) -> residues 0 -> [merge-up] SM
G4 [merge-up] DELIVERED to SM 12:5xZ (tip 40e921b6e, MB 1d9e7da5e, 1290 passed) -> AWAIT landing; then remove /mnt/agi-ram/worktrees/de-base-G4 · 13 landed RAM worktrees removed 13:2xZ (records in .agi/sessions/harvest-20261001; RAM 31%) · de-base-DG3.71 KEPT: an uncommitted council_report.py edit -- read it before removing
GATE before ANY start or dispatch: loadavg1 < 16 AND io PSI some avg60 < 50 (belam 12:58Z)
DG5 on v5 since 10:47Z: key expires 18:46Z -> RENEW BEFORE 18:00Z (R7 + restart)
```

## §2 Landed (this session)
row 60 LANDED by SM edb74b29e (tip 3c3ff20f5) · card re-linked dca759633 · 4 new posts up on v5 · G4 closed in-loop + delivered

## 🔴 Where it stops
Two murs running (g5c, g6); G4 awaits SM landing; belam owes: TM-new A/B/C, DG4 assignment, GO for the moves.
```
python3 extensions/agi/bin/send.py read director-general-3; systemctl --user is-active agi-director-general-3-mur-g5c agi-director-general-3-mur-g6; ls .agi/sessions/workflows/runs/mur-de-base-g5c/ .agi/sessions/workflows/runs/mur-de-base-g6/
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
| v5 boot: trust | a fresh post stops at the folder-trust dialog: set projects./var/lib/agi/<post>/t.hasTrustDialogAccepted in that user's .claude.json BEFORE start (as the user, 600) |
| v5 boot: inbox | an ABSENT inbox file makes the mail poll type mail+CR every 5 s (answers any modal): create it empty (g:agi rw) before start, until G5.3 item 5 lands |
| v5 boot: .fresh | agi-run eats ~/.fresh on the first start; a run that died before any turn restarts with -c = 'No conversation found': touch ~/.fresh as the user |
| v5 boot: modal | a 'Try the new fullscreen renderer' modal (Yes preselected) opens after turn 1: one Esc into /run/agi-<post>/i as the user |
| start gate | belam [red] 12:58Z: ONE post start at a time; between starts read loadavg1 < 16 AND io PSI some avg60 < 50 (cat /proc/pressure/io); 4 starts 3-4 min apart drove io PSI 88 and an oomd kill of TM-new |


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
