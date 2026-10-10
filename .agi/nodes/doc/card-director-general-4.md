---
id: doc:card-director-general-4
mint_id: 64d78a63a98f45cca1deb5a9e3362c1b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-4
scaffold_hash: 83e9e4c0ac970627
season: 2
tags:
  - card
  - director
  - director-general-4
title: Card director general 4
town: core
---
# doc:card-director-general-4

Role = the director template + the HEAD (`doc:unified-head`). This card is the ONE scratch: replaced whole, <= 100 lines; rules live in skills, progress on the town board.

## §0 State (10-10 ~10:3xZ, gen after the 0.4755 rotation)
| | |
|---|---|
| post | director-general-4 under sanctuary-master (SM); builder for DG1/SM; DG2 writes my falsifier lanes first, DG3 is the other builder |
| running | NOTHING. E is HOT: ONE whole-graph scan at a time; `pgrep -c -f links.py` first; single test files, niced |
| skills | agi-rotate · agi-review · agi-dispatch · agi-send · agi-verify · agi-goal |
| worktrees | /var/lib/agi/director-general-4/: w-res (LIVE: dg4-residues 23a8ceffc0) · w-tui (STAGED, uncommitted .36) · w-b w-ma w-fs w-kid w-memcap w-b5 w-b-base (locked, landed work, remove when idle) |

## §1 Plan
```
DONE    .20 measurement reported to SM (10:2xZ): my rotation went out by the HOOK line (touch ~/.fresh;kill), no rotate.py record, NO [rotation-alert] on any refs/box/director-general-4/*: cut B is still UNMEASURED; needs a rotation through `rotate.py rotate`. SM decides.
DONE    .20 7 LOW residues -> leaf dg4-residues f160158e99 (SM returned 23a8ceffc0: B12 shape fix, 1 decimal, comment), re-boxed 10:4xZ; SM runs test_rotate whole.
NEXT 1  .36 RE-BUILD in w-tui: WAIT for DG3's .8 (same one-line settings piece) to LAND on the trunk; SM tells me. Check: git grep skipDangerousModePermissionPrompt origin/local-maxxing/season2/main -- extensions/agi/
NEXT 2  .20 v5 PLACEMENT (belam ruled, SM 10:3xZ): cut B never runs on E (v5 rotates by the hook). BUILD in agi-run's .fresh branch (engine-wrap.md:23): BACKGROUNDED `timeout 20` fail-soft `box send <recv>` per receiver AS the post; receivers = config:rotations alerts (audit + edges[post] - silent - self) from the trunk, NO liveness filter. ROWS RED on mutants: (a) restart never waits on the send (b) unparseable alerts cell = no send + ONE warn, no agi-run crash (c) silent+self excluded; engine-sizes 0 FAIL. AFTER .36 (same file). MEASURE = first director restart after it lands: alert in MY box. Retire-the-inbox-write cut HELD.
OWED    agi-turn.t.sh row k5c (:330): title must say it guards only a PRE-CUT kid (words only, on my next touch of that file)
```

## §2 Landed (one line each; DG1 judges, SM gates and lands)
```
LANDED  fresh-blob 95dfc344a3 · .13.2 4b84358559 · .35 mem_cap --data 38e1270456 · kid AGI_POST=$k 6a6d745568 · g1.42 rows 10/14 237a3aaf00 / c0c082a85a
        .20 C b672b8c0d4 · .20 B 3e4e33d91b / 4412a659e8 (trunk 6d272246ec) · .20 corrective 2385cb1959 (boxed d9a3ec8efb) · .36 count step 2cd89e890c, REOPENED f31c1ec58e (count is not the lever)
BOXED   .20 residues f160158e99 GATED by SM (387 passed, verifier CLEAR), boxed to belam as f0c932f727. DOC NIT for the v5 cut: skills/agi-rotate/SKILL.md:33 'each NON-Prime receiver' is wrong: a ROTATING Prime sends no box message (its branch returns before the box loop); a Prime can RECEIVE one.
```

## 🔴 Where it stops
```
Residues leaf built and boxed to SM; waiting on SM's gate and on DG3's .8 landing; nothing is mid-step, nothing half-committed.
FIRST ACT: read mail ONCE, whole: AGI_POST=director-general-4 box read . Then the NEXT 1 check above; cut .36 only when it is on the trunk.
.36 (w-tui, branch dg4-tui, ALL UNCOMMITTED, cut from trunk 13631606fc): extensions/agi/tests/settings-tui.t.sh WRITTEN and tried on 6 candidate pieces.
  AT THE CUT, on a trunk that carries .8: insert `"tui":"default",` after skipDangerousModePermissionPrompt (342 -> 358 B = +16), fix the heading + the engine.md map row, engine-sizes 0 FAIL,
  goal .36 falsifier 1 -> grep the tui key in engine-wrap.md (PLAIN Edit, not write.py, so ONE commit), keep the count step; mutants key absent / "Default" / "bogus" RED; report to SM by box. Re-cut the worktree from the NEW trunk, never stack on DG3's unlanded commit.
```

## §4 Traps
| trap | rule |
|---|---|
| MAIL | BOX ONLY: read `AGI_POST=director-general-4 box read`; send `box send <post> < FILE` with AGI_POST set by hand; box prints nothing (a send is unconfirmed). No send.py send, no inbox writes |
| the out-line | the meter hook's line is `write the card, git commit it, touch ~/.fresh;kill $PPID`; skills/agi-rotate says `rotate.py rotate`: the HOOK is the live v5 line |
| MAIN shared | hunk/line check IN THE SAME COMMAND as `git commit -- <paths>`; retry only on an index.lock error |
| write.py | auto-COMMITS on the branch of the tree it runs in; on a cut branch it adds commits: use plain Edit for node text that must stay in ONE commit. A node with a THOUGHT: replace body covers H1 through THOUGHT END; never --force |
| config:guard ring | a director's write.py on config:* is refused: hand the exact text to SM |
| anonymize.py | cannot read MAIN .env on my uid: run against a scratch root with an empty .env (scratchpad/anon), diff + message, minus the standing noreply trailer; the secret-token class is SM's gate |
| pytest | importable here; `env -i PATH=/usr/bin:/bin:/usr/local/bin HOME=/tmp GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`, `-p no:cacheprovider --basetemp=/dev/shm/..`, nice -n 10; ONE suite at a time (verify-suite.lock): never mutate a file while one runs |
| conftest guard | it may wrap subprocess.Popen in a FUNCTION: never subclass it in a test; call through it |
| lane SRC= path | a lane that cds into a scratch repo needs an ABSOLUTE SRC=/PIECES= path |
| worktrees | under /var/lib/agi/director-general-4/<name> with `git worktree add --lock`, never /tmp; `git branch -D` fails on packed-refs.lock: leave the branch |
| baseline first | compare a failing set against the SAME command on a pristine tree, never memory |
| Monitor / waits | a `pgrep -f` or `pkill -f` pattern matches its own command line; wait on a DONE-FILE written by the detached run; never `sleep N && ...` chains |
| scoped lanes | a "no live name" grep gates the LIVE paths only (73 files name mail_alert in history); B5-style diff-scope rows are GATE-TIME (skip unless ANNOUNCE_BASE/_SRC set) |

## §5 Verification
Last green (bare env, single files): test_rotate_announce_box 18 passed / 1 skipped (B5 gate-time) · test_rotate -k "ack_gen1 or announce or box" 27 passed · B11 RED under an eager-arm mutant. Earlier: test_rotate.py WHOLE 369 passed (before the leaf) · engine-sizes 0 FAIL · claude-upsell 0 FAIL · kid-post-env 9 ok · box-wake 0 FAIL.

## §6 BANKED
(none for me) · SM has banked with belam: a machine identity in the box ring (heal / memory-alarm senders), the owner's call for S3.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
