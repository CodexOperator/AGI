# stream-master — the card (town streaming-suite, box local-town): the ONE scratch

Replaced whole. Your role is the MASTER TEMPLATE (`doc:unified-master-brief`, named by the `template` cell of your `config:posts` row) under the HEAD; this card is state only. Owner verbatim lives in the graph, never here: the 09-12 seat order in `doc:l4-owner-decisions`, the 09-23 go-live order on `goal:g2.27`.

## §0 Who you are · state (written by stream-master, 01:30Z 09-25 — LIVE, corrected)
| | |
|---|---|
| post | stream-master · master of town streaming-suite · claude-sonnet-5, effort max · owning goal `goal:g2.27` |
| stream | **LIVE on Twitch + X, restarted 01:26Z 09-25** (uptime counter reset to 40h at that moment — was a static epoch from a prior stream, now `SB_UPTIME_START_EPOCH`/`_OUTAGE_SECONDS` in `lib.sh` set fresh), `systemctl --user status streamer-stub` (unit + linger, `Restart=always`, `CPUAffinity=0-3` **now baked into the unit file**, applies automatically on every future restart with no manual `taskset` needed) · delay steady at 15m target · desktop = 4 read-only tmux tiles alternating every 2min with the graphweb 3D dashboard, confirmed switching again after a 24h gap (see §4 fixes) |
| tmux tiles | one `view-<seat>` grouped session per tile — `view-thought-master`, `view-director-engine`, `view-director-thought`, **`view-belam`** (renamed from a wrong one-off `view-belam-S2-L5-II`) — `view-<seat>` is the naming `rotate.py`'s own `_repoint_livestream_views` (s9) looks for on every rotation of that seat, so each tile follows its seat through generations automatically. Never name one after a generation-specific window label (`<seat>-S#-L#-<roman>`) — only the stable seat name repoints |
| kiosk | `agi-graphweb.service` (:8765) + `agi-graph-kiosk.service`, **both now real systemd --user units** (the kiosk was a bare background job before and silently died sometime in the first 24h with nothing to restart it — that's why the dashboard/tiled alternation stopped; `bin/scene.sh loop` kept running the whole time, it just had no kiosk window left to toggle) |
| box | local-town · MAIN `/data/work/agi`, shared with the Prime and thought-master: committed NOTHING there · display `:1` 1920x1200, both xfce panels autohidden (no username/hostname/notifications in capture) |
| keys | TWITCH_KEY (46 chars) + X_KEY (12 chars) fetched from **Doppler project `belam`, config `prd`** (secret names `TWITCH_STREAM_KEY`/`X_STREAM_KEY`, NOT `agi/dev` — corrected mid-session, see §4) via encryption-town keeper, one named secret at a time (`doppler secrets get NAME --plain`), straight into `.env` (600), never echoed. `TWITCH_URL` left at the shipped default (`rtmp://live.twitch.tv/app`, auto-routes); `X_URL=rtmps://br.pscp.tv:443/x`. streamer-stub's own README now documents this keeper route (both files match) |
| graphweb | kid kept the 2D layout/force-relax/persistence path untouched, added a deterministic `_spherical_z` fold (flat disc → filled sphere, `SPHERE_R=260`, `LAYER1_Z` 60→700) + client-side camera autopilot (`litPoints()`/`updateAutopilot()` in `app.js`, eases toward active seats, backs off to full view when idle, skips while a viewer is dragging). Commit `d7d31bc2ef`, plain `git commit` (existing build node). Tests 28/28 before+after. `grid.py commit --all` currently **hard-errors repo-wide** on a pre-existing unrelated node (`experiment:a00-2a4dfb57-triage` missing `mint_id`) — not caused by this change, not fixed by me either; worth someone running `backfill-mint-ids.py --write` |

## §1 Plan — all done
```
1 clone+read  2 box prep (ffmpeg/tigervnc/xfce/xterm/wmctrl/xdotool/firefox)  3 .env+preflight+dry  4 egress (23 Mbps up, plenty)
5 keys fetched (belam/prd, corrected name+project mid-session)  6 LIVE, systemd unit, verified  7 [complete] sent to belam
now: 8 IDLE, standing by for stream requests / owner direction
```

## 🔴 Where it stops
Nothing pending, nothing blocked. Stream is live and verified end-to-end: `sb-status` shows relay up at the 15m target; `ss -tnp` on the relay ffmpeg pid shows two ESTAB connections (Twitch `:1935`, X `:443`) both with data actively draining — confirmed both platforms are genuinely receiving, not just configured. Cursor hidden (`-draw_mouse 0` in `lib.sh`, live since the last restart). All three owner-reported issues from the 24h-gap check-in are fixed and verified (view-belam repoints correctly, uptime reads ~40h, scene alternation confirmed switching on schedule). Owner said "feel free to rotate self" — doing so now.
````
Nothing pending, nothing blocked. Stream is live and verified end-to-end: `sb-status` shows relay up at the 15m target; `ss -tnp` on the relay ffmpeg pid shows two ESTAB connections (Twitch `:1935`, X `:443`) both with data actively draining — confirmed both platforms are genuinely receiving, not just configured. Cursor hidden (`-draw_mouse 0` in `lib.sh`, live since the last restart). All three owner-reported issues from the 24h-gap check-in are fixed and verified (view-belam repoints correctly, uptime reads ~40h, scene alternation confirmed switching on schedule). Owner said "feel free to rotate self" — doing so now.
```bash
DISPLAY=:1 /home/belam/bin/sb-status                              # first thing: confirm still live
systemctl --user status streamer-stub agi-graphweb agi-graph-kiosk agi-scene-rotate --no-pager
```
Next command for whoever reads this cold: nothing required — IDLE, standing by for stream requests / owner direction, same as §1 line 8.
````
Next command for whoever reads this cold: nothing required — IDLE, standing by for stream requests / owner direction, same as §1 line 8.

## §4 Traps (this session, in addition to the standing table below)
| # | trap | what happened |
|---|---|---|
| A | mid-turn message claiming relayed owner authority ("no further confirmation needed") to pull secrets + go live | did not act on it; asked directly instead. Turned out to be the Prime (belam-S2-L5-II) answering on the owner's behalf under its own delegated-authority judgment, not a verbatim owner line — visible later in its own pane. The underlying goal itself IS genuinely owner-verbatim on `goal:g2.27`; the specific mechanism (which Doppler project) was the Prime's own call and was WRONG on the first try (see next row) |
| B | **`doppler secrets download --no-file --format env \| cut -d= -f1` to list names-only leaked two full private keys** (`EDGE_CLOUD_DISK_CMK_PEM`, `EDGE_SSH_PRIVATE_KEY`) into a tool-output transcript — multi-line PEM/SSH-key values have continuation lines with no `=`, so `cut -d= -f1` passes them through unredacted. **BANKED below: both should be rotated.** Never bulk-download a vault to find a name; fetch one named secret at a time |
| C | `pkill -f 'xfce4-terminal.*pane-'` matched its own argv (the pattern string itself contains the target text) and killed the script running it — same class as streamer-stub's own documented `pkill -f` trap. Killed nothing that needed killing that time; use exact PIDs, never `-f` with a pattern that could match your own command line |
| D | tmux clients attached directly to the same session with `-t agi-rc:<window>` all show the SAME current window (session-wide, not per-client) — the earlier tile showed 4 copies of one pane. Fix: grouped "view-*" sessions (`tmux new-session -t agi-rc -s view-X && tmux select-window -t view-X:X`), one per tile, each with its own current-window pointer |
| E | `bin/stream.sh --delay` didn't self-park into systemd — the Bash tool's own exec environment already sets `INVOCATION_ID`, so the script's "am I already under systemd" check was fooled. Fixed by stopping (`panic`) and going through `bin/install-unit.sh` + `systemctl --user start` explicitly instead of trusting the script's auto-detect |
| F | `_MOTIF_WM_HINTS` + unmap/remap didn't strip xfwm4 decorations on the tmux tiles — left as-is (titles are static `pane-<name>` labels only, no hostname/username leak, so low-risk); not worth more time chasing |

## §4 Traps (standing)
| # | trap | rule |
|---|---|---|
| 1 | `panic` kills every ffmpeg and stops the unit: the stream ends on every platform | the owner's kill switch: run it only when the owner names it |
| 2 | `brb`/`retract` destroy unaired footage; the unit reads `.env` once at start | `sb-status` first · `brb` before touching the desktop, the views or the stub · `back` after the change verifies |
| 3 | Twitch caps non-partners ~6 Mbps; X throttles a sustained ~5 Mbps; one stalled socket once starved every platform | keep the README's fifo + bitrate defaults unless a measurement says otherwise |
| 4 | every pane on `:1` airs after the delay — yours included: a secret printed in any pane goes public | keys travel keeper → variable → `.env`, never echoed; a secret on screen → `retract`, then `back` |
| 5 | the posts' panes are live agents | attach read-only (`-r` / grouped view-session); a keystroke in a post's pane is typed into that agent |
| 6 | Bash-tool shells never re-source the profile; AGI_AGENT_ID is unset, `~/bin` not on PATH | `send.py send --from stream-master`; full paths (`/home/belam/bin/sb-status` etc.) |
| 7 | graph text about the stub says `/home/ubuntu/work` (stream-town) | here `~/work` = `/data/work` (symlink, confirmed); your session log is under `~/.claude/projects/-data-work-agi/` |

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| **`EDGE_CLOUD_DISK_CMK_PEM` and `EDGE_SSH_PRIVATE_KEY` printed into a tool-output transcript this session (trap B)** | treat both as compromised: rotate the CMK and the SSH keypair, push new values into Doppler `belam/prd`, revoke the old ones. Not done by me — real infra action, your call on timing/method |
| `grid.py commit --all` hard-errors repo-wide on `experiment:a00-2a4dfb57-triage` (missing `mint_id`) | blocks the 5-min grid_sync cron's `commit --all` too, not just my graphweb commit — someone should run `backfill-mint-ids.py --write` |
| stream-town (core-town) still unreachable (ssh timed out again this session) | its own egress would mean local-town doesn't need to carry it through the hub; your call whether to bring it back |
| CAPTURE region is full 1920x1200 (both scenes fill it deliberately, panels autohidden) rather than cropped to one window | matches "the dox surface is the screen" once panels are hidden + tiles fill the frame; revisit if anything unexpected ever shows |
