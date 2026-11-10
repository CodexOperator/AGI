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
## §0 State (19:52Z 11-10) -- gen 89 OUT at the line (472344/1000000). Hub A. Trunk = posts/belam 085845b280 (L504). Next free L = 509. Next free GATE = 664.
- LANDED gen 89: L497 295e157d87 · L498 dc8ffa183b · L499 302669bf16 · L500 641d8dea53 · L501 e11807d128 · L502 8e1466cb69 · L503 778ddd3c4f (RULES, belam wrap 16c6934758) · L504 085845b280 (heal pair; alive verified 19:50Z).
- IN FLIGHT: L505 10a048c2ac (aio sweep pair 04e2c858f2) SENT 19:47:19Z, awaiting belam's land. Then the chain cuts L506 alive sweep 56a8e4d8fe -> L507 DG1 example build node 71c48c9d7c -> L508 DGo1 CLOSE g4.18.2.2 211995b66f. All four gated GREEN and 3/3; cut dirs tmp/l505..l508 BUILT + guarded.
- CHAIN: `tmp/chain504.sh` (bg; DIES AT THE OUT). Relaunch at wake if not in ps: `cd /data/work/gate-sm && sh tmp/chain504.sh >> tmp/chain504.out 2>&1` (run_in_background). It loops 504..508; a cut whose cut.out ends 'sent belam' is DONE: before relaunch, edit the loop to start at the first unsent L (or it re-cuts a sent one).
- GATE662 (DG1 design-stage fable exception 84c0cb6f73, brief :76 + skill s1, PLAIN) RUNNING, 3/3 (sp 19:39:45Z, aio 19:42:00Z, alive 19:43:44Z); pytest 354/0 at 19:47Z. On ALLDONE: build L509 (mkcut entry n=509 g=662 prev=508). DG1 fixes the brief's LANES 'every post uses Sonnet' line at the next touch (agreed, no child).
- GATE663 (F1 v2.2 0a3a3e01ee) BUILT, waiter queued after 662: AMEND 3/3 (alive 19:50:27Z, aio 19:50:49Z, sp 19:51:30Z): ONE DG1 child owed (no y while any opt-in word is on the capture + both-screens mutant; FAIL if R holds a .grok path). RE-POINT gate663.sh TIP to the child BEFORE it starts (sed both the 40-hex and the 10-hex), or kill its waiter.
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
gen 89 -> 90: L505 sent, unlanded; chain504 + GATE662 + GATE663 waiter running as bg jobs that DIE AT THE OUT. GATE663 waits on DG1's child.
```
FIRST: box read whole; ps -eo args | grep -E '^sh (gate|tmp/)'; tail -3 /data/work/gate-sm/tmp/chain504.out; tail -3 /data/work/gate-sm/tmp/gateq89.out
THEN: relaunch the chain from the first L whose cut.out lacks 'sent belam'; relaunch GATE662 if r662/summary lacks ALLDONE (sh gate662.sh); GATE663 only after its TIP is re-pointed to DG1's child.
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
- LEAF (alive 19:50Z): a post's long job (a gate's ALLDONE) wakes the post, not only mail; general form; mint at a quiet window.
- TRAP SWEEP OWED for skills/agi-master-gate (RULES, ALONE, belam wraps): gen 85-89 §4 lines.
- sp NIT (gate template): the pytest lane re-reads load5 in the SAME command and holds above 8 (L490 + L497 named-reds were load).
- OWNER BATCH via belam: the actor_rows CREATE grant (L463's R2) + the 2c 'resume_failed' row cell.
- posts/thought-master and posts/director-thought-1: never push. CONSOLE $200 (owner 11-06): non-Claude-Code harnesses only.
## §7 ATOMS (inbound asks, one row each; closed when placed; open > 1 lap = red)
| atom | from | in | placed | closed |
|---|---|---|---|---|
| OWNER: grok-bot GO + plan-master | belam [owner] 04:00Z 11-10 | 04:00Z | F1 L493/L496/L500/L502 landed; v2.2 in review | open: v2.2 child + gate; belam run 4; DG1 plan-master leaf after |
| OWNER: research-then-design as a graph skill (c:e780e4c65887) | meme-master 09:41Z | 09:41Z | L498 leaf, L503 skill (RULES) | open: L507 node + L508 CLOSE (chain); design exception GATE662 |
| OWNER: deck full pass + A/B | meme-master 09:5xZ | 09:46Z | leaf L497, copy L499 | open: running director unnamed (thought-master asked 09:54Z); sp both-markers term held for it |
| OWNER 19:2xZ: models / opt-in / design YES / spirit | belam [owner] 19:3xZ | 19:34Z | relayed; council [decision] 19:43Z; models DONE | open: owner one-word confirm (opt-in + design YES); levels-line readings to the owner via belam |
| CHECK T2 (trajectory) | belam [ask] 08:4xZ 11-09 | 08:44Z | most landed | open: DG2 .46.19; .42.2 runner; .44.7 capsule-xfer |
| objscan ip-class mask on anonymize.ip_allow paths | DG2 [note] 19:4xZ 11-09 | 19:48Z | mine | open: quiet window |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's | open: DG3's mint |
| OWNER 2 PLUGIN | belam [owner] 20:47:15Z 11-08 | 20:47Z | goal:g1.23.2 HORIZON | open: design doc placement |
