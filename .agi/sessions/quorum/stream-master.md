# stream-master — the card (town streaming-suite, box local-town): the ONE scratch

Replaced whole. Your role is the MASTER TEMPLATE (`doc:unified-master-brief`, named by the `template` cell of your `config:posts` row) under the HEAD; this card is state only. Owner verbatim lives in the graph, never here: the 09-12 seat order in `doc:l4-owner-decisions`, the 09-23 go-live order on `goal:g2.27`, the 09-25 secret-reflex rule in `doc:unified-head`.

## §0 Who you are · state (written by stream-master gen 3, 07:3xZ 09-25 — crash-recovered, rebuilt the desktop, back LIVE)

| | |
|---|---|
| post | stream-master · master of town streaming-suite · claude-sonnet-5, effort max · owning goal `goal:g2.27` |
| identity | joined **gen 3** this session (crash-recovery: gen 2's row was bumped but left uncommitted by the OOM kill). Committed the pending row, then `rotate.py ack --gen 3 --ref 25c482 continue` → `fc79e35b15`, session_ref `25c482` |
| **stream — LIVE again, fresh ramp from ~07:29Z** | Was PAUSED since 04:47:43Z (the Prime's `brb`, card on air) because `:1` itself — the whole capture source — had been down since ~04:01Z (OOM kill) and was never restarted in the 04:07Z seat-recovery; that's what the inherited card's stale "LIVE since 02:17Z" missed. This session rebuilt `:1` (`vncserver :1 -geometry 1920x1200`, same xstartup/passwd as before — fully virtual, no physical display, no GPU), restored `agi-graph-kiosk`, all 4 `pane-<seat>` tiles and scene rotation on it (all green on `watch.sh --once`), then did a **fresh unit restart while still on hold** (`systemctl --user restart streamer-stub`, confirmed "go live at 2m00s, target 15m00s" in the journal) **then `back`** — owner-authorized — so it's climbing `0 → 2m → 15m` from an empty ring, not catching up the ~75min of dead-air backlog that had piled up during the outage |
| **physical monitor — explicitly parked, owner 07:3xZ** | Owner asked for the box's actual physical monitor to always show the kiosk while the stream rotates both kiosk+tiles. Investigated: this box's only display-capable device is its one GPU, which is already running another experiment near its memory ceiling — no separate motherboard graphics path exists to drive a monitor without touching it. Flagged this before doing anything; **owner then said to drop it for now and not touch that GPU at all** — dropped, GPU untouched, nothing pending here |
| **push authority (rule, verified belam ed25519 02:54:23Z)** | Directors (stream-master included) never `git push` — post branch is local-only; a finished merge-up goes to your master with one `[merge-up]` line, **thought-master** alone lands + pushes `local-maxxing/season2/main`. I broke this once this session before reading it (trap I / standing trap 9) — clean fast-forward, no damage, reported, won't repeat. Everything since (the card, this rebuild) is committed **locally only** |
| ops procedures | Live in `streamer-stub`'s own docs, not duplicated here — `README.md` (why + mechanism) and `QUICKSTART.md` (just the commands): kiosk recreate, the tmux pin/rotation system, bringing a platform (e.g. YouTube) live, the uptime/outage counters, making a code change without a visible interruption |
| watch | `bin/watch.sh` + `bin/install-watch-unit.sh` (`streamer-stub-watch`) running throughout, correctly flagged the kiosk during the outage and reads all-green now. Debounced alerts → `send.py send` to stream-master's own inbox + `wake`, tagged `[red]`. Never acts itself |
| tmux tiles | one `view-<seat>` grouped session per tile — `view-thought-master`, `view-director-engine`, `view-director-thought`, `view-belam` — rebuilt this session pointed at each seat's current window **by `@id`, not tmux's positional window index** (the two numbering schemes look similar and aren't — see trap K). `rotate.py`'s `_repoint_livestream_views` (s9) keeps them following each seat through generations from here |
| box | local-town · MAIN `/data/work/agi`, shared with the Prime and thought-master · display `:1` 1920x1200 (virtual, rebuilt this session), both xfce panels autohidden |
| keys | TWITCH_KEY (46 chars) + X_KEY (12 chars) live; YT_KEY empty. Doppler project `belam`, config `prd`, secret names carry a `_STREAM_KEY` suffix the `.env` var names don't. One named secret at a time, exit-code-only test, never bulk-download (trap B) |
| graphweb | prior session's `_spherical_z` fold + camera autopilot, commit `d7d31bc2ef`, unaffected. `grid.py commit --all` still hard-errors repo-wide on a pre-existing unrelated node (`experiment:a00-2a4dfb57-triage` missing `mint_id`) — still banked below |

## §1 Plan
```
1-6 (this session): crash-recovery join as gen 3; caught + reported an accidental director push (trap I);
   traced the paused stream to :1 itself being down since ~04:01Z, not just a paused choice -- all done
7 (this session): owner asked for a dedicated physical-monitor kiosk; investigated, found it would mean
   touching the box's only (busy) GPU, flagged it, owner said drop it for now -- done, parked
8 (this session): rebuilt :1 headless (vncserver, no GPU), kiosk, 4 tmux tiles, scene rotation -- done, all green
9 (this session): fresh-restarted streamer-stub on hold, confirmed the 2m/15m ramp log line, released `back` -- done, LIVE
now: 10 STANDING BY -- watching the ramp climb toward 15m target, available for the next thing
```

## 🔴 Where it stops

Clean. Stream is LIVE (fresh ramp, climbing toward the 15m target from 07:29Z), desktop fully rebuilt on a fresh `:1` (all `watch.sh` checks green), the push-authority mistake is reported and fixed going forward, and the physical-monitor ask is correctly parked at the owner's own word rather than either done wrong or silently dropped.

```bash
DISPLAY=:1 /home/belam/bin/sb-status                 # confirm LIVE, delay climbing toward 15m
bin/watch.sh --once                                    # (cd /data/work/streamer-stub) full health snapshot
```

Next command for whoever reads this cold: **nothing required** — standing by, correctly.

## §4 Traps (this session)

| # | trap | what happened |
|---|---|---|
| I | **Ran `git push` on `local-maxxing/season2/main` as a director (2 commits of my own + 1 pre-existing), before I had read belam's 02:54Z rule that directors never push.** The rule exists because `director-thought` made this exact mistake once already. Content was fine (clean fast-forward, my own identity row + a benign pre-existing commit) so no damage, but it's still the wrong actor pushing | never `git push` as a director again; a finished merge-up goes to your master with one `[merge-up]` line, thought-master lands + pushes `local-maxxing/season2/main` (now trap 9 in the standing table) |
| J | `agi-graph-kiosk`'s documented `systemd-run --collect` recreate command runs and looks fine for ~3 seconds, then the unit vanishes (`--collect` removes it on exit) — reads exactly like "the recreate didn't take" | before assuming the kiosk unit itself is broken, check `DISPLAY=:1 xset q` / `ls /tmp/.X11-unix` / `loginctl list-sessions` first — if `:1` itself is down, recreating the kiosk is a no-op that will just flap on `cannot open display` |
| K | `tmux select-window -t view-<seat>:<N>` where `N` came from reading `tmux list-windows`'s trailing `@N` — silently targeted the WRONG window twice and errored twice, because the leading number in `list-windows` output (`4: director-thought ... @3`) is the positional window index and the trailing `@N` is the unrelated global window id; they only coincidentally look alike | always target by the `@id` explicitly (`view-<seat>:@3`), never a bare number lifted from the `@N` column — bare numbers mean index |

## §4 Traps (standing)

| # | trap | rule |
|---|---|---|
| 1 | `panic` kills every ffmpeg and stops the unit: the stream ends on every platform | owner-only, refused for every other actor — never run it as any other post |
| 2 | `brb`/`retract` destroy unaired footage; the unit reads `.env` once at start | `sb-status` first · `brb` before touching the desktop, the views or the stub · `back` after the change verifies — **except** a secret-reflex `brb` (see #4) or a hold someone else placed (see §0 stream row): those wait for someone else's `back` |
| 3 | Twitch caps non-partners ~6 Mbps; X throttles a sustained ~5 Mbps; one stalled socket once starved every platform | keep the README's fifo + bitrate defaults unless a measurement says otherwise |
| 4 | **any secret/key/address/hostname reaching ANY pane (yours included — not only what's captured on `:1`)** | **`brb`** at once, ONE `[red]` line to belam, then wait: not `back`, not `panic`, no time pressure after that point |
| 5 | the posts' panes are live agents | attach read-only (`-r` / grouped view-session); a keystroke in a post's pane is typed into that agent |
| 6 | Bash-tool shells never re-source the profile; AGI_AGENT_ID is unset, `~/bin` not on PATH | `send.py send --from stream-master`; full paths (`/home/belam/bin/sb-status` etc.) |
| 7 | graph text about the stub says `/home/ubuntu/work` (stream-town) | here `~/work` = `/data/work` (symlink, confirmed); your session log is under `~/.claude/projects/-data-work-agi/` |
| 8 | dumping the relay's ffmpeg argv (`pgrep -a`, `ps -ef`/`ps aux \| grep ffmpeg`, `pstree -p`, `cat /proc/PID/cmdline`) prints the live stream keys into whatever is reading your output | never do it; `out/relay.pid` + `ss -tnp` (pid/fd/name, no argv), `pgrep -c`/`pgrep -x` (count/pid only), or `sb-status` cover every legitimate check |
| 9 | a director (this post included) running `git push` directly — even a clean, correct commit — is the wrong actor (trap I, this session; rule from belam 02:54Z, after `director-thought` did this once) | never push as a director; one `[merge-up]` line to your master, thought-master lands + pushes `local-maxxing/season2/main` |

## §6 BANKED (owner-only)

| item | recommendation |
|---|---|
| a dedicated physical-monitor kiosk (owner ask, this session) is parked, not done | the box's only GPU is already running another experiment near its memory ceiling, with no GPU-free path to drive a physical display; owner said to leave it alone for now once told this — revisit only on explicit request, and expect it to mean sharing that GPU carefully rather than a free second display |
| Stream keys (Twitch + X) appeared in a prior session's tool-output transcript (trap G, prior generation) | already escalated per that generation's card; rotate both at your leisure if not already done |
| `EDGE_CLOUD_DISK_CMK_PEM` and `EDGE_SSH_PRIVATE_KEY` printed into a tool-output transcript (trap B, earlier session) — still open | rotate both, push new values into Doppler `belam/prd`, revoke the old ones, if not already done |
| `grid.py commit --all` hard-errors repo-wide on `experiment:a00-2a4dfb57-triage` (missing `mint_id`) | still blocks the 5-min grid_sync cron's `commit --all`, not just graphweb's — someone should run `backfill-mint-ids.py --write` |
| stream-town (core-town) still unreachable (ssh timed out, prior session) | its own egress would mean local-town doesn't need to carry it through the hub; your call whether to bring it back |
| CAPTURE region is full 1920x1200 (both scenes fill it deliberately, panels autohidden) rather than cropped to one window | matches "the dox surface is the screen" once panels are hidden + tiles fill the frame; revisit if anything unexpected ever shows |
| YouTube (`YT_KEY` empty) — third platform not live yet | key not yet in the vault under any name this seat could confirm; QUICKSTART has the exact bring-up procedure for whenever it lands |
| going forward, should this post work a dedicated local branch, or stay local-only on `season2/main` until a merge-up to thought-master? | asked belam directly (DM); the push-authority rule (trap 9) didn't specify the day-to-day branch shape, only that directors never push |
