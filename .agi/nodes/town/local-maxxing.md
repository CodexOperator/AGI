---
id: town:local-maxxing
mint_id: c1cbfc52f6924643979555fee0f0386d
type: town
parents:
  - vision:the-living-being
  - ladder:ladder
  - goal:g26.towns
next_edges: []
council: council-local-maxxing
edited_by: thought-master
location: local-town
master: thought-master
scaffold_hash: 3876620b4bc4f88e
season: 1
thought_session: belam-S2-L5-I
town: core
trajectory_standin:
  - "formation: thought-master (MAIN = trunk local-maxxing/season2/main) -> director-thought (Sonnet; research rounds; the ONLY active director on town work) · director-engine OFF g7.33 by owner order 09-23 (Prime-assigned g15 residues only) -> pi parents/kids (OpenRouter) + pi-local (the resident 9B, 0 USD)"
  - "priority (owner 09:4xZ-09:5xZ 09-23, verbatim on goal:g5): [1] the OSCILLATOR HEAD-PRUNING chain (goal:g5.22), director-thought full force until the jev code fixes land · [2] the switch mvp (goal:g5.27) round 1 after the Prime's pass 2 · [3] the jev MAGIC PANE (goal:g5.24) resumes when the jev code fix lands = director-engine's choice surface (EF.21, goal:g1.25; it signals '[jev] choice surface ready' + SHA to director-thought) -- the TypeSafe keys are LIVE since 10:2xZ (owner: TYPESAFE_KEY + TYPESAFE_KEY2, 5 USD each, both HTTP 200, forwarded to kids by pi and pi-local); local kids still wait on the harness fix · off-the-shelf combinations (g5.23 · g5.25 · g5.30) as capacity allows"
  - "metrics: HEAD + KV (09-23, the sparks): OSC.01 coherence ranks damage no better than random (lift 1.00002), but a plain activation score ranks it at Spearman 0.40 · OSC.02 one KV group of the served 9B costs, by depth, L3 3.0 · L7 3.5 · L11 4.8 · L15 5.2 · L19 7.0 · L23 6.5 · L27 7.2 · L31 13.8 pct NLL (mean; within L3 0.8 to 8.2) = a per-group SENSITIVITY MAP · OSC.03 every head has a stable, self-identifying RoPE band fingerprint (336/336 stable, 331/336 self-identifying; low band 171, high band 37) · OSC.04 band-energy masks beat random 4.5-6x, smooth curve: 99.9 pct energy drops 11 pct of q pairs at agreement 0.93 / KL 0.034 · OSC.05 (running, first numbers) q4_0 KV = 2.39x context (49,664 -> 118,784 tokens) at +0.07 pct NLL, q8_0 1.52x at -0.03 pct, decode ~35 pct slower at 16k depth · reference deepseek-v4.1-flash 93.9 pct HumanEval / 0.869 IFEval strict (N=10 re-score 0.8701) · C2 = B + LoRA (armC2_bonsai27b-abliterate-s2) ACCEPTED at the 09-23 gate: IFEval N=10 mean 0.8002, CI [0.7992, 0.8012] > bar 0.7819 on every seed + HumanEval 143/164 = 92.9 pct of ref (single run) -> within 10 pct on every battery row that exists (the typed-round row does not exist yet) -> TRIGGERS the SWITCH mvp (g5.27), never a switch by itself · B = Bonsai 2 27B PTQ1_0 (7.27 GB, 20.5-23 tok/s): HumanEval 92.2 pct FIRES, IFEval N=10 mean 0.7773, CI [0.7763, 0.7782] -> does NOT fire · Qwen3.5-9B Q4 (6.0 GB, 62.7 tok/s): HumanEval 78.0/79.3 pct -> NOT met · IFEval noise = letter_frequency's stdlib random + langdetect, both seeded"
  - "landed since 09-20: ABC.01/02 · ABL.01 (cvector dead on Qwen3.5) · SWR.01 (reference bar) · MP.01 (corpus 63/200 real forms) · TEL.01-03 (KV shift unavailable on IMROPE; only Bonsai-1.7B can shift) · SWR.02-B + B.03 · engine EF.01-09 (grid cron LIVE into refs/grid/local-maxxing/) · 09-23 batch B: SWR-C2.02 + SWR-RS.01 (C2 fires both rows) + agent-prompt.md Rules item 13 (paths live in config; owner 08:4xZ) + TMM.39/40 corrections"
  - "live 11:4xZ 09-23: batch C (CFG.01 + CFG.02 + OSC.01) REVIEWED by name, accept_with_residue -> returned to director-thought to close 3 small residues, lands after the Prime's pass 2 · OSC.02 (served-9B KV-group ablation by measured delta-loss) -- its GPU phase done, the router back on :8080 · rr-mp02-g01 (propose-only) · director-engine: EF.21 = goal:g1.25 CLI GRAMMAR (the jev choice surface) + more rounds · pool: account floor -50 on the trunk (owner 10:3xZ, 'so headroom never blocks a round'; supersedes the 10:1xZ restore) · per-spawn key TTL 300 min"
  - "queue: [1] LAYERING LADDER (goal:g5.22; owner 13:xZ: every nudge counts, stack them): L1 KV format -- OSC.05's q4_0 (2.39x at +0.07 pct) is a KEEPER whatever its bar says; try the off-the-shelf K/V split (-ctk q8_0 -ctv q4_0); propose the winner to the Prime for the router · L2 per-group KV precision from OSC.02's sensitivity map (early attention blocks lower precision, the last block highest) -- measure in Python first, llama.cpp per-layer KV types would be custom · L3 band energy as a PRECISION allocator instead of zeroing (OSC.04's ranking; 4-bit, not zero, for low-energy pairs) · L4 GEOMETRY: a rotary pair's wavelength 2pi/theta = a head's attention horizon -> local (high-band) heads keep only a recent KV window, retrieval (low-band) heads keep all (streaming vs retrieval heads, no training); distance-aware masks (a fast pair aliases beyond a few wavelengths: mask it only for far keys) · L5 band maps ACROSS QUANTIZATION (0.5B at f32/bf16/q8/q4 -> a full-RoPE 3-8B at q8 vs q4 -> the served 9B's 8 attention blocks at q4) and ACROSS MODELS (C2 vs B through a llama.cpp tensor dump; Fast-dLLM v2 1.5B vs its parent Qwen2.5-1.5B -- does diffusion training move positional geometry?) · L6 KERNELS (owner 13:xZ: kernels, hardware and instructions are off-the-shelf blocks too; 0.001 pct nudges stack): a serving flag/build sweep on the served 9B, then C2 -- flash-attn, MMQ vs cuBLAS, micro-batch -ub, CUDA graphs, KV types, threads, mmap/mlock -- NLL held, tok/s with repeats and a CI so a 0.1 pct gain is real, every gain kept and stacked (L1 + L6 run as ONE serving sweep) · L7 MEMORY TIERS: a traffic map (bytes per token per tier) + what horizon-aware KV placement would move, off-the-shelf placement first (llama.cpp -ot tensor overrides, --no-kv-offload); C2 first -- its weights nearly fill the card · L8 WATCHDOG: v1 = JEV-POWERED (owner 13:xZ: TypeSafe jev-latest in its multiple-choice format, keys live): each placement decision -- which heads / KV blocks stay in VRAM, go to RAM or come back for the next window -- posed as ONE typed multiple choice built from the main model's attention traces; an API call is too slow per token, so v1 decides per window, capped per round; its choices also label the traces to distill v2 = a small local CPU side model that prefetches a layer ahead; both scored against recency and the static horizon map at a fixed VRAM budget · L9 LATTICE: side models on the data stream doing input->output replacement -- off-the-shelf first rungs: the released C2C fuser (hypothesis:lm-c2c-kv-bridge-released-fusers) and a CPU draft model for speculative decoding (llama.cpp -md, draft on the CPU) · L10 CLOSED LOOPS (owner 13:xZ: closed loops over predictions -- each side formats and sends the next batch while it waits on the other): first MEASURE the loop -- an nsys timeline of one serving request (CPU threads, CUDA kernels, H2D/D2H copies, the idle gaps on each side) = the open-loop map; then close it with off-the-shelf overlap: speculative decoding with a CPU draft (the CPU drafts the next tokens while the GPU verifies), continuous-batching slots, pinned host buffers, CUDA graphs, async copy streams, and the CUDA wait mode (a spinning CPU thread = an open lane with the lowest latency; a blocking sync frees the core for other work) · L11 CPU LANES (the CPU as a remote GPU): the topology is 2 CCX x 4 cores x 2 SMT (CCX0 = cpus 0-3,8-11 and CCX1 = 4-7,12-15, 16 MB L3 each); llama.cpp's threadpool knobs are the off-the-shelf lanes -- --cpu-mask / --cpu-range / --cpu-strict per CCX, --poll (busy-polling lanes ready the moment work lands), --prio, -t / -tb; e.g. CCX0 = the main model's CPU side, CCX1 = the watchdog or draft; measured with perf (via sudo) · L12 EVERY TRANSISTOR: an inventory of the idle compute on the board (GPU async copy engines, tensor cores, AVX2 / FMA, the two L3s, RAM channels, DMA engines) and the levers that reach each, user-level first · [2] switch mvp round 1 (serve C2 + HumanEval on the served build) after pass 2 and behind any head-pruning chunk that loads a model; round 2 after its slot + the Prime's pi-provider go · [3] CFG.01 + CFG.02 merge-up · [4] magic pane MP.02 (T.01/S.01 on director-engine's manifest; jev arm on TYPESAFE_KEY) when the jev fixes land · FT.00 re-planned on C2 after the switch"
  - "engine g15 (director-engine, Prime-assigned): 0921 chunk 1 = R1 EF.12 + R2 EF.11 PROVED, mur 0 demote, 476 passed -- HELD at the trunk gate: it carries pre-hold g7.33 EF.10 (rotate.py +122, no mur) -> the Prime/core decide · chunk 2 = 14 engine residue dispositions · 0923 R1 EF.13 PROVED (anonymize loopback) · R4 EF.14 + R5 EF.15 running · R7 banked to the Prime · the 0921 batch's 13 lm-* rounds: 12 accepted with residue, lm-pi-local-9b-kid demoted (TMM.39)"
  - "rig (measured 13:xZ 09-23): AMD Ryzen 7 3700X (Zen 2, 8c/16t, AVX2 + FMA + F16C, NO AVX-512, L3 32 MB) · RTX 2070 SUPER 8 GB (Turing sm_75: fp16 tensor cores, no bf16; 448 GB/s VRAM) on PCIe gen3 x16 (~16 GB/s theoretical, ~28x below VRAM) · 15 GB RAM · 2 CCX x 4 cores x 2 SMT (CCX0 cpus 0-3,8-11; CCX1 4-7,12-15) · governor schedutil, hugepages 0, THP madvise · nsys + ncu + perf present, sudo works · storage = USB-attached SSDs (a cold tier, speed unmeasured) -> a VRAM<->RAM swap pays only when predicted early enough to hide the transfer; storage is for parked state, not per-token traffic"
  - "windows: the Prime's pass-2 mur 11:41Z 09-23 claims ~3 GB + 2 cores (5 h notice) -> no pi-local round live across it · GPU = one research round at a time · memory_max 6G, ONE model-loading host kid · no multi-kid round under a pi-local parent (its 49,664-token slot overflowed at 39 min, G.01)"
  - "open: (2) kids do not inherit --harness pi-local -> no local-inference kids yet (routed) (3) resumed seats export no AGI_ACTOR (routed) (4) director-engine's chunk-1 merge-up held on pre-hold g7.33 work (the Prime) (5) dispatch has no wall knob: agent_timeout_mins is defeated for single-parent rounds (SM.23b) (6) a positional send lands in a raw inbox a worktree post's read never shows (7) machine paths stale on this box -> hypothesis:harness-bin-paths-resolve-per-box (director-engine; PI_BIN covers pi meanwhile) (8) cli.py done's scoped commit drops .agi/config.json (9) 3 pre-existing suite failures on the trunk (10) anonymize refuses 127.0.0.1 until director-engine's EF.13 lands · CLOSED 10:1xZ-10:2xZ: key TTL (-> 300 min) · the floor bypass (-> 1.6) · the TypeSafe keys (owner: two 5 USD lanes, live)"
  - "rules (town, standing; BOX TUNABLES (owner 13:xZ 'we aren't hacking anyone but ourselves'; sudo works here): a round may flip a REVERSIBLE box tunable (CPU governor, THP / hugepages within a RAM budget, IRQ affinity) ONLY inside its own window -- before-value recorded, restored whatever happens, named in its merge-up; reboot-level changes (isolcpus / nohz_full boot params) and firmware / BIOS / clocks / voltages = the owner's go only, never an agent's; RELENTLESS OPTIMISM, owner 13:xZ: every round reports its LARGEST SAFE STEP and it joins the layered stack; a missed bar never ends a chain while any positive step exists; moved off the master card 09:3xZ 09-23 per the owner's master template): cap 1 USD per round · ONE research round per GPU · memory_max 6G, ONE model-loading host kid · abliterated-in-prod · SWITCH = within 10 pct of the reference on every existing battery row -> mvp -> build (goal:g5.27) · PACE slow, small chunks · batch-max (one merge-up per batch; board rows travel in it) · diagram-max (goal:g5.31) · director-thought SELF-LOOPS on this trajectory (independent research in its priority order: plan, mint, dispatch, review by name, close residues in-loop) and both directors message thought-master ONLY for a blocker or a fully completed merge-up (owner 09:5xZ, superseding 08:3xZ's ask-first) · no multi-kid round under a pi-local parent (the 9B's 49,664-token slot) · paid rounds carry a 120-min ORDERS wall (the key TTL is 300 now; the wall stays until dispatch grows a real wall knob, SM.23b) · the account floor is -50 on the trunk (owner 10:3xZ, supersedes the 1.6 restore) · IFEval: seed both RNGs, N=10 CI rule (TMM.32) · this field = the live board, written whole by the town master, one version per write (the grid cron records it)"
visions:
  - vision:local-maxxing
  - vision:local-maxxing-smarter
  - vision:local-maxxing-together
---
<!-- BODY:BEGIN -->
# town:local-maxxing

## town = ops · trajectory = KG (stand-in TEMPORARY)

```
town:local-maxxing ──▶ OPS home (who / research bundle / what's left / location)
                         location: local-town
trajectory:local-maxxing (soon) ──▶ KG coordination
                         (metrics / mini-vision progress / links→chain nodes)
.geometry/towns/local-maxxing ──▶ Pass-1 raw self (see goal:g7.34.3+)
```

**TRAJECTORY STAND-IN section below is TEMPORARY** pending `trajectory:*`
type (`goal:g7.34.1` / `.2` on town:core). Until mint+migrate, this town
body carries the stand-in. Metrics/links tables move to the trajectory node;
ops bundle stays on town.

## COORDINATION POINTER (core protocol)

`town:core` uses GRAPH-ONLY board protocol (`doc:standing-llm-ops` §3 + `.geometry/towns/core.md`).
This town (`local-maxxing`) stays **research**; follow the same graph-board rule if/when claiming core-adjacent engine work — do not message Belam for routine batches.

## GOAL BUNDLE

LOCATION ──▶ local-town

```
town:local-maxxing
├─ GOAL BUNDLE (diagram-max) — RESEARCH only
│  ├─ g5.22–.31 … research tracks (was g14.6–.16; nested .N kept)
│  ├─ g5.17–.21 … remapped from legacy g14.1–.5 / g14.3 lineage
│  ├─ goal:g1.25 …… CLI GRAMMAR (G1 umbrella: the jev choice surface; owner 09-23)
│  └─ town:local-maxxing tagged goals (same set ∩)
│  └─ goal:g7.33 …… MOVED → town:core (engine; parked unassigned)
└─ TRAJECTORY STAND-IN ← folded from doc:lm-town-trajectory
   (TEMP pending trajectory:* — g7.34.1/.2; doc kept, deprecated pointer)
```

### Goal ids (bundle)

| id | role |
|---|---|
| goal:g5 | umbrella: the town's goal -- owner lines land here (replaces the retired g14, owner 09-23 09:0xZ) |
| goal:g5.22 | TRACK I inference |
| goal:g5.23 | TRACK II fine-tune |
| goal:g5.24 | TRACK III jev + magic pane |
| goal:g5.24.3 | MAGIC PANE detector |
| goal:g1.25 | CLI GRAMMAR = the jev choice surface, across umbrellas (G1 config-maxxing; director-engine; owner go 09-23 10:0xZ; the node reaches the trunk with director-engine's merge-up) |
| goal:g5.25 | abliteration |
| goal:g5.25.1 | own refusal lever |
| goal:g5.26 | research corpus |
| goal:g5.27 | the switch / battery |
| goal:g5.27.1 | battery + reference |
| goal:g5.28 | side track spiking |
| goal:g5.29 | research treasury |
| goal:g7.33 | **MOVED → town:core** (engine fixes; parked unassigned) |
| goal:g5.30 | KV-cache telepathy |
| goal:g5.31 | diagram-max + batch-max |
| goal:g5.17 | Sensei assigns fine-tune / local-maxxing (remap) |
| goal:g5.18 | local-maxxing TOWN (remap) |
| goal:g5.19 | Thought Master post (remap) |
| goal:g5.20 | secrets hub banked (remap) |
| goal:g5.21 | Bend2/HVM map (remap) |

Town schema parents = ladder only → **linking is Agent Notes / this body**, not `parents:` to goals.

### Trajectory stand-in — LIVE rows = the `trajectory_standin` field (owner 2026-09-23: written whole by thought-master, the town master, one version per write; `write.py town:local-maxxing 'set trajectory_standin [...]'`). The rows below are the 09-21 fold of `doc:lm-town-trajectory`, frozen; both migrate into `trajectory:local-maxxing` at G7.34.2.

**What it is (owner 01:3xZ 09-21, verbatim on goal:g14):** a super node to the side that links into all relevant nodes — bigger than a single subgoal, sometimes bigger than a perpetual, smaller than a vision. Metrics chased for this track: layer techniques so bigger models run on smaller footprints with longer context windows. **How it changes:** metric change = new node version (overwrite body; reason in THOUGHT); A/B = branch worktree. Proper `trajectory` type queued (`goal:g7.34.1` schema + `goal:g7.34.2` mint; previously noted as G7.33.5); until it lands **this town section IS the stand-in**. `doc:lm-town-trajectory` remains as pointer — do not delete yet.

#### Metrics chased (newest first)

| date | model (params) | footprint | ctx line | tok/s | quality (battery) | how | node |
|---|---|---|---|---|---|---|---|
| target | bigger | smaller | longer | usable | within 10 pct of deepseek-v4.1-flash on HumanEval + IFEval — reference MEASURED 09-21: 93.9 pct HumanEval (154/164) · 0.869 IFEval strict (470/541) | layered: dead-head prune → context/throughput → fine-tune → QAT → telepathy | goal:g5.27; experiment:a00-559ee702-d3c7dd |
| 09-20/21 | Bonsai 2 27B PTQ1_0 (27.36B, 1.75 bpw) | 7,268 MiB VRAM (8 GB rig) | 64K, 1 stream | 23.0 empty / 18.9 at 16.8K | HumanEval 86.6 pct = 92.2 pct of reference (FIRES 0.9x; C2 +LoRA 92.9); IFEval — (SWR.02) | ternary PTQ (shipped) | experiment:a00-bb10233d-5a7f1f · a00-559ee702-d3c7dd |
| 09-20 | Qwen3.5-9B Q4_K_M (9B) | 6,010 MiB | 64K | 62.68 (2.87 J/tok) | HumanEval 78.0 / 79.3 pct (A / A2) | Q4 (shipped) | experiment:a00-c4441397-c8a8c6 |

#### Links

goal:g14 · goal:g5.22 · goal:g5.23 · goal:g5.24 · goal:g5.25 · goal:g5.26 · goal:g5.27 · goal:g5.28 · goal:g5.29 · goal:g5.30 · goal:g5.31 · doc:lm-round0-table · doc:lm-local-town-box-facts · doc:lm-research-corpus-registry · doc:recurrent-looped-transformer · idea:lm-nodes-as-kv-caches · hypothesis:lm-kv-slot-save-beats-reprefill · hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box · hypothesis:lm-own-refusal-direction-on-qwen35-9b-cuts-refusals-at-no-coding-cost · hypothesis:lm-hidden-state-mean-direction-cuts-refusals-on-qwen35-9b · hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery · hypothesis:lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens · hypothesis:lm-dead-head-kc-threshold-is-not-a-critical-point · hypothesis:lm-morals-and-sanctuary-corpus-assembles-to-a-clean-sft-set · **doc:lm-town-trajectory** (pointer; folded here) · ~~goal:g7.33~~ → town:core · **goal:g7.34*** (parked geometry/trajectory spine on town:core)

#### Board (formation · live · queue — replace in place)

```
formation  thought-master (Opus, MAIN=trunk; IDLE between merge-ups) -> director-thought (Sonnet, research) + director-engine (Sonnet; G5.31.1-2 research/process — engine g7.33 now on town:core parked) -> pi parents/kids
rules      diagram-max (goal:g5.31) · batch-max · board/trajectory = VERSIONS (replace body), never notes
memory     15 GB box · memory_max 6G · ONE model-loading host kid · GPU = one research round at a time
live       see doc:lm-town-trajectory board for tip ids (folded snapshot 2026-09-21)
research   MP.01 -> TEL.01 -> SWR.02 -> FT.00 -> … (tracks on g5.22–.29, .30–.31)
engine     goal:g7.33 (+ G7.33.*) → MOVED town:core (parked unassigned)
geometry   goal:g7.34* → town:core parked (trajectory type + .geometry/towns)
comms      magic pane (G5.24 / g7.32 messaging on core) = future unified messaging layer
```

## Agent Notes

- Owner ask 2026-09-21: fold trajectory stand-in into town body; keep `doc:lm-town-trajectory` until trajectory type ships.
- Owner ask 2026-09-21: engine goal:g7.33 ownership → town:core (parked unassigned); research tracks stay here.
- Belam 2026-09-21: stand-in TEMP; town=ops / trajectory=KG; spine work = goal:g7.34* on town:core.
- Actor Belam; master cell = thought-master.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Belam 2026-09-21: clarify town=ops vs trajectory=KG; TRAJECTORY STAND-IN temporary pending g7.34.1/.2; keep research bundle + metrics diagrams
<!-- THOUGHT:END -->
