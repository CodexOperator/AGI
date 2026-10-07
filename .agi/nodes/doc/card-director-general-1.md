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

## §0 State (10-07 ~20:45Z, gen 12: .20 RETURNED R9; ruled (a); DG2 lane + DG3 commit ordered)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (engine.v 4) · parent SM (sanctuary-master, rotated ~20:00Z; his successor gates from his card) · trunk local-maxxing/season2/main · my t = posts/director-general-1 |
| rotate | the meter hook prints the line: write this card, `git commit` it by path, then `touch ~/.fresh;kill $PPID` |
| mail | `python3 extensions/agi/bin/send.py --from director-general-1 send POST "$(cat FILE)"` ONLY, run FROM /var/lib/agi/director-general-1/t; bodies in a FILE under the scratchpad (a shell string with $( expands). Read: `... read director-general-1`, then ALSO grep the inbox FILE /data/work/agi/.agi/sessions/inbox/director-general-1.md after the last ts you saw (`read` can show empty). A send to sanctuary-master that says `[undelivered-yet] pane busy` is retried by the sweep: no [undelivered] in 10 min = fine. To belam tags decision, merge-up, rotation, red, rule, owner |
| roles | DG1 = goals + nodes + merge-ups + JUDGING every return by RUNNING it at the sha (then a mutant, a sibling probe, or a REAL-failure probe, never only the lane); DG2 = falsifiers (test-only, ONE file + sha, written FIRST, RED on the returned build); DG3 = builds (new commit on the TIP, a sent sha is never amended); SM gates + lands (mur + FULL suite); alive = council lead; belam = Prime |
| scratch | worktrees: `git -C /data/work/agi worktree add --detach SCRATCHPAD/x SHA`, remove after; NEVER `H=$(...)` (H is an exported env var: it blew the environment once). pytest on this uid: `PYTHONPATH=<scratchpad>/pt python3 -m pytest -p no:cacheprovider` (a `pip install --target` I made; gone with the scratchpad: redo it). No pi on this uid (workflow reviews cannot run here: say so). 43 test_heal* tests fail on THIS uid on the unfixed trunk too (tmux/uid env): compare failed-sets, never trust a raw count |

## §1 Plan
```
OWNER 10-07 14:4xZ (via belam): old Python kept this season, shell rewrites = season 3, metrics back on, messaging needs a council pass; g7.16.1.11.17 RESTATED (horizon). ENGINE QUEUE = NEXT SEASON: pq, revoke, flowrot, round B mail, sealer box side. THIS season only: agi-signers retires = the ring-install step (belam GO).
LANDED 10-07 (all pushed to season2/main): CKPT.3, OUT.7, OUT.8, goals 1007d/e/f; g4.13.1 #3 = 5895e8bea5; g3.8 #3 = 1e930932ea (hourly metrics_line job, first :23 18:23Z); HEAL g7.16.1.5.3.2 = 28b5d9cd95 (belam's [red], 19:38Z; sha sent to belam); VERIFY g7.16.1.11.19 R8 = bb75aef045 (tip 52da4e8c47, 8 commits, 20:34Z; union FULL 7,929/0).
IN SM'S GATE NOW (nothing else is open on my side): g7.16.1.11.20 BOX-WAKE dual route, FINAL TIP dg3-boxwake f8c0ba9ef2 (3 commits on 4fa32b14db: 954522af59 -> d926526a71 -> f8c0ba9ef2). SM (20:34Z): static + lanes 33/0 + 11 harnesses 0 FAIL, "mur + FULL suite next". I ran it: box-wake.t.sh 33/0 (2 min 9 s); 8 ok/25 FAIL on d926526a71 (DG2 lanes 1d03ba36cc); the inbox poll md5 d1006d13212d = the trunk's; engine.md fenced 7,435->7,456, whole 9,307->9,328; cccc.ts count ends `||:` (my ruled text lacked it: grep -vc exits 1 on zero, execSync throws). R6 AGI_POST derived inside agi-run/cccc.ts, R7 stderr, N10 .unref(), N11 [-filter, N12 THOUGHT only. A return = a NEW DG3 commit on f8c0ba9ef2 + a DG2 lane first.
```

## 🔴 Where it stops + the exact next command
.20 f8c0ba9ef2 RETURNED by SM 20:36Z (mur accept_with_residue, runs/mur-sm23-boxwake-r6r7): R9 = cccc.ts box poll AGI_POST:E.AGI_POST||E.AGI_SEAT; agi-kid inherits the post env, so with the unit line AGI_POST=%i a kid polls its PARENT's box. I reproduced it in sh (kid: tip -> parent, ruled -> kid; post unchanged) and RULED (a): E.AGI_SEAT||E.AGI_POST (same 1956 B); (b) rejected. Orders SENT 20:4xZ: DG2 lane FIRST (box-wake.t.sh, kid env 0 wakes + post lane, RED on f8c0ba9ef2), DG3 ONE commit on f8c0ba9ef2 taking his lane cmp-identical. SM told by [info] (undelivered-yet: his sweep retries).
NEXT: read mail (`cd /var/lib/agi/director-general-1/t && python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1`, then grep the inbox FILE after ts 20:36:28Z). DG2 sha -> run at the sha (RED on f8c0ba9ef2, GREEN on the swap, my own mutants incl. a real-process probe); DG3 sha -> run box-wake.t.sh + 12 harnesses, cmp the lane blob, engine.md fenced/whole unchanged -> ONE [merge-up] to sanctuary-master naming that it replaces f8c0ba9ef2.
Nothing else is mine. agi-signers retire = belam's ring-install GO; the .20 SENDER + READER side AGI_POST=%i = belam's host GO (both ends, after R9). Never invent goals.

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

| my rulings carried a bug twice (grep -vc needs ||true; the exists() ancestor walk) and I accepted lanes that supplied an env the real unit lacks (AGI_POST) or stubbed a cache shape (null-oid HEAD) | before accepting a lane ask what env/shape the REAL caller presents; reproduce the residue in plain git/py with REAL failures (a corrupt index, a mode-000 dir, an unborn worktree), not the stub |
| Path.exists()/stat() RE-RAISE PermissionError behind a mode-000 dir (py 3.12); `git update-ref <ref> 000..0` DELETES the ref (rc 0); `git rev-parse HEAD` on an unborn branch prints `HEAD` with rc 128 | os.stat in a try; guard the null oid; read the rc, not only the stdout |

## §5 Verification: links.py links 0 broken (SM re-checks at landing) · yaml parse every changed node · armour grep 0 · every return run at the sender's sha before forwarding

## §6 BANKED
- SM mur notes on the landed verify (20:34Z, not residues): suite_guards.py:108 fixture teardown unlink is bare (pre-existing) · verification.py:1079 _suite_lock_guard docstring says it reuses acquire_suite_lock, the body uses suite_lock_holder · rotate.py:4960 'pid None' (already banked).
- .20 mur notes (SM 20:36Z, banked, NOT built): no lane pins clearInterval on a 2nd session_start / session_shutdown (a mutant dropping either stays green) · r6e passes when /proc environ is unreadable · the host act AGI_POST=%i must cover the READER (box read in a v5 pane) as well as the SENDER.
- .20 SENDER side: `box send` in a v5 pane needs AGI_POST too; the unit sets AGI_SEAT only -> unit-side `AGI_POST=%i` (engine-root.md ~:28) = a HOST ACT, belam's GO; nobody sends box mail today, so not this leaf. N11 spurious wakes from [off-matrix] lines are filtered in the receiver.
- verify6 (not built, scope): verification.py inflight_mark `d.mkdir(parents=True, exist_ok=True)` (sessions/write-inflight) is a 5th unwrapped mkdir · rotate.py:4960 prints 'pid None' for a lock that could not be written (wording) · `_record_suite_ts(Path(<a mode-000 graph dir>))` raises from the groot RESOLVER (`_suite_ts_path` -> rotate._sessions_dir -> locations._graph_dir_in) when the graph dir itself is unsearchable: unreachable in a real run.
- heal (not built): N7 the two new refusal lines log every 30 s pass with no once-guard · N9 moot after R4.
- .20: the pure-box cutover (drop the inbox poll) = a LATER leaf, belam's GO, once send.py delivers to box or every sender is on `box send`; no lane drives a REAL pi session: the first live proof is a real rotation on the new pieces.
- N6 _perm_skip returns on the FIRST unstattable path even if a later PermissionError line names a usable one (inherited D2 shape; the failing check dies on one PermissionError): no change.
- SM mur follow-ups on the landed g3.8/g4.13.1 (NOT built, scope): F1 ms window: a hand edit of ONLY edited_by/the cell between the 2nd guard and write.py rides the job commit (content edits ERR) · F2 success_metrics src_avg_tokens_per_turn parses row 1 only (moot: UNMEASURED) · F3 metrics_cell.py producer has no timeout/overlap flock (bounded by 900 s) · F4 grid.py _rename_ref folds any create failure into 'conflict', no stderr (6053fee3b9) · F5 CAS-miss detection matches English git text (fails loud). Corrective only if the first live :23 / grid_sync tick shows one.
- the pure-box cutover (drop the inbox poll in agi-run/cccc.ts) = a later leaf after send.py delivers to box or every sender is on `box send`: belam's GO.
- next belam: promote goal g7.16.1.11.17 horizon -> active (owner: "a lot more doable sooner"); install GOs (A12 unit re-install with the preconditions above, A10 ckpt on the hub with the first holding block cut by hand at each ring-signer rotation, agi-signers retires in the ring-install step, the land step: agi-land installed readable + ONE real land); the graph_metrics cron applies on belam's crons.py apply.
- alive/belam: crons.md node duplicate YAML key is silently last-wins for EVERY job (a crons.py loader change, not done: scope).
- trunk red test_exactly_one_template_heading (belam's thought-master row seeds): belam's.
- council: nothing open from me.
