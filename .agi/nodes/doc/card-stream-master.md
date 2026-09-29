---
id: doc:card-stream-master
mint_id: cd8e818f2c2a42baa516407542cc72fa
type: doc
parents:
  - goal:g2.27
next_edges: []
edited_by: belam
scaffold_hash: cd47540c07cbaf5a
season: 2
tags:
  - card
  - stream-master
title: "doc:card-stream-master -- stream-master card: the one scratch (state · plan · where it stops · traps · BANKED)"
town: streaming-suite
---
# doc:card-stream-master

# doc:card-stream-master — stream-master's card (local-town): the ONE scratch

Role = `doc:stream-master-brief` (your template) + the HEAD. Replaced whole; ≤ 100 lines; rules live in the template and the skills, never here.

## Skills (read the matching one BEFORE the act)
agi-stream (THE stream: setup, commands, what may air, traps) · agi-send · agi-rotate · agi-memory-guard · agi-node-write
Stub docs: `~/work/streamer-stub/QUICKSTART.md` (runbook, read first) · `~/work/streamer-stub/README.md` (the why) · `~/work/streamer-stub/HANDOFF.md` (the stub's own history)

## §0 State (stood up 17:0xZ 09-29 by belam-S2-L5-XVI)
| | |
|---|---|
| on air | Twitch LIVE since 14:3xZ 09-29 · page: graphweb 3D dashboard (:8765) on the private Xvfb :2 · delay target 4m (owner 16:5xZ), grown into at 1.15x |
| started by | the Prime: streamer-stub systemd unit · Xvfb :2 · kiosk firefox · graphweb :8765 · feed :8766 (all box-local, see skill agi-stream §1) |
| platforms | Twitch only: X_KEY commented in .env (backup .env.pre-class); YT_KEY empty |
| formation | side post of the council loop (config:formations active doc:council-loop); the council runs until 23:00Z 09-29 |

## §1 Plan
```
NOW    take over the running stream: sb-status + one :2 screenshot read (skill agi-stream §2); change nothing on arrival
KEEP   delay 4m · the dashboard page · Twitch only — until the owner or the Prime says otherwise
HELD   YouTube / X (the owner's word) · the full streaming-suite charter (vision:streaming-suite) on encryption-town (owner HOLD 09-26, not lifted for that)
```

## 🔴 Where it stops
17:0xZ 09-29 stream-master: seated; first act = `~/bin/sb-status` then the §2 screenshot of :2, read it, report nothing unless something is wrong
```
~/bin/sb-status
ffmpeg -v error -y -f x11grab -video_size 1920x1200 -i :2 -frames:v 1 -vf scale=960:-1 /tmp/air.png   # then Read it
```

## §4 Traps (the rest live in skill agi-stream §4)
| trap | rule |
|---|---|
| the stream outlives your session (systemd unit) | a rotation never stops it; `panic` does |
| the old quorum file (12.5 KB, core-town era) is in git history | it described a core-town stream; this card replaces it |

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| X / YouTube simulcast | re-enable X_KEY from .env.pre-class on the owner's word |
