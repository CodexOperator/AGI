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

## §0 State (10-02 ~00:0xZ, gen 6 awake, everything landed incl. -23, queue empty, waiting for orders)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (agi-post@director-general-1, cgroup-confirmed; row engine.v 4, boot true) · parent SM · trunk local-maxxing/season2/main |
| mail | `send.py --from director-general-1 send POST 'text'` ONLY (inbox form). To belam tags merge-up · decision · rotation · red · rule · complete · owner (an ack = ONE [rule] line); NEVER SendMessage to belam. Bodies with an apostrophe or a backtick: write a heredoc file, then `msg=$(cat F); send.py ... "$msg"`; no angle brackets. goal:g1.40 race: re-send ONCE if unanswered in 15 min |
| roles | DG1 = inner loops + nodes + the merge-ups; DG2 = experiments/falsifiers; DG3 = builds; SM gates + lands (Sonnet mur + full gate); belam = the Prime (config/anchor rings, every HOST ACT = his own GO, quoted: command + before-state + one-command rollback) |
| skills | agi-goal · agi-send · agi-dispatch · agi-rotate · agi-corrective · agi-node-write (old setup only: I edit nodes with Edit/Write; agi-turn commits) |

## §1 Plan
```
done   ALL LANDED: level round 3a33c71b9 · -20 8083ec340 · -22 819331783 · -21 c59788625 · BOX AUDIT bae704905 · -23 4b741b4f9 (outcome + decisions: logs_dir stays, user stays; SM struck the {home} item) · -19 -16 -17 · DG3 M1/M3 M2 + agi-land follow-ups. All dg1-* worktrees removed
now    NOTHING QUEUED ON ME (SM 23:5xZ). Waiting for the next order; never invent goals
asked  belam [owner] 01:5xZ (10-03): (1) UNBLOCK answered by [rule]: DG1 waits only on the council's flow-rotation design (owner/time unnamed; asked) (2) GRID answered by [rule], VERIFIED: node.md + payload = ONE grid tree (scratch test v1/v2 payload-only/v3 node-only/no-change; live 310/310 live build nodes grid tip == disk; cron v180). GAPS: 18 of 32 retired build nodes have no grid version holding their payload; files named by mvp source_files / hyp tests, file_scope / experiment probes not in the node's slot. My recommendation: no fix to the live path; optional goal:g1 round = commit_file also takes mvp source_files (29 nodes) + backfill the 18 from git history. WAIT for belam go/no-go; start NOTHING without it
bank   the 6 portable box hits belong to their owning builds (DG3 install acts, box.allow); DG3: A3 round (goal .11.11.1.1) after A2, install acts A1-A8 + agi-land land step (each its own belam GO line); hollow-review hyp g733-... NOT dispatched (belam: not urgent)
hold   phase W (skill agi-spawn-chain) until the council flow-rotation design lands · shell tests goal .16 + t1-t3 after W · goal .17 belam-on-v5 horizon
```

## §2 Landed today (one line each; trunk shas)
c2decf431 Z4 phase A · 96140880b pb3 · 3e10246bd Z4 re-cut · 2e9902533 W amended + shell-tests nodes · bc9658da7 g1.40 + .17 + agi-spawn-chain name · 71b8677c3 AA1.M leaf + 3 hyps · 826a0d831 AA1.M active

## 🔴 Where it stops + the exact next command
Idle, queue empty, no worktree open (belam go/no-go on the grid round pending). NEXT: `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1`; act only on a block newer than 23:5xZ. Hold items need the council's flow-rotation design (phase W) or an owner/belam order. pytest for my account: venv with system site packages (python3 -m venv --system-site-packages V; V/bin/pip install pytest).

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
