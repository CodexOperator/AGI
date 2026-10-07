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

## §0 State (10-07 ~16:30Z, gen 10 live)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (engine.v 4) · parent SM · trunk local-maxxing/season2/main · my t = posts/director-general-1 |
| rotate | the meter hook prints the line: write this card, `git commit` it, then `touch ~/.fresh;kill $PPID` |
| mail | `python3 extensions/agi/bin/send.py --from director-general-1 send POST "$(cat FILE)"` ONLY, run FROM /var/lib/agi/director-general-1/t; bodies in a FILE (a shell string with $( expands: DG2 and DG3 both garbled one). Read: `... read director-general-1`, then ALSO grep the inbox FILE /data/work/agi/.agi/sessions/inbox/director-general-1.md (`read` can show empty). To belam tags decision, merge-up, rotation, red, rule, owner; ONE [rule] line back |
| roles | DG1 = goals + nodes + merge-ups + JUDGING every return by RUNNING it at the sha (then a mutant or sibling probe); DG2 = falsifiers (test-only, ONE file + sha, written FIRST, RED on the trunk); DG3 = builds; SM gates + lands (Sonnet mur, FULL suite); alive = council lead (designs); belam (rotating, next belam wakes) = Prime |
| scratch | worktrees: `git -C /data/work/agi worktree add --detach SCRATCHPAD/x SHA`, remove after; a branch: `git -C /data/work/agi branch N BASE` then `worktree add PATH N` |

## §1 Plan
```
OWNER 10-07 14:4xZ (via belam): old Python kept this season, shell rewrites = season 3, metrics back on, messaging needs a council pass; g7.16.1.11.17 RESTATED (horizon).
ENGINE QUEUE = NEXT SEASON, not built: pq, revoke(+LC_ALL=C), flowrot, round B mail, sealer box side. THIS season only: agi-signers retires = the ring-install step (belam GO).
LANDED (local trunk, pushed): CKPT.3, OUT.7, OUT.8, goals 1007d (120296316) + 1007e (5175738fb).
SM rotates (meter 0.40): his successor gates from his card; send [merge-up]s as usual. SM 17:00Z: FULL suite on the g3.8 union ad08961a4 = 7,914/0.
.19 VERIFY: dg3-verify6 0c6fc2d9a3 (trunk 5f672d11e5) RUN by me: lanes 42/0 (c4d60a0b32 blob-identical), both rotate.py callers read only rc 0 as pass; DG3 pytest 125 passed + 8 fails identical on the trunk. [merge-up] SENT 17:2xZ ("pane busy", sweep retries); choices (a) suite-only SKIP vetoes, (b) rc 2 write error ACCEPTED. The skip-only test renamed test_skip_only_is_not_green (my 16:39Z ruling).
g3.8 R1-R4: lanes 211a0a00c7 (36) ok; DG3 dg3-gmetrics2 ed0eae1462 (metrics_cell.py NEW, cell metrics_line, cmd via the helper): lanes 36/0, live line 632 B. MY PROBE: the helper COMMITS A HAND EDIT made during the 65 s run (check before cmd, recover after). SENT [return] to DG3 (re-check right before write.py; commit only write.py's own dirt) + DG2 lane r2e (hand edit during the run: HEAD unmoved, edit uncommitted, ONE skip/ERR line). metrics_cell.py needs NO build node (ruled). Then I run the re-cut + [merge-up].
g4.13.1 #3 gridcas flatten: DG2 lane 0563a18377 RUN (52 ok / 1 FAIL n1-lock-real), DG3 GO; his sha comes after g3.8. 
.20 messaging: DG2 lanes a1425b7d5 ACCEPTED (6 ok/16 FAIL on trunk); DG3 builds last (keep ~/o cap loop, cccc.ts s=n, pi types).
A12 stays ROLLED BACK (belam's install GO).
```

## 🔴 Where it stops + the exact next command
Waiting on mail. Next: `cd /var/lib/agi/director-general-1/t && python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1`, then grep the inbox FILE after ts 17:16:17Z.
1. DG2 lane r2e sha -> RED on ed0eae1462 (scratch worktree, `git show SHA:extensions/agi/tests/graph-metrics.t.sh` over it); DG3 re-cut: run the lanes, my hand-edit probe again (printf >> node inside the cmd: HEAD unmoved), the clean-node sanity, live `--line` once; then [merge-up] g3.8 #3 to SM.
2. DG3 gridcas sha: run grid-collapse.t.sh 53 ok at it (MAIN + non-repo cwd), forward [merge-up] g4.13.1 #3.
3. SM verdict on .19 (successor SM): a return = NEW DG3 commit, DG2 lane first for survivors.
4. DG3 .20 build: run box-wake.t.sh at it (cap loop kept), a pi probe, then SM.
Never invent goals; agi-signers retire = belam's GO.

## §4 Traps
| trap | rule |
|---|---|
| `git worktree add -b N PATH BASE` creates the branch then often fails | `git -C /data/work/agi branch N BASE` then `git worktree add PATH N`; scratch runs `--detach`, remove after |
| sends fail with "not inside an agi project" | I ran them from a removed worktree: `cd /var/lib/agi/director-general-1/t` first |
| links.py links ~3 min | nohup to a file, wait with an until loop on a .done marker |
| a nodes file may NEVER carry a full key header (the gate refuses the file forever) | spell it with dots; grep -c -e '-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----' every changed file = 0 |
| a follow-up is cut from the LIVE trunk after SM's [landed]; never cherry-pick a branch still in his gate | rename a landed node in place (same mint_id), never retire it |
| my accepted falsifier pairs were green on defects the mur found (agi-out D1, W-1) | run the pair at the sha, then one mutation or sibling-file probe; a green is not a proof |
| the rail counts ONLY engine.md (config:engine): fenced code <= 8,192 AND whole <= 12,288 | pieces in engine-grow/-root/-post/-wrap are expansion; measure `git show REV:.agi/nodes/.geometry/engine.md` |
| a bin edit passes the range's pytest (test_bin_help_smoke reddened g3.8 after my lanes-only run) and NO v5 uid has pytest or .env | name what I could not run in the [merge-up]; SM's gate runs pytest + anonymize |
| a helper that checks a precondition BEFORE a minute-long step and acts AFTER it (metrics_cell.py committed a hand edit made in between) | probe the gap: change the world inside the step (a cmd that edits the node) and watch HEAD |
| a host act is belam's own GO | never run one; forward as ONE line (command, before-state, rollback) |
| I mis-ruled twice by not checking my own record/bytes (the fenced count; the 7,100 ckpt bar vs a "split") | before a BAR or BYTES ruling: re-measure the RULED way (engine.md awk over the fences) and grep this card + git log of it for a standing ruling |
| judging a falsifier file: a green is not a proof | build 4-8 mutants of the REAL piece (splice into the engine-*.md section, or GROW_GATE=<piece file>) and run every lane file; name what stays green (equivalent / fails-safe) |
| running harnesses | grow-gate files: `GROW_GATE=<piece> sh file <sha>` (piece = first fence after the ### header; a sibling fence like ckpt is a 2nd block); agi-out-states: `AGI_OUT=<piece> sh file <sha>`; agi-outline: `env HOME=$(mktemp -d) sh file` AND host HOME; ab/keys: CEIL default now 6350 (7100 for the ckpt round, DG2 bumps) |

| a byte ruling measured on ONE of two paired lanes (said 'fits, 3 B spare'; agi-fresh said 809) | run BOTH lanes of a pair (agi-outline AND agi-fresh) before any 'fits'; list the harness files by `grep -l grow-gate`, never from memory |
| I ruled 'no unit change' on an ESTIMATE (~29 B) not a measure (DG3's was +18) and reversed | a bytes ruling carries the measured number or says 'unmeasured, provisional'; ask the builder for the measure before ruling against |
| an install forward ran only the NEW tree (A12 rolled back, 193 restart cycles of exit 127) | every install forward carries a run of the new step over an OLD/stale tree too: what a not-yet-merged post presents; agi-flush never merges a conflicting t |

## §5 Verification: links.py links 0 broken (SM re-checks at landing) · yaml parse every changed node · armour grep 0 · every return run at the sender's sha before forwarding

## §6 BANKED
- next belam: promote goal g7.16.1.11.17 horizon -> active (owner: "a lot more doable sooner"); install GOs (A12 unit re-install with the preconditions above, A10 ckpt on the hub with the first holding block cut by hand at each ring-signer rotation, agi-signers retires in the ring-install step, the land step: agi-land installed readable + ONE real land); the graph_metrics cron applies on belam's crons.py apply.
- alive/belam: crons.md node duplicate YAML key is silently last-wins for EVERY job (a crons.py loader change, not done: scope).
- trunk red test_exactly_one_template_heading (belam's thought-master row seeds): belam's.
- council: nothing open from me.
