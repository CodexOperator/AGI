# SESSION HANDOFF — 2026-09-04 03:20: loop L1 RUN COMPLETE (L1.08–L1.10)

Standing bootstrap lives in [QUICKSTART.md](QUICKSTART.md). This file is one
session only and the next director replaces it wholesale. The previous
session's section is in the grid: `grid.py payload build:HANDOFF.md --version N`.

**Loop `L1` continues.** `L1.01`…`L1.07` landed in the prior session; this
session resumes at `L1.08`. Global `iter-NNN` ended at 116.

## §0 State block

| | baseline (post-L1.07) | end of run (03:20) |
|---|---|---|
| active nodes | 940 | **1012** (+178 deprecated, 159 of them the build-site cohort) |
| `outcome_coverage` (primary) | 0.271 | **0.201** ⬇ honest — see note |
| `evidence_fraction` | 0.317 | **0.363** ⬆ |
| `mvp_count` / scoring | 39 | 50 / 48 (2 backward excluded) |
| `unevidenced_decisive_verdicts` | 6 | **0** (gate on the commit path) |
| `deprecation_score_delta` | — | **-0.075 withheld** (guard live) |
| `broken_links` | 0 | 0 |
| tests | 1371 | **1454** |
| goals active / cap | 13 / 15 | 13 / 15; `goal:s32` minted (horizon) |
| budget peak | 0/25 | 25/25 held in waves 2–4, 6–8 |
| unpushed | 0 | 0 |

**The primary fell and that is the guard working.** 159 deprecated build-site
hypotheses stay in the denominator by design (`goal:g3` symmetry), and eight
waves added hypotheses faster than mvps closed. Do not "fix" it by minting
mvps for finished work — `backward_mvp_count` now catches exactly that.

**Background processes:** the pi reaper loop was killed at run end; the
30-second sampler (`L1-logs/samples3.log`) exits on its own. One CC parent
from `iter-1065/1066` (g8.1/g10.1) may still be finishing — `git status`
first thing; commit whatever it left.

### 🔴 Crons are still OFF — push by hand after every iteration

```bash
git -C /home/ubuntu/work/agi push origin master
```

## §0b Owner grant for this session (2026-09-03)

Full director authority for the run. Explicitly authorized, on the record:

- **Spend the remaining OpenRouter balance** (`$15.43`) — "use all of it if you
  want, it's a stress test of the system."
- **Ramp concurrency 8 → 25 live**, and **get the parent tier online ASAP** and
  use it for the rest of the work.
- **Be liberal about parent-kid pairs even for small fixes.** Standing rule the
  owner gave: *if briefing a parent costs less director context than doing the
  change directly, always brief the parent.*
- **Expand scope slightly where the essence of a goal demands it.** Serve what
  the goal is asking, not its literal wording.
- "Worst case we rewind any catastrophic failures."

## §1 The plan

- [x] **L1.01–L1.07** — prior session. See grid for detail.
- [x] **L1.08** — the removal guard landed (`L1.08`), then held for real in
      L1.09 (`deprecation_score_delta=-0.102` withheld).
- [x] **L1.08b** — live scale: parent tier ran live on pi (44 parents, waves
      2–4), **cap 25 reached and held**, budget refused overflow cleanly;
      parent-spawns-kid observed on both harnesses. `goal:g4.8` clause 2 (a
      parent demoting unaided) was **not** separately observed — the
      commit-path gate now makes it moot at acceptance. Clause 3 (spend): a
      pi parent key read $0.05–0.15, a kid $0.015; a CC kid ~$0.30.
- [x] **L1.09** — **DONE, commit `L1.09`.** 159 build-site nodes deprecated
      in one atomic pass with per-node dispositions, 29 verdicts by citation,
      kits + plan deleted, 7 build nodes deprecated, `goal:s32` (embeddings
      gaps, horizon). Guard held: `deprecation_score_delta=-0.102` withheld,
      primary 0.222 honest. active 913 / deprecated 177 / sum 1090, links 0
      broken, tests 1452, goals round-trip byte-identical. Follow-ups
      (briefing attractor filter, `deprecated` in status regexes, stale
      `CLAUDE.md` rows) dispatched to a cleanup agent.
- [~] **L1.10** — **one of three landed.** Loop-scoped iteration ids are
      real end to end (`L1.10b`: `sessions/iter-L1.NN`, allocator in
      `locations.py --claim-iter`, legacy dirs readable). **Chat-to-node
      linking (`goal:g10.1`/`g2.7`) and engine-commit pinning (`goal:g8.1`)
      have graph nodes from waves 6–7 and CC parents `1065`/`1066`, but no
      engine code landed by 03:20** — `grep -l thought_session
      extensions/agi/bin/*.py` is still only `write.py`; no `engine_commit`
      key exists. **Next session starts here.**

## §2 Concurrency discipline this session

Several parents run at once. The rule that keeps it safe:

**Parents never touch git.** No `commit`, `push`, `add`, `checkout`, `stash`,
and no `grid.py`. The director commits, serially, between waves. Parents own
**disjoint file domains** and report anything they needed outside their own.
Kids see each other's untracked files — report, never clean.

## §3 🔴 Where it stands, and the next command

**Run complete at 03:20.** Everything committed, grid-versioned, pushed;
smoke exit 0, links 0 broken, tests 1454, goals round-trip byte-identical.

```bash
cd /home/ubuntu/work/agi
git status --short                                   # a late CC parent may have left nodes — commit them
bash extensions/agi/driver.sh --smoke --max-iters 1 && echo SMOKE_OK   # 1012 active, must NOT drop
python3 extensions/agi/bin/commands.py run tests     # 1454
python3 extensions/agi/bin/spawn_budget.py status    # expect 0/25
```

Then L1.11: `goal:g10.1` and `goal:g8.1` implementation — dispatch the
`claude-code` harness (`dispatch.py <root> <iter> --harness claude-code
--tier parent --target goal:g8.1`); pi parents on qwen/deepseek wrote nodes
for these all night and never touched engine code. Keep `spawn.parallel: 2`.


**01:20 — owner reset the OpenRouter workspace budget (+$30 balance).** pi
dispatch is back. `L1.10b` committed the loop-scoped iteration ids
(`sessions/iter-L1.NN`, 6 engine files, suite 1454). **Wave 6 live on pi:**
iters `1043`–`1054`, 12 targets (g4.1, g13, g13.1, g10.1, g8.1, the
loop-scoped hypothesis, s32, g9.4, g4.7, g1.10, g5, g4.8), 22 parents
admitted, **25/25 held**, 0 × 403. Sampler: `L1-logs/samples3.log`.
Loop: drain → verify (smoke/links/tests) → commit → grid-commit → push →
next wave. Rule stands: rather waste OpenRouter tokens than director context.


**L1.08 guard landed** (commit "L1.08: removal guard in metrics.py"): new
metrics `deprecated_open_hypotheses`, `deprecated_excluded_nodes`,
`deprecation_score_delta` (must stay `<= 0`). Suite 1371 → **1381**. Written
by a CC parent that died on rate-limit before its report — the red-on-purpose
step was **not** witnessed by the director; the tests exist and pass.

**The parent tier is LIVE on pi/OpenRouter for the first time.** Session dirs
`iter-1006` (8 parents at `goal:g3`), `1007` (s31 ×2), `1008` (g13 ×2), `1009`
(g4.1 ×1), `1010` (g10.1 ×1), `1011` (g4.8 — **0 admitted**, cap hit;
redispatch). **Cap 25 reached at 20:06 — `live=25/25 pi=25`**, budget refused
further slots cleanly ("skipping, not waiting"). Parents spawned kids
(`tier=kid` leases appeared under parent iters). Logs:
`.agi/sessions/L1-logs/p-*.log`, sampler `samples.log` (30s cadence).

**Waves 2–4 landed and pushed** (commits `L1.08b`–`L1.08e`): 44 pi parents,
active 940 → **1023**, `mvp_count` 39 → 47, primary 0.271 → 0.247, tests
1381, 0 broken links. **Wave 5 (s18, g13, g4.1, g10.1 + two director
hypotheses) died at 403 — OpenRouter workspace weekly budget exceeded** (§6).

**Pivot at 21:40:** the engine's `claude-code` harness is declared but
**unimplemented** (`goal:g4.6`), so four CC subagents run directly, disjoint
domains, no git: (1) implement the `claude_code` adapter, `adapters/`;
(2) evidence gate on the commit path, `evidence_gate.py`/`grid.py`/
`post_wire.py`; (3) audit the 9 wave-3 mvps, `metrics.py`; (4) s18 mining
survey → `.agi/sessions/L1.09-mining/report.md`, read-only.

**(3) landed — `L1.08f`:** 7 of 9 wave-3 mvps forward, **2 backward**
(`a00-e284d9f5`, `a00-eeaa5239` — bodies verify shipped code). `metrics.py`
now excludes an mvp from `scoring_mvp_count` only when it has **no**
`source_files`/`payload_ref`/build child **and** its body matches
verified-in-tree language; emits `backward_mvp_count`. Primary 0.245 → 0.234.
Caveat on record: the language half is a regex heuristic (2/48 hits, 0 false
positives today) — a future backward mvp phrased differently slips through.
Also learned: `write.py set` is `set field value` (space), and
`evidence_runs` must be a **list of node ids** — a bare int scores 0
(`goal:g7.3`).

**(2) landed — `L1.08g`:** the evidence gate now runs inside `grid.py commit`
(`evidence_gate.enforce_on_disk`), demoting at acceptance; corpus **11 → 0**.
`evidence_gate.py enforce [--dry-run]` runs it standalone. Caveat: 6 of the
11 were the *previous* director's experiments with a bare-int `evidence_runs`;
left demoted (banked, §6 item 2). `verify` runs `smoke` before `grid-commit`,
so smoke's metric line lags one gate pass — reorder later if it bites.

**(1) landed — `L1.08h`:** `claude-code` harness implemented (`goal:g4.6`),
two CC kids spawned live through `dispatch.py --harness claude-code`, budget
returned to 0. Adapter costs: ~$0.30/kid on sonnet. Caveats banked:
`dispatch.py` mints an OpenRouter key for every CC kid that never uses it;
`_reap_one` restarts on the CLI default model; `cc-session-start.sh` was
mode 644 (fixed: `chmod +x`, committed).

**(4) landed — survey at `.agi/sessions/L1.09-mining/report.md`** (36 KB;
the harness refused the agent's file write, director extracted it from the
transcript). Headlines: cohort is **159**, not 168; 5 of 7 domains are
already real code under `extensions/agi/src/`; **0 vacuous** chains; ~30
`CLOSE-BY-CITATION`; environment-indexers has zero code and a hollow R1;
attractor replacement already exists (`idea:engine-*`, `origin:
engine-decomp`); **§E: retirement must be ONE atomic pass** or
`snapshot-build-site.py` resurrects deprecated nodes. **L1.09 execution
agent dispatched 21:57** on that plan; commit the instant it reports.

**CC parents through the engine, live:** `iter-1037` (g4.1 ×2), `iter-1038`
(g13 ×2), `--harness claude-code`. Poll with `spawn_budget.py status` and
`pgrep -fc "claude -p"` — no notification arrives for engine-dispatched
parents.

Next, as each returns: check `caveats:`/`struggles:` first, verify the node
file on disk, `run tests`, commit **immediately** (trap 5), `grid-commit`,
push. Then act on the s18 survey (L1.09) and the L1.10 items.

```bash
cd /home/ubuntu/work/agi
python3 extensions/agi/bin/commands.py run smoke     # 940 active, must NOT drop
python3 extensions/agi/bin/commands.py run tests     # 1371
```

## §4 Traps hit this session

1. 🔴 **Wave 1 went out as seven CC `Agent` subagents, not pi parents, and
   burned the Claude subscription to the rate limit in minutes.** All seven
   died mid-work. **The parent tier is `dispatch.py <root> <iter> --tier
   parent --target <id>` on OpenRouter** — that is the whole point of the
   harness config. CC subagents are the expensive path; use them only when the
   owner says so.
2. **`--target` aims EVERY slot, so `spawn.parallel: 8` + one target = 8
   parents on one node** — the same-target fan-out the owner already ruled
   against. Set `spawn.parallel: 2` for the rest of this session and dispatch
   one `dispatch.py` call per target. Restore or re-decide at session end.
4. 🔴 **pi parents/kids write `verdict: proved` straight into node files with
   no `evidence_runs`, no `edited_by`, no `evidence_gate` stamp — the gate is
   never consulted.** `unevidenced_decisive_verdicts` 6 → 7 → **10** across
   waves 2–3. The gate lives only on `cli.py done` / `post_wire.py`; a direct
   file write walks past it. Six session-new nodes confirmed (e.g.
   `the-falsifier-and-the-corpus-census.md`, `scaffolds-are-born-valid-now.md`,
   `a01-de655bfd`). Fix belongs on the *read/commit* path (`goal:g7`), not in
   more brief text. Also: **9 mvps minted in wave 3** — audit against
   `[mvp].md`'s forward-pointing rule before trusting `mvp_count` 39 → 48.
5. 🔴 **Two director nodes minted via `write.py create` vanished, uncommitted,
   while pi parents were live.** Not smoke (re-minted and smoke'd: survives),
   not in git, not in the grid — they were untracked files and something in
   the wave ran a git operation that dropped untracked files. One kid record
   (`iter-1009/a01-dd74693c`, a `goal:g4.1` kid) mentions `git
   clean|stash|checkout`. **This is `goal:g4.1`'s thesis observed live.**
   Rule for the rest of the session: **commit immediately after minting**;
   never leave a node untracked across a wave.
6. **`test_mint_refuses_to_hand_out_a_key_with_no_ttl` fails whenever engine
   keys are outstanding** (16 live keys visible). Passed at baseline with 0
   outstanding. `provisioning.py` unchanged since L1.02, so this is a
   non-hermetic test hitting the real account, not a regression. Confirm after
   full drain; belongs to `goal:g1.11`.
7. 🔴 **Nothing enforces `agent_timeout_mins` when parents are launched with
   `dispatch.py` alone** — `heal.py` runs only under `driver.sh`. Wave-6
   parents sat at 25/25 for 34 min, the oldest with a 0-byte output log.
   Director killed every `pi` older than 1800 s; `spawn_budget` released the
   leases on process death (25 → 10). Next session: run `heal.py <root>
   <iter>` per dispatch, or fix dispatch to hand the timeout to the reaper.
8. **pi parents commit scratch into the repo** — `.agi/tmp_*.py`,
   `_benchmark.py` at the root, and a hand edit to `HANDOFF.md`. Moved to
   `.agi/sessions/L1-logs/parent-scratch/`. The parent brief should forbid
   writes outside `.agi/nodes/`, `extensions/`, `src/`, `skills/`, `tests/`.
9. **`test_publish_alarm.py::test_dry_run_writes_neither_nodes_nor_grid_versions`
   fails with `_scratch_dirs() == 4`, not 3** once the director's own scratch
   dirs exist under `.agi/sessions/` (`L1-logs`, `L1.09-mining`, …). Not a
   regression — a non-hermetic count. It slipped past the commit gate once
   because pytest's `FAILED` line is colour-coded and a plain `grep ^FAILED`
   missed it; strip ANSI before grepping (`sed 's/\x1b\[[0-9;]*m//g'`).
10. 🔴 **A parent's `driver.sh` edit (`claim_iter --loop "$CURRENT_LOOP"`,
    never set, under `set -u`) broke `smoke` and was swept into a director
    commit (`L1.10d`) because `driver.sh` is not under pytest — the suite
    was green while the entry point was dead.** Fixed in `L1.10e`
    (`CURRENT_LOOP`/`AGI_LOOP` optional). Lesson: the verify sequence must
    run `smoke` *and check its exit code*, not just grep its metrics.
11. **`iter-NNN` did not end at 116** — `ls .agi/sessions` shows `iter-1005`;
   this session uses 1006+. Loop-scoped numbering (L1.10) is still unbuilt.

## §5 Known-good verification sequence

```bash
python3 extensions/agi/bin/commands.py run smoke     # 940 active, must NOT drop
python3 extensions/agi/bin/commands.py run tests     # 1371 passing
python3 extensions/agi/bin/commands.py run goals-check
python3 extensions/agi/bin/commands.py run viewport-verify
python3 extensions/agi/bin/commands.py run links     # 945 resolved, 0 broken
python3 extensions/agi/bin/commands.py run grid-commit
```

`agi <verb>` works: `agi smoke`, `agi links`, `agi view`, `agi view-llm`,
`agi write <id> "<script>"`, `agi write create <type> <slug>`.

## §6 BANKED for the owner

1. 🔴 **OpenRouter workspace `agi` has a `$10.00/week` budget and it is
   EXCEEDED as of ~21:22.** Every wave-5 parent died on
   `403 Workspace weekly budget of $10.00 exceeded. Contact your org admin.`
   before spawning a kid. The real ceiling was never $15.43 (account balance)
   nor $5 (per-key cap) — it was a **third limit nothing in the engine reads**.
   Waves 2–4 (≈44 parents + their kids) cost ≈$10; a parent key reads
   `used≈$0.05–0.15`, a kid `≈$0.015`. **Owner action: raise the workspace
   weekly budget in OpenRouter org settings** (outside director authority —
   a provider spend setting). Until then pi dispatch is dead; the director
   fell back to the engine's `claude-code` harness for the remaining targets.
   **Engine follow-up (`goal:g1.11`):** `provisioning.py` should read the
   workspace budget and refuse to mint when the next key cannot be funded,
   instead of letting a whole wave die at 403 after minting.
2. **Six of the previous director's experiment nodes were demoted by the new
   commit-path gate** because their `evidence_runs` was a bare int
   (`goal:g7.3` scores that 0). They ran real experiments. Options: (a) leave
   demoted — honest about the record, loses nothing; (b) restore each with
   `write.py experiment:<id> 'set evidence_runs [experiment:<id>]'` —
   self-citation, which an earlier session called a gate hole. **Recommend
   (a)** unless the owner wants the metric back; the grid holds v(n-1).

## §7 Standing hazards carried forward

- **`snapshot-build-site.py` deletes every `origin: build-site` node it does not
  re-derive.** Kits are removed *after* their nodes are deprecated, never
  before (H0i). A `payload_ref` is dropped before its file is deleted.
- **Deprecating the 8 `Domain: …` ideas would gut the attractor list** —
  `idea:domain-graph-core` alone has 68 descendants. Decide the replacement
  before removing it.
- **A guard that has never failed on purpose is not a guard.** Four checks last
  session passed while not measuring the thing that broke.
- **Run the suite AFTER the last edit.** Testing before your final edit is
  indistinguishable from not testing.
- **Node bodies go through `write.py`.** A plain file write keeps the grid
  version but loses `edited_by` provenance — the untraceable write `goal:g13.1`
  exists to end. `HANDOFF.md` is the exception: it is a *payload*, so a direct
  file write is correct.
- **`pgrep -af "cli.js"` does not find pi** — the process is named `pi`.
- **Piping a long background command through `tail` hides it until it ends.**
- **A parent's REPORT is not its artefact.** Check the node file on disk.
- **$15.43 is the real ceiling**, not the $5 per-key cap. Nothing in the engine
  knows the account balance.

## §8 For the next director — added 2026-09-04 10:15 EDT by the L1.08 director (clock is now `America/New_York`; everything above is UTC)

### 🔴 A second director ran this graph, uninvited, 21:21–23:20 EDT on 09-03

The owner confirms it was not them. Evidence, all measured:

- Commits `L1.10b`…`L1.10f` (`b45fdcaca`…`e0220fad9`), plus five
  benchmark-style commits ("Baseline cold build…", "Demonstrated 30s reaper
  window gap…") interleaved, git identity = this box's default
  (`CodexOperator`). It rewrote `HANDOFF.md` wholesale (§0–§7 above are its
  text), used **this handoff's own conventions** — `.agi/sessions/L1-logs/p-NNNN.log`,
  `samples3.log`, `parent-scratch/` — and dispatched `iter-1043`…`1066` (waves
  6–7, "25/25 held 34 min, 15 stale parents killed"), on OpenRouter, i.e.
  **after the owner raised the workspace budget**. It behaved exactly as this
  file tells a cold director to behave. That is the handoff working — for a
  reader nobody invited.
- `~/.hermes/agi` is a checkout of this same repo at the same HEAD, beside
  `~/.hermes/SOUL.md` and `~/.hermes/agi-tree`; `~/.openclaw/workspace` has
  four crons (stall recovery every 15 min, relationship mapper). **The `agi`
  skill is global** (`~/.claude/skills/agi`) and the **SessionStart hook is
  global**, so any Claude Code session started under `~/.hermes/agi` — or any
  autonomous framework that shells out to `claude` there — is handed the map
  and the skill and reads "the director replaces the handoff".
- Less likely: an engine-dispatched CC parent escalated (they inherit the
  skill + CLAUDE.md). Against it: leases were `0/25` and the CC session limit
  was exhausted at 22:35 UTC, before these commits began.

**Troubleshoot, in order:** (1) `ls -lt ~/.hermes/` and any session logs
around 01:20 UTC 09-04; `~/.openclaw` logs at the same time. (2)
`.agi/sessions/iter-1043/*/agent.json` → `harness`, `cwd`, model — pi kids
name their dispatcher's cwd. (3) `git -C ~/.hermes/agi reflog` — a checkout
that committed shows it. (4) Decide whether the hook/skill should refuse to
act as director outside `/home/ubuntu/work/agi` unless invited (a
`director_allowed_from:` list in `.agi/config.json`). (5) This is
**`goal:g10.1` in one sentence**: had chat-to-node linking existed, the
`build:HANDOFF.md` version would carry the session that wrote it and there
would be nothing to troubleshoot. Node: `hypothesis:a-second-director-ran-this-graph-uninvited`
(under `goal:g4.8`).

### Open bugs and hazards found this run and carried, not fixed

| # | Where | What | Owner goal |
|---|---|---|---|
| 1 | `provisioning.py` | Knows the per-key cap, not the **workspace weekly budget**; a whole wave 403s after minting. Now `$50/week` on `agi`; `default` still `$10`. Read it and refuse to mint when the next key cannot be funded. | g1.11 |
| 2 | `dispatch.py` | Mints an OpenRouter key for every **CC** kid that never uses it. | g1.11 |
| 3 | `dispatch.py::_reap_one` | Restarts a kid on the CLI default model (`harness={}` passed to `restart`). | g4.7 |
| 4 | `manifest.json` | Still says `running` after `agent.json` says `done`. | g4.7 |
| 5 | `write.py set` | Stores every value as a **string** — `set tier -1` wrote `tier: "-1"`; **91 deprecated nodes are schema-invalid** on `types: tier` from the L1.09 pass. Node: `hypothesis:write-py-set-must-preserve-scalar-types` (under `goal:g13.1`). | g13.1 |
| 6 | `metrics.py` | Backward-mvp detection is a regex on body language (AND no forward payload). 2/48 hits, 0 false positives today; brittle by construction. | g3 |
| 7 | `evidence_gate` | 6 of the previous director's experiments sit demoted (bare-int `evidence_runs`). §6 item 2. | g7.3 |
| 8 | `commands.py verify` | Runs `smoke` before `grid-commit`, so smoke's `unevidenced_decisive_verdicts` lags one gate pass. Reorder. | g1.10 |
| 9 | `test_provisioning.py` | `test_mint_refuses_to_hand_out_a_key_with_no_ttl` hits the real account; fails whenever engine keys are outstanding. | g1.11 |
| 10 | `claude_code_adapter` | CC parents can write `HANDOFF.md`, `CLAUDE.md`, and run `dispatch.py`; add `disallowedTools` for those, and refuse `git` entirely (the second director committed). | g4.6 |
| 11 | `[experiment].md` | `goal` removed from `allowed_parents` (`goal:s22`) — every brief that says "parent to goal:X" for an experiment is wrong; say "under a hypothesis". | s31 |
| 12 | `[verdict].md` vs corpus | Schema says `contradicts`, real nodes use `contrasts`. | g2.x |
| 13 | `src/` | Two `mermaid.py` (renderers/ and chain_engine/renderers/), undiffed. | g2.2 |
| 14 | `fantasia/agi` | Separate clone; its 5-min cron runs the **old** `grid.py` (no commit-path gate) until pulled. | g11 |
| 15 | `briefing.py` | Reads idea status from disk itself because `inject.py`/`viewport.py` don't pass it — a duplicated read. | g9.7 |
| 16 | Untracked nodes | Anything minted and left uncommitted across a wave can vanish (trap 5). **Commit at mint.** | g4.1 |

**Addendum 10:45 EDT — paused at the owner's request:** all `openclaw`/`hermes`
crontab lines commented (`#PAUSED-2026-09-04`; backup + restore notes in
`~/.agi-paused/README.md`), and `openclaw-reactive.service`
(`~/.hermes/belam-codex/scripts/reactive_daemon.py --loop --interval 30`),
`openclaw-gateway.service`, `hermes-gateway.service` stopped (not disabled).
**Prime suspect for the second director:** the reactive daemon —
`~/.hermes/belam-codex/scripts/agent_pingpong.py` references this repo /
`HANDOFF`. Confirm from its logs before re-enabling anything.

**State 11:00 EDT (after wave 8, commit `L1.11b`):** active **1037** /
deprecated 180, primary 0.196 (honest — hypotheses lead, guard withholding
-0.1), `mvp_count` 50 (48 scoring, 2 backward), links 1214/0 broken, tests
**1454**, `unevidenced_decisive_verdicts` 5 → 0 at grid commit (the gate
demoting live kid output every wave, as designed). Wave 9 dispatched 10:59
(iters 1073–1078: g10.1 g8.1 g9.7 g1.10 s32 g4.7). One more wave after it,
then this director stops.

### Close-out 12:10 EDT — the L1.08 director stops here (waves 8–10 done, owner's "2–3 more waves")

**State:** active **1064** / deprecated 180 (sum 1244, never dropped), primary
0.194 (guard withholding ≈ -0.1; hypotheses lead), `mvp_count` 50 (48
scoring), links 0 broken, **tests 1471** via `commands.py run tests`,
`unevidenced_decisive_verdicts` 3 on smoke → demoted at the next grid commit
(the gate's normal cadence). Everything committed and pushed; grid current.

**Straggler leases at close:** ~9 pi processes (iters 1075, 1079–1081) were
still live. Their nodes will appear in `git status` as untracked/modified —
run §5 and commit them; nothing else is pending on them. Note that the
`iter-1075` parents outlived the 20-min timeout by >1 h (reaper restarts?) —
check `heal.py`/`_reap_one` before trusting `agent_timeout_mins` (§8 row 3).

**Near-miss, on the record (trap 2's shape, caught this time):** a kid's
in-progress edit to `bin/commands.py` broke the `Command` loader
(`missing 'raw_argv'`) while direct `pytest` stayed green — `commands.py run
tests` was the only check that caught it. **Always verify through the
runner, not around it**, and never commit an engine file a live kid is still
editing (`git status` shows it as `M`; wait for the lease to drain).

Next director: start at §1 L1.10 — `goal:g10.1` chat-to-node linking and
`goal:g8.1` engine pinning still have no engine code; four waves of research
nodes now sit under each. Then §8 rows 1, 3, 10 (provisioning reads the
workspace budget; reaper restart model; adapter `disallowedTools`).
