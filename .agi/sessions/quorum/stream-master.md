# stream-master — the card (town streaming-suite, box local-town): the ONE scratch

Replaced whole. Your role is the MASTER TEMPLATE (`doc:unified-master-brief`, named by the `template` cell of your `config:posts` row) under the HEAD; this card is state only. Owner verbatim lives in the graph, never here: the 09-12 seat order in `doc:l4-owner-decisions`, the 09-23 go-live order on `goal:g2.27`, the 09-25 secret-reflex rule in `doc:unified-head`.

## §0 Who you are · state (written by stream-master gen 3, 06:5xZ 09-25 — crash-recovered; correcting a stale card that still said LIVE)

| | |
|---|---|
| post | stream-master · master of town streaming-suite · claude-sonnet-5, effort max · owning goal `goal:g2.27` |
| identity | joined **gen 3** this session (crash-recovery: gen 2's row was already bumped to gen 3 in the tree but left uncommitted — presumably the same OOM kill that took every seat at 04:00Z interrupted whoever was mid-join). Committed the pending row, then `rotate.py ack --gen 3 --ref 25c482 continue` → `fc79e35b15`, session_ref `25c482` |
| **stream — NOT live** | **PAUSED since 04:47:43Z** (the Prime's own `brb`, "card on air, ring kept") — the card this generation inherited still said "LIVE again from ~02:17Z", which predates the 04:00Z OOM kill and is stale; corrected here. Ring is now AT its max window (`RING_MAX_SECONDS` = delay(900s) + 3600s = 4500s; `sb-status` reads ~4502s unaired), so the **oldest paused-era footage has started aging out** — not an emergency (bounded ring, working as designed), but worth knowing before PASS 6 (noted for 09:48Z). Not releasing `back` myself: this hold was the Prime's, not mine, and a hold placed by someone else isn't mine to lift without knowing why (see §6) |
| **X display `:1` is down (new finding, this session)** | No Xorg/VNC process anywhere on the box, `/tmp/.X11-unix/` is empty (mtime 04:01Z — the OOM window), `loginctl list-sessions` and `who` show no graphical session. Down since ~04:01Z, never brought back in the Prime's 04:07Z seat-recovery. **This is the real reason the stream is still on the card, not just a paused choice** — there is currently nothing live on `:1` to capture. A `tigervncserver@:1` system unit exists on this box but is `disabled`/`inactive`; README only documents display-`:1` recreate for two *other* boxes (`vnic`: `vncserver :1` by hand; `belam-prime`: that same systemd unit) — this box (hostname `belam-gpu`) isn't covered by either row, and it has a GPU other work may depend on, so I did not guess an invocation. Banked to belam/owner, see §6 |
| kiosk — a downstream symptom, not its own bug | `agi-graphweb` (:8765) and `agi-scene-rotate` are both healthy, up since 09-24, survived the OOM kill untouched. Only `agi-graph-kiosk` was gone; recreated it verbatim per README's documented `systemd-run` command, but it now dies in ~3s on `Error: cannot open display :1` and the transient unit's own `--collect` removes it on exit — that's fully explained by the `:1`-down finding above, not a second problem. Don't re-attempt the kiosk recreate until `:1` is back |
| **push authority (new rule, this session — verified belam, ed25519, 02:54:23Z)** | Directors (`director-engine`, `director-thought`, every post whose row carries `role: director` — stream-master included) never `git push`; a post branch is local-only. A finished merge-up goes to your master with one `[merge-up]` line; **thought-master** alone lands + pushes `local-maxxing/season2/main`. **I broke this once** — see trap I below; no repeat |
| ops procedures | Live in `streamer-stub`'s own docs, not duplicated here — `README.md` (why + mechanism) and `QUICKSTART.md` (just the commands): kiosk recreate, the tmux pin/rotation system, bringing a platform (e.g. YouTube) live, the uptime/outage counters, making a code change without a visible interruption. Read those, not just this row, before touching any of it |
| watch | `bin/watch.sh` (read-only health poll) + `bin/install-watch-unit.sh` (transient unit `streamer-stub-watch`) still running, still correctly treats the `brb` hold as healthy. It flagged `agi-graph-kiosk is not active` this session — that alert is real and is the `:1`-down finding above, not a false positive. Debounced alerts → `send.py send` to stream-master's own inbox + `wake`, tagged `[red]`. Never acts itself |
| tmux tiles | one `view-<seat>` grouped session per tile — `view-thought-master`, `view-director-engine`, `view-director-thought`, `view-belam` — `rotate.py`'s `_repoint_livestream_views` (s9) follows the stable seat name through generations. Never name one after a generation-specific window label. Full recreate procedure: README "The pin: which seats are on screen" |
| box | local-town · MAIN `/data/work/agi`, shared with the Prime and thought-master · display `:1` **normally** 1920x1200, both xfce panels autohidden — currently down, see above |
| keys | TWITCH_KEY (46 chars) + X_KEY (12 chars) live; YT_KEY empty. Doppler project `belam`, config `prd`, secret names carry a `_STREAM_KEY` suffix the `.env` var names don't. One named secret at a time, exit-code-only test, never bulk-download (trap B) |
| graphweb | prior session's `_spherical_z` fold + camera autopilot, commit `d7d31bc2ef`, unaffected by anything this session. `grid.py commit --all` still hard-errors repo-wide on a pre-existing unrelated node (`experiment:a00-2a4dfb57-triage` missing `mint_id`) — still banked below |

## §1 Plan
```
1 (this session): crash-recovery join as gen 3 -- row commit 8abad52787 + ack fc79e35b15 -- done
2 (this session): `git push`'d those (+1 pre-existing) commits to origin as a director, BEFORE reading belam's
   02:54Z push-authority rule sitting unread in my inbox -- done, mistake (see trap I); damage = none
   (clean fast-forward d3b0bab5d1..fc79e35b15, no conflict); reported, will not repeat
3 (this session): ground-truth check against the inherited card -- found PAUSED not LIVE, ring at max window -- done
4 (this session): agi-graph-kiosk missing -- recreated per README -- done, but it just flaps (see below)
5 (this session): traced the flap to X display :1 itself being down since ~04:01Z, never restarted after
   the OOM -- banked rather than guessing a fix on a GPU box (see §6) -- done
6 (this session): reported all of the above to belam -- done
now: 7 STANDING BY -- not releasing `back`, not touching `:1`/the kiosk further, available for a named command
```

## 🔴 Where it stops

Not fully clean, and that's accurate rather than a problem to paper over: the stream is genuinely down (paused + its capture source down), but every open thread is either resolved or correctly banked — nothing is silently broken.

- Resolved this session: gen-3 identity join; the stale "LIVE" claim corrected; the kiosk mystery traced to its real, upstream cause.
- Banked, owner-only (§6): who brings `:1` back on this specific box, and how.
- Reported, no reply needed to keep working: the push-authority mistake (trap I).

```bash
systemctl --user status agi-graph-kiosk agi-graphweb agi-scene-rotate --no-pager   # kiosk stays absent (collected) until :1 is back
DISPLAY=:1 xset q                                                                   # still "unable to open display" until :1 comes back
DISPLAY=:1 /home/belam/bin/sb-status                                                # confirm PAUSE state / ring size
bin/watch.sh --once                                                                 # (cd /data/work/streamer-stub) full health snapshot
```

Next command for whoever reads this cold: **check belam's reply on the `:1` question (§6) before touching the desktop or kiosk again**; everything else in this card is current as of 06:5xZ.

## §4 Traps (this session)

| # | trap | what happened |
|---|---|---|
| I | **Ran `git push` on `local-maxxing/season2/main` as a director (2 commits of my own + 1 pre-existing), before I had read belam's 02:54Z rule that directors never push.** The rule exists because `director-thought` made this exact mistake once already. Content was fine (clean fast-forward, my own identity row + a benign pre-existing commit) so no damage, but it's still the wrong actor pushing | never `git push` as a director again; a finished merge-up goes to your master with one `[merge-up]` line, thought-master lands + pushes `local-maxxing/season2/main` (now trap 9 in the standing table) |
| J | `agi-graph-kiosk`'s documented `systemd-run --collect` recreate command runs and looks fine for ~3 seconds, then the unit vanishes (`--collect` removes it on exit) — reads exactly like "the recreate didn't take" | before assuming the kiosk unit itself is broken, check `DISPLAY=:1 xset q` / `ls /tmp/.X11-unix` / `loginctl list-sessions` first — if `:1` itself is down, recreating the kiosk is a no-op that will just flap on `cannot open display` |

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
| **X display `:1` is down on this box (`belam-gpu`) since ~04:01Z — nothing streamable to capture until it's back** | Need either the right recreate command for *this* box (README only documents `vnic`'s `vncserver :1` by hand and `belam-prime`'s `tigervncserver@:1` unit — neither confirmed for `belam-gpu`, which also carries GPU considerations I can't assess from here) or the Prime/owner to bring it up directly. Everything downstream (kiosk, live desktop capture, resuming `back`) is blocked on this one thing |
| Stream keys (Twitch + X) appeared in a prior session's tool-output transcript (trap G, prior generation) | already escalated per that generation's card; rotate both at your leisure if not already done |
| `EDGE_CLOUD_DISK_CMK_PEM` and `EDGE_SSH_PRIVATE_KEY` printed into a tool-output transcript (trap B, earlier session) — still open | rotate both, push new values into Doppler `belam/prd`, revoke the old ones, if not already done |
| `grid.py commit --all` hard-errors repo-wide on `experiment:a00-2a4dfb57-triage` (missing `mint_id`) | still blocks the 5-min grid_sync cron's `commit --all`, not just graphweb's — someone should run `backfill-mint-ids.py --write` |
| stream-town (core-town) still unreachable (ssh timed out, prior session) | its own egress would mean local-town doesn't need to carry it through the hub; your call whether to bring it back |
| CAPTURE region is full 1920x1200 (both scenes fill it deliberately, panels autohidden) rather than cropped to one window | matches "the dox surface is the screen" once panels are hidden + tiles fill the frame; revisit if anything unexpected ever shows |
| YouTube (`YT_KEY` empty) — third platform not live yet | key not yet in the vault under any name this seat could confirm; QUICKSTART has the exact bring-up procedure for whenever it lands |
| going forward, should this post work a dedicated local branch, or stay local-only on `season2/main` until a merge-up to thought-master? | asked belam directly (DM); the push-authority rule (trap 9) didn't specify the day-to-day branch shape, only that directors never push |
