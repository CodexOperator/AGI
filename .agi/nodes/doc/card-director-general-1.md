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
now    -25 SENT to SM ~02:5xZ (nodes only, 1 file): branch dg1-minus-25, worktree /data/work/agi/.agi/worktrees/dg1-minus-25, tip cb7daf410 on a609336a9: AA2 per-generation keys ONE-BOX half RELEASED (belam 02:3xZ, owner 02:3xZ); cross-box half NOT released (council); principal form = A3's. links 5759/0. WAIT for SM [landed]/[returned]; on [landed] remove the dg1-minus-25 worktree
judged DG2 returns I RAN at the sha and forwarded to DG3: (1) closer falsifier 0c88e036a (de-base-dg2-6, box-carry.t.sh +22, k8): 52 ok / 2 FAIL on the 3,105 B piece; build = one sweep line in the --fetch timer pass BEFORE the hub exit, box-carry <= 3,255 B (2) W-1 falsifier a84d23430 (de-base-dg2-7, NEW agi-kid-flow.t.sh +98): 21 FAIL / 6 ok on the 390 B agi-kid; CEILING DECIDED 1,856 B for the runner proper, slice walk + kid-of + model_hint = W-2. DG3 order: A3 signers wiring (goal g7.16.1.11.11.1.1) FIRST (A6 + the ring wait on it), then the closer, then W-1, grid fix (goal g7.33.19.1) when handed
judged (3) AA2 keys falsifier de-base-dg2-8 2cca158ef (agi-fresh.t.sh): I RAN it, 6 FAIL / 10 ok = DG2's numbers; build order sent to DG3 (one-line ExecStartPre edit with the -nt guard, ceiling 745 B) queued behind A3 signers, closer, W-1
dg2    next from DG2 (my hand-on, queued): agi-fresh.t.sh (AA2 keys one-box falsifier, hyp g716111-aa2-a-key-is-fresh-...), grid cases (g7.33.19.1); K3 (goal g7.16.1.11.18 falsifier 1) is SM's order, branch dg2-k3-mu fc7a1cabe at SM; K1 agi-mint.t.sh after belam's kid cell
wait   belam [rule] 02:3xZ (goal .11.17 belam-on-v5): (3) the [config] ring and (4) the anchor signer have no leaf/hyp: the COUNCIL designs them, THEN DG1 nests them under goal g7.16.1.11.17 in one nodes round; no build before the design
bank   belam: model_hint ruling (a) cap by the invoker's kid cell (on the W hyp); kid cell with usd + K1 GOs; skills clause rename at W's merge-up; owner options (mvp source_files in the grid slot, the 18 retired payloads: NO-GO for now); the unit edits' installs = his own root GOs
hold   shell tests goal .16 + t1-t3 (builds after W-1) · goal .17 belam-on-v5 horizon · never invent goals
```

## §2 Landed today (one line each; trunk shas)
3a33c71b9 level round · bae704905 box audit (code 2507bad35 + belam/box-scan) · 8083ec340 -20 (A3 leaf, goal .13 active) · 819331783 -22 hollow-review hyp · c59788625 -21 box.root finding hyp · 4b741b4f9 -23 outcome · f40ae4c38 -24 AA2 placement

## 🔴 Where it stops + the exact next command
Rotated at the line with -25 at SM and two DG2 falsifiers forwarded to DG3. FIRST ACT on wake: `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1` (act only on blocks newer than 02:55Z 10-03; the last handled was DG2's agi-fresh delta). Then: SM [landed] on -25 -> `git -C /data/work/agi worktree remove .agi/worktrees/dg1-minus-25`; SM [returned] -> skill agi-corrective, fix on dg1-minus-25 (amend), links (nohup), re-send; a DG2/DG3 return -> run it at its sha (git worktree add --detach into the scratchpad), compare to their numbers, forward or send back.

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
