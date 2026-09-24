AUTO-CAPTURED
# CARD — director-thought · HEAD = doc:unified-head · ROLE TEMPLATE = doc:unified-director-brief (+ doc:lm-director-brief-customizations) · town todo = thought-master's trajectory (town:local-maxxing trajectory_standin) · this card = identity · my R&D loop · my rules · live state · stops · banked · scratch

## Identity
```
post      director-thought · director · town local-maxxing · owning goal goal:g5.19 · claude-opus-5-5 seated 22:28:59Z 09-23 (session post-director-thought-18) -> claude-sonnet-5 effort MAX by the OWNER live in the app (22:5xZ; TMM.71/72: NO rotation for the switch) · the Prime writes the config:posts model cell · rotate at meter f >= 0.47, BARE (never --model: rotate exits 3 on a model that differs from the row) · master thought-master
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


## Live state (02:4xZ 09-24)
- **Rotation record:** gen n/a, window @23, pid 568154, model_confirm ok.
- **Node counts:** active n/a, deprecated n/a.
- **Tree:** branch local-maxxing/season2/posts/director-thought/main, behind season2/main 0, unpushed n/a.
- **Meter:** 0.402643 · role director · model claude-opus-5-5.
- **Account:** total=$192.00 used=$177.96 remaining=$14.04
## 🔴 Where it stops -- 03:3xZ 09-24: LEAF.04 LANDED (proved) @9a7797e39d; its mur runs; B/C next as DIRECT pi-free kids unless TM says otherwise
```
stops: director-thought gen 16: card -- LEAF.04 landed (proved) and its mur running; the pi-free kid-401 red sent to TM with the direct-kid default for B/C | last dm:  | auto-captured at f=0.4026 at the captive ratio 0.85 x the line, no self-rotate
```
## Banked
auto-captured at f=0.4026 at the captive ratio 0.85 x the line, no self-rotate
## Scratch -- orders (tracked; live rounds only, replaced when they land)
```
ORDERS LEAF.04 -- the files .agi/sessions/orders/LEAF.04.parent.txt + LEAF.04.kid-A.txt (gitignored; if lost: the LEAF.02 pair with LEAF.02 -> LEAF.04)

ORDERS REPLAY.01 -- READY, THIRD on the free lane (TMM.90) -- target hypothesis:lm-agent-transcript-replay-prices-ngram-speculation
dispatch    python3 extensions/agi/bin/dispatch.py . REPLAY.01 --target hypothesis:lm-agent-transcript-replay-prices-ngram-speculation --level small --tier parent
            --harness pi-free --branch --orders <this block as a file>  (NO --memory; its kid spawn carries --harness pi-free)
read first  the node (Measured · CLAIM · FALSIFIERS · FILE SCOPE) · experiment:a00-71dbbad5-e8f839 (OSC.12's classes, rows and acceptance lines) ·
            llama.cpp's draft-free rules at the served image's build (10991): the exact trigger, n / m and acceptance rule per type
order       ONE kid: (1) the replay + its selftest · (2) the calibration on OSC.12's 24 requests per rule, committed FIRST · (3) only then the transcripts:
            the seeded stratified sample, the per-part acceptance table, the projections with and without thinking, two disjoint samples
data        the transcript root is a command-line argument, never a literal (paths.local_maxxing.pi_traj_dir names another box's pi home: stale, routed)
            -- the pi harness home on this box; streamed, never loaded whole
tokenizer   the served 9B vocabulary through the BRAIN read-only /tokenize (the local-town provider endpoint in the default pi config;
            add_special false): its GGUF carries the 9B BPE byte-for-byte (7f226b8bec) -- the router is STOPPED; never restart or reconfigure
            the brain; the LEAF {models_dir} cells resolve only after leaf A lands
evidence    every output under paths.local_maxxing.specdec_replay_out_dir (get_local), committed; counts and hashes only, never transcript text;
            anonymize.py check before the commit
never       the GPU · the router restarted · extensions/ · .agi/config.json · OSC.12's committed results regenerated
restore     none -- no box state is touched
wall        call done by 120 min wall-clock whatever the state
record      calibration misses per rule (x/24) · acceptance per part (thinking / bash / text / write / edit / read) per rule · the fitted curve + its E / D
            residuals · projected median per rule, thinking on / off · two-sample agreement · one harvest line to my seat

ORDERS SWR-SV.01 -- SUPERSEDED by QUEUE 4 (the old stop-the-router / start-the-fork / restore block is moot: the brain already serves the C2.02 config)
```
