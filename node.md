---
id: doc:card-director-science-1
mint_id: d55057fc5ba24e7ab2bb66cbf9d326bf
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-science-1
scaffold_hash: b3449e9971f09f91
season: 2
tags: []
title: Card director science 1
town: core
---
# doc:card-director-science-1

# doc:card-director-science-1 —# doc:card-director-science-1 — director-science-1's card (was director-general-2; council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines. Skills: agi-send · agi-goal · agi-verify · agi-rotate · agi-memory-guard · agi-master-gate. Template: doc:unified-director-brief + role doc:role-director-science.
My lane: FALSIFIER lanes first (test-only + a sha), RED on the build's parent, GREEN on a scratch reference, one-edit mutants + named stays-greens; SM gates. Since 10-11 SM also hands me whole leaves (lane + build).

## §0 State (10-24, gen 27: .44.x leaves closed/banked; wave-1 leaves .46.6-.46.8 LANDED as L82 and CLOSE sent)
| Field | Value |
|---|---|
| Owner rule | quiet: mail ONLY SM (directors); ONE message per finished thing, no acks. STANDING CLOSE FORM: "CLOSE <leaf> = <sha> + falsifiers RE-RUN at <trunk sha>: <counts>". Owner 10-22 05:0xZ: close the CURRENTLY active season leaves, report, IDLE; no new starts |
| Board | trunk = core/season3/main. A plain commit in ~/t is refused: agi-at <path>; agi-sync merges the trunk each turn; ~/t is a detached view (`git reset -q --hard posts/director-science-1` after a sync; never `git merge` in ~/t: it strands a commit). Extra worktrees: /data/work/gate-director-science-1/wt-* (6 registered, all locked; wt-sci1 = 9c39718b17; wt-sci1.dead = removable) |
| DONE | pidchk fails closed + st2-cond3-a dsig = L59 237923cbb2 (9c39718b17), CLOSE sent, re-run at c35aff54a5: agi-town-start 96/0 · host-act 114/0 · agi-town 63 ok + the 7 ref-guard FAILs under my uid (SM: 70/0 under its uid). G6 gate-dir repair done (6 new / 0 old / 0 prunable). .44.7 Agent Notes line landed 2ec269cd00 |
| .44.7 | ACTIVE: built + lane-proven; live half = the first real box move between two boxes, PAIRED with .44.8's fresh-box leg (council 3/3 10-22). SM places no move to close a leaf. Before any box-move.sh touch: blob 00e4e20ea9 (capsule-xfer.* KNOWN LEAK) |
| .44.8 | NOT mine (council); stays ACTIVE on the owner's legs (nspawn GO + next fresh box); its last build (stop -> start round-trip row) is placed on director-goals-1. Do NOT set its status |
| .44.8.1 | HELD, not started: 8acb585a24 on my branch only (not on the trunk). Council 3/3 09:0xZ: out of this season's set, banked BY NAME in the owner's report; first item when .44.8 resumes or the owner's pick. Two items: pidchk refuses ZERO-row posts.md (mutant: re-indented posts.md); dsig adds stat %n %a %u %g |

## §1 Plan — goal:g7.16.1.11.46 WAVE 1: my leaves .46.6 C1 · .46.7 C2 · .46.8 C3 are LANDED (L82 eabbd58744 = tip 039c45eda6, SM [landed] 10-24 01:15Z)
History: [merge-up] c2e7217f06 -> council RETURN (agi-infer read a DEFAULT credential file and replaced the caller's infer_key; 4ac9112d8d + amendment c9a1c2f38f) -> fixed tip 039c45eda6 (AGI_INFER_CRED read ONLY when set) -> GO 3/3 -> L82. CLOSE sent 10-24 (falsifiers RE-RUN at eabbd58744: secrets-lanes 11/0 · agi-cred 28/0 (I had said 30: corrected) + 7 mutants RED · lane-header 25/0 · k3-infer 38/0 (agi-infer 1332 B <= 1350) · engine-sizes 26/0).
STATUS of all three = "passed except banked": Doppler service token (owner) · ROOT INSTALL of agi-cred/.service/.timer (belam; reading the pieces) · real wrkspc ids / option B (owner) · live leg · agi-lane NOT wired into agi-kid (DG3's kid-launch land). No goal status set by me. Worktree /data/work/gate-director-science-1/wt-w1 (LOCKED, tip 039c45eda6) is removable once belam's install is done.
Notes for the leaf bodies (council): the 5-min agi-cred check exits non-zero with no live agi-post@ (a town stop reads failed; never page on it during a stop). K7: kids at most 2 live, never while agi.slice > 5.0 GB (none used). .44.8.1 stays HELD (banked by name).

## §1b DONE 10-24: belam's [red] on agi-cred fixed and INSTALLED
Final tip 9af9a74343 = L87 e801e96a92 (SM [landed] 02:31Z); belam INSTALLED agi-cred + .service + .timer (5 min) from L87 at 02:31:54Z (credits_live false, /etc/credstore empty); first run `posts 10 pids 190 read 190 gone 0 key-hits 0`. CLOSE sent (falsifiers re-run at e801e96a92: agi-cred 40/0 · secrets-lanes 11/0 · lane-header 25/0 · k3-infer 38/0 · engine-sizes 26/0). Tip chain was fa1427f9a7 -> dc0bb605c6 -> 9af9a74343 (each superseded). Worktree /data/work/gate-director-science-1/wt-w1 (LOCKED) is removable: `git -C /data/work/agi worktree unlock` + `remove`, only on SM's or belam's word.
LESSONS: model "unreadable" as an EXISTING pid with a dangling environ AND as an environ that is a DIRECTORY (-r true, read fails: the one that hides a silent green); simulate a race with a shim (tr removes the proc dir when its stdin is that environ), never a timing; when the trunk moves under a worktree, re-apply ONLY your own paths' diff (git diff BASE -- paths, git apply --3way on the new trunk), never `reset --soft` onto it; count rows by running the test before writing a number.

## 🔴 Where it stops + the exact next command
V2 (.46.20) 10-26: LANDED PARTIAL as L157 4b54379a73 (re-cut 292fe310e2; credpiece.py + cred-piece.t.sh 21 ok + manifest entry; council 3/3 GO). Measured: refresh rewrites ~/.claude/.credentials.json in place and ROTATES the refresh token => one login = one home, a capsule seed is one-shot; re-seed = rm file + fresh /login + re-seal (all in the leaf). OPEN: Falsifier 1 (fresh-home login after the root placement) waits for the OWNER's GO (SM banks in card-belam §6); do not place anything before it. ROW for the next touch of credpiece.py: each [cred] PROBLEM line also carries 'in <abs path>' (self-perpetuating). Never test a refresh in a copied home. Cold start: box read; act only on what arrives. | 10-26 18:xxZ SM relay (alive 18:09:38Z): lane-header.t.sh trunk red is MINE (plain, tests only): SENT [merge-up] ba46831210 on posts/belam 463ef803aa (any-value sed, fail-closed exit 99, v-c own cell, LH_STOP + decoy-root rows g-a..g-d, 2 mutants); lane 0 FAIL 3m23s. Quote no workspace id in mail. If returned: fix in wt-w1 on the live posts/belam, ONE commit. | 18:5xZ: SECOND plain commit 5d9e7ce507 on ba46831210 = secrets-lanes.t.sh (mut() 0-bytes guard exit 99, base normalized, h-a..h-d, 16 ok/0 FAIL) SENT for GATE309 (stack ba46831210 + it + alive 27c927d971). Offered (not cut): rep() NO EDIT -> exit 99 in lane-header + agi-cred. Do not self-test by running a copy of a lane without an INNER guard (recursion: a copy re-runs its own copy rows). Never pgrep -f in a shell whose own command line matches (kills the shell).
10-27: leaf goal:g7.16.1.11.13.6 LANDED L230 71d806080e; CLOSE sent + close commit 53de4127bd (status complete) as [merge-up]. Nothing else open but V2 (owner GO).
10-28: leaf goal:g7.16.1.11.38.2 CLOSED (L274 + close L284 c61152bf56). Crumbs for agi-strand next touch: M5 row + 2>&1 note. SENT [merge-up] 9d3634cc19 on posts/belam 2ce5624054 (wt-w1). agi-strand 30/0; PIECES=trunk -> 2 FAIL. Next: gate; at land re-run agi-strand + engine-sizes, CLOSE .38.2. Approvals: aio 18:59:23Z, sp 19:01:46Z (L274 RULES alone). NEXT-TOUCH ROW (sp crumb): git shim rev-list exits 0 with NO output -> want rc 2 + "rev-list said" (mutant M5 = case line cut, then RED). BOX LOAD RULE (alive 19:39:12Z): while /proc/loadavg field 2 > 8, send tips with my own lanes only, no links.py/pytest-wide/19 scanners (gate: heavy: GATE<N>), print the load read.
10-31: .46.6 CLOSED (L309 b7500aaf49) · .46.8 CLOSED (L310 76e6099896, F2 banked: no lane unit, V5 uncut). Held: .46.7 (owner: one shared workspace intended?), .46.20 (owner GO), .44.8.1 (waits .44.8).
11-05 JOB 3 (SM placement 08:5xZ; idea:an-evidenced-disproof-scores-as-a-proof, L350): MEASURE sent as [finding]: the 63:6 demotions are all season-1 writes (evidence gate, evidence_runs=0); counters symmetric EXCEPT the primary outcome_coverage = mvps/hyps (proof-only hyps reach an mvp 6.4%, disproof-only 1.4%). Next: wait for the council's leaf placement; then ONE tip (idea node finding + leaf) to SM's gate. Break files: ~/free/INDEX.md.
11-09: (1) .46.20 V2: root act PASS 12:27:42Z (belam; 1st run 12:19Z rolled back: StandardOutput=null hid the journal line). F1 PASS 12:3xZ (claude -p with ANTHROPIC_AUTH_TOKEN/BASE_URL/API_KEY UNSET; tokens unchanged vs aside). CLOSE RE-CUT on alive's TERM = [merge-up] 7a8eb7c7d7 on 51a8273735 (wt-close; RE-CUT 2, replaces 28875c28aa + abfb93cda2; F1 MUTANT RED (rc 1 "Not logged in"); 3/3 APPROVE AS GATED 12:47Z (28875c28aa + abfb93cda2 VOID); NEXT TOUCH: THOUGHT names the mutant + alive add (post uid, EXIT trap, rc + one line, scratch checked gone); line 38 clauses (a)/(b) OPEN -> V1 .46.19, (c) MET; atom 2.25 OPEN), GATE627; F2 29/0, F3 0. NEXT: gate -> land -> CLOSE line. TRAP: a plain claude -p in this env answers via ANTHROPIC_AUTH_TOKEN and proves nothing. Crumbs for the next touch are in the node THOUGHT. (2) .46.7 CLOSED: L468 d2c3e96f5a LANDED 11:53:55Z (3/3, F1 re-run 16/0). DONE. JOB 3 (.idea evidenced-disproof): measure sent 11-05, waits for the council's leaf.

## §4 Traps (this generation only)
- A worktree added UNLOCKED can be pruned by anyone's `git worktree prune`: add with `--lock --reason`, copy edits to scratch before moving a dir.
- agi-town.t.sh under MY uid: 7 FAILs (st-acks, F1, R2 x2, R3, R6 x2) = ref-guard on refs/box/belam/*, identical on a pristine export; SM reads that lane under its uid.
- A scratch export for the lanes needs `skills/` too (st2-skill-names reads skills/agi-town/SKILL.md), plus extensions, .agi/nodes/.geometry, .agi/config.json.
- A scripted edit of a test line: never `rstrip("'")` a quoted shell line; `sh -n` the file and read the tail row after.
- `box read | head -N` drops the tail of a long mail for good (peek is empty after): read with no head.

## §6 BANKED
Nothing needs the owner beyond what SM's report carries (.44.7 live half, .44.8 legs, .44.8.1).
