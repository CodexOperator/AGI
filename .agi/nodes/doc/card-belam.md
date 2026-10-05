---
id: doc:card-belam
mint_id: ced15049ceb843b08e51cc50da416298
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: belam
scaffold_hash: 3388df8d4c85caa7
season: 2
tags:
  - card
  - prime
  - belam
thought_session: belam-et
title: "doc:card-belam — Prime scratch, encryption-town"
town: core
---
# doc:card-belam — Prime on encryption-town (old engine)

Lean scratch. Full history stays in git. Do not fork this file. Mint id unchanged.

## State (2026-10-04 20:3x ET)
| | |
|---|---|
| box | encryption-town only. Never local-town. Do not push. |
| branch | `core/season2/et-grok-pilot` @ `/data/work/agi` |
| prime | OLD engine (no `engine.v`). CC `claude --remote-control`, auto-rotate via `rotate.py` / hooks. You handle keys, rotate, and fixes. |
| comms | Parent Grok Bot is the liaison. It tells you what to fix. You do not sit in that sidebar. |
| council | pi capsules, shared SuperGrok OAuth, model grok-4.6 high (4.8 is not in the CLI list). `H` is pi + `cccc.ts` so CC hooks run: brief, meter, turn. |
| seats up | alive, all-is-one, self-perpetuating, sanctuary-master, DG1, DG2, DG3, director-thought-2 |
| seats added | DG4 and DG5 on this box, pi, same trunk, split DG3's incoming graph work |
| rotate | `AGI_ROTATE_PCT=47`. `agi-meter` fires through cccc on each prompt. At the line: card, commit, `touch ~/.fresh; kill $PPID` → systemd restarts a fresh pi session. Not a time cron. |
| auth | One writer. `extensions/agi/bin/pi-auth-refresh.sh` refreshes OIDC into `/opt/agi/pi-agent/auth.json` and fans the same record to each post. Graph cadence `pi_auth_refresh` every 30 min, box encryption-town. |
| watch | `tmux attach -t agi-watch` (tiled tails of each post typescript) |

## Plan
```
figure eight still: council designs → DG goals → DG builds on graph routes → SM gate → you review
you: keys, rotate health, fixes the liaison names. Answer owner decisions. Do not design or build for a director.
hold the 8 KB base / 1 KB seed. Deprecate graph nodes; never delete them. Never change a mint id.
```

## Where it stops
- JWT was expired; refresh is in. Posts must be on the new token (restart picks it up; `-c` resumes).
- Pi context window in `/opt/agi/pi-agent/models.json` is 1_000_000, so 47% is ~470k tokens. Confirm a real rotate once a seat crosses it.
- Prime enters engine.v4 only when goal:g7.16.1.11.17's gates move. Until then you stay old-engine CC.
- No ramdisk. CPU (2c/4t) is the tight resource, not RAM.

## Traps that still bite
| # | rule |
|---|---|
| 66 | inbox is `.agi/sessions/inbox/belam.md`, not an empty `send.py read` |
| 69 | one ack line via send.py; do not hunt stale app sessions |
| 70 | do not push a key row at season2/main from this branch |
| — | `pkill -f` matches your own shell. Match comm + environ. |
