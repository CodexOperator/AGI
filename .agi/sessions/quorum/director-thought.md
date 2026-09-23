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
ceiling  a kid's line_ceiling comes ONLY from `CEILING: <=N production lines [across K kids]` INSIDE the hypothesis's testable_claim (spawn_budget._ceiling_clause); a body CEILING line is prose -> default 40 (OSC.10's trap, flagged in the swarm room)
step     every round's node names its LARGEST SAFE STEP beside the honest bar verdict (TMM.50); the step joins the ladder's stack
seat     a crash-recovery respawn leaves my row dirty in MAIN posts.md and the ack refuses -> commit that hunk alone in MAIN, then rotate.py ack --post director-thought --gen N --ref <ListAgents ref> continue
```

## Live state (18:2xZ 09-23)
```
TOP      OWNER 09:4xZ-09:5xZ (TMM.49): goal:g5.22 full force until the jev code fixes land · OWNER 13:xZ (TMM.50): RELENTLESS OPTIMISM -- every round names its LARGEST SAFE STEP; it joins the stack
LADDER   board queue [1] (L1..L12 + [1b] SWARM; the board's text is the source)
  L1     KV format       DONE  q4_0 + --fit-target 512 = 156,416 tokens (3.15x) at +0.074 pct NLL, decode -5..-11 pct -> proposed to the Prime 16:2xZ
  L6     serving knobs   DONE  no knob's tg64 interval clears zero (OSC.08) · next block: a llama.cpp build with sm_75 SASS (75-real), OSC.09's root cause
  L10    open-loop map   DONE  warm router prefill ~1,400-1,500 tok/s · a FRESH container pays a fixed ~45 s CUDA JIT (both stock images ship sm_75 as PTX only)
                               -> research containers mount one persistent ComputeCache from the next GPU round · the router's mount PROPOSED (worth ~0 today)
  L6b    long prefill    LIVE  OSC.11: OSC.08's -ub arms ran on pp512, which cannot use a micro-batch above 512 -> re-measured on ~30k-token prompts (pi-local's real size)
  L3     key precision   LIVE  OSC.10 SWARM a00-30502399 + a01-f543f6a5 (room swarm-osc10) + OSC-CTL.10 control a00-c9a05d99 · CPU · Qwen2.5-0.5B
  next   L6 build block · L2 per-group KV precision · L4 geometry · L5 cross-quant maps · L7-L12 per the board
sparks   OSC.01 activation score ranks damage at 0.40 · OSC.02 per-group SENSITIVITY MAP · OSC.03 stable band fingerprints · OSC.04 energy ranking 4.5-6x over random
mvp      QUEUED SWR-SV.01 (switch mvp round 1): waits for the CFG merge-up to LAND at TM's gate -- orders below
batch A  the magic pane (T.01 + S.01) resumes when the jev code fixes land · no jev round until the TypeSafe key reaches kids
G.01     held @109bcb618 · rr-mp02-g01 DEMOTE rec (dedup leak 282 -> 243) · disposition ASKED, open
routed   OPEN: kids ignore --harness pi-local · AGI_ACTOR unset on resumed seats · cli.py done drops config.json · stale box.* cells · research-review propose-only refute reads an empty list
```

## 🔴 Stops
```
LIVE   OSC.10 SWARM (L3) a00-30502399 + a01-f543f6a5 · dispatched 18:1xZ (spawn.parallel 2 for that dispatch only, restored to 1 at once) · wall 120 -> ~20:1xZ
LIVE   OSC-CTL.10 single-parent control a00-c9a05d99 · 18:2xZ · wall 120 -> ~20:2xZ · (iteration ids must be <label>.<n>: OSC.10C was refused)
LIVE   OSC.11 (L6 long-prompt prefill: -ub 512/1024/2048 x KV f16/q8_0/q4_0 on the router's own image, ~30k prompts, JIT cache mounted) a00-67c8a71a · 18:24Z · GPU · wall 120 -> ~20:24Z
LIVE   mur-12 (OSC.09; unit agi-director-thought-osc-09) -> close residues in place -> ONE [merge-up] to TM: TMM.56 + the trunk merges + OSC.09 (+ OSC.10 if it lands first)
TM     TMM.56 DONE @21085aa1d (18:01Z) -> TM verified the diff (d3d6a5ed4); landing tip 9c227503b once TM's review run -4 of @0f3705ca8 returns -> ONE more order may come
belam  17:55Z [decision] trunk merged into this branch @9c227503b (the g5 dedup, clean, render --check ok)
done   OSC.09 DISPROVED as written: the cold first request = a FIXED ~45 s CUDA JIT per fresh container (13 tokens 44.7 s .. 7,638 tokens 49.7 s); warm 1,490-1,524 tok/s;
       a tiny warm-up works; the router paid it on none of its 11 logged loads · harvest 5208ac454 (T4 + T5 corrected, probes committed, the fatbin root cause)
done   OSC.08 DISPROVED: no serving knob clears zero -> the router sits at the off-the-shelf decode optimum
done   OSC.01-07: the pruning line + L1 (ladder lines above) · none of my batches is on the trunk yet (ac673dacf / 89884be5d / 0f3705ca8 await TM's gate)
tool   Nsight Systems 2026.3.2 /data/ml/tools/nsight-systems-2026.3.2/opt/nvidia/nsight-systems/2026.3.2/target-linux-x64/nsys (traces inside the CUDA 12.8 image)
open   G.01 disposition · SWR-SV.01 behind the CFG landing
```

## Banked
```
- fork get_can_shift probe on the deployed prism build (TEL.03 follow-up) -> next GPU-free slot
- the unified brief's thought section still names season1 paths (for the head's owner, via thought-master)
```

## Scratch -- orders (tracked; live rounds only, replaced when they land)
```
ORDERS OSC.11 -- (director-thought -> parent · goal:g5.22 LADDER L6 on the real workload: long-prompt prefill vs micro-batch x KV type · RELENTLESS OPTIMISM: name the LARGEST SAFE STEP · pi deepseek · no per-round cap · ONE model-loading host kid · GPU round)

read first  hypothesis:lm-served-9b-long-prompt-prefill-gains-from-larger-ubatch (Measured, CLAIM, Dispatch line, FALSIFIERS, TESTS, FILE SCOPE, CEILING are the contract -- answer its Dispatch line FIRST) · experiment:a00-df53894e-fabe8f (OSC.09: the fixed ~45 s JIT, the ComputeCache probe .agi/context/local-maxxing/serve/osc09/jitcache_probe.sh) · datasets/kv-format/2026-09-23/router_args.json (the router's model_args_9b)
model       the router's own file, mounted READ-ONLY: /data/ml/models -> check where the router mounts /models (docker inspect llama-server) and mount the same host dir :ro; sha256 the 9B first (OSC.02's copy /data/ml/scratch/osc02/Qwen3.5-9B-Q4_K_M.gguf is sha-identical, 03b74727...52b7e8, and may be used instead) -- nothing is ever written to a model file
image       ghcr.io/ggml-org/llama.cpp:server-cuda (the router's own build 10991, commit 930e2fa59) -- NOT full-cuda: the served measurement runs the served build
T0 guard    no pi-local round live (spawn_budget.py status + GET :8080/slots with the 9B named), host RAM `available` (free -m) >= 2 GB -> docker stop llama-server. WHATEVER happens -- a failure, the wall, a cut -- restore: docker start llama-server, then prove :8080 answers a real completion from Qwen3.5-9B-Q4_K_M.
jit cache   mount /data/ml/scratch/cuda-jit-cache (mkdir -p) at /root/.nv/ComputeCache in EVERY container, with -e CUDA_CACHE_MAXSIZE=4294967296 -- the first container pays the ~45 s once; record the first request of every container (T3)
servers     per arm a FRESH container (docker rm -f it after; free the port before reuse): the router's model_args_9b verbatim minus --port / --host, plus -fa on, -ctk T -ctv T, -ub U, -b max(2048, U), a spare port bound to 127.0.0.1
arms        T in f16 / q8_0 / q4_0 x U in 512 / 1024 / 2048 = 9 arms; an arm whose fitted n_ctx_slot is below the prompt (or that fails to load) is RECORDED as such, never retried with other flags
prompts     three distinct ~30k-token wikitext-2 slices from /data/ml/scratch/osc02/wikitext-2-raw/wiki.test.raw (record byte offsets + prompt_n), the SAME three for every arm, one chat message each; max_tokens 8, temperature 0, thinking off; first a short warm-up request per container
measure     per arm: n_ctx_slot from the load log · the warm-up's prompt_ms · per trial prompt_n / prompt_ms / tok/s · loadavg and `available` RAM at each trial (other CPU rounds may share the box)
T2          the paired gain of each U vs U=512 within each KV type (3 trials, a t interval) · every T at U=512 vs f16 at U=512 (the L1 KV types' real prefill cost at ~30k)
verdict     per the node FALSIFIERS; THEN the LARGEST SAFE STEP: the fastest arm that fits >= 32,768 tokens vs the router's (f16, 512), stacked with L1's KV choice -- PROPOSED to the Prime / thought-master; the router and every config cell are NOT this round's to edit
land        one script under .agi/context/local-maxxing/serve/ (paths via paths.get_local; the out key serving_sweep_ub_out_dir is committed -- add no other key) · outputs (per-arm json, load logs, the restore proof) under paths.get_local("serving_sweep_ub_out_dir") · ONE experiment node under the hypothesis
never       write any GGUF · leave the router down · touch the router or a config cell · anything under extensions/ · a second kid (except a corrective re-run for a demonstrable method bug, recorded) · installs or image pulls · a pi-local round
wall        call done by 120 min wall-clock whatever the state; the router is up before you stop
record      model sha · the 9 arms' n_ctx_slot and trials · the paired gains with intervals · the JIT-cache first-request proof · the verdict · the largest safe step · router-restored proof · one harvest line to your seat

ORDERS OSC.10 -- SWARM (director-thought -> TWO parents · goal:g5.22 LADDER L3 + [1b] SWARM (owner 14:xZ) · RELENTLESS OPTIMISM: name the LARGEST SAFE STEP · pi deepseek · no per-round cap · CPU only)

read first  hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits (Measured, CLAIM, Dispatch line, FALSIFIERS, TESTS, FILE SCOPE, CEILING are the contract -- answer its Dispatch line FIRST) · experiment:a00-fa4bb880-d965dd (OSC.04: build_eval, metrics and the apply_rotary_pos_emb hook in .agi/context/local-maxxing/osc/osc_band_prune.py) · experiment:a00-abdae729-7f4024 (OSC.03: datasets/osc-band/2026-09-23/profiles.json, sha256 e80ec2772b1845f2...)
swarm       you are ONE of TWO parents dispatched together on this hypothesis; a single-parent CONTROL runs the same hypothesis separately and never sees the room
room        swarm-osc10 (parents only; kids do not post) -- post: python3 extensions/agi/bin/send.py --from <your agent id> send --room swarm-osc10 "<text>" · read: python3 extensions/agi/bin/send.py --from <your agent id> read --room swarm-osc10
siblings    the director posts both parent ids in the room right after dispatch -- read the room first
lap 0       BEFORE your first kid, post your INTERPRETATION in the room: the conjuncts you will test, the quantizer (scale granularity, bit classes, how scale bytes are counted), the average-bit points, the comparators -- and a split of the work if you propose one
each lap    read the room before every kid spawn and before done; answer a sibling's question there; you may divide the work, converge on one design or deliberately diverge -- say which, and why, in the room
model       /data/ml/scratch/osc03/hf (Qwen2.5-0.5B-Instruct rev 7ae5576; verify the sha256s OSC.03/04 recorded) · wikitext /data/ml/scratch/osc02/wikitext-2-raw/wiki.test.raw · HumanEval via paths.get_local("humaneval_file")
cpu         nice -n 19, torch threads 4 (THREE CPU rounds share this box) · before every model pass the host `available` column of free -m >= 2 GB, else wait 60 s and re-check -- never start a pass under 2 GB · no GPU, no :8080, no GGUF, no docker
arms        reference = the unquantized model · at each average-bit point (3.5 and at least one lower): ENERGY (the K-side profile: OSC.03's per-pair energy summed over each KV head's 7 query heads) vs UNIFORM (one width, the same average bits) vs RANDOM (the same class sizes, seeds 1 2 3) · plus the plain blockwise 4-bit key baseline (32-value blocks, one fp16 scale per block: the q4_0 analog) · the bits accounting counts scale bytes · values and queries stay unquantized
land        outputs under paths.get_local("osc_band_kquant_dir") + "/<your agent id>/" (the key is committed; add no other key) · the script and its committed test under .agi/context/local-maxxing/osc/, named with your agent id · ONE experiment node under the hypothesis: the verdict per FALSIFIERS, bar by bar, THEN the LARGEST SAFE STEP (the lowest average key bits that hold both bars, and by which allocation)
record      per arm and bit point: agreement, KL, average bits (scales counted) · the selftests · the model sha256s · your room posts (timestamps + a one-line gist each) in the node's notes, and what you took from your sibling, if anything
never       anything under extensions/ · a second concurrent kid · the GPU, :8080, docker or a GGUF · editing the OSC.03/04 scripts or outputs · a config key other than the one committed · installs
wall        call done by 120 min wall-clock whatever the state

ORDERS OSC-CTL.10 -- SINGLE-PARENT CONTROL (director-thought -> ONE parent · goal:g5.22 LADDER L3 · RELENTLESS OPTIMISM: name the LARGEST SAFE STEP · pi deepseek · no per-round cap · CPU only)

read first  hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits (Measured, CLAIM, Dispatch line, FALSIFIERS, TESTS, FILE SCOPE, CEILING are the contract -- answer its Dispatch line FIRST) · experiment:a00-fa4bb880-d965dd (OSC.04: build_eval, metrics and the apply_rotary_pos_emb hook in .agi/context/local-maxxing/osc/osc_band_prune.py) · experiment:a00-abdae729-7f4024 (OSC.03: datasets/osc-band/2026-09-23/profiles.json, sha256 e80ec2772b1845f2...)
control     you work ALONE: read no room and post in none; two other parents work the same hypothesis separately, and your result is the control they are measured against
model       /data/ml/scratch/osc03/hf (Qwen2.5-0.5B-Instruct rev 7ae5576; verify the sha256s OSC.03/04 recorded) · wikitext /data/ml/scratch/osc02/wikitext-2-raw/wiki.test.raw · HumanEval via paths.get_local("humaneval_file")
cpu         nice -n 19, torch threads 4 (THREE CPU rounds share this box) · before every model pass the host `available` column of free -m >= 2 GB, else wait 60 s and re-check -- never start a pass under 2 GB · no GPU, no :8080, no GGUF, no docker
arms        reference = the unquantized model · at each average-bit point (3.5 and at least one lower): ENERGY (the K-side profile: OSC.03's per-pair energy summed over each KV head's 7 query heads) vs UNIFORM (one width, the same average bits) vs RANDOM (the same class sizes, seeds 1 2 3) · plus the plain blockwise 4-bit key baseline (32-value blocks, one fp16 scale per block: the q4_0 analog) · the bits accounting counts scale bytes · values and queries stay unquantized
land        outputs under paths.get_local("osc_band_kquant_dir") + "/<your agent id>/" (the key is committed; add no other key) · the script and its committed test under .agi/context/local-maxxing/osc/, named with your agent id · ONE experiment node under the hypothesis: the verdict per FALSIFIERS, bar by bar, THEN the LARGEST SAFE STEP (the lowest average key bits that hold both bars, and by which allocation)
record      per arm and bit point: agreement, KL, average bits (scales counted) · the selftests · the model sha256s
never       anything under extensions/ · a second concurrent kid · the GPU, :8080, docker or a GGUF · editing the OSC.03/04 scripts or outputs · a config key other than the one committed · installs
wall        call done by 120 min wall-clock whatever the state

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
