---
name: agi-stream
description: >
  Run the sanctuary's live stream on local-town: streamer-stub (Twitch, delayed), the PRIVATE Xvfb display
  it grabs, what may appear on it (the 3D graph dashboard and the masked activity feed, never a terminal),
  switching pages, the delay, hold / cut / hard-off, and the traps paid for on 09-29. Use whenever a post
  starts, changes, pauses or stops the stream, or puts anything on the streamed display.
---

# agi-stream — what airs, and how to stop it

Source of truth: `~/work/streamer-stub/README.md` (the why) and `~/work/streamer-stub/QUICKSTART.md` (the runbook).
Read QUICKSTART before any go-live, pause or restart. Charter: `vision:streaming-suite` (the frame is the work itself;
a delay in front of it; every doxxing surface removed). This skill carries only the local-town setup and its traps.

## 1 · The setup (owner 09-29: "only livestream on twitch" · "show the dashboard" · "delay the stream by 4 minutes")
```
Xvfb :2  1920x1200  PRIVATE display (<home>/xvfb/root/usr/bin/Xvfb; no window manager, no terminals, no mouse)
  └─ kiosk firefox (profile ~/snap/firefox/common/stream-profile — the snap reads only $HOME)
       one page at a time:  graphweb :8765   extensions/agi/bin/graphweb.py serve --host 127.0.0.1 --port 8765  (3D graph + seats)
                            feed     :8766   <home>/classfeed/feed.py  (council room + commits, every line masked)
streamer-stub systemd user unit  →  x11grab :2  →  ring (out/ring, 2 s segments)  →  relay  →  Twitch
   .env: DISPLAY_SRC=:2 · X_KEY commented (Twitch only; the original is .env.pre-class) · YT_KEY empty
```
The real desktop `:1` holds the posts' terminals: it never airs.

## 2 · Commands
| want | do |
|---|---|
| state | `~/bin/sb-status` |
| delay | `~/bin/live 4m` · `live 0` = the 6 s floor (three segments) · higher is grown into at 1.15x, lower drops footage at once |
| hold (card on air, ring kept) | `~/bin/brb` → `~/bin/back` |
| cut (unaired footage destroyed) | `~/bin/retract` → `~/bin/back` |
| hard off | `~/bin/panic` then `systemctl --user stop streamer-stub` |
| start | `systemctl --user start streamer-stub` (NOT `bin/stream.sh --delay` from a Claude shell — §4) |
| fresh start, no old backlog | while on `brb`: `systemctl --user restart streamer-stub`, then `back` (QUICKSTART "fresh restart") |
| switch the page | stop the kiosk firefox by EXACT argv (§4), relaunch it on `:2` with the other URL |
| look at what airs | `ffmpeg -v error -y -f x11grab -video_size 1920x1200 -i :2 -frames:v 1 -vf scale=960:-1 /tmp/air.png` and READ the png |

## 3 · Before anything new goes on :2
- Scan what the page will show for home paths, addresses, keys, emails and host names (counts only, never print a value).
  Goal ids like `G15.1.2.3` look like addresses and are not; `unmask-` looks like `sk-` and is not.
- Take the §2 screenshot and read it. A terminal, a notification or a login page on `:2` = `retract` first, then fix.
- One publisher per key: another box (core-town) may hold the Twitch key; a conflict shows as the relay dropping.

## 4 · Traps paid for (09-29)
| trap | rule |
|---|---|
| `bin/stream.sh --delay` runs in the FOREGROUND when `INVOCATION_ID` is set (it is, in a Claude Code shell), so a timeout kills it | start and restart through `systemctl --user` only |
| a kill matcher over `/proc/*/cmdline` that looks for "firefox" or "stream-profile" matches your OWN Bash shell (its argv carries the command text) → exit 144 | match `os.path.basename(argv[0]) == "firefox"` AND `--kiosk` in argv |
| xdotool cannot focus a window on `:2` (no window manager) | never type into the kiosk: relaunch it on the new URL |
| `.env` is sourced AFTER the environment | a display or key change goes in `.env` (back it up first, mode 600); an env var is overwritten |
| a paused stub keeps its ring: `back` after a long pause airs old footage | fresh start (§2) when the source display changed |
| the feed's masks are regexes | a new kind of leak needs a new mask in feed.py before it can air |
