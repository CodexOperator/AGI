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

## §0 State (10-02 ~20:1xZ, gen 6 awake, -19 sent, level-rule round queued)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (agi-post@director-general-1, cgroup-confirmed; row engine.v 4, boot true) · parent SM · trunk local-maxxing/season2/main |
| mail | `send.py --from director-general-1 send POST 'text'` ONLY (inbox form). To belam tags merge-up · decision · rotation · red · rule · complete · owner (an ack = ONE [rule] line); NEVER SendMessage to belam. Bodies with an apostrophe or a backtick: write a heredoc file, then `msg=$(cat F); send.py ... "$msg"`; no angle brackets. goal:g1.40 race: re-send ONCE if unanswered in 15 min |
| roles | DG1 = inner loops + nodes + the merge-ups; DG2 = experiments/falsifiers; DG3 = builds; SM gates + lands (Sonnet mur + full gate); belam = the Prime (config/anchor rings, every HOST ACT = his own GO, quoted: command + before-state + one-command rollback) |
| skills | agi-goal · agi-send · agi-dispatch · agi-rotate · agi-corrective · agi-node-write (old setup only: I edit nodes with Edit/Write; agi-turn commits) |

## §1 Plan
```
done   -19 corrective SENT to SM 20:0xZ: tip 76986d735 on f53e626ac (supersedes b72c4fd20), folds DG2 a27347fa4 (matrix cases only under MATRIX=figure8; default suite on the 1,927 B build) + the three "2,019 B" Limits lines marked SUPERSEDED; links 5748/0 broken; 0 .py. [rule] sent to belam: level-rule round taken
now    WAIT for SM [landed]/[returned] on -19 (inbox); remove no worktree until then
next   LEVEL-RULE ROUND (belam [decision] 19:59Z, ONE atomic merge-up, cut from the LIVE trunk AFTER -19 lands; worktree off origin/local-maxxing/season2/main):
       (1) level a() line, 444 B, whole text in posts/alive:.agi/nodes/doc/rse-aa1-boxes.md ("THE LEVEL RULE", ~l.323), 21/21 on 4f8ff13f2; replaces the a() line wherever the trunk has it
           (trunk: .geometry/engine*.md build + g716111-capsule-build.md l.335; box-mail.t.sh) (2) agi-land (doc rse-aa3-land.md AA3.2 l.41-48; trunk copy in .geometry/engine*.md ### agi-land): group = any row with a members cell (~+10 B, all-is-one)
           (3) WHO LANDS thought-master-new: council lands=[SM] today -> propose a keep row lands cell, council names it (4) byte-exact config:posts rows for belam: keep row whole (inert, members [sanctuary-master, thought-master-new]) + SM and TM-new parent -> keep; belam writes on a branch, SM lands all four in ONE update
       + falsifier re-run on the trunk tip (21/21 or the new count). Q1 inert rows add no level; Q2 belam > council{alive,all-is-one,self-perpetuating} + keep{SM,TM-new} > DG1-3 under SM, DT-1 under TM-new; DG4/DG5/DT-2 unplaced (down by owner)
       DG2 will send the level-rule matrix delta (cases + who-is-on-which-level) AFTER the council line lands: fold it into the round
then   follow-up -20: my seat edits to goal g7.16.1.11.11 + g7.16.1.11.11.1 (`git diff origin/local-maxxing/season2/main -- those 2`)
hold   phase W (skill agi-spawn-chain) until the council's flow-rotation design lands · shell tests goal .16 + t1-t3 after W · goal .17 belam-on-v5 horizon
```

## §2 Landed today (one line each; trunk shas)
c2decf431 Z4 phase A · 96140880b pb3 · 3e10246bd Z4 re-cut · 2e9902533 W amended + shell-tests nodes · bc9658da7 g1.40 + .17 + agi-spawn-chain name · 71b8677c3 AA1.M leaf + 3 hyps · 826a0d831 AA1.M active

## 🔴 Where it stops + the exact next command
Awake, -19 sent, waiting on SM, then the level-rule round. NEXT: `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1`; when SM [landed] -19: `git fetch origin && git worktree add /data/work/agi/.agi/worktrees/dg1-level-rule origin/local-maxxing/season2/main`, then read the level-rule text from posts/alive (`git show posts/alive:.agi/nodes/doc/rse-aa1-boxes.md`) and find the a() / agi-land lines on the fresh trunk with `git grep -n "a(){" origin/local-maxxing/season2/main`.

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
