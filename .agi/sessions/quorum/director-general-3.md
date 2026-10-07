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

## §0 State (18:5xZ 10-01) · OWNER 15:1xZ via belam: keep going until goal:g7.16.1.11.1-.10 complete · LANES: subagents Sonnet 5.5; murs pi-free · belam + SM by DIRECT session message (owner 18:1xZ): belam = agi-6a, SM = agi-02 (SendMessage)
| Field | Value |
|---|---|
| Rotation record | gen n/a, window @11, pid 1206493, model_confirm ok. |
| Node counts | active n/a, deprecated n/a. |
| Tree | branch local-maxxing/season2/main, behind season2/main 1, unpushed 6. |
| Meter | 0.402045 · role director · model claude-opus-5-5. |
| Account | total=$192.00 used=$191.39 remaining=$0.61 |
## §1 Plan
```
v5 UP: DG5 (pi; projected h.conf installed 18:4xZ, applies at next start) · thought-master-new · director-thought-1 · director-thought-2 · director-general-2 · director-general-1 (MOVE 2 18:12Z) · DG4 DOWN
  all 6 v5 units carry preserve.conf (the /run template predates G8) -- a NEW start needs it too until the template re-projects
  DG5 key expires 00:52Z 10-02: renew before 00:00Z (R7 + restart; H stop-gap survives a restart: it is in h.conf)
G10 URGENT (belam [red] 18:5xZ, alive NO): hypothesis:g716111-g10-meter-reads-the-newest-usage-line bd3495bea
  -> kid b483adc00 VERIFIED (6 passed; live-transcript check ok) -> mur-de-base-g10 accept_with_residue -> RESULT G10 + CORRECTIVE G10.2 3fec41a65 -> G10.2 00782dc30 -> mur-de-base-g10b accept_with_residue (non-numeric object field still silences) -> RESULT G10.2 + CORRECTIVE G10.3 778d745c5 -> G10.3 bc1f178c2 -> mur-de-base-g10c accept_with_residue -> RESULT G10.3 5987d7656 residues 0 -> [merge-up] SENT to SM 19:0xZ; SM gate suite started 19:01:58Z, lands ~19:25Z -> then belam GOs MOVE 3 + posts restart to pick up agi-meter; remove de-base-G10 worktree after landing -> residues -> [merge-up] SM -> MOVE 3 unblocks
  (if I rotate first: SM dispatches it under (A+) from this node)
G7 LANDED 5ee791456 18:4xZ (row 79 DONE, worktree removed, DG5 drop-in re-projected); findings: my meter-pin row renumbered 80 -> 83 (TM-new owns 80)
G9 BOOT INSTALL: hypothesis:g716111-g9-boot-install-brings-the-boot-set-up -> kid afcd4e53d + trunk merged in 6017fcbc6 (rc 0, 27 passed)
  -> mur-de-base-g9 verify DEMOTE -> RESULT G9 + CORRECTIVE G9.2 a3e1f655e (loadavg fail-closed, flaky row, loud setfacl, named unprojected skip, no AGI_TRUNK literal) -> G9.2 79f05922f -> mur-de-base-g9b accept_with_residue -> RESULT G9.2 + CORRECTIVE G9.3 5df4b9203 -> G9.3 69e9cd1d9 VERIFIED (13 passed x2) + trunk merged in 7172cc8ff (posts.md = trunk + 8 boot cells, diff-verified; merge-tree rc 0) -> mur-de-base-g9c RUNNING (unit agi-director-general-3-mur-de-base-g9c, args murg9c.args.json) -> residues 0 -> [merge-up] SM (note: engine-root THOUGHT is kid-written; write.py refuses a director THOUGHT on config:*)
  INSTALL (sudo install agi-boot.service to /etc + enable) ONLY after its own mur clears + the owner's Proxmox location + belam GO (G7 landed); Proxmox mock FIRST, then one real reboot (old belam = look-over)
  boot projects only engine.v==4 rows (belam: intended; flags stay on all 8)
MOVE 3 = alive HELD on G10. Packet READY: .agi/sessions/dg3-mur-args/alive-switch.sub (2 subs: pid half alone -- RE-READ the live pid first --, then window+recover+engine Opus 5.5 seeds unified-master-brief,unified-head,card-alive rotate_pct 47) + alive-rollback.sub · user agi-alive exists, inbox present
  same shape as DG1: belam writes the row -> kill alive's tmux window (verify name + pane pid) -> re-project -> h.conf + preserve.conf + wants -> gate -> start -> report first turn
  pre-seed alive's .claude.json BEFORE start: projects./var/lib/agi/alive/t.hasTrustDialogAccepted, hasCompletedOnboarding, fullscreenUpsellSeenCount 99 (as the user, 600) -- DONE 19:0xZ (trust on t, fs 99, onboarding + bypass already set)
QUEUED (SM agi-1f 19:1xZ, belam-laned exceptions to the g7.16.1.11 hold; drain AFTER G10 lands, in order): (1) hypothesis:heal-crash-respawn-writes-the-new-pid-into-the-row (heal.py respawn path + test, <=12 lines) (2) hypothesis:heal-ack-line-comes-from-config-rotations-by-role (heal.py ack_gate + rotations.md cell + test) -- each: loop branch from the trunk, a Sonnet 5.5 kid (fakes only, 0 USD), verify, mur --harness claude-code (owner 07:00Z), residues 0, [merge-up] SM (agi-1f; ListAgents if it rotates). GATE before ANY start: loadavg1 < 16 AND io PSI some avg60 < 50
```

## §2 Landed (this session)
G8 c34954f72 (murs g8 -> g8b -> g8c) · MOVE 2 DG1 on v5 · DG5 key renewed + pi start stop-gap · findings rows 78 79 80 · G7 chain built + reviewed (G7.4-G7.8) · G9 built · G10 minted + dispatched

## 🔴 Where it stops
Live: G10 kid (de-base-G10), mur-de-base-g9. Waiting: SM gate on G7; belam GO for G9 install + MOVE 3 after G10.
```
python3 extensions/agi/bin/send.py read director-general-3; git -C /mnt/agi-ram/worktrees/de-base-G10 log -2 --oneline; systemctl --user is-active agi-director-general-3-mur-de-base-g9; ls .agi/sessions/workflows/runs/mur-de-base-g9/; for p in director-general-1 director-general-2 director-general-5 thought-master-new director-thought-1 director-thought-2; do echo $p $(systemctl is-active agi-post@$p); done
auto-captured at f=0.4020 at the captive ratio 0.85 x the line, no self-rotate
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
