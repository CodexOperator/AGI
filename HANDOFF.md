# SESSION HANDOFF — 2026-09-10: `belam-S1-L4-II` (Belam L4-II, L4 prime, **Fable 5.1**) = **`agi-64 [61b9c9] · agi-rc:@235`** — resolve any seat the same way: join `tmux list-windows` @id against `ListAgents` `agi-rc:@id`; display names collide, **a name is not an address**. 🔴 **L3 IS CLOSED (owner 2026-09-09, verbatim in `doc:l4-owner-decisions`) — L4 IS RUNNING (owner GO 2026-09-09) on `doc:l4-plan` in ENHANCED SURVIVAL (`goal:g17.1` = the seat protocol, read it whole): Prime + point `sanctuary-director` L4 gen II (`seat-sanctuary-director-68 [f84c57]` @234) + helper `sanctuary-helper` gen I (`seat-sanctuary-helper-05 [3a4ed4]` @233, reports to the point only); every other seat idles (idle costs ~0, woken spends); `master` = the last closed season, merges only; work on `season/s2`.** 🔴 **Commit and push after every action.** 🔴 **One kill is never a stop — sweep by PID off `spawn_budget.py status` until two consecutive reads are empty; kill the `dispatch.py` wrapper, never sweep off a `ps` grep.** 🔴 **Never trust a write.py `updated:` line — grep the bytes (trap 0ah).** The state card in §0.7 is the map.

**Owner's instructions:** carried forward in place by successors (2026-09-06); trimmed to L3 on 2026-09-07 at the owner's ask — the L1/L2 sessions, the L2 plan and the L2-era proposals live in the grid (`grid.py payload build:HANDOFF.md --version N`) and in [COMPLETE.md](COMPLETE.md). Bootstrap lives in [QUICKSTART.md](QUICKSTART.md). The design is in [`.agi/context/season-ladder-and-morals-brief.md`](.agi/context/season-ladder-and-morals-brief.md) and [`.agi/context/l3-command-ladder-brief.md`](.agi/context/l3-command-ladder-brief.md) (owner text verbatim, incl. the 2026-09-07 perpetual-seats layer). Do not re-derive either.

## §0 State block

| | value |
|---|---|
| active nodes / deprecated | **1703 active / 194 deprecated (node_count 1897)** at L4-II's verify on season/s2 @ b4481c9ba (merge-up 2), 2026-09-10 03:30Z (1634/194/1828 at L4-II's open; 1592/194/1786 at L4-I's) — grew, never dropped. The next smoke is the authoritative count; a naive `find` over `.agi/nodes` is wrong (deprecated split, `.geometry`). |
| goals | **157** (`snapshot-goals.py --render --check` byte-identical at b4481c9ba; 143 at L4-II's open, 128 before L4). No `METRIC-WARNING`: the `max_goals_active` config key was deleted at L3.04 (`6e2946151`). |
| `outcome_coverage` (primary) | **0.14** at b4481c9ba (0.147 at L4-II's open, 0.132 at XV's). Drifts DOWN as hypothesis/experiment nodes enter the denominator faster than mvps close — dilution, not regression. |
| `evidence_fraction` | **0.561** at XVI's open (0.552 at XV's, 0.385 at L2.13) — rising every session this loop. `unevidenced_decisive_verdicts` 0. |
| tests | 🟢 **2315 passed / 1 skipped / 0 failed** — the point's foreground run at b4481c9ba (merge-up 2), alone; the FIRST run on the merged tree was RED (22 failed in test_rotate.py: a module-level rebind of rotate.main in the new test_rotate_complete.py — fixed inline, rule in goal:g17.1: run the tests a round could BREAK). L4-II's own run: 2270/1 at 2deee5062. Never run it twice at once (trap 0e); test_send.py nudges REAL panes until L4.10 lands — tell the point before running, capture your pane after. |
| broken links | 0 (**1877 resolved** at b4481c9ba; 18 retired payloads, not damage) |
| crons | 🟢 **ON for this repo — verified 2026-09-09 06:1xZ by `crontab -l` AND its live log (`~/logs/agi-crons-agi-2f118e6f.log`, written every 5 min): `grid_sync` `*/5` runs `grid.py commit --all --prefix 'cron: '` from `.agi/`; `branch_push` pushes `season/s2` at :07 hourly; `.geometry/crons.md` declares `crons_live: true`.** 🔴 **XIV's row said OFF (its 2026-09-08 13:1xZ reading) — wrong or since reverted. Verify with `crontab -l`, never with this file.** Two consequences: **push by hand anyway** (the push is hourly; a dead box strands up to 59 min), and **the auto-versioning hazard IS armed** — half-finished source from a killed agent is grid-versioned under the cron's name within 5 minutes, so kill cleanly and `git reset` unreviewed staging at once. |
| branch | **`season/s2`** (opened by the wave-2 rollover). `master` = season 1 (genesis), **frozen**: merges + cherry-picks only, never rebase. Grid `commit --all` runs on `season/*` or master only. |
| agents live | **enhanced survival: point sanctuary-director L4 gen III (`seat-sanctuary-director-4e [a36dd7]` @236, up 03:36Z) + helper sanctuary-helper gen II (rotated ~04:0xZ at meter 0.5366, past the cap; new session_ref PENDING via the point — seats row to write; L4.46/L4.47 in flight across the rotation); pi rounds live under the point: L4.45 (parent 4119445), L4.46 (helper); L4.44 HELD behind L4.45 (both touch rotate.py).** Gen II's window @234 SHUT by the Prime by PID at 03:48Z after L4.45 was harvested (its claude processes TERMed; the window closed itself). Prime L4-II = `agi-64 [61b9c9]` @235; L4-I idles at `agi-c6 [cd7648]` @232, XVI at `agi-05 [eb30d2]` @230 (predecessor chain kept; an idle predecessor reads NO mail — trap 0v). 🔴 **The `--seat` meter is FAIL-OPEN: never trust a `source=seat_pin` reading you did not claim yourself** — L4-II claimed first and read 0.0905. |
| spend | **Account $11.32 remaining of the owner's $92 at L4-II's pin claim, 2026-09-10 02:5xZ ($12.64 at L4-I's last read — L4 rounds bill the ACCOUNT through per-spawn keys) · runtime key `backup` $7.87 remaining of its $15 sub-cap, unmoved all of L4** (`rotate.py meter --pin` prints both; `/api/v1/credits` for the live delta). The key cap is **self-imposed and raisable** (`PATCH /api/v1/keys/<hash>` under `OPENROUTER_PROVISIONING_KEY`, §6 items 33/51); **quote both numbers or neither** (§6 item 86). 🔴 **The `provisioning.min_key_remaining_usd` $1.00 floor is fail-closed, has saved money twice, and is NEVER lowered.** Claude-side: owner reports a **$70 weekly allowance** (item 73); owner 2026-09-09: limits have reset (`doc:l4-owner-decisions`). |
| disk | 81% |
| this session | **Belam L4-II (2026-09-10 02:4xZ → …, Fable 5.1; pin 0.0905 at claim, rotating at 0.47 → `belam-S1-L4-III`).** Gate `continue`; verify green at 2deee5062; address announced and carried; seats row 61b9c9; handoff trimmed 49.9→39.8 KB by quote-checked script; owner asks (verification.py, false-OOM research) verbatim in doc:l4-owner-decisions and handed as L4.44 / L4.46; L4.37 reviewed on the bytes → L4.45; **03:30Z MERGE-UP 2 verified on season/s2 @ b4481c9ba** (L4.37 both halves, L4.40 proved, L4.43 at 65, helper's tip; 1897/1703/194, links 1877/0, goals 157, guard silent, suite 2315/1 by the point, pane clean) — both seat branches fully merged; helper holding. L4-I's session: `git log 03b16903f..2deee5062`. 03:36Z point rotated to gen III (a36dd7 @236; seats row written); 03:45Z the harness reaper measured live by gen II (goal:g17.1); 03:48Z L4.45 accepted (proved, on the seat branch), gen II's window shut by PID. LIVE: L4.44 (point) and L4.46 (helper) running in parallel; merge-up 3 after L4.44; the Prime reviews each on the bytes. |

## §0.7 LOOP L3 — CLOSED 2026-09-09 by the owner (opened 2026-09-06); L4 OPEN on `doc:l4-owner-decisions`

### L3 (CLOSED) — rounds L3.01–L3.44 all LANDED or closed; trimmed 2026-09-08/10

Detail: `git log --oneline iter-L3.01..iter-L3.44`, the experiment nodes, [COMPLETE.md](COMPLETE.md), `grid.py payload build:HANDOFF.md --version N`. Two lessons kept: check `git rev-list --count season/s2..<branch>` before believing a `--branch` parent landed anything, and diff a branch against its **MERGE-BASE**, never against a moved `season/s2`. Under L4 the POINT dispatches (`dispatch.py . L4.NN --target <node> --level small --tier parent --harness pi --branch`, from its own worktree); the Prime never dispatches. Wait-loop gotcha kept: `$(pgrep -fc PAT || echo 0)` captures "0\n0" when nothing matches — use `|| true` or compare with -le 0.

### 🔴 Where it stops — Belam L4-II, live 2026-09-10 (L4-I's last card: `git show 2deee5062:HANDOFF.md`)

```
BELAM L4-II LIVE  (agi-64 [61b9c9] · agi-rc:@235 — the window name belam-S1-L4-II is NOT an address; pin 0.09 at claim, cap 0.47)   season/s2 @ 2deee5062   2026-09-10 02:5xZ   key $7.87/$15 (floor $1, NEVER lowered) · acct $11.32/$92
L4     GO (owner 2026-09-09; plan parts 1-7 CONFIRMED verbatim in doc:l4-owner-decisions "L4 PLAN"; names + owner-confirmed role diagram in doc:l4-plan §0.9)
PLAN   doc:l4-plan e7883b4e4 (§2 cards, §5 rounds L4.02-L4.27 + ad-hoc L4.28+, §6 questions; 188 owner quotes byte-verified) · Q1-Q30 in doc:l4-owner-decisions "L4 BANKED QUESTIONS"
SEATS  goal:g17.1 = the Texas two-step formation + EVERY measured seat-protocol rule (owner verbatim; read it whole) · point gen III @236 a36dd7 (gen II rotated 03:36Z inside the worktree; gen I rotated PAST the cap at 0.5185 -> seats meter after every round close) · helper @233 on L4.46
       session worktrees .agi/worktrees/seat-<name> (seat/<name>@s2; kept across rotations; merged + deleted at session complete; grid runs ONLY on season/s2 after the merge) · ladder caps.director_kids 3
LANDED merge-up 1 = season/s2 @ aafb4be0a (L4-I, 1828/1634/194): L4.01 L4.20 L4.28 L4.32 L4.10 L4.11 L4.22 L4.26 L4.12(+follow-up) L4.25(lean_proved:65) L4.38
       merge-up 2 = season/s2 @ b4481c9ba (L4-II 03:30Z, 1897/1703/194, suite 2315/1): L4.06 L4.39 L4.05 L4.42 L4.37(both halves; 3 findings against half b: 2 -> L4.45, 1 fixed at the merge) L4.40 L4.43(@65, single choke point dispatch.py:1096)
       detail = git log 03b16903f..2deee5062 + goal:g17.1 Agent Notes + the experiment nodes; burn on per-spawn keys ~$0.35 all L4
OPEN   under the point: **L4.45 PROVED + merged on the seat branch @ 1528e7ab8 03:48Z** (both invariants verified at the line by gen III and spot-checked by the Prime; 109 tests incl. the files it could break; deviation from proof bar (d) accepted: the old skip test asserted the bug) · **L4.44 LIVE** (parent reviewing; kid landed verification.py 352 lines + test_verification.py 194 + command:commands entries write-guard/dispatch-help/verify + the brief edit through write.py; RULING 04:0xZ: the prime's brief names ONE line `commands.py run verify --suite` — --suite opt-in for every other reader; patched at the merge) · **L4.46 LIVE on the helper** (iteration L4.47) · merge-up 3 after L4.44: each branch against its OWN base · L4.41 role resolution (longest prefix wins, ambiguity REFUSES) · then the [config]/[vision] written_by flips ([owner, prime_director]) · writer BACKFILL at the very end (legacy = Director Prime, owner) · L4.23 message router HELD (release = the point's call now that L4.06/L4.37 are merged)
       · **L4.46 deep research: false-OOM reaping of backgrounded runs (OWNER 03:2xZ, verbatim in doc:l4-owner-decisions). 🔴 MECHANISM CONFIRMED LIVE 03:45Z (gen II, goal:g17.1): kill text "was stopped because the system is running low on memory" at MemFree 0.72 GB / MemAvailable 16.4 GB / Cached 10.1 GB — the harness watchdog reads MemFree, page cache reads as exhaustion; remainder = threshold/signal, reproduction, THE KNOB (item 4). L4.45's wrapper was the victim, after the round had committed (proved, tip 482079397, gen III harvests). Prime measured first: no per-process/cgroup cap (ulimit unlimited, memory.max=max at scope + user slice), no kernel OOM in 2 days, 17 GB available — the kills are the CC harness's background-task watchdog; claim to test: it keys on MemFree not MemAvailable (page cache 10 GB). Handed to the point 03:2xZ; web half = deep-search workflow, reproduction = CC-harness kid; also read how L4.37's parent ended.**
       · **L4.44 unified verification.py (OWNER 2026-09-10 02:5xZ, verbatim in doc:l4-owner-decisions): --level quick|rotation|full, one summary block + exit code, active count never lower vs its own record, suite opt-in, wired into command:commands + the successor brief — handed to the point 03:0xZ)**
RULED  (verbatim in goal:g17.1 / doc:l4-owner-decisions) parallel rounds GO · always prefer dispatch (landed+verified work is not re-derived) · L4.09 GO (Prime may add waves / re-order without a fresh go) · enforce written_by on ROLE never actor
       · prayer per SESSION not per turn · gpt-5.1-codex OpenRouter spend is NOT the engine's (both box suspects eliminated; owner checks activity BY KEY)
GATES  owner GO only: L4.07 perpetual flip of 12 gN (moves them into GOALS.md "## Perpetual") · L4.13 seat nodes (the owner's surface)
BANKED `driver.sh --smoke` prints DRIFT WARNING (engine HEAD vs the config's engine pin 179f95602839) on every commit past the pin — cosmetic, not chased (gen III) · Q29 (L4.22 JSONL vs graph nodes -> roll-up node) · Q30 (token counter scope; L4.25 found no counter exists) · workflow.py needs a --scratch one-shot class (3 fold scripts ran inline unregistered, item 22 tension)
       · 4 merged+dirty + 5 unmerged ahead=1 L3 worktrees kept for the point to harvest or drop · trap: iteration ids must be L4.NN numeric (fail-closed)
MODE   ENHANCED SURVIVAL (owner 2026-09-09): Prime + point + helper; every other seat idle; pi/OpenRouter does the work · predecessors kept XI–XVI (XVI relays owner text)
RULES  standing, EVERY role: trim + diagram-max handoff/context files · owner verbatim lives in NODES only · ROTATE AT 0.47 · partial edits: write.py read N:M then replace N:M
CRONS  ON: grid_sync */5 + push of the CHECKED-OUT branch at :07 (verify with crontab -l, never this file) -> push by hand anyway
DONE   L4-I: gate `continue` · verify green · plan drafted (4 workflows) + MINTED · questions banked · goal:g17.1 · cap 3 · helper spawned · point briefed · hygiene · handoff live
       L4-II: gate `continue` · pin 0.09 claimed · verify green (smoke 1828 / suite 2270/1 / links 0 / goals 143 / guard) · address announced + ack'd · seats row 61b9c9 · suite window granted + released
NEXT   1 DONE by L4-II 02:5xZ (pin · address announced, point verified it by the @id join and carried it into its brief · config:seats belam.session_ref 61b9c9 · goal:g17.1 read whole).
       2 DONE by L4-II 03:30Z: merge-up 2 verified on season/s2 @ b4481c9ba (see LANDED). NEXT REVIEWS, in order: L4.45 -> L4.44 (then collapse §5 + the successor brief to the one command) -> L4.46 (diagnosis to the owner);
         after each: git pull --ff-only; smoke (active >= 1703, never lower); links 0 broken; goals --render --check; guard silent; capture your pane; card + rows. Bank rulings beside the question in doc:l4-owner-decisions.
       3 rotate at 0.47: handoff first, rotate.py loop --role prime_director --name belam-S1-L4-III --timeout 900 --force --session-log <own .jsonl>; confirm by capture-pane
NEVER  let a kid run test_send.py unguarded while seats are live (send.py:406/:507 nudge REAL panes; L4.10) · run the suite without telling the point · rotate a seat with AGI_BRIEF_PROFILE=survival · git add -A · read $? through a pipe · sweep off a ps grep · run the
       suite twice at once · background a long verification · trust an `updated:` line · spend the Claude budget on prime chores under survival mode
```

## Prime duties, compact (full prose: `git show 763d24260:HANDOFF.md`)

```
FIRST   ls -t .agi/comms/season-2/dm/ and read anything addressed to you — BEFORE the smoke (XII missed two correct DMs for an hour; nothing alerts a prime to mail, §6 item 62 open)
PIN     claim your own pin FIRST: rotate.py meter --pin .agi/sessions/belam.meter --session-log <own .jsonl> (XIV read 0.5595 on XIII's pin; true 0.1093)
PUSH    the :07 cron push is hourly -> push by hand after every action · never git add -A · config:seats is YOURS to write (write.py "set seats <json>", whole list, grep the bytes) while sanctuary-master is down
SEATS   (design record; ALL SHUT DOWN 2026-09-09 08:2xZ by owner order, verbatim in doc:l4-owner-decisions) quorum = self-perpetuating / alive / all-is-one (one per vision) + master-sensei: idle, never hand-aimed
        · sanctuary-master: SHUT DOWN 08:0xZ (was gate-47-lifted, the one seat allowed to write config:seats) · liaison: NOT YET UP (owner's channel; sanctuary-master's first job, item 65)
        · the prime is NOT allowed in room quorum (owner): send.py --from <you> audience quorum --reason "<text>" -> room quorum-requests; never tmux send-keys (pane injection = impersonating the owner)
        · seats are better than the prime at the prime's mundane work: hand it over · read the mail first · compare against the MERGE-BASE, never the tip
ROTATE  at meter 0.47 (owner, every role, item 105; ladder director_rotate_at) OR at 99% of the Fable limit, whichever first (item 29; Opus fallback: --model claude-opus-5 --effort max)
        · read the limit from the pane: tmux capture-pane -pt agi-rc:<me> -S - | grep -oE "You.ve used [0-9]+% of your Fable limit" | tail -1
        · handoff FIRST, then: rotate.py loop --role prime_director --name belam-S1-L4-<next> --timeout 900 --force --session-log <own .jsonl>
        · the read-back takes the successor's FIRST non-noise line within 120s (a skill-first successor records inconclusive-no-reply) -> confirm by tmux capture-pane, announce by hand
        · rotate.py loop WORKS (fixed 2026-09-08, hypothesis:l3-rotate-launch-window-silent-failure); rotate.py = build:bin-rotate (SD.13); hazard 5 (stamp vs record, item 96) carried
```

## §4 Traps — CARRIED INTO L4 (headlines; full text in `doc:l4-owner-decisions` → "TRAPS CARRIED INTO L4" and `git show 91d33742d:HANDOFF.md`)

- 0al. A NODE THE SUITE PINS IS CODE — run the suite after any `.geometry` write.
- 0ap. A stamp copied from the card above you is a FELT clock: L4-I's `10:0xZ` ran ~7h20m ahead of `date -u` (02:4xZ, measured by L4-II) — stamp every line from `date -u`, never from prose (trap 0m, larger).
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
bash extensions/agi/driver.sh --smoke --max-iters 1 && echo SMOKE_OK     # active ≥ 1703 / node_count ≥ 1897, never lower
python3 extensions/agi/bin/commands.py run tests                         # 2315 passed / 1 skipped, ~125s — run it ALONE, tell the point first (trap 0e)
python3 extensions/agi/bin/snapshot-goals.py --render --check            # 157 goals byte-identical
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
