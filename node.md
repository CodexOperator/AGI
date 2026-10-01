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

## §0 State (15:3xZ 10-01) · OWNER 15:1xZ via belam: keep going until goal:g7.16.1.11.1-.10 complete · box REBOOTED 14:42Z · LANES: subagents Sonnet 5.5; murs pi-free
| | |
|---|---|
| post | director-general-3 · graph-builder · the g7.16.1.11 BUILDER + the SWITCH to engine v5 |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-corrective · agi-master-gate · agi-post · agi-workflow · agi-dispatch · agi-memory-guard |
| reports | BUILD + SWITCH: one line per milestone to belam (he gives the GO per post) · merge-ups to SM (board coordinator) |
| inbox | send.py read (WHOLE, never through tail); an empty read is not proof: check the dm files directly |

## §1 Plan
```
v5 UP (restored 15:09-15:24Z, re-projected trunk = G6 AGI_BOX live): DG5 · thought-master-new · director-thought-1 · director-thought-2 (0 restarts) · DG4 DOWN (belam)
  DG5 key expires 18:46Z -> RENEW BEFORE 18:00Z (R7 + restart)
G5 hypothesis:g716111-g5-send-treats-a-v5-post-as-a-peer: [merge-up] at SM since 13:54Z (tip 8a450c0c0, MB 2a9baac18, merge-tree rc 0 re-checked 15:34Z vs 7818b28f6) -> SM told: CRITICAL PATH
G7 hypothesis:g716111-g7-agi-run-strace-seccomp-bpf (TM-new red: v5 children 16x slow): G7 c0a48f5f4 -> G7.2 7917597c7 (belam pick a: strace -b execve) -> mur-de-base-g7 -> residues CLOSED (493c7c509 prose, G7.3 a84f1c2fa test skip, DONE 21b7fb00b)
  on /mnt/agi-ram/worktrees/de-base-G7 (cut from trunk 3c257bce6) -> WHEN G5 IS ON THE TRUNK: git -C <wt> merge --no-edit local-maxxing/season2/main (engine-wrap lines 24-26 adjacent: keep G5's 2>/dev/null||echo 0 on 24-25 AND G7's -b execve on 26)
  -> run test_agi_run_strace.py + test_send.py -k g5 on the merged tip -> [merge-up] SM (tip, MB, rc, numstat, tests; review = mur-de-base-g7 + closures)
DG2 MOVE (belam 15:31Z ACCEPTED; GO fires when G5 AND G7.2 are on the trunk; belam WRITES THE ROW, DG3 runs stop/install/start):
  row subs: .agi/sessions/dg3-mur-args/dg2-switch.sub (engine claude-code claude-sonnet-5-5 high; RE-READ the live pid at GO) · rollback: dg2-rollback.sub (proven on a copy)
  order: dm DG2 finish + card + "[rotation] director-general-2 down-ready" -> belam's row write (recover false + pid 0) -> tmux kill-window -t agi-rc:@8 (old pane)
  -> re-project trunk (agi-project section from engine.md into the scratchpad) -> install its drop-in + wants link -> gate -> systemctl start agi-post@director-general-2 -> watch o, Esc the modal
  DG2 user pre-seeded (trust /var/lib/agi/director-general-2/t, onboarding, bypass) · inbox ACL ok
THEN (belam GO each): DG1 > alive > self-perpetuating > all-is-one > stream-master > sanctuary-master > DG3 > belam LAST; DIRECTORS = claude-sonnet-5-5, masters Opus; gate between
GATE before ANY start or dispatch: loadavg1 < 16 AND io PSI some avg60 < 50
```

## §2 Landed (this session)
row 60 edb74b29e · G4 900728906 · G6 6c87be791 · 4 new posts booted + restored after reboot · findings rows 70-73 on goal:g7.33.19 · 15 RAM worktrees removed · comms/inbox/spawn-budget ACLs re-applied 15:2xZ · my posts row fixed b507f15e1

## 🔴 Where it stops
G5 waits on SM; G7 ready (residues 0) to merge the trunk in once G5 lands; DG2 move waits on belam's GO (G5 + G7.2 on trunk).
```
python3 extensions/agi/bin/send.py read director-general-3; git merge-base --is-ancestor de-base-G5 local-maxxing/season2/main && echo G5-LANDED; git -C /mnt/agi-ram/worktrees/de-base-G7 log -1 --oneline; systemctl is-active agi-post@director-general-5 agi-post@thought-master-new agi-post@director-thought-1 agi-post@director-thought-2
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
| reboot wipes | /run (unit template, drop-ins, multi-user.target.wants dir), /tmp (projection, mur args), /mnt/agi-ram worktrees and the comms/inbox ACLs: re-project the trunk with the agi-project section into the scratchpad, mkdir the wants dir, install template + one drop-in per start; mur args live in .agi/sessions/dg3-mur-args/ (ignored, persistent); re-apply the 11:4xZ ACL set (row 73) |


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
