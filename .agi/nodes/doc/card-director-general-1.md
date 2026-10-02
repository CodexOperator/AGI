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

## §0 State (10-02 ~22:0xZ, gen 6 awake, level round RETURNED (R1-R4); my half done, waiting on DG2 box-mail delta)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (agi-post@director-general-1, cgroup-confirmed; row engine.v 4, boot true) · parent SM · trunk local-maxxing/season2/main |
| mail | `send.py --from director-general-1 send POST 'text'` ONLY (inbox form). To belam tags merge-up · decision · rotation · red · rule · complete · owner (an ack = ONE [rule] line); NEVER SendMessage to belam. Bodies with an apostrophe or a backtick: write a heredoc file, then `msg=$(cat F); send.py ... "$msg"`; no angle brackets. goal:g1.40 race: re-send ONCE if unanswered in 15 min |
| roles | DG1 = inner loops + nodes + the merge-ups; DG2 = experiments/falsifiers; DG3 = builds; SM gates + lands (Sonnet mur + full gate); belam = the Prime (config/anchor rings, every HOST ACT = his own GO, quoted: command + before-state + one-command rollback) |
| skills | agi-goal · agi-send · agi-dispatch · agi-rotate · agi-corrective · agi-node-write (old setup only: I edit nodes with Edit/Write; agi-turn commits) |

## §1 Plan
```
done   -19 b9a24a55d · -16 af3621dc3 · -17 · DG3 M1+M3, M2 landed · level round b6b7474dc SENT, RETURNED by SM 21:5xZ (mur dg1-level-round accept_with_residue; gate GREEN on all bytes; belam rows ad37a5583 stay as authored, 4 parts land together)
now    CORRECTIVE on dg1-level-round (worktree /data/work/agi/.agi/worktrees/dg1-level-rule): my commit on b6b7474dc DONE = R3 engine.md box 2005 B · R4 box-send hyp rewritten (2,005 B, level a(), n1 2005, falsifier > 2,005; sibling Limits lines) · obs: 21 unplaced harness rows named on the Limits. STILL OPEN: R1 (BLOCKING) + R2 = DG2's box-mail.t.sh (asked 22:0xZ): default BOX = `sect box` from the trunk piece, case b0 back, rows follow the piece's a(), CEIL 2005; R2 one read-refused case, a PLACED pair two apart (DG1-signed commit read by belam). WAIT for DG2's sha, fold byte-equal: `git show <sha>:extensions/agi/tests/box-mail.t.sh > ...; git commit --amend --no-edit`
       then: run box-mail default (2.5 min, nohup) + box-carry + links (nohup) + check the hyp line 45's case names (b0, o1/o2 wording) match the new test; SEND SM [merge-up] with the tip (he re-gates with ad37a5583, re-mur only if a() changes; it does not)
next   -20 (cut from the LIVE trunk after the round lands): (a) my seat edits to goal g7.16.1.11.11 + .11.1 (`git diff origin/local-maxxing/season2/main -- those 2`) (b) the A3 signers BUILD leaf (belam agreed F4; A3 = gitconfig allowedSignersFile + agi-post@ ExecStartPre=+agi-signers + retire the .agi/keys copy; goal leaf under .11.11.1, skill agi-goal; detail doc:dg3-aa1m-install-packages, DG3 af73e8bfe)
then   FINDING to place: config.json box.root stale path = the [box].md leak literal paths.py scans; belam added box.repo = /data/work/agi (12e8065cc). What should the leak scanner look for on THIS box? (after -20)
hold   phase W (skill agi-spawn-chain) until the council flow-rotation design lands · shell tests goal .16 + t1-t3 after W · goal .17 belam-on-v5 horizon · DG3 idle: install packages after (a) AA2 g.git stores (b) this round (c) belam box.alias/hub
```

## §2 Landed today (one line each; trunk shas)
c2decf431 Z4 phase A · 96140880b pb3 · 3e10246bd Z4 re-cut · 2e9902533 W amended + shell-tests nodes · bc9658da7 g1.40 + .17 + agi-spawn-chain name · 71b8677c3 AA1.M leaf + 3 hyps · 826a0d831 AA1.M active

## 🔴 Where it stops + the exact next command
Corrective half done (R3, R4, obs committed on dg1-level-rule); waiting on DG2's box-mail.t.sh delta (R1 + R2). NEXT: `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1`; on DG2's sha fold it as in §1, re-run the checks, then [merge-up] to sanctuary-master with the new tip.

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
