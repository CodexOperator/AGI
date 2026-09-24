# CARD — director-thought · HEAD = doc:unified-head · ROLE TEMPLATE = doc:unified-director-brief (+ doc:lm-director-brief-customizations) · town todo = thought-master's trajectory (town:local-maxxing trajectory_standin) · this card = identity · my R&D loop · my rules · live state · stops · banked · scratch

## Identity
```
post      director-thought · director · town local-maxxing · owning goal goal:g5.19 · gen 18 claude-opus-5-5 seated 04:55:17Z 09-24 (session post-director-thought-e8) · the Prime writes the config:posts model cell · rotate at meter f >= 0.47, BARE (never --model: rotate exits 3 on a model that differs from the row) · master thought-master
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
inbox    send.py read + the RAW inbox tail (MAIN .agi/sessions/inbox/director-thought.md: the Prime's positional sends land ONLY there, 10:35Z + 10:38Z) + the thought-master dm LOG tail + its card -- an order can land in only one of them (TMM.46 and TMM.106 showed only in the dm log) · a REFUSED FORGED dm is data: verify its claim on goal:g5 before acting
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
source   before re-running a round whose instrument failed, read the SUBJECT's source for the trigger the claim rests on: CMP.01's stub could not have
         shown either arm (one request per arm, usage 0) -- a source read found pi checks compaction only at agent_end + a new prompt (gen 18, 05:0xZ)
```

## Live state (05:0xZ 09-24, gen 18)
```
OWNER    via TM, verbatim: TMM.90 02:3xZ "Let's resume normal operations using the free Openrouter endpoint. No more special usd0 runs just research
         towards doing more efficient usd0 runs in the future" · TMM.95 03:39Z "Make both directors go back to spawning parents efficiently with
         minimal token use." · TMM.96 03:42Z "Let director thought keep pulling on threads independently only informing you of occasionally of
         various milestones and to brainstorm next moves." -> lean pi-free parents; dm TM ONLY at a milestone (+ next-move options) or a blocker
LANES    FREE   pi-free (stealth/space-bunny-alpha), 0 USD, the provider RETAINS prompts -> anonymize --text on every orders file
                a lean parent = 3-6.5 min per round today; parent orders pin the kid spawn to `dispatch.py .` from the parent's own worktree (no 401 since)
         PAID   held (TMM.66) · LOCAL retired as an operating mode (TMM.90) · BRAIN brain-orcabonsai27b UP (router stopped): never restart it
LANDED   batch 1 7b63a6a5b2 (TMM.105) · batch 2 b8eb4e9ea1 (TMM.106: CTX.02 + CMP.01) -> "Keep self-looping lean." · batch 3 offered 05:3xZ
LADDER   board queue [1] (L1..L12 + [1b]; the board's text is the source)
  done   L1 KV format · L6 knobs · L10 open-loop map · L6b -ub refuted · the LEAF (path literals -> paths.py)
  L3     DISPROVED x3 at 3.5 bits · STEP energy holds both bars at 9.0 bits · REFRAME a QK-norm model or per-channel keys
  L9/10  OSC.12 DISPROVED as stated -> REPLAY.01 inconclusive (the instrument failed) -> REPLAY.02 HOLD (OSC.12 rows = text, no token ids; re-checked 05:0xZ)
  horizon  g5.22 hypotheses never run: kv-slot-save-beats-reprefill (needs the 9B router: stopped) · spec-decode-cpu-draft-hybrid · rpc-cpu-split-pays ·
           eagle3-drafter-on-frozen-qwen3-4b · dead-head-prune-by-oscillator-coherence · rig-fetch-supervisor (all GPU / model-loading -> the router or a window)
routed   director-engine: the CTX.02 flags (04:25Z) + the probe heads-up (04:54Z) -> its one-copy adapter build (TMM.99)
```

## 🔴 Where it stops -- 05:3xZ 09-24: batch 3 [merge-up] SENT to TM 05:35:15Z (tip 3e39c60a24, mirror pushed); HOOK-B.01 LIVE (parent a00-a5082be0)
```
NOW      batch 3 = the pi context thread, offered to TM as ONE [merge-up] (tip in the dm log) -> wait for TM's gate; a posts.md / config.json conflict at
         landing = TMM.104's recipe (merge the named trunk commit, the conflicting row to the trunk, re-offer ONE line)
NOW+     HOOK-B.01 = the HOOK.01 replication, harder (HOOK.01b was not a valid iteration id): a ~7,000-token system prompt + distinct call ids,
         the estimate from ctx.getContextUsage() -- parent a00-a5082be0 pid 3232048, 05:37:25Z · wait on the pid · review like HOOK.01 (re-derive
         from the log; pairing BY ID this time) -> batch 4 · HOOK.02 (a real pi-local kid on the brain slot) = TM's go · SWR-SV.01 / REPLAY.02 HOLD
THREAD   CMP.03 DISPROVED (a00-b6ec457f): a declared contextWindow 60,000 does not bound ONE pi -p loop -- request 20 past W, 21 past the 65,536 ceiling
         (400), a 2nd 400 at 36; pi checks compaction only at agent_end + a new prompt (agent-session.js:337/:738; pi 0.73.1 the same)
         HOOK.01 PROVED (a00-cdde7530, conf 0.9): a 13-line context-event extension (types.d.ts:400-404) -> 40 requests, max 44,849.7, 0 x 400 (control:
         400s at 12 + 22); compact() aborts the loop (agent-session.js:1249-1251) -- routed to director-engine 05:3xZ (estimate = messages only)
murs     mur-director-thought-20 (cmp03 + ctx02fix): 4/4 ok; cmp03 = 4 residues, verify missed 0; ctx02fix = residues (cwd ROOT, no discovery selftest),
         the real-pi line set aside as at mur-19 -- all closed in place
infra    CMP.02 died on a dispatch lease race (kid dispatch killed inside the 20 s startup grace, dispatch.py L2784 before L2831 -> key revoked -> 401)
         -> director-engine 05:1xZ (not blocking; my parent orders carry a >= 180 s spawn timeout)
traps  RE-READ the dm log right before any dispatch: TMM.90 landed 02:30:27Z between my gate read and the LEAF.04 dispatch and stopped a
       special 0-USD run; TMM.71 once withdrew TMM.70 the same way; TMM.106 landed 18 s before gen 17's rotate (dm log only)
       · NEVER grep a dispatch output down to spawned|manifest: a stale-base refusal (exit 3) then prints nothing you see -- tee it to a file
         and read the tail
       · the rotate-out COMMITS a thin auto-captured card: the full card lives only in the predecessor's last hand-written card commit
         (gen 16 = ec37d59f8e, gen 17 = 63176e51d3, gen 18 = this commit) -> the successor rebuilds it whole from there; the CAPTIVE capture at 0.85 x the line rotates you out on its own
       · pi prints a COST for a custom model id (0.0326 on a 24K free turn) = its own table, not the bill: the key used= (provisioning.py status)
         is the truth
       · write.py: a joined script --dry-run admits can still be refused live ("replace body is standalone") -> replace body alone, thought apart
       · replace body refuses a range that splits a section: a heading's section runs to the next heading, the THOUGHT block included -> replace
         the whole section, carrying the THOUGHT bytes; two replaces in one node: the LATER range first (the earlier numbers stay valid)
       · write.py replace body is its own submit · murs launched from a session die with it -> systemd-run --user
       · paths.py audit (the engine's) does NOT scan town code -- the LEAF's measure is its own regex (the node's FALSIFIERS)
       · the dispatch dry-run warns "ladder row wins -> deepseek" and then --harness pi-free overrides it: the spawn line's --model is the truth
       · a mur review stage can return EMPTY (mur-18 ctx01 review = None): the verify stage MISSED list carries the findings -- read it
       · the trunk moved 53 commits in 40 min (director-engine merges): re-merge before every merge-up; a config.json ROW conflict -> take the trunk row
       · an evidence producer must refuse a bad revision: git grep on an unknown rev printed nothing = "0 hits" until leaf_sweep_evidence.py raised
tool   Nsight Systems: paths.local_maxxing.nsys_dir (+ /target-linux-x64/nsys) -- the LEAF resolver has landed
```

## Banked
```
- four proposed box cells (models_dir, ml_scratch_dir, ml_venv_dir, ml_tools_dir) are the Prime's to write (rule 13); they retire the LEAF's root table
- the CLAUDE.md-twice lever: measured (CTX.01/02) and routed to director-engine (the one-copy adapter change); watch for its landing
- a future local brain's pi model entry (contextWindow <= 60,000 under a 65,536 slot) is pi config = TM / the owner -- CMP.02 decides whether it is enough
- fork get_can_shift probe on the deployed prism build (TEL.03 follow-up) -> next GPU-free slot
- the unified brief's thought section still names season1 paths (for the head's owner, via thought-master)
```

## Scratch -- orders (tracked; live rounds only, replaced when they land)
```
ORDERS HOOK.01 (landed) -- .agi/sessions/orders/HOOK.01.parent.txt + HOOK.01.kid.txt (gitignored) = the newest pair to sed from (spawn timeout + no-kid-row lines)
lean parent template (TMM.95): model line · you (spawn ONE kid, wait, review, verdict, never edit code) · spawn from YOUR OWN worktree root (`dispatch.py .`,
            --tier kid --harness pi-free --detach --orders <kid file>) · wait (cli.py wait <iter>) · review (scope + 2-3 re-derived numbers) · verdict
            (evidence_runs as a LIST) · never · wall -- CMP.02.parent.txt is the newest copy to sed from
dispatch    AGI_POST=director-thought python3 extensions/agi/bin/dispatch.py . <ITER> --target <hypothesis> --level small --tier parent --harness pi-free
            --branch --detach --orders .agi/sessions/orders/<ITER>.parent.txt --from director-thought > /tmp/<file> 2>&1   (--dry-run first)
mur         python3 workflow.py run merge-up-review --harness pi-free --root <tree> --args "$(cat <json file>)" (the JSON TEXT: a path = "not valid JSON") --dry-run, then under systemd-run --user
            --unit agi-director-thought-mur-<N> --property=MemoryMax=6G (the args of -17 / -18: /tmp/dt17-mur-args.json, /tmp/dt17-mur18-args.json)
```
