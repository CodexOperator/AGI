# plan-master design facts — 2026-10-06 (ET tip `085383152` read-only)

**Status:** ABSORB into captive residue. Do **not** invent a poller. A+B v6 LOCK unchanged.

## 1. Instant capsule wake already in geometry
- `engine-root.md` `### agi-carry@.path` — PathChanged on `/var/lib/agi/%i/g.git/refs/box/%i`, runs `box-carry` (**inotify, not poll**).
- **0 units projected** on ET (`agi-carry*` empty).
- Owner riff (10:29) = **install/project `agi-carry`**, then point raw-shell mail-wake at it instead of a 5s `sleep` loop.
- SoT for instant mail/ping wake: **project agi-carry + wire mail-wake to PathChanged**, not minute/5s poll.

## 2. mail-wake captive y/N already live
- Live for **plan-master** + **thought-master**.
- `wk()` prints `[unwired]` because `/opt/agi/bin/agi-wake` missing (known **W1 / g5.34.6.2** gap).

## 3. `### orient` captive `ok` does NOT exist yet
- Orient today: clears / dumps / exits. **No** captive `ok` gate.
- Owner ask (10:29 #2) is **NEW** — **not** covered by existing g5.34.7.* (incl. g5.34.7.2 clear+reprint).
- Needs **design leaf** (under .7 or .8) → council ONE → SM gate → DG.
- SM minting **goal:g5.34.7.6** (design) for council pen: post-dump captive exact `ok` before shell continues.

## Non-goals
Inventing a poller · claiming g5.34.7.2 already covers orient-ok · solidifying sleep-loop mail-wake as SoT
