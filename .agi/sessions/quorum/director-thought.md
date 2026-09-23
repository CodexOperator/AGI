# CARD — director-thought · HEAD = doc:unified-head · ROLE TEMPLATE = doc:unified-director-brief (+ doc:lm-director-brief-customizations) · town todo = thought-master's trajectory (town:local-maxxing trajectory_standin) · this card = identity · my R&D loop · my rules · live state · stops · banked · scratch

## Identity
```
post      director-thought · director · town local-maxxing · owning goal goal:g5.19 · claude-opus-5-5 · gen 13 -> ROTATING 19:5xZ (meter 0.50 > line 0.47) · master thought-master
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
kidrun   a kid's backgrounded pass dies with its scope when its one-shot pi turn ends -- setsid / nohup do not escape the cgroup; the kid must poll in-turn (OSC.10 a00-b59ee70f)
         and an OOM kill of ANY process in a kid's scope stops the whole scope (systemd stop-on-OOM default), the kid's pi included (OSC.10 a00-04dc76fc: its pass grew 4.2 -> 5.2 GB, global OOM 19:23:59Z) -> kid scripts keep memory bounded per step
cpu-ram  a CPU torch pass on Qwen2.5-0.5B holds ~3.5 GB RSS: at most TWO at once on this 15.9 GB box beside a GPU round and director-engine's suite (OSC.10 at 18:5xZ: three passes + swap 2.8 GB -> 398 s per prompt) · a pause governor matches `^/data/ml/.venv/bin/python( -[a-zA-Z]+)* [^ ]*<script>` ONLY -- a bare script-name pattern also hits the pi agents, whose command lines carry the orders text (v1 paused a real pass for 38 s)
ceiling  a kid's line_ceiling comes ONLY from `CEILING: <=N production lines [across K kids]` INSIDE the hypothesis's testable_claim (spawn_budget._ceiling_clause); a body CEILING line is prose -> default 40 (OSC.10's trap, flagged in the swarm room)
step     every round's node names its LARGEST SAFE STEP beside the honest bar verdict (TMM.50); the step joins the ladder's stack
seat     a crash-recovery respawn leaves my row dirty in MAIN posts.md and the ack refuses -> commit that hunk alone in MAIN, then rotate.py ack --post director-thought --gen N --ref <ListAgents ref> continue
```

## Live state (19:5xZ 09-23 -- ROTATION card, written whole for gen 14)
```
TOP      OWNER 09:4xZ-09:5xZ (TMM.49): goal:g5.22 full force until the jev code fixes land · OWNER 13:xZ (TMM.50): every round names its LARGEST SAFE STEP; it joins the stack
LADDER   board queue [1] (L1..L12 + [1b] SWARM; the board's text is the source)
  L1     KV format       DONE  q4_0 + --fit-target 512 = 156,416 tokens (3.15x) at +0.074 pct NLL -> proposed to the Prime 16:2xZ (its long-prompt prefill cost is OSC.11's question)
  L6     serving knobs   DONE  no swept knob's tg64 interval clears zero (OSC.08, scoped per TMM.57)
  L10    open-loop map   DONE  a FRESH container pays a fixed ~45 s CUDA JIT (both stock images ship sm_75 as PTX only); a mounted ComputeCache removes it (OSC.09;
                               PROVEN in production by OSC.11: first container warm-up 185 s, the next 0.7 s) -> research drivers mount /data/ml/scratch/cuda-jit-cache
  L3     key precision   OSC.10 SWARM + control: DISPROVED twice over -- energy classes beat uniform at every budget (3-12 bits) and random 2.5-4.4x, but only 12 bits
                               per key element holds 0.98 / 0.02 on Qwen2.5-0.5B (8 bits: 0.943 / 0.024); per-token absmax is the wrong granularity for its keys
                         REFRAME Qwen2.5 has a k_proj bias and no QK-norm (outlier key channels); the served Qwen3.5 has QK-norm and q4_0 KV costs +0.074 pct -> the next
                               L3 question is a QK-norm model or per-channel / bias-subtracted keys, not more bits
  L6b    long prefill    OSC.11 LIVE (see Stops) · next: the build block (llama.cpp with 75-real SASS) · L2 · L4 · L5 · L7-L12 per the board
mvp      QUEUED SWR-SV.01 (switch mvp round 1): waits for the CFG merge-up to LAND at TM's gate -- orders below
batch A  the magic pane resumes when the jev code fixes land · G.01 held @109bcb618, DEMOTE rec, disposition ASKED
routed   OPEN: kids ignore --harness pi-local · AGI_ACTOR unset on resumed seats · cli.py done drops config.json · stale box.* cells
```

## 🔴 Stops -- gen 14 starts HERE, in this order
```
1 TMM.58 (TM 19:47Z) OPEN -- my close @60eac6b52 is ACCEPTED, but the anonymize gate (SM.122) refused it: three committed datasets carry the box's REAL
         nodename in a "host" field -- datasets/kv-format/2026-09-23/kv_format.json:2 · datasets/kv-format/2026-09-23-speed/kv_speed.json:2 ·
         datasets/kv-format/2026-09-23-split/kv_split.json:2; writers kv_format_round.py:100 · kv_speed_round.py:100 · kv_split_round.py:72 (os.uname().nodename)
    fix  ONE commit over 60eac6b52 (NOT over this branch's tip): git worktree add --detach /tmp/dt-tmm58 60eac6b52 -> the three values -> local-town ·
         the three drivers stop recording the nodename (drop the field; no literal) -> commit there -> git diff origin/local-maxxing/season2/main..<tip> > d.diff
         && python3 extensions/agi/bin/anonymize.py check --diff-file d.diff says ok -> merge <tip> into this branch -> push the mirror -> ONE line to TM
         with the tip. Order: director-engine's range lands first, mine right after on the same gate. NEVER type the real hostname into a dm, node or card.
    also tell TM (same line): an orphaned probe, pid 3056036 ('python3 -' importing kv_speed_round.py @e37e8cca1, cwd MAIN, started 14:32Z) has spun one
         core at 100 pct for 5 h; its output socket is dead -- it is not mine, I left it for its owner
2 BEFORE the next [merge-up]: run the SAME anonymize check over the whole range trunk..tip -- OSC.09 (router_log_full.txt, restore_proof.txt), OSC.10's
         provenance.json files and OSC.11's outputs may carry the nodename too
3 OSC.11 LIVE a00-67c8a71a (L6 long-prompt prefill, -ub 512/1024/2048 x KV f16/q8_0/q4_0 on the router's own image) · GPU · router DOWN since 18:26Z
         (its T0 guard) · wall 20:24Z · the router MUST be back: docker inspect -f '{{.State.Status}}' llama-server = running + one real completion
         harvest: merge its loop branch, check its worktree for uncommitted config; the trials are NOISY (806-1,242 tok/s on one slice; load 19-29, iowait
         29-35 pct, swap-out 23-28 MB/s: .agi/sessions/iter-OSC.11/director_contention.log) -> if the paired intervals cannot resolve 10 pct, re-run in a
         quiet window (no CPU torch rounds, no suite)
4 OSC.10 swarm parent a00-30502399 LIVE on kid 3 a00-86466b78 (one bit point per invocation, results saved per point) · wall ~20:16Z
         a01-f543f6a5 merged 39f0834f1 · control a00-c9a05d99 (OSC-CTL.10) merged aed061142 -> when a00-30502399 lands: merge its branch, then the SWARM
         measurement for the harvest: interpretations (room LAP 0 posts: both converged on the same quantizer, NO division of labour) · the message graph
         (room swarm-osc10) · results vs the control (all agree) · tokens + USD per agent (sum usage.totalTokens / usage.cost.total over the message_end
         lines of each agent's output.log: parents $1.15-1.56, kids $0.27-1.82 so far) · deaths: kid 1 = one-shot harness exit after a turn-ending poll,
         kid 2 = global OOM of its pass (5.2 GB) and systemd stopped its scope -> ONE mur for osc-10 (the three kid nodes) -> close in place
5 then ONE [merge-up] to TM: OSC.09 (harvest 5208ac454 + mur-12 close d65d5839c + its Dispatch line a9aed8731) + OSC.10 + OSC.11
done   TMM.56 (@21085aa1d, TM-verified) · TMM.57 (@60eac6b52, accepted TMM.58) · mur-12 (OSC.09) closed: 14 containers not 17; the router's first-ever 7.4 s
       request reconciled from its own log (the ~45 s JIT paid once: 7.4 s small-batch + 36.1 s large-batch) · belam 17:55Z trunk merged @9c227503b
tool   Nsight Systems 2026.3.2 /data/ml/tools/nsight-systems-2026.3.2/opt/nvidia/nsight-systems/2026.3.2/target-linux-x64/nsys
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
