---
id: doc:card-sanctuary-master
mint_id: 9a4a831c938a4501b30d37248ad319c0
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 3e856c7e9b80c2ab
season: 2
tags: []
title: Card sanctuary master
town: core
---
# doc:card-sanctuary-master

# doc:card-sanctuary-master — sanctuary-master's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; <= 100 lines; written DURING the work so a dead session is resumable.
## §0 State (19:57Z 11-10) -- gen 90 awake. Hub A. Trunk = posts/belam 2d8a6a92ab (L506). Next free L = 510. Next free GATE = 666.
- LANDED gen 89: L497 295e157d87 · L498 dc8ffa183b · L499 302669bf16 · L500 641d8dea53 · L501 e11807d128 · L502 8e1466cb69 · L503 778ddd3c4f (RULES, belam wrap 16c6934758) · L504 085845b280 (heal pair; alive verified 19:50Z).
- LANDED gen 90: L505 10a048c2ac (aio sweep pair 04e2c858f2) · L506 2d8a6a92ab (alive sweep, alive verified 20:10Z). IN FLIGHT: the chain cuts (window :31-:03) L507 DG1 example build node 71c48c9d7c -> L508 DGo1 CLOSE g4.18.2.2 211995b66f. All four gated GREEN and 3/3; cut dirs tmp/l505..l508 BUILT + guarded.
- CHAIN: `tmp/chain504.sh` (bg; DIES AT THE OUT; gen 90 relaunched 19:56Z, loop now 506 507 508). Relaunch at wake if not in ps: `cd /data/work/gate-sm && sh tmp/chain504.sh >> tmp/chain504.out 2>&1` (run_in_background). It loops 504..508; a cut whose cut.out ends 'sent belam' is DONE: before relaunch, edit the loop to start at the first unsent L (or it re-cuts a sent one).
- GATE662 GREEN 20:16:37Z (354/0, links 6093/0, nine lanes 0). L509 BUILT (tmp/gen90/mkcut.py) + guarded; tmp/l509/run.sh ARMED (bg): waits L508 on the trunk, then cuts. GATE663 running since 20:16:42Z (gateq90.sh).
- GATE663 TIP RE-POINTED to DG1's child d675091a90 (%G? G, +8 -2): alive APPROVE AS GATED (19:54Z) + one NIT (two-bracketed-choices alternation before the y), DG1's choice; pointer sent 19:56Z. DG1 19:5xZ: NO new tip, 663 gates d675091a90; the nit is a FLOOR until belam's run 4 prints grok's real trust screen. WORDS 3/3: alive APPROVE 19:54Z, sp APPROVE 19:55Z (the .grok find fails closed on an unread R), aio APPROVE 19:56:49Z (floor: a symlinked subdir's .grok passes; no risk, grok reads R's root) = 3/3. On 663 ALLDONE green: cut L509/L510 per order.
- GATE664 = DG1 CLOSE goal:g7.31.1.3 39df47e0b2 (nodes template, PLAIN), waiter tmp/gateq90b.sh (bg, DIES AT THE OUT) runs it after 'end gate663' in gateq90.out. Pointer sent 20:0xZ. WORDS: sp APPROVE 20:03:12Z (read), aio APPROVE 20:04:21Z (RAN F1-F3 green, red control + mutants), alive APPROVE 20:06:14Z = 3/3. On 664 ALLDONE green: cut.
- GATE665 = alive council-form CHILD 1 c333222d67 (parent 6e7010d1b9; sp + aio AMEND taken whole: 'or how it is' + the owner's honesty line), RE-POINTED 20:19Z before start; agi-review, PLAIN, skills template; waiter tmp/gateq90c.sh (bg) after 'end gate664'. WORDS on the child 2/2 + author: sp APPROVE 20:20:20Z, aio APPROVE 20:20:31Z (both read). On 665 ALLDONE green: cut.
- F1 (goal:g7.31.1.2): v2.1 run 3 (19:35Z) rc 1, nothing killed, caught grok's FOLDER-TRUST screen in R. belam CONFIRMED grok Opt OUT (default) pending the owner's one-word confirm. Ask of belam's next run: which file under 971's home grows when grok records the trust.
- OWNER 19:2xZ + 19:3xZ (relayed WHOLE): council on opus/high, belam fable/medium (DONE 958347ffa9 + re-pin); 'And yea' = design-stage exception (GATE662; belam to fold a confirm into its owner message); the SPIRIT below.
- HOW WE WORK (council [decision] alive 19:43:44Z, 3/3, the owner's spirit): one-line ANGLE per seat; one seat runs the heavy proof, two read + challenge, '== <angle>, nothing'; SM sends a one-line POINTER when the builder is cc'd and gates a chain once it settles; any post may ask another how it is, no tip needed. alive cuts one agi-review line after L506.
| | |
|---|---|
| post | master-gate + BOARD COORDINATOR (placement, gates = me · word = the council · belam = owner items + host acts + RULES wraps) |
| land step | pre-read (%G? == G, merge-tree clean) -> gate the MERGED tree -> words -> cut (byte-identical to the gated tree) -> RULES = belam wraps -> [landed] to builder + council |
| RULES list | .agi/config.json land.rules_paths: .geometry/, guard/, config.json, schemas/, .github/, .gitattributes, skills/agi-master-gate, owner-ruling-*.md, CLAUDE.md/AGENTS.md/QUICKSTART.md |
| scripts | /data/work/gate-sm: gateNNN.sh (templates: nodes 649, skills 645, whole suite 639), tmp/lNNN cut dirs, tmp/gen88/mkcut.py, tmp/gen86/guard.py |
| send | ONLY `cd ~/t && sh /data/work/gate-sm/gsend.sh FILE post...`; it refuses home-path literals (write [SLASH] or a role name) |
| box | `AGI_POST=sanctuary-master box read > /data/work/gate-sm/tmp/boxread-now.txt` at every mail wake, read it whole |
| skills | agi-master-gate, agi-send, agi-node-write, agi-goal, agi-verify, agi-post, agi-rotate, agi-review, agi-memory-guard, agi-research-then-design |
## §1 Plan
```
1. Wake: box read; ps for chain504 + gate waiters; relaunch what died (see §0).
2. L505 [landed] -> pointer to aio + council; chain cuts L506..L508; each [landed] -> pointer.
3. GATE662 green -> L509. DG1's F1 v2.2 child -> re-point GATE663 -> words (one runs, two read) -> gate -> cut.
```
## 🔴 Where it stops
gen 90: L505 + L506 LANDED (trunk 2d8a6a92ab, belam card 05d209c750); belam restarting ~20:15Z, NO mail to belam before 20:20Z; L507 cuts at :31; chain504 (506..508) + gateq90 (662, 663) + gateq90b (664) + gateq90c (665) are bg jobs.
```
NEXT: each L506..L508 [landed] -> pointer; on 662 ALLDONE -> L509; on 663 ALLDONE -> words (one runs, two read) -> cut.
CHECK: ps -eo args | grep -E '^sh (gate|tmp/)'; tail -3 /data/work/gate-sm/tmp/chain504.out /data/work/gate-sm/tmp/gateq90.out
```
## §2 Landed gen 89: L497-L504 (see §0). Gates green: 649-661 (657 the WHOLE suite 9835/0). L501 first cut 4db836bbd8 VOID (crossed belam's card).
## §4 Traps (gen 89; at the next rotation each moves to skills/agi-master-gate, RULES, belam wraps, or drops)
- A tip that ADDS a skills/agi-* dir needs config:rotations' two skills rows + a measured byte_cap in the SAME chain (GATE654 red): run test_skills_first_turn_entry at its gate.
- A RULES cut: mkcut writes 'plain'; edit cut.sh's RULES-hits line and the head's 'NOT a RULES land' line by hand (L503's way).
- Gate-script build by replace: assert on lines, not on '649' in the whole text (a tip hash can hold it).
- A red the tip cannot reach (load-timing): re-run the failing files ALONE on pre and merged, record r<N>/summary.rerun, ask the council to ACCEPT, add L490's named-reds block to cut.sh (L497).
- Background end events reach me only at my next turn: green gates sat 16:44Z-19:34Z. Nothing inside the session wakes it (box send to self rc 1).
## §5 Verification: every landing = the gated tree at cut (byte-identical on every changed path) + 0 D + anon 0 + email-class [] + capsule 67/0 + store check 0; belam's verify-land + links; alive's land read.
## §6 BANKED
- LEAF (alive 19:50Z): a post's long job (a gate's ALLDONE) wakes the post, not only mail; general form; mint at a quiet window. alive 20:00Z: on this box heal cannot be the waker (no heal watch runs), the leaf says so or brings a waker up.
- FALSE LINE (alive 20:00Z): crons.md declares the agi-reaper service; it is not live on this box. crons.md or the box row says so. Not tonight.
- TRAP SWEEP OWED for skills/agi-master-gate (RULES, ALONE, belam wraps): gen 85-89 §4 lines.
- sp NIT (gate template): the pytest lane re-reads load5 in the SAME command and holds above 8 (L490 + L497 named-reds were load).
- OWNER BATCH via belam: the actor_rows CREATE grant (L463's R2) + the 2c 'resume_failed' row cell.
- posts/thought-master and posts/director-thought-1: never push. CONSOLE $200 (owner 11-06): non-Claude-Code harnesses only.
## §7 ATOMS (inbound asks, one row each; closed when placed; open > 1 lap = red)
| atom | from | in | placed | closed |
|---|---|---|---|---|
| OWNER: grok-bot GO + plan-master | belam [owner] 04:00Z 11-10 | 04:00Z | F1 L493/L496/L500/L502 landed; v2.2 in review | open: v2.2 child + gate; belam run 4; DG1 plan-master leaf after |
| OWNER: research-then-design as a graph skill (c:e780e4c65887) | meme-master 09:41Z | 09:41Z | L498 leaf, L503 skill (RULES) | open: L507 node + L508 CLOSE (chain); design exception GATE662 |
| OWNER c:1ae05e71c801: v1.1-with-videos rclone to gdrive subfolder | meme-master 20:0xZ | 20:05Z | relayed WHOLE to belam 20:05Z (host act) | CLOSED: belam [done] 20:1xZ, 20/20 sha + rclone check 0 diff |
| OWNER: deck full pass + A/B | meme-master 09:5xZ | 09:46Z | leaf L497, copy L499 | open: running director unnamed (thought-master asked 09:54Z); sp both-markers term held for it |
| OWNER 19:2xZ: models / opt-in / design YES / spirit | belam [owner] 19:3xZ | 19:34Z | relayed; council [decision] 19:43Z; models DONE | open: owner one-word confirm (opt-in + design YES); levels-line readings to the owner via belam |
| CHECK T2 (trajectory) | belam [ask] 08:4xZ 11-09 | 08:44Z | most landed | open: DG2 .46.19; .42.2 runner; .44.7 capsule-xfer |
| objscan ip-class mask on anonymize.ip_allow paths | DG2 [note] 19:4xZ 11-09 | 19:48Z | mine | open: quiet window |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's | open: DG3's mint |
| OWNER 2 PLUGIN | belam [owner] 20:47:15Z 11-08 | 20:47Z | goal:g1.23.2 HORIZON | open: design doc placement |
