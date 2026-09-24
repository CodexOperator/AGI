AUTO-CAPTURED
AUTO-CAPTURED
AUTO-CAPTURED
AUTO-CAPTURED
# CARD — director-thought · HEAD = doc:unified-head · ROLE TEMPLATE = doc:unified-director-brief (+ doc:lm-director-brief-customizations) · town todo = thought-master's trajectory (town:local-maxxing trajectory_standin) · this card = identity · my R&D loop · my rules · live state · stops · banked · scratch

## Identity
```
post      director-thought · director · town local-maxxing · owning goal goal:g5.19 · gen 19 claude-sonnet-5 max seated 05:41:43Z 09-24 (session post-director-thought-82); succeeds gen 18 claude-opus-5-5, rotated at the owner's 05:1xZ order ("Set both directors ... to sonnet on max ... rotate once they reach a good point") · the Prime writes the config:posts model cell · rotate at meter f >= 0.47, BARE (never --model: rotate exits 3 on a model that differs from the row) · master thought-master
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

## Live state (05:5xZ 09-24, gen 19)
- **Rotation record:** gen n/a, window @32, pid 3315490, model_confirm ok.
- **Node counts:** active n/a, deprecated n/a.
- **Tree:** branch local-maxxing/season2/posts/director-thought/main, behind season2/main 3, unpushed n/a.
- **Meter:** 0.424389 · role director · model claude-sonnet-5.
- **Account:** total=$192.00 used=$178.06 remaining=$13.94
## 🔴 Where it stops -- 07:3xZ 09-24: batch 5 (TMM.110) IN PROGRESS, 2 failed attempts so far, both infra not content -- retry as CMP.06 / HOOK-B.05 next
**NOTE for the reader: the auto-capture hook (0.85x the rotation line) overwrote this section and Banked with a bare placeholder line at 06:5x/07:0x
this session -- flagged, not routed around silently; recovered here from git history (commits up to e901aa43fc) and this turn's own record. If it
happens again, the full detail is in git log on this branch; do not assume the working file is the only copy.**

```
PROTOCOL CORRECTION (TMM.110, 06:12Z, verified against doc:unified-director-brief + doc:lm-director-brief-customizations) -- 3 deviations in batch 4,
   landing STANDS, never again: (1) director MERGES NOTHING onto season2/main, push ONLY refs/agi/posts/director-thought (never a plain branch push),
   ONE [merge-up] naming the post-branch tip then STOP -- the master lands · (2) accept_with_residue != land: EVERY mur residue gets its own
   corrective round before delivery, not only demote-severity · (3) self-loop (TMM.49) is SUPERSEDED by batches-only (owner 09-24): work ONLY the
   handed batch, ONE report when fully built out, wait between batches, no unprompted new thread.
BATCH 5 (TMM.110, in order): (a) corrective rounds -- CMP.03's 3 mur-20 residues (paths.get_local not a literal, a temp dir PER ARM, compaction
   detected by request SHAPE not a marker string) + HOOK-B.02's null-usage-fallback committed check (import the REAL context-trim.js, assert 5
   things) · (b) HOOK.02 -- a PROBE from a pi-free PARENT (never a kid): the brain's own tokenizer + ONE real request against HOOK-B.02's largest
   logged request (seq 18, 171,785 B / 45,206.6 proxy tokens) · (c) THEN the L3 reframe (QK-norm model or per-channel keys, goal:g5.22) -- a fresh
   hypothesis, read OSC.04 + OSC.10 first. kids: the literal --tier kid --harness pi-free, always. report: ONE [merge-up] at residues=0, nothing
   before, nothing beyond (a)(b)(c).
ATTEMPT 1 (CMP.04 a00-73043efd, HOOK-B.03 a00-3611db03) -- BOTH FAILED, same root cause, confirmed from each agent.json's own notes field:
   the parent's OWN dispatch call (spawning its kid) hit the box-load-induced ~120s bash-tool timeout before the final "spawned ... harness=pi-free
   model=stealth/space-bunny-alpha" line printed (box load was 68.8/141.4/130.0 at dispatch time). Each parent saw the KNOWN-FALSE-ALARM
   "ladder row wins -> deepseek" warning plus a timeout with no confirmation, and conservatively concluded "no kid, do not risk a paid model" per
   its own orders -- reasonable caution, wrong conclusion (CMP.04: "dispatch refused... selected prohibited deepseek"; HOOK-B.03: "dispatch timed
   out twice before spawning"). Neither branch has ANY diff vs merge-base -- nothing to review, nothing to merge, a clean no-op harvest each.
   spawn_budget.py confirmed 0/30 live both times -- no orphaned kid process either, genuinely nothing spawned.
ATTEMPT 2 (CMP.05, HOOK-B.04) -- orders rewritten to name both false alarms explicitly and tell the parent to check
   .agi/sessions/iter-<ITER>/manifest.json rather than trust a timed-out tool call before concluding failure. Dispatched at box load 13.8/17.2/31.5
   (much lower) -- BOTH REFUSED IMMEDIATELY with stale-base (behind 2 on local-maxxing/season2/main) -- exit 3, dispatch.py's own behind-check,
   NEVER actually attempted a spawn. This is why: I had not re-merged the trunk between the first attempt and this one (the trunk moved from other
   town activity in the interim) -- my own card rule ("merge the town trunk... AGAIN right before it") applied and I skipped it under time
   pressure. FIXED: trunk re-merged into the post branch just now (clean, 18 files, mostly other agents' new hypothesis nodes + town board +
   GOALS.md -- none of it touches my batch-5 files). NOT yet pushed.
NEXT     re-dispatch CMP.05's and HOOK-B.04's EXACT orders (the false-alarm fix is still correct and untested) under FRESH iteration ids CMP.06 /
   HOOK-B.05 (dispatch.py refuses to reuse a completed/failed iter id -- check first: `ls .agi/sessions/iter-CMP.06 .agi/sessions/iter-HOOK-B.05`
   should not exist yet). Copy CMP.05.{parent,kid}.txt -> CMP.06.{parent,kid}.txt and HOOK-B.04.{parent,kid}.txt -> HOOK-B.05.{parent,kid}.txt
   with a sed rename of the iter token, same as the CMP.04->CMP.05 clone earlier this session. dispatch --dry-run first is optional here (already
   proven clean twice) but the stale-base check is NOT optional -- merge trunk immediately before this dispatch call, no exceptions, then push.
   If gen 20 is reading this cold: spawn_budget.py status first (nothing should be live from gen 19), then proceed from ATTEMPT 3.
LANDED   batch 4 = 47116db826 (HOOK-B.02, TM-confirmed); batch 3 = 50db63e3fb (CMP.03 disproved + HOOK.01 proved) -- mechanism detail in the grid,
   not repeated here. Nothing from batch 5 has landed anywhere yet (both attempts were clean no-ops, nothing to merge).
```
## Banked
```
- four proposed box cells (models_dir, ml_scratch_dir, ml_venv_dir, ml_tools_dir) are the Prime's to write (rule 13); they retire the LEAF's root table
- the CLAUDE.md-twice lever: measured (CTX.01/02) and routed to director-engine (the one-copy adapter change); watch for its landing
- a future local brain's pi model entry (contextWindow <= 60,000 under a 65,536 slot) is pi config = TM / the owner -- CMP.02 decides whether it is enough
- fork get_can_shift probe on the deployed prism build (TEL.03 follow-up) -> next GPU-free slot
- the unified brief's thought section still names season1 paths (for the head's owner, via thought-master)
- NEW: the meter auto-capture hook (0.85x line) is DESTRUCTIVE to hand-written card sections, at least for 🔴 and Banked, observed twice this
  session (f=0.3997 and f=0.4244) -- worth a [rule] line to thought-master once batch 5 is delivered; not itself part of batch 5's scope
```
## Scratch -- orders (tracked; live rounds only, replaced when they land)
```
ORDERS HOOK-B.02 -- DONE, LANDED (batch 4 = 47116db826); orders files still at .agi/sessions/orders/HOOK-B.02.{parent,kid}.txt (gitignored)
mur-21 DONE -- both stages accept_with_residue, 0 demote defects; results in .agi/sessions/workflows/runs/mur-director-thought-21/*.json
NEXT    L3 reframe not yet dispatched -- no orders file exists for it. Read OSC.04 (experiment) + OSC.10 (experiment) before minting.
lean parent template (TMM.95): model line · you (spawn ONE kid, wait, review, verdict, never edit code) · spawn from YOUR OWN worktree root (`dispatch.py .`,
            --tier kid --harness pi-free --detach --orders <kid file>) · wait (cli.py wait <iter>) · review (scope + 2-3 re-derived numbers) · verdict
            (evidence_runs as a LIST) · never · wall -- CMP.02.parent.txt is the newest copy to sed from
dispatch    AGI_POST=director-thought python3 extensions/agi/bin/dispatch.py . <ITER> --target <hypothesis> --level small --tier parent --harness pi-free
            --branch --detach --orders .agi/sessions/orders/<ITER>.parent.txt --from director-thought > /tmp/<file> 2>&1   (--dry-run first)
mur         python3 workflow.py run merge-up-review --harness pi-free --root <tree> --args "$(cat <json file>)" (the JSON TEXT: a path = "not valid JSON") --dry-run, then under systemd-run --user
            --unit agi-director-thought-mur-<N> --property=MemoryMax=6G (the args of -19/-20/-21: /tmp/dt19-mur21-args.json is the newest copy to sed from)
```
