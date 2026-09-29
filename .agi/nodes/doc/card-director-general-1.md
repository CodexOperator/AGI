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

# doc:card-director-general-1 — director-general-1's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (23:00Z 09-29 — STOPPED on the owner's 23:00Z stop ("Keep working till 7pm"), relayed by the council; re-seated 17:3xZ after the crash, ack gen 2 · session_ref 80bf37)
| | |
|---|---|
| post | director-general-1 |
| stage | RESUMED 23:4xZ (owner: "Restart council including DG5 stand up") · DG1 = goals + hypotheses for S4 (bundle 4), S6 (g7.16.1.6 write form), S7 (g7.16.1.7 spawn/rotate); NOT in room directors (belam 23:5xZ: DG3/4/5 only) · WAITING on alive's placement handoff for .6/.7 (both horizon, assigned to the council) · order when placed: S6 machinery leaves (DG3) -> S7 (DG5) -> S6 fill-in (DG4) · NEW LOOP (belam 23:5xZ): after DG2's MVP-vs-hypotheses pass, DG1 checks BUILD nodes vs goals -> correctives as nested subgoals -> no residue -> OUTCOME node per goal (parent = the goal) -> SM. Asked DG2 to hand rows one at a time. Prep 00:0xZ, read-only falsifier greps HOLD for W-G, W0, W1a, W1b, W2a (shape guard removed) -- tests pending DG2. Stop ~04:00Z |
| protocol | doc:council-loop · goal:g7.16.1 |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high |
| skills | agi-goal · agi-node-write · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   bundles 1 + 2 · bundle 3 stage 1 (9181cee26) + row R (11b2de165; R1 v3 b2d946498 grouped cutover) · bundle 3 CLOSED 1f39ffb1c
done   bundle 4 stage 1 (db3e22e55) · heading_level fix (68f23e0f6) · W-G 6 callers (521334b6b)
done   re-scope 1 (68d4c8504) · re-scope 2 (d4a186957) · W0 falsifier (45771a9e1) · W-G build line + horizon leaf g7.16.1.4.1.1 (d1de2e804; council: bundle 5, RETIRE, 99e0f3580)
done   belam mint [decision] 22:1xZ applied (7cf590f0d): g4.18.6.4.1 UNHELD, every W2 gate = "is a node's mint_id"
done   NEW LOOP 00:xZ: outcomes FINALIZED for bundles 1-3 (367d53349 + bundle-2 adoption): goal:g7.16.1.1 closed (4 leaves), goal:g7.16.1.3 12 leaves closed (2 falsifiers restated to HOME_PATH_RE), outcome:council-bundle-2 adopted (.2.9 moved to .7); W0 closed; SM told -> bigger_outcome
next   DG2 hands rows one at a time (W-G, W1a, W1b, W2a pending its MVP pass) -> build vs goal -> correctives as nested subgoals -> bundle-4 OUTCOME when SM clears 98-105 · .6/.7 leaves when alive places them · STOP ~04:00Z
blocked none
```

## §2 Landed — bundle 4 (goal:g7.16.1.4, base 1f39ffb1c)
| row | leaves | state |
|---|---|---|
| input | g7.16.1.4.3 | DG2 measure |
| W-G | g7.16.1.4.1 (+ .1.1 horizon, bundle 5 retire) | BUILT (41107692f, 254f58ef7), active until SM re-review clean |
| W0 | g7.16.1.4.2 | BUILT (82fce8a34) |
| W1 | g4.18.5.1 · .2 · .3 | .2 landed (write.py self-commits) |
| W2 | g4.18.6.1 · .2.1 · .2.2 · .3.1-.3 · .4 · .4.1 · .4.2 · .5 | re-scoped twice; .4.1 unheld (option a) |
| W3 | g4.18.7.1 · .2 · .3 (one row, ceiling 125) | pending |
Superseded, kept as evidence: hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup · hypothesis:every-link-reader-resolves-mint-ids.

## 🔴 Where it stops
23:00Z 09-29: stopped, idle, nothing in flight. My council-room lines may sit uncommitted beside other posts' lines (never commit theirs). Next act on wake:
```
python3 extensions/agi/bin/send.py --from director-general-1 read director-general-1
tail -30 .agi/comms/season-2/room/council-loop.md
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| write.py now COMMITS each write itself (W1b landed) | under the suite lock it writes the file, refuses its commit, and exits 0: check `git status` after a write and commit by path once the lock clears |
| a commit under .agi/sessions/verify-suite.lock (d1de2e804, 21:5xZ, self-reported to alive) | gate EVERY commit: `[ -e .agi/sessions/verify-suite.lock ] \&\& { echo LOCKED; exit 1; }; git commit ...` -- printing the lock is not stopping on it |
| `git ls-files` hides untracked nodes | a crashed seat's mints are untracked: `git ls-files --others` before re-minting |
| rotate.py ack refuses while posts.md is dirty | the recovery respawn commits the rows within seconds; retry, never commit its rows |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| `send.py read <self>` without --from resolves to 'unknown' | always `send.py --from director-general-1 read director-general-1` |
| the handoff may land only in the room | `tail .agi/comms/season-2/room/council-loop.md` at wake |
| `anonymize.py check FILE` refuses a positional | `check --diff-file FILE` |
| a negative grep over .agi/nodes hits the nodes that QUOTE its pattern (bundle 3 H3; bundle 4 W0 hit its own title, 45771a9e1) | exclude the quoting nodes or anchor the pattern; run the falsifier once before committing the leaf. H3 anchor: anchor `· triage: parked: formation g[0-9.]+ \|$` (39 rows, 5 carriers) |
| a goal minted without heading_level (DG2 [red] 20:4xZ, fixed 68f23e0f6) | `--set heading_level=<id segment count>` on every goal create; the render hard-fails without it and reds every closeout |
| a count or claim copied into every leaf of a row | measure it once per row with its own command; a wrong shared Measured line (W2: 8654, no walk, links gates parents) was wrong in 5 leaves at once |
| GOALS.md is retired (owner 17:3xZ) | never render it; goals are read from their nodes |
| moving a live process tree into a scope (R1 cutover, measured 18:4xZ on dummies) | AttachProcessesToUnit needs a Delegate=yes target; a moved parent leaves its children: move EVERY pid; probe with sleep dummies only, never tmux / a post / the RC service |

## §5 Verification: `links.py links` 0 broken · anonymize ok on each diff

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
