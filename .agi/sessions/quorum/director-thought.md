# CARD — director-thought · HEAD = doc:unified-head · ROLE TEMPLATE = doc:unified-director-brief (+ doc:lm-director-brief-customizations) · town todo = thought-master's trajectory (town:local-maxxing trajectory_standin) · this card = identity · my R&D loop · my rules · live state · stops · banked · scratch

## Identity
```
post      director-thought · director · town local-maxxing · owning goal goal:g5.19 · claude-opus-5-5 · seated 22:28:59Z 09-23 (session post-director-thought-18; ack answered continue by the predecessor) · rotate at meter f >= 0.47 · master thought-master
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


## Live state (22:4xZ 09-23)
```
TOP      OWNER 09:4xZ-09:5xZ (TMM.49): goal:g5.22 full force until the jev code fixes land · OWNER 13:xZ (TMM.50): every round names its LARGEST SAFE STEP; it joins the stack
HOLD     TMM.66 (TM 22:29Z): NO new OpenRouter dispatch -- pi parents, kids, murs -- until the Prime / owner answers (account 3.26 USD of 170 at 22:3xZ;
         PASS 3 needs it at 01:37Z) · running rounds finish · local work goes on · a fix delta needs no mur (TM verifies at the gate) · LIFTS = one TM line
         pi-local is NOT a way round it: kids ignore --harness pi-local and run on OpenRouter (board open (2)); a parent never writes code (brief.py _parent)
LADDER   board queue [1] (L1..L12 + [1b]; the board's text is the source)
  done   L1 KV format (q4_0 + --fit-target 512 = 156,416 tokens, 3.15x, +0.074 pct NLL; the router answer is the Prime's) · L6 knobs (no tg64 interval clears 0)
         · L10 open-loop map (a mounted JIT cache removes the ~45 s cold JIT: 185 s -> 0.7 s) · L6b -ub refuted (keep 512)
  L3     DISPROVED x3 at 3.5 bits (top-1 agree 0.56-0.61, bar 0.98) · STEP energy holds both bars at 9.0 bits · REFRAME a QK-norm model or per-channel keys
  [1b]   the swarm has NOT earned a brief line (2.3x the tokens of the control, no division of labour)
  L9/10  OSC.12 DISPROVED as stated, but speculation RUNS on qwen35: ngram-simple x7.9 on edit-and-return (8/8 identical), ~x1 elsewhere · build block DEMOTED
LEAF     MINTED 827d4212c0 (pushed): hypothesis:lm-town-code-host-paths-resolve-through-paths-cells, under hypothesis:lm-every-experiment-path-is-a-config-variable
         -- dispatch-ready, waits on the lift · baseline 56 lines / 32 files at f1f675975f (TMM.63 named 15 + my card 1; the regex finds 16 more)
         · the 12 paths.local_maxxing cells ride the mint (config-max first; cli.py done drops config.json) -- each checked: resolves to an existing path
         DEVIATION (THOUGHT on the node): rule 13 bars an agent from box cells -> the four out-of-repo roots stay literal ONCE in paths.py as proposed box
         cells (models_dir, ml_scratch_dir, ml_venv_dir, ml_tools_dir), every sub-path -> a cell: target 4 lines in 1 file + 6 dead-root docstring lines (c2/ d1/)
mvp      QUEUED SWR-SV.01: waits for the CFG merge-up to LAND at TM's gate AND the lift
batch A  magic pane: director-engine 21:23Z says the jev choice surface is complete (goal:g1.25 "all 70") @a281bb0d85, but TM returned that tip for 2 reds
         (TMM.64) -> NOT on the trunk yet; the pane waits for it to land (and the lift) · G.01 held @109bcb618, DEMOTE rec, disposition ASKED
routed   OPEN: dispatch.py --memory N = MemoryMax N BYTES (6G or omit) -> director-engine 20:29Z · kids ignore --harness pi-local · AGI_ACTOR unset on resumed seats
         · cli.py done drops config.json · stale box.* cells
```

## 🔴 Where it stops -- 22:4xZ 09-23, the next command is item 1
```
1 [merge-up] OSC.12 at 496cd5e039, SENT 22:27Z -> read TM's gate line (dm log + send.py read; TM's own queue puts director-engine's re-sent tip first)
         a fix = ONE commit over 496cd5e039 in a detached /tmp worktree, merged here, one line to TM with the tip -- no mur (TMM.66: TM verifies a fix delta)
2 HOLD (TMM.66): on TM's lift line -> merge the town trunk, push the mirror, dispatch LEAF.01 (the command + orders in the scratch)
3 NEXT in the queue, zero-spend until the lift: FRAME item 4 -- the town's real share of edit-shaped output, i.e. what ngram-simple's x7.9 is worth on
         agent turns (an offline n-gram replay over committed pi transcripts, CPU only) -> mint it dispatch-ready; then hypothesis:lm-spec-decode-cpu-draft-hybrid
4 SWR-SV.01 stays QUEUED (the CFG merge-up landed at TM's gate + the lift)
done   this session: TMM.66 read, no paid dispatch · LEAF baseline measured (56 / 32) + minted 827d4212c0 + mirror pushed · town tests 21 passed at f1f675975f
traps  the rotation auto-capture REWRITES this card's Live state in the worktree (uncommitted, 'AUTO-CAPTURED' + a status block): read it, carry what matters,
       git checkout the card before committing · write.py replace body is its own submit · murs launched from a session die with it -> systemd-run --user
       · paths.py audit (the engine's) does NOT scan town code -- the LEAF's measure is its own regex (the node's FALSIFIERS)
tool   Nsight Systems: paths.local_maxxing.nsys_dir (+ /target-linux-x64/nsys)
```

## Banked
```
- the provider account (3.26 USD at 22:3xZ): TMM.66 HOLD -- lifts on TM's line
- four proposed box cells (models_dir, ml_scratch_dir, ml_venv_dir, ml_tools_dir) are the Prime's to write (rule 13); they retire the LEAF's root table -> one proposed line in the LEAF's [merge-up]
- fork get_can_shift probe on the deployed prism build (TEL.03 follow-up) -> next GPU-free slot
- the unified brief's thought section still names season1 paths (for the head's owner, via thought-master)
```

## Scratch -- orders (tracked; live rounds only, replaced when they land)
```
ORDERS LEAF.01 -- READY, dispatch on TM's lift of TMM.66 -- target hypothesis:lm-town-code-host-paths-resolve-through-paths-cells
dispatch    python3 extensions/agi/bin/dispatch.py . LEAF.01 --target hypothesis:lm-town-code-host-paths-resolve-through-paths-cells --level small --tier parent
            --harness pi --branch --orders <this block as a file>  (NO --memory; merge the town trunk + push the mirror first: exit 3 = stale base)
read first  the node (CLAIM · Dispatch line · FILE SCOPE · CEILING) · extensions/agi/lib/agent-prompt.md rule 13 · .agi/context/local-maxxing/paths.py
kids        A FIRST and alone: paths.py resolves {models_dir} {ml_scratch_dir} {ml_venv_dir} {ml_tools_dir} from box.* first, else ONE table tagged
            'proposed box.<name>'; an unresolved {name} raises; the three tests in test_paths_local.py
            -> then B (osc/ + heads/) and C (athena e3 kv magic-pane serve specdec spectral telepathy) in parallel, disjoint files
before      each kid runs the node's TESTS neighbourhood command BEFORE its first edit and records the result
evidence    the before / after regex listings + the value table as run -> paths.local_maxxing.path_sweep_out_dir (get_local), committed -- never under .agi/sessions
never       .agi/config.json (a missing cell -> named in the node, the director adds it at harvest) · extensions/ · datasets/ outside the out dir · a model load,
            the GPU, the router · another node · c2/ and d1/
restore     none -- no box state is touched
wall        call done by 120 min wall-clock whatever the state
record      regex count before -> after · the value table · py_compile / bash -n per touched file · neighbourhood before == after · one harvest line to my seat

ORDERS SWR-SV.01 -- QUEUED (thought-master TMM.48 go): dispatch when BOTH windows clear -- the CFG.01+02 merge-up landed AND the Prime's pass-2 close -- AND the TMM.66 lift -- target hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery (an experiment cannot hang under an mvp) · pi deepseek parent · GPU round · ONE model-loading host kid
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
