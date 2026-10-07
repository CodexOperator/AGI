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
PRIORITY 18:3xZ (SM [order], belam [red] 18:27Z, it HOLDS the season2/main merge; outranks verify6 R2 + the .20 dual route, both stay QUEUED): goal:g7.16.1.5.3.2 = heal.py sweep reads a FAILED git status as clean. Confirmed in the bytes at trunk c7d2f98f56: :1905 `status_lines, _ = _git(status)` drops the rc -> an UNMERGED tree: needs_archive, dirty=[], _sweep_archive pins HEAD only, `worktree remove --force` (:2011) drops uncommitted bytes. :1882 rev-parse rc dropped too and is NOT already safe (head "" + failed status = empty `want`, returns None). Goal minted (node-only leaf under complete g7.16.1.5.3): LANDED alone by SM = 6bdaf7a00a (cut the heal work from it; he gates the merge-up with the full rail and sends belam the sha). Route: DG2 pytest lanes FIRST (f1 failed status unmerged dirty, f2 clean/merged, f3 rev-parse, f4 sweep goes on, controls c1-c3; RED on c7d2f98f56) -> DG3 ONE heal.py commit + build-node THOUGHT -> I run + the QUICK-FIX REVIEW workflow (skill agi-workflow, by name, on pi) -> [merge-up] to SM (he gates full rail + sends belam the landing sha). Orders sent 18:4xZ.
OWNER 10-07 14:4xZ (via belam): old Python kept this season, shell rewrites = season 3, metrics back on, messaging needs a council pass; g7.16.1.11.17 RESTATED (horizon).
ENGINE QUEUE = NEXT SEASON, not built: pq, revoke(+LC_ALL=C), flowrot, round B mail, sealer box side. THIS season only: agi-signers retires = the ring-install step (belam GO).
LANDED (local trunk, pushed): CKPT.3, OUT.7, OUT.8, goals 1007d (120296316) + 1007e (5175738fb).
SM rotates (meter 0.40): his successor gates from his card; send [merge-up]s as usual. SM 17:00Z: FULL suite on the g3.8 union ad08961a4 = 7,914/0.
.19 VERIFY 17:3xZ: SM RETURNED verify6 0c6fc2d9a3 (mur-sm22: D1-D6 + (a) MET, 623/0 pytest) for R1 = _write_state :889 swallows OSError for ANY owner (loud->silent); RULED: route via _io_failed (own dir ERROR rc 2), N1 test header '2. SKIP-only is NOT green', N2 _perm_skip needs os.path.exists; DG2 lanes 4dd2c1cf89 RUN by me on 0c6fc2d9a3 = 43 ok / 2 FAIL (d2d d6e); DG2 found _IO_ERRORS.clear() at :2381 AFTER run_level wipes the baseline error -> move before (accepted); N2 REFINED: vanished = os.stat FileNotFoundError, PermissionError (under a mode-000 dir) stays SKIP; DG2 adds d2e, DG3 builds (46 lanes). Was: dg3-verify6 0c6fc2d9a3 (trunk 5f672d11e5) RUN by me: lanes 42/0 (c4d60a0b32 blob-identical), both rotate.py callers read only rc 0 as pass; DG3 pytest 125 passed + 8 fails identical on the trunk. [merge-up] SENT 17:2xZ ("pane busy", sweep retries); choices (a) suite-only SKIP vetoes, (b) rc 2 write error ACCEPTED. The skip-only test renamed test_skip_only_is_not_green (my 16:39Z ruling).
LANDED 17:5xZ by SM (pushed): g4.13.1 #3 dg3-gridcas2 b00c1db1fb = 5895e8bea5; g3.8 #3 dg3-gmetrics2 0ee6c275a5 = 1e930932ea (union 36e1bf2c30: FULL 7,915/0, mur accept). LIVE watch is SM's: grid_sync */5 tick (new grid.py) + crons.py apply installs graph_metrics, first :23 at 18:23Z (cell metrics_line on town:local-maxxing, belam writes).
.20 messaging: dg3-boxwake 954522af59 RETURNED by me (SM asked who sends box mail): `box send` is post-side only, send.py writes ONLY the inbox file, nobody sends box mail -> dropping the inbox poll orphans every wake. MY MISS (lanes s1/s2 encoded the full removal). Re-cut = DUAL ROUTE (inbox poll as on the trunk + box n poll; each types its OWN line); pure-box cutover = a LATER leaf with belam's GO. DG2 lanes first (s1 inverts to a control), DG3 after the verify narrowing. Not forwarded.
.19 verify6 a159c558c6 RETURNED by SM 18:0xZ (mur final: all MET) for R2: mkdir outside the try at verification.py :886 _write_state and :1283 _record_suite_ts (+ MY find :1040 suite-lock acquire) -> traceback not the named skip/ERROR. RULED: both mkdirs inside the try -> _io_failed, :1040 returns (None, None); N4 stamp only when _IO_ERRORS empty (rc!=0 run certifies nothing, stale stamp retracted); N5 l8 comment fix (DG2); N6 banked. DG2 lanes d6g d6h d6i first, DG3 ONE new commit on a159c558c6, then .20 dual route. SM trunk now 2a8007c3c3; his FULL suite on the verify union running (18:01Z).
A12 stays ROLLED BACK (belam's install GO).
```

## 🔴 Where it stops + the exact next command
Waiting on mail. Next: `cd /var/lib/agi/director-general-1/t && python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1`, then grep the inbox FILE after ts 17:53:10Z.
0. verify6 R2: DG2 lanes 29ad3d5bbe RUN by me on a159c558c6 = 50 ok / 4 FAIL (d6g1 d6g2 d6h d6i); DG3 GO after heal (mkdirs in try, _io_failed nearest-existing-ancestor, stamp needs not _IO_ERRORS, :1040 optional).
0. HEAL RED FIRST: DG2 lanes sha -> scratch worktree at c7d2f98f56, `git show SHA:<test>` over it, pytest (throwaway pip --target) RED count = his; DG3 sha: lanes 0 FAIL + test_heal*.py; my sibling probes (a real worktree: failing status via a git shim on PATH; rev-parse fail with a live gitdir); `read agi-workflow` then the quick-fix review; [merge-up] SM.
1. DG2 lanes (d6g d6h d6i + the l8 comment): RED on a159c558c6 (scratch worktree, `git show SHA:...verify-v5-uid.t.sh` over it), the 49 stay; DG3 new commit: lanes 0 FAIL, my sibling probes (a 555 parent: ERROR rc 2 / root parent: skip; EISDIR baseline + green suite: rc 2 and NO stamp); [merge-up] to SM (tip, whole range).
2. DG2 dual-route lanes sha -> RED on 954522af59; DG3 dual-route build -> I run box-wake.t.sh at it + a probe: ONE inbox append and ONE box mail each wake once with their OWN line, the cap loop untouched, bytes measured -> [merge-up] .20 to SM.
3. SM's first live :23 (18:23Z) and grid_sync tick: if F1-F5 (BANKED §6) bite, they become correctives.
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
- N6 _perm_skip returns on the FIRST unstattable path even if a later PermissionError line names a usable one (inherited D2 shape; the failing check dies on one PermissionError): no change.
- SM mur follow-ups on the landed g3.8/g4.13.1 (NOT built, scope): F1 ms window: a hand edit of ONLY edited_by/the cell between the 2nd guard and write.py rides the job commit (content edits ERR) · F2 success_metrics src_avg_tokens_per_turn parses row 1 only (moot: UNMEASURED) · F3 metrics_cell.py producer has no timeout/overlap flock (bounded by 900 s) · F4 grid.py _rename_ref folds any create failure into 'conflict', no stderr (6053fee3b9) · F5 CAS-miss detection matches English git text (fails loud). Corrective only if the first live :23 / grid_sync tick shows one.
- the pure-box cutover (drop the inbox poll in agi-run/cccc.ts) = a later leaf after send.py delivers to box or every sender is on `box send`: belam's GO.
- next belam: promote goal g7.16.1.11.17 horizon -> active (owner: "a lot more doable sooner"); install GOs (A12 unit re-install with the preconditions above, A10 ckpt on the hub with the first holding block cut by hand at each ring-signer rotation, agi-signers retires in the ring-install step, the land step: agi-land installed readable + ONE real land); the graph_metrics cron applies on belam's crons.py apply.
- alive/belam: crons.md node duplicate YAML key is silently last-wins for EVERY job (a crons.py loader change, not done: scope).
- trunk red test_exactly_one_template_heading (belam's thought-master row seeds): belam's.
- council: nothing open from me.
