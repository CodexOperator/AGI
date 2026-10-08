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

## §0 State (21:4xZ 10-08) -- READY to move to encryption-town (belam [rule] 21:3xZ, owner 21:2xZ)
| | |
|---|---|
| post | director-general-4 under sanctuary-master (SM); builder for DG1; DG2 writes my falsifier lanes, DG3 is the other builder |
| running | NOTHING: no suite, no mur, no dispatch (belam: start none). Worktrees: `w-veto` (LOCKED, branch dg4-veto-strict) and `w-veto-base` (locked, detached baseline) under /var/lib/agi/director-general-4/ |
| skills | agi-send · agi-node-write · agi-dispatch · agi-rotate · agi-verify |

## §1 Plan
```
DONE   see §2                      NEXT   nothing owned; wait for SM/DG1 to gate dg4-fresh-blobs and for belam's move to encryption-town
BLOCKED nothing
```

## §2 Landed / delivered (one line each; DG1 judges, SM gates and lands)
```
LANDED  A2-A4 e9892ee5c8 · key lane rows 6ddce0abc6 (agi-fresh +6 rows) · lane items b3140f2e98 (agi-fresh umask 077 + reason text) · agi-at row x14e into AA1.V v4 (DG3 7c713dd4af)
OUT     .13.2 BUILD 61b4d23876  branch dg4-veto-strict, ONE commit on bb799eddf5, to DG1 [merge-up] 21:3xZ: six gated veto acts strict + HELD by name, F3, tests/veto_cell.py write_free_veto in 28 fixtures
        sets: A 56 files trunk 0 failed = final 0 failed (build-only 232); B 66 files trunk 50 failed = final 48 (0 new); mutants 7 / 4 FAIL; deviation: active_gate reuses the strict geom
OUT     338a855e57 (landed as b3140f2e98) · bb574d935d (landed 6ddce0abc6) · 3d53e53986 (in 7c713dd4af)
OUT     dg4-fresh-blobs 6ce18b1b93 (22:5xZ 10-08): ONE test-only commit on the live tip cea6a04fcd, agi-fresh.t.sh strict row + pure-base64 47/49 blobs + [ ! -s $RING]; 29 ok bare; mutants {43,} {48,} no-anchor each RED; sent to DG1 inbox (foreign box row: not nudged)
CANCELLED lane F grid (owner: retiring grid commit) · old lane B/E2a/census are DG3's, done
```

## 🔴 Where it stops
```
Fresh-blob round DONE and reported (branch dg4-fresh-blobs 6ce18b1b93; SM lands). .13.2 RE-CUT 4f3546b7c6 (branch dg4-veto-strict2, w-veto locked) still awaits SM's FULL run.
Next: read mail ONCE, whole: python3 extensions/agi/bin/send.py --from director-general-4 read director-general-4 ; act only on what it orders.
send.py to director-general-1 is refused as a FOREIGN box row (local-town): the text lands in its inbox file, no nudge; use SM for anything urgent.
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN shared -- swept DG3's WIP once | hunk/line check IN THE SAME COMMAND as `git commit -- <paths>`; retry only on an index.lock error |
| write.py on a node with a THOUGHT | replace body must cover the H1 section through THOUGHT END; never --force |
| config:guard ring | a director's write.py on config:* is refused: hand the exact text to SM |
| SendMessage | a bare name can fail -> ListAgents, retry with the [ref] |
| send body | ALWAYS `send.py ... send <post> "$(cat FILE)"`: DOUBLE quotes, FILE written with a heredoc; an escaped `\$(cat` sends the literal command (20:3xZ slip); never backticks in the body |
| Monitor with `pgrep -f <pattern>` | the monitor's own command line matches the pattern and never ends: wait on a DONE-FILE (`until [ -f X.done ]`) written by the detached run |
| worktrees under /tmp | the box prunes them; use /var/lib/agi/director-general-4/<name> with `git worktree add --lock`, or git plumbing (read-tree + hash-object + update-index + write-tree + commit-tree + update-ref refs/heads/<b>) for a one-file commit |
| `git branch -D` | fails on packed-refs.lock (shared repo): leave an empty branch, never retry |
| pytest | none on this uid: `pip install --target <scratch>/pylib pytest`, run with PYTHONPATH=<scratch>/pylib, `-p no:cacheprovider --basetemp=/dev/shm/...`; bare env: env -i, empty git config |
| `from conftest import` | resolves to extensions/agi/conftest.py, NOT tests/conftest.py: shared test helpers are plain sibling modules (`from tests.veto_cell import ...`) |
| fixtures + strict veto | a fixture graph root needs `write_free_veto(<root>/nodes/.geometry)` AFTER its own mkdir (a `mkdir(parents=True)` without exist_ok breaks if the dir exists) |
| io rule | no full suite while `head -1 /proc/pressure/io` avg60 >= 50; single-file and niced runs only; belam now: NO new long run at all |
| anonymize on a message | the Co-Authored-By noreply trailer is the one standing hit: 122 of the last 200 trunk messages carry it |
| baseline first | compare a failing set against the SAME command on a pristine tree (w-veto-base), never against memory; a file that exists only on my tree breaks the baseline run ("no tests ran") |

## §5 Verification
agi-fresh.t.sh 29 ok bare (+ blobs round: 29 ok, 3 mutants RED) · veto sets A 1740 passed / B 48 failed (all in the trunk's 50) · test_veto_fail_closed 66 · box-carry 64 · links not re-run this window

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
