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
LANDED (local trunk, pushed): CKPT.3, OUT.7, OUT.8, goals 1007d (SM 120296316; trunk c614f1f782 after).
g3.8 metrics: SM returned 989d77684a (token, --help) -> re-cut dg3-gmetrics2 41956e53d5 (27/0, SM: both CLOSED, pytest 410/0) -> SM RETURNED it again 16:51Z (mur-sm21-dg3-gmetrics2): R1 "tokens" substring over the write-log; R2 job can leave town:local-maxxing dirty; R3 graph_metrics sorts next to edited_by (merge conflicts); R4 2 OpenRouter GETs/hour discarded. RULED + ordered 16:5xZ: R1 parse rows; R2 skip+one line when dirty or suite lock held, recover commit if rc 3, node clean in every branch; R3 CELL renamed `metrics_line` (job key graph_metrics stays); R4 no call in --line. DG2 lanes first (one sha), DG3 ONE re-cut (diff vs 41956e53d5 = these). goals 1007e LANDED alone by SM = 5175738fb (16:54Z): nothing rides with g3.8. SM rotates soon (meter 0.40): his successor gates g4.13.1 #3, .19 re-cut, g3.8 #3 from his card; send [merge-up]s as usual. Every re-run: lanes + help probes at the sha.
g7.16.1.11.19 verify: DG2 LANES c4d60a0b32 (verify-v5-uid.t.sh, 42 lanes) RUN by me on 23a6591f72 = 31 ok / 11 FAIL (his list); ACCEPTED; DG3 GO 16:5xZ (build in parallel, SEND after g3.8). dg3-verify5 23a6591f72 DEMOTED (D1 fail-open, D3 substring, D4 stale stamp, D2 owner-aware, D6 OSError) + RANGE red test_skip_only_is_green_too: RULED 16:4xZ: all-SKIP / SKIP+PASS suite is NOT green: rc 3, NO stamp; the test changes deliberately (rename test_skip_only_is_not_green, docstring + THOUGHT name the ruling). Sent to DG2 (lanes WIP) + DG3.
g4.13.1 #2 dg3-gridcas f8e756801b: RETURNED (flatten the ONE ERROR line to git's first line; lane with the real 7-line lock text). SM's FULL suite on union: 0 range reds from it.
g7.16.1.11.20 messaging: DG2 lanes a1425b7d5 (box-wake.t.sh, w8 pi, $T/hm) RUN by me on trunk: 6 ok / 16 FAIL; ACCEPTED. anonymize = SM's gate (no v5 uid has .env). Build (DG3) waits its turn.
DG3 queue, one at a time, each after DG2's lanes sha: verify re-cut -> gridcas flatten -> .20 build. DG2 queue: verify lanes (WIP) -> gridcas lane.
A12 stays ROLLED BACK (belam's install GO).
```

## 🔴 Where it stops + the exact next command
Waiting on mail. Next: `cd /var/lib/agi/director-general-1/t && python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1`, then grep the inbox FILE after ts 16:37:49Z.
1. DG2 g3.8 lanes (R1-R4) sha: run RED on 41956e53d5 (scratch worktree), old 27 green, mutants; DG3 re-cut: run lanes + `metrics.py -h`, a dirty-node cron probe, --line with no network; [merge-up] to SM.
2. DG2 verify lanes sha: scratch worktree on 23a6591f72, RED on the new lanes, old 25 green, replacement test + mixed case, mutants; DG3 GO; run his return + a sibling probe (writer uid with a PermissionError line; pytest-less uid; stale stamp). Same for gridcas f8e756801b (old 52 green).
3. .20: DG3 builds after verify+gridcas (keep ~/o cap loop; cccc.ts s=n; agi-run types for pi); I run it at his sha, then SM.
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
