---
id: idea:g7161146-crons-py-retirement
mint_id: 72b16abba2664aa1a376b93ed0d29b26
type: idea
parents:
  - goal:g7.16.1.11.46
next_edges: []
model: claude-opus-5-5
role: director
scaffold_hash: b89f45c7811825a1
scale: small
season: 3
status: open
tags: []
title: (b) retire crons.py and its config:crons projection, its FIRST step a reader census (every caller and reader, each with its replacement) before any cut
town: core
---

# idea:g7161146-crons-py-retirement

## OWNER 2026-10-26 05:10:58Z (c:d4ac22e3b15f), verbatim (chat to belam, item 3; card-belam:271, atom c2)
"Sure maybe we can retire Crons py as well soon if possible"

## OWNER 2026-11-01 10:0xZ (c:a3b39b982eae), verbatim (chat to belam, item 1 of the owner's walk of belam's card §6, on grid_stale; belam's [owner-a] 9eeb9ddb66 on refs/box/belam/sanctuary-master)
"1. Yes but I thought we're doing away with crons py."

## Idea
Retire crons.py (and the config:crons projection it applies) once nothing reads it. The owner said it on 10-26 and again on 11-01 (both above). belam's same message: the retirement "has not started; the owner expects it, so it is a candidate leaf".
FIRST STEP, before any cut: a READER CENSUS (the seat_status shape): every caller of crons.py and every reader of config:crons on the trunk and on the host: grid_sync's `;` chain (CLAUDE.md: crons.py apply re-run every 5 min), branch_push, the board commit job under another uid (`crons.py apply --sudo`), stall_watch's own kill-switch line, crons_live's kill switch, CLAUDE.md's lines, the skills that name it, and the tests. Each row: the reader, what it reads, and what replaces it. The census decides whether a leaf exists: a cut leaves no reader without its replacement.
What would make it a leaf: the census on the trunk with every row's replacement named, and the council's word.
Placed by the council 3/3 (alive [decision] 07:29:02Z 11-05 (III)(b); all-is-one 10:19:03Z, self-perpetuating 10:21:11Z 11-01); minted 11-09 on SM's [place] 08:55Z (alive's red on itself 08:54:05Z: never minted).
