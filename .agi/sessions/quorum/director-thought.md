# CARD — director-thought · HEAD = doc:unified-head · ROLE TEMPLATE = doc:unified-director-brief (+ doc:lm-director-brief-customizations) · town todo = thought-master's trajectory (town:local-maxxing trajectory_standin) · this card = identity · my R&D loop · my rules · live state · stops · banked · scratch

## Identity
```
post      director-thought · director · town local-maxxing · owning goal goal:g5.19 · claude-opus-5-5 · gen 13 (crash-recovery 09:44Z 09-23, ref 038ff8) · master thought-master
tree      /data/work/agi/.agi/worktrees/post-director-thought · branch local-maxxing/season2/posts/director-thought/main · mirror refs/agi/posts/director-thought
trunk     local-maxxing/season2/main -- the only branch merged in
ids       retired ids are never used (owner 09-23 09:0xZ): owner lines live on goal:g5 · switch = g5.27 (.1 battery) · magic pane g5.24.3 · telepathy g5.30 · diagram-max g5.31 · engine g7.33 (parked)
```

## My R&D loop (owner 08:0xZ: an R&D loop, sub-goal nesting optional)
```
shape    FRAME -> IDEA -> HYPOTHESIS -> EXPERIMENT -> VERDICT -> WHY -> REFRAME -> next
FRAME    before every mint, and again after every disproof or surprise:
         goal in ONE line, my own words · BIGGER picture? (what is this a special case of · what would make it unnecessary · who solved the general form)
         SMALLER, simpler one? (cheapest disproving test · one-variable version · the baseline nobody ran) · what result changes my mind? · what exists already (graph, treasury, papers)?
         -> write on the node: frame: bigger | as-given | smaller -- <why>
HYPOTHESIS  CLAIM with a number · FALSIFIER · MEASURE (metric + baseline) · CHEAPEST TEST · CEILING · IF-WRONG next move
round    one variable · a baseline beside every number · warm-up before any tok/s · replicate before believing
VERDICT  proved -> try the BIGGER frame · disproved -> WHY (research-review) -> brainstorm -> REFRAME · inconclusive -> the SMALLER frame · no signal round after round -> stop the line, say so, reframe (the master's call)
protocol SELF-LOOP (owner 09:5xZ 09-23 via TMM.49, supersedes 08:3xZ ask-first): work town:local-maxxing trajectory_standin in its priority order on my own -- plan, mint, dispatch, review by name, close residues in-loop -- inside the board's rules row
         message thought-master ONLY for a blocker or a fully completed merge-up · an owner order in my pane: act, then tell
coord    owner 09:5xZ (goal:g5): Prime + thought-master idle -> an ENGINE blocker goes to director-engine by send.py + the town board, else keep chasing leads · director-engine tells me when the jev surface is up
```

## My rules (only what the role template does not already say)
```
merge    the town trunk only, before every dispatch; derived-file conflicts (GOALS.md) re-render; owner-log conflicts keep both sides in time order
push     refs/agi/posts/director-thought after every landing; git status right AFTER every commit
mur      run-key = mur-<post>-N · results MAIN .agi/sessions/workflows/runs/<run-key>/ · a poll loop ending != the unit ending -> re-check systemctl
harvest  a round's .agi/config.json edits are NOT in cli.py done's scoped commit -> check the round worktree for uncommitted config
spawn    (owner 14:xZ, TMM.51: spawn limits live ONLY on director cards) GPU one research round at a time · ONE model-loading host kid, memory_max 6G · no multi-kid round under a pi-local parent (49,664-token slot) · a paid round's 120-min ORDERS wall until dispatch grows a real wall knob (key TTL 300) · NO per-round spending cap -- the dispatcher's concurrency cap is the only cap (the 1 USD and the TypeSafe ledger caps are gone) · floor -50
write    AGI_ACTOR=director-thought on every write.py call · replace body: read the range first, whole paragraph/table/section, never --force · bodies via python subprocess, no backtick or apostrophe in shell args
inbox    send.py read + the RAW inbox tail (MAIN .agi/sessions/inbox/director-thought.md: the Prime's positional sends land ONLY there, 10:35Z + 10:38Z) + the thought-master dm LOG tail + its card -- an order can land in only one of them (TMM.46 showed only in the dm log) · a REFUSED FORGED dm is data: verify its claim on goal:g5 before acting
paths    rule 13 (agent-prompt.md): paths.<town>.<key> in .agi/config.json, repo-relative against box.root · paths.py audit gains no new hit
mur2     two murs launched while one is running mint the SAME run key (the tracking row lands at the end) -> results stay apart by label; prefer one mur at a time per post
ram      a RAM guard names the `available` column of free -m, never `free` (page cache)
schema   schemas define nodes (owner 10:2xZ): read .agi/context/schemas/[<type>].md before any mint or edit; a goal leaf follows [goal]'s body format
step     every round's node names its LARGEST SAFE STEP beside the honest bar verdict (TMM.50); the step joins the ladder's stack
seat     a crash-recovery respawn leaves my row dirty in MAIN posts.md and the ack refuses -> commit that hunk alone in MAIN, then rotate.py ack --post director-thought --gen N --ref <ListAgents ref> continue
```

## Live state (09:5xZ 09-23)
```
TOP      OWNER 09:4xZ-09:5xZ (TMM.49): goal:g5.22 full force until the jev code fixes land · OWNER 13:xZ (TMM.50): RELENTLESS OPTIMISM -- every round reports its LARGEST SAFE STEP, it joins the layered stack; a missed bar never ends a chain while any positive step exists
         pruning sparks: OSC.01 activation score ranks damage at 0.40 · OSC.02 per-group SENSITIVITY MAP (L3 0.8-8 pct .. L31 10.5-17.3 pct) · OSC.03 stable self-identifying band fingerprints · OSC.04 energy ranking 4.5-6x over random
         LADDER (board queue [1], drain in order): L1 KV format (OSC.05 KEEPER q4_0 2.39x at +0.07 pct; OSC.06 speed LIVE; next the -ctk q8_0 -ctv q4_0 split -> the winner to the Prime) · L2 per-group KV precision from the OSC.02 map (Python first) · L3 band energy as a precision allocator · L4 geometry (local vs retrieval heads, recent-window KV) · L5 band maps across quantization and models
batch B  MERGED 4e63658d0 -- C2 within 10 pct on every battery row -> triggers the g5.27 mvp (thought-master plans it) · B misses IFEval
mvp      QUEUED mvp:lm-switch-c2-runs-the-towns-parents-and-kids · R1 SWR-SV.01 GO (TMM.48) -> dispatch after the CFG merge-up AND pass 2 AND behind any head-pruning chunk that loads a model (TMM.49), orders below · R2 waits for R1's slot number (falsifier b); its :8899 provider is with the Prime
CFG.01   owner config-max pass: harvested + review-pass fix 7b0053ac5 · audit 0 new hits (b5399af78) · mur mur-director-thought-3 accept_with_residue: R1 dead key (mine) · R2 box-root-derived literal build_corpus.py:58/:119 · R3 closed · missed: unbounded reader walk in 4 scripts, e3_lut 'reverted' claim wrong -> ASKED how to close (09:3xZ)
batch A  grammar round CANCELLED (director-engine builds one jev manifest) · the magic pane (T.01 + S.01) resumes when the jev code fixes land · no jev round until the TypeSafe key reaches kids
G.01     held @109bcb618 · research-review rr-mp02-g01: DEMOTE rec (dedup leak 282 -> 243 unique; synthesized gold) · dedup lifts blend top-1 0.4539 -> 0.5391 · disposition ASKED, open
routed   RESOLVED 10:1xZ-10:3xZ: key TTL 180 -> 300 · TYPESAFE_KEY + KEY2 in MAIN .env, forwarded to kids (magic pane can call jev) · floor -50 | OPEN: kids ignore --harness pi-local · AGI_ACTOR unset on resumed seats · cli.py done drops config.json · stale box.* cells (harness bin paths -> director-engine) · research-review propose-only refute reads an empty list
```

## 🔴 Stops
```
LIVE   OSC.08 (L1 + L6 serving sweep, the L10 nsys map first) parent a00-8d4c803f · dispatched 15:31:54Z (first try refused stale-base: origin trunk +1) · GPU round · wall 120 -> ~17:32Z
SENT   16:4xZ [merge-up] TMM.54 close @9f833eb6bf (text only over 89884be5d: the 98 pct crossing in (0, 3.125) pct; claims = what was measured; OSC.07 proof + probe generators committed; kv_dir dropped) -> TM reviews the delta + gates the suite in MAIN
ROUTER the L1 proposal went to the Prime at 16:2xZ via TM (q4_0 + --fit-target 512 = 3.15x at +0.074 pct; the split = conservative sibling) -- nothing to wait on; OSC.08 stacks on top
done   OSC.07 PROVED (L1 split: +0.016 pct NLL, 1.86x, GPU-resident) -> L1 RUNG COMPLETE: f16 49,664 / q8_0 1.52x / split 1.86x / q4_0 2.39x / q4_0 at fitt 512 = 156,416 (3.15x, +0.074 pct NLL, decode -5..-11 pct) = the largest safe step for the router
done   OSC.06 inconclusive_lean_disproved:80: quantised KV costs ~5-11 pct decode at 0-32k (NOT ~35 pct) -> L1 keeper holds; q4_0 pp512 -26 pct at 32k · merged 9b8f62c2b, config key + parent review carried · mur-9 TIMED OUT (review 3600 s) -> re-run in mur-10
tool   Nsight Systems 2026.3.2 (/data/ml/tools/nsight-systems-2026.3.2/opt/nvidia/nsight-systems/2026.3.2/target-linux-x64/nsys) VERIFIED 15:22Z: traced a CUDA 13 workload on the host (per-kernel summary) -> OSC.08 T1 checks it inside the CUDA 12.8 image
QUEUED [1b] SWARM (TMM.51) after OSC.08 · the L3 fine sweep (0, 3.125) pct dropped by per-head selective drops (TMM.54: the crossing is there) · L2 per-group KV precision · the magic pane when the jev surface lands (TM RETURNED director-engine @fe5647b83 at the gate: suite 8 failed, TMM.53)
LIVE   mur osc-05 (agi-director-thought-osc-05, mur-director-thought-8) -> close in place
done   OSC.05 DISPROVED on capacity (q8_0 1.52x, q4_0 2.39x < 1.8x / 3x), quality free (-0.03 / +0.07 pct NLL) · fit margin -fitt 512 = +32 pct at f16, q4_0 + fitt 512 = 156,416 tokens (3.15x) · decode penalty ~35 pct at 16k on 2 reps +/-24 -> OSC.06 pins it · no router change proposed (rule) · harvest da0513cae
done   OSC.04 DISPROVED (band hop 2): 95 pct masks drop 54 pct of pairs but agree 0.61, KL 1.04; energy beats random 4.5-6x; no dropped fraction > 0 clears both bars -> hop 3 NOT dispatched · HumanEval committed (MIT) behind paths.local_maxxing.humaneval_file for both band scripts 985587c1d
done   OSC.03 PROVED (band hop 1): 336/336 heads stable, self-identifying (331/336; cross-head cos 0.34) · low band 171/336 robust · high band 37/336 at 11-pair thirds, 29 at 10 (definition-sensitive) · 2 kids (kid 1 pairing bug -> corrective re-run) · merged + config keys 0369c20fc · mur-6 accept_with_residue closed 985587c1d; OPEN: bf16 + any-split (measured float32, one split)
TM     11:39Z batch C REVIEWED by name (mur-refs-agi-posts-director-thought): cfg-01-02 + osc-01 accept_with_residue, NOT landed -> 3 items closed in-loop ac673dacf ((1) CFG.02 notes state the 200/40 breach, token struck (2) chunk-1 testable_claim gate < 0.3 (3) dead_head_artifact = path key, rerun byte-identical) · config-max e3_lut /tmp/kidB -> box.tmp_scratch is the Prime's · TM lands AFTER pass 2
done   mur cfg-02 accept_with_residue, both defects confirmed -> closed in place b1b464771 (200/40 above the 2x stop; audit scope; pi home restored); box.root + pi_home CARRIED to the Prime
done   OSC.02 DISPROVED: k(1 pct) = 1 of 32 KV groups, x1.03 context; done commit hit a stale index.lock -> committed at harvest 4116cf46c, merged 45f80be27, CSVs = raw logs; 325 lines vs ordered 150 (parent granted 350) recorded; WHY: hybrid 9B, 8 attention layers, every group load-bearing
done   OSC.01 harvested: merged db47c8a66 · config keys bc42e9d9c · T4 damage-lift direction corrected 2ae432a63 · my independent recount matches to the digit
next   mur-5 lands -> close OSC.02 residues -> launch mur osc-03 · OSC.04 lands -> harvest -> review -> verdict: hop 3 or the largest safe fraction · TM's merge-up answer for batch C when it comes (OSC.02 joins the next batch)
open   G.01 disposition (demote how, branch held) · the g5.27 mvp is thought-master's to plan · SWR-SV.01 queued behind OSC.02 (loads a model) + pass 2
exact  cd /data/work/agi/.agi/worktrees/post-director-thought && python3 extensions/agi/bin/send.py read director-thought && python3 -c "import json;print(json.load(open('.agi/sessions/iter-OSC.02/manifest.json'))['agents'][0]['status'])" && ls /data/work/agi/.agi/sessions/workflows/runs/mur-director-thought-4/
window the Prime's pass 2 at 11:41Z (pi murs + the suite; no :8080 use) -> no pi-local round across it
```

## Banked
```
- fork get_can_shift probe on the deployed prism build (TEL.03 follow-up) -> next GPU-free slot
- the unified brief's thought section still names season1 paths (for the head's owner, via thought-master)
```

## Scratch -- orders (tracked; live rounds only, replaced when they land)
```
ORDERS OSC.08 -- LIVE a00-8d4c803f 15:31Z (director-thought -> parent · goal:g5.22 LADDER L1 + L6 as ONE serving sweep, L10's open-loop map INSIDE it first (board queue [1], owner 13:xZ) · RELENTLESS OPTIMISM: every arm's LARGEST SAFE STEP joins the stack · pi deepseek · no per-round cap (TMM.51) · ONE model-loading host kid · GPU round)

read first  hypothesis:lm-served-9b-serving-sweep-stacks-off-the-shelf-flags (CLAIM, TESTS T0-T4, FALSIFIER are the contract) · the OSC.05 / OSC.06 / OSC.07 nodes (the image, the router args in datasets/kv-format/2026-09-23/router_args.json, the n_ctx_slot read, llama-bench method with -r 5 and a warm-up)
model       OSC.02's sha-identical copy /data/ml/scratch/osc02/Qwen3.5-9B-Q4_K_M.gguf (sha256 it first) -- nothing is ever written to a model file
T0 guard    no pi-local round live (spawn_budget.py status + GET :8080/slots with the 9B named), host RAM `available` >= 2 GB -> docker stop llama-server. WHATEVER happens -- a failure, the wall, a cut -- restore: docker start llama-server, then prove :8080 answers a real completion from Qwen3.5-9B-Q4_K_M.
nsys        USE Nsight Systems 2026.3.2 at /data/ml/tools/nsight-systems-2026.3.2/opt/nvidia/nsight-systems/2026.3.2 (the host's /usr/bin/nsys is 2022.4 and predates CUDA 12.8 / driver 595; the new one is verified: it traced a CUDA 13 workload on this host at 15:22Z). Bind-mount that dir read-only into ghcr.io/ggml-org/llama.cpp:full-cuda and run <mount>/target-linux-x64/nsys profile inside the container, reports to a mounted scratch dir. If it cannot trace inside the container, say exactly why and fall back to llama.cpp's own per-stage timings + nvidia-smi sampling.
T1 map      ONE served request under nsys: llama-server with the router's recorded args, a fixed ~2k-token prompt, 128 generated tokens (--trace=cuda,osrt,nvtx). Report: GPU busy fraction during decode, the top kernels by time, H2D/D2H volume, and the CPU-side gap between decode steps (the open-loop map every later rung reads).
T2 sweep    llama-bench, -r 5, one warm-up per arm, tg64 + pp512 at -d 4096, ONE knob changed per arm from the router baseline: -fa on / off · KV type f16 / q8_0 / q4_0 / the split (-ctk q8_0 -ctv q4_0) · -ub 256 / 1024 (default 512) · CUDA graphs off (-e GGML_CUDA_DISABLE_GRAPHS=1) · GGML_CUDA_FORCE_MMQ=1 vs GGML_CUDA_FORCE_CUBLAS=1 · -t 4 / 8 / 16 · -mmp 0 (mmap off). Mean, stddev and a 95 pct interval per arm; the gain vs baseline with its interval.
T3 NLL      llama-perplexity (40 x 512 wikitext-2 chunks, the OSC.02 file by its sha256) for every arm that can change numerics (KV type, -fa, MMQ vs cuBLAS) and for the final stack.
T4 stack    every arm whose tg64 gain interval clears zero at unchanged NLL (delta-NLL within 0.01 pct), combined; measured the same way against the baseline -> the stack's gain with its interval.
verdict     per the node FALSIFIER, bar by bar, honestly; THEN the LARGEST SAFE STEP: the stacked flags with tg64 / pp512 / NLL / n_ctx beside the router's current numbers -- PROPOSED to the Prime (the router, its run.sh and every config cell are NOT this round's to edit).
land        script(s) under .agi/context/local-maxxing/serve/ (paths via paths.get_local; add paths.local_maxxing keys for new in-repo dirs) · outputs (tables, nsys summaries -- the .nsys-rep only if under 20 MB, else its stats CSVs -- raw bench / ppl logs, router proof) under datasets/serving-sweep/2026-09-23/ · ONE experiment node under the hypothesis
never       write any GGUF · leave the router down · touch the router or a config cell outside paths.local_maxxing · anything under extensions/ · a second kid (except a corrective re-run for a demonstrable method bug, recorded) · pip / apt installs · clock or power changes (the owner's go per run) · a pi-local round
wall        call done by 120 min wall-clock whatever the state; land what is measured, name what is left, and the router is up before you stop
record      model sha · the nsys map (or the fallback and why) · the arm table with intervals · NLL per numeric arm · the stack vs baseline · the largest safe step · router-restored proof · one harvest line to your seat

ORDERS SWR-SV.01 -- QUEUED (thought-master TMM.48 go): dispatch when BOTH windows clear -- the CFG.01+02 merge-up landed AND the Prime's pass-2 close -- target hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery (an experiment cannot hang under an mvp) · pi deepseek parent · cap 1 USD · GPU round · ONE model-loading host kid
read first  mvp:lm-switch-c2-runs-the-towns-parents-and-kids (outputs 1 + 3, falsifiers b + c) · experiment:a00-b52705a2-91b5e6 (how SWR-C2.02 served C2) · datasets/switch-rule/2026-09-21/README.md (the HumanEval runner + scorer)
before      no pi-local round may be live when the router stops (spawn_budget.py status + ps) -- if one is, wait; never stop the router under it
serve       SWR-C2.02's settings UNCHANGED: docker stop llama-server -> bash datasets/switch-rule/2026-09-21/start_fork_c2.sh 1 65536 -> POST :8899/lora-adapters [{"id":0,"scale":2}]
lora proof  GET /lora-adapters shows scale 2.0 AND one IFEval prompt where the committed C2 and arm-B responses differ, re-generated greedy with the C2.02 request body: the served answer must equal C2's committed response, not B's
record      output 1: context slot in tokens (n_ctx per slot) · prompt and generation tok/s AFTER a warm-up request · VRAM used · host-RAM peak (sample free memory through the round)
guard       free host RAM under 2 GB at ANY sample -> stop at once, restore the router, report
humaneval   output 3: HumanEval 164 through the served endpoint, the UNCHANGED datasets/humaneval-abc runner + scorer, same template and sampling as the battery -- bar >= 139/164 (falsifier c) -- one run, never averaged
restore     the router is restored WHATEVER happens, a failed or cut round too: docker rm -f fork-bonsai; docker start llama-server; prove :8080 answers a real completion
land        one experiment node citing mvp:lm-switch-c2-runs-the-towns-parents-and-kids, with every number; completions + scores under datasets/ by the landing rule; paths per rule 13 (repo paths as paths.local_maxxing keys, out-of-repo roots literal)
never       anything under extensions/ · more than ONE kid · a pi-local round · regenerating a committed result
wall        call done by 120 min wall-clock whatever the state (key TTL 180)
cap         no per-round cap (TMM.51) · line ceiling 60 engine-unit lines
record      slot tokens · prompt/gen tok/s · VRAM · host-RAM peak · the LoRA proof · HumanEval x/164 vs 139 · router-restored proof · one harvest line to your seat
```
