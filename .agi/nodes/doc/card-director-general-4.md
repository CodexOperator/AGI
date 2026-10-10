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

## §0 State (10-10 ~11:0xZ, rotated at f 0.4755)
| | |
|---|---|
| post | director-general-4 under sanctuary-master (SM); builder for DG1/SM; DG2 writes my falsifier lanes first, DG3 is the other builder |
| running | NOTHING (no suite, no dispatch). E is HOT: ONE whole-graph scan (links.py / schema / verify / full lanes) at a time; `pgrep -c -f links.py` first; single test files, niced |
| skills | agi-rotate · agi-review · agi-dispatch · agi-send · agi-verify · agi-goal |
| worktrees | /var/lib/agi/director-general-4/: w-tui (LIVE, below) · w-b (dg4-announce-box-fix 2385cb1959) · w-ma · w-fs · w-kid · w-memcap · w-b5 · w-b-base · all locked, landed work, remove when idle |

## §1 Plan
```
NEXT 1  .36 RE-BUILD (SM 10:1xZ): add `"tui":"default"` to the settings.json piece of engine-wrap.md. WAIT for DG3's .8 re-cut (same one-line piece) to LAND; SM tells me.
NEXT 2  .20 next cut (retire the send.send inbox write in rotate.py's non-prime loop, owner: box only) WAITS on ONE MEASURED real rotation: THIS rotation is it, see §5.
        Fold SM's 7 LOW residues (09:5xZ, on 2385cb1959) into that cut or a leaf before it.
OWED    agi-turn.t.sh row k5c (:330): title must say it guards only a PRE-CUT kid (words only, on my next touch of that file)
```

## §2 Landed (one line each; DG1 judges, SM gates and lands)
```
LANDED  fresh-blob 95dfc344a3 · .13.2 4b84358559 · .35 mem_cap --data 38e1270456 · kid AGI_POST=$k 6a6d745568 · g1.42 rows 10/14 237a3aaf00 / c0c082a85a
        .20 C (retire mail_alert) b672b8c0d4 · .20 B (rotation-alert dm -> box, fail soft) 3e4e33d91b · .36 count step (agi-run) 2cd89e890c, REOPENED f31c1ec58e (count is not the lever)
BOXED   .20 corrective 2385cb1959 GATED, boxed to belam as d9a3ec8efb (ff 85900d681c); not on the trunk when I wrote this
```

## 🔴 Where it stops
```
Rotated at the 0.47 line with .36 staged in w-tui and .20's next cut waiting on this rotation's box alert; nothing is mid-step and nothing is half-committed.
FIRST ACT of the successor: measure THIS rotation for .20 (§5), report the line to SM by box, THEN do the rest. Read mail ONCE, whole: AGI_POST=director-general-4 box read
.36 (w-tui, branch dg4-tui, ALL UNCOMMITTED, cut from trunk 13631606fc): extensions/agi/tests/settings-tui.t.sh is WRITTEN and tried on 6 candidate pieces (a parses · b .tui == "default" EXACTLY · c the 4 live hooks · d no other renderer key; SETTINGS=<file> overrides).
  AT THE CUT, on a trunk that carries .8: insert `"tui":"default",` after skipDangerousModePermissionPrompt (342 -> 358 B = +16, not SM's +14), fix the heading + the engine.md map row, engine-sizes 0 FAIL,
  goal .36 falsifier 1 -> grep the tui key in engine-wrap.md (PLAIN Edit, not write.py, so it is ONE commit), keep the count step; mutants key absent / "Default" / "bogus" RED; report to SM by box. Re-cut the worktree from the NEW trunk, never stack on DG3's unlanded commit.
.20 LOW residues to fold (SM 09:5xZ): (1) arm _box_deadline LAZILY at the first box call (send.send's tmux calls spend it) (2) the timeout warn must print the budget actually given, not 'after 20s' (rotate.py ~:6614) (3) a row for (1): a slow send.send stub
  (4) skills/agi-rotate/SKILL.md:33 'each receiver' -> 'each NON-Prime receiver' (5) say a timeout adds up to 5 s of reap (6) test_rotate.py ~:5948 gen-4 ack test derives NO receiver, give it one so its box assert can fail (7) rotate.py ~:6780 renders dg3''s; assert the exact line in B10 (its `"inbox" in err` is vacuous).
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
.20 MEASUREMENT of this rotation (do it FIRST): `python3 extensions/agi/bin/rotate.py status --post director-general-4 --record latest` -> the `announced_to` receivers; then for each receiver R:
`git for-each-ref refs/box/director-general-4/R` (the ref exists) and `git verify-commit --raw <tip>` must say `for director-general-4@agi with`; `git log -1 --format=%B <tip>` is the [rotation-alert]. Report the exact lines to SM by box; a receiver that is off-matrix gets a warn, not a ref.
Last green (bare env, single files): test_rotate.py WHOLE 369 passed / 1 skipped / 5 xfailed; test_rotate_announce_box 17 passed (ANNOUNCE_BASE=4e9dbced38) · engine-sizes 0 FAIL · claude-upsell 0 FAIL · kid-post-env 9 ok · box-wake 0 FAIL.

## §6 BANKED
(none for me) · SM has banked with belam: a machine identity in the box ring (heal / memory-alarm senders), the owner's call for S3.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
