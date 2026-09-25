# stream-master — the card (town streaming-suite, box local-town): the ONE scratch

Replaced whole. Your role is the MASTER TEMPLATE (`doc:unified-master-brief`, named by the `template` cell of your `config:posts` row) under the HEAD; this card is state only. Owner verbatim lives in the graph, never here: the 09-12 seat order in `doc:l4-owner-decisions`, the 09-23 go-live order on `goal:g2.27`, the 09-25 secret-reflex rule in `doc:unified-head`.

## §0 Who you are · state (written by stream-master, 02:1xZ 09-25 — PAUSED, awaiting release)

| | |
|---|---|
| post | stream-master · master of town streaming-suite · claude-sonnet-5, effort max · owning goal `goal:g2.27` |
| stream | **PAUSED (`brb`) since ~02:03Z 09-25 — NOT live right now.** Ring kept, `back` resumes exactly where it stopped. Paused per the owner's standing secret-reflex rule (see §0 "safety reflex" row) after a diagnostic command printed the live keys into this session's own tool-output transcript (§4 trap G) — reported to belam, awaiting `back`/direction from them or the owner. **A cold successor: do NOT run `back` yourself** — it is explicitly not in this seat's grant for this class of event; check the inbox / ask belam first. |
| safety reflex (owner, 09-25 00:5xZ, durable `doc:unified-head`) | **Standing, every post:** a secret/key/address/hostname reaching your pane → `brb` at once → ONE `[red]` line to belam → wait, no time pressure. `panic` is owner-only (refused for every other actor); `back` is also not in this grant for a leak event — someone else releases it. Supersedes the OLD standing trap-4 wording below ("secret on screen → retract, then back") for this box: **`brb` not `retract`** (nothing here reaches the capture path anyway — see trap G), and **you don't self-release**. |
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
9 (this session, unplanned): secret reached my own pane (trap G) -> brb'd, reported to belam per the 09-25 reflex rule — done, NOW BLOCKED on belam/owner
now: 10 STANDING BY for (a) belam/owner's response on the trap-G report / release, (b) the watch's alerts, (c) further stream requests
```

## 🔴 Where it stops

Two independent reasons to be standing by, not one:

1. **The stream is paused (`brb`), not live**, pending `back` from belam or the owner per the fresh secret-reflex rule (§0) — this seat does not self-release for this class of event. Check `send.py read stream-master` and `send.py read --to belam stream-master` (or however the reply surfaces) before assuming it's still open.
2. **The health watch is running** (`streamer-stub-watch.service`, 30s interval) and will page this seat's inbox + `wake` it on any transition to unhealthy — nothing to poll by hand.

All the audit/documentation work requested this session is done: `streamer-stub/README.md` and `streamer-stub/QUICKSTART.md` now cover the kiosk, the tmux pin/rotation system, bringing YouTube up alongside Twitch+X, resetting the uptime/outage counters, making a clean code change, and the watch itself. The watch is installed and verified (both the health-check logic via `--once`, and the alert pipeline via a real test send+wake, before trusting it unattended).

```bash
DISPLAY=:1 /home/belam/bin/sb-status                                  # confirm still PAUSED (or back already happened)
python3 extensions/agi/bin/send.py read stream-master                 # belam's reply on the trap-G report, if any
bin/watch.sh --once                                                    # (cd /data/work/streamer-stub) full health snapshot
```

Next command for whoever reads this cold: **nothing required** unless the inbox already holds a reply — this is a standby state, correctly, for two independent and legitimate reasons.

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
| 8 | dumping the relay's ffmpeg argv (`pgrep -a`, `ps aux \| grep ffmpeg`, `pstree -p`) prints the live stream keys into whatever is reading your output (trap G, this session) | never do it; `out/relay.pid` + `ss -tnp` (pid/fd/name, no argv) or `sb-status` cover every legitimate check |

## §6 BANKED (owner-only)

| item | recommendation |
|---|---|
| **Stream keys (Twitch + X) appeared in this session's own tool-output transcript (trap G)** | contained — never reached the capture region or the broadcast, not repeated, not written anywhere. Lower blast-radius than trap B's CMK/SSH keys (this only lets someone push video *as* the channel, not touch infra), and the README already treats a `ps`-visible key as accepted risk for this single-tenant box — but your call whether the fresh reflex rule means rotating these two anyway. Not done by me; paused (`brb`) and reported per the rule, no further action taken pending your read |
| `EDGE_CLOUD_DISK_CMK_PEM` and `EDGE_SSH_PRIVATE_KEY` printed into a tool-output transcript (trap B, prior session) — still open | rotate both, push new values into Doppler `belam/prd`, revoke the old ones, if not already done |
| `grid.py commit --all` hard-errors repo-wide on `experiment:a00-2a4dfb57-triage` (missing `mint_id`) | still blocks the 5-min grid_sync cron's `commit --all`, not just graphweb's — someone should run `backfill-mint-ids.py --write` |
| stream-town (core-town) still unreachable (ssh timed out again, prior session) | its own egress would mean local-town doesn't need to carry it through the hub; your call whether to bring it back |
| CAPTURE region is full 1920x1200 (both scenes fill it deliberately, panels autohidden) rather than cropped to one window | matches "the dox surface is the screen" once panels are hidden + tiles fill the frame; revisit if anything unexpected ever shows |
| YouTube (`YT_KEY` empty) — third platform not live yet | key not yet in the vault under any name this seat could confirm; QUICKSTART has the exact bring-up procedure for whenever it lands |
