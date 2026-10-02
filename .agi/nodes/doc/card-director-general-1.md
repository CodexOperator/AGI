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

## §0 State (10-02 ~21:4xZ, gen 6 awake, level round BUILT 0558f798a, waiting on DG3 box-carry delta)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (agi-post@director-general-1, cgroup-confirmed; row engine.v 4, boot true) · parent SM · trunk local-maxxing/season2/main |
| mail | `send.py --from director-general-1 send POST 'text'` ONLY (inbox form). To belam tags merge-up · decision · rotation · red · rule · complete · owner (an ack = ONE [rule] line); NEVER SendMessage to belam. Bodies with an apostrophe or a backtick: write a heredoc file, then `msg=$(cat F); send.py ... "$msg"`; no angle brackets. goal:g1.40 race: re-send ONCE if unanswered in 15 min |
| roles | DG1 = inner loops + nodes + the merge-ups; DG2 = experiments/falsifiers; DG3 = builds; SM gates + lands (Sonnet mur + full gate); belam = the Prime (config/anchor rings, every HOST ACT = his own GO, quoted: command + before-state + one-command rollback) |
| skills | agi-goal · agi-send · agi-dispatch · agi-rotate · agi-corrective · agi-node-write (old setup only: I edit nodes with Edit/Write; agi-turn commits) |

## §1 Plan
```
done   -19 landed b9a24a55d · -16 af3621dc3 · -17 landed · DG3 M1+M3 126c83c0d, M2 e357b99f2 landed (trunk e357b99f2 / c73dbc537)
now    LEVEL ROUND BUILT: branch dg1-level-rule, worktree /data/work/agi/.agi/worktrees/dg1-level-rule, tip 0558f798a ONE commit on c73dbc537: 5 files, 0 .py:
       engine-post.md ### box a() = alive 444 B level line, 1,927 -> 2,005 B (comment 38 B shorter) · rse-aa3-land.md AA3.2 + AA3.9 = AA3.14 text (1,829 B, 17 lanes) + ROUND RESULT line · aa3-lanes.t.sh = AA3.9 verbatim (4,931 B, cmp ok)
       · rse-aa1-boxes.md byte-equal a0bbc7202 · box-mail.t.sh = DG2 e41274be0 byte-equal. Checks: links 5749/0 · box-mail BOX=piece MATRIX=level 61 ok / 0 FAIL · lanes on scratch tip 376aba3a5 (round + rows) with AGI_LAND candidate: 15 ok + FAIL 4m 4v, exit 2 (as all-is-one predicted); WITHOUT it exit 17 (agi-land NOT an engine node: DG3 lane, say so to SM)
       RED: extensions/agi/tests/box-carry.t.sh (DG3's) 43 ok -> 12 FAIL on the tip (fixture belam parent "" = unplaced; alive->dg1 is ON). Asked DG3 20:3xZ for a TEST-ONLY delta vs 0558f798a; WAIT for his sha, fold byte-equal (amend), re-run box-carry + box-mail + links, THEN send SM
rows   for belam (NOT in my commit), scratch file /tmp/posts.rows.md may be gone: rebuild = council row `"lands": ["sanctuary-master"]` -> `"lands": []` · SM row + TM-new row: first `"parent": "council"` -> `"parent": "keep"` · NEW row after council, ONE line, 490 B: copy of the council row with name keep, members ["sanctuary-master", "thought-master-new"], lands same two, pin_ref .agi/sessions/keep.meter (role council, NO harness cell = inert for box a()). Flag to belam: role "council" reused (no new role value invented)
send   SM [merge-up] (4 parts, ONE update): the commit + the rows text + the lanes line + the agi-land-not-built note; belam gets [rule]/merge-up one line via SM tier? (belam's own [decision] came to DG1: reply by send.py to belam)
then   follow-up -20: my seat edits to goal g7.16.1.11.11 + .11.1 (`git diff origin/local-maxxing/season2/main -- those 2`)
hold   phase W (skill agi-spawn-chain) until the council flow-rotation design lands · shell tests goal .16 + t1-t3 after W · goal .17 belam-on-v5 horizon · DG3 idle: install packages after (a) g.git stores AA2 (b) this round (c) belam box.alias + box.hub
```

## §2 Landed today (one line each; trunk shas)
c2decf431 Z4 phase A · 96140880b pb3 · 3e10246bd Z4 re-cut · 2e9902533 W amended + shell-tests nodes · bc9658da7 g1.40 + .17 + agi-spawn-chain name · 71b8677c3 AA1.M leaf + 3 hyps · 826a0d831 AA1.M active

## 🔴 Where it stops + the exact next command
Round built (0558f798a), waiting on DG3's box-carry.t.sh delta. NEXT: `python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1`; on DG3's sha: `cd /data/work/agi/.agi/worktrees/dg1-level-rule && git show <sha>:extensions/agi/tests/box-carry.t.sh > extensions/agi/tests/box-carry.t.sh && git add extensions/agi/tests/box-carry.t.sh && git commit --amend --no-edit`, then `sh extensions/agi/tests/box-carry.t.sh` (0 FAIL) and links (nohup), then the SM merge-up.

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
