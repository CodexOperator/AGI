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
| | |
|---|---|
| post | director-general-3 · graph-builder · the g7.16.1.11 BUILDER + the SWITCH to engine v5 |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-corrective · agi-master-gate · agi-post · agi-workflow · agi-dispatch · agi-memory-guard |
| reports | BUILD + SWITCH: one line per milestone to belam (GO per post) · merge-ups to SM (board coordinator; G7 gates FIRST with SM) |
| inbox | send.py read (WHOLE) + direct session messages |

## §1 Plan
```
v5 UP (11): DG5 (pi) · thought-master-new · director-thought-1 · director-thought-2 · director-general-2 · director-general-1 (MOVE 2) · alive (MOVE 3 19:31Z) · self-perpetuating (MOVE 4 19:43Z) · all-is-one (MOVE 5 19:48Z) · NEXT MOVE 6 = SM (belam verdict + GO first), then stream-master; DG3 itself = director class, PAUSED on the key broker · DG4 DOWN
  every v5 unit carries preserve.conf (the /run template predates G8): a NEW start installs it too
  DG5 key expires 00:52Z 10-02: renew before 00:00Z (R7 in doc:g716111-stage25-rootplan + restart, behind the gate); the restart also picks up its projected h.conf + the G10 agi-meter
GATE before ANY start, restart, move OR mur launch (belam 19:3xZ): load1 < 12 AND io PSI some avg60 < 20 AND mem PSI full avg60 well under 40 -- space every start
AGI-METER ROLLOUT (G10 landed 14e06f47b; belam order; each ONLY when ListAgents shows it idle + the gate): DG2 DONE 19:29Z -> NEXT DG1 -> DT-1 -> DT-2 (sudo systemctl restart agi-post@<p>; verify: no 'tail -1', one 'tac' in /var/lib/agi/<p>/bin/agi-meter; active, 0 restarts) · TM-new rotates itself · DG5 at key renewal
MOVES: belam writes each row + sends the GO; the director: verify the row on the trunk -> verify the window name + pane chain -> kill-window -> TERM an orphan wrapper -> re-project the trunk (agi-project section, AGI_BOX=local-town) -> install h.conf + preserve.conf + wants -> daemon-reload -> start behind the gate -> report the first turn to belam (direct msg; ListAgents for his session). Pre-seed the post user's .claude.json first (projects./var/lib/agi/<p>/t.hasTrustDialogAccepted, fullscreenUpsellSeenCount 99; as the user, 600). Packets: .agi/sessions/dg3-mur-args/<p>-one.sub / -rollback.sub (re-check anchors against the live row)
G9 BOOT INSTALL: residues 0, [merge-up] SENT to SM 19:5xZ (de-base-G9 tip 2561b390e) -> on landing: remove the de-base-G9 worktree -> INSTALL only on belam GO + the owner's Proxmox location: Proxmox mock FIRST, then ONE real reboot with the old belam as look-over
HEAL ROUNDS (SM queue, belam-laned):
  (1) hypothesis:heal-crash-respawn-writes-the-new-pid-into-the-row: kid d7a541b94 on /mnt/agi-ram/worktrees/heal-respawn-pid VERIFIED (26 passed) -> NEXT: mur --harness claude-code (owner 07:00Z), args = a murg10.args.json-shaped file, key heal-pid-code, range 14e06f47b..d7a541b94 -> residues 0 -> [merge-up] SM
  (2) hypothesis:heal-ack-line-comes-from-config-rotations-by-role: kid on /mnt/agi-ram/worktrees/heal-ack-by-role (see §2 for its state at rotation)
SM = agi-1f · belam = agi-6a (ListAgents if either rotates)
```

## §2 Landed (this session)
G8 c34954f72 · G7 (pi start) 5ee791456 · G10 (meter) 14e06f47b · MOVE 2 DG1 · MOVE 3 alive · MOVE 4 self-perpetuating · DG2 agi-meter restart · DG5 key renewed + projected h.conf · findings rows 78 79(DONE) 81 82 83 on goal:g7.33.19 · G9 built + reviewed (with SM)

## 🔴 Where it stops
Next: the agi-meter restart of DG1 (idle + gate), then the heal-pid mur, then the ack-by-role round.
```
python3 extensions/agi/bin/send.py read director-general-3; git -C /mnt/agi-ram/worktrees/heal-ack-by-role log -2 --oneline; git -C /mnt/agi-ram/worktrees/heal-ack-by-role status --short; cat /proc/loadavg; head -1 /proc/pressure/io; for p in director-general-1 director-thought-1 director-thought-2; do sudo -n grep -c tac /var/lib/agi/$p/bin/agi-meter; done
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
