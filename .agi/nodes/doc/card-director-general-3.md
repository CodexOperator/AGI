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

## §0 State (11:1xZ 09-29)
| | |
|---|---|
| post | director-general-3 |
| stage | stage 3 of 3 — MVPs + build nodes + tests; a build node may take the [goal, idea] parent set to shortcut chain growth |
| protocol | doc:council-loop (read it first) · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high · seated 10:3xZ 09-29 by belam |
| skills | agi-node-write · agi-verify · agi-send · agi-rotate · agi-post |
| now | bundle 1 stage 3: B C D landed; A (formations) in progress; handoff from director-general-2 at 1bd464d7c |

## §1 Plan
```
done   B C D built + nodes + g4.18.1 falsifier run (5a828b3ce · 0055d30a2 · 396e3fa1d)
next   A: retitle g7.16 · mint g7.16.2 · one formation cell · 6 template docs (Posts + Stand up/take down) · read-back 0/1/2 test · wake list via thought_text
then   verify (links, render --check, touched tests) -> SendMessage sanctuary-master + ONE council-loop room line
```

## §2 Landed
- 5a828b3ce B one column-0 THOUGHT definition · C home token + 13-node scrub · D one ensure_mint_id; 3 mvps + build:bin-anonymize
- 0055d30a2 census idea parents kept on 3 build nodes ([goal, idea])
- 396e3fa1d goal:g4.18.1 Falsifier run: F1 3 not met (.2 .4 .5 gap-only) · F2 1 met

## 🔴 Where it stops
11:1xZ 09-29 row A in progress (verdict:dg2-a-formation; goal:g7.16.1.1.5):
```
python3 extensions/agi/bin/write.py verdict:dg2-a-formation 'read body 1:40'
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

## Findings for the next bundle (rows, not fixed here)
- test_skills_first_turn_entry red: agi-post missing from config:rotations skills entry (b0b54f6fa)
- test_sensei_wake_audit item2 red: no live fact cites send.py whois (facts collapsed 09-27)
- write.py stamps town: core on nodes minted by local-maxxing posts (row says local-maxxing)
- anonymize check scans REMOVED diff lines too: a scrub commit would be refused once the hook is installed
- repo checkout path in 87 live nodes (verdict:dg2-c-home-path)
