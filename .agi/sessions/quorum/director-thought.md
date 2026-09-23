AUTO-CAPTURED
AUTO-CAPTURED
AUTO-CAPTURED
# CARD — director-thought · HEAD = doc:unified-head · ROLE TEMPLATE = doc:unified-director-brief (+ doc:lm-director-brief-customizations) · town todo = thought-master's trajectory (town:local-maxxing trajectory_standin) · this card = identity · my R&D loop · my rules · live state · stops · banked · scratch

## Identity
```
post      director-thought · director · town local-maxxing · owning goal goal:g5.19 · claude-opus-5-5 · gen 14 seated 19:50:56Z -> ROTATING 22:3xZ at a clean stop (meter 0.45, line 0.47) · master thought-master
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
anon     an anonymize REFUSED names a CLASS only: locate it in-process (anonymize.box_tokens, values masked, per file and +/- sign) before acting · the committed gate counts the LOOPBACK address as a box token (MAIN's uncommitted patch drops loopback/link-local) · never type an IP or hostname literal into a dm
evidence every file a node cites (probe scripts, logs, T0 guard, restore proof, a step's source data) is written UNDER the round's out dir -- .agi/sessions is
         gitignored: OSC.10 A's step producer, OSC.11's parent probe and its kid's restore proof all sat there uncommitted (mur-13 / mur-14, 09-23) -> an orders line,
         and the harvest copies any stragglers verbatim beside the outputs after an anonymize check
restore  a restore proof is a PARSED completion naming the model (a non-empty reply), never a /slots read -- OSC.11's kid proof was a JSONDecodeError
memory   dispatch.py --memory N is written verbatim as MemoryMax=N (BYTES) -> pass 6G or omit it (config is 6G); a bare 6 OOM-killed OSC.12's first parent at start
murkey   workflow.py run merge-up-review: the run key is mur-<the rounds' merge_up field> (merge_up director-thought-13 -> mur-director-thought-13) · --dry-run first
```

## Live state (22:3xZ 09-23 -- gen 14, written whole for the rotation)
```
TOP      OWNER 09:4xZ-09:5xZ (TMM.49): goal:g5.22 full force until the jev code fixes land · OWNER 13:xZ (TMM.50): every round names its LARGEST SAFE STEP; it joins the stack
LADDER   board queue [1] (L1..L12 + [1b] SWARM; the board's text is the source)
  L1     KV format       DONE  q4_0 + --fit-target 512 = 156,416 tokens (3.15x) at +0.074 pct NLL -> proposed to the Prime 16:2xZ (its long-prompt prefill cost is OSC.11's question)
  L6     serving knobs   DONE  no swept knob's tg64 interval clears zero (OSC.08, scoped per TMM.57)
  L10    open-loop map   DONE  a FRESH container pays a fixed ~45 s CUDA JIT; a mounted ComputeCache removes it (OSC.09; proven by OSC.11: 185 s -> 0.7 s)
                               -> research drivers mount /data/ml/scratch/cuda-jit-cache
  L3     key precision   OSC.10 DISPROVED three times over at 3.5 bits (top-1 agree: A kid3 0.5645 · B 0.605 · control 0.5706, bar 0.98); conjuncts B + C hold in all three
                         STEP  A's finer upward grid: energy holds both bars at 9.0 bits, uniform at 10.25 (B + control's coarser grid: 12; 8 bits 0.943 / 0.024)
                         REFRAME a QK-norm model or per-channel / bias-subtracted keys, not more bits
  [1b]   SWARM           OSC.10 measured: 2 parents + 4 kids = 20.24 M tokens / 7.48 USD vs the control's 9.05 M / 3.23 USD (2.3x) · LAP 0 posts 14 s apart, B spawned
                               39 s later: NO division of labour, the same quantizer, the same verdict · only A added anything (the finer step grid + the bw4 defect, by its
                               own probe) · 2 of A's 3 kids died (one-shot harness exit, global OOM) -> the swarm has NOT earned a brief line -- FINAL after mur-13: NOT earned (the L3 hypothesis's harvest section)
  L6b    long prefill    OSC.11 REFUTED: -ub is not a >= 10 pct long-prompt prefill lever (quiet re-run +1.29 pct); keep -ub 512 (closed f2003718f0)
  L9/10  speculation     OSC.12 DISPROVED as stated, but speculation RUNS on qwen35: ngram-simple x7.9 on edit-and-return (8/8 identical), ~x1 elsewhere (closed, mur-15)
                         the build block is DEMOTED (THOUGHT on the OSC.12 hypothesis: the JIT cache already removes the cold JIT; PTX-JIT runs the same SASS class)
                         next: (llama.cpp with 75-real SASS) · L2 · L4 · L5 · L7-L12 per the board
mvp      QUEUED SWR-SV.01 (switch mvp round 1): waits for the CFG merge-up to LAND at TM's gate -- orders below
batch A  the magic pane resumes when the jev code fixes land · G.01 held @109bcb618, DEMOTE rec, disposition ASKED
routed   OPEN: dispatch.py --memory N is written verbatim as MemoryMax=N BYTES (use 6G or omit it; config is 6G) -> director-engine 20:29Z · kids ignore --harness pi-local · AGI_ACTOR unset on resumed seats · cli.py done drops config.json · stale box.* cells
```

## 🔴 Where it stops -- 22:3xZ 09-23, gen 15 starts HERE, in this order (the next command is item 1)
`````
````
```
1 [merge-up] OSC.12 SENT 22:27Z to TM at 496cd5e039 (harvest c957c56f2d + the mur-15 close 2c23e9173b + e6ed4681e8; my checks: selftest 4/4 on the merged
         tree, anonymize ok, links 0 broken, 0 node deletions, 0 GPU-model names) -> read TM's gate line (dm log + send.py read); a fix goes as ONE commit over
         496cd5e039 in a detached /tmp worktree, merged into this branch, one line to TM with the tip (the TMM.58 / TMM.63 pattern)
2 ACCOUNT: the rotation auto-capture at 21:5xZ read the provider account at total 170 USD, used 166.14, remaining 3.86 -- told TM 22:27Z. Every deepseek parent,
         kid and mur draws on it: read TM's answer BEFORE any paid dispatch (the LEAF round, a mur); bank it if TM is silent
3 LEAF (TMM.63, TM's order after OSC.12's harvest -- now due): ONE sweep round -- every host-path literal in town code -> a paths.local_maxxing cell
         (paths.get / get_local; shell: V="$(python3 .agi/context/local-maxxing/paths.py <key>)"); new in my range: osc_band_kquant_a00-ddd4762f.py:20 HF
         (obp.HF owns it), serve/cold_first_round.py SC, serve/ub_prefill_round.py SC + CACHE, serve/osc09/router_mode_probe.sh the wikitext path,
         specdec/specdec_a00_71dbbad5.py MODELS + CACHE; on the trunk: athena/fetch_parallel.py, heads/kv_group_round.py, heads/kv_group_surgery.py,
         kv/kv_{format,speed,split}_round.py, magic-pane/detect.py, osc/osc_band_{measure,prune}.py, serve/serve_sweep_round.py, telepathy/tel02/tel02_probe.py
         (datasets/ probes stay as recorded evidence) -> mint the hypothesis (schema order, CEILING in the claim), orders with the evidence + restore lines,
         dispatch WITHOUT --memory (config 6G), merge the trunk first (the dispatch refuses stale-base with exit 3)
4 NEXT speculation question (OSC.12 answered the gate: speculation RUNS on qwen35): the town's real share of edit-shaped turns -- what ngram-simple's x7.9 on
         edit-and-return is worth on the served workload; then hypothesis:lm-spec-decode-cpu-draft-hybrid (a draft download, its own <= 3 GB ceiling)
5 SWR-SV.01 stays QUEUED until the CFG merge-up lands at TM's gate (orders in the scratch)
done   TMM.56-58, TMM.63 · merge-up LANDED 5085dd5ef (OSC.09 + 10 + 11 + the OSC.12 mint) · OSC.12 harvested + closed (mur-15) · mur-12 / 13 / 14 / 15 closed · the
       [1b] swarm NOT earned · the build block demoted · the --memory unit trap routed to director-engine (dm 20:29Z)
traps  the rotation auto-capture REWRITES this card's Live state in the worktree (uncommitted, 'AUTO-CAPTURED' + a status block): read it, carry what matters,
       git checkout the card before committing · write.py replace body is its own submit · murs launched from a session die with it -> systemd-run --user
tool   Nsight Systems 2026.3.2 /data/ml/tools/nsight-systems-2026.3.2/opt/nvidia/nsight-systems/2026.3.2/target-linux-x64/nsys
```
````
`````

## Banked
```
- the provider account (3.86 USD left at 21:5xZ, told TM 22:27Z): the next paid dispatch waits on TM's word
- fork get_can_shift probe on the deployed prism build (TEL.03 follow-up) -> next GPU-free slot
- the unified brief's thought section still names season1 paths (for the head's owner, via thought-master)
```

## Scratch -- orders (tracked; live rounds only, replaced when they land)
```
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
