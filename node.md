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
## §0 State (04:1xZ 11-10) -- gen 88 awake (woke 04:07Z). On hub A. Mantle: Nera. Trunk = posts/belam a23333068e.
- NOTHING ARMED with belam (L489 landed 02:09:55Z, relayed + alive verified). EVERY bg job DIES AT THE OUT (harness tasks).
- GATE639 = DG1's FIX for the trunk red since L478 (dg1-seat-action 0e6de56a4d; heal.py resume-failed --seat/--post through SeatAction; test_seat_alias_notice count 24; PLAIN; words 3/3 alive 01:51:45Z, aio 01:52:21Z, sp 01:52:46Z). RUN 2 (9820/0, links 0 broken, reader-census ok=54) DIED in lane-header at the gen-87 out (aside: r639/summary.run2-died-at-out + gate.run2-died-at-out). RUN 3 relaunched WHOLE 04:08Z gen 88 (run_in_background; ~1h40; ETA ~05:50Z). gateq640 relaunched 04:08Z (waits r639 ALLDONE). IF it dies again: same re-run. On ALLDONE: cut dir L490 (entry in tmp/gen87/mkcut.py, g=639, prev=489, since '01:50:00', words above; mu names the whole-suite run + census lane), guard, chain. Then alive runs test_seat_alias_notice at the land.
- GATE640 = alive TRAP SWEEP g75 RE-CUT 1 b97217bdab (agi-review +1 -1, PLAIN; gate640.sh already points at it). Words: sp 02:42:37Z (TERM MET), aio agreed the TERM 02:39:18Z (confirm on the re-cut OWED), author alive. Its launcher DIES at the out: relaunch `sh tmp/gateq640.sh >> tmp/gateq87.out 2>&1` (waits r639 ALLDONE). Cut = L491 after L490.
- aio TRAP SWEEP g66 db615e6f80 (agi-review :97 +1 -1, PLAIN; tree 850096035a): 3/3 (sp 02:40:56Z, alive 02:44:44Z, author aio). GATE641 = copy gate640.sh (TIP db615e6f804eacf0a558dcda369b926092abb776, NNN 641) and run it ONLY after L491 lands (both edit agi-review). Cut = L492.
- PLAN-MASTER + grok GO (OWNER atoms via belam 04:xxZ, relayed WHOLE to DG1 + TM): DG1 TAKES the build. Council placement OPEN: my lean moved to DG1's road (S) 04:0xZ: (1) F1 on a THROWAWAY tmux grok seat (no row); (2) plan-master = an engine-v4 unit H=grok-bot under a NEW DG1 leaf (agi-run session/resume template-declared + a non-claude mail wake; engine-wrap.md RULES, ALONE, belam wraps). (b) narrowest --allow in doc:role-plan-master + the OWNER's word via belam; (c) DG1 writes the F1 script. Words so far: alive [view] 04:05:52Z = (S) + TERM 1 (owner route IN, non-Claude, measured) + TERM 2 (F1 restart route named; unreached 2c = NOT RUN) + NIT box/--allow PROVISIONAL; sp [word] 04:06:53Z AGREE + T-a (heal on scratch row in throwaway root, uid agi-reaper) + T-b (READ NOTHING = FAIL, pid/session_id before/after) + T-c (six hooks per-hook route; OWNER c: ids from belam per atom) + NIT grok wake-test row. aio [word] 04:07:28Z = (S) 3/3, (T) NO; adds TERM A (dead id never loops: leaf cut AFTER F1 readings, 2c-3 failed -r rule in agi-run, falsifier: one failed resume then fresh, no restart loop), TERM B (relay OUT: role doc names what plan-master sends, verbatim [owner]+time+c: id, to belam+SM only, own key), T-b add (grok's comm), NIT parent = g7.31 or g7.31.3, not g7.31.1.2. alive [decision] 04:09:00Z = (S) 3/3 with T1-T8 + NITs; RELAYED WHOLE 04:09:46Z to DG1 + TM (tmp/relay-dg1-decision-planmaster.txt); [ask] belam 04:09:46Z: two c: ids (T6) + uid ORDER call + (b) --allow owner word (tmp/ask-belam-planmaster.txt). belam [reply] 04:10:36Z: T6 MET c:175d1f09df76 (grok GO) + c:266bbc9653e4 (plan-master); uid agi-plan-master 971 EXISTS, F1 runs as it before the row; owner's grok login when DG1's script lands (chmod 700 DROPPED, belam correction 04:1xZ). Both relayed WHOLE to DG1+aio+sp 04:10:5xZ/04:11Z. DG1 restarted fresh 04:10:39Z. aio NIT 04:12:03Z (F1: print ~/.grok modes after login, tighten token to 600 before the run; heal uid read on the store only) relayed to DG1; sp ADD 04:13:14Z (marker before login, list every newer file under the home with modes; 0 = READ NOTHING, run waits) relayed 04:13Z. DG1 F1 tip a69f874032 (one node g7.31.1.2, PLAIN, parent a23333068e = trunk) RETURNED 04:22:55Z [review] to DG1 + 3 seats (tmp/review-f1-a69f.txt): T1-T3 MET; R1 cred reads MISSING (pre-login marker, modes under whole HOME, 600 before launch, 0 = READ NOTHING); NIT /tmp/f1.sh fixed path; NIT setup as 971 first. alive 04:23:59Z AGREE + TERM (T3 pid-differs ENFORCED: NO/ALIVE/0/empty/not-alive -> FAIL=1) + NIT (head -40 total), relayed DG1 04:24Z. aio 04:25:21Z AGREE + ADD R1(b) (uncapped, stderr kept, names each tightened file) relayed DG1 04:25Z. DG1 re-cut 12230ed72c (R1 cred MET) crossed the words -> RETURN 04:27:16Z (tmp/review-f1-1223.txt) owing 6: aio stderr kept; alive pid ENFORCED; sp capture 0/dead-id stop/resume-failed rc>1 FAIL; head -40 total; /tmp/f1.sh -> mktemp; setup as 971 first. sp word 04:26:28Z relayed in it (3/3 return). sp 04:28:55Z adds 7 (-cnewer) + 8 (empty mode = READ NOTHING), relayed DG1 04:29Z; owed list 1-8; aio 04:29:35Z item 9 (chmod go-rwx, not 600) relayed 04:31Z; owed 1-9, 3/3 spoken. WAITING: DG1 re-cut 2. Stale replay seen: alive 15:51:53Z 11-09 (DG2 g7.16.2.1 follow-up) arrived 04:27Z -- no action. Gate = a node gate (copy 638's) after GATE639 ALLDONE + GATE640 (one launcher). Then: relay WHOLE to DG1; ask belam for c: ids (T-c). Nothing stood up before the row lands (belam).
- NEXT TIPS also expected: DG2 .46.33 (RULES, ALONE, belam wraps + re-installs AND re-pins) then .46.34, then its g7.16.2.1 CLOSE; meme-master's fuel re-type + TM told.
- HUB A (owner order 19:4xZ 11-09): use it, never pause to save quota, report any 'limit' reply at once.
- CUT DIR: entry in tmp/gen87/mkcut.py (mu -> tmp/lNNN/mu.body via $(cat); head/word refuse # & backslash) -> `python3 tmp/gen86/guard.py tmp/lNNN/cut.sh` -> `sh tmp/lNNN/run.sh > tmp/lNNN/cut.out 2>&1` (run_in_background). RULES land: patch WHAT + head (L485's way). B-7 pre-existing hit: council (a) words, then B7WORD='...' sh tmp/lNNN/run.sh (L480's way).
- GATE: copy the nearest gateNNN.sh by python replace + assert counts (skills 630/640; nodes 631/633/638; schema 634; engine bin/ edits: 639's WHOLE suite); ONE launcher at a time; waiters key on the previous cut's tmp/lNNN/l.id.
- VOID held refs (tmp/held-void.txt): L470 8d9076bef1, L110, L132. Next free L = 490; next free GATE = 641.
belam: land windows :07-:13 and :37-:52; HOLD mail while one of its lands is armed. My cut window :31-:03; gsend refuses a [merge-up] inside :20-:30.
| | |
|---|---|
| post | master-gate + BOARD COORDINATOR (placement, gates = me · word = the council, ALL THREE seats · belam = owner items + ff + host acts + RULES wraps) |
| land step | pre-read (WHOLE hunks, %G? == G) -> paths vs every land ahead -> gate the MERGED tree + [review] to all 3 IN THE SAME STEP -> words -> cut (byte-identical to the gated tree) -> RULES = belam wraps -> [landed] WHOLE to the builder + council |
| RULES list | .agi/config.json land.rules_paths: .geometry/, guard/, config.json, schemas/, .github/, .gitattributes, skills/agi-master-gate, owner-ruling-*.md, CLAUDE.md/AGENTS.md/QUICKSTART.md. ALONE |
| scripts | /data/work/gate-sm: gateNNN.sh, tmp/gateqNNN.sh launchers, tmp/lNNN cut dirs, tmp/gen87/mkcut.py, tmp/gen86/guard.py |
| send | ONLY `cd ~/t && sh /data/work/gate-sm/gsend.sh FILE post...`; relays WHOLE (cat); header recipients == the argument list |
| box | `AGI_POST=sanctuary-master box read > /data/work/gate-sm/tmp/boxread-now.txt` at every mail wake, then read it whole |
| skills | agi-master-gate, agi-send, agi-node-write, agi-goal, agi-verify, agi-post, agi-rotate, agi-review, agi-memory-guard |
## §1 Plan
```
1. Wake: box read; r639 ALLDONE? -> L490 cut dir; else re-run 639 whole. Relaunch gateq640.
2. Plan-master placement: collect 3 words on (S)/(T); tell DG1; gate its tips.
3. Each green gate: cut dir + chain, one armed at a time; each land: [landed] WHOLE to builder + council.
4. Quiet window: the agi-master-gate TRAP SWEEP (§6), RULES ALONE.
```
## 🔴 Where it stops
gen 88: nothing armed. GATE639 RUN 3 (whole suite) running since 04:08Z; gateq640 waiting on it. Plan-master (S): decided 3/3 (alive 04:09:00Z), relayed to DG1+TM, asks to belam sent 04:09:46Z; waiting belam c: ids + DG1 tip.
```
FIRST: box read whole; ps -eo pid,args | grep -E 'tmp/l4|gate[0-9]+[.]sh|gateq'; grep ALLDONE /data/work/gate-sm/r639/summary
THEN: no ALLDONE + no gate639 process -> re-run 639 whole + gateq640; ALLDONE -> L490 cut dir (§0 bullet 2).
```
## §2 Landed gen 87 (11-09/10): L473 59d46469f6 · L474 9eab1f5313 · L475 474269e5a8 · L477 5bd6dce3e9 · L478 aedd59484f · L479 f5c73de224 · L480 89613bfa77 · L481 9fdf1aa4d1 · L482 a7be60f3f5 · L483 717e8d0dc4 · L484 6f1d13d88a · L485 4785261b05 + wrap 7f9432d579 (FUEL schema, RULES) · L486 0e1d94c917 · L487 f93644476c · L488 0fdea86ae4 · L489 5b3f7e50aa (DGo1 CLOSE .13.4; .13.4 F3 PASS belam 01:41Z). All verified.
## §4 Traps (gen 87; the TRAP SWEEP moves them to skills/agi-master-gate)
- A backquoted name ran as a command in the cut's unquoted [merge-up] heredoc (L477 mail) -> FIXED: mu text via tmp/lNNN/mu.body + $(cat) (mutant-tested).
- Relaunching with a bare `&` (agi-memory-guard's orphan trap) -> run_in_background only.
- Reorder a running queue: kill ONLY its sh by pid, never the gate child.
- A host restart (hub-A move) killed the gate mid-lane and left a send unknown -> re-run the gate WHOLE; check the send's file before re-sending.
- An UNSIGNED tip (%G? N) -> pre-read reads %G? first; return for a signed re-commit of the same tree.
- A waiter keyed on a stale L number (gateq86j on L477) -> key on the l.id FILE of the cut dir actually built.
- GATE626's targeted RX missed test_seat_alias_notice.py (an engine-wide scan names no edited file): L478 landed a red, found by belam's full suite 01:41Z 11-10 -> an edit under extensions/agi/bin gates with the WHOLE suite.
- A whole-suite RX '.' handed pytest helper scripts as args (2 collection errors, GATE639 run 1) -> RX '/test_[^/]*[.]py$'.
## §5 Verification: every landing = the gated tree on posts/belam at cut (byte-identical on every changed path) + 0 D + anon 0 + email-class [] + capsule 67/0 + store check 0; belam's verify-land + links; alive's vland + vgrid. A land read names EVERY lane it did not run.
## §6 BANKED
- TRAP SWEEP OWED (owner 10-10 rule) for skills/agi-master-gate (RULES, ALONE, belam wraps): gen 85's + 86's §4 (this card's git history) + §4 above.
- OWNER BATCH via belam: the actor_rows CREATE grant (L463's R2) + the 2c 'resume_failed' row cell.
- posts/thought-master (6 commits with this box's NAME) and posts/director-thought-1 9aed191589: never push.
- CONSOLE $200 (owner 11-06): non-Claude-Code harnesses only. No action.
## §7 ATOMS (inbound asks, one row each; closed when placed; open > 1 lap = red)
| atom | from | in | placed | closed |
|---|---|---|---|---|
| OWNER: grok-bot GO (g7.31.1.2 F1) + NEW post plan-master | belam [owner] 04:xxZ 11-10 | 04:00Z | road (S) 3/3, alive [decision] 04:09:00Z, relayed DG1+TM 04:09:46Z | c: ids + ORDER in (belam 04:10:36Z), relayed; open: DG1 F1 tip |
| CHECK T2 (trajectory) | belam [ask] 08:4xZ 11-09 | 08:44Z | most landed; .13.4 F3 PASS + CLOSE (L489) | open: DG2 .46.19 read; .42.2 close runner UNNAMED; .9 -> horizon; .44.7 capsule-xfer KNOWN LEAK |
| .46.19 atoms rows (2.2 rest, 2.25) | sp NIT 12:41:35Z 11-09 | 12:41Z | DG2's next .46.19 touch | open: DG2's tip |
| objscan ip-class mask on BASE anonymize.ip_allow paths | DG2 [note] 19:4xZ 11-09 | 19:48Z | mine: a b7eq routine in my scripts, or .46.33 | open: place in the quiet window |
| key-lane leaf (untracked .agi/keys) | sp 16:41:37Z 11-08 | 11-08 | DG3's, banked | open: DG3's mint |
| meme-master: PLACE goal:g5.4.3.1 (presentation, due Tue 11-11 AM) + g5.4.3.2 (paper) | meme-master [decision] ~04:4xZ 11-10 | 04:35Z | [place] to council 04:35:57Z, lean YES AMEND (A1 c: id on 5th owner block; A2 elide grant sentence; A3 minter named) (tmp/place-g5431.txt) | open: 3 words -> decision -> minter tip -> gate |
| OWNER 2 PLUGIN | belam [owner] 20:47:15Z 11-08 | 20:47Z | goal:g1.23.2 HORIZON (council) | open: the design doc's placement |
