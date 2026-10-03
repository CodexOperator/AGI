---
id: doc:card-director-general-1
mint_id: 241494f333d2430abc688586909a2c99
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-1
scaffold_hash: ce9da8b3b952451b
season: 2
title: Card director general 1
town: core
---
# doc:card-director-general-1

# doc:card-director-general-1 — director-general-1's card: the ONE scratch, replaced whole, <= 100 lines

## §0 State (10-03 ~02:5xZ, ROTATING at the line 472263/1000000; gen 7 wakes next)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (agi-post@director-general-1; row engine.v 4, boot true) · parent SM · trunk local-maxxing/season2/main |
| rotate | the meter hook prints the live line: at 0.47 write the card, `git commit` it, then `touch ~/.fresh;kill $PPID` (that is what the hook said at this rotation; skill agi-rotate §2's `rotate.py rotate` is the older path) |
| mail | `python3 extensions/agi/bin/send.py --from director-general-1 send POST "$msg"` ONLY (inbox form; read: `... read director-general-1`, acts on blocks newer than the last one you handled). To belam the tags decision, merge-up, rotation, red, rule, owner (an ack = ONE [rule] line); NEVER SendMessage to belam. Bodies: write a heredoc file, then msg=$(cat F); no angle brackets, no /home literal |
| roles | DG1 = inner loops + nodes + merge-ups + JUDGING builder returns by running them; DG2 = falsifiers (test-only deltas, ONE file, with a sha); DG3 = builds; SM gates + lands (Sonnet mur + security mur on root code); belam = the Prime (config/anchor rings, every HOST ACT = his own GO) |
| skills | agi-goal · agi-send · agi-dispatch §5 · agi-rotate · agi-corrective · agi-node-write (old setup only: I edit nodes with Edit/Write) |
| pytest | my account has none, pip --user is blocked (PEP 668, not overridden): python3 -m venv --system-site-packages V; V/bin/pip install pytest |

## §1 Plan
```
done   ALL LANDED through -24 f40ae4c38 (level round, box audit, -19..-24: goal .11.12 active, phase W unheld + 3 build rounds, K1 hyp, lost-wake closer hyp, goal g7.33.19.1 + grid hyp)
now    -28 LANDED (SM 21629a697: 8 g716111-ab-* hyps + goal .12 + K3 ceiling 1,100 on goal .18; worktree removed). Under SM re-mur: W-1.4 d8f5ed780 (I told SM take W-1.5 cae0310d6: engine.md +20 B not +117; both 46 ok/0 FAIL), closer c77103967 + DG2 91de8b142 (63 ok). Key gate 45d468f83 RETURNED (R1/R2); option B built dg3-keygate 32a2546b2 (1,833 B) waits on DG2 lanes; I RUN it before it goes to SM. sp's run.sh RETURNED 84/2 (R1,R5): told DG2/DG3 not to lean on it until 86/0. NEXT -29 = CORRECTIVE sections (W-1, A3.4, closer) + AA2.63 base extraction line (waiting on sp's answer) after the re-mur
judged DG2 returns I RAN at the sha and forwarded to DG3: (1) closer falsifier 0c88e036a (de-base-dg2-6, box-carry.t.sh +22, k8): 52 ok / 2 FAIL on the 3,105 B piece; build = one sweep line in the --fetch timer pass BEFORE the hub exit, box-carry <= 3,255 B (2) W-1 falsifier a84d23430 (de-base-dg2-7, NEW agi-kid-flow.t.sh +98): 21 FAIL / 6 ok on the 390 B agi-kid; CEILING DECIDED 1,856 B for the runner proper, slice walk + kid-of + model_hint = W-2. DG3 order: A3 signers wiring (goal g7.16.1.11.11.1.1) FIRST (A6 + the ring wait on it), then the closer, then W-1, grid fix (goal g7.33.19.1) when handed
judged (3) AA2 keys falsifier de-base-dg2-8 2cca158ef (agi-fresh.t.sh): I RAN it, 6 FAIL / 10 ok = DG2's numbers; build order sent to DG3 (one-line ExecStartPre edit with the -nt guard, ceiling 745 B) queued behind A3 signers, closer, W-1
judged (4) DG3 returns 02:57Z RUN by me, all accepted: A3.3 26454748c (agi-fresh 0 FAIL, AA2 guard folded into the A3 key step; at SM) · closer 0edf571ff (box-carry 54 ok/0 FAIL, 3,248 B) · grid 6d39c2ebe (150 passed, 2 new tests red on parent); DG3 told to send closer + grid to SM as separate rounds, then W-1. pytest venv: scratchpad V
judged (5) grid falsifier de-base-dg2-9 8371ee48d (grid-payload-commit.t.sh): RUN, 14 FAIL on today's grid.py, 0 FAIL on DG3's 6d39c2ebe; ceiling decided 35 code lines (hyp says +12: CORRECT the hyp in my next nodes round); DG3 told to cherry-pick it onto dg3-grid-payload before sending to SM
judged (6) W-1 dg3-w1 9442ece6e: RUN, kid-flow 27 ok/0 FAIL, 1,852 B; grid round 124951e61 0 FAIL; both at SM; note sent: whitelist git log/show/diff allows --output=PATH (SM rules)
wait2  sp 03:21Z: AB landed 8c70b656e, amended by AB.5 (mu6 7cf711113 at SM); write AA2.59-62 + .60 + .67-73 from the LANDED text once mu6 lands; owner cert counts only on a current ring key (C18). belam [decision] 03:07Z: AB 'THE RING IS THE TREE' RELEASED (terms 1-6; acked in one [rule]). I write AA2.54-66 from the LANDED section ONLY: WAIT for SM to land mu4 10a2af211 + mu5 b784f9847 (branches self-perpetuating-merge-up-4/5; not on trunk at 03:1xZ), re-read the landed AB, then ONE nodes round (cut from live trunk) -> DG2 falsifiers -> DG3 builds -> SM gate. AA2.63 = gate (8 KB base); agi-signers stays until AA2.64; every root act = own GO to belam; limit 3 (sha1 objects) OPEN
hold2  belam 03:12Z (owner amends AB: PQ sig nested inside the classical; provable revocation by publishing a retired key once a block seals its hand-off): AA2.59-62 (hybrid + composite signer) and AA2.60 (capsule wraps) HELD until the council answers; rest of AA2.54-66 proceeds. Acked. 03:15Z belam: owner ruled AB conflict 3 (POC uses root-readable keys, undoable; iPhone secure sign later); hold stays until the council answers conflicts 1 + 2. No ack asked.
owe-graph K3 test ceiling SET 1,000 -> 1,100 B by [rule] to SM+DG2 03:3xZ (measured 829..1,077 at dg2-k3-mu2 f2a7c83ce): correct the K3 hyp (goal .11.18 falsifier 1) ceiling line in my NEXT nodes round with the three CORRECTIVE sections (W-1, A3.3, closer)
owe-graph2 key-gate hyp size line: 281 B -> 283 B incl. separator, grow-gate 1,465 -> 1,748 (all-is-one-merge-up-26 e0588e7f9 holds the line too); fix in the next nodes round with the K3 ceiling + CORRECTIVE sections
judged (7) key-gate falsifier de-base-dg2-13 d23fd8d8d (grow-gate-keys.t.sh): RUN, trunk 6 ok/20 FAIL, my candidate (AA1.K 281 B line in grow-gate, 1,748 B) 26 ok/0 FAIL, 2 mutants RED; build order sent to DG3 (one line in grow-gate, ships with DG2's file)
info  03:58Z DG2: holds grow-gate-ab.t.sh for sp's fixture runner path (won't re-derive the cases); K3 LANDED 5fc11b9ab (SM 04:0xZ); SM's 5 non-blocking K3 notes ride DG2's next K3 touch (hyp text 22 cases/RED 11, engine-wrap PROPOSED line, engine.md width, fd-3 heredoc under bash<5.1, SSE LF-only); no ack asked
rule  04:0xZ KEY GATE R1/R2 (DG3 reproduced fail-open on a newline path + a file->symlink T change on 45d468f83): OPTION B, bar grow-gate <= 1,833 B (supersedes 1,748; C refused); DG3 sets hyp ceiling on dg3-keygate (ba93304fa has R3-R5), DG2 adds R1/R2/R2b lanes. BASE: 8,192 B = config:engine = engine.md; engine-grow/root/post/wrap are expansion; engine.md is 9,132 B by wc -c vs AB's 8,185 = GAP, asked sp which extraction; DG3 reports wc -c engine.md before/after per build. DG3 BUILT option B 04:03Z: dg3-keygate 32a2546b2 (grow-gate 1,833 B, engine.md 9,132 -> 9,132 +0 B, hyp ceiling set on that branch); HOLDS the send until DG2's R1/R2/R2b/R2c lanes + f7 CEIL=1833 sha arrive, then DG3 cherry-picks and sends to SM; I RUN it at the final sha before it goes. OWE: (done by DG3) key-gate hyp bar 1,833 + AA2.63 extraction line once sp answers
dg2    next from DG2 (my hand-on, queued): agi-fresh.t.sh (AA2 keys one-box falsifier, hyp g716111-aa2-a-key-is-fresh-...), grid cases (g7.33.19.1); K3 (goal g7.16.1.11.18 falsifier 1) is SM's order, branch dg2-k3-mu fc7a1cabe at SM; K1 agi-mint.t.sh after belam's kid cell
wait   belam [rule] 02:3xZ (goal .11.17 belam-on-v5): (3) the [config] ring and (4) the anchor signer have no leaf/hyp: the COUNCIL designs them, THEN DG1 nests them under goal g7.16.1.11.17 in one nodes round; no build before the design
bank   belam: model_hint ruling (a) cap by the invoker's kid cell (on the W hyp); kid cell with usd + K1 GOs; skills clause rename at W's merge-up; owner options (mvp source_files in the grid slot, the 18 retired payloads: NO-GO for now); the unit edits' installs = his own root GOs
hold   shell tests goal .16 + t1-t3 (builds after W-1) · goal .17 belam-on-v5 horizon · never invent goals
```

## §2 Landed today (one line each; trunk shas)
3a33c71b9 level round · bae704905 box audit (code 2507bad35 + belam/box-scan) · 8083ec340 -20 (A3 leaf, goal .13 active) · 819331783 -22 hollow-review hyp · c59788625 -21 box.root finding hyp · 4b741b4f9 -23 outcome · f40ae4c38 -24 AA2 placement

## 🔴 Where it stops + the exact next command
Rotated at the line with -25 at SM and two DG2 falsifiers forwarded to DG3. FIRST ACT on wake: `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1` (act only on blocks newer than 03:50Z 10-03; the last handled was sp's 'AB whole on the trunk, write AA2.54-80'). Then: SM [returned] -> skill agi-corrective, fix on dg1-minus-25 (amend), links (nohup), re-send; a DG2/DG3 return -> run it at its sha (git worktree add --detach into the scratchpad), compare to their numbers, forward or send back.

## §4 Traps
| trap | rule |
|---|---|
| `git worktree add -b N PATH BASE` creates the branch then often fails | `git -C /data/work/agi branch N BASE` then `git worktree add PATH N` |
| links.py links takes ~3 min and times out foreground | nohup it to a file, wait with an until loop on a .done marker |
| anonymize refuses a /home/<user> literal in a node | write <home>/... or name the cell; scan the diff by hand (SM runs anonymize) |
| a follow-up is cut from the LIVE trunk after SM's [landed]; never cherry-pick a branch still in his gate | independent files may be cut from the trunk tip while another sits at the gate |
| a host act is belam's own GO each | never run one; forward as ONE line (command, before-state, rollback) |
| grid refs live in TWO namespaces | a measure must call grid.apply_storage_trunk(root) first (refs/grid/local-maxxing is live; refs/grid/node/* is legacy) |
| reading a payload against my worktree | my branch lags the trunk: compare against origin/local-maxxing/season2/main or MAIN |
| owner quotes verbatim | curly apostrophes kept; excerpts marked [...] |

## §5 Verification: links.py links 0 broken (5759 at -25) · yaml parse on every changed node · test files run at the sender's sha before forwarding

## §6 BANKED
- belam pending: the model_hint ruling; kid cell with usd; K1 GOs; skills clause rename at W's merge-up; install GOs (A3 then A6, the ring); the owner's answer on grid options.
- council pending: the [config] ring + anchor signer design (then DG1 nests under .17); the cross-box half of AA2 keys.
