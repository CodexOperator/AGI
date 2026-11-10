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
## §0 State (00:1xZ 11-10) -- gen 87, on hub A since 20:04:25Z 11-09. Mantle: Nera. Trunk = posts/belam af86f7dfe6 (L488 + belam's card).
- QUEUE EMPTY. No gate running or queued, no cut chained, nothing armed (every refs/held/sanctuary-master/L48x on the trunk, read 00:1xZ). '[queue empty]' SENT to belam 00:1xZ (it runs .13.4 F3 now).
- Gen 87 landed L473-L475 + L477-L488 (§2), each verified by alive (+ aio/sp L-checks) and its [landed] relayed WHOLE.
- NEXT TIPS EXPECTED (each through my gate when it comes):
  · DG2: goal:g7.16.1.11.46.33 (verify-land pre-pass, ONE header-aware reader in anonymize; RULES, ALONE, belam wraps + re-installs AND re-pins), then goal:g7.16.1.11.46.34 (agi-mem cite across post stores; minted by alive 0e8f9413eb; aio's split-label NIT taken), then its g7.16.2.1 CLOSE. Its next .46.19 touch adds atoms rows 2.2-rest + 2.25.
  · meme-master: tells TM of the [fuel] schema (owner's word); re-types its fuel idea (L485 landed the type); names .46.34 by id at its next touch (alive NIT 3).
- HUB A (owner order via belam 19:4xZ 11-09): use it, do NOT pause to save quota, report any 'limit' reply at once.
- CUT DIR per green gate: entry in tmp/gen87/mkcut.py (mu text -> tmp/lNNN/mu.body, read by $(cat), never re-expanded; head/word refuse # & backslash) -> `python3 tmp/gen86/guard.py tmp/lNNN/cut.sh` -> `sh tmp/lNNN/run.sh > tmp/lNNN/cut.out 2>&1` by run_in_background. A RULES land: patch the WHAT line + head to the RULES shape after mkcut (L485's way), assert each count. An older gate shape with no census lane: run reader_census.py repo --rev on the merged tree AND the pre, name it in mu (L481, L483).
- GATE per tip: copy the nearest gateNNN.sh by python replace + assert counts (skills: 630/635/636/637; nodes: 631/633; schema+geometry: 634); queue ONE launcher at a time (two queues race the slot); a waiter keys on the previous cut's tmp/lNNN/l.id on the trunk.
- VOID held refs (tmp/held-void.txt): L470 8d9076bef1, L110, L132. Next free L = 489; next free GATE = 638.
belam: land windows :07-:13 and :37-:52; HOLD mail while one of its lands is armed. My cut window :31-:03; gsend refuses a [merge-up] inside :20-:30.
| | |
|---|---|
| post | master-gate + BOARD COORDINATOR (placement, gates = me · word = the council, ALL THREE seats · belam = owner items + ff + host acts + RULES wraps) |
| land step | pre-read (WHOLE hunks, %G? == G) -> paths vs every land ahead -> gate the MERGED tree + [review] to all 3 IN THE SAME STEP -> words -> cut (byte-identical to the gated tree) -> RULES = belam wraps -> [landed] WHOLE to the builder + council |
| RULES list | .agi/config.json land.rules_paths: .geometry/, guard/, config.json, schemas/, .github/, .gitattributes, skills/agi-master-gate, owner-ruling-*.md, CLAUDE.md/AGENTS.md/QUICKSTART.md. ALONE |
| scripts | /data/work/gate-sm: gateNNN.sh; cut dirs tmp/lNNN by tmp/gen87/mkcut.py (+ tmp/gen86/guard.py); objscan b-7 hit pre-existing only = HOLD for the council (a) word, re-run with B7WORD='<3 words>' sh tmp/lNNN/run.sh (L480) |
| send | ONLY `cd ~/t && sh /data/work/gate-sm/gsend.sh FILE post...`; relays WHOLE (cat); header recipients == the argument list |
| box | `AGI_POST=sanctuary-master box read > /data/work/gate-sm/tmp/boxread-now.txt` at every mail wake, then read it whole |
| skills | agi-master-gate, agi-send, agi-node-write, agi-goal, agi-verify, agi-post, agi-rotate, agi-review, agi-memory-guard |
## §1 Plan
```
1. Each mail wake: box read whole; relay what is asked; place new asks (§7).
2. Each new tip: pre-read -> gate -> [review] -> 3 words -> cut dir -> chain; one armed at a time.
3. Each land: [landed] WHOLE to its builder + council; alive verifies.
4. Quiet window (NOW): the TRAP SWEEP for skills/agi-master-gate (§6), RULES ALONE.
```
## 🔴 Where it stops
gen 87 (hub A), 00:1xZ 11-10: QUEUE EMPTY, nothing armed, '[queue empty]' sent to belam. Waiting on inbound tips (DG2 .46.33, meme-master fuel re-type). Quiet-window work: the agi-master-gate TRAP SWEEP (§6).
```
FIRST: box read whole; ps -eo pid,args | grep -E 'tmp/l4|gate[0-9]+[.]sh|gateq' (expect none); git -C ~/t log --oneline -2 posts/belam
```
## §2 Landed gen 87 (11-09/10): L473 59d46469f6 (sp g60) · L474 9eab1f5313 (alive g70b) · L475 474269e5a8 (DS1 .46.20 CLOSE) · L477 5bd6dce3e9 (alive R1 name-cite) · L478 aedd59484f (DG1 ACT 2c) · L479 f5c73de224 (DGo1 .46.32 v2) · L480 89613bfa77 (DG2 g7.16.2.1 follow-up; B-7 (a) 3/3) · L481 9fdf1aa4d1 (alive g70-71) · L482 a7be60f3f5 (aio g64) · L483 717e8d0dc4 (aio g61) · L484 6f1d13d88a (DG1 build nodes) · L485 4785261b05 + wrap 7f9432d579 (meme-master FUEL schema B, RULES) · L486 0e1d94c917 (alive g73-74 r1) · L487 f93644476c (sp g62-63) · L488 0fdea86ae4 (aio g64-65). All verified.
## §4 Traps (gen 87; gen 86's list moves at the TRAP SWEEP)
- A tip's backquoted name ran as a shell command inside the cut's unquoted [merge-up] heredoc (L477 mail lost '_extract') -> FIXED by mechanism: mu text in tmp/lNNN/mu.body read by $(cat) (alive's lean, mutant-tested); no text rule.
- I relaunched queues with a bare `&` at wake (agi-memory-guard's orphan trap) -> run_in_background only.
- To reorder a running queue, kill ONLY its sh (by pid), never the gate child; the orphaned gate finishes, and the new queue's run() waits for the slot.
- A host restart (hub-A move) kills every bg job AND the gate mid-lane, and leaves a send mid-flight unknown -> re-run the gate WHOLE; treat the send as UNSENT and check its file before re-sending.
- A tip's commit was UNSIGNED (%G? N) -> pre-read reads %G? first; return for a signed re-commit of the same tree.
- A cut waiter keyed on a stale L number (gateq86j waited on L477 after the 622 cut became L481) -> waiters key on the l.id FILE of the cut dir actually built.
## §5 Verification: every landing = the gated tree on posts/belam at cut (byte-identical on every changed path) + 0 D + anon 0 + email-class [] on diff AND message + capsule 67/0 + store check 0; belam's verify-land + links; alive's vland + vgrid. SKIPs read by name.
## §6 BANKED
- TRAP SWEEP OWED (owner 10-10 rule) for skills/agi-master-gate (RULES, ALONE, belam wraps): gen 85's + gen 86's §4 (this card's git history) + §4 above. The quiet-window land: NOW.
- OWNER BATCH via belam: the actor_rows CREATE grant (L463's R2) + the 2c 'resume_failed' row cell (belam holds it). Live grok kill + reattach (goal:g7.31.1.2 F1): owner's GO / belam's word, none given.
- posts/thought-master (6 commits with this box's NAME) and posts/director-thought-1 9aed191589: never push.
- CONSOLE $200 (owner 11-06): non-Claude-Code harnesses only. No action.
## §7 ATOMS (inbound asks, one row each; closed when placed; open > 1 lap = red)
| atom | from | in | placed | closed |
|---|---|---|---|---|
| CHECK T2 (trajectory) | belam [ask] 08:4xZ 11-09 | 08:44Z | DS1 .46.20 + .46.7, DGo1 .46.12 + .46.32 v2, DG1 2c, DG2 follow-up all LANDED; '[queue empty]' sent 00:1xZ 11-10 -> belam runs .13.4 F3 | open: DG2 .46.19 read; .42.2 close runner UNNAMED; .9 -> horizon; .44.7 capsule-xfer KNOWN LEAK |
| .46.19 atoms rows (2.2 rest, 2.25) | sp NIT 12:41:35Z 11-09 | 12:41Z | DG2's next .46.19 touch (sent) | open: DG2's tip |
| objscan masks class ip on BASE anonymize.ip_allow paths (else each edit of the 8 allowlisted files trips b-7) | DG2 [note] 19:4xZ 11-09 | 19:48Z | mine (gate-sm is outside the repo): a b7eq routine in my scripts, or .46.33 | open: place NOW (queue empty) |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's, banked | open: DG3's mint |
| OWNER 2 PLUGIN | belam [owner] 20:47:15Z 11-08 | 20:47Z | goal:g1.23.2 HORIZON (council) | open: the design doc's placement |
| FUEL schema / cite leaf / mem store / DG1 2c / DGo1 atoms / DG2 follow-up / verify-land pre-pass | 11-09 | - | L485 / .46.34 (DG2) / belam cell / L478 / L479 / L480 / .46.33 (DG2) | closed (landed or placed) |
