# SESSION HANDOFF — 2026-09-10: `belam-S1-L4-V` (Belam L4-V, L4 prime, **Opus 5 max**) — **claim your own address by the `tmux list-windows` @id ↔ `ListAgents` join; a name is not an address.** 🔴 **L4 RUNNING in ENHANCED SURVIVAL on `doc:l4-plan` (`goal:g17.1` = the seat protocol, read it whole — it is the session's memory): Prime + point `sanctuary-director` gen VII (`seat-sanctuary-director-16 [4a9edc]` @245, agi-rc:9) + helper `sanctuary-helper` gen III (`seat-sanctuary-helper-cd [9d073a]` @240, reports to the point only); every other seat idles; work on `season/s2`, `master` takes merges only.** 🔴 **Commit and push after every action.** 🔴 **Stamp every line from `date -u` — L4-III wrote a felt clock ~5h slow for half a session (trap 0ap).** 🔴 **GREP PROVES PRESENCE; ONLY A STRUCTURAL ASSERTION PROVES SHAPE.** 🔴 **AUTHORITY IS VERIFIED AGAINST THE GRAPH, NEVER THE MESSAGE — `config:seats` at HEAD.** The card in §0.7 is the map.

**Owner's instructions:** carried forward in place by successors (2026-09-06); trimmed to L3 on 2026-09-07 at the owner's ask — the L1/L2 sessions, the L2 plan and the L2-era proposals live in the grid (`grid.py payload build:HANDOFF.md --version N`) and in [COMPLETE.md](COMPLETE.md). Bootstrap lives in [QUICKSTART.md](QUICKSTART.md). The design is in [`.agi/context/season-ladder-and-morals-brief.md`](.agi/context/season-ladder-and-morals-brief.md) and [`.agi/context/l3-command-ladder-brief.md`](.agi/context/l3-command-ladder-brief.md) (owner text verbatim, incl. the 2026-09-07 perpetual-seats layer). Do not re-derive either.

## §0 State block

| | value |
|---|---|
| active nodes / deprecated | **1819 active / 194 deprecated (2013)** verified by the Prime on season/s2 @ 5bbccc86f (merge-up 16), `verify` 9/9 on my own read. Grew at every one of seventeen readings, never dropped; crossed 2000 at merge-up 14. |
| goals | **163** — re-rendered and round-trip byte-identical by me at 20:4xZ. 🔴 **This row read 159 for at least two sessions while the card two screens down read 163; the card was right.** A number that two places in one file disagree about is a number nobody is reading. Check it with `snapshot-goals.py --render --check`, never with this row. |
| `outcome_coverage` (primary) | **0.14** at b4481c9ba (0.147 at L4-II's open, 0.132 at XV's). Drifts DOWN as hypothesis/experiment nodes enter the denominator faster than mvps close — dilution, not regression. |
| `evidence_fraction` | **0.561** at XVI's open (0.552 at XV's, 0.385 at L2.13) — rising every session this loop. `unevidenced_decisive_verdicts` 0. |
| tests | 🟢 **2548 passed / 3 skipped** at merge-up 16 (`verify-suite` **10/10 on the FIRST read** — twice now, my rotation run and the point's merge-up). 🔴 **THE TWO-READ PROCEDURE IS RETIRED — it was true until 2026-09-10 18:5xZ and is now WRONG.** L4.101 item 2 fixed the ordering artifact: `bin-suite-fresh` now judges the run COMPLETING rather than the run before it, so a first `--suite` on an uncovered tree passes on its own merits. **A successor who expects a red first read will misread a genuine failure as the artifact** — the dangerous direction. 🔴 A NEW FILE IN `bin/` STILL NEEDS THE SUITE (`test_bin_help_smoke` enrols every `bin/*.py`); ship new tools as SUBCOMMANDS to dodge it. 🔴 **A green suite is not a working command; a green test can *require* a defect (L4.74); a round's falsifiers can contradict each other; and a green `verify` says NOTHING about a credential's validity.** |
| broken links | 0 (**1882 resolved** at 13d5bc2f7; 18 retired payloads, not damage) |
| crons | 🟢 **ON for this repo — verified 2026-09-09 06:1xZ by `crontab -l` AND its live log (`~/logs/agi-crons-agi-2f118e6f.log`, written every 5 min): `grid_sync` `*/5` runs `grid.py commit --all --prefix 'cron: '` from `.agi/`; `branch_push` pushes `season/s2` at :07 hourly; `.geometry/crons.md` declares `crons_live: true`.** 🔴 **XIV's row said OFF (its 2026-09-08 13:1xZ reading) — wrong or since reverted. Verify with `crontab -l`, never with this file.** Two consequences: **push by hand anyway** (the push is hourly; a dead box strands up to 59 min), and **the auto-versioning hazard IS armed** — half-finished source from a killed agent is grid-versioned under the cron's name within 5 minutes, so kill cleanly and `git reset` unreviewed staging at once. |
| branch | **`season/s2`** (opened by the wave-2 rollover). `master` = season 1 (genesis), **frozen**: merges + cherry-picks only, never rebase. Grid `commit --all` runs on `season/*` or master only. |
| agents live | **enhanced survival: Prime `belam-S1-L4-V` = `agi-06 [66537b]` @244 (agi-rc:2) · point `sanctuary-director` gen VII (`seat-sanctuary-director-16 [4a9edc]` @245, agi-rc:9; row written from the join at 0d2f0246c BEFORE it acted) · helper `sanctuary-helper` gen III (`seat-sanctuary-helper-cd [9d073a]` @240, to the point only)** — joined from `ListAgents` by the @id join and written into `config:seats` BEFORE the seat acted (69f84f178); a seat cannot authorize itself by asserting its own ref. Idle predecessors: sanctuary-director gen VI `3251f9` @243 (window now `sanctuary-director.gen7`), L4-IV `agi-a5 [e7f117]` @242, sanctuary-director gen V `3d6888` @241, L4-III `agi-7f [7902ac]` @239, L4-II `agi-64 [61b9c9]` @235, L4-I `agi-c6 [cd7648]` @232, XVI `agi-05 [eb30d2]` @230 — idle predecessors read NO mail (trap 0v), reach them with `send.py send`. 🔴 **The `--seat` meter is FAIL-OPEN: never trust a `source=seat_pin` reading you did not claim yourself.** |
| spend | 🔴 **THE `.env` `OPENROUTER_API_KEY` NAMES A DELETED KEY — `backup` WAS DELETED BY THE OWNER on 2026-09-10 (keys 3 → 2), and `.env` was deliberately left untouched.** Measured by me at 17:3xZ, not taken on trust: `curl …/credits` with it returns `401 User not found`, and `provisioning.py status` prints `OPENROUTER_API_KEY: unknown — key_usage failed: HTTP 401`. 🔴 **`envfile.py --check` STILL PASSES, because it requires the key's PRESENCE and not its validity — that is the landmine; a green `verify` says nothing about this key.** Why the loop runs anyway: **provisioning is AVAILABLE** (`keys_visible=2`, `engine_minted=1`, outstanding `agi-2` used $0.597), every spawn mints its OWN ~$5 key through `OPENROUTER_PROVISIONING_KEY`, and gen V's conditional pre-flight (`306b77bb6`) skips the runtime leg while provisioning is up. **Gate OPEN.** Account: **$17.84 remaining of $107.00** (read through provisioning at 17:2xZ). Measured round cost **$0.0977 · $0.0749 · $0.0911 (produced) · $0.2156 (failed) · $0.2397 (the free-model probe)**. Per-spawn keys are **revoked when the agent finishes** — **a post-hoc diff cannot see an ephemeral resource; observe DURING.** 🔴 **`agi` ($10.92/$40) is the one unexplained credential left; the owner named only `backup`, so it was NOT touched.** 🔴 **The provisioning-ABSENT path is now a real hazard, not a hypothetical: with the runtime key dead it should REFUSE clearly instead of letting a spawn discover a 401 mid-round — banked as a round for the point.** |
| disk | 81% |
| this session | **Belam L4-V (2026-09-10 20:0xZ → , claude-opus-5 max, `agi-06 [66537b]` @244, agi-rc:2).** Pin claimed **0.1171** on my own transcript. Gate answered with a DIFF — the handoff named L4-IV live in four places; `continue` would have been the false answer, and that is now **3 of 3** correct answers the read-back would score as failures. Seat row **already correct at HEAD** (c1c3cbae0, written by L4-IV from the join) — verified, not rewritten. `verify-suite` **10/10 on the FIRST read** (links 0 · goals byte-identical · guard silent · active 1817/194/2011 · viewport · dispatch · budget · tests **2546/3** in 135.8s · bin-suite-fresh · node-count at floor) — the two-read retirement confirmed by a session with no stake in it. ACCOUNT **$16.91 of $107.00** (read through provisioning at 20:1xZ; $17.84 at 17:2xZ). L4-IV's full record is the `L4-IV:` line in the DONE block below. |

## §0.7 LOOP L3 — CLOSED 2026-09-09 by the owner (opened 2026-09-06); L4 OPEN on `doc:l4-owner-decisions`

### L3 (CLOSED) — rounds L3.01–L3.44 all LANDED or closed; trimmed 2026-09-08/10

Detail: `git log --oneline iter-L3.01..iter-L3.44`, the experiment nodes, [COMPLETE.md](COMPLETE.md), `grid.py payload build:HANDOFF.md --version N`. Two lessons kept: check `git rev-list --count season/s2..<branch>` before believing a `--branch` parent landed anything, and diff a branch against its **MERGE-BASE**, never against a moved `season/s2`. Under L4 the POINT dispatches (`dispatch.py . L4.NN --target <node> --level small --tier parent --harness pi --branch`, from its own worktree); the Prime never dispatches. Wait-loop gotcha kept: `$(pgrep -fc PAT || echo 0)` captures "0\n0" when nothing matches — use `|| true` or compare with -le 0.

### 🔴 Where it stops — Belam L4-V, live 2026-09-10 (L4-IV's last card: `git show 098d3c877:HANDOFF.md`)

```
BELAM L4-V — LIVE (Opus 5 max, standing — owner)   agi-06 [66537b] @244 / agi-rc:2   season/s2 @ 098d3c877   **2026-09-10 20:0xZ TRUE UTC** (stamp from `date -u` or a commit hash — mine drifted +80 min mid-session, trap 0ap)   pin 0.1171 / cap 0.47   ACCOUNT ~$17.3 of $107.00
L4     GO (owner 2026-09-09; plan parts 1-7 CONFIRMED verbatim in doc:l4-owner-decisions "L4 PLAN"; names + owner-confirmed role diagram in doc:l4-plan §0.9)
PLAN   doc:l4-plan e7883b4e4 (§2 cards, §5 rounds L4.02-L4.27 + ad-hoc L4.28+, §6 questions; 188 owner quotes byte-verified) · Q1-Q30 in doc:l4-owner-decisions "L4 BANKED QUESTIONS"
SEATS  goal:g17.1 = the Texas two-step formation + EVERY measured seat-protocol rule (owner verbatim; read it whole — the newest notes are the reaper, the respawn, the report rule and this rotation)
       session worktrees .agi/worktrees/seat-<name> (seat/<name>@s2; kept across rotations; merged + deleted at session complete; grid runs ONLY on season/s2 after the merge) · ladder caps.director_kids 3
LANDED merge-ups 1-7 = season/s2 aafb4be0a -> b4481c9ba -> 13d5bc2f7 -> 3add44829 -> 27f6f55ca -> 2b17a7e5a -> dcf0b24a0 (1828 -> 1951 nodes, never a drop; suites 2270/1 -> 2413/1), rounds L4.01-L4.70.
       Full per-merge records with their measured rules: goal:g17.1 Agent Notes (one note per merge-up) · git log 03b16903f..8cf15b3e7 · the experiment nodes. Do NOT re-derive them here.
       Closed sagas, dead by measurement — do not re-open: THE REAPER = system-wide PSI on /proc/pressure/memory (trigger "some 150000 2000000", ANY process on the box), NOT MemFree, NOT freemem(),
       NOT the seat's own cgroup; THE KNOB = env CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP (set in the tmux env by the Prime; exported by every spawn path since L4.55) · THE RESPAWN BLEED = a
       finished parent was restarted onto its own committed round ($7.23 -> $5.22 in 30 min); fixed at merge-up 4 (a `<agent> done:` commit on the agent branch is completion) and proven at L4.55.
OPEN   **20:3xZ TRUE UTC (`date -u` 20:37Z; my felt clock ran ~30 min FAST between 20:2x and 20:37 — trap 0ap, caught by a commit timestamp) — L4-V live.** **MERGE-UP 16 ACCEPTED** (5bbccc86f; 1819/194/2013; links 0; goals 163; suite 2548/3; my own `verify` 9/9). Merge-ups 5–16 all accepted; one note each in `goal:g17.1`. Do NOT re-derive.
       · **THE POINT ROTATED: gen VII `seat-sanctuary-director-16 [4a9edc]` @245**, row written from the join BEFORE it acted (0d2f0246c), briefed with FIVE rounds + three banked (msg 3a2f1886). It dispatches; I review.
       · 🔴 **OWNER SPOKE TWICE TONIGHT ON WORKFLOWS (verbatim in `doc:l4-owner-decisions`)** — caught the Prime running an inline, unregistered workflow. Answered honestly: yes, on the fly, and that one evaporated with the session until I registered it (`prime-open-questions`, 42cad809a — durable, but its manifest prompts are `<TODO>` skeletons, so NOT yet runnable on pi). Four asks → two rounds under `goal:g1.14`: authoring-as-a-routed-verb with NATIVE tooling per harness, and a `.geometry/workflows.md` config node for types + the prime-owned default harness + two override levels.
       · **THE READ-ONLY SURVEY (six agents, adversarial pass) REFUTED TWO OF ITS OWN THREE FINDINGS** — the pass earned its keep. Commit-guard: NOT live, fixed twice on 09-07 (b96d6b3da, bbe04ce9b), inbox item closed on the node, one structural residual worth a node. Seat-branch: the 'merge-up 13 pending' bullet was stale (306b77bb6 landed via e9eca4e1c) — but the investigator's RECOMMENDATION ('do not run merge-up 16') was refuted and reality agreed: the round had returned and merged green while the survey was still running. **In a live system only MONOTONE facts survive the latency of the investigation that measured them** — ancestry did, 'what to do next' did not. Suite-lock: still live, SEVEN lock-free paths not five, two of them engine code (`season.py` merge-up gate runs pytest bare) — the round is minted with the obstacles named.
       · **L4.104 CLOSED by merge-up 16.** The point's next round is its own choice from the batch.
GATES  owner GO only: L4.07 perpetual flip · L4.13 seat nodes · 🔴 **STILL OPEN — INSTALL THE ROTATION-REMINDER HOOK?** Built (L4.94), deliberately NOT installed; it touches every session on this box. Recommended yes, scoped to fire only inside a project holding `.agi/` and only past threshold. **If he rules yes the PRIME installs it once and verifies — not a seat.**
       Recommended yes, scoped to fire only inside a project holding `.agi/` and only past threshold. **If he rules yes, the PRIME installs it once and verifies it — not a seat.**
       · Banked, not urgent: rotate the engine onto a FRESH runtime key so `backup` can stay capped forever. Path built since 09-07.
SPEND  answered by measurement, do not re-open: **free models = NO** (`openrouter/free` went 30/30 in probes then returned `404 unavailable for free` to a real round — AVAILABILITY IS NOT CAPABILITY;
       only 2 of 21 free models produce usable output; enumerate by `pricing == 0`, since the `:free` suffix misses 14% including the best candidate — THE NAME IS A HEURISTIC, THE FIELD IS THE FACT).
       **Batching = no OpenRouter route** (same key: 200 on `/files`, HTML 404 on `/batches`); a discount needs a new credential = owner's. Re-probe `/files` each season rollover. **Batch the sweeps, not the loop.**
RULES  earned this session, all with an instance behind them — this block is the session's real yield:
       · **A remedy that reuses the broken mechanism is not a remedy** (the meter brief said "re-pin"; a bare re-pin IS the capture).
       · **A guard the standard remedy disarms is worse than no guard — it certifies the state it failed to check** (`cmd_meter` re-stamps the caller's generation onto a foreign pin).
       · **A mitigation that hides the symptom before the cause is fixed buys a green light and loses the bug** — and the Prime committed this in its own round spec; gen V caught it.
       · **Two independent measurements that agree too precisely are one measurement** (a captured meter tracked the Prime's to two decimals).
       · **A post-hoc diff cannot see an ephemeral resource — observe DURING** (per-spawn keys are revoked at agent finish).
       · **A round whose falsifiers contradict each other** (gen V, self-caught) and **a claim whose conjuncts contradict** (L4.02) — the same check at two altitudes.
       · **A round that fixes the gate it must pass through cannot be dispatched** — hand-land it. Twice now: the parent brief (L4.77), the dispatch pre-flight (306b77bb6).
       · **MECHANISM, NOT WORDING** is in the parent+director briefs and is REPRODUCING ITSELF unprompted. Cite the mechanism, never a correlate — the Prime broke this one and said so.
       · **Identity is SUPPLIED, never inferred** (meter) · **authority is verified against the graph** (seats) · **detect, do not repair** (reconciler) · **the inference is ONE-WAY: a dead pid proves stopped, a live pid proves nothing.**
       L4-V's, each with an instance: · **A claim about a reader that was never read is wording** (I built round 4 on the handoff's description of `rotate.py`, never opened it; the falsifier fired on my own DONE block) · **A disprover run before dispatch is the cheapest round there is** (gen VII spent one measurement, saved a parent) · **In a live system only MONOTONE facts survive the latency of the investigation that measured them** (the survey's ancestry held, its 'what to do next' was wrong by the time it returned) · **A check that guards a proxy for the resource certifies the state it failed to inspect** (the suite lock, `envfile.py` — twice in one loop) · **A stamp reasoned from context is a felt clock even after you have written the warning down** (trap 0ap, mine)
NEXT   1 🔴 **NOTHING IS BLOCKED AND NOTHING IS OWED BY THE PRIME.** The point (`sanctuary-director` gen VII, `4a9edc` @245) holds the batch and dispatches the next round itself. Review what it lands, one report at a time, **from the report AND the bytes**. Verify on season/s2 with `commands.py run verify` — ONE read, 9/9. **The floor after merge-up 16: active 1819 (194 deprecated / 2013 total), links 0 broken, goals 163 byte-identical, suite 2548/3.** Record each merge-up as one note in `goal:g17.1`, update §0, commit, push. It messages only when necessary (owner standing order) — **silence is the system working, not a stall.**
       2 **RULED (goal:g17.1, cd964481c): THE SUITE WINDOW IS ADVISORY, NOT EXCLUSIVE — say it that way.** A bare `pytest` walks past the lock; the survey then found SEVEN lock-free paths, two of them engine code. The fix is `hypothesis:l4-the-suite-lock-belongs-to-pytest-not-its-caller` (round 3 in the point's batch) and its proof RUNS SUITES — the point must coordinate every run with the Prime. Named once because the project paid for this shape twice in one loop (this + `envfile.py`): **a check that guards a proxy for the resource certifies the state it failed to inspect.**
       3 **BATCH HANDED TO GEN VII (msg 3a2f1886), in priority order:** (1) `hypothesis:l4-workflow-authoring-is-a-harness-tool` — OWNER · (2) `hypothesis:l4-workflow-types-and-default-harness-are-a-geometry-node` — OWNER · (3) `hypothesis:l4-the-suite-lock-belongs-to-pytest-not-its-caller` · (4) `hypothesis:l4-rotate-readback-false-negative-and-the-orphan-by-design` — 🔴 **REVERSED by gen VII's pre-dispatch disprover (88c3d9ca8): the reader reads the successor's `--debug-file`, Claude Code's DEBUG LOGGER — 42 logs, 294,616 lines, zero prose ever; it already records a diff if one arrives; L4-I and L4-III answered `continue` and still read as silent. My accept-set claim was wording. RULED GO on an explicit identity-supplied, generation-checked `rotate.py ack`; presence kept on both paths; debug-file reader DELETED; gate + both briefs in the same round** · (5) `hypothesis:l4-the-merge-up-window-must-be-a-lock-not-an-announcement`. Banked for it to mint: trimguard as a SUBCOMMAND (🔴 `.agi/sessions/trimguard.py` is UNTRACKED and load-bearing) · commit-guard residual 2 (single-toplevel scope, note on `hypothesis:l3-commit-guard-inert-under-g11`) · provisioning-ABSENT should refuse.
       4 Watch the ACCOUNT, never the `.env` key — that key is DELETED and the owner confirms the prefix in history is old and non-functional (§0 spend row): `provisioning.py status`. **$16.91 of $107.00 measured by me at 20:1xZ** ($17.84 at 17:2xZ — ~$0.93/3h at this cadence). Below **$1.00 account-wide** the point finishes its open round and stops dispatching pi. 🔴 A green `commands.py run verify` says NOTHING about a credential's validity — `envfile.py --check` tests presence. 🔴 **FALLBACK (owner, verbatim in `doc:l4-owner-decisions`): SONNET PARENTS AND KIDS via `--harness claude-code`** — the WORK tier falls back, not the director tier; whether a director runs sonnet or opus is a separate FORMATION question he has not decided. The switch stays the owner's to authorise.
       5 Rotate at 0.47: **handoff FIRST** (gen V measured it — it closed at 0.4091 deliberately because gen III closed at 0.56 and wrote a worse brief; the handoff is the first artefact to degrade), then `rotate.py loop --role prime_director --name belam-S1-L4-VI --model claude-opus-5 --effort max --timeout 900 --force --session-log <own .jsonl>`. 🔴 **CONFIRM BY THE `ListAgents`/@id JOIN OR `capture-pane`, NEVER BY THE READ-BACK — its false-negative rate is now 4 of 4 on healthy successors across two seats, and the cause is known: the gate permits a diff, the reader accepts only `continue`.** Then verify the successor's `session_ref` in `config:seats` — **L4-IV wrote mine before I acted (c1c3cbae0) and that is the protocol working; the successor's duty is to VERIFY the row at HEAD, not to write it.**
RULED  (verbatim in goal:g17.1 / doc:l4-owner-decisions) parallel rounds GO · always prefer dispatch (landed+verified work is not re-derived) · L4.09 GO (Prime may add waves / re-order without a fresh go)
       · enforce written_by on ROLE never actor · prayer per SESSION not per turn · gpt-5.1-codex OpenRouter spend is NOT the engine's (owner checks activity BY KEY — the one exception is the ACCOUNT row above)
GATES  🔴 **ONE LEFT, OWNER-ONLY: INSTALL THE ROTATION-REMINDER HOOK?** Built as L4.94, merged, three defects repaired, deliberately NOT installed — it touches every session on this box. Recommended YES,
       scoped to fire only inside a project holding `.agi/` and only past threshold; **the PRIME installs it once and verifies it, not a seat.** · owner GO only, unchanged: L4.07 perpetual flip of 12 gN · L4.13 seat nodes.
       ✅ CLOSED BY THE OWNER 2026-09-10: **qwen/qwen3.8-27b ($39.20, 49.4%) is his and was authorized** — the measurement stays as a record, no action owed, do not re-propose. **The truncated `sk-or-v1-537bbe7c…`
       prefix in three experiment nodes is OLD AND NON-FUNCTIONAL** (his words) — Belam V's "rotate the key at go-public" is retired, and 🔴 **those nodes are NOT to be edited: they are archive and correct as they stand.**
       nobody here knows what it is. The owner's containment was CORRECT and closed the SECOND-largest spender (codex \$12.38/1214 req matches deleted key `backup` lifetime \$11.4847). The loop itself is
       \$21.56 = **27.2%**; **72.8% of this account is not this project.** Measured by the point under L4.97 and RE-MEASURED INDEPENDENTLY by the Prime against `/api/v1/activity` — matched to the cent.
       Full table + the single recommendation (ask him BEFORE any further containment) in `doc:l4-owner-decisions`. **NO KEY TOUCHED, none will be** — `agi` (\$10.92/\$40) stays untouched because he
       named only `backup`. · owner GO only: L4.07 perpetual flip of 12 gN · L4.13 seat nodes · **INSTALL THE ROTATION-REMINDER HOOK?** (L4.94, built + 3 defects repaired, deliberately NOT installed —
       it touches every session on this box). Recommended YES, scoped to fire only inside a project holding `.agi/` and only past threshold; **the PRIME installs it once and verifies it, not a seat.**
BANKED `driver.sh --smoke` prints DRIFT WARNING (engine HEAD vs the config's engine pin 179f95602839) on every commit past the pin — cosmetic, not chased · Q29 (L4.22 JSONL vs graph nodes -> roll-up node)
       · Q30 (token counter scope; L4.25 found no counter exists) · workflow.py needs a --scratch one-shot class (3 fold scripts ran inline unregistered, item 22 tension)
       · 4 merged+dirty + 5 unmerged ahead=1 L3 worktrees kept for the point to harvest or drop · trap: iteration ids must be L4.NN numeric (fail-closed)
MODE   ENHANCED SURVIVAL (owner 2026-09-09): Prime + point + helper; every other seat idle; pi/OpenRouter does the work · predecessors kept XI-XVI + L4-I + L4-II
RULES  standing, EVERY role: trim + diagram-max handoff/context files · owner verbatim lives in NODES only · ROTATE AT 0.47 · partial edits: write.py read N:M then replace N:M (CLI form)
       · OWNER 2026-09-10 05:0xZ: directors message the Prime ONLY when necessary (merge-up numbers · a Prime-only decision · a rotation line · a red merge / rule-changing finding) — never progress,
       status, acks, harvests; the Prime reads the bytes at the merge-up (verbatim in doc:l4-owner-decisions)
CRONS  ON: grid_sync */5 + push of the CHECKED-OUT branch at :07 (verify with crontab -l, never this file) -> push by hand anyway
DONE   L4-I: gate `continue` · verify green · plan drafted (4 workflows) + MINTED · questions banked · goal:g17.1 · cap 3 · helper spawned · point briefed · hygiene · handoff live
       L4-II: verify green · seats rows for 3 seat rotations · handoff trimmed 49.9 -> 42 KB · verification.py + the reaper knob + the report order discharged · merge-ups 2, 3, 4 verified · respawn bleed fixed
       L4-III: gate `continue` · pin 0.1141 claimed · verify-suite 9/9 (1730/194/1924) · seats row 7902ac pushed · merge-up 5 GO'd + window granted · strays reported · ACCOUNT ceiling measured + banked
       L4-IV: gate answered with a DIFF (the handoff named me while §0 still described L4-III) · pin claimed explicitly · verify-suite 9/9 twice · seats belam=e7f117 + director gen VI=3251f9 · runtime key measured DEAD · successor brief fixed in ONE edit · predecessor stopped writing season/s2 · MERGE-UPS 13/13b/14/15 ALL ACCEPTED GREEN (1780→1817 active, 2011 total, never a drop) · **REPO SET PUBLIC** on owner order after a full credential sweep · **L3 predecessors reaped** (1.69 GB RAM) · trim guard RECOVERED TWO LOST OWNER QUOTES · CLAUDE.md:305-316 corrected in one gated edit · two-read rule retired
       L4-V: gate answered with a DIFF (5 hunks — the handoff named L4-IV live in four places) · pin 0.1171 claimed on my own transcript · **`verify-suite` 10/10 on the FIRST read, confirming the two-read retirement from a session with no stake in it** · seat row VERIFIED at HEAD, not rewritten (L4-IV had already written it) · crons re-verified against `crontab -l` after an empty log tail nearly said otherwise · **three machine-written records rescued from disk and committed** (d2a46e599) · **the read-back false negative traced to a SPECIFICATION CONTRADICTION and the held round's claim sharpened** (a9debc784) · **§6 second-pass collapse, −7.0KB, guard run before AND after with the unresolved set unchanged** (50cceb9de) · goals-check went red on my own goal-node notes and was re-rendered (the check working) · 🔴 **fell into trap 0ap myself — stamped 20:5x/21:0x/21:1xZ from a felt clock while `date -u` read 20:2x–20:37Z; corrected in place, offset recorded in `goal:g17.1`** · **MERGE-UP 16 ACCEPTED from report AND bytes** (1819/2013, 9/9) · suite window RULED advisory · **owner's two workflow messages banked verbatim, the Prime's own unregistered inline workflow REGISTERED** (`prime-open-questions`) · **three rounds minted** (two owner asks under g1.14, the suite lock under g1.10) · point gen VII row written from the join, briefed with the batch · **round 4 REVERSED on the point's measurement and ruled GO on the ack channel** (88c3d9ca8)
NEVER  let a kid run test_send.py unguarded while seats are live (send.py:406/:507 nudge REAL panes; L4.10) · run the suite without telling the point · rotate a seat with AGI_BRIEF_PROFILE=survival · 🔴 **REAP `@238 sanctuary-director.gen5`, `@241 sanctuary-director.gen6` OR `@237 sanctuary-helper.gen2`** — gen V left them alive DELIBERATELY as the only two live fixtures of the orphaned-rotation shape; tidying them loses the reproduction (@238 + @241 are a MATCHED PAIR — same seat, consecutive generations, identical step-4 failure; @237 is a different cause with the same residue)
       · git add -A · read $? through a pipe · sweep off a ps grep · run the suite twice at once · background a long verification · trust an `updated:` line · adopt a seat's work instead of verifying it
       · spend the Claude budget on prime chores under survival mode
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
        · 🔴 **DO NOT WAIT ON YOUR READ-BACK. Its false-negative rate is 2 of 2 on the one seat with two observations** (`sanctuary-director` gen IV and gen VI, one generation apart, warning verbatim identical,
          successor ALIVE and working both times). `rotate.py loop` **exits 0** while step 4 warns and step 5 never runs — a silent failure wearing a success code — and because step 5 (reap own window) is GATED
          behind the read-back, **a rotation can never reap its own window; the orphan is by design, not bad luck.** Root cause: TWO states for THREE realities (confirmed / alive-but-unconfirmed / absent), the
          middle collapsed onto the third. **And the brief disagrees with the mechanism:** this gate permits `continue` OR a diff, the read-back accepts only `continue` — L4-IV answered with a diff, correctly,
          and would have scored as a failure. Round: `hypothesis:l4-rotate-readback-false-negative-and-the-orphan-by-design` (HELD). **Confirm by the `ListAgents`/@id join or `capture-pane`, then announce by hand.**
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
git branch --show-current                                   # season/s2
python3 extensions/agi/bin/commands.py run verify-suite     # the prime's ONE rotation command (L4.44, owner 2026-09-10): links, goals round-trip, guard, smoke + never-lower baseline, viewport, dispatch, budget, then the engine suite under a lock (~3 min)
python3 extensions/agi/bin/commands.py run verify           # the same without the suite (26s): every other role, and the Prime after each merge-up
python3 extensions/agi/bin/grid.py commit --all             # 0 errors since L3.20
git push origin season/s2
```

## §6 Owner decisions — settled, do not re-ask

🔴 **§6 IS GUARD-CLEAN AND COLLAPSIBLE — the dangerous half is already done (2026-09-10, L4-IV).** Run `python3 .agi/sessions/trimguard.py` from the repo root BEFORE removing a single line: it extracts every
genuinely double-quoted span of 25+ chars, strips the `(N quotes archived)` marker and any truncated trailing word, greps `.agi/nodes/` for a 55-char prefix, and **exits non-zero listing anything that resolves in no node.**
It ABORTED on its first real run and recovered **two owner quotes that existed only in this file** — item 29 `"Fallback to opus acceptable."` and item 91 `"They should have individual branches."` — both now verbatim in
`doc:l4-owner-decisions`. 🔴 **BOTH LINES CARRIED `(1 quote archived)` AND BOTH MARKERS WERE WRONG: an archive marker is a CLAIM, not a verification.** Treat every `(N quotes archived)` here as UNVERIFIED until the guard says otherwise.
**Two adjudicated waivers, recorded not auto-waived** (the guard still aborts on them and must NOT be weakened): `ROLES SELF-SELECT THEIR SLICES…` (a director's gloss in item 95; that item's real owner quote does resolve) and
`The honest answer was NO on both halves…` (a predecessor's prose in item 63). Collapsing the ~19KB index to a pointer is now mechanical and safe, and is worth ~18KB to every future session. **I did not do it** — at meter 0.33,
spending the remaining window rewriting the file my successor must read trades a certain good for a probable harm (gen V's measured rule: the handoff degrades first). It is yours, cheaply.

**§6 was collapsed on 2026-09-09 under the owner's ruling (verbatim in `doc:l4-owner-decisions`): finished items are one line each; every owner quote they held is archived verbatim, keyed by item number, in `doc:l3-command-ladder-brief` → *§6 OWNER VERBATIM ARCHIVE* (167 quotes); the last full-prose HANDOFF is `grid.py payload build:HANDOFF.md --version 298`. Open items keep their prose below the index.**

```
STILL OPEN: none — L3 closed 2026-09-09; items 55 (live half), 71, 96, 103 carried into doc:l4-owner-decisions "L4 BACKLOG"; 104 resolved (closed)
```

### Closed items — index, one line each · **second pass 2026-09-10 (L4-V): quote fragments and every `(N quotes archived)` marker removed, −7.0KB.** The guard was run BEFORE and AFTER: 41 quoted spans → 6, and the set that resolves in NO node is **unchanged at the same two adjudicated waivers** (item 95's director gloss, item 63's predecessor prose), which are kept verbatim on purpose. Every one of the 35 removed spans resolved in a node first — that is the rule, executed, not asserted. Negations, conditions, attributions and supersessions were preserved by machine, not by care (item 105 was the one rescue).

- **0.** L2-era rules still in force (items 1–6 of the 2026-09-06 list, compressed)
- **7.** Branching, decided
- **8.** Merge, not rebase
- **9.** RESOLVED 2026-09-06 (after L2.13) — the owner supplied the three visions
- **10.** Owner decisions 2026-09-06 (L3 brainstorm), settled
- **11.** SETTLED 2026-09-06 (owner)
- **12.** Settled 2026-09-06 (later)
- **13.** Settled 2026-09-06 (last)
- **15.** Owner rule 2026-09-07 (verbatim)
- **16.** BANKED 2026-09-07 (Belam II, owner asked in chat): mantles per vision for the three advisors
- **17.** BANKED 2026-09-07 05:00 UTC (from the Alive advisor): the three season-2 visions carry `proposes_goals: []`
- **18.** OWNER DESIGN LAYER 2026-09-07 (04:40–07:36 UTC), settled — verbatim in `.agi/context/l3-command-ladder-brief.md`, section
- **14.** Owner answers 2026-09-06 (belam, at L3 open)
- **19.** Owner direction 2026-09-07 ~14:40 UTC (to Belam IV, verbatim)
- **20.** Owner layer 7/7b (2026-09-07, relayed by Belam III's DM at 14:46 UTC; verbatim in `doc:l3-command-ladder-brief` quotes 7 and 7b, end of the owner sect…
- **21.** Owner addendum to `vision:alive`, 2026-09-07 ~15:00 UTC (verbatim)
- **22.** Owner 2026-09-07 15:10 UTC (verbatim)
- **23.** Owner 2026-09-07 15:25 UTC (verbatim)
- **24.** OWNER LAYER 8, 2026-09-07 ~16:00 UTC (to Belam IV, verbatim; also quote (9) in `doc:l3-command-ladder-brief`)
- **25.** Owner 2026-09-07 16:20 UTC (verbatim)
- **26.** Owner 2026-09-07 ~17:55 UTC (to Belam V, verbatim; quote (11) in `doc:l3-command-ladder-brief`)
- **27.** Owner 2026-09-07 ~17:55 UTC (verbatim; quote (12) in the doc)
- **28.** Owner 2026-09-07 ~19:05 UTC (verbatim)
- **29.** SETTLED 2026-09-07 19:46 UTC (owner, verbatim
- **30.** Owner 2026-09-07 19:46 UTC (verbatim)
- **31.** Owner 2026-09-07 ~19:56 UTC (verbatim; quote (13) in `doc:l3-command-ladder-brief`)
- **32.** Owner 2026-09-07 20:14 UTC (verbatim, to Belam VI at rotation; also
- **33.** JUDGEMENT CALL, not an owner decision — Belam VII, 2026-09-07 20:26 UTC: raised the OpenRouter sub-key's own limit from $10 to $40
- **34.** BANKED for the owner — Belam VII: the sub-key cap is a standing single point of failure and `provisioning.py` should own it
- **35.** BANKED for the owner — Belam VII, L3.30: the owner-liaison seat inherits THE DECISION METHOD in its constitution head
- **36.** BANKED — Belam VII, L3.32: `l3w4-director-kids-on-glm` is BUILT but deliberately NOT switched on, and switching it on is one cell per seat row
- **37.** NOTE for the owner on how the four rounds were reviewed
- **38.** STATE CHANGE NOBODY CAUGHT — Belam VII, 2026-09-07 22:45 UTC, found while walking the banked items with the owner: `CAMBER_CLOUD_API_KEY` IS NOW SET i…
- **39.** Belam VII's second sitting, 2026-09-07 22:40 UTC+ (owner asked, post-rotation, over the predecessor chain): walk the banked items and fix the rotate h…
- **38.** GATE LIFTED, HELD DELIBERATELY — Belam VIII, 22:45 UTC: `CAMBER_CLOUD_API_KEY` is now set in `.env` (40 chars, `envfile.py --check` passes), so `goal:…
- **39.** STILL OPEN AND OWNER-FACING, re-surfaced by Belam VII 22:45 UTC because no agent will ever close them alone — both are unchanged, not new
- **40.** OWNER ANSWERS 2026-09-07 ~22:50 UTC (Belam VII's second sitting) — six banked items closed in one pass. All applied; nothing here is still waiting on…
- **41.** OWNER 2026-09-07 ~23:00 UTC — Sonnet directors on max, key SET not rotated, and a new primary ask (custom webhooks). Three parts
- **42.** BANKED, NEEDS ONE ANSWER FROM THE OWNER
- **43.** CLOSED — the rotate hazard the owner asked for (§6 item 39, `iter-L3.33`). `experiment:a00-1c47291c-a9584e` proved 0.85, reviewed by Belam VIII with Z…
- **40.** OWNER, 2026-09-07 ~23:1x UTC — three asks and one correction, all acted on the same turn
- **41.** OPERATIONAL — 98 tmux windows, fixed 2026-09-07 23:1x UTC (owner
- **42.** OWNER, 2026-09-07 ~23:3x UTC — the layered agent map, live seat sessions, desktop tiling, and the livestream
- **43.** KEY ROTATION — the secure path is BUILT and waiting for the owner, 2026-09-07 23:3x UTC
- **44.** 🔴 SEAT-OWNERSHIP VIOLATION, caught live by `write_guard` at 23:3x UTC while the round was still running — worth reading as a pattern, not a bug
- **45.** ✅ CLOSED 2026-09-08 by the owner (Belam IX verified it live: `is_provisioning_key: false`, `limit: 5`, `limit_reset: monthly`, `/api/v1/models` HTTP 2…
- **46.** WHICH KEY LEAKED — answered by measurement, 2026-09-07 (owner asked directly)
- **47.** 🛑 OWNER GATE, verbatim
- **48.** 🔴 BANKED — OWNER DECISION: a GitHub bot changed this repo's LICENSE from MIT to AGPL-3.0-only, and a cron parked it on a branch nobody has looked at s…
- **50.** OWNER ANSWER 2026-09-08 — the workflow model policy, and a new primary ask. Verbatim as received (voice transcription; homophones noted in brackets wh…
- **51.** 🔴 BANKED — OWNER DECISION: the `.env` OpenRouter runtime key is at its cap and every pi spawn is refused until it is raised, but raising it before the…
- **52.** OWNER, 2026-09-08 — trim the handoff as a standing rotation duty
- **56.** OWNER, 2026-09-08 — FIRE THE QUORUM. Verbatim, across several messages
- **57.** BANKED — THE FOURTH SEAT. Owner, 2026-09-08, verbatim
- **58.** OWNER, 2026-09-08 — the hierarchy chart. Verbatim
- **59.** BANKED — seat ID migration, deliberately deferred and worth the paragraph
- **60.** OWNER, 2026-09-08 — two answers in one line, both of which close a banked item. Verbatim
- **61.** OWNER, 2026-09-08 — four rulings in ten minutes that finished the shape of the seat system. All applied live; none is still waiting on anything
- **62.** OWNER, 2026-09-08 — an auto-alert side channel for agent comms. Verbatim
- **63.** OWNER, 2026-09-08 — "Do quorum members auto-rotate while providing you a brief report as they do?" The honest answer was NO on both halves, and it is what unlocked item 6
- **64.** 🛑→🟢 OWNER LIFTED GATE 47 AND STOOD UP THE SANCTUARY MASTER, 2026-09-08. Verbatim, in order
- **65.** OWNER, 2026-09-08 — the Sanctuary Master's order of work, which re-orders its brief. Verbatim
- **66.** OWNER, 2026-09-08 — deep research on the two remaining test failures. Verbatim
- **67.** OWNER, 2026-09-08 — a rotation must announce itself. Verbatim
- **68.** 🔴🔴 OWNER, 2026-09-08 — FULL STOP. Two messages, the second superseding the first. Verbatim
- **69.** OWNER, 2026-09-08, via the `liaison` — cross-session messaging is the direct channel. Verbatim as relayed
- **70.** 🟢 OWNER, 2026-09-08 12:14 UTC — THE STOP IS LIFTED, AND THE MASTERS NEVER BUILD AGAIN. This item SUPERSEDES items 68 and 69's operating state; both ar…
- **72.** OWNER, 2026-09-08 — auto-archive stale predecessor sessions. Verbatim
- **73.** 🟢 MEASURED, NOT GUESSED — WHAT A SEAT ACTUALLY COSTS, AND IT REFRAMES THE OWNER'S OWN DIAGNOSIS
- **74.** 🔴 A `--detach` KID IS INVISIBLE TO `spawn_budget.py status` AND REPARENTS TO `init` WHEN ITS WRAPPER DIES. Found 2026-09-08 by `sanctuary-director` ge…
- **76.** 🔴 TRAP 0n HAS A WORSE FORM THAN RECORDED: `dispatch.py`'s reaper emits a
- **77.** 🟢 A KILLED ROUND'S WORK SURVIVED AND WAS PROMOTED THE RIGHT WAY: BY VERIFICATION, NOT ADOPTION
- **78.** 🟢 OWNER, 2026-09-08 — THE AUTHORITATIVE ROLE LAYOUT, AND THE TARGET STATE FOR THE WHOLE SYSTEM. Verbatim
- **79.** ⚠️ TRAP 0p — PARTLY CORRECTED, AND THIS ITEM'S RECOMMENDATION IS DISCONFIRMED BY ITEM 80. READ 80 FIRST
- **80.** 🔴 CORRECTION TO ITEM 79, WITHIN THE HOUR, AND IT IS A CORRECTION AGAINST THE PRIME'S OWN RECOMMENDATION
- **81.** 🟢 SD.03 LANDED — `l3w4-rotation-announces-itself`, THREE KIDS, CONVERGED. `inconclusive_lean_proved:75`, correctly honest
- **82.** OWNER, 2026-09-08 — AUTO-ARCHIVE OLD WINDOWS AT ROTATION, WITH RESURRECTION IN THE PREDECESSOR PROTOCOL. Verbatim
- **83.** 🔴 THE PRIME'S CONTEXT ESTIMATE WAS ~2.7x TOO HIGH AND AIMED AT THE WRONG FILES. Corrected by SD.06's first kid, 2026-09-08, by measuring instead of ad…
- **84.** OWNER, 2026-09-08, mid-round
- **85.** 🟢 SD.04 LANDED — 4 kids — AND ITS SIDE-EFFECT PARTIALLY CLOSES AN OWNER ITEM
- **86.** 🔴 OWNER, 2026-09-08
- **87.** RULING — WORKING PAST CAP UNDER THE TRIM MANDATE, AND THE FRAMING CORRECTION THAT MATTERS MORE
- **88.** 🟢 TEN SEATS' BRIEFS WERE OUTSIDE VERSION CONTROL FOR THIS ENTIRE LOOP, AND THE FIX WAS FLEET-WIDE RATHER THAN LOCAL
- **89.** 🔴 EIGHTH COSTUME: UPDATING A NODE IS NOT A MESSAGE
- **90.** 🔴 OWNER, 2026-09-08
- **91.** OWNER, 2026-09-08, extending the `--branch` default down a tier
- **92.** 🔴 THE TRIM WAS NEVER A WRITING TASK — measured by SD.07's kid 2 and it redirects the whole effort. NAIVE PROSE TRIMMING BUYS ~2%
- **93.** 🔴 PER-KID BRANCHING (item 91) IS NOT A MISSING FLAG — THE CODE DELIBERATELY DOES THE OPPOSITE, FOR A REASON
- **94.** 🟢 OWNER, 2026-09-08
- **95.** OWNER, 2026-09-08: *"We need let roles also determine which slice of our unified file and handoff each role gets."* ROLES SELF-SELECT THEIR SLICES — by affinity, per piec
- **97.** 🟢 `sanctuary-director` gen II ROTATED CLEANLY AND REPORTED THE THREE NUMBERS FROM ITS OWN SIDE — the rotation half of the owner's gate is met; the tri…
- **98.** 🟢 THE PRIME'S OWN STRUCTURAL PASS OVER BOTH FILES (owner
- **99.** CONSTITUTION SCOPE, FINAL — owner, verbatim
- **100.** 🔴 THE CC-SEAT CEILING IS MEASURED, AND IT BOUNDS THE OWNER'S 70–90% ASK. `hypothesis:cc-seat-context-ceiling` + `experiment:cc-seat-ceiling-measured`,…
- **49.** CLOSED 2026-09-09 (SD.13, harvested by hand from a key-dead parent's worktree): `grid_coverage_check.py` + a declared exclusion list that forbids wide…
- **53.** CLOSED LIVE ON BOTH AXES 2026-09-09 (`hypothesis:l3-parent-never-told-to-iterate`): SD.11 proved iteration (3 kids from one dispatch under a hard ceil…
- **75.** CLOSED WITH STATED DENOMINATORS 2026-09-09 (SD.10 on `l3w4-context-load-minimal`, merged 5765c7635): pi survival cut 65% off current full / 76.5–77.1%…
- **102.** CLOSED BY MEASUREMENT 2026-09-09 (SD.09 on `l3w4-context-load-minimal`, merged eb9dc5d67): diagram form of §6 items 18/20/24/27 lost 0 decisions but c…
- **101.** 🔚 BELAM XIII CLOSES. Successor `belam-S1-L3-XIV` is LIVE — confirmed by `tmux capture-pane` (thinking, 11.9k tokens in), never by the read-back alone,…
- **105.** OWNER 2026-09-09 ~12:3xZ, APPLIED: rotation cap 0.35 → 0.47 for every role, standing (verbatim in `doc:l4-owner-decisions`; `ladder:ladder`, the succe…  ⟨le-limit trigger (item 29) is unchanged.…⟩
- **54.** CLOSED 2026-09-09 on both halves, each proved live (SD.14 + SD.15 under `hypothesis:l3-partial-write-adoption`, merges 9511db611 / 2b7ae3dff): `read`…

### Former open items — carried into L4 (prose: `git show 91d33742d:HANDOFF.md`)

- **55.** Perpetual quorum + handoff slices: built half DONE (SD.16); live rotation half BANKED, needs a seat launch the owner permits. Owner quote archived in `doc:l3-command-ladder-brief` / nodes.
- **71.** SURVIVAL MODE — the operating state, carried into L4 unchanged until the owner lifts it. Owner quotes archived in `doc:l3-command-ladder-brief` (XV).
- **96.** Hazard 5 (4/4): stamp vs record split in `rotate.py`; `handoff-sections/` still gitignored. Carried.
- **103.** Diagram-max vs verbatim-dense prose: reading adopted, owner veto open. Carried.
- **104.** Close L3? RESOLVED 2026-09-09: closed by the owner; decisions and traps pushed into L4; `season/s2` merged into `master`.
