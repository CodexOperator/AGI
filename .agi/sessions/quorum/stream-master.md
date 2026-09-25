# stream-master — the card (town streaming-suite, box local-town): the ONE scratch

Replaced whole. Your role is the MASTER TEMPLATE (`doc:unified-master-brief`, named by the `template` cell of your `config:posts` row) under the HEAD; this card is state only. Owner verbatim lives in the graph, never here: the 09-12 seat order in `doc:l4-owner-decisions`, the 09-23 go-live order on `goal:g2.27`, the 09-25 secret-reflex rule in `doc:unified-head`.

## §0 Who you are · state (written by stream-master, 02:2xZ 09-25 — LIVE again, fresh ramp)

| | |
|---|---|
| post | stream-master · master of town streaming-suite · claude-sonnet-5, effort max · owning goal `goal:g2.27` |
| stream | **LIVE again from ~02:17Z 09-25**, released by a DIRECT instruction from the same operator driving this seat's own interactive terminal — **not** through the graph/DM channel belam and I had both been treating as the only release path (see the deviation note right below). Brought back with a **full unit restart while still on HOLD** (fresh `grab.sh` wipes the ring, fresh `relay.sh` re-initialises `FLOOR=DELAY_START`; both confirmed by the startup log line "go live at 2m00s, target 15m00s"), THEN `back` — so it started from a genuinely empty ring and is climbing `0 -> 2m -> 15m` per `lib.sh`'s own design, not fast-forwarding the ~6 min backlog a plain `back` on the old process would have. This is now the documented pattern for "give me a clean restart, not a catch-up" — see QUICKSTART "Go live / pause / cut / resume". belam informed (02:1xZ, tagged `[owner]`, flagging the channel mismatch) |
| deviation, recorded (owner 2026-09-25 ~02:2xZ, this session) | The standing rule from §0 below ("back is the owner's... not even belam self-releases") assumed the owner would act through the graph. Here the instruction came directly into this session's own chat from whoever is operating this seat's Claude Code terminal — treated as owner authority because it is the same real-world operator, present and direct, which is a *stronger* signal than a relayed/signed DM, not a weaker one. Judgment call, not a re-interpretation of the rule: the rule is about WHO may release a hold (the owner only), not WHICH channel they must use to say so |
| safety reflex (owner, 09-25 00:5xZ, durable `doc:unified-head`; tightened by belam 02:06Z) | **Standing, every post:** a secret/key/address/hostname reaching your pane → `brb` at once → ONE `[red]` line to belam → wait, no time pressure. `panic` is owner-only (refused for every other actor); `back` is also not in this grant for a leak event — the OWNER releases it, confirmed 09-25 (not even belam self-releases another post's brb of this kind). Supersedes the OLD standing trap-4 wording below ("secret on screen → retract, then back") for this box: **`brb` not `retract`**, and **you don't self-release**. belam's own added rule, same reply: **never `ps -ef` / `pgrep -a` / `cat /proc/PID/cmdline` on the relay** — count or pid only (`pgrep -c`, `pgrep -x`, or `ss -tnp` for sockets); see trap 8 |
| ops procedures | **Now live in `streamer-stub`'s own docs, not duplicated here** — `README.md` (why + mechanism) and `QUICKSTART.md` (just the commands), covering: the kiosk (`agi-graphweb`/`agi-graph-kiosk`, transient, recreate commands), the tmux pin + rotation system (`view-<seat>` grouped sessions, `pane-<seat>` xterms, geometry, `rotate.py`'s auto-repoint), bringing a platform (e.g. YouTube) live once its key exists, resetting/logging the uptime+outage counters (`SB_UPTIME_START_EPOCH`/`_OUTAGE_SECONDS`, hardcoded in `bin/lib.sh`), and making any code change without a visible interruption (`brb` → edit → restart → `sb-status` → `back`). Read those, not just this row, before touching any of it. |
| watch | **Built + running this session:** `bin/watch.sh` (read-only health poll — streamer-stub unit, per-platform ESTAB sockets via `ss -tnp` only — never argv-dumping, see trap G — ring-starvation, the 3 desktop services, every currently-pinned `pane-<seat>`) + `bin/install-watch-unit.sh` (transient unit `streamer-stub-watch`, mirrors `install-scene-unit.sh`'s convention). Debounced alerts → `send.py send` to `stream-master`'s own inbox + a `wake` nudge, tagged `[red]`. Never acts itself (no `brb`/`panic` calls) — a watcher that can act is a watcher that can panic the stream on a false positive. `watch --once` any time; `tail -f out/watch.log` for history. Correctly treats the current `brb` hold as healthy (verified) — will not alert about "relay down" while intentionally paused. |
| tmux tiles | one `view-<seat>` grouped session per tile — `view-thought-master`, `view-director-engine`, `view-director-thought`, `view-belam` — `view-<seat>` is the naming `rotate.py`'s own `_repoint_livestream_views` (s9) looks for on every rotation of that seat, so each tile follows its seat through generations automatically. Never name one after a generation-specific window label (`<seat>-S#-L#-<roman>`) — only the stable seat name repoints. Full recreate procedure: README "The pin: which seats are on screen" |
| kiosk | `agi-graphweb.service` (:8765) + `agi-graph-kiosk.service`, both **transient** systemd --user units (no file on disk — `systemctl --user cat NAME` shows the `ExecStart` to recreate from; README has the exact commands). Do not expect either to survive a reboot |
| box | local-town · MAIN `/data/work/agi`, shared with the Prime and thought-master · display `:1` 1920x1200, both xfce panels autohidden (no username/hostname/notifications in capture) |
| keys | TWITCH_KEY (46 chars) + X_KEY (12 chars) live; YT_KEY empty (YouTube not yet brought up — README/QUICKSTART have the "add a platform" procedure for when that key exists). Doppler project `belam`, config `prd`, secret names carry a `_STREAM_KEY` suffix the `.env` var names don't (`TWITCH_STREAM_KEY`→`TWITCH_KEY` etc. — README's Doppler snippet was wrong about this before this session, now fixed). One named secret at a time, exit-code-only test, never bulk-download (trap B, prior session) |
| graphweb | prior session's `_spherical_z` fold + camera autopilot, commit `d7d31bc2ef`. `grid.py commit --all` still hard-errors repo-wide on a pre-existing unrelated node (`experiment:a00-2a4dfb57-triage` missing `mint_id`) — unrelated to anything this session touched; still banked below |

## §1 Plan
```
1-7 (prior sessions): clone+read, box prep, keys, LIVE, systemd unit — done
8 (this session): audit + document kiosk/pin/dual-stream/counters/clean-change, build + start the health watch — done
9 (this session, unplanned): secret reached my own pane (trap G) -> brb'd, reported to belam per the 09-25 reflex rule — done, resolved (belam replied, escalated key rotation)
10 (this session): direct operator instruction -> brought the stream back LIVE with a fresh restart, not a backlog catch-up — done, verified on-air
now: 11 STANDING BY for the watch's alerts / further stream requests
```

## 🔴 Where it stops

Nothing pending, nothing blocked. Stream is LIVE (fresh ramp, see §0), the trap-G thread is closed (belam confirmed + escalated), and the health watch is running and will page this seat's inbox on any transition to unhealthy — nothing to poll by hand.

All the audit/documentation work requested this session is done: `streamer-stub/README.md` and `streamer-stub/QUICKSTART.md` now cover the kiosk, the tmux pin/rotation system, bringing YouTube up alongside Twitch+X, resetting the uptime/outage counters, making a clean code change (and the fresh-restart-vs-backlog-catchup distinction learned this turn), and the watch itself.

```bash
DISPLAY=:1 /home/belam/bin/sb-status                                  # confirm still live, check the delay is climbing toward 15m
bin/watch.sh --once                                                    # (cd /data/work/streamer-stub) full health snapshot
```

Next command for whoever reads this cold: **nothing required** — standing by, correctly.

## §4 Traps (this session, in addition to the standing table below)

| # | trap | what happened |
|---|---|---|
| G | **`pgrep -a -x ffmpeg` (used to find the relay's ffmpeg pid while designing the watch's connectivity check) printed the full tee argument — both live Twitch and X ingest URLs WITH keys — into this session's own tool-output transcript.** Same leak class as the README's own documented-and-accepted `ps` leak, but the owner's fresh 09-25 reflex rule (§0) treats any such sighting as `brb`-worthy regardless of blast-radius reasoning — complied rather than argued myself out of it. Contained: never reached `:1` or the capture region (this seat's own pane is not a pinned stream tile, no `view-stream-master` session exists), not repeated, not written into any doc. `bin/watch.sh`'s own connectivity check was rewritten to count `ss -tnp` sockets by process name only (no argv) before it ever ran unattended — see the "Automated health watch" section in README for why. **Never `pgrep -a` / `ps aux \| grep ffmpeg` / `pstree -p` on this relay for any reason** — `out/relay.pid`, `sb-status`, or `ss -tnp` (pid/fd/name only) cover every legitimate need without touching argv |
| H | stale duplicated content + a stray closing code-fence in this card's own "Where it stops" section (prior session) — cleaned up in this rewrite; if a future wholesale Write ever produces a doubled paragraph again, it's a copy-paste-into-the-Write-call slip, not a tool bug |

## §4 Traps (standing)

| # | trap | rule |
|---|---|---|
| 1 | `panic` kills every ffmpeg and stops the unit: the stream ends on every platform | owner-only, refused for every other actor (09-25, tightened from "the owner's kill switch: run it only when the owner names it") — never run it as any other post |
| 2 | `brb`/`retract` destroy unaired footage; the unit reads `.env` once at start | `sb-status` first · `brb` before touching the desktop, the views or the stub · `back` after the change verifies — **except** a secret-reflex `brb` (see #4): that one waits for someone else's `back` |
| 3 | Twitch caps non-partners ~6 Mbps; X throttles a sustained ~5 Mbps; one stalled socket once starved every platform | keep the README's fifo + bitrate defaults unless a measurement says otherwise |
| 4 | **any secret/key/address/hostname reaching ANY pane (yours included — not only what's captured on `:1`)** | **`brb`** (not `retract` — updated 09-25) at once, ONE `[red]` line to belam, then wait: not `back`, not `panic`, no time pressure after that point. Old wording ("secret on screen → retract, then back") is superseded — see §0 |
| 5 | the posts' panes are live agents | attach read-only (`-r` / grouped view-session); a keystroke in a post's pane is typed into that agent |
| 6 | Bash-tool shells never re-source the profile; AGI_AGENT_ID is unset, `~/bin` not on PATH | `send.py send --from stream-master`; full paths (`/home/belam/bin/sb-status` etc.) |
| 7 | graph text about the stub says `/home/ubuntu/work` (stream-town) | here `~/work` = `/data/work` (symlink, confirmed); your session log is under `~/.claude/projects/-data-work-agi/` |
| 8 | dumping the relay's ffmpeg argv (`pgrep -a`, `ps -ef`/`ps aux \| grep ffmpeg`, `pstree -p`, `cat /proc/PID/cmdline`) prints the live stream keys into whatever is reading your output (trap G, this session; rule confirmed + widened by belam 02:06Z, "for every post") | never do it; `out/relay.pid` + `ss -tnp` (pid/fd/name, no argv), `pgrep -c`/`pgrep -x` (count/pid only), or `sb-status` cover every legitimate check |

## §6 BANKED (owner-only)

| item | recommendation |
|---|---|
| **Stream keys (Twitch + X) appeared in this session's own tool-output transcript (trap G)** | **already escalated — belam reported it to you 02:06Z with a recommendation to rotate both at your leisure.** Contained on this end (never reached the capture region or the broadcast, not repeated, not written anywhere); this row is just a pointer so it isn't lost, not a duplicate ask |
| `EDGE_CLOUD_DISK_CMK_PEM` and `EDGE_SSH_PRIVATE_KEY` printed into a tool-output transcript (trap B, prior session) — still open | rotate both, push new values into Doppler `belam/prd`, revoke the old ones, if not already done |
| `grid.py commit --all` hard-errors repo-wide on `experiment:a00-2a4dfb57-triage` (missing `mint_id`) | still blocks the 5-min grid_sync cron's `commit --all`, not just graphweb's — someone should run `backfill-mint-ids.py --write` |
| stream-town (core-town) still unreachable (ssh timed out again, prior session) | its own egress would mean local-town doesn't need to carry it through the hub; your call whether to bring it back |
| CAPTURE region is full 1920x1200 (both scenes fill it deliberately, panels autohidden) rather than cropped to one window | matches "the dox surface is the screen" once panels are hidden + tiles fill the frame; revisit if anything unexpected ever shows |
| YouTube (`YT_KEY` empty) — third platform not live yet | key not yet in the vault under any name this seat could confirm; QUICKSTART has the exact bring-up procedure for whenever it lands |
