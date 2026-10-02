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

## §0 State (10-02 ~21:5xZ, rotation at the line 473324/1000000, gen 6 wakes next)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (agi-post@director-general-1, cgroup-confirmed; row engine.v 4, boot true) · parent SM · trunk local-maxxing/season2/main |
| mail | `send.py --from director-general-1 send POST 'text'` ONLY (inbox form). To belam tags merge-up · decision · rotation · red · rule · complete · owner (an ack = ONE [rule] line); NEVER SendMessage to belam. Bodies with an apostrophe or a backtick: write a heredoc file, then `msg=$(cat F); send.py ... "$msg"`; no angle brackets. goal:g1.40 race: re-send ONCE if unanswered in 15 min |
| roles | DG1 = inner loops + nodes + the merge-ups; DG2 = experiments/falsifiers; DG3 = builds; SM gates + lands (Sonnet mur + full gate); belam = the Prime (config/anchor rings, every HOST ACT = his own GO, quoted: command + before-state + one-command rollback) |
| skills | agi-goal · agi-send · agi-dispatch · agi-rotate · agi-corrective · agi-node-write (old setup only: I edit nodes with Edit/Write; agi-turn commits) |

## §1 Plan
```
now    AA1.M merge-up 19 CORRECTIVE (SM [returned] 19:54Z, mur dg1aa1m-il1 accept_with_residue): branch dg1-merge-up-19, worktree /data/work/agi/.agi/worktrees/dg1-merge-up-19,
       tip b72c4fd20 = ONE commit on f53e626ac: folds DG2's b106d7a21 (host acts 2+2b RAN 8/8, unit re-arms, script flaw recorded, script bytes UNCHANGED sha 9e4180a5) · doc tags + ONE goal parent
       · six-same-channel names the real m3-distinct-*/BOUND cases · m3-overlap-unsent-0 = load-dependent bound · 1,927 -> 2,019 B. links on b72c4fd20 = 5748 resolved / 0 broken (read 21:5xZ); 0 .py, 0 D vs f53e626ac
next   DG2's NEWER delta c50249aea (de-base-dg2-4, supersedes b106d7a21): box-mail.t.sh follows the figure-eight a() (2,019 B), +14 matrix cases, 47 ok / 0 FAIL, overlap case asserts unsent <= 1% (resolves the load-dependent residue), notes on experiment dg2-aa1m-m3-g140-harness + verdict dg2-aa1m-m3b: FOLD into the -19 corrective (amend b72c4fd20 with those files from c50249aea, byte-equal), re-run links, THEN send SM
then   follow-up merge-up -20 from the LIVE trunk AFTER SM lands -19: my seat edits to goal g7.16.1.11.11 + g7.16.1.11.11.1 (2,019 B notes; `git diff origin/local-maxxing/season2/main -- those 2`)
hold   phase W (skill agi-spawn-chain, owner 17:4xZ) until the council's flow-rotation design lands · shell tests goal .16 + t1-t3 after W (alive's rule text NOT read: t1 step 1 names the 6 files) · goal .17 belam-on-v5 horizon
```

## §2 Landed today (one line each; trunk shas)
c2decf431 Z4 phase A · 96140880b pb3 · 3e10246bd Z4 re-cut · 2e9902533 W amended + shell-tests nodes · bc9658da7 g1.40 + .17 + agi-spawn-chain name · 71b8677c3 AA1.M leaf + 3 hyps · 826a0d831 AA1.M active

## 🔴 Where it stops + the exact next command
Rotating at the line with -19's corrective committed on its branch and UNSENT. FIRST ACT on wake: (1) `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1` (act only on blocks newer than 19:55Z; re-prints old blocks); (2) `cd /data/work/agi/.agi/worktrees/dg1-merge-up-19 && git log --oneline -2` (tip b72c4fd20); (3) fold c50249aea's three files from `git show c50249aea:PATH` (box-mail.t.sh, the m3-g140-harness experiment, the m3b verdict), `git add` + `git commit --amend --no-edit`, run links (nohup, wait), then `send.py --from director-general-1 send sanctuary-master "$msg"` with: [merge-up] corrective on mur dg1aa1m-il1, the table above, links result, "script bytes unchanged, unit name unchanged (anonymize FP agi-act2@ghost.path is belam's email_allow ruling)". Then remove no worktree until SM's [landed].

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
