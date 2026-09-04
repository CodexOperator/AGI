# SESSION HANDOFF — 2026-09-03: loop L1 RESUMED at 08 — LIVE SCRATCHPAD

Standing bootstrap lives in [QUICKSTART.md](QUICKSTART.md). This file is one
session only and the next director replaces it wholesale. The previous
session's section is in the grid: `grid.py payload build:HANDOFF.md --version N`.

**Loop `L1` continues.** `L1.01`…`L1.07` landed in the prior session; this
session resumes at `L1.08`. Global `iter-NNN` ended at 116.

## §0 State block

| | baseline this session | now |
|---|---|---|
| active nodes | 940 | **982** (after wave 1–2) |
| deprecated | 8 | 9 |
| `outcome_coverage` (primary) | 0.271 | **0.224** ⬇ honest: +42 nodes, no chain closed |
| `evidence_fraction` | 0.317 | 0.320 |
| `mvp_count` | 39 | 39 |
| `broken_links` | 0 (1 retired payload, not damage) | 0 |
| tests | 1371 passing | **1381** |
| `unevidenced_decisive_verdicts` | 6 | **7** ⚠ one slipped in wave 1–2 |
| goals active / cap | 13 / 15 | 13 / 15 |
| budget peak | 0/25 live | **25/25, pi=25, held 20:06–20:15** |
| unpushed | 0 | 0 (pushed after wave 2) |

**Wave 3 dispatched 20:37** — iters `1012`–`1019`, targets g4.8, s18, g7,
g9.7, g1.10, g13.1, g4.7, g5, two parent slots each. Sampler ends ~21:04;
restart it if wave 4 runs past.

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
- [ ] **L1.10** — chat-to-node linking (`goal:g10.1`, `goal:g2.7`),
      engine-commit pinning (`goal:g8.1`), loop-scoped iteration numbering.
      **In flight via engine CC parents:** `iter-1039` (loop-scoped ids,
      `hypothesis:loop-scoped-iteration-ids-cannot-clobber` under g7),
      `iter-1041` (g10.1). `iter-1040` = attractor-filter follow-up
      (`hypothesis:attractor-list-must-hide-deprecated-ideas` under g9.7).
      g8.1 dispatch waits for 1039 to drain (subscription rate limit).

## §2 Concurrency discipline this session

Several parents run at once. The rule that keeps it safe:

**Parents never touch git.** No `commit`, `push`, `add`, `checkout`, `stash`,
and no `grid.py`. The director commits, serially, between waves. Parents own
**disjoint file domains** and report anything they needed outside their own.
Kids see each other's untracked files — report, never clean.

## §3 🔴 Where it stands, and the next command

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
7. **`iter-NNN` did not end at 116** — `ls .agi/sessions` shows `iter-1005`;
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
