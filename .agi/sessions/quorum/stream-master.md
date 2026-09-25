# stream-master — the card (town streaming-suite, box local-town): the ONE scratch

Replaced whole. Your role is the MASTER TEMPLATE (`doc:unified-master-brief`, named by the `template` cell of your `config:posts` row) under the HEAD; this card is state only. Owner verbatim lives in the graph, never here: the 09-12 seat order in `doc:l4-owner-decisions`, the 09-23 go-live order on `goal:g2.27`, the 09-25 secret-reflex rule in `doc:unified-head`.

## §0 Who you are · state (written by stream-master gen 4, 22:4xZ 09-25 — crash-recovered after a box reboot cycle; stream found fully down, not relit yet)

| | |
|---|---|
| post | stream-master · master of town streaming-suite · claude-sonnet-5, effort max · owning goal `goal:g2.27` |
| identity | joined **gen 4** this session. Same crash-recovery shape as gen 2→3: gen 3's own rotate-self had already bumped this row to generation 4 (session_ref/session_id/session_name cleared) but never committed it. Committed the pending row (`4a457664a1`), then `rotate.py ack --seat stream-master --gen 4 --ref cb6dc3 continue` → `87513b0b44`, session_ref `cb6dc3` |
| **stream — DOWN, not the "LIVE, climbing to 15m" the inherited gen-3 card said** | That card was written ~07:3xZ and went stale: the box rebooted at least twice since (21:45Z and 22:19Z, visible in other seats' commits this window), which drops `:1` and the three transient units by design (`agi-graphweb`/`agi-graph-kiosk`/`agi-scene-rotate` — none registered at all right now) and left `streamer-stub.service` itself `loaded/disabled/inactive (dead)`. `sb-status`: relay not running, 3 stale pids, ring holding 463 segments (~926s, ~233MB) that never aired. **Owner asked only to set the delay this session — have NOT rebuilt the desktop or gone back live on Twitch/X without checking first**, since that's a bigger, public-facing action than a config value |
| **delay target — set to 4m, per owner ask this session** | `bin/live.sh 4m`: wrote `out/delay` (a flag file, survives restarts by design, no unit restart needed). Applied at once (4m < the stale on-disk 15m50s). Whichever session next brings the relay up will target 4m, not the old 15m, whether that's me later this session or a successor |
| push authority (unchanged, standing trap 9) | Directors never `git push`. Only local commits this session: the row bump (`4a457664a1`) and the ack's own row write (`87513b0b44`) |
| ops procedures | Live in `streamer-stub`'s own docs, not duplicated here — `README.md` (why + mechanism) and `QUICKSTART.md` (just the commands) |
| box | local-town · MAIN `/data/work/agi`, shared with the Prime and thought-master · display `:1` currently **down** (no VNC session; confirmed via `systemctl`/watch) |
| keys | Not touched this session; per the last-known card, TWITCH_KEY + X_KEY live, YT_KEY empty, Doppler project `belam`/`prd` — unverified fresh this session |

## §1 Plan
```
1 (this session): recover seat identity as gen 4 -- commit the pending row bump, then ack -- done
2 (this session): owner asked to set stream delay to 4 minutes -- done (out/delay, applied at once,
   independent of whether the relay is currently running)
3 (this session): checked actual state instead of trusting the inherited (stale) card -- found the
   whole stack down (desktop + streamer-stub unit) from a box reboot cycle after the card was written
4 (this session): reported the down state to the owner and asked before doing a full rebuild + going
   back live on real platforms, rather than assuming -- awaiting answer
now: 5 STANDING BY for the owner's go-ahead on the rebuild
```

## 🔴 Where it stops

Identity taken cleanly (gen 4), delay target set to 4m exactly as asked. Stream itself is down (post-reboot, desktop + unit both need rebuilding) — flagged to the owner rather than unilaterally relighting three public platforms; waiting on their answer before touching the desktop or `streamer-stub.service`.

```bash
cd /data/work/streamer-stub && bin/sb-status                 # confirm still down / relit
systemctl --user status streamer-stub agi-graphweb agi-graph-kiosk agi-scene-rotate --no-pager
```

Next command for whoever reads this cold: if the owner has said go, follow QUICKSTART "Bring the desktop up" (graphweb → kiosk → scene → tiles → watch, in that order) then `bin/stream.sh --delay`; if not yet answered, nothing further until they do.

## §4 Traps (this session)

(none yet)

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
