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

## §0 State (15:1xZ 10-01) · WIND-DOWN LIFTED (owner 15:1xZ via belam: keep going until goal:g7.16.1.11.1-.10 complete) · BOX REBOOTED 14:42Z (/run, /tmp, RAM worktrees wiped; branches safe) · LANES: subagents Sonnet 5.5; murs pi-free
| | |
|---|---|
| post | director-general-3 · graph-builder · the g7.16.1.11 BUILDER + the SWITCH to engine v5 |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-corrective · agi-master-gate · agi-post · agi-workflow · agi-dispatch · agi-memory-guard |
| reports | BUILD + SWITCH: one line per milestone to belam (he gives the GO per post) · merge-ups to SM (board coordinator) |
| inbox | send.py read (WHOLE, never through tail: tail hides blocks for good) |

## §1 Plan (the owner's morning)
```
RESTORE after reboot (belam 15:03Z order: DG5 > thought-master-new > DT-1 > DT-2, ONE at a time, gate between): re-projected trunk into scratchpad proj7 (G6 live: AGI_BOX in every drop-in); template + wants dir re-created in /run; DG5 15:09Z · TM-new 15:16Z · DT-1 15:18Z UP (0 restarts) · DT-2 15:24Z -- RESTORE DONE, all 0 restarts. ACLs re-applied 15:2xZ (row 73). G7 hypothesis:g716111-g7-agi-run-strace-seccomp-bpf (TM-new red: v5 children 16x slow under strace -f): built c0a48f5f4 on /mnt/agi-ram/worktrees/de-base-G7, result on node 198f73be1 (threads NOT freed); belam PICKED (a) 15:23Z -> G7.2 7917597c7 (-b execve; 4 threads 0.043 s; pi-post track loss disclosed) -> mur-de-base-g7 RUNNING (unit agi-director-general-3-mur-g7, args .agi/sessions/dg3-mur-args/murg7.args.json, 3c257bce6..c65644b06) -> residues 0 -> merge trunk (with G5) INTO de-base-G7 -> [merge-up] SM. Then:thought-master-new (lane A, research loop; old TM on standby) · director-thought-1 · director-thought-2 · director-general-5 (key expires 18:46Z: RENEW BEFORE 18:00Z, R7 + restart)
v5 STOPPED: director-general-4 (13:00Z, belam: memory relief; wants link kept; restarts ONLY on belam's word, with an assignment)
G6 hypothesis:g716111-g6-projection-carries-agi-box: [merge-up] DELIVERED 13:24Z (tip 5a31a9cf7) -> LANDED by SM 6c87be791 (14:01Z) -- NO auto re-projection on this box (agi-project.path/.service not loaded): the morning moves RE-PROJECT HEAD into a fresh /tmp dir first (/tmp/agi-proj6 predates G5 + G6), diff, then install each h.conf; then remove /mnt/agi-ram/worktrees/de-base-G6
G5 hypothesis:g716111-g5-send-treats-a-v5-post-as-a-peer: chain G5 -> G5.2 -> G5.3 cfa9b3e27 -> G5.4 7dad3b4d4 -> G5.5 3315ac438 -> mur-de-base-g5e verify ACCEPT 11/11 MET -> record closed 8a450c0c0 -> [merge-up] DELIVERED to SM 13:54Z (tip 8a450c0c0, MB 2a9baac18, rc 0, 508 passed) -> SM: queued for the MORNING gate (merge-tree vs 6c87be791 re-run then)
  after G5 + G6 land: remove /mnt/agi-ram/worktrees/de-base-G5 and de-base-G6 (harvest write-log first, plain git worktree remove)
  (mur-de-base-g5e run files: .agi/sessions/workflows/runs/mur-de-base-g5e/)
  findings already filed for G5: rows 70 (size headers) 71 (write.py set took an invented key -- my slip) on goal:g7.33.19
MOVES (owner's morning, belam 13:00Z): G5 + G6 LANDED FIRST; then from DG2 in the ORDER below, ONE at a time, gate between each, the OLD session STOPPED before the NEW one starts
  ORDER: DG2, DG1, alive, self-perpetuating, all-is-one, stream-master, sanctuary-master, DG3, belam LAST
GATE before ANY start or dispatch: loadavg1 < 16 AND io PSI some avg60 < 50 (belam 12:58Z)
```

## §2 Landed (this session)
row 60 LANDED edb74b29e · G4 LANDED 900728906 (13:41Z) · 4 new posts booted on v5 (TM-new, DT-1, DT-2, DG4) · G6 built + reviewed clean · G5.3-G5.5 built · findings rows 70-72 on goal:g7.33.19 (b3bdbb998) · 15 landed RAM worktrees removed (RAM 59 -> 28 pct; records in .agi/sessions/harvest-20261001) · old DG3 scope (3 orphan itest loops) stopped · card re-linked dca759633

## 🔴 Where it stops
WIND-DOWN 13:5xZ: G6 LANDED 6c87be791; G5 queued for SM morning gate; no unit, subagent or round of mine is live. 15:07Z heal crash-resume: ack already answered continue; MAIN posts.md left DIRTY by heal on MY row (session_name "" -> agi-6a, but ListAgents names this session agi-e9 [9e8bc5]) -- not committed, not reverted: SM/belam to judge in the morning.
```
python3 extensions/agi/bin/send.py read director-general-3; systemctl --user is-active agi-director-general-3-mur-g5e; ls .agi/sessions/workflows/runs/mur-de-base-g5e/; systemctl is-active agi-post@thought-master-new agi-post@director-thought-1 agi-post@director-thought-2 agi-post@director-general-5
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
