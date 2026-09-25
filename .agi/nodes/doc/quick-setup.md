---
id: doc:quick-setup
mint_id: aec6d5d6d6b64541b85e5b0d9028abde
type: doc
parents:
  - goal:g1.25
next_edges: []
edited_by: belam
scaffold_hash: eae2cd2781042856
season: 2
thought_session: belam-S2-L5-V
title: doc:quick-setup -- box setup + startup runbook (interim; the engine init route after the g1.25 registry)
town: local-maxxing
---
# doc:quick-setup

# doc:quick-setup — box setup + startup runbook (interim: becomes the engine's init route after the goal:g1.25 registry)

`QUICKSTART.md` (repo root) stays the clone / deps / install bootstrap; this doc is everything after it, in boot order. ✔ = verified on local-town 09-25 · TODO = a director-engine fill, file:line.

## 0. Boot order
```
box up ─▶ 1 memory guard ─▶ 2 streamer-stub units ─▶ 3 claude-remote-control (tmux agi-rc) ─▶ 4 seats: Prime, masters, directors
       ONE AT A TIME, MemAvailable >= 3 GiB between ─▶ 5 crons apply ─▶ 6 grid refs + branches ─▶ 7 Prime session crons ─▶ 8 verify
```

## 1. Memory ✔ (09-25, after the 04:00Z OOM took every seat down)
| piece | where | what |
|---|---|---|
| memguard | `/usr/local/sbin/agi-memguard.py` · system unit `agi-memguard.service` (enabled, OOMScoreAdjust=-1000, Nice=-10) | every 5 s: claude / tmux / ffmpeg / streamer-stub / launch-wrapper -> oom_score_adj -900 + nice -5 · pi workers -> +500 · SIGSTOP any process > 70% RAM, or the biggest unprotected one under 1 GiB free (resume: `kill -CONT <pid>`) · a >= 3 GiB drop in 30 s -> journal + `/var/log/agi-memguard.log` + [red] to belam (10-min limit) |
| no cascade | `~/.config/systemd/user/{claude-remote-control,streamer-stub,streamer-stub-watch}.service.d/10-agi-survival.conf`: `OOMPolicy=continue` | the default `stop` turned ONE OOM kill into stopping the unit, its tmux server and every seat |
| budget | box 15 GiB · stream ~5.3 GiB · a Claude seat ~0.4-0.8 GiB | PASS chunks wait for MemAvailable >= 1500 MB (launch.sh) · research reviews run under `systemd-run --user --property=MemoryMax=6G` |
| later | a reserved `agi-core.slice` (MemoryMin) for seats + stream | needs the units restarted into it: at a PLANNED restart, never live |

## 2. Streaming (✔ paths · TODO: the stub's own start order, from its README)
| piece | where |
|---|---|
| repo | `~/work/streamer-stub` (= /data/work/streamer-stub; `locations.streamer_stub` unset -> this default, locations.py:537) |
| units | `streamer-stub.service`, `streamer-stub-watch.service` (user units) |
| commands | `~/bin/sb-status` (read-only: hold.sh --status + panic.sh --status) · `~/bin/brb`, `~/bin/back` -> the stub's bin/hold.sh (argv[0] dispatch) · `~/bin/panic` -> bin/panic.sh |
| PATH | agents: `~/.local/bin/brb` only (their Bash shells lack ~/bin) · the owner: `/usr/local/bin/panic` |
| rules | brb = every post, by hand, then ONE [red] to belam · back = the owner (thought-master for its own brb) · panic = the owner only (commands.stream.fragment.md: owner_only) · never print a key, address or host name; never `ps -ef` / `pgrep -a` the relay (its argv holds the keys) · relay target delay 15m (owner: ~2 min) |

## 3. Seats: rows, keys, activation
| step | how |
|---|---|
| rows | config:seats = `.agi/nodes/.geometry/posts.md` (name, role, model, settings, pid, window, generation, session_id, session_name) · `rotate._load_seats(Path('.agi'))` |
| rotate | at the line: `python3 extensions/agi/bin/rotate.py rotate` (bare, keyed) -> handoff, successor spawn, the seat's key re-minted and its key row published to season2/main |
| wake | STARTUP runs config:rotations' first_turn entries · a RECOVERED seat's first act: `rotate.py ack --seat <seat> --gen <n> --ref <ref> continue` |
| keys | seat key per generation -> key row on season2/main (`send.py whois --key <pubkey> --claim <seat>` = IS-AUTHORIZED) · provider keys: `.env` at the MAIN root, `envfile.py --check`, per-spawn keys `provisioning.py status` (mint floor 1 USD) · TODO: the keygen verb for a brand-new seat |
| identity | resolved from the seat's tmux pane + row: a seat restarted outside its window reads 'unknown' (meter `no-post`) -> `send.py ... --from <seat>` and fix the row's pid / window |
| low-level | `rotate.py spawn --name --tier --model --effort --settings --prompt-file` (tmux only, no seat logic) |

## 4. Heal and the reaper
| piece | how |
|---|---|
| watch | `heal.py watch`: a row whose pid is dead -> `_watch_one_seat` -> `_recover_seat` respawns through the seat's own spawn path (the row's model / effort / settings), writes the row, records `rotations/<seat>.<ts>.json` crash-recovery |
| manual recovery ✔ | FIRST point every LIVE seat's row at its live pid / window (`rotate._successor_row_write`, pass session_name through) or the watcher spawns a second copy · then per dead seat: `heal._watch_one_seat(Path('.agi'), row, heal._all_windows(None), rotate, launcher=<wrapper>)`, the wrapper writing the built command to `/tmp/agi-recover-<seat>.sh` and handing tmux `bash <file>` |
| defects | `_launch_recovered` passes the whole prompt to tmux -> "command too long" (director-engine) · settings normalization FIXED 664d935157 |
| reaper | `heal.py pin-reap` + the rotation wrapper: after a join the predecessor's wrapper reaps its chain (~60 s); the after_join `[reap-proof]` line proves it · GAP: numeral-chain Prime windows are not reaped (gens I-IV lingered until 04:02Z) · TODO: pin-reap flags |

## 5. Crons
| piece | how |
|---|---|
| declared | `.agi/nodes/.geometry/crons.md` (crons_live + per-job schedules) -> `crons.py apply`; `crons.py show` |
| jobs | grid_sync every 5 min (grid commit --all ; ref push ; crons.py apply -- `;` so a failed push never blocks the heal) · branch_push hourly :07 · publish_engine / engine_push stay disabled |
| kill switch | `crons_live: false` (one edit); back on = one manual `crons.py apply` |
| Prime session crons | `.agi/sessions/prime-merge.crons.md`: CHECK "13 */4 * * *" + the PASS one-shot -- session-only, RE-ARMED at every wake |

## 6. Grid refs and branches
| piece | how |
|---|---|
| grid | `refs/grid/*` per node · `grid.py commit --all` (the cron; the Prime on season2/main after a merge) · `grid.py versions / payload / log / diff` |
| push | `grid.push_split_epoch` in `.agi/config.json` (a per-branch cell; this trunk 1789955640 -- never carried into another branch's config unexamined) · push-changed sends only tips origin lacks, <= 200 per push (a code default: hypothesis:grid-push-batch-limit-is-a-config-cell) |
| repair | a node without mint_id is never versioned: `backfill-mint-ids.py --write` |
| branches | directors LOCAL-ONLY (never push) · thought-master alone pushes `local-maxxing/season2/main` · belam pushes `season2/main` and fast-forwards `local-maxxing/main` to each PASS's reviewed TIP (owner 09-25) |

## 7. Verify (every boot)
`commands.py run verify` (bin-suite-fresh FAIL known) · `links.py links` (0 broken) · `snapshot-goals.py --render --check` · `spawn_budget.py status` · `provisioning.py status` · `crons.py show` · `sb-status` (rc only while live)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
2026-09-25 05:3xZ belam-S2-L5-V: OWNER verbatim: "Can we create a quick setup doc that includes all the startup instructions until we build a proper ini route. Things like key generation, post activation, heal use and how the reaper works, the memory allocation strategies, the streaming setup startup, any other set up stages like crons and proper grid ref pointing. It'll be a doc until it can be made engine. But that comes after registry because registry kinda includes all these routines that we can build on top." Parent goal:g1.25 (the registry) because the doc is that registry's seed. Written from what the Prime ran and verified on local-town 09-25 (the OOM recovery); the TODO rows (stub start order, keygen verb, pin-reap flags) go to director-engine rather than a Prime survey -- the owner asked for minimal token spend.
<!-- THOUGHT:END -->
