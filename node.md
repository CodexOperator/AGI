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

## §0 State (04:5xZ 10-01, new session) — f~0.09 · LANES (owner via belam 02:27Z): DG3 = Opus 5.5 subagents at effort MEDIUM for EVERYTHING, up to 3 live; murs pi-free · no STOP
| | |
|---|---|
| post | director-general-3 · graph-builder · the .11 BUILDER (Opus subagents) |
| skills | agi-node-write · agi-goal · agi-verify · agi-send · agi-rotate · agi-corrective · agi-master-gate · agi-post · agi-workflow · agi-dispatch · agi-memory-guard |
| SM board rule | [merge-up] to SM, WAIT for SM's GO; SM gates + LANDS. BUILD stages report ONE [decision] line to belam each |
| inbox | send.py read is the source; the dm FILES (comms/season-2/dm/*director-general-3*) can hold [board] lines the read missed -- tail them at wake |

## §1 Plan
```
BUILD goal:g7.16.1.11 (radically simple engine; config:engine)
  S1   PASS (02:0xZ) reported · S2 PASS 7/7 (doc:g716111-stage2-rootplan 92cd0739be) ACCEPTED by belam 03:48Z, box re-verified clean
  S2.5 GO (belam 03:48Z): director-general-5 on the LIVE repo under engine v4; bar = parity matched-or-better (55 rows incl. guards + magic pane anchor)
       PHASE A done: doc:g716111-stage25-rootplan 29044ff734 (v4 16,375 B; 51/55 parity; 17 root acts + 4 MAIN commits; N4 HARD GATE)
       council [red] §N.5 folded: Slice=agi.slice + a system agi.slice capped FROM config:guard; N4 proved BEFORE DG5 starts; council pane (no dtach)
       HARNESS CHANGE (owner 04:40Z): DG5 = Claude Code Sonnet 5.5 + REMOTE CONTROL ON, own user, copied CC creds (claudeAiOauth, 600), in agi.slice;
         ONE kid on pi-free + CCCC; NEVER pi posing as CC to RC; report app-visible y/n + the creds' uid/network binding
       PHASE A' first run LOST at the 04:45Z rotation (only build/assemble.py touched) -> RELAUNCHED 04:5xZ (Opus, no root) into /tmp/agi-stage25/v4c/ (v4b untouched) -> mint doc:g716111-stage25-rootplan update -> [decision] to belam -> PHASE C ON belam's WORD
       OPEN with belam (04:3xZ, acked 04:4xZ): shared-refresh-token RISK of copied creds · slice overcommit · memguard patch R-MG · key broker = stage 3 ·
         WHO STOPS the OLD-engine director-general-5 scope still running (plan holds while it lives) · C1/C2 = Prime landings
  STOP before stage 3 (migration, retiring Python): the owner's word through belam
HELD   key / identity / signing / rotate / spawn-row / write-gate rounds + goal:g7.16.1.7 (the build replaces them)
LIVE ROUNDS (each -> pi-free re-mur -> residues 0 -> [merge-up] to SM)
  .10.7   goal:g7.16.1.10.7 merge gate: LANDED 9158583d26 by SM 03:56Z under OPTION A (suite 7733 / 5 known reds, none in range; links 5587/0); inert until the Prime's cells; activation waits on crmur
          leaf goal:g7.16.1.10.7.1 (horizon) carries the skill retirement; the merge_gate cells wait for crmur; SM carries the grep-wins [rule]
  row60   hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit: de-base-DG3.69 tip b9576d2d43 (218p/8s; prod +52/58; test 260/260)
          -> mur h60d accept_with_residue (verify agrees); 3 prose residues closed by the director -> tip 855daaccd; [merge-up] SENT to SM 04:5xZ (merge-tree rc 0 vs d43321e06b) -> WAIT for SM's GO
  g7556f  hypothesis:g7556-fstype-root-mount-and-ram-tier-through-ramw: de-base-DG3.70 tip d73bf50bf6 (137p/8s; tests +37/40)
          -> mur h7556g: review ACCEPT, verify timed out 3600 s, note demoted; merged-tree 99p/8s -> [merge-up] SENT to SM 05:1xZ -> WAIT for SM's GO
  crmur   hypothesis:council-report-reads-the-mur-args-shape-per-round: de-base-DG3.71 tip 2634a61987 (483p/8s/1x; +22/+40; lean 85:
          the FLAT shape without tips still writes ?..?) -> mur hcr: review accept_with_residue (gap INSIDE the claim), verify FAILED rc 2 ->
          CORRECTIVE DG3.71b DONE (Opus): tip 0de7f23ab -> mur hcrb: verify ACCEPT, residues 0; merged-tree 295p/8s (incl. merge_gate) -> [merge-up] SENT to SM 05:1xZ (delivered) -> WAIT for GO; GATES the merge_gate cells
QUEUE  (SM order) done/in-flight: row 60 -> g7556 fork -> council-report fork -> .10.7
FINDINGS goal:g7.33.19 rows 38-68 (65 blind harvest x5 · 66 grace literal · 67 four no-grep carriers · 68 heal.py dead counter)
PRIVACY the scrub commit-map is local-only: NEVER track, print or copy an old sha / old->new pair
```

## §2 Landed
this session (trunk): card re-link 823060f68e · goal:g7.16.1.10.7.1 minted 61dd3a0d68 · findings rows 65-68 · docs g716111-stage2-rootplan / stage25-parity / stage25-rootplan
this session (loop branches, sent/under review): .10.7 chain -> 27042fc3cf · row 60 -> b9576d2d43 · g7556 fork -> d73bf50bf6 · crmur -> 2634a61987
earlier: .10.5 2ed4492434 · g7556 627c94a040 · .10.3 521ebaa951 · goal:g1.31.3.2.1 e585436f87 (previous card versions: grid)

## 🔴 Where it stops
No murs running. Three [merge-up]s wait on SM's GO (row60 855daaccd · g7556 d73bf50bf6 · crmur 0de7f23ab); Opus Phase A' (v4c) running; Phase C waits on belam's word. First commands on wake:
```
python3 extensions/agi/bin/send.py read director-general-3; tail -5 .agi/comms/season-2/dm/director-general-3--sanctuary-master.md; for u in h60d h7556g hcr; do echo $u $(systemctl --user is-active agi-director-general-3-mur-$u); done; ls /tmp/agi-stage25/v4b/ 2>/dev/null
```
then per finished mur: read .agi/sessions/workflows/runs/mur-de-base-dg3-{69,70-*,71}/{review,verify}_*.json (masked) -> residues 0 = [merge-up] to SM (tip, merge-base, merge-tree vs trunk rc, numbers, mur keys) else an Opus corrective on the same de-base branch + re-mur.

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

## §5 Verification (20:5xZ): .10.3 tip ebff97679f 269p/8s (reds + manifest + help) · .10.5 tip 9a861b4fd3 476p/8s/1x (council + write + manifest + help) · g7556 tip 132p/8s · links 5533 resolved 0 broken

## §6 BANKED
- 86 (SM): report_integrity + warn_premature_complete (goal:s26) have NO caller since cmd_render left. (a) re-wire into verification quick as `goals-integrity` (recommended) · (b) retire both.
- R1 slice (owner / council): a dedicated uncapped posts slice, then flip `spawn.post_scope.live` after PASS B3 with the owner present.
- goal:g4.18.4 Falsifier 2 scans all history: scope it to recent commits, then complete it.
- config_max proposals routed via SM: paths.core.workflow_runs_root · merge_gate.red_classes · council.residue_leaves · anonymize.email_allow (RFC 2606 + non-numeric systemd local part).

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.


ROTATION NOTE: Agent-tool subagents die with this session -- rotate only once Phase A' (v4c) + DG3.71b have returned (or name them lost in the stops line).
