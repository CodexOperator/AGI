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
- [ ] **L1.08** — the removal guard (`goal:g3` symmetry: removal cannot move
      scoring either). **In flight, PARENT-A.** Gates L1.09.
- [ ] **L1.08b** — live scale: parent-spawns-kid, cap 8→16→25, `goal:g4.8`
      clauses 2 & 3. **In flight, PARENT-D.**
- [ ] **L1.09** — the wide run: cavekit exit + legacy sweep. Survey in flight
      (PARENT-C); execution waits on the guard.
- [ ] **L1.10** — chat-to-node linking (`goal:g10.1`, `goal:g2.7`),
      engine-commit pinning (`goal:g8.1`), loop-scoped iteration numbering.
      Design recon in flight (PARENT-E).

## §2 Concurrency discipline this session

Several parents run at once. The rule that keeps it safe:

**Parents never touch git.** No `commit`, `push`, `add`, `checkout`, `stash`,
and no `grid.py`. The director commits, serially, between waves. Parents own
**disjoint file domains** and report anything they needed outside their own.
Kids see each other's untracked files — report, never clean.

## §3 🔴 Where it stands, and the next command

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

Next: when leases drain, `smoke` (count must not drop), `links`, check
`unevidenced_decisive_verdicts`, commit nodes, `grid-commit`, push, redispatch
`goal:g4.8`.

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
5. **`iter-NNN` did not end at 116** — `ls .agi/sessions` shows `iter-1005`;
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

_(empty — nothing yet needs a decision the grant does not already cover)_

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
