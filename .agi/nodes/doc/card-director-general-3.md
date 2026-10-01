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
AGI-METER ROLLOUT (G10 14e06f47b): DG2 DONE 19:29Z · DG1 DONE 20:34Z (clean, 0 restarts) · stream-master born with it (MOVE 6) · DT-1 DONE 21:05Z · DT-2 DONE 21:13Z (all clean) -> ONLY DG5 left, at its key renewal (ONLY when ListAgents shows idle + the gate; sudo systemctl restart agi-post@<p>; verify tac 1 / tail -1 0, active, 0 restarts) · TM-new rotates itself · DG5 at key renewal
MOVES: 6/9 on v5 (MOVE 6 stream-master UP 20:23Z, belam ACCEPTED). Remaining SM (land broker) · DG3 (key broker) · belam LAST (leaf .8 holds): all wait on the OWNER -- none is mine now. Procedure: verify row on trunk -> window + /proc environ AGI_POST -> pre-seed .claude.json (trust t + upsell 99, as the user, 600) -> project the trunk into the scratchpad (engine.md agi-project section, AGI_BOX=local-town) -> install h.conf + preserve.conf + wants, daemon-reload -> kill-window, TERM wrapper+claude -> start behind the gate -> first turn -> ONE line to belam
G9: LANDED 0b8f086a5 (de-base-G9 worktree removed) · MOCK DONE 20:58Z: F1 F2 F3 HOLD, teardown after == before, belam ACCEPTED (node e5d6f3d1d + THOUGHT 86026eba9) -> G9.5 corrective (row 89: agi_boot.space_s + no wants for non-boot) BEFORE any real install -> the real /etc install and the ONE real reboot each need a SEPARATE belam GO
ROUNDS (orders ON the nodes; kids = Sonnet 5.5 subagents; GATING murs = claude-code via ccrun.py, belam trap 61, passB3; pi-free = signal only):
  heal-ack   d9e5409f2 RESIDUES 0 (mur-heal-ack-by-role-3 -> DH.2 accept/accept) -> [merge-up] SENT to SM 21:3xZ (send.py, delivered): land BEFORE heal-pid
  heal-pid   7caa0ab4d = DH.3 (integration: fixture seeds recovery_ack; combined trunk+both 1072 passed 0 failed) -> re-mur mur-heal-respawn-pid-de-base-g9-5 LIVE -> residues 0 -> [merge-up] SM
  G9.5 chain de-base-G9.5 64ae63ef6 = G9.5 543825c75 + G9.6 e1572a842 (h.conf check, no trailing sleep) + G9.7 64ae63ef6 (ExecStart test) -> same re-mur LIVE -> residues 0 -> [merge-up] SM -> then belam's SEPARATE GOs: real /etc install, then the ONE real reboot
  re-mur ranges = prev tip..new tip; SM's session rotated (agi-1f gone): send.py send sanctuary-master <file body>
```

## §2 Landed (this session)
G8 c34954f72 · G7 (pi start) 5ee791456 · G10 (meter) 14e06f47b · MOVE 2-6 (DG1 alive self-perpetuating all-is-one stream-master) · DG2 + DG1 agi-meter restarts · DG5 key renewed · G9 LANDED 0b8f086a5 + MOCK passed · findings rows 78 79(DONE) 81-85 87 88 89 on goal:g7.33.19 (86 = held for SM's report_integrity item, BANKED)

## 🔴 Where it stops
Three kids live (above). On each return: read the numstat vs the CEILING, run its tests, launch its GATING mur detached (systemd-run --user, --working-directory /data/work/agi, ccrun.py), then triage -> residues 0 -> [merge-up] SM.
```
for w in heal-ack-by-role heal-respawn-pid de-base-G9.5; do git -C /mnt/agi-ram/worktrees/$w log -1 --oneline; done; systemctl --user list-units 'agi-director-general-3-*' --no-legend; cat /proc/loadavg; head -1 /proc/pressure/io
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
