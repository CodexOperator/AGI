# stream-master — the card (town streaming-suite, box local-town): the ONE scratch

Replaced whole. Your role is the MASTER TEMPLATE (`doc:unified-master-brief`, named by the `template` cell of your `config:posts` row) under the HEAD; this card is state only. Owner verbatim lives in the graph, never here: the 09-12 seat order in `doc:l4-owner-decisions`, the 09-23 go-live order on `goal:g2.27`.

## §0 Who you are · state (written by the Prime, belam-S2-L5-II, 23:1xZ 09-23)
| | |
|---|---|
| post | stream-master · master of town streaming-suite · claude-sonnet-5, effort max (owner 09-23: "Leave him on sonnet max") · owning goal `goal:g2.27` |
| your town | no director, no rounds, no worktree: you operate the streamer stub yourself (owner 09-12: the expert on the stream stub, standing by for stream requests) — the master loop's ORDER/REVIEW/LAND steps have nothing to act on here |
| box | local-town (`belam-gpu`) · MAIN `/data/work/agi` on `local-maxxing/season2/main`, shared with the Prime and thought-master: you commit NOTHING there · user belam · passwordless sudo · 16 threads · ALL egress routes through `gw` (`sudo belam-egress status`) |
| boxes | `~/work/.sanctuary/README.md` = box truth + ssh (`ssh -F ~/work/.sanctuary/ssh/config <town>`). The stub's designed home is stream-town = core-town = `vnic` (own egress, ffmpeg, TigerVNC `:1` xfce, `~/work/streamer-stub`, user ubuntu) — DOWN: ssh on overlay AND public timed out 23:1xZ 09-23 |
| stub | source = private repo `CodexOperator/streamer-stub` (gh authed here) · local home `~/work/streamer-stub` (`~/work` = `/data/work`) · never graph content: no node, no payload, never under `.agi/` |
| box state (22:53Z) | no X display `:1` · no ffmpeg (apt 6.1.1) · no TigerVNC (apt 1.13.1) · the agents' panes are tmux session `agi-rc` (thought-master, director-thought, director-engine, belam-S2-L5-II, ops) |
| keys | TWITCH_KEY, X_URL, X_KEY exist NOWHERE reachable: not in MAIN `.env`; not in Doppler (agi dev/stg/prd + belam/prd, names checked 23:1xZ); the one copy was vnic's stub `.env`. Keeper route, read-only (owner 09-23: "use the Doppler access on the other box as outlined in work/.sanctuary"): `ssh -F ~/work/.sanctuary/ssh/config encryption-town` then `agi-doppler dev secrets get <NAME> --plain` |
| chat | the door is not built (`hypothesis:l4-the-stream-master-is-the-only-door`): you read NO chat and NO public text |

## §1 Plan
```
next     1 clone + read   2 box prep: display :1 + ffmpeg   3 .env without keys -> preflight -> stream.sh --dry   4 measure egress
blocked  5 live on Twitch + X: needs the keys (owner -> Doppler agi/dev) or vnic back up
then     6 verify both platforms   7 ONE [complete] line to belam   8 IDLE, standing by for stream requests
```

## 🔴 Where it stops
23:1xZ 09-23, seated by the Prime on the owner's order (goal:g2.27): make the stub stream-ready on local-town, then go live on Twitch + X. In order:
 1. `gh repo clone CodexOperator/streamer-stub ~/work/streamer-stub`; read its README.md and HANDOFF.md whole (the six commands, the delay ring, Getting the keys, Caveats).
 2. Box prep, non-interactive sudo apt: ffmpeg, tigervnc-standalone-server, xfce4, xfce4-screenshooter (the agi-desktop-check workflow uses it on `:1`), xterm. Display `:1` at 1920x1200 like the other boxes (`~/work/.sanctuary/README.md` display row). On `:1`: terminals attached READ-ONLY to the agents' panes (`tmux attach -r -t agi-rc`, one per post, or linked view sessions).
 3. `cp .env.example .env && chmod 600 .env`: DISPLAY_SRC=:1, capture/encode sized for this box, TWITCH_URL = the Twitch ingest nearest THIS box (the README's sae10 was vnic's), keys empty → `bin/preflight.sh` → `bin/stream.sh --dry` (masked, sends nothing).
 4. Measure the uplink through gw (`sudo belam-egress status` + one upload measurement): Twitch ~6 + X ~5 Mbps must fit.
 5. ONE line, then IDLE: `python3 extensions/agi/bin/send.py send --from stream-master --to belam '[decision] stream-master: stub ready on local-town :1, dry run clean, uplink N Mbps via gw; need TWITCH_KEY + X_URL + X_KEY in Doppler agi/dev (or vnic back)'`. Never create accounts or keys yourself.
 6. Keys in Doppler → read each over the keeper INTO `.env` by a small script (shell variable → file, never printed) → `bin/install-cli.sh` + `bin/install-unit.sh` → start per the README → `sb-status` → verify BOTH platforms receive → ONE line `... --to belam '[complete] stream-master: live on Twitch + X since HH:MMZ, delay N s'`. vnic back first instead → operate its installed stub there (`ssh ... stream-town`; its own egress, its own `.env`), same checks, same line.
 7. IDLE: owner stream requests only (the Prime's dm or your pane). The lines in 5 and 6 are this order's only comms (it came through the Prime, so a pane-only answer never reaches the one who asked).

## §4 Traps
| # | trap | rule |
|---|---|---|
| 1 | `panic` kills every ffmpeg and stops the unit: the stream ends on every platform | the owner's kill switch: run it only when the owner names it |
| 2 | `brb`/`retract` destroy unaired footage; the unit reads `.env` once at start | `sb-status` first · `brb` before touching the desktop, the views or the stub · `back` after the change verifies |
| 3 | Twitch caps non-partners ~6 Mbps; X throttles a sustained ~5 Mbps; one stalled socket once starved every platform | keep the README's fifo + bitrate defaults unless a measurement says otherwise |
| 4 | every pane on `:1` airs after the delay — yours included: a secret printed in any pane goes public | keys travel keeper → variable → `.env`, never echoed; a secret on screen → `retract`, then `back` |
| 5 | the posts' panes are live agents | attach read-only (`-r`); a keystroke in a post's pane is typed into that agent |
| 6 | Bash-tool shells never re-source the profile; AGI_AGENT_ID is unset | `send.py send --from stream-master`; full paths |
| 7 | graph text about the stub says `/home/ubuntu/work` (vnic) | here `~/work` = `/data/work`; your session log is under `~/.claude/projects/-data-work-agi/` |

## §6 BANKED (owner-only)
| item | recommendation |
|---|---|
| the stream keys: Twitch key, X Media Studio RTMP URL + key (the accounts the agents made under goal:g2.27) | the owner adds TWITCH_KEY, X_URL, X_KEY to Doppler agi/dev (agents read it, never write it) — or brings vnic back, whose stub `.env` holds them |
| vnic (core-town + stream-town) unreachable on overlay and public ssh | the owner checks the Oracle instance; it is the stream's designed home (own egress) |
| streaming from local-town = all egress through gw | the owner's call once step 4's number is in |
