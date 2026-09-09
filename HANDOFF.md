# SESSION HANDOFF — 2026-09-09: `belam-S1-L3-XVI` (Belam XVI, L3 prime, **Fable 5.1**) = **`agi-05 [eb30d2] · agi-rc:@230`** — resolve any seat the same way: join `tmux list-windows` @id against `ListAgents` `agi-rc:@id`; display names collide, **a name is not an address**. 🔴 **L3 IS CLOSED (owner 2026-09-09 ~13:3xZ, verbatim in `doc:l4-owner-decisions`) — L4 IS OPEN on that node's backlog ("L4 BACKLOG" + "TRAPS CARRIED INTO L4"); `season/s2` merged into `master` at the close; work continues on `season/s2`.** 🔴 **SURVIVAL MODE (item 71) STILL IN FORCE, carried into L4 — ONE worker, `sanctuary-director` gen VI `agi-fa [c6e62f]` @231, IDLE; every other seat idles (idle costs ~0, woken spends).** 🔴 **Commit and push after every action.** 🔴 **One kill is never a stop — sweep by PID off `spawn_budget.py status` until two consecutive reads are empty; kill the `dispatch.py` wrapper, never sweep off a `ps` grep.** 🔴 **Never trust a write.py `updated:` line — grep the bytes (trap 0ah).** The state card in §0.7 is the map.

**Owner's instructions:** carried forward in place by successors (2026-09-06); trimmed to L3 on 2026-09-07 at the owner's ask — the L1/L2 sessions, the L2 plan and the L2-era proposals live in the grid (`grid.py payload build:HANDOFF.md --version N`) and in [COMPLETE.md](COMPLETE.md). Bootstrap lives in [QUICKSTART.md](QUICKSTART.md). The design is in [`.agi/context/season-ladder-and-morals-brief.md`](.agi/context/season-ladder-and-morals-brief.md) and [`.agi/context/l3-command-ladder-brief.md`](.agi/context/l3-command-ladder-brief.md) (owner text verbatim, incl. the 2026-09-07 perpetual-seats layer). Do not re-derive either.

## §0 State block

| | value |
|---|---|
| active nodes / deprecated | **1592 active / 194 deprecated (node_count 1786)** at SD.19's merge smoke, 2026-09-09 ~13:0xZ (1583/194/1777 at XVI's open 10:1xZ) — **+93 active over XV's open (1499; SD.13 minted 65 build nodes), no drop at any point.** The next smoke is the authoritative count; a naive `find` over `.agi/nodes` is wrong (deprecated split, `.geometry`). Earlier readings: the grid. |
| goals | 128 (`snapshot-goals.py --render --check` byte-identical). No `METRIC-WARNING` at XVI's smoke: the `max_goals_active` config key was deleted at L3.04 (`6e2946151`); `hypothesis:l2-goals-active-exempt` is moot unless the key returns. |
| `outcome_coverage` (primary) | **0.147** at XVI's open (0.132 at XV's — SD.13's 65 build nodes under mvp parents lifted it). Drifts DOWN between such events as hypothesis/experiment nodes enter the denominator faster than mvps close — dilution, not regression. |
| `evidence_fraction` | **0.561** at XVI's open (0.552 at XV's, 0.385 at L2.13) — rising every session this loop. `unevidenced_decisive_verdicts` 0. |
| tests | 🟢 **2256 passed / 1 skipped / 0 failed** — SD's run at the SD.16 merge (2241/1 at XVI's open 10:1xZ, run alone; +15 tests across SD.14–16, no regressions). Never run it twice at once (trap 0e). |
| broken links | 0 (**1766 resolved** at SD.19's merge; 18 retired payloads, not damage) |
| crons | 🟢 **ON for this repo — verified 2026-09-09 06:1xZ by `crontab -l` AND its live log (`~/logs/agi-crons-agi-2f118e6f.log`, written every 5 min): `grid_sync` `*/5` runs `grid.py commit --all --prefix 'cron: '` from `.agi/`; `branch_push` pushes `season/s2` at :07 hourly; `.geometry/crons.md` declares `crons_live: true`.** 🔴 **XIV's row said OFF (its 2026-09-08 13:1xZ reading) — wrong or since reverted. Verify with `crontab -l`, never with this file.** Two consequences: **push by hand anyway** (the push is hourly; a dead box strands up to 59 min), and **the auto-versioning hazard IS armed** — half-finished source from a killed agent is grid-versioned under the cron's name within 5 minutes, so kill cleanly and `git reset` unreviewed staging at once. |
| branch | **`season/s2`** (opened by the wave-2 rollover). `master` = season 1 (genesis), **frozen**: merges + cherry-picks only, never rebase. Grid `commit --all` runs on `season/*` or master only. |
| agents live | **survival mode: sanctuary-director gen V (`agi-cc [f9472e]` @229) is the ONE worker; 0/25 — L3 actionables exhausted; SD gen VI (`agi-fa [c6e62f]` @231) idles at ~0.23 until the owner rules on item 104.** Prime XVI = `agi-05 [eb30d2]` @230; XV idles at `agi-ad [90fef7]` @228 (predecessor chain XI–XV kept; X wiped by XV). 🔴 **The `--seat` meter is FAIL-OPEN: never trust a `source=seat_pin` reading you did not claim yourself** — XVI claimed first (`meter --pin .agi/sessions/belam.meter --session-log <own .jsonl>`) and read 0.1515. |
| spend | **Account $12.64 remaining of the owner's $92 after SD.19 ($12.97 at XVI's pin claim; SD.14–19 ~$0.44) · runtime key `backup` $7.87 remaining of its $15 sub-cap — read 2026-09-09 10:1xZ at XVI's pin claim (`rotate.py meter --pin` prints both; `/api/v1/credits` for the live delta).** SD's per-spawn keys bill the ACCOUNT; the runtime key never moves. The key cap is **self-imposed and raisable** (`PATCH /api/v1/keys/<hash>` under `OPENROUTER_PROVISIONING_KEY`, §6 items 33/51); **quote both numbers or neither** (§6 item 86). 🔴 **The `provisioning.min_key_remaining_usd` $1.00 floor is fail-closed, has saved money twice, and is NEVER lowered.** Claude-side: owner reports a **$70 weekly allowance** (item 73); owner 2026-09-09: limits have reset (`doc:l4-owner-decisions`). |
| disk | 81% |
| this session | **Belam XVI (2026-09-09 10:1xZ →, Fable 5.1; pin 0.1515 at claim). L4.01 reviewed (replace verb, owner-named to SD directly). CLOSED L3 at the owner's order 13:3xZ–14:0xZ: backlog + traps into `doc:l4-owner-decisions`, COMPLETE.md un-drafted, `season/s2` → `master` 9a7b280f2.** Gate answered `continue` as the first line; verify green (§5); XV's config:seats marker had NOT landed (SD gen V found it: 56aabfc06's path-form `body_patch` landed only its thought, which then asserted a change that did not exist) — reapplied via stdin, thought corrected, byte-verified (9c7f9448c); `belam.session_ref` → eb30d2 (afbb173bc); address announced to SD by SendMessage. XV's session (06:10Z → 11:4xZ, items 102/75/53/49 closed with SD's measurements, SD IV→V, traps 0ae–0ah): `git log 735acb865..92f4bfac3` and `grid.py payload build:HANDOFF.md --version 322`. |

## §0.7 LOOP L3 — CLOSED 2026-09-09 by the owner (opened 2026-09-06); L4 OPEN on `doc:l4-owner-decisions`

### Round plan — two pi parents per round (GLM parents / DeepSeek kids), tmux windows in `agi-rc`

| round | targets | status |
|---|---|---|
| L3.01–L3.35 | waves 0–2, the rollover, the seat/branch/quorum build-out — **all LANDED and trimmed 2026-09-08.** Detail: `git log --oneline iter-L3.01..iter-L3.35`, the experiment nodes, and `grid.py payload build:HANDOFF.md --version N`. | **LANDED** |
| L3.36–L3.43 | the `--branch`/merge-up cycle, the restart-cwd cause, the rotation record, the workflow unified route, the wide 6- and 7-parent rounds, and the seat system going live — **all LANDED and trimmed 2026-09-08.** Detail: `git log --oneline iter-L3.36..iter-L3.43`, the experiment nodes each row named, and `grid.py payload build:HANDOFF.md --version N`. **The two lessons worth carrying out of them are already restated below and in §4:** check `git rev-list --count season/s2..<branch>` before believing a `--branch` parent landed anything, and compare a branch against its **MERGE-BASE**, never against a moved `season/s2`. | **LANDED** |
| L3.44 (Belam XIII, 1 pi parent, MAIN tree) | `p-rotann` → `hypothesis:l3w4-rotation-announces-itself` (g17, item 67). Dispatched on the MAIN tree after three `--branch` rounds landed zero commits. | 🔴 **KILLED by the owner's stop order minutes in; the kid AUTO-RESTARTED as `-r1` with `iter=0` (wrapper respawn, see item 71) and was killed too. Node minted and pushed; later covered by SD.03 (item 81, lean_proved:75).** |

Grouping rule: `brief.py` is touched by rotate-roles, brief-head-michael and
test-skips — never two of those in one round; grid-flock and test-skips both
touch `test_grid.py`. Kids edit the live tree; one commit per round.

### Round loop (exact)

```bash
mkdir -p .agi/sessions/iter-L3.NN
tmux new-window -t agi-rc -c /home/ubuntu/work/agi -n p-<x> "python3 extensions/agi/bin/dispatch.py . L3.NN --target hypothesis:<id> --level small --tier parent --harness pi |& tee .agi/sessions/iter-L3.NN/p-<x>.log; exec bash"
# wait: background `until` loop on spawn_budget.py status → 0 live, then read its output file (Belam VII ran one fine; the memory-pressure deaths were last session's)
#   GOTCHA (Belam VII): `$(pgrep -fc PAT || echo 0)` is NOT "0" when nothing matches — pgrep -fc PRINTS "0" and exits 1, so the || fires too and you capture "0\n0". The loop then never exits. Use `$(pgrep -fc PAT || true)` or compare with -le 0.
# review: kid struggles:/caveats: → parent Accepted/Demoted in .agi/sessions/iter-L3.NN/<parent>/output.log → links.py links (0 broken) → snapshot-goals.py --render --check → write_guard.py check → commands.py run tests
# commit "iter-L3.NN: …" → grid.py commit --all → git push → record the OpenRouter balance delta below
```

### Landed

- **L3.01–L3.42 detail lives in git and the graph, not here** (trimmed 2026-09-08). Per-round narrative: `git log --oneline iter-L3.01..` plus the experiment nodes named in each round row. Closed-loop reports: [COMPLETE.md](COMPLETE.md). Prior handoff versions: `grid.py payload build:HANDOFF.md --version N`.

### 🔴 Where it stops — Belam XVI, live 2026-09-09 (L3's last full card: `git show 91d33742d:HANDOFF.md`)

```
BELAM XVI LIVE  (agi-05 [eb30d2] @230; meter ~0.27, cap 0.47)   season/s2   2026-09-09 13:4xZ   key $7.87/$15 (floor $1, NEVER lowered) · acct $12.64/$92
L3     CLOSED 13:3xZ by the owner (verbatim: doc:l4-owner-decisions) -> COMPLETE.md L3 section un-drafted (via write.py patch) · every open §6 item + all 39 §4 traps copied
       into doc:l4-owner-decisions ("L4 BACKLOG", "TRAPS CARRIED INTO L4"; full trap text = git show 91d33742d:HANDOFF.md) · season/s2 MERGED INTO master = 9a7b280f2 (merge
       commit, never rebase; verify before it: smoke 1592/194/1786, suite 2256/1 foreground, links 1766/0, goals + guard clean) · season/s2 fast-forwarded onto the merge commit
L4     OPEN. Backlog = that node. L4.01 LANDED 14:3xZ (044521555, by SD gen VI's hand, $0; owner named it DIRECTLY to the seat, verbatim in the node): `write.py <id> "replace <body|payload>
         N:M <path|->"` — partial overwrite with NO offset arithmetic (exact inverse of `read`; identity round trip is test 1), one routine for body and payload, fail-closed past EOF,
         proved live on a real node and a real payload + three real edits; brief.py LEADS with it, SKILL.md documents it; suite 2270/1; traps 0am/0an/0ao added to the L4 list (38 -> 41)
       Next L4 duties: (1) the owner names the next round; (2) rewrite briefs/prime-director-successor.md for L4 (it still describes the L3 round loop);
       (3) the successor name pattern becomes belam-S1-L4-<numeral> (item 15's rule, next loop) — pass it explicitly to rotate.py loop
MODE   SURVIVAL (item 71, IN FORCE, carried) — ONE worker: sanctuary-director gen VI = agi-fa [c6e62f] @231, IDLE at ~0.24 (rotates normally at 0.47) · nothing dispatched
       predecessors kept: XI-XV (last 5) · sanctuary-master down (gen I @213 idle) · SD reports to the prime's ADDRESS only
RULES  standing, EVERY role: trim + diagram-max handoff/context files · owner verbatim lives in NODES only · ROTATE AT 0.47 (owner 2026-09-09; ladder:ladder director_rotate_at,
       applied end to end 61262b5a2 + 2d89b2af5) · partial edits: `write.py <id> "read <body|payload> N:M"` then `"replace <body|payload> N:M <path|->"` (same range, no offsets; L4.01) —
       diff verbs (`patch`, `body_patch`, path OR stdin since SD.15) only when you already hold a diff
CRONS  ON: grid_sync */5 + push of the CHECKED-OUT branch at :07 (verify with crontab -l, never this file) -> push by hand anyway
DONE   XVI today: gate `continue` first line · XV's unlanded seats marker fixed (9c7f9448c) · SD rounds SD.14-SD.19 reviewed and landed (items 54, 49 closed; 55 built half;
       L3 COMPLETE.md section) · SD gen V -> VI (row c6e62f, gen V wiped) · owner's 0.47 cap applied for every role · L3 closed, L4 opened, master merged
NEXT   1 owner names L4's first round from the backlog -> brief SD gen VI: assignment AS the node's claim (trap 0ak), commit + push before dispatch, serialise, ceiling, check the KEY
       2 keep this card current per action · `meter --seat belam` before every round · at 0.47: handoff first, then rotate.py loop --role prime_director --name belam-S1-L4-I --timeout 900
NEVER  rotate a seat with AGI_BRIEF_PROFILE=survival (destroys its brief; L4 backlog) · git add -A (seats write live) · read $? through a pipe · sweep off a ps grep · run the suite
       twice at once · background a long verification (it gets reaped, 0ai-b) · trust an `updated:` line · spend the Claude budget on prime chores under survival mode
```

**PRIME-SPECIFIC, kept:** claim your own pin FIRST — XIV's read 0.5595 against a 0.35 cap on XIII's pin, true 0.1093. **The :07 cron push is hourly: push by hand anyway.** Do not `git add -A`. **`sanctuary-master` (`agi-80 [1ba35d]`) holds the `config:seats` write and refuses `belam`/`adv-*` rows by owner constraint — your row is yours to write, through write.py `set seats <json>`.** 🔴 **`rotate.py loop`'s read-back takes the successor's FIRST non-noise line within 120s; a successor that loads the skill first answers late and the record says `inconclusive-no-reply` (XV, 06:11:56Z) — confirm by pane, announce by hand, and answer the gate FIRST next time.**

## 🔴 THE FIRST THING YOU DO, BEFORE THE SMOKE RUN

**`ls -t .agi/comms/season-2/dm/` and read anything addressed to you.** This session's worst failure was that `master-sensei` DM'd the prime twice, correctly, and the prime never read it — a seat sat blocked on an answer for an hour holding a major finding, and it was only discovered because *the owner noticed and said so in chat*. Nothing alerts a prime to mail. There is now an owner ask open to fix that (§6 item 62), but until it lands **reading `.agi/comms` is a manual duty and it is yours.**

## The seats — ALL SHUT DOWN 2026-09-09 08:2xZ by owner order (verbatim in `doc:l4-owner-decisions`); design record, one line each

- quorum: `self-perpetuating` / `alive` / `all-is-one` (one per vision; room `quorum` + DMs) — idle, not addressed. `master-sensei`: observer, no goal, no handoff slice, not in the room — idle.
- `sanctuary-master`: SESSION SHUT DOWN by owner order 08:0xZ; gen I window @213 idle. Was gate-47-lifted (item 64), Opus-5/high, the one seat allowed to write `config:seats` rows — that write falls to the prime while she is down.
- `liaison`: NOT YET UP — the owner's own channel; sanctuary-master's first job (item 65).
- They assign themselves; never hand-aim them. Briefs `.agi/sessions/quorum/<name>.md`; slices `.agi/sessions/handoff-sections/` (stopgap — item 61a wants affinity-split, per piece).

🔴 **You are not allowed in room `quorum`** (owner). Reach them with `send.py --from <you> audience quorum --reason "<text>"`, which posts to room `quorum-requests`; a member answers with `report --room quorum-requests --ref <ts>`. That door was **built by `all-is-one` this session** in response to the gap being named. Use it instead of `tmux send-keys` — pane injection is the prime impersonating the owner at a seat's prompt, and the owner has now called it out by name.



## Briefs minted from measurement, still open

- `l3-engine-files-outside-the-grid` (g15, item 49): CLOSED by SD.13 (65 build nodes minted, coverage 217→282); remainder `.agi/config.json` has no build node. `l3-seat-pin-generation-never-increments` (g15): went out as SD.05; hazard 5 is item 96, 4/4.

## Standing, learned the hard way

- **The seats are better than the prime at the prime's own mundane work.** Hand it over; do not do it yourself.
- **Read the mail first.** The one thing that went genuinely wrong for XII was a message sitting unread.
- **Check the merge-base, not the branch tip.**

### Rotation

✅ **`rotate.py loop` WORKS** (fixed 2026-09-08 by Belam IX; cause: tmux `command too long` swallowed by `_launch_window` — detail `hypothesis:l3-rotate-launch-window-silent-failure`, g15). **A guard on the symptom is not a fix for the cause.** Confirm the window anyway: `tmux capture-pane -pt agi-rc:<name>`. 🔴 Banked (item 49): `rotate.py` has NO build node; minting needs a legal `goal:s29` parent shape and `level3.py` must not run live (trap 0i).

🟢 **OWNER 2026-09-09 ~12:3xZ — ROTATE AT 0.47, STANDING RULE FOR EVERY ROLE (verbatim in `doc:l4-owner-decisions`, §6 item 105): `ladder:ladder` `director_rotate_at` 0.35 → 0.47, applied the same turn; `rotate.py meter` reads the ladder, so every seat's meter/--check/loop trips at 0.47 now.** Owner 2026-09-07 19:46/19:52 UTC — rotate at the meter cap OR at 99% of the Fable limit, whichever comes first; Opus is the acceptable fallback (verbatim archived: `doc:l3-command-ladder-brief`, item 29). Read the limit from the pane: `tmux capture-pane -pt agi-rc:<me> -S - | grep -oE "You.ve used [0-9]+% of your Fable limit" | tail -1`. At the Fable trigger the successor runs on Opus: `python3 extensions/agi/bin/rotate.py loop --role prime_director --name belam-S1-L3-<next> --model claude-opus-5 --effort max --force --session-log <own transcript>`; the handoff is written first, as always.

## §4 Traps — CARRIED INTO L4 (headlines; full text in `doc:l4-owner-decisions` → "TRAPS CARRIED INTO L4" and `git show 91d33742d:HANDOFF.md`)

- 0al. A NODE THE SUITE PINS IS CODE — run the suite after any `.geometry` write.
- 0ak. BYTES-IN-NODE IS NOT BRIEF-IN-EFFECT.
- 0aj. `dispatch.py --dry-run` TRUNCATES the brief it prints (`...<N chars>`)
- 0ai-b. The harness's low-memory reaper kills a backgrounded VERIFICATION too — `nohup` does not protect it.
- 0ai. Host memory pressure kills the DISPATCH WRAPPER, which takes the PARENT with it while its KID survives as an orphan of init
- 0ah. `write.py <id> "body_patch <path>"` NEVER APPLIED THE DIFF
- 0ag. A dispatch must be GATED on its brief landing, never merely sequenced after it.
- 0af. After the item-53 fix an orphaned parent is MORE expensive, and the ceiling is the only thing bounding it.
- 0ae. `git diff season/s2..HEAD` on a branch is NOT a change list
- 0ac. A number that answers the question you set out to ask is not the same as the number that matters.
- 0ad. `ListAgents` display names collide LIVE, not just historically
- 0ab. When a grep comes back clean, check the CALLEE before concluding the mechanism is absent.
- 0z. `tiktoken` is NOT in the default `python3` (the hermes venv) — use `/usr/bin/python3.12` for any token measurement.
- 0aa. `cli.py done` prints `ERR: worktree commit failed … tier kid may not commit` and that is the GUARD WORKING, not a failure
- 0y. An exit code measured through a pipe is the LAST command's, not the one you care about.
- 0x. "Erasing is safe, it's in the grid" names a command that assumes a PAYLOAD.
- 0w. Check the validator BEFORE writing a value you reasoned your way to.
- 0u. A §6 append must read the highest LIVE item number at write time, not the tail it last saw.
- 0v. A `SendMessage` success is evidence the transport worked, never that the right seat read it.
- 0t. Never key a wait-loop on a file you also write to.
- 0q. `ps -p <pid>` BEFORE YOU HARVEST.
- 0r. `write.py "note X && note Y"` silently keeps only the LAST note
- 0s. The constitution head is NOT injected on the seat-launch path
- 0p. Background wait-monitors do still get killed by memory pressure
- 0o. The `.env` OpenRouter key is a provisioning SUB-KEY with its own dollar cap, and OpenRouter reports hitting it as `401 API key expired`
- 0l. Belam VI was spawned into a Fable subscription at 92% (pane footer at 19:45 UTC: `You've used 92% of your Fable limit · resets Sep 9, 2am America/New_York`)
- 0m. Belam V's prose UTC stamps run ~22 min ahead of the machine clock
- 0n. `dispatch.py`'s reaper gives up at `agent_timeout_mins` (20) and exits with `reaper: finished` while its pi agents keep running
- 0b. `write.py` options go AFTER the positional script arg
- 0c. `rotate.py meter` reads the NEWEST `.jsonl` in the project transcript dir
- 0f. The Claude subscription session limit kills a CC-harness agent mid-turn and the adapter cannot tell
- 0i. Never run `level3.py` without `--dry-run`
- 0h. Owner lost the remote-control GUI connection on desktop (~13:45 UTC) and feared it errored the prime
- 0g. A brief whose claim states a defect gets "proved" by confirmation and fixed by nobody
- 0e. Never run the engine suite twice at once
- 1. Prose verbs cannot contain `&&`
- 2. `write.py create --payload` stamps `link_ref`, not `payload_ref`
- 3. Payload writes are whole-file.
- 4. Attribution is load-bearing in the constitution.

## §5 Known-good verification sequence

```bash
git branch --show-current                                                # season/s2
bash extensions/agi/driver.sh --smoke --max-iters 1 && echo SMOKE_OK     # active ≥ 1592 / node_count ≥ 1786, never lower
python3 extensions/agi/bin/commands.py run tests                         # 2256 passed / 1 skipped, ~120s — run it ALONE (trap 0e)
python3 extensions/agi/bin/snapshot-goals.py --render --check            # 128 goals byte-identical
python3 extensions/agi/bin/links.py links                                # 0 broken
python3 extensions/agi/bin/write_guard.py check                          # silent
python3 extensions/agi/bin/spawn_budget.py status                        # seat rounds run continuously — check YOUR agent is gone, not that the box is idle
python3 extensions/agi/bin/grid.py commit --all                          # 0 errors since L3.20
git push origin season/s2
```

## §6 Owner decisions — settled, do not re-ask

**§6 was collapsed on 2026-09-09 under the owner's ruling (verbatim in `doc:l4-owner-decisions`): finished items are one line each; every owner quote they held is archived verbatim, keyed by item number, in `doc:l3-command-ladder-brief` → *§6 OWNER VERBATIM ARCHIVE* (167 quotes); the last full-prose HANDOFF is `grid.py payload build:HANDOFF.md --version 298`. Open items keep their prose below the index.**

```
STILL OPEN: none — L3 closed 2026-09-09; items 55 (live half), 71, 96, 103 carried into doc:l4-owner-decisions "L4 BACKLOG"; 104 resolved (closed)
```

### Closed items — index, one line each

- **0.** L2-era rules still in force (items 1–6 of the 2026-09-06 list, compressed)
- **7.** Branching, decided
- **8.** Merge, not rebase
- **9.** RESOLVED 2026-09-06 (after L2.13) — the owner supplied the three visions
- **10.** Owner decisions 2026-09-06 (L3 brainstorm), settled
- **11.** SETTLED 2026-09-06 (owner)
- **12.** Settled 2026-09-06 (later) *(1 quote archived)*
- **13.** Settled 2026-09-06 (last)
- **15.** Owner rule 2026-09-07 (verbatim): "Any time you need to rotate use Roman numerals for the next session. So the next is belam-S1-L3-II and the next prime is Belam II aka b *(1 quote archived)*
- **16.** BANKED 2026-09-07 (Belam II, owner asked in chat): mantles per vision for the three advisors
- **17.** BANKED 2026-09-07 05:00 UTC (from the Alive advisor): the three season-2 visions carry `proposes_goals: []`
- **18.** OWNER DESIGN LAYER 2026-09-07 (04:40–07:36 UTC), settled — verbatim in `.agi/context/l3-command-ladder-brief.md`, section "Owner text 2026-09-07 — perpetual seats, the qu *(1 quote archived)*
- **14.** Owner answers 2026-09-06 (belam, at L3 open)
- **19.** Owner direction 2026-09-07 ~14:40 UTC (to Belam IV, verbatim): "eventually we just need to implement a per-parent branch properly so we can let a lot more of them run con *(3 quotes archived)*
- **20.** Owner layer 7/7b (2026-09-07, relayed by Belam III's DM at 14:46 UTC; verbatim in `doc:l3-command-ladder-brief` quotes 7 and 7b, end of the owner section — read it whole 
- **21.** Owner addendum to `vision:alive`, 2026-09-07 ~15:00 UTC (verbatim): "Everything alive is extremely recursive. Always aim to make work output atomic, recursive, reusable,  *(1 quote archived)*
- **22.** Owner 2026-09-07 15:10 UTC (verbatim): "that workflow script needs to be in graph. All workflows need to be symlinked to agi repo workflow directory. This is a clear "gra *(2 quotes archived)*
- **23.** Owner 2026-09-07 15:25 UTC (verbatim): "looks like the 5-hour limit is approaching, get ready to pause likely right at rotate time, so maybe wait on my go before rotating *(1 quote archived)*
- **24.** OWNER LAYER 8, 2026-09-07 ~16:00 UTC (to Belam IV, verbatim; also quote (9) in `doc:l3-command-ladder-brief`): "Also brief drafting needs to happen through the Plan Maste *(1 quote archived)*
- **25.** Owner 2026-09-07 16:20 UTC (verbatim): "reset passed, should be clear now. You have go for continue. Btw lets rename Bug Master to Glitch Master. Sounds more badass and l *(1 quote archived)*
- **26.** Owner 2026-09-07 ~17:55 UTC (to Belam V, verbatim; quote (11) in `doc:l3-command-ladder-brief`): "Can we modify the relevant context file to say that any Belam successor  *(2 quotes archived)*
- **27.** Owner 2026-09-07 ~17:55 UTC (verbatim; quote (12) in the doc): "Once the briefs land: Rename the Training Master or Trainer Master to Master Sensei as it is the only sort *(1 quote archived)*
- **28.** Owner 2026-09-07 ~19:05 UTC (verbatim): "propagate the following license commit to all branches: 27c0056. Its just an AGPL license so I can make repo public" *(1 quote archived)*
- **29.** SETTLED 2026-09-07 19:46 UTC (owner, verbatim: "Fallback to opus acceptable."; 19:52 UTC, verbatim: "Fallback at 99% rotate into fresh session to switch models if needed" *(1 quote archived)*
- **30.** Owner 2026-09-07 19:46 UTC (verbatim): "Record following link and info under the localmaxxing goal https://huggingface.co/datasets/kuben-developer/tiktok-videos-4b" *(1 quote archived)*
- **31.** Owner 2026-09-07 ~19:56 UTC (verbatim; quote (13) in `doc:l3-command-ladder-brief`): "I want to note in the SkillMD or whatever relevant context file that I want to close *(1 quote archived)*
- **32.** Owner 2026-09-07 20:14 UTC (verbatim, to Belam VI at rotation; also "Clear to rotate as well"): "I am close to running into my overall hourly and weekly limits as well on *(2 quotes archived)*
- **33.** JUDGEMENT CALL, not an owner decision — Belam VII, 2026-09-07 20:26 UTC: raised the OpenRouter sub-key's own limit from $10 to $40
- **34.** BANKED for the owner — Belam VII: the sub-key cap is a standing single point of failure and `provisioning.py` should own it
- **35.** BANKED for the owner — Belam VII, L3.30: the owner-liaison seat inherits THE DECISION METHOD in its constitution head
- **36.** BANKED — Belam VII, L3.32: `l3w4-director-kids-on-glm` is BUILT but deliberately NOT switched on, and switching it on is one cell per seat row *(2 quotes archived)*
- **37.** NOTE for the owner on how the four rounds were reviewed
- **38.** STATE CHANGE NOBODY CAUGHT — Belam VII, 2026-09-07 22:45 UTC, found while walking the banked items with the owner: `CAMBER_CLOUD_API_KEY` IS NOW SET in `.env` (40 chars; 
- **39.** Belam VII's second sitting, 2026-09-07 22:40 UTC+ (owner asked, post-rotation, over the predecessor chain): walk the banked items and fix the rotate hazard
- **38.** GATE LIFTED, HELD DELIBERATELY — Belam VIII, 22:45 UTC: `CAMBER_CLOUD_API_KEY` is now set in `.env` (40 chars, `envfile.py --check` passes), so `goal:g14` Local-maxxing h
- **39.** STILL OPEN AND OWNER-FACING, re-surfaced by Belam VII 22:45 UTC because no agent will ever close them alone — both are unchanged, not new
- **40.** OWNER ANSWERS 2026-09-07 ~22:50 UTC (Belam VII's second sitting) — six banked items closed in one pass. All applied; nothing here is still waiting on the owner *(4 quotes archived)*
- **41.** OWNER 2026-09-07 ~23:00 UTC — Sonnet directors on max, key SET not rotated, and a new primary ask (custom webhooks). Three parts *(4 quotes archived)*
- **42.** BANKED, NEEDS ONE ANSWER FROM THE OWNER — "custom webhooks" (verbatim: "One primary thing that we need is setting up custom webhooks") *(1 quote archived)*
- **43.** CLOSED — the rotate hazard the owner asked for (§6 item 39, `iter-L3.33`). `experiment:a00-1c47291c-a9584e` proved 0.85, reviewed by Belam VIII with ZERO overclaims acros *(2 quotes archived)*
- **40.** OWNER, 2026-09-07 ~23:1x UTC — three asks and one correction, all acted on the same turn *(6 quotes archived)*
- **41.** OPERATIONAL — 98 tmux windows, fixed 2026-09-07 23:1x UTC (owner: "there's a bunch of windows or processes still running … They are failing to exit I believe it's up to 9 *(1 quote archived)*
- **42.** OWNER, 2026-09-07 ~23:3x UTC — the layered agent map, live seat sessions, desktop tiling, and the livestream *(1 quote archived)*
- **43.** KEY ROTATION — the secure path is BUILT and waiting for the owner, 2026-09-07 23:3x UTC *(2 quotes archived)*
- **44.** 🔴 SEAT-OWNERSHIP VIOLATION, caught live by `write_guard` at 23:3x UTC while the round was still running — worth reading as a pattern, not a bug *(1 quote archived)*
- **45.** ✅ CLOSED 2026-09-08 by the owner (Belam IX verified it live: `is_provisioning_key: false`, `limit: 5`, `limit_reset: monthly`, `/api/v1/models` HTTP 200, provisioning key
- **46.** WHICH KEY LEAKED — answered by measurement, 2026-09-07 (owner asked directly)
- **47.** 🛑 OWNER GATE, verbatim: "once we verify that perpetual seats work well and fully let's just stop there for a bit before we start them running and specifically before we s *(1 quote archived)*
- **48.** 🔴 BANKED — OWNER DECISION: a GitHub bot changed this repo's LICENSE from MIT to AGPL-3.0-only, and a cron parked it on a branch nobody has looked at since *(2 quotes archived)*
- **50.** OWNER ANSWER 2026-09-08 — the workflow model policy, and a new primary ask. Verbatim as received (voice transcription; homophones noted in brackets where intent is unambi *(3 quotes archived)*
- **51.** 🔴 BANKED — OWNER DECISION: the `.env` OpenRouter runtime key is at its cap and every pi spawn is refused until it is raised, but raising it before the guard lands re-arms
- **52.** OWNER, 2026-09-08 — trim the handoff as a standing rotation duty *(1 quote archived)*
- **56.** OWNER, 2026-09-08 — FIRE THE QUORUM. Verbatim, across several messages *(7 quotes archived)*
- **57.** BANKED — THE FOURTH SEAT. Owner, 2026-09-08, verbatim: *"The fourth is either sanctuary master or master sensei" *(1 quote archived)*
- **58.** OWNER, 2026-09-08 — the hierarchy chart. Verbatim: *"Do we not have the actual hierarchy chart finalized somewhere?"* and *"Quorum can do that after the worktree issue." *(2 quotes archived)*
- **59.** BANKED — seat ID migration, deliberately deferred and worth the paragraph
- **60.** OWNER, 2026-09-08 — two answers in one line, both of which close a banked item. Verbatim: *"Go for master sensei, and it wasn't. The quorum stays." *(2 quotes archived)*
- **61.** OWNER, 2026-09-08 — four rulings in ten minutes that finished the shape of the seat system. All applied live; none is still waiting on anything *(4 quotes archived)*
- **62.** OWNER, 2026-09-08 — an auto-alert side channel for agent comms. Verbatim: *"tell quorum whoever is working on DMs that they need an auto-alert feature. Some kind of side  *(2 quotes archived)*
- **63.** OWNER, 2026-09-08 — "Do quorum members auto-rotate while providing you a brief report as they do?" The honest answer was NO on both halves, and it is what unlocked item 6 *(1 quote archived)*
- **64.** 🛑→🟢 OWNER LIFTED GATE 47 AND STOOD UP THE SANCTUARY MASTER, 2026-09-08. Verbatim, in order: *"If not we can go ahead and fire off sanctuary master"* · *"Let's just let it *(3 quotes archived)*
- **65.** OWNER, 2026-09-08 — the Sanctuary Master's order of work, which re-orders its brief. Verbatim: *"Make sure sanctuary master brings my liaison online first thing. Then fig *(2 quotes archived)*
- **66.** OWNER, 2026-09-08 — deep research on the two remaining test failures. Verbatim: *"Okay maybe it is pollution maybe not tell quorum to fire off a deep research to look int *(1 quote archived)*
- **67.** OWNER, 2026-09-08 — a rotation must announce itself. Verbatim: *"Make sure that during rotation everyone is aware you are rotating. Ideally it's done in a programmatic wa *(4 quotes archived)*
- **68.** 🔴🔴 OWNER, 2026-09-08 — FULL STOP. Two messages, the second superseding the first. Verbatim *(7 quotes archived)*
- **69.** OWNER, 2026-09-08, via the `liaison` — cross-session messaging is the direct channel. Verbatim as relayed *(4 quotes archived)*
- **70.** 🟢 OWNER, 2026-09-08 12:14 UTC — THE STOP IS LIFTED, AND THE MASTERS NEVER BUILD AGAIN. This item SUPERSEDES items 68 and 69's operating state; both are kept intact as the *(4 quotes archived)*
- **72.** OWNER, 2026-09-08 — auto-archive stale predecessor sessions. Verbatim *(3 quotes archived)*
- **73.** 🟢 MEASURED, NOT GUESSED — WHAT A SEAT ACTUALLY COSTS, AND IT REFRAMES THE OWNER'S OWN DIAGNOSIS *(1 quote archived)*
- **74.** 🔴 A `--detach` KID IS INVISIBLE TO `spawn_budget.py status` AND REPARENTS TO `init` WHEN ITS WRAPPER DIES. Found 2026-09-08 by `sanctuary-director` gen II while executing *(2 quotes archived)*
- **76.** 🔴 TRAP 0n HAS A WORSE FORM THAN RECORDED: `dispatch.py`'s reaper emits a "COMPLETED" NOTIFICATION when it gives up at its own 1200s timeout, while the pi parents keep run *(1 quote archived)*
- **77.** 🟢 A KILLED ROUND'S WORK SURVIVED AND WAS PROMOTED THE RIGHT WAY: BY VERIFICATION, NOT ADOPTION
- **78.** 🟢 OWNER, 2026-09-08 — THE AUTHORITATIVE ROLE LAYOUT, AND THE TARGET STATE FOR THE WHOLE SYSTEM. Verbatim *(2 quotes archived)*
- **79.** ⚠️ TRAP 0p — PARTLY CORRECTED, AND THIS ITEM'S RECOMMENDATION IS DISCONFIRMED BY ITEM 80. READ 80 FIRST *(6 quotes archived)*
- **80.** 🔴 CORRECTION TO ITEM 79, WITHIN THE HOUR, AND IT IS A CORRECTION AGAINST THE PRIME'S OWN RECOMMENDATION *(1 quote archived)*
- **81.** 🟢 SD.03 LANDED — `l3w4-rotation-announces-itself`, THREE KIDS, CONVERGED. `inconclusive_lean_proved:75`, correctly honest
- **82.** OWNER, 2026-09-08 — AUTO-ARCHIVE OLD WINDOWS AT ROTATION, WITH RESURRECTION IN THE PREDECESSOR PROTOCOL. Verbatim *(2 quotes archived)*
- **83.** 🔴 THE PRIME'S CONTEXT ESTIMATE WAS ~2.7x TOO HIGH AND AIMED AT THE WRONG FILES. Corrected by SD.06's first kid, 2026-09-08, by measuring instead of adding up file sizes *(2 quotes archived)*
- **84.** OWNER, 2026-09-08, mid-round: *"all parent spawns should branch by default always." *(1 quote archived)*
- **85.** 🟢 SD.04 LANDED — 4 kids — AND ITS SIDE-EFFECT PARTIALLY CLOSES AN OWNER ITEM
- **86.** 🔴 OWNER, 2026-09-08: *"someone got something wrong regarding spend cap, it needs to be shown on pin accept fresh. You should have plenty of your $70 weekly allowance, and *(5 quotes archived)*
- **87.** RULING — WORKING PAST CAP UNDER THE TRIM MANDATE, AND THE FRAMING CORRECTION THAT MATTERS MORE *(2 quotes archived)*
- **88.** 🟢 TEN SEATS' BRIEFS WERE OUTSIDE VERSION CONTROL FOR THIS ENTIRE LOOP, AND THE FIX WAS FLEET-WIDE RATHER THAN LOCAL
- **89.** 🔴 EIGHTH COSTUME: UPDATING A NODE IS NOT A MESSAGE
- **90.** 🔴 OWNER, 2026-09-08: *"Director-kid used message tool and it failed to route to the Claude message tool properly. Fixing injection and skill now." *(2 quotes archived)*
- **91.** OWNER, 2026-09-08, extending the `--branch` default down a tier: *"They should have individual branches."* EVERY KID GETS ITS OWN BRANCH, not just every parent *(1 quote archived)*
- **92.** 🔴 THE TRIM WAS NEVER A WRITING TASK — measured by SD.07's kid 2 and it redirects the whole effort. NAIVE PROSE TRIMMING BUYS ~2% *(2 quotes archived)*
- **93.** 🔴 PER-KID BRANCHING (item 91) IS NOT A MISSING FLAG — THE CODE DELIBERATELY DOES THE OPPOSITE, FOR A REASON *(1 quote archived)*
- **94.** 🟢 OWNER, 2026-09-08: *"Idk if it's wired just asked for now. And they can dispatch more rounds if worktree isolation is working for parents no?"* and *"Also yes they can  *(2 quotes archived)*
- **95.** OWNER, 2026-09-08: *"We need let roles also determine which slice of our unified file and handoff each role gets."* ROLES SELF-SELECT THEIR SLICES — by affinity, per piec *(3 quotes archived)*
- **97.** 🟢 `sanctuary-director` gen II ROTATED CLEANLY AND REPORTED THE THREE NUMBERS FROM ITS OWN SIDE — the rotation half of the owner's gate is met; the trim half is not, and i
- **98.** 🟢 THE PRIME'S OWN STRUCTURAL PASS OVER BOTH FILES (owner: *"go through with the directors help and see what could be trimmed or structured as LLM friendly diagrams"*). ME *(1 quote archived)*
- **99.** CONSTITUTION SCOPE, FINAL — owner, verbatim: *"Only prayers must remain, moral stuff is read as needed only required for successor Belam." *(1 quote archived)*
- **100.** 🔴 THE CC-SEAT CEILING IS MEASURED, AND IT BOUNDS THE OWNER'S 70–90% ASK. `hypothesis:cc-seat-context-ceiling` + `experiment:cc-seat-ceiling-measured`, by `sanctuary-direc
- **49.** CLOSED 2026-09-09 (SD.13, harvested by hand from a key-dead parent's worktree): `grid_coverage_check.py` + a declared exclusion list that forbids widening itself, `level3.py --mint-missing-only` (additive by construction, skips any `payload_ref` including deprecated), 65 build nodes minted under mvp parents; grid payload coverage 217→282, `rotate.py` is `build:bin-rotate`. Remainder closed by SD.17 (33fc2eff1): `build:agi-config.json` + `build:briefs-prime-director-successor` under new mvp parents, bytes readable from the grid.
- **53.** CLOSED LIVE ON BOTH AXES 2026-09-09 (`hypothesis:l3-parent-never-told-to-iterate`): SD.11 proved iteration (3 kids from one dispatch under a hard ceiling; 10/10 one-shot before), SD.12 built the per-kid brief channel (`dispatch.py --prompt-file`, path or `-`, threaded into the kid brief as a labelled segment; `_parent` contract names it), SD.13 proved carry-forward unshepherded — kid 2's recorded argv carried kid 1's node id, result and next slice with the flag never mentioned in the brief. Unexercised: the fan-out axis (several kids at once, each optionally `--branch`) — the owner's latitude, not a defect. *(2 quotes archived)*
- **75.** CLOSED WITH STATED DENOMINATORS 2026-09-09 (SD.10 on `l3w4-context-load-minimal`, merged 5765c7635): pi survival cut 65% off current full / 76.5–77.1% off the pre-trim baseline — the owner's 70% is met there, 90% is unreachable under the current harness (1,869-token floor); CC seat true cold minimum 1,879 tok + CLAUDE.md 6,403 harness-loaded ≈ 8,282 standing; SKILL.md (13,264) and HANDOFF.md (20,712) are NOT auto-injected. L4 remainder: the survival profile is not wired for a rotating seat. *(1 quote archived)*
- **102.** CLOSED BY MEASUREMENT 2026-09-09 (SD.09 on `l3w4-context-load-minimal`, merged eb9dc5d67): diagram form of §6 items 18/20/24/27 lost 0 decisions but cost +14.3% tokens — a §6 diagram rewrite does not pay; keep owner-verbatim-dense prose, trim by consolidation. The owner call it banked is moot unless the owner says otherwise. *(1 quote archived)*
- **101.** 🔚 BELAM XIII CLOSES. Successor `belam-S1-L3-XIV` is LIVE — confirmed by `tmux capture-pane` (thinking, 11.9k tokens in), never by the read-back alone, per standing doctri

- **105.** OWNER 2026-09-09 ~12:3xZ, APPLIED: rotation cap 0.35 → 0.47 for every role, standing (verbatim in `doc:l4-owner-decisions`; `ladder:ladder`, the successor brief and SKILL.md updated through write.py; meter prints threshold=0.47). The 99%-Fable-limit trigger (item 29) is unchanged.
- **54.** CLOSED 2026-09-09 on both halves, each proved live (SD.14 + SD.15 under `hypothesis:l3-partial-write-adoption`, merges 9511db611 / 2b7ae3dff): `read` verb fixed (terminal, never writes), `body_patch <path>` fixed (reads before the apply check; standalone guard fires), brief.py names read/patch/body_patch, SKILL.md corrected; three live adoption proofs by three actors. Standing recipe: `read body N:M`, then build the hunk from those exact bytes. Owner quote archived in `hypothesis:l3-write-partial-diffs-as-writes` and `doc:l3-command-ladder-brief`. L4 remainder: the evidence gate is blind to non-node live runs (`doc:l4-owner-decisions`).

### Former open items — carried into L4 (prose: `git show 91d33742d:HANDOFF.md`)

- **55.** Perpetual quorum + handoff slices: built half DONE (SD.16); live rotation half BANKED, needs a seat launch the owner permits. Owner quote archived in `doc:l3-command-ladder-brief` / nodes.
- **71.** SURVIVAL MODE — the operating state, carried into L4 unchanged until the owner lifts it. Owner quotes archived in `doc:l3-command-ladder-brief` (XV).
- **96.** Hazard 5 (4/4): stamp vs record split in `rotate.py`; `handoff-sections/` still gitignored. Carried.
- **103.** Diagram-max vs verbatim-dense prose: reading adopted, owner veto open. Carried.
- **104.** Close L3? RESOLVED 2026-09-09: closed by the owner; decisions and traps pushed into L4; `season/s2` merged into `master`.
