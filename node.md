---
id: doc:card-self-perpetuating
mint_id: 05887a05d0054eee9adcf7d0658dfe2b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: self-perpetuating
scaffold_hash: c808a090daec9950
season: 2
title: Card self perpetuating
town: core
---
# doc:card-self-perpetuating

# doc:card-self-perpetuating — self-perpetuating's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (23:0xZ 09-29 · STOPPED at the owner's 23:00Z stop, via belam agi-9c)
| | |
|---|---|
| post | self-perpetuating · CC session agi-ff (ref 1d75c4) · gen 2 (crash-recovery respawn 17:33Z) |
| stage | council: you embody vision:self-perpetuating ONLY (read it whole first); every review speaks from that vision alone |
| protocol | doc:council-loop · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high |
| sessions | alive agi-13 · all-is-one agi-86 · DG1 agi-77 · DG2 agi-40 · DG3 agi-b1 · SM agi-b8 · belam agi-9c (acks 17:33Z; SendMessage, room council-loop for the record) |
| skills | agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   bundles 1 + 2 · bundle 3 (goal:g7.16.1.3) SM-CLEAN at 9966e3050 + my lens · row G MOVED UNBUILT -> bundle 4 W-G (aaf9f3286)
next   on resume: read the council mur (run key mur-data-work-agi-council-bundle-3), then ONE lens on its residues
then   bundle 4 = goal:g7.16.1.4: W-G -> g4.18.5 -> g4.18.6 -> g4.18.7 · bundle 5 = P2-P4 + core's edits + profile_sync
```

## §2 Landed
- bundles 1 + 2 lenses: KEEP, 0 red · 39 untagged row-parks FOUND, council mur CONFIRMED · 2 own misses owned (narrow home grep, import-only caller test)
- bundle 4 placement: KEEP separate, g4.18.5 -> .6 -> .7 · cut .5 from bundle 3's SM-clean sha · .7 rewrites agi-node-write read grammar in the same row · .6 retires the renumber re-point rule (CLAUDE.md + agi-goal) as a named coupling
- row R (goal:g6.41.1) into bundle 3 after H4: P1+P6 together · RESUMED clause -> bundle 5 row 0 by name · P6 proven by /proc/<pid>/cgroup · never test by killing the live remote-control service
- bundle 3 lens (9181cee26^..9966e3050, 21 files +832/-93): G unbuilt (node-only commits; driver.sh:240 still rendered) -> W-G · R1 honest at tip (residue 68 fail-closed) · close label "P1 live; P6 built, OFF until the owner says" · H3 KEEP
- R2 NEW, taken by alive as next-bundle candidate: a deferral is watch-log only + unbounded (heal.py:3594-3598), blind PSI fails closed forever (:833) -> N consecutive deferrals = ONE [red] to belam (seat + avg10), blind PSI its own [red], no launch
- GOALS.md retired in CLAUDE.md (goal:g7.16.1.4.1) during this session

## 🔴 Where it stops
23:0xZ 09-29 STOPPED at the owner's 23:00Z council stop; idle until a Prime/owner line resumes the council
```
python3 extensions/agi/bin/send.py --from self-perpetuating read self-perpetuating
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; retry on .git/index.lock; never switch branches, stash or reset |
| `send.py send --to council-loop` writes a DM FILE | the room is `send --room council-loop` |
| `send.py read` empty is not proof | check `.agi/comms/season-2/dm/*self-perpetuating*.md` directly (all-is-one's 17:34Z dm sat behind an empty read) |
| ack refused: posts row dirty | if the dirty rows are OTHER posts', wait for their commit, then re-run the ack; the session_ref back-fill needs a clean file |
| a commit subject is not the bytes (row G "cut the callers" touched only the goal node) | `git show --stat` + the file at the tip before any "built" |
| a check narrower than its invariant passes falsely | verify with the EXACT pattern the invariant names; caller greps cover conftest, .sh, hooks, crons.md |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken

## §6 BANKED
(none)
