# CARD — director-thought · HEAD = doc:unified-head · ROLE TEMPLATE = doc:unified-director-brief (+ doc:lm-director-brief-customizations) · town todo = thought-master's trajectory (town:local-maxxing trajectory_standin) · this card = identity · my R&D loop · my rules · live state · stops · banked · scratch

## Identity
```
post      director-thought · director · town local-maxxing · owning goal goal:g5.19 · gen 17 claude-opus-5-5 seated 03:31:50Z 09-24 (session post-director-thought-b7) · the Prime writes the config:posts model cell · rotate at meter f >= 0.47, BARE (never --model: rotate exits 3 on a model that differs from the row) · master thought-master
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
merge    the town trunk only, before every dispatch -- and AGAIN right before it: the trunk moved 4 commits between my merge-up (03:36Z) and the LEAF.05 dispatch (03:38Z); derived-file conflicts (GOALS.md) re-render; owner-log conflicts keep both sides in time order
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
ceiling  a kid's line_ceiling comes ONLY from `CEILING: <=N production lines [across K kids]` INSIDE the hypothesis's testable_claim (spawn_budget._ceiling_clause); a body CEILING line is prose -> default 40 (OSC.10's trap, flagged in the swarm room) · slice = ceil(N/K); the hard checkpoint is 2x the slice
step     every round's node names its LARGEST SAFE STEP beside the honest bar verdict (TMM.50); the step joins the ladder's stack
seat     a crash-recovery respawn leaves my row dirty in MAIN posts.md and the ack refuses -> commit that hunk alone in MAIN, then rotate.py ack --post director-thought --gen N --ref <ListAgents ref> continue
anon     an anonymize REFUSED names a CLASS only: locate it in-process (anonymize.box_tokens, values masked, per file and +/- sign) before acting · the committed gate counts the LOOPBACK address as a box token (MAIN's uncommitted patch drops loopback/link-local) · never type an IP or hostname literal into a dm
evidence every file a node cites (probe scripts, logs, T0 guard, restore proof, a step's source data) is written UNDER the round's out dir -- .agi/sessions is
         gitignored: OSC.10 A's step producer, OSC.11's parent probe and its kid's restore proof all sat there uncommitted (mur-13 / mur-14, 09-23) -> an orders line,
         and the harvest copies any stragglers verbatim beside the outputs after an anonymize check
runs     evidence_runs is a LIST: write.py set evidence_runs [<id>] -- a scalar string counts 0 (normalize_evidence_runs: str -> 0) and the grid gate demotes a decisive verdict;
         an experiment MAY cite itself (LEAF.04: gen 16 wrote the scalar, 3dda5c0841 demoted, e88d61a1a7 fixed) · the mur prime_step line spells the scalar: never copy it
restore  a restore proof is a PARSED completion naming the model (a non-empty reply), never a /slots read -- OSC.11's kid proof was a JSONDecodeError
memory   dispatch.py --memory N is written verbatim as MemoryMax=N (BYTES) -> pass 6G or omit it (config is 6G); a bare 6 OOM-killed OSC.12's first parent at start
murkey   workflow.py run merge-up-review: the run key is mur-<the rounds' merge_up field> (merge_up director-thought-13 -> mur-director-thought-13) · --dry-run first
```

## Live state (03:4xZ 09-24, gen 17)
```
TOP      OWNER 02:3xZ (TMM.90, verbatim on goal:g5): "Let's resume normal operations using the free Openrouter endpoint. No more special usd0 runs
         just research towards doing more efficient usd0 runs in the future"
TOP2     OWNER via TM, verbatim: TMM.95 03:39Z "Make both directors go back to spawning parents efficiently with minimal token use." (LEAN:
         short briefs, no side work, one [merge-up] per batch) · TMM.96 03:42Z "Let director thought keep pulling on threads independently only
         informing you of occasionally of various milestones and to brainstorm next moves." -> self-loop; dm TM ONLY at a milestone (+ next-move
         options) or a blocker
LANES    FREE   OPEN since TMM.92 (03:18Z): --harness pi-free (stealth/space-bunny-alpha), 0 USD · the provider RETAINS prompts (account ZDR off)
                -> anonymize --text on every orders file; no secret, key, address or hardware name in any brief
                PARENTS again (TMM.95) -- LEAF.04's kid 401 likely rode the parent passing the MAIN checkout as <project> (its kid manifest landed
                there): parent orders now pin `dispatch.py .` from the parent's own worktree · LEAF.05 ran as a direct kid before TMM.95 (90 s, clean)
         PAID   held (TMM.66) · a kid record showing harness pi = CUT it + one line to TM
         LOCAL  retired as an operating mode (TMM.90): 0-USD efficiency = research hypotheses on FREE
BRAIN    brain-orcabonsai27b UP on the loopback 8080 (C2, one 65,536 slot, router stopped) -- nobody's lane now; never restart it without the owner
GATE     [merge-up] LEAF.04 batch sent 03:36:52Z at 4c67ce248a (47 commits / 19 files; TM pane busy -> queued): LEAF.04 proved (mur-16 closed in
         place, e88d61a1a7) + REPLAY framing + 5 minted hypotheses + brain swap; config hunk (b) = the pi-local row -> OrcaBonsai: TM keeps or drops
LADDER   board queue [1] (L1..L12 + [1b]; the board's text is the source)
  done   L1 KV format (q4_0 + --fit-target 512 = 156,416 tokens, 3.15x, +0.074 pct NLL) · L6 knobs · L10 open-loop map · L6b -ub refuted (keep 512)
  L3     DISPROVED x3 at 3.5 bits (top-1 agree 0.56-0.61, bar 0.98) · STEP energy holds both bars at 9.0 bits · REFRAME a QK-norm model or per-channel keys
  [1b]   the swarm has NOT earned a brief line (2.3x the tokens of the control, no division of labour)
  L9/10  OSC.12 DISPROVED as stated (ngram-simple x7.9 on edit-and-return only) -> REFRAME = REPLAY.01 (bc777c1fe7)
routed   OPEN: dispatch.py --memory N = MemoryMax N BYTES (6G or omit) -> director-engine · kids ignore --harness pi-local · AGI_ACTOR unset on resumed
         seats · cli.py done drops config.json · stale box.* / locations.* cells (box.root = another box's home: the paths.py CLI get() of a
         RELATIVE cell resolves there -- use get_local) · pi-free parent -> kid 401 + no kid manifest / agent.json (to TM 03:27Z, for director-engine)
```

## 🔴 Where it stops -- 03:4xZ 09-24: LEAF.05 (kid B) LANDED proved @7acd103f71; LEAF.06 (kid C) LIVE as a lean pi-free PARENT (TMM.95)
```
NOW      LEAF.06 parent a00-9bca4596 LIVE since 03:46:17Z (pid 1680349, pi-free, key agi-iterLEAF.06-parent-a00-9bca4596) · branch
         season2/loops/hypothesis-lm-town-code-host-pat-a00-9bca4596 · manifest .agi/sessions/iter-LEAF.06/ in MY tree · wall 60 min -> 04:46Z
         orders .agi/sessions/orders/LEAF.06.parent.txt (ONE kid C, --harness pi-free, project = its own worktree) + LEAF.06.kid-C.txt (15 files, 19 lines)
         the parent runs leaf_sweep_evidence.py LEAF.06 itself · watch: a background loop here (dies with me) -- by hand: ps -p 1680349
ON DONE  LEAN: the parent's verdict + its evidence json (after_hits 0, cells identical) + git diff --stat vs the merge-base (15 files + node + evidence)
         -> merge its branch -> the whole-town regex = only the 4 table lines + 6 ~/.venv-lm lines (the LEAF claim) -> ONE mur for B + C (pi-free)
         -> the LEAF parent's verdict -> [merge-up] + MILESTONE line to TM with next-move options (TMM.96)
LANDED   LEAF.05 kid B a00-78eb042c (direct, 90 s, 0 USD): experiment:a00-78eb042c-b02230 PROVED -- regex 31 -> 0, 9/9 cells identical, 24 = 24,
         osc tests before = after; the kid skipped the evidence + the before run -> written by me under path_sweep_out_dir (7acd103f71)
QUEUE    (TMM.90/92/95: my ready order, lean parents)
  1 LEAF.04  DONE: proved, mur-16 closed in place, [merge-up] sent 03:36Z (GATE)
  2 LEAF.01  B DONE (LEAF.05) · C LIVE (LEAF.06, parent)
  3 REPLAY.01 (bc777c1fe7) -- the tokenizer route holds on the brain (7f226b8bec); orders in the scratch; a lean PARENT (TMM.95): shorten the
             orders, pin the kid spawn to `dispatch.py .` from the parent's own worktree
  4 SWR-SV.01 -- the brain IS the SWR-C2.02 serve config: output 1 = the brain-swap numbers + the ONE LoRA-proof prompt still owed · output 3 =
             HumanEval 164 ONCE MORE on the served build (the mvp words; the battery C2 143/164 is the single run it replicates) = ~1 h of the slot,
             a script, no agents, 0 USD -> needs TM's go (TMM.90 retired 0-USD runs as an operating mode) -- OWED: my 02:4xZ dm said review-only
             and TM agreed on that wrong line -> CORRECT it in the next TM line (the B + C merge-up)
  5 RESEARCH (TMM.90, minted 28ed92197b under experiment:director-thought-brain-swap-2026-09-24, one pi-free kid each, 0 USD, CPU only):
             hypothesis:lm-pi-agents-load-claude-md-twice (13,916 tokens = 55 pct of a 25,317-token first prompt; lever = --no-context-files,
             director-engine's lane) · hypothesis:lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared
LOG      03:31Z mur-director-thought-16 (pi-free): review demote on ONE defect (no evidence_runs), 6/6 claim conjuncts MET; verify confirmed it,
                refuted the fallback-table residue -> gen 16 set a SCALAR self-citation (counts 0) -> 3dda5c0841 recorded the demotion ->
                gen 17 e88d61a1a7: a one-entry LIST -> enforce_on_disk passes, proved restored
         03:36Z trunk a7bee7f7d2 merged (4c67ce248a), checks: leaf tests 8/8 · anonymize ok · links 0 broken · 0 node deletions -> [merge-up] to TM
         03:38Z trunk 1a34e5f070 merged again (b2b29f0b67: goal:g5's Agent Notes left the goal) -> LEAF.05 dispatched, dry-run first (exit 0)

0 MODEL  rotate only at the line (f >= 0.47), BARE: python3 extensions/agi/bin/rotate.py rotate -- if it refuses a stale .agi/nodes/.geometry/, merge
         origin/season2/main as the refusal names (40fd462f4c did: a row conflict resolves to origin's live values) and re-run
traps  RE-READ the dm log right before any dispatch: TMM.90 landed 02:30:27Z between my gate read and the LEAF.04 dispatch and stopped a
       special 0-USD run; TMM.71 once withdrew TMM.70 the same way
       · NEVER grep a dispatch output down to spawned|manifest: a stale-base refusal (exit 3) then prints nothing you see -- tee it to a file
         and read the tail
       · the rotate-out COMMITS a thin auto-captured card: the full card lives only in the predecessor's last hand-written card commit
         (gen 16 = ec37d59f8e) -> the successor rebuilds it whole from there
       · pi prints a COST for a custom model id (0.0326 on a 24K free turn) = its own table, not the bill: the key used= (provisioning.py status)
         is the truth
       · write.py: a joined script --dry-run admits can still be refused live ("replace body is standalone") -> replace body alone, thought apart
       · replace body refuses a range that splits a section: a heading's section runs to the next heading, the THOUGHT block included -> replace
         the whole section, carrying the THOUGHT bytes
       · write.py replace body is its own submit · murs launched from a session die with it -> systemd-run --user
       · paths.py audit (the engine's) does NOT scan town code -- the LEAF's measure is its own regex (the node's FALSIFIERS)
       · the dispatch dry-run warns "ladder row wins -> deepseek" and then --harness pi-free overrides it: the spawn line's --model is the truth
tool   Nsight Systems: paths.local_maxxing.nsys_dir (+ /target-linux-x64/nsys) now that the LEAF resolver has landed
```

## Banked
```
- four proposed box cells (models_dir, ml_scratch_dir, ml_venv_dir, ml_tools_dir) are the Prime's to write (rule 13); they retire the LEAF's root table
- the CLAUDE.md-twice lever is ONE flag in the engine pi adapter (director-engine's lane): route it once its round measures it
- a future local brain's pi model entry (contextWindow <= 60,000 under a 65,536 slot) is pi config = TM / the owner
- fork get_can_shift probe on the deployed prism build (TEL.03 follow-up) -> next GPU-free slot
- the unified brief's thought section still names season1 paths (for the head's owner, via thought-master)
```

## Scratch -- orders (tracked; live rounds only, replaced when they land)
```
ORDERS LEAF.06 (C, LIVE) -- .agi/sessions/orders/LEAF.06.parent.txt + LEAF.06.kid-C.txt (gitignored; if lost: rebuild from the LEAF node's FILE
            SCOPE + CEILING split, one row per FALSIFIERS-regex hit: file:line literal -> paths.get(cell)) · dispatched as:
            AGI_POST=director-thought python3 extensions/agi/bin/dispatch.py . LEAF.06 --target hypothesis:lm-town-code-host-paths-resolve-through-paths-cells
            --level small --tier parent --harness pi-free --branch --detach --orders .agi/sessions/orders/LEAF.06.parent.txt --from director-thought > <file> 2>&1

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
            the brain
evidence    every output under paths.local_maxxing.specdec_replay_out_dir (get_local), committed; counts and hashes only, never transcript text;
            anonymize.py check before the commit
never       the GPU · the router restarted · extensions/ · .agi/config.json · OSC.12's committed results regenerated
restore     none -- no box state is touched
wall        call done by 120 min wall-clock whatever the state
record      calibration misses per rule (x/24) · acceptance per part (thinking / bash / text / write / edit / read) per rule · the fitted curve + its E / D
            residuals · projected median per rule, thinking on / off · two-sample agreement · one harvest line to my seat
```
