---
id: doc:lm-progress-2026-09-18
mint_id: 70faa1a9895f4fcca055eb4daf165bab
type: doc
parents:
  - goal:g5.7
next_edges: []
edited_by: belam
scaffold_hash: 43839ba7b1c66d06
season: 2
thought_session: dissolve-legacy-2026-09-19
title: "Progress report, thought-master seating 2026-09-18 06:54Z-17:3xZ, in the COMPLETE.md seven-section shape applied goal by goal: 5 director rounds landed (1 hypothesis closed disproved, 1 conjunct proved, Uno step 1+2 measured the Camber XS billing and VRAM ceilings, retry live), 1 hypothesis minted from a hand-judged literature slice, the too-big-model download queue extended; failures = the 10:22Z box OOM, Camber billing readable only by a human, rig state unverified, pufferlib undispatched"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# doc:lm-progress-2026-09-18
# Progress report — thought-master seating 2026-09-18 06:54Z → 17:3xZ (COMPLETE.md shape, applied mid-loop, goal by goal)

Ongoing report, not a loop close: no round outline was handed to this seating; the field was the card's NEXT list + the director's laps + owner lines in the pane. Everything below is grounded in a trunk commit or a node; a claim that is not says so. Trunk = `local-maxxing/season1/main`, batched into `season2/main` by the Prime at 14:07Z (`d04790db3`).

## 1. What ran
- One seating, one context window, claude-code/opus-5/max, meter 0.25 of the 0.47 line at write time. 72 trunk commits since 06:54Z (own + director + merged trunk traffic).
- Director rounds (pi harness, OpenRouter): TM.32 bend2 ARM4C half (cap 0.55 USD) · TM.33 schedule fix (0.30) · TM.34 Uno step 1 (1.00 + Camber) · TM.35 bend2 GPU half (1.00) · TM.36 Uno step 2 (1.00 + Camber) · TM.37 Uno retry (1.00 + Camber, LIVE since 17:04Z; used so far 0.19 USD). Research: one trove-survey run (staged-freeze slice), read stage only, ~0.01 USD.
- Camber Cloud (the g14 gate): job 27649 CPU-XSMALL 318 s = 5.3 CPU-min (owner read); job 27689 GPU-XSMALL 251 s = ~4.2 GPU-min; retry job pending inside a 20-min cap. Total OpenRouter account: 29.74 of 65.00 USD used, 35.26 remaining (credits endpoint, 17:29Z).
- One box-wide OOM/load storm at 10:22Z (15-min loadavg 271-372, swap near full; Prime stamp correction `90303ef3f`, earlyoom rail `46ace6fa9`) killed all six live town agents (3 parents + 3 kids). All three rounds were rescued from surviving worktrees by the director (`06ac7403a`, `0cae533d6`, `c5296c920`); nothing was re-run.

## 2. Scoreboard (start → now)
- Nodes: 3518 (predecessor card 06:5xZ) → 3528 files in the worktree (212 in `deprecated/`, 940 hypotheses, 1420 experiments); Prime batch count at 14:07Z 3311 active / 217 deprecated / 3528 total. 0 deletions in every landing (checked per merge).
- Links: 3497/0 broken (06:5xZ) → 3508/0 broken (14:1xZ).
- Suite: not run in this worktree (every landing was nodes/context only, no `extensions/` file changed); the Prime's batch verify 11/11.
- Primary metric `outcome_coverage`: 0.063 at seating (injection frame); not re-measured (no smoke run from this worktree) — unknown at end.

## 3. Per goal, how far it got
**goal:g14 (local-maxxing town — the smallest model that can do the job, everywhere)**
- Owner line 07:00Z ("are the too-big downloads queued? to be downloaded onto that box") banked verbatim + answered on `hypothesis:lm-uno-diffusion-draft-on-l4` (`3c715da9c`): the athena 31B pair (~51 GB) and Qwen3-8B bf16 (16.4 GB) were already queued too-big-raw; **Qwen3.8-27B bf16 55.6 GB + Qwen3.5-35B-A3B Q4_K_M ~20 GB added** behind the rig queue (slow mode, sha256, 20 % disk floor), ordered to the director, relayed to the Prime (banked `0554deffb`). Rig-side execution NOT yet verified (see §5).
- `hypothesis:lm-bend2-spiking-sim` — **CLOSED DISPROVED both halves**: ARM4C LIF 13.0x slower than OpenMP-C (TM.32, `eea005dd4`), GPU2070S CUDA LIF 37.8x slower, CUDA lane engaged but 0 % util (TM.35, `c102dc404`, note `b39616425`). LIF fixture + C baseline kept as the reference; spiking-sim continues in C/CUDA; PufferLib stays its own node.
- `hypothesis:lm-uno-diffusion-draft-on-l4` — step 1 ran (job 27649; billing unreadable by API key → owner read: per-minute, spin-up billed, monthly allowance not credits; `cb9b0375e`, `b08acfa94`); step 2 ran and **OOMed in the engine loader** at 21.69/22.03 GiB before Uno produced a token, driver died on arm 2 (`0699ad669`, `59659d46b`; lean_disproved:55, honest null rows); retry recipe approved + Prime GO 14:04Z (`dcb40fcba`); **TM.37 retry live**. Claim (>= 1.5x at batch 1, identical greedy text) still UNTESTED.
- `hypothesis:lm-athena-identity-seat-ab` — schedule-fix conjunct **PROVED** (TM.33: zoneinfo 02-06 America/New_York 1.5 MB/s else 0.5, measured pause/resume quiet line, 9/9 tests; `b6baafd13`); the A/B itself pending the 51 GB of bytes.
- `idea:lm-draft-refit-own-traffic` — owner question 06:48Z (staged encoder-freeze → decoder-only training) answered from a 10-digest literature slice (`eda2cff8e`), judged by hand (`add736e41`): no paper has the exact staged recipe; Medusa-1 / EAGLE-3 / DSpark / DeepSeek-V3.2-Exp warm-up carry the frozen-trunk half with numbers.
- `hypothesis:lm-eagle3-drafter-on-frozen-qwen3-4b` — **MINTED** (`add736e41`): a drafter trained on the town's own kid traffic against a frozen Qwen3-4B on the rig, 0 USD compute, measuring the catch-up curve (steps to 90 % of final acceptance) — the number the owner asked about. Queued off-box after spec-decode; needs the Qwen3-4B bytes first.
- `hypothesis:lm-pufferlib-oscillator-policy` (owner CRITICAL) — NOT dispatched: ordered 11:4xZ and again 17:0xZ; the director idled 14:07-17:04Z on a load-blip hold, then reached its rotation line without having read the node; rotating since 17:26:45Z; both halves are its successor's first action.
- Rounds gated + landed + reviewed by name: 5 (TM.32-36), 14 + 5 + 4 files, 0 deletions, 1 scrub commit (`0d5084d9a`: provider/hardware name → ARM4C alias).

**goal:g5.19 (the charter: Round 0, gentle cadence)**
- Round 0 table exists (`doc:lm-round0-table`, predecessor 06:xxZ). This seating turned two of its ESTIMATE rows into MEASUREMENTS: the XS instance bills **per minute**, **spin-up is billed**, the L4 exposes **22.03 GiB usable** (not 24), the allowance is **monthly hours** (40 CPU-h; ~50 GPU-h/month obtainable per the owner 11:5xZ, `aa6149e78`), readable only on the web. Cadence held: one paid research round at a time, every spend line through the Prime.
- (d) the looped-transformer chain: not advanced this seating.

**goal:g5.18 (town node/visions), goal:g5.20 (secrets hub — core town's)**: untouched.

## 4. Goals closed
0 goals closed. 1 hypothesis closed (bend2, disproved on evidence: 2 experiments, both with parent re-runs). No `complete` marks written; none found unsubstantiated in the touched nodes.

## 5. Completion-failure categories (everything that did not close)
- `ceiling-found-by-dying` — the 10:22Z box OOM killed all six town agents mid-round (rounds rescued, ~3 h of wall lost, TM.34's parent worktree deleted with no harvest dm — recovered only because its kid had a separate worktree; forwarded to the Prime/SM). Also Uno step 2: the 22 GiB VRAM ceiling was found by the loader dying, not by arithmetic (the checkpoint is 15.26 GiB; peak ≈ params + one shard). Also the director: reached its 0.47 context line before dispatching pufferlib.
- `banked-to-owner` — Camber billing granularity: no API surface exposes the bill, so step 2 waited ~2 h on a human web read (13:01Z); every further Camber job is a per-job owner/Prime line by rule. The Uno retry itself needed a second such line (given 14:04Z).
- `verification-blindness` — whether the rig's 27B fetch + supervisor download queue survived the storm is unknown (no post on the rig; TM.35 skipped the first-act report); the staged-freeze survey's critique/panel/judge stages never ran (critic OOM/timeout, SM.111/SM.112 pending) — the slice was judged by hand; `outcome_coverage` not re-measured.
- `hazard-carry-over` — pufferlib both halves (owner CRITICAL) carried through three director laps undispatched; the athena A/B has waited on 51 GB at 0.5 MB/s since 09-17.

## 6. Findings that are not failures
- The Camber XS numbers above (per-minute, spin-up billed, 22.03 GiB usable, monthly allowance). The XS L4's 22 GiB cannot hold Qwen3-8B bf16 with the Uno engine's current loader; the always-fits fallback (K2-Horizon-0.9B + adapter, 2.4 GiB) is now part of every Uno round.
- Bend 2.0.5's CUDA lane builds and runs on Turing but offloads nothing for a LIF workload (0 % util) — measured, not inferred; a plain C baseline at 16 threads is 1.264 s for the reference workload.
- The literature slice: nobody has trained a coupled-oscillator readout or an SNN C2C fuser against a frozen LLM trunk — an OPEN intersection (from an 8-paper scan).
- Harness: a director's "holding until the gate clears" is a turn that ends — a hold is an idle director until someone dms it (3 h lost); a hold line now gets an immediate "re-check and dispatch" reply. Recorded on the card; the SM added RECONCILE-AT-WAKE to the director brief.
- Wall time jumps while the box thrashes: this pane stalled 07:13-10:22Z; every stamp now comes from `date -u`.

## 7. Minted or changed (graph edges)
- MINTED: `hypothesis:lm-eagle3-drafter-on-frozen-qwen3-4b` ← parents `idea:lm-draft-refit-own-traffic`, `goal:g14`. `doc:lm-progress-2026-09-18` (this report) ← `goal:g14`.
- LANDED experiments (director rounds, parent-reviewed): `a00-81a331fa-da3c24` (TM.33 proved), `a00-8614c12a-b3c466` (TM.34), `a00-d54c0f0c-7fc31d` (TM.32), `a00-123b8762-b07e8b` (TM.35 disproved), `a00-cb88d326-21c0cc` (TM.36).
- NOTES (owner/Prime lines verbatim + verdict-by-name): `hypothesis:lm-uno-diffusion-draft-on-l4` (×5), `hypothesis:lm-bend2-spiking-sim` (×2), `hypothesis:lm-athena-identity-seat-ab`, `idea:lm-draft-refit-own-traffic`. `tests:` of the Uno node rewritten as the step-2 brief.
- CONTEXT: 10 literature digests under `troves/2026-09-18-owner-papers/`; `athena/fetch_parallel.py` + `test_fetch.py` (schedule + quiet line); `bend/` runbook + fixtures; `uno/` cmds, prompts, rows.
- ORDERS standing with the director: rig download queue (+27B bf16, +35B-A3B Q4), pufferlib both halves, Uno retry (live), eagle3 drafter after spec-decode, every kid its own worktree.

<!-- BODY:END -->
