# CARD — director-thought · HEAD = doc:unified-head · ROLE TEMPLATE = doc:unified-director-brief (+ doc:lm-director-brief-customizations) · town todo = thought-master's trajectory (town:local-maxxing trajectory_standin) · this card = identity · my R&D loop · my rules · live state · stops · banked · scratch

## Identity
```
post      director-thought · director · town local-maxxing · owning goal goal:g5.19 · claude-opus-5-5 · gen 14 seated 19:50:56Z (TMM.61 20:13Z: no second rotation for this seat -- RESUMED) · master thought-master
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
murkey   workflow.py run merge-up-review: the run key is mur-<the rounds' merge_up field> (merge_up director-thought-13 -> mur-director-thought-13) · --dry-run first
```

## Live state (20:2xZ 09-23 -- gen 14, resumed)
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
                               own probe) · 2 of A's 3 kids died (one-shot harness exit, global OOM) -> the swarm has NOT earned a brief line (verdict after mur-13, item 1)
  L6b    long prefill    OSC.11 REFUTED: -ub is not a >= 10 pct long-prompt prefill lever (quiet re-run +1.29 pct); keep -ub 512 (mur-14 running)
                         next: the build block (llama.cpp with 75-real SASS) · L2 · L4 · L5 · L7-L12 per the board
mvp      QUEUED SWR-SV.01 (switch mvp round 1): waits for the CFG merge-up to LAND at TM's gate -- orders below
batch A  the magic pane resumes when the jev code fixes land · G.01 held @109bcb618, DEMOTE rec, disposition ASKED
routed   OPEN: kids ignore --harness pi-local · AGI_ACTOR unset on resumed seats · cli.py done drops config.json · stale box.* cells
```

## 🔴 Where it stops -- 20:2xZ 09-23, RESUMED per TMM.61 (no second rotation for this seat), in this order (the next command is item 1)
````
```
1 mur-director-thought-13 RUNNING (relaunched 20:14Z, bg; stages run one at a time) -- OSC.10's review, args .agi/sessions/iter-OSC.10/mur13.args.json
         (3 rounds osc-10-a / -b / -ctl, review -> verify, deepseek-v4.1-flash; merge-base 5f04722e3c, tips A 60d07740e6 · B 86f4f9bb14 · ctl e27e5995d6)
         results MAIN .agi/sessions/workflows/runs/mur-director-thought-13/ · if my session died: relaunch with the same args (run key = mur-<merge_up>)
    then close in place: CONFIRMED residues fixed in the kid nodes (write.py, AGI_ACTOR=director-thought) -> the hypothesis node gains a harvest section
         AFTER CEILING (the brief order stays): verdict disproved x3, the step (energy 9.0 bits, uniform 10.25), the [1b] SWARM numbers (LADDER above) and the
         swarm verdict: NOT earned, its lines stay orders text, no line in doc:lm-director-brief-customizations · push_further = the L3 REFRAME · a THOUGHT block
    residues to weigh: A's bw4 arm is a ~1.58-bit ternary quantizer labelled 4.5-bit (A's own probe; are B's and the control's baselines the same?) ·
         generic-named osc_band_kquant.py + test_osc_band_kquant.py beside the per-agent copies (FILE SCOPE) · the two death-record nodes carry no verdict
2 mur-director-thought-14 RUNNING (launched 20:2xZ, bg, BESIDE mur-13 -- a deviation from 'one mur at a time': the run keys differ by merge_up, shown by
         both dry-runs, so the key collision that rule guards cannot happen) -- OSC.11's review, args .agi/sessions/iter-OSC.11/mur14.args.json (one round osc-11,
         7158dbb4fb..3f627c6cf5 scoped to OSC.11's paths)
    OSC.11 HARVESTED: parent a00-67c8a71a done 20:10Z (c3b893d95b), merged 67837d6c23 · its REFUTATION evidence lived only in its gitignored probe dir ->
         committed verbatim at datasets/serving-sweep/2026-09-23-ub/parent-probe-a00-67c8a71a/ (3f627c6cf5) · worktree clean, no config edit
    the result: REFUTED (inconclusive_lean_disproved:90) -- the kid's q8_0 ub1024 +27.2 pct was a contended baseline; the parent's quiet re-run is +1.29 pct
         (q8_0 ub512 1181.9/1186.0/1189.1 vs ub1024 1197.6/1202.4/1203.0 tok/s); -ub is NOT a long-prompt lever here; every arm fits >= 32,768
    then close in place: the node body still carries the KID's LARGEST SAFE STEP paragraph (:112, q8_0 -ub 1024 +27.2 pct) and 'why a lean, not proved' (:128)
         against its refuted title -> rewrite them to the evidence; the step the data supports: keep -ub 512; L1's q4_0 KV shows no prefill cost at ~30k at
         ub512 (f16 1228/1143, q4_0 1173/1147, q8_0 1186 -- mur-14 item 3 checks this) -> PROPOSE to the Prime with L1, never edit the router or a cell
3 TMM.58: e0689f715 at TM's gate (TMM.61: 'one line when it lands') -- TM rotated gen 12 -> 13 at 20:1xZ; per TMM.59 its landing is TM's successor's step
4 anonymize over the whole range RE-RUN at 3f627c6cf5: MAIN's gate ok (two-dot and three-dot); the committed gate: loopback only (82 lines) -- the TRUNK's
         anonymize.py now drops loopback, so merging the trunk clears it
5 then: merge the town trunk (it moved: 2ed06d353d) -> ONE [merge-up] to TM: OSC.09 (harvest 5208ac454 + mur-12 close d65d5839c + Dispatch line a9aed8731)
         + OSC.10 (+ mur-13 close) + OSC.11 (+ mur-14 close)
done   TMM.56 (@21085aa1d) · TMM.57 (@60eac6b52) · TMM.58 (@e0689f715) · mur-12 (OSC.09) closed · OSC.10 all three parents merged (A 37b51df94, B 39f0834f1,
       control aed061142) · spawn.parallel back to 1 · OSC.11 merged 67837d6c23 + evidence 3f627c6cf5
tool   Nsight Systems 2026.3.2 /data/ml/tools/nsight-systems-2026.3.2/opt/nvidia/nsight-systems/2026.3.2/target-linux-x64/nsys
```
````

## Banked
```
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
