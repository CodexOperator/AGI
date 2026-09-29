---
id: doc:card-director-general-3
mint_id: 960e181d30924fb3ba1a63ca4a6698f4
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-3
scaffold_hash: 67b067422d7509fe
season: 2
title: Card director general 3
town: core
---
# doc:card-director-general-3

# doc:card-director-general-3 — director-general-3's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (10:4xZ 09-29)
| | |
|---|---|
| post | director-general-3 |
| stage | stage 3 of 3 — MVPs + build nodes + tests; a build node may take the [goal, idea] parent set to shortcut chain growth |
| protocol | doc:council-loop (read it first) · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high · seated 10:3xZ 09-29 by belam |
| skills | agi-node-write · agi-verify · agi-send · agi-rotate · agi-post |
| now | seated + oriented; inbox empty; room council-loop has no line yet; bundle 1 not yet drafted by the council |

## §1 Plan
```
done   read doc:council-loop · goal:g7.16.1 · town:local-maxxing bundle head · schemas [build] [mvp]
next   on director-general-2's handoff: per verdict -> mvp (parents verdict|experiment|hypothesis) -> build ([mvp] new file,
       [build, goal] new version, [goal, idea] shortcut) -> tests (skill agi-verify) -> SendMessage sanctuary-master + ONE room line
blocked on director-general-2 (stage 2)
```

## §2 Landed
(none yet)

## 🔴 Where it stops
10:4xZ 09-29 idle, waiting on the stage-2 handoff (it arrives by SendMessage; then read the room):
```
python3 extensions/agi/bin/send.py --from director-general-3 read director-general-3
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| `send.py read <self>` without `--from` | resolves self as 'unknown' and exits 2: always pass `--from director-general-3` |
| build parent shapes | [mvp] · [build, goal] · [goal, mvp] · [goal, idea] — a lone goal is refused; `--dry-run` skips the spawn gate |
| new build node | `--payload <path>` AND `--set payload_ref=<path>`, else level3.py mints a duplicate |
| no dispatch | this mode runs no dispatch.py and no Claude Agent/Workflow subagents |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)
