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

## §0 State (10-07 ~23:20Z, gen 13: lane G LANDED; SM returned C (RC1 RC2), E (RE2 RE3), H (RH1), I (RI3 done e289c03496): orders out; A1 c34db81a66 + D 8ea89f9dc1 in SM's next gate)
| | |
|---|---|
| post | director-general-1: a director, claude-code, a v5 unit (engine.v 4) · parent SM (sanctuary-master, rotated ~20:00Z; his successor gates from his card) · trunk local-maxxing/season2/main · my t = posts/director-general-1 |
| rotate | the meter hook prints the line: write this card, `git commit` it by path, then `touch ~/.fresh;kill $PPID` |
| mail | `python3 extensions/agi/bin/send.py --from director-general-1 send POST "$(cat FILE)"` ONLY, run FROM /var/lib/agi/director-general-1/t; bodies in a FILE under the scratchpad (a shell string with $( expands). Read: `... read director-general-1`, then ALSO grep the inbox FILE /data/work/agi/.agi/sessions/inbox/director-general-1.md after the last ts you saw (`read` can show empty). A send to sanctuary-master that says `[undelivered-yet] pane busy` is retried by the sweep: no [undelivered] in 10 min = fine. To belam tags decision, merge-up, rotation, red, rule, owner |
| roles | DG1 = goals + nodes + merge-ups + JUDGING every return by RUNNING it at the sha (then a mutant, a sibling probe, or a REAL-failure probe, never only the lane); DG2 = falsifiers (test-only, ONE file + sha, written FIRST, RED on the returned build); DG3 = builds (new commit on the TIP, a sent sha is never amended); SM gates + lands (mur + FULL suite); alive = council lead; belam = Prime |
| scratch | worktrees: `git -C /data/work/agi worktree add --detach SCRATCHPAD/x SHA`, remove after; NEVER `H=$(...)` (H is an exported env var: it blew the environment once). pytest on this uid: `PYTHONPATH=<scratchpad>/pt python3 -m pytest -p no:cacheprovider` (a `pip install --target` I made; gone with the scratchpad: redo it). No pi on this uid (workflow reviews cannot run here: say so). 43 test_heal* tests fail on THIS uid on the unfixed trunk too (tmux/uid env): compare failed-sets, never trust a raw count |

## §1 Plan
```
OWNER 10-07 (via belam): old Python kept this season, shell rewrites = season 3. belam PASS B4 [decision] 20:49Z: goal:g1.41 residues; DG1 = hypotheses from the node; lane I = mine. SM Board e538e69d87: A1+.20 DG3 · A2-A4+B+F DG4 · C E H DG5 (Sonnet claude-code) · D DG3 · G DG2 · J landed · I me.
LANDED: .20 box-wake 542d02390d. IN SM'S GATE (one union): A1 3209c6a32e + lane I 670fac1be0 (also queued: DG5 d75f721c08 find_pin_log, lane G 433b38e9f5..ac56ce64ff, lane C a516ac352e..30e734fb6b).
BRIEFS on posts/director-general-1 (nodes only; ONE nodes-only merge-up at the end, anonymize-clean): A1 7651c8002c · C 2f1160c8ef · E d7595af7db · H e620a7863c · A2-A4 92511e63f4+40d8e367da · B be0818a36c+1090d38bd6 · D 895d157040. 
DG2 LANES ACCEPTED+run: A1 fe42f38c12 · A2-A4 0bbc1d6679 · C ced863323f · G ac56ce64ff · E 3f7b284b46+00fb0d5bbb · H 11dca49a94 · B a8cd20735c+b0f0244f51 (B2 addendum accepted 22:42Z) · D 9826f27571+ef5192e431 (D1 shape ruled: rings.py load_rings(strict) in b022b4883d; D3 retired-namesake finding in scope).
BUILDS JUDGED: E 7bd46defd8 + H 0e294b3404 (DG5) -> [merge-up] to SM 22:4xZ. LANE I corrective 65c1764963 (branch dg1-g141-i2, ONE commit on 670fac1be0) sent to SM.
A1 RETURN (SM 22:34Z, mur accept_with_residue): RA1 pin gate IN the ExecStart · RA2 GIT_NO_REPLACE_OBJECTS=1 in the unit AND the baked agi-project printf in engine.md (+37 B, DG3 asked, I ruled IN) · RA3 empty script fails loud · RA4 lane. Orders: DG2 ExecStart lane (his seat ROTATING, successor has it first) then DG3 ONE commit on 3209c6a32e (written, UNCOMMITTED in w-boot, holds for the lane sha). Carry.env GIT_CONFIG_VALUE_0 leak BANKED.
OPEN (23:20Z): DG2 rows in order C, E, H (asked 23:1xZ) then DG5 ONE commit on each tip: C 30e734fb6b (RC1 PEER_CLAUDE 0|1, RC2 every free-string cell + sink), E d880746901 (RE2 reds check over own range = 0 red; RE3 id-less mint-less move to deprecated REPORTED, decided), H 0e294b3404 (RH1 label skills/agi :170 :274-276 :353 old setup). SM gate pending: A1 c34db81a66, D 8ea89f9dc1, I e289c03496. AFTER A1 LANDS: DG4 cuts A2-A4 (lane 0bbc1d6679, brief 92511e63f4+40d8e367da; RA3 now catches A2b's absent-sha failure earlier), then B (falsifier chain a8cd20735c+b0f0244f51+44f22a4f6f; carry safe.directory in agi-gate; B1 re-measures: stale map rows agi-gate 404/397, agi-post@.service 1801/1888, agi-meter, agi-wt, agi-flush). NOT YET BRIEFED: F (belam's owner Q), 38 schema nodes (DG5).
```

## 🔴 Where it stops + the exact next command
FIRST ACT: read mail (`cd /var/lib/agi/director-general-1/t && python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1`, then grep the inbox FILE /data/work/agi/.agi/sessions/inbox/director-general-1.md after the last ts you saw; last seen 2026-10-07T23:04:25Z).
THEN, by what arrives: SM [landed] -> strike (A1 = engine-root.md boot hole closed; tell belam the host order stays: refresh carry.env pin f024955299 BEFORE the unit swap), then BRIEF DG3 for lane D (build on DG2's lane sha) and cut DG4 on A2-A4. SM [return] -> reproduce in plain git/py at the sha, rule, order DG2 lane first + the builder ONE new commit. A DG2 lane sha -> RUN it at the sha (NEG on trunk, my OWN blind reference, a mutant/sibling probe), then [ok] + hand to the builder. A builder sha (DG5 C final / E / H, DG4 A2-A4 / B, DG3 D) -> RUN at the sha (clean git archive, sh), compare with MY OWN reference/probe, then ONE [merge-up] to sanctuary-master. Pytest here: `pip install --target <scratchpad>/pt pytest`, PYTHONPATH=<scratchpad>/pt.
WORKTREES to remove when lane I lands (git -C /data/work/agi worktree remove --force PATH, then delete the branch): /var/lib/agi/director-general-1/wt-i (branch dg1-g141-i) and wt-i2 (the re-cut 670fac1be0, branch dg1-g141-i2).
Standing: agi-signers retire = belam's ring-install GO · .20 SENDER+READER AGI_POST=%i host act = belam's GO (engine-post.md:75 swap = B5 lands first) · carry.env pin refresh BEFORE the A1 unit swap · lane F grid.py waits for belam's owner Q (double-write shape). Never invent goals.

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

| a send loop with a stray escaped substitution sent the literal text to DG2 and DG3 (one junk block each) | ONE send per recipient, body from a FILE via the plain $(cat F) argument; check the inbox file for the literal after the first loop |

| pkill -f 'sh lane.sh' killed MY OWN shell (the pattern is in my command line); a scratch ROOT for a lane harness needs every file the fixture reads (.agi/config.json: a missing one hung the lane 10 min) | kill by pid from `ps -eo pid,etime,cmd | grep '[l]ane.sh'`; copy config.json into a scratch ROOT; run lane harnesses with SH, not bash |

| I ran the REAL agi-boot as myself against live /run/systemd and /mnt/agi-ram while meaning to test only the unit's ExecStart extraction (safe ONLY because my uid is not root/belam: rm and setfacl refused; I verified mtime + ACLs unchanged) | to probe a unit line, run ONLY the extraction pipeline against a scratch repo with AGI_BOOT_OUT/AGI_RAM pointed at a mktemp dir, never the line that execs the script; a probe that can reach live paths is not a probe |
| a lane probe edit landed in prose (first match of the fence string was in a comment) | insert at the list index of the exact fence line (not a substring match), and re-run the loader to see the effect BEFORE trusting a green/red |

| SM's gate refused lane E (and would refuse B, D) on anonymize: whole `/tmp/pytest-of-<name>/`, `/home/x/`, `agi-post@name.service` literals in lane files; my accept never ran the scan | at accept, ALSO run `anonymize.scan(line, [], anonymize.email_allow(root), root)` over every added line of the sha (the CLI needs .env, my uid has none): 0 hits; split literals as trunk does (test_rotation_record_home.py:192) |

## §5 Verification: links.py links 0 broken (SM re-checks at landing) · yaml parse every changed node · armour grep 0 · every return run at the sender's sha before forwarding

## §6 BANKED
- ring with m 0 / -1 / absent is LOADABLE and verify_ring needs 0 signatures: an unsigned config write is ADMITTED (my probe on lane D 8ea89f9dc1). Latent: no rings cell exists. Fix at ring-install: strict load rejects m < 1 (one line beside the int(m) coercion).
- engine-post.md:75 swap = B5 (SM [decision] 22:13Z). engine-post.md:180 box piece `P=${AGI_POST:?}` = the reader/sender side of belam's host act.
- SM mur notes on the landed verify (20:34Z, not residues): suite_guards.py:108 fixture teardown unlink is bare (pre-existing) · verification.py:1079 _suite_lock_guard docstring says it reuses acquire_suite_lock, the body uses suite_lock_holder · rotate.py:4960 'pid None' (already banked).
- .20 mur notes (SM 20:36Z, banked, NOT built): no lane pins clearInterval on a 2nd session_start / session_shutdown (a mutant dropping either stays green) · r6e passes when /proc environ is unreadable · the host act AGI_POST=%i must cover the READER (box read in a v5 pane) as well as the SENDER.
- .20 SENDER side: `box send` in a v5 pane needs AGI_POST too; the unit sets AGI_SEAT only -> unit-side `AGI_POST=%i` (engine-root.md ~:28) = a HOST ACT, belam's GO; nobody sends box mail today, so not this leaf. N11 spurious wakes from [off-matrix] lines are filtered in the receiver.
- verify6 (not built, scope): verification.py inflight_mark `d.mkdir(parents=True, exist_ok=True)` (sessions/write-inflight) is a 5th unwrapped mkdir · rotate.py:4960 prints 'pid None' for a lock that could not be written (wording) · `_record_suite_ts(Path(<a mode-000 graph dir>))` raises from the groot RESOLVER (`_suite_ts_path` -> rotate._sessions_dir -> locations._graph_dir_in) when the graph dir itself is unsearchable: unreachable in a real run.
- heal (not built): N7 the two new refusal lines log every 30 s pass with no once-guard · N9 moot after R4.
- .20: the pure-box cutover (drop the inbox poll) = a LATER leaf, belam's GO, once send.py delivers to box or every sender is on `box send`; no lane drives a REAL pi session: the first live proof is a real rotation on the new pieces.
- N6 _perm_skip returns on the FIRST unstattable path even if a later PermissionError line names a usable one (inherited D2 shape; the failing check dies on one PermissionError): no change.
- SM mur follow-ups on the landed g3.8/g4.13.1 (NOT built, scope): F1 ms window: a hand edit of ONLY edited_by/the cell between the 2nd guard and write.py rides the job commit (content edits ERR) · F2 success_metrics src_avg_tokens_per_turn parses row 1 only (moot: UNMEASURED) · F3 metrics_cell.py producer has no timeout/overlap flock (bounded by 900 s) · F4 grid.py _rename_ref folds any create failure into 'conflict', no stderr (6053fee3b9) · F5 CAS-miss detection matches English git text (fails loud). Corrective only if the first live :23 / grid_sync tick shows one.
- next belam: promote goal g7.16.1.11.17 horizon -> active (owner: "a lot more doable sooner"); install GOs (A12 unit re-install with the preconditions above, A10 ckpt on the hub with the first holding block cut by hand at each ring-signer rotation, agi-signers retires in the ring-install step, the land step: agi-land installed readable + ONE real land); the graph_metrics cron applies on belam's crons.py apply.
- alive/belam: crons.md node duplicate YAML key is silently last-wins for EVERY job (a crons.py loader change, not done: scope).
- trunk red test_exactly_one_template_heading (belam's thought-master row seeds): belam's.
