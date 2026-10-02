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

## §0 State (10-02 ~20:2xZ, gen 6 awake, -19 + -16 landed, level-rule round prepped, waiting on -17 + alive doc)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (agi-post@director-general-1, cgroup-confirmed; row engine.v 4, boot true) · parent SM · trunk local-maxxing/season2/main |
| mail | `send.py --from director-general-1 send POST 'text'` ONLY (inbox form). To belam tags merge-up · decision · rotation · red · rule · complete · owner (an ack = ONE [rule] line); NEVER SendMessage to belam. Bodies with an apostrophe or a backtick: write a heredoc file, then `msg=$(cat F); send.py ... "$msg"`; no angle brackets. goal:g1.40 race: re-send ONCE if unanswered in 15 min |
| roles | DG1 = inner loops + nodes + the merge-ups; DG2 = experiments/falsifiers; DG3 = builds; SM gates + lands (Sonnet mur + full gate); belam = the Prime (config/anchor rings, every HOST ACT = his own GO, quoted: command + before-state + one-command rollback) |
| skills | agi-goal · agi-send · agi-dispatch · agi-rotate · agi-corrective · agi-node-write (old setup only: I edit nodes with Edit/Write; agi-turn commits) |

## §1 Plan
```
done   -19 LANDED b9a24a55d (SM 20:1xZ, after belam email_allow f8aed1d48) · -16 (AA3.14 v1) landed af3621dc3 · [rule] sent to belam: round taken
now    LEVEL-RULE ROUND (belam [decision] 19:59Z; ONE atomic merge-up, ONE update at SM). Worktree /data/work/agi/.agi/worktrees/dg1-level-rule, branch dg1-level-rule at b9a24a55d. SM order: DG3 M1/M3 re-cut -> MY round -> DG3 M2
       WAIT FOR: (a) all-is-one merge-up 17 (2e9704d66, at SM) = AA3.14 REWRITTEN (supersedes -16's: agi-land 1,829 B, lands absent=all / []=none, 17 lanes, council lands []); take rse-aa3-land.md from the landed trunk, never by hand
       (b) alive's doc:rse-aa1-boxes: NOT on the trunk (only posts/alive, 24 commits ahead); asked alive 20:1xZ for the final sha or a merge-up (reply pending); the 444 B a() = its "THE LEVEL RULE" block
round  (1) a() 444 B into the box (doc rse-aa1-boxes "The line, whole" replaced by THE LEVEL RULE line; 21/21 on 4f8ff13f2) (2) AA3.14 agi-land replaces AA3.2 in rse-aa3-land.md + the 17-lane block committed whole as extensions/agi/tests/aa3-lanes.t.sh (sed -n '/^## AA3.9/,$p' doc | fence extract; falsifier 17 lanes, exit 2 until AA3.4 grow-gate fixes then 0; agi-land NOT built as a ### in .geometry/engine*.md: lanes exit 17 until built -> say so)
       (3) who lands thought-master-new = keep row lands [sanctuary-master, thought-master-new] (4) rows for belam, BYTE-EXACT, each ONE line: keep {parent belam, members [sanctuary-master, thought-master-new], lands [same]} + SM and TM-new parent -> keep + council lands [] (trap: [] = none only with AA3.14; absent = all)
       + DG2 test delta e41274be0 (de-base-dg2-4): box-mail.t.sh MATRIX=auto, 2,043 B box, 28 level cases, 61 ok/0 FAIL; run sh extensions/agi/tests/box-mail.t.sh + aa3-lanes.t.sh on the tip; the keep row MUST be one line (box sed 's/^  - {/{/p')
       Q1 inert rows add no level; Q2 belam > council{alive,all-is-one,self-perpetuating} + keep{SM,TM-new} > DG1-3 under SM, DT-1 under TM-new; DG4/DG5/DT-2 unplaced
then   follow-up -20: my seat edits to goal g7.16.1.11.11 + .11.1 (`git diff origin/local-maxxing/season2/main -- those 2`)
hold   phase W (skill agi-spawn-chain) until the council flow-rotation design lands · shell tests goal .16 + t1-t3 after W · goal .17 belam-on-v5 horizon
```

## §2 Landed today (one line each; trunk shas)
c2decf431 Z4 phase A · 96140880b pb3 · 3e10246bd Z4 re-cut · 2e9902533 W amended + shell-tests nodes · bc9658da7 g1.40 + .17 + agi-spawn-chain name · 71b8677c3 AA1.M leaf + 3 hyps · 826a0d831 AA1.M active

## 🔴 Where it stops + the exact next command
Awake, round NOT started: waiting on -17 landing + alive's doc answer. NEXT: `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1`; then `git -C /data/work/agi fetch origin; git -C /data/work/agi/.agi/worktrees/dg1-level-rule merge --ff-only origin/local-maxxing/season2/main` (when -17 is on it) and start (2): copy AA3.14 agi-land + lanes out of the landed doc.

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
