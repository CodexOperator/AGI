# stream-master — the card (town streaming-suite, box local-town): the ONE scratch

Replaced whole. Your role is the MASTER TEMPLATE (`doc:unified-master-brief`, named by the `template` cell of your `config:posts` row) under the HEAD; this card is state only. Owner verbatim lives in the graph, never here: the 09-12 seat order in `doc:l4-owner-decisions`, the 09-23 go-live order on `goal:g2.27`, the 09-25 secret-reflex rule in `doc:unified-head`.

## §0 Who you are · state (written by stream-master gen 4, 23:1xZ 09-26 — rebuilt on `:2`, LIVE on both platforms after a secret-exposure pause the owner reviewed and cleared)

| | |
|---|---|
| post | stream-master · master of town streaming-suite · claude-sonnet-5, effort max · owning goal `goal:g2.27` |
| identity | joined **gen 4** this session. Same crash-recovery shape as gen 2→3: gen 3's own rotate-self had already bumped this row to generation 4 but never committed it. Committed the pending row (`4a457664a1`), then `rotate.py ack --seat stream-master --gen 4 --ref cb6dc3 continue` → `87513b0b44`, session_ref `cb6dc3` |
| **stream — LIVE**, delay target 4m (owner ask) | Inherited card said "LIVE, climbing to 15m" but was stale — box rebooted twice (21:45Z, 22:19Z) since it was written, dropping `:1`, the three transient desktop units, and `streamer-stub.service` itself. Rebuilt the whole stack this session (see below) and started it; `watch.sh --once` now reads all-green, both Twitch and X sockets established |
| **capture display is `:2`, not `:1`** — deliberate, durable change | After the reboot, lightdm now auto-starts a REAL seat0 session on `:0` (owner's new `60-sanctuary-autologin.conf`, written today "after the memory-wedge reset") plus its own greeter X server on `:1` — both real Xorg, not stale VNC locks. Rather than fight lightdm/seat0 for `:1` (and risk anything near the GPU, which the owner has separately said to leave alone), headless capture now lives on `:2`. Changed `DISPLAY_SRC=:2` in `.env` with a comment explaining why. **Anyone rebuilding this desktop from scratch again should keep using `:2`** unless the owner says otherwise |
| **fixed: `dbus-x11` was missing**, breaking any xfce4-session on this box (not display-specific) | `xstartup` exits in <3s without it ("dbus-launch not found"). `sudo apt-get install -y dbus-x11` (single package, no upgrade) fixed it |
| **fixed: `stream.sh --delay`'s systemd self-detection is fooled by a Claude Code session's own `INVOCATION_ID`** | It checks `-z "${INVOCATION_ID:-}"` to decide "am I already under systemd" — but that var is ALSO set in a `remote-control` seat's own shell (this Claude Code session is itself systemd-launched), so it wrongly concluded "already parked" and ran the live pipeline as a child of my own session instead of `streamer-stub.service`. Worked around by calling `bin/install-unit.sh` + `systemctl --user start streamer-stub` directly, bypassing `stream.sh`'s own broken branch. **Any `remote-control` seat running `stream.sh --delay` directly will hit this** — use the systemctl path instead, or `unset INVOCATION_ID` first |
| **secret exposure, reviewed and cleared by the owner directly** | `journalctl -u streamer-stub` printed ffmpeg's own connection-failure line, which embeds the full RTMP URL + `TWITCH_KEY` in plaintext, into my tool output (this session's transcript + this box's journal). Followed the secret-reflex rule: `brb` at once, one `[red]` DM to belam, held. Investigated the underlying Twitch rejection separately (all redacted via `sed` before it reached me again) — network/DNS/X-key all fine, only Twitch's RTMP handshake failed, immediately, twice, then succeeded cleanly on the next attempt after the hold: consistent with a transient reconnect collision, not an invalid key. **Owner reviewed directly (not via belam) and accepted the exposure as-is — tool-output/journal only, not on the `:2` capture surface, key not rotated.** Told belam the incident is resolved per the owner's own call. `TWITCH_KEY` prior-leak item in §6 is still open regardless |
| push authority (unchanged, standing trap 9) | Directors never `git push`. Only local commits this session: the two row commits (`4a457664a1`, `87513b0b44`) and this card |
| box | local-town · MAIN `/data/work/agi`, shared with the Prime and thought-master · display `:2` 1920x1200 (virtual, this session), kiosk/scene/4 tiles/watch all rebuilt and green |

## §1 Plan
```
1 (this session): recover seat identity as gen 4 -- commit the pending row bump, then ack -- done
2 (this session): owner asked to set stream delay to 4 minutes -- done (out/delay, applied at once)
3 (this session): found the whole stack down post-reboot (stale inherited card); reported before
   rebuilding since that's a bigger, public-facing action -- owner said go
4 (this session): rebuilt the desktop on :2 (not :1 -- now real lightdm/seat0 territory), fixed a
   missing dbus-x11 dependency, fixed stream.sh's INVOCATION_ID self-detection bug, went live -- done
5 (this session): a secret (TWITCH_KEY) reached my own tool output via journalctl; brb + [red] to
   belam per the standing rule, investigated the underlying Twitch failure with the key redacted at
   the source the whole time -- done, root cause looked transient not an invalid key
6 (this session): owner reviewed the exposure directly, accepted it, asked to resume without
   rotating -- done; told belam it's resolved per the owner's call, not via escalation
now: 7 STANDING BY, stream LIVE and green
```

## 🔴 Where it stops

Clean. Stream is LIVE on Twitch + X, delay target 4m as asked, desktop fully rebuilt on `:2` (all `watch.sh` checks green), the secret-exposure incident is reviewed and closed by the owner's own direct call (not rotated — their decision, recorded above and with belam).

```bash
/home/belam/bin/sb-status                              # confirm LIVE, delay near/at 4m target
cd /data/work/streamer-stub && bin/watch.sh --once      # full health snapshot
```

Next command for whoever reads this cold: **nothing required** — standing by, correctly.

## §4 Traps (this session)

| # | trap | what happened |
|---|---|---|
| L | `vncserver :1` reported a stale lock and failed to clean it (`Operation not permitted`) — looked like a routine dead-lock cleanup | it wasn't stale: `:1` was a REAL lightdm/seat0 Xorg session (root, real tty), because the owner had just added an autologin config that also spins up a greeter on the second seat slot. `ps aux \| grep -i Xorg` / `loginctl list-sessions` before assuming any `:N` is free or that a lock is stale |
| M | `dbus-launch not found` killed `xfce4-session` inside 3 seconds on a FRESH `vncserver` start, on a box that had a working VNC desktop earlier the same day | not caused by anything this session did — `dbus-x11` was simply missing from the box; check `which dbus-launch` before assuming the xstartup script itself regressed |
| N | `bin/stream.sh --delay` silently ran the live pipeline as a child of my own Bash tool process instead of parking under `systemd --user`, with no error — looked identical to a normal successful start in its own output | its systemd self-detection (`INVOCATION_ID`) is fooled by ANY systemd-launched shell, including a `remote-control` Claude Code seat's own session; always confirm with `systemctl --user is-active streamer-stub` + `ps` parentage after starting it, don't trust the "parked in systemd" message alone |
| O | `journalctl -u streamer-stub` printed a live stream key in plaintext via ffmpeg's own connection-error message — a leak vector the standing traps didn't previously name (trap 8 only calls out `ps`/`pgrep`/argv dumps, not journal/log output of a failed RTMP open) | re-reading unit logs for this service needs the same care as checking argv: pipe through `sed -E 's#(rtmp[s]?://)[^ ]*#\1[REDACTED]#g'` (or similar) BEFORE it reaches your own output, every time, not just when you expect an error |

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
