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

## §0 State (10-03 ~02:5xZ, gen 6 awake, everything landed through -24; builders handed; judging returns)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (agi-post@director-general-1, cgroup-confirmed; row engine.v 4, boot true) · parent SM · trunk local-maxxing/season2/main |
| mail | `send.py --from director-general-1 send POST 'text'` ONLY (inbox form). To belam tags merge-up · decision · rotation · red · rule · complete · owner (an ack = ONE [rule] line); NEVER SendMessage to belam. Bodies with an apostrophe or a backtick: write a heredoc file, then `msg=$(cat F); send.py ... "$msg"`; no angle brackets. goal:g1.40 race: re-send ONCE if unanswered in 15 min |
| roles | DG1 = inner loops + nodes + the merge-ups; DG2 = experiments/falsifiers; DG3 = builds; SM gates + lands (Sonnet mur + full gate); belam = the Prime (config/anchor rings, every HOST ACT = his own GO, quoted: command + before-state + one-command rollback) |
| skills | agi-goal · agi-send · agi-dispatch · agi-rotate · agi-corrective · agi-node-write (old setup only: I edit nodes with Edit/Write; agi-turn commits) |

## §1 Plan
```
done   ALL LANDED through -24 f40ae4c38 (SM 02:3xZ): level round, box audit, -19..-23, -24 (goal .11.12 active, W unheld + 3 build rounds, K1 hyp, lost-wake closer hyp, goal g7.33.19.1 + grid hyp). No dg1-* worktree open
now    NOTHING QUEUED ON ME. Builders handed by mail (02:4xZ): DG3 = A3 signers wiring first (A6 + the ring wait on it), closer, grid fix, W-1; DG2 = falsifiers (closer case in box-carry.t.sh, agi-kid-flow.t.sh, grid cases; K3 is DG2's per SM). My job now: JUDGE their returns (skill agi-dispatch §5) and hand on the next; answer belam/SM
bank   belam: model_hint ruling (a) cap by the invoker's kid cell; kid cell with usd + K1 GOs; skills clause rename at W's merge-up; owner options (mvp source_files in the grid slot, the 18 retired payloads: NO-GO for now)
hold   shell tests goal .16 + t1-t3 (builds after W-1) · goal .17 belam-on-v5 horizon
```

## §2 Landed today (one line each; trunk shas)
c2decf431 Z4 phase A · 96140880b pb3 · 3e10246bd Z4 re-cut · 2e9902533 W amended + shell-tests nodes · bc9658da7 g1.40 + .17 + agi-spawn-chain name · 71b8677c3 AA1.M leaf + 3 hyps · 826a0d831 AA1.M active

## 🔴 Where it stops + the exact next command
Idle: all my merge-ups landed, builders handed. NEXT: `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1`; act only on blocks newer than 02:3xZ 10-03: a DG2 falsifier delta or a DG3 build return = judge by bytes (skill agi-dispatch §5: run the test file, check sha/range, byte ceiling) then fold/forward to SM as a [merge-up] if it is mine to send, or tell the sender to send; belam/SM questions. Never invent goals.

## §4 Traps
| trap | rule |
|---|---|
| `git worktree add -b N PATH BASE` creates the branch then often fails to make the tree | run `git worktree add PATH N` (no -b) once; a stuck CHERRY_PICK_HEAD in a worktree gitdir: rm it there |
| links.py links takes ~3 min and times out foreground | nohup it to a file + a Monitor on a .done marker |
| anonymize.py needs MAIN .env: unreadable for my uid | SM runs it; scan the diff by hand for key/IP/email/home patterns; unit names like agi-act2@ghost.path trip EMAIL_RE (belam to rule an email_allow cell; never rename: sha 9e4180a5 is what he GOed) |
| a follow-up is cut from the LIVE trunk AFTER SM's [landed]; never cherry-pick a branch still in his gate | copy files byte-equal, compare, links, one commit |
| a host act is belam's own GO each | never run one; forward DG2's package as ONE line (command, before-state, rollback), read the script whole + check its sha256 first |
| `.py` in an AA1.M range | SM's gate refuses: leave scratch twins out (host-act-2-twin.py stays on DG2's branch) |
| owner quotes verbatim | curly apostrophes kept; excerpts marked [...] |

## §5 Verification: links.py links 0 broken · yaml parse on every changed node · script sha256 9e4180a5 (act 2) and a53de7d5 (act 2b ghost) unchanged

## §6 BANKED
- belam pending: anonymize email_allow cell for agi-* unit names. DG3: M2 re-review (box-carry + agi-signers + 4 unit texts), install GOs after it. Host act 1 re-run (must read G after the signers fix) and act 3 (second box) still to come, each its own GO.
- belam [decision] 19:5xZ: DG1 -> belam is OFF by design under the box matrix (speak up ONE tier: mail SM); sibling DG1 -> DG2 -> DG3 ON via the figure-eight edge once the box is built; until then send.py.
