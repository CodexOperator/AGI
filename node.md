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

## §0 State (17:1xZ 10-01) · OWNER 15:1xZ via belam: keep going until goal:g7.16.1.11.1-.10 complete · LANES: subagents Sonnet 5.5; murs pi-free
| | |
|---|---|
| post | director-general-3 · graph-builder · the g7.16.1.11 BUILDER + the SWITCH to engine v5 |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-corrective · agi-master-gate · agi-post · agi-workflow · agi-dispatch · agi-memory-guard |
| reports | BUILD + SWITCH: one line per milestone to belam (he gives the GO per post) · merge-ups to SM (board coordinator) |
| inbox | send.py read (WHOLE, never through tail); an empty read is not proof: check the dm files directly |

## §1 Plan
```
v5 UP: DG5 · thought-master-new · director-thought-1 · director-thought-2 · director-general-2 · DG4 DOWN (belam)
  all 5 live units carry preserve.conf (RuntimeDirectoryPreserve=restart) -- a NEW start needs it too until G8 lands
  DG5 key RENEWED 16:52Z (R7) -> expires 00:52Z 10-02: renew before 00:00Z
  DG5 STOP-GAP 17:00Z: h.conf H = /usr/local/bin/node /opt/agi/pi/dist/cli.js ... (before-value .agi/sessions/dg3-mur-args/dg5-h.conf.before-1701Z) -- any pi post start needs it until G7.4 lands + re-projection
G8 (MOVES 2..9 HELD on it): G8.2 kid 626281b34 on de-base-G8 VERIFIED (7 passed, numstat 2/1 + 45/8, stash 0)
  -> mur-de-base-g8b accept_with_residue (D1 node text fixed b160c3fac; D3 + 2 missed -> CORRECTIVE G8.3 on the node; D2 refuted -> config_max proposal via SM) -> G8.3 ac87315dd -> mur-de-base-g8c accept_with_residue, last residue MEASURED (scratch unit: crash restarts, stop = exit-code visible) -> RESULT G8.3 94a803a40, residues 0 -> [merge-up] SENT to SM 17:4xZ (tip 94a803a40, mb 7144c3029, merge-tree rc 0 vs b8e76739d) + belam told -> WAIT: SM lands, belam re-GOs the moves
  -> residues 0 -> RESULT G8.2 record on the node -> merge the trunk IN if it moved -> [merge-up] SM -> tell belam (moves re-GO)
G7.4 ([red] to belam 17:02Z: G7.2 -b execve ends every PI post at start; claude posts fine): CORRECTIVE G7.4 on hypothesis:g716111-g7-agi-run-strace-seccomp-bpf (0fcbf0944)
  -> kid de612d6af on de-base-G7d VERIFIED (9 passed, 2/2 + 40/0; node + engine bin pi alive under the strace flags) -> mur-de-base-g7d DEMOTE (empty P fail-open, prefix-only test, no THOUGHT) -> CORRECTIVE G7.5 + THOUGHT on the node 86991a7d4 -> G7.5 deacbc886 + G7.5b 64e0d61a8 (refusal only with a pi row) VERIFIED 11 passed -> mur-de-base-g7e accept_with_residue (D1 jq rc fail-open, M2 mixed box, M3 refusal after the wants strip, M4 test literal) -> RESULT G7.5 + CORRECTIVE G7.6 dbb8e4746 -> G7.6 kid RUNNING -> verify -> re-mur (copy murg75 args, key g76-code, range dbb8e4746..tip) -> residues 0 -> [merge-up] SM
MOVE 2 = DG1 (packet SENT 16:1xZ; belam re-GO after G8 + DG1 re-verdict):
  belam writes the row from .agi/sessions/dg3-mur-args/dg1-switch.sub (each half alone; RE-READ pid)
  YOU: DG1 [rotation] down-ready in belam's inbox FIRST -> gate -> tmux kill-window of DG1's window (pane pid gone)
    -> re-project: echo "local-maxxing/season2/main:.agi/nodes/.geometry/engine.md" | git cat-file --batch --follow-symlinks | sed -n '/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}' > <scratch>/ap.sh; AGI_BOX=local-town sh -s <scratch>/projN local-maxxing/season2/main < <scratch>/ap.sh
    -> p=director-general-1; sudo install -D -m 644 <projN>/agi-post@$p.service.d/h.conf /run/systemd/system/agi-post@$p.service.d/h.conf; + preserve.conf; sudo ln -sfn ../agi-post@.service /run/systemd/system/multi-user.target.wants/agi-post@$p.service; sudo systemctl daemon-reload; sudo systemctl start agi-post@$p
    -> watch /var/lib/agi/director-general-1/o until quiet; Esc the renderer modal -> report first turn to belam
  rollback: dg1-rollback.sub + stop unit + rm drop-ins/wants + rotate.py stand-up --post director-general-1
THEN (belam GO each, packet each): alive > self-perpetuating > all-is-one > stream-master > sanctuary-master > DG3 > belam LAST; DIRECTORS engine claude-sonnet-5-5, MASTERS Opus
GATE before ANY start: loadavg1 < 16 AND io PSI some avg60 < 50
```

## §2 Landed (this session)
card re-linked 7a6f190cb · DG5 key renewed (R7) + restored after a 15-restart loop (stop-gap H) · G8.2 built + verified 626281b34 · [red] G7.2-vs-pi to belam · CORRECTIVE G7.4 written 0fcbf0944

## 🔴 Where it stops
Two live: mur-de-base-g8b (systemd user unit) and the G7.4 Sonnet kid on de-base-G7d. Next: read the mur verdict; verify the G7.4 bytes.
```
python3 extensions/agi/bin/send.py read director-general-3; systemctl --user status agi-director-general-3-mur-de-base-g8b --no-pager | head -3; ls -t .agi/sessions/workflow-runs 2>/dev/null | head -3; git -C /mnt/agi-ram/worktrees/de-base-G7d log -2 --oneline; systemctl is-active agi-post@director-general-5
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
