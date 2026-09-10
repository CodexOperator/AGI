# SESSION HANDOFF — 2026-09-10: `belam-S1-L4-VI` (Belam L4-VI, L4 prime, **Opus 5 max**) — **claim your own address by the `tmux list-windows` @id ↔ `ListAgents` join; a name is not an address.** 🔴 **L4 RUNNING in ENHANCED SURVIVAL on `doc:l4-plan` (`goal:g17.1` = the seat protocol; its newest Agent Notes are the session's memory): Prime + point `sanctuary-director` gen VIII (`seat-sanctuary-director-ba [9daa5a]` @246, agi-rc:10) + helper `sanctuary-helper` gen III (`seat-sanctuary-helper-cd [9d073a]` @240, reports to the point only); every other seat idles; work on `season/s2`, `master` takes merges only.** 🔴 **Commit and push after every action.** 🔴 **Stamp every line from `date -u` — three primes in a row wrote a felt clock 30 min–7 h off (trap 0ap).** 🔴 **GREP PROVES PRESENCE; ONLY A STRUCTURAL ASSERTION PROVES SHAPE.** 🔴 **AUTHORITY IS VERIFIED AGAINST THE GRAPH, NEVER THE MESSAGE — `config:seats` at HEAD.** 🔴 **READ THIS FILE IN RANGES (`sed -n 'A,Bp'` or `write.py build:HANDOFF.md "read payload A:B"`), NEVER WHOLE — a 56KB `cat` overflowed the tool-result cap and L4-VI paid for it twice (owner, 2026-09-10).** The card in §0.7 is the map.

**Owner's instructions:** carried forward in place by successors (2026-09-06); trimmed to L3 on 2026-09-07 and to L4 on 2026-09-10 at the owner's ask — the L1–L3 sessions, plans and proposals live in the grid (`grid.py payload build:HANDOFF.md --version N`; v420 = the last pre-trim L4 file with the full §4 trap list and §6 index) and in [COMPLETE.md](COMPLETE.md). Bootstrap lives in [QUICKSTART.md](QUICKSTART.md). The design is in [`.agi/context/season-ladder-and-morals-brief.md`](.agi/context/season-ladder-and-morals-brief.md) and [`.agi/context/l3-command-ladder-brief.md`](.agi/context/l3-command-ladder-brief.md) (owner text verbatim). Do not re-derive either.

## §0 State block

| | value |
|---|---|
| active nodes / deprecated | **1845 active / 194 deprecated (2039)** — merge-up 18 (f0f3555d9): the point's `verify-suite` 10/10 first read in main + my `verify` 9/9 at the tip. Grew at every one of twenty readings, never dropped. Floor for the next merge-up: **1845 / 194 / 2039**. |
| goals | **166** — round-trip byte-identical after merge-up 18. 🔴 Check with `snapshot-goals.py --render --check`, never with this row (a row and a card disagreed for two sessions once; the card was right). |
| `outcome_coverage` (primary) | **0.14** (0.147 at L4-II's open, 0.132 at XV's). Drifts DOWN as hypothesis/experiment nodes enter the denominator faster than mvps close — dilution, not regression. |
| `evidence_fraction` | **0.621** after merge-up 18 (0.561 at XVI's open, 0.385 at L2.13) — rising every session this loop. `decisive_evidence_fraction` 1.0; `unevidenced_decisive_verdicts` 0. An experiment may cite ITSELF in `evidence_runs` (it is the run); a verdict may not — the gate enforces the asymmetry. |
| tests | 🟢 **2573 passed / 3 skipped**, 10/10 on the first read (four runs in a row: L4-V's rotation, merge-ups 17 and 18, L4-VI's rotation). 🔴 **THE TWO-READ PROCEDURE IS RETIRED (L4.101): a red first read is a GENUINE failure, never an ordering artifact.** 🔴 A NEW FILE IN `bin/` STILL NEEDS THE SUITE (`test_bin_help_smoke`); ship new tools as SUBCOMMANDS. 🔴 A green suite is not a working command; a green test can *require* a defect (L4.74); a green `verify` says NOTHING about a credential's validity. |
| broken links | 0 (18 retired payloads unresolved, not damage) |
| crons | 🟢 **ON — verify with `crontab -l` and the live log `~/logs/agi-crons-agi-2f118e6f.log`, never with this file.** `grid_sync` `*/5` runs `grid.py commit --all --prefix 'cron: '`; `branch_push` pushes the CHECKED-OUT branch at :07 hourly; `.geometry/crons.md` declares `crons_live: true`. Consequences: **push by hand anyway** (a dead box strands up to 59 min) and **the auto-versioning hazard IS armed** — half-finished source from a killed agent is grid-versioned under the cron's name within 5 min, so kill cleanly and `git reset` unreviewed staging at once. |
| branch | **`season/s2`**. `master` = season 1, **frozen**: merges + cherry-picks only, never rebase. Grid `commit --all` runs on `season/*` or master only — never `--allow-branch`. |
| agents live | **Prime `belam-S1-L4-VI` = `agi-31 [aca130]` @247 (agi-rc:9), row written by L4-V from the join BEFORE I acted (6da89f01e), verified at HEAD by me, not rewritten · point `sanctuary-director` gen VIII `seat-sanctuary-director-ba [9daa5a]` @246 (agi-rc:10) · helper `sanctuary-helper` gen III `seat-sanctuary-helper-cd [9d073a]` @240 (to the point only).** Belam chain at the owner's cap of FIVE: L4-II `agi-64 [61b9c9]` @235 · L4-III `agi-7f [7902ac]` @239 · L4-IV `agi-a5 [e7f117]` @242 · L4-V `agi-06 [66537b]` @244 · L4-VI (L4-I reaped by L4-V at rotation, the oldest each rotation — owner dd0f977c6). Idle seat predecessors `6f9bb5` @238 (gen IV; window named `.gen5`), `3d6888` @241 (gen V; window named `.gen6`), helper gen II `dc94bb` @237 — window names lag the gens, the ref is the address; kept as fixtures until 0a's reaper lands. Idle predecessors read NO mail (trap 0v); reach them with `send.py send`. 🔴 **The `--seat` meter is FAIL-OPEN: never trust a `source=seat_pin` reading you did not claim yourself.** |
| spend | **ACCOUNT $16.03 remaining of $107.00** (read through `OPENROUTER_PROVISIONING_KEY` at 22:31Z; ~$0.9/3h at this cadence). 🔴 **The `.env` `OPENROUTER_API_KEY` names a DELETED key (owner, 2026-09-10) and `envfile.py --check` passes on its PRESENCE — a green `verify` says nothing about it.** The loop runs because provisioning is AVAILABLE: every spawn mints its own ~$5 key; the pre-flight (306b77bb6) skips the runtime leg while provisioning is up. Per-spawn keys are **revoked at agent finish — observe DURING, a post-hoc diff cannot see them.** Below **$1.00 account-wide** the point finishes its open round and stops dispatching pi. **FALLBACK (owner, verbatim in `doc:l4-owner-decisions`): SONNET PARENTS AND KIDS via `--harness claude-code`** — the WORK tier falls back; a director's model is a separate formation question he has not decided. 🔴 `agi` ($10.92/$40) is the one unexplained credential left; the owner named only `backup`, so it was NOT touched. |
| pi parent model | **`deepseek/deepseek-v4.1-flash` (owner order 2026-09-10 ~22:2xZ, verbatim in `doc:l4-owner-decisions`)** — landed at 55783ac8a in the THREE places a dispatched parent actually reads: ladder pi parent rows (tier 1 + tier 0) + `harnesses.pi.models.parent` + `allowed_models`; proved from the built command (`dispatch.py … --dry-run` → `--model deepseek/deepseek-v4.1-flash`). 🔴 `agent_dispatch.model` (6da89f01e) is read ONLY on the legacy no-`harnesses` path — a cell nothing reads here. Kids stay `~deepseek/deepseek-v4-flash-latest`; rounds already live keep their spawn model. |
| disk | 81% |
| this session | **Belam L4-VI (2026-09-10 22:15Z →, claude-opus-5 max, `agi-31 [aca130]` @247, agi-rc:9).** Pin 0.1885 claimed on my own transcript at 22:30Z. See DONE. |

## §0.7 L3 CLOSED 2026-09-09 (rounds L3.01–L3.44 landed; detail: `git log --oneline iter-L3.01..iter-L3.44`, [COMPLETE.md](COMPLETE.md), grid v420) · L4 OPEN on `doc:l4-owner-decisions`

Two L3 lessons kept: check `git rev-list --count season/s2..<branch>` before believing a `--branch` parent landed anything; diff a branch against its **MERGE-BASE**, never a moved `season/s2`. Under L4 the POINT dispatches (`dispatch.py . L4.NN --target <node> --level small --tier parent --harness pi --branch`, from its own worktree); the Prime never dispatches.

### 🔴 Where it stops — Belam L4-VI, live 2026-09-10 (L4-V's last card: `git show 498ee2c97:HANDOFF.md`)

```
BELAM L4-VI — LIVE (Opus 5 max, standing — owner)   agi-31 [aca130] @247 / agi-rc:9   season/s2 @ f0f3555d9+   2026-09-10 22:5xZ (date -u)   pin ~0.22 / cap 0.47   ACCOUNT $16.03 of $107.00 at 22:31Z
L4     GO (owner 2026-09-09; plan parts 1-7 CONFIRMED verbatim in doc:l4-owner-decisions "L4 PLAN"; names + role diagram in doc:l4-plan §0.9)
PLAN   doc:l4-plan (§2 cards, §5 rounds L4.02-L4.27 + ad-hoc L4.28+, §6 questions) · Q1-Q30 in doc:l4-owner-decisions "L4 BANKED QUESTIONS"
SEATS  goal:g17.1 = the Texas two-step formation + EVERY measured seat-protocol rule (owner verbatim; the newest notes are the rulings on 0a's gate, the ack channel's prime-path proof, the reaper, the respawn)
       session worktrees .agi/worktrees/seat-<name> (seat/<name>@s2; kept across rotations; merged + deleted at session complete; grid runs ONLY on season/s2 after the merge) · ladder caps.director_kids 3
LANDED merge-ups 1-18 = season/s2 aafb4be0a -> ... -> b9beea8bf -> f0f3555d9 (1828 -> 2039 nodes, never a drop; suite 2270/1 -> 2573/3), rounds L4.01-L4.108 + L4.120-122 — one note per merge-up in goal:g17.1;
       do NOT re-derive. Merge-up 18 = L4.120 trimguard is now `cli.py trimguard` (the untracked .agi/sessions/trimguard.py is superseded) · L4.121 commit-guard worktree-toplevel bypass closed (agent-git
       pre-commit/pre-push hooks) · L4.122 provisioning-absent closed as already fixed · L4.108 stale-base guard: a --branch dispatch from a seat BEHIND season/s2 refuses with exit 3 until synced
       (`--allow-stale-base <reason>` records an override) — intended discipline, not a bug.
       Closed sagas, dead by measurement — do not re-open: THE REAPER = system-wide PSI on /proc/pressure/memory (ANY process on the box), knob CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP exported by every
       spawn path since L4.55 · THE RESPAWN BLEED (a finished parent restarted onto its own round) fixed at merge-up 4, proven L4.55 · FREE MODELS = NO (availability is not capability; only 2 of 21 usable;
       enumerate by pricing == 0, the :free suffix misses 14%) · BATCHING = no OpenRouter route (re-probe /files each rollover) · READ-BACK false negative = the reader read a DEBUG LOG; replaced by the
       explicit ack channel (L4.106), proven on BOTH seats (gen VIII `continue` 22:10Z, prime `diff` 22:17Z) · THE TWO-READ SUITE RULE retired (L4.101) · qwen/qwen3.8-27b spend is the owner's, authorized.
LIVE   (point's lanes, dispatching on deepseek since 55783ac8a; ~6-8 pi parents concurrent — owner) L4.109 = (b) hypothesis:l4-dispatch-echoes-less-than-it-knows on dispatch.py · L4.110 = 0a (rulings A/B folded
       in, ceiling 3 serial) · L4.111 = hypothesis:l4-workflow-types-and-default-harness-are-a-geometry-node · NEXT in the dispatch.py lane after L4.109: hypothesis:l4-a-round-alarms-its-dispatcher-by-default
       (OWNER 22:44Z, g4.7 — completion/death/timeout each send ONE nudged dm to the seat stamped dispatched_by at spawn, no flag; the defect that lost L4.120/121's completions) · then the model-change
       round · the SERIAL chain on rotate.py: 0a -> 0b hypothesis:l4-startup-is-one-script-or-a-driven-prompt
       -> 0c hypothesis:l4-identity-is-a-signature-not-a-story (MODULAR: swappable Signer/Verifier, ed25519 default, secp256k1/EIP-191 so a wallet key can be a seat key; on one box a spoofing guard, not
       access control) · (a) hypothesis:l4-a-seats-live-model-is-measured-not-assumed (meter prints live vs row + DRIFT, verify gains a FAILING seat-model check, telemetry PUSHED never polled; its
       rotate.py half after 0c) · (b) hypothesis:l4-dispatch-echoes-less-than-it-knows (one line per spawn, no key material on stdout, spawn.json redacted) · workflow rounds under goal:g1.14:
       hypothesis:l4-workflow-authoring-is-a-harness-tool (L4.105 landed the author verb; rounds 2/3 follow) + hypothesis:l4-workflow-types-and-default-harness-are-a-geometry-node ·
       hypothesis:l4-the-suite-lock-belongs-to-pytest-not-its-caller (L4.107 landed the per-worktree lock; cross-worktree exclusion is STILL the Prime's coordinated window) ·
       hypothesis:l4-a-seat-rotates-at-its-own-line (OWNER 22:44Z, g17 — config:seats sanctuary-helper carries rotate_at 0.29 NOW, inert until rotate.py honors a row's rotate_at over the ladder's
       0.47 in meter/loop/rotate-self/alarms; SERIAL on rotate.py behind 0c; until it lands the helper self-rotates at 0.29 by the point's brief — the owner measured it losing track past 0.3) ·
       NEW (owner 22:27Z) hypothesis:l4-a-model-change-is-one-write-and-harness-config-is-ours under goal:g4.6 — derive not sync (ladder roles row = the one source; allowed_models derived);
       harness-home files (~/.pi/agent/settings.json, models.json) become build-node payloads at a configurable locations.pi_home; proof on a FIXTURE + temp home, the live cut-over is ONE commit the
       Prime reviews · helper lane: L4.120-122 LANDED at merge-up 18; the helper takes its next lane from the point.
HELD   hypothesis:l4-the-stream-goes-live = L4's FINAL round (goal:g18.1 ACTIVE; goal:g18 the product, PERPETUAL/HORIZON under vision:self-perpetuating) — until the rotate chain and the workflow rounds land:
       streamer-stub to fresh accounts the round creates, owner's one touchpoint = backup email info when asked, verified from a second network 60 min, keys off ps, dox pre-flight, delay >= 30 s.
RULED  by the Prime, recorded in goal:g17.1, do not re-open: 0a's config-gate — (A) rotations.md STAYS type config prime/owner-only, the round proves on a FIXTURE and ships body + the exact create line,
       the PRIME creates it once at merge-up (same as the L4.94 hook and 0b's install: a round proves on a fixture, the Prime installs once and verifies with a fresh session, never a seat);
       (B) a SELF-ROW carve-out as DATA in schemas/[config].md (self_row: list seats, key name, fields session_ref/generation/window) + ONE generic rule in write.py's _enforce_written_by —
       a seated writer may update only the row whose name equals its RESOLVED seat, only those fields; role/model/tier/harness/effort/owning_goal/worktree/rotated_by stay prime/owner-only, refused whole.
       · the suite window is ADVISORY not exclusive across worktrees (cd964481c) — every run coordinated with the Prime · parallel rounds GO · always prefer dispatch · L4.09 GO (Prime may re-order
       without a fresh go) · enforce written_by on ROLE never actor · prayer per SESSION not per turn · gpt-5.1-codex spend is not the engine's · the three sk-or-v1-537bbe7c… experiment nodes are
       ARCHIVE and correct as they stand, never edited.
GATES  owner GO only: 🔴 INSTALL THE ROTATION-REMINDER HOOK? (L4.94, built, 3 defects repaired, deliberately NOT installed — touches every session on this box; recommended YES scoped to a project
       holding .agi/ past threshold; the PRIME installs and verifies, not a seat) · L4.07 perpetual flip of 12 gN · L4.13 seat nodes · banked, not urgent: rotate the engine onto a FRESH runtime key.
RULES  earned, each with an instance behind it (full text goal:g17.1): a remedy that reuses the broken mechanism is not a remedy · a guard the standard remedy disarms certifies the state it failed to
       check · a mitigation that hides the symptom before the cause buys a green light and loses the bug · two measurements that agree too precisely are one measurement · observe DURING, a post-hoc
       diff cannot see an ephemeral resource · a round whose falsifiers contradict each other, and a claim whose conjuncts contradict, are the same check at two altitudes · a round that fixes the gate it
       must pass through is hand-landed · MECHANISM, NOT WORDING (cite the mechanism, never a correlate) · identity is SUPPLIED never inferred · authority is verified against the graph · detect, do not
       repair · a dead pid proves stopped, a live pid proves nothing · a claim about a reader that was never read is wording · a disprover run before dispatch is the cheapest round there is · in a live
       system only MONOTONE facts survive the latency of the investigation that measured them · a check that guards a PROXY for the resource certifies the state it failed to inspect (suite lock,
       envfile.py) · a stamp reasoned from context is a felt clock even after you have written the warning down · L4-VI's: a config cell nothing reads is a change that reports success — prove a
       config change from the BUILT command (dispatch --dry-run), never from the diff.
NEXT   1 REVIEW merge-up 19 when the point sends numbers (one message, numbers only — owner standing order): read the BYTES on season/s2 (`git log --oneline <old tip>..`, zero deletions under .agi/nodes,
         the experiment nodes' verdict + evidence_runs, a spot-check of each claim against the code, `commands.py run verify` 9/9, active never below 1845), accept or demote, one note in goal:g17.1,
         floor row above updated. Merge-up 18 took ~8 tool calls this way.
       2 The point holds 0a's config-gate ruling (RULED above) and the new g4.6 round; it dispatches — you review. Never pull work back to the Prime, never dispatch yourself, never write in a seat's worktree.
       3 🔴 0b edits the LIVE global SessionStart hook and 0a's rotations.md is prime-created: at THEIR merge-ups the PRIME installs / creates once and verifies with a fresh session.
       4 Watch the ACCOUNT through provisioning (`provisioning.py status` shows keys and outstanding spend; the balance is `/api/v1/credits` with OPENROUTER_PROVISIONING_KEY) — never the .env key.
       5 Rotate at 0.47: **handoff FIRST** (the handoff is the first artefact to degrade), then `rotate.py loop --role prime_director --name belam-S1-L4-VII --model claude-opus-5 --effort max
         --timeout 900 --force --session-log <own .jsonl>`. Confirm by the ListAgents/@id join or capture-pane, then the ack record in .agi/sessions/rotations/. Write the successor's
         config:seats row from the JOIN before it acts (L4-IV and L4-V both did; the successor VERIFIES at HEAD, never rewrites) — until 0a lands and does it inside rotate-self. Reap the oldest
         Belam by PID so the chain stays at five (owner). 🔴 A successor: read your OWN model from your transcript's newest turn before trusting the row — the harness silently downgraded
         the point to opus 4.8 mid-session once (`model_refusal_fallback`, [cyber] false positive; goal:g17.1 793b40cf1) — until round (a) lands and pushes it to you.
FIRST  (until 0b's bootstrap lands) ls -t .agi/comms/season-2/dm/ and read anything addressed to you BEFORE the smoke · claim your own pin FIRST: rotate.py meter --pin .agi/sessions/belam.meter
       --session-log <own .jsonl> · verify your seats row at HEAD · run verify-suite ONCE in the foreground (the suite window is yours; it refuses against a live holder) · read this file in RANGES.
MODE   ENHANCED SURVIVAL (owner 2026-09-09): Prime + point + helper; every other seat idle; pi/OpenRouter does the work; the Prime reviews and never spends the Claude budget on chores a seat can do.
RULES  standing, EVERY role: trim + diagram-max handoff/context files as parts finish · owner verbatim lives in NODES only (vision/goal/hypothesis/doc), never here · ROTATE AT 0.47 · partial edits:
       write.py read N:M then replace N:M · directors message the Prime ONLY when necessary (merge-up numbers · a Prime-only decision · a rotation line · a red merge / rule-changing finding; owner
       2026-09-10 05:0xZ verbatim in doc:l4-owner-decisions) · config:seats is YOURS to write while the Keep is down (write.py "set seats <json>", the whole list, byte-verify) · never git add -A ·
       never read $? through a pipe · never sweep off a ps grep (a pgrep for 'pytest' matches every claude command line carrying the word — 190KB, L4-VI) · never run the suite twice at once ·
       never background a long verification · never trust an `updated:` line · never adopt a seat's work instead of verifying it · never let test_send.py run unguarded while seats are live
       (send.py nudges REAL panes; L4.10) · never rotate a seat with AGI_BRIEF_PROFILE=survival · never reap @238/@241/@237 by hand (0a's reaper takes them under the owner's rule).
CRONS  ON: grid_sync */5 + push of the CHECKED-OUT branch at :07 (verify with crontab -l, never this file) -> push by hand anyway
DONE   L4-I..L4-V: one line each in `git show 498ee2c97:HANDOFF.md` (DONE block) — L4-I gate + plan minted + g17.1 + helper; L4-II verification.py + reaper knob + merge-ups 2-4; L4-III merge-up 5 +
       ceiling banked; L4-IV merge-ups 13-15, repo PUBLIC, L3 predecessors reaped, trim guard rescued two owner quotes; L4-V merge-ups 16-17, ten owner messages banked -> nine rounds, g1.17/g18/g18.1
       minted, ack channel's first live success, chain capped at five.
       L4-VI (cont.): merge-up 18 ACCEPTED from report + bytes (1845/194/2039, 2573/3, evidence 0.621) · owner's helper-0.29 + auto-alarm message banked verbatim, the seat cell written, two rounds minted (g17 rotate
       line, g4.7 auto-alarm) and handed to the point in one message · L4.120/121's missed completions measured (both done on their agent branches) before acting.
       L4-VI: gate answered with a five-hunk DIFF through the ack channel — the FIRST diff ever read back on the prime path (record 22:17:52Z) · seats row VERIFIED at HEAD (L4-V wrote it from the join)
       · pin 0.1885 claimed on my own transcript · verify-suite 10/10 FIRST read (2565/3, 1836/194/2030) · merge-up 17 accepted (the suite was the one open item; gen VIII 10/10 in main + mine) ·
       the owner's parent-model order made REAL in the three places a parent reads (55783ac8a; the point's category-4 was correct: 6da89f01e changed the one cell nothing reads) · the owner's
       "one write, harness config is ours" ask banked verbatim + minted under g4.6 with the derive-not-sync answer · 0a's config-gate (A)/(B) RULED as schema data · ack prime-path proof noted on the
       round-4 node · handoff trimmed 56.6KB -> this, through the guard before and after, L3 block + §4 traps + §6 index collapsed to pointers (owner order 498ee2c97).
```

## §4 Traps — carried into L4

The full headline list (0al … 4): `doc:l4-owner-decisions` → **"TRAPS CARRIED INTO L4"** (the node, line 62) and grid v420 §4. The ones a cold prime hits first: **0ap** stamp from `date -u`, never from prose · **0al** a `.geometry` node the suite pins is CODE — run the suite after writing one · **0aj** `dispatch.py --dry-run` TRUNCATES the brief it prints · **0y** an exit code read through a pipe is the LAST command's · **0r** `write.py "note X && note Y"` keeps only the LAST note · **1** prose verbs cannot contain `&&` · **0c** `rotate.py meter` reads the NEWEST `.jsonl` unless `--session-log` is explicit · **0v** a `SendMessage` success is evidence the transport worked, never that the right seat read it · **0e** never run the engine suite twice at once · **0i** never run `level3.py` without `--dry-run`.

## §5 Known-good verification sequence

```bash
git branch --show-current                                   # season/s2
python3 extensions/agi/bin/commands.py run verify-suite     # the prime's ONE rotation command (L4.44, owner 2026-09-10): links, goals round-trip, guard, smoke + never-lower baseline, viewport, dispatch, budget, then the engine suite under a lock (~3 min)
python3 extensions/agi/bin/commands.py run verify           # the same without the suite (26s): every other role, and the Prime after each merge-up
python3 extensions/agi/bin/grid.py commit --all             # 0 errors since L3.20
git push origin season/s2
```

## §6 Owner decisions — settled, do not re-ask

**Every §6 item (0–105) is CLOSED or carried, and the index of one-liners was collapsed on 2026-09-10 (L4-VI, owner order 498ee2c97) after the guard (`python3 .agi/sessions/trimguard.py`) was run before and after.** Where the content lives: owner quotes verbatim, keyed by item number, in `doc:l3-command-ladder-brief` → *§6 OWNER VERBATIM ARCHIVE* (167 quotes) and, from L4 on, in `doc:l4-owner-decisions`; the one-line index in grid v420 (`grid.py payload build:HANDOFF.md --version 420`); the last full-prose file is v298. 🔴 **An archive marker is a CLAIM, not a verification** — the guard found two owner quotes that existed only in this file on its first run (items 29 and 91, since archived). Run it before removing a single quoted line; it aborts on a span that resolves in no node. The two spans it aborted on at v420 were a director's gloss (item 95) and a predecessor's prose (item 63) — adjudicated, not owner quotes, and removed with the index.

### Former open items — carried into L4 (prose: `git show 91d33742d:HANDOFF.md`)

- **55.** Perpetual quorum + handoff slices: built half DONE (SD.16); live rotation half BANKED, needs a seat launch the owner permits. Owner quote archived in `doc:l3-command-ladder-brief` / nodes.
- **71.** SURVIVAL MODE — the operating state, carried into L4 unchanged until the owner lifts it. Owner quotes archived in `doc:l3-command-ladder-brief` (XV).
- **96.** Hazard 5 (4/4): stamp vs record split in `rotate.py`; `handoff-sections/` still gitignored. Carried.
- **103.** Diagram-max vs verbatim-dense prose: reading adopted, owner veto open. Carried.
- **104.** Close L3? RESOLVED 2026-09-09: closed by the owner; decisions and traps pushed into L4; `season/s2` merged into `master`.
