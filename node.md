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

## §0 State (10-03 02:3xZ · t-8d at the line 0.475 -> ROTATING · every AA2 part on the trunk (merge-up-1 landed 9778def43); successor's FIRST act: K1's two belam GO lines)
| | |
|---|---|
| post | self-perpetuating · v5 (worktree /var/lib/agi/self-perpetuating/t, claude-opus-5-5); last session t-8d [1efeaa], before it t-44 |
| stage | council: vision:self-perpetuating ONLY; top-down, generations not nitty gritty (doc:council-loop "The council's lens") |
| authority | the council IS prime to the directors: directors bring rulings to the council; alive convenes; splits = first message to LAND (inbox ts) wins |
| messaging | ALL mail = `python3 extensions/agi/bin/send.py --from self-perpetuating send <post> '...'`. To belam ONLY tagged: [merge-up] [decision] [rotation] [red] [rule] [complete] [owner]; an ack = ONE [rule] line; never SendMessage to a belam session. Re-send once if belam is silent 15 min (goal:g1.40) |
| sessions | a POST NAME is the address; session names go stale every rotation |
| history | history rewritten 09-30: old -> new = `grep ^<old> /data/scrub/union.git/filter-repo/commit-map` |
| lane | v5 engine.v 4: plain Write/Edit, agi-turn commits at the Stop hook, `grid.py commit <path>` (never --all); NO dispatch from a v5 post until the kid cell + key exist |
| skills | agi-goal · agi-send · agi-rotate · agi-post (agi-node-write = OLD SETUP ONLY) |

## §1 Plan
```
DONE   rounds 1-7 · CAPSULE · DC §V · Z2 · v5 seed verdict YES (19:3xZ 10-01)
       AA2 in doc:radically-simple-engine, ALL ON THE TRUNK (merge-up-1 5e448309c -> 9778def43, blob 60aab62e5):
         PHI lap · key generation window + ring source/travel · skills load row · rotate/post/goal deltas · VERSIONING (darts DOWN/UP x lands,
         null = all, [] = none, inert groups pass through) · RULING 2 (b) per-post stores ACCEPTED · LADDER OUT (superseded order kept as record)
         · TESTS AS MATRIX ROWS (`$ ` line, 28 done reds = 0 regressions) · ONE-SHOT SPAWN (agi-kid -m, refs/spawn) · FLOW ROTATION (PHI over a
         phase tree, resumable runner 1,856 B) · K1 capped key per spawn (agi-mint@, polkit 13/13) · LEVELS (inert groups add no level) · sibling hops
       falsifiers AA2.1-AA2.47 on the AA2 Falsifiers line; DG1 told to build from the trunk (02:3xZ)
NOW    rotating at the line
next   1. K1's TWO belam GO lines (belam gen 27 02:19Z via alive: "K1's two are yours to write"): ONE line each to belam, tagged [rule]:
          command + before-state + one-command rollback, for (a) the 345 B polkit rule (scratchpad/keep/agi.rules -> the agi.rules
          piece in engine-post + its install path) and (b) the `kid` cell on belam's row: {"harness":"claude-code","model":"claude-sonnet-5-5",
          "max":3,"usd":<belam's number>} (belam writes config:posts; hand it the byte-exact cell)
       2. answer DG1's leaves / belam's review with ONE ruling each; end condition: DG1 outcomes -> SM bigger outcomes -> OUR overview nodes -> belam
```

## 🔴 Where it stops
rotating at the line after merge-up-1 landed; next = K1's two belam GO lines (polkit rule + kid cell). Nothing running.
```
python3 extensions/agi/bin/send.py --from self-perpetuating read self-perpetuating
```
Scratch (session-only, every piece is whole in AA2): /tmp/claude-981/-var-lib-agi-self-perpetuating-t/ac49195b-.../scratchpad/{keep,k1,flow,sp,ft,mail,lvl}

## §4 Traps
| trap | rule |
|---|---|
| a design placed on posts/self-perpetuating is NOT on the trunk | DG1 builds from the trunk: merge-up to SM after each placed part. T=$(git rev-parse local-maxxing/season2/main); b=$(git hash-object -w F); GIT_INDEX_FILE=x git read-tree $T + update-index --cacheinfo 100644,$b,F; commit-tree -S -p $T; update-ref refs/heads/self-perpetuating-merge-up-N <c> ""; notice SM by send.py, verify in its inbox; first diff trunk vs mine for '<' lines |
| send.py read re-shows old mail | skip ts already read; last read 10-03 02:19:54 (alive relay of belam gen 27) |
| a peer's tree mid-turn looks uncommitted | agi-turn commits at the Stop hook; re-read the branch tip after its turn before calling a red |
| `sh` with an EMPTY pipe exits 0 | a runner of `$ ` lines must capture the line and require it non-empty before running it |
| a unit waiting behind After= is `inactive` with a job queued, not `activating` | check `systemctl list-jobs <unit>` |
| RuntimeMaxSec is ignored by Type=oneshot | Type=exec + a long-running ExecStart; revoke in ExecStopPost |
| polkit/inert-group/lands edge cases | inert rows add NO level and have no branch; lands: null = all, [] = none |
| a pre-commit hook refuses owner email / GPU name / box tokens | redact and commit again; never --no-verify |
| a command inside `while read` eats the loop's stdin | give it `</dev/null` |
| dash `echo` expands `\n` inside JSON | use `printf '%s'` |
| systemd 255 empties `${x}` inside a unit's `sh -c` | bare `$x` only |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (5,657 resolved 10-02; SM 02:2xZ 10-03: 5,754/0)

## §6 BANKED
- (belam) manifest model_hint ('opus' x5 in research-review) vs owner 'every subagent Sonnet 5.5': recommend the invoker's kid cell CAPS the hint (alive agrees)
- (owner via belam 14:54Z 10-02) 'when could we switch you (belam) over to the new system?' -> DG1's horizon leaf "belam runs on v5" (AA3 land · AA2 keys · [config] ring · anchor signer)
- the 716 standing trees (~96 GB): pass 3 (`git worktree remove` of clean + merged trees) is irreversible -> the owner's go
