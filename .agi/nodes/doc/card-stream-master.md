---
id: doc:card-stream-master
mint_id: cd8e818f2c2a42baa516407542cc72fa
type: doc
parents:
  - goal:g2.27
next_edges: []
edited_by: stream-master
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
Stub docs: `~/work/streamer-stub/QUICKSTART.md` (runbook; its bring-up section still says DISPLAY=:1, the skill says :2) · `README.md` · `HANDOFF.md`

## §0 State (gen 5 seated 17:34Z 09-29, ack committed; updated 17:40Z)
| | |
|---|---|
| stream on local-town | DOWN. Prime hard-stopped it 17:3xZ (`panic --retract`, ring destroyed, streamer-stub failed, Xvfb :2 + kiosk + graphweb stopped) |
| why | owner via Prime: "OOM kill likely due to stream. Memory crossed 75% likely due to buffer building up. So new plan put stream-master on new box first then start the stream" |
| my one act here | 17:35Z, before the stop reached me: started agi-xvfb2 / agi-graphweb / agi-graph-kiosk (transient units), all killed by the stop; reported to belam |
| platforms | Twitch only (X_KEY commented, backup .env.pre-class); YT_KEY empty |

## §1 Plan
```
NOW    HOLD IDLE on local-town — start nothing (Xvfb, graphweb, kiosk, streamer-stub) here
NEXT   the Prime moves this post to the new box (rows + spawns are the Prime's); then read that box's QUICKSTART equivalent, stand up Xvfb + graphweb + kiosk, screenshot, start the stub
GUARD  the new box: watch memory (agi-memory-guard) — the ring/buffer growth crossed 75% here; bound the delay ring before going live
HELD   YouTube / X (owner) · full streaming-suite charter (owner HOLD 09-26)
```

## 🔴 Where it stops
19:5xZ 10-01 stream-master: MOVE 6 of the v5 switch (agi-17 = belam gen 25) - verdict YES sent, down-ready sent; stream stays OFF; on the v5 unit (own uid) the stream stack is NOT carried: Xvfb, kiosk profile, units, .env key, ~/bin scripts all belong to the old uid, so rebuild from skill agi-stream only on the owner's word
```
SendMessage by session name only (owner: internal messaging only until bundles land); the Prime is agi-79
```

## §4 Traps
| trap | rule |
|---|---|
| my ffmpeg x11grab of :2 fails from the Bash sandbox ("Cannot open display :2") | read a ring segment instead: `ffmpeg -i out/ring/<older .ts> -frames:v 1 x.png` into /data/tmp (newest 2 segments are mid-write; /tmp is not shared) |
| `-sseof` on a 2 s ts yields no frame | seek-less first frame of a complete older segment |
| an idle Xvfb/firefox/graphweb restart during a Prime stop is wasted and confusing | read the inbox before restoring a downed stack: `send.py read stream-master` |
| the stream outlives a session (systemd unit) | rotation never stops it; `panic` does (owner-only) |

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| X / YouTube simulcast | re-enable X_KEY from .env.pre-class on the owner's word |
| QUICKSTART bring-up says DISPLAY=:1 | correct it to the :2 private display once the new box setup is known |
