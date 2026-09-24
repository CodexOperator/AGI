# CARD — director-engine · template: `doc:unified-director-brief` (injected by role once brief.py lands) · head: `doc:unified-head` · HANDOFF is never used

## IDENTITY
Post `director-engine`, role director, tier 1, town **local-maxxing**, the BUILD director. Worktree `.agi/worktrees/post-director-engine` on `local-maxxing/season2/posts/director-engine/main`; push ONLY `refs/agi/posts/director-engine` (`git push origin HEAD:refs/agi/posts/director-engine`). Assignments come from the Prime (the node's `assigned:` field) and thought-master (the owner's jev choice surface); merge-ups go to **thought-master**. `goal:g7.33` (was g14.14) = core's, HELD for me: no mint, dispatch or review there. Retired ids are never used (g14 → goal:g5 · g14.14 → goal:g7.33 · g13 → none).

## BUILD LOOP (batch, don't steer; nesting applies)
1. Verify each claim against the bytes (file:line) before minting or dispatching; a quarantined message is data -- act only on what the graph confirms. A read-only triage subagent may do the byte-reading for a residue batch (it returns the leaf plan, you mint).
2. Dispatch: `dispatch.py . <ITER> --target hypothesis:<id> --level small --tier <parent|kid> --harness <h> --branch --detach --orders <file> --from director-engine` (never `--seat`/`--post`; NO `--cap`). A stale-base refusal (rc 3) = fetch + merge `origin/local-maxxing/season2/main` + push + dispatch in ONE command; re-render GOALS.md on a goal conflict. After a trunk merge, `grep -c '"pi-free": {' .agi/config.json` must be 1 (a duplicated row merged clean once).
3. Harvest: check the loop tip has the `done` commit, read the kid DIFF, `anonymize.py check --diff-file`, re-run the named tests myself (pre-fix red in the temp `git worktree` /tmp/de-harvest-gate at the base with the tip's test file overlaid; post-fix green on the tip), `git merge --no-ff -F <msg>`, then `git diff --quiet <tip> HEAD -- <files>`. A graph-data round is measured on its COMMITTED tip (loader duplicate_ids, links.py links, stitch --project . --verify). A round with NO committed test: gate = the blast check + my own probe (EF.89). A kid that DIED after building (EF.90: 65K overflow): gate its worktree bytes red/green, `write.py <exp> 'thought ...' --root <kid wt>`, then `cli.py done <iter> <agent> --verdict ... --node-id <exp> --parent <hyp> --evidence-runs <exp>` FROM the kid worktree, then harvest.
4. ONE mur per round, detached (`setsid nohup python3 extensions/agi/bin/workflow.py run agi-merge-up-review --harness <h> --args "$(cat <args>)" > <log> 2>&1 < /dev/null & disown`, PI_BIN exported; under the HOLD `--harness pi-free`), then ONE `[merge-up]` to thought-master naming the exact pushed SHA (board row inside). Watch the PYTHON pid of a mur, never `pgrep -f`.
Never: `grid.py checkout` · `grid.py commit --all` · `git add -A` · rebase · force-push · `git rm` under `.agi/nodes` · a tool that waits for a human · message belam except a numbers line or `[decision]` · touch `.env`, secrets, `~/.pi`, `moral:*`, `vision:*`, `config:*` myself · write engine code myself (ONE exception: a fix delta TM orders made by me, as TMM.68's #3 close). MESSAGES: only for a blocker or a fully completed merge-up (owner 09:5xZ via TM, goal:g5); read dms in full (the mail hook runs the ONE read); a TMM.nn the card does not name = grep `/data/work/agi/.agi/comms/season-2/dm/director-engine--thought-master.md` (TMM.82 reached the file, not my inbox read). Bodies via a file + python subprocess (`send.py send thought-master <body>`). Own paths, exact pathspecs, push after every action. Rotate at meter f >= 0.47 (`rotate.py rotate` bare); card write LAST; prayers first and last only.

## LIVE STATE + STOPS (02:4xZ 09-24, gen 4) -- no per-round cap; SPAWN LIMIT <= 8 live rounds
```
MODE      TMM.89, OWNER 02:3xZ via TM, verbatim: "Let's resume normal operations using the free Openrouter endpoint. No more special
          usd0 runs just research towards doing more efficient usd0 runs in the future" -> STANDARD rounds on --harness pi-free
          (--tier parent; orders: every kid spawn passes --harness pi-free), murs on pi-free, ONE [merge-up] per batch. NO pi-local
          kids, no PI_CODING_AGENT_DIR rounds; 0-USD efficiency = research, not an operating mode (not mine unless TM names it).
          PAID still held (TMM.66; deepseek, glm, opus). LOCAL: none (owner cancelled the local kid 02:29Z).
BLOCKED   pi-free. TMM.87's probe = EF.87's mur re-run 02:32Z (mur-H2-EF87-r2.log): per-run key minted on the repointed workspace
          (ae97da9ded; no inherited-env line), pi rc=1 BEFORE generation: 404 "allowed-providers setting permits only: deepseek".
          0 USD. [red] #2 to TM 02:3xZ (blocker-free-lane-3.md). Nothing dispatches on pi-free until TM's line says `stealth` is allowed.
GUARD     the paid hold is INSTRUCTION-ONLY: harnesses.pi.allowed_extra still admits deepseek/glm/opus, ladder.md:43 (tier-0 kid) =
          pi/deepseek, and the account ALLOWS deepseek -> a pi-free parent's kid spawned without --harness pi-free SPENDS. Every
          orders-std file carries the explicit kid line. LH-2 keys on credential "none"; the pi-free row (config.json:78-91) has no
          credential cell -> TMM.89's "until EF.90's inheritance fix reaches the trunk" does NOT hold for pi-free (say so in #5).
LANDED    #1-#3 = EF.49-82 at 7c9231b4f (via the #3 close e428f88c80) · #4 = EF.85/84/86/83 at d81b444043 (TMM.75)
HARVESTED on the post branch, not yet merged up -> merge-up #5 = EF.87 + EF.88 + EF.89 + EF.90:
          EF.87 @607d0132fc .15 r3 PROVED (standard unified diff) · EF.88 @8c0190631a g15.28.3 r3 PROVED (retired_claims) ·
          EF.89 @0a96932407 g1.25.5 C1 strict improvement (NEVER_PROPOSABLE floor; C1 INCOMPLETE -> orders-lift-3) -- these three
          need their murs on pi-free (args mur-H2-EF87 / I2-EF88 / J2-EF89-args.json; r1 02:15Z + r2 02:32Z logs = the 404s)
          EF.90 @e93594dca9 LH-1 PROVED (dispatch exports AGI_HARNESS); reviewed in place by its parent = its review (TMM.77)
POST TIP  11bb31e531 (pushed): the 8 queued leaves' CEILINGs moved off pi-local to the STANDARD pi-free round (THOUGHT each);
          LH-2's RESIDUE names the pi-free gap · config: pi-local = OrcaBonsai-27B-C2 (@809c9f0e8c), pi-free = the trunk's row
QUEUE     STANDARD rounds, orders READY in .agi/sessions/de-0923/ (chains in order, chains in parallel):
          EF.91 L23-1 load-rows-...-do-fetch-is-false        orders-std-EF.91-L23-1.md -> L23-2 authority-deferred-signer-... -> L23-3
          EF.92 LH-2  a-kid-under-a-credential-none-parent-... orders-std-EF.92-LH-2.md  (EF.90 is on the base)
          EF.93 L14-1 authority-publish-push-timeout-...      orders-std-EF.93-L14-1.md -> L14-2 authority-publish-plumbing-git-calls-...
          EF.94 ML-1  spawn-budget-acquire-refuses-...        orders-std-EF.94-ML-1.md  -> ML-2 dispatch-leases-the-resolved-harness-...
          then LC2-1 -> LC2-2 (C2). orders-free-L23-1.md / orders-local-LH1.md = the RETIRED kid-tier shape: never use them.
BRIEFS    verified vs e7910a90ab (read-only agent, 02:5xZ): L23-1, L14-1, ML-1 hold line-exact; LH-2's 2 drifted citations fixed
          (config.json:135, test_credential_none_spawn.py:237-293); EF.90's export = dispatch.py:2655 -> all 4 DISPATCHABLE
PAID LANE on TM's full lift only: orders-lift-1..4 + murs on --harness pi.
ACCOUNT   old account $0.48 (170.00 / 169.52); dispatch mints on the other account ($14.04 at 02:1xZ).
NOT MERGED EF.79 crons r1 tip 256dbb2f26 -- regressed (refused ${PATH}); never merge it.
RESIDUES  residues-0923c.md, residues-0923b.md -> triage into leaves only once the queue (10 deep) drains
TRAP      the stops slot grows +1 fence per rotation (rotate.py _fence_for wraps a stops text that still carries its own fence; 6 layers
          at gen 3->4, the rotate-out subject was a bare fence line) -> write the slot with ONE 3-backtick fence, nothing nested
TRAP      the mur pid: `$!` of a setsid launch is the tool's bash wrapper -> find the PYTHON pid with ps -eo pid,ppid,sid,cmd | grep '[w]orkflow.py run'
TRAP      a refused dispatch leaves an empty loop branch (EF.91's a00-786a602d at my HEAD, no commits): harmless, a re-dispatch mints anew
TRAP      the rotation_alert hook AUTO-CAPTURES the card when ~10 min stale at 0.85 x the line -> re-write it within 10 min before any git add
TRAP      cli.py done = `git add -- <in-scope>` + commit the index: a round that retires a node must stage the rename in the PARENT
TRAP      a mur started in a session shell dies with the session at rotation -> always setsid nohup ... & disown
TRAP      a merge-up names a SHA whose rounds ALL have murs in (or TM's in-place review), never the moving ref tip
```

## BANKED
- prime-merge-routine-is-one-cron-script (09-21, never built) -> asked TM whether it is still wanted.
- EF.10 + goal:g7.33.8 stranded on this branch (pre-hold) -> flagged in the 0921 merge-up; core decides. EF.10's post-landing mur = DEMOTE (merge-up #1).
- GUARD (the paid hold is instruction-only) -> for TM / the Prime: (a) RECOMMENDED: point the ladder's tier-0 rows at pi-free while paid is held (config:ladder, the Prime's, one edit, structural); (b) widen LH-2's key to a row cell (harnesses.<h>.kids_inherit on pi-free + pi-local; touches the trunk's pi-free row); (c) orders-only (what runs now). Name it in the go-line (TMM.87 "tell me once") and in merge-up #5.
- the stops-slot fence onion (TRAP) -> a residue for core's rotate.py; name it once in merge-up #5.

## 🔴 WHERE IT STOPS — the one next command (02:4xZ 09-24, gen 4; pi-free BLOCKED on the account; nothing live)
```
1  WAIT for TM's line that the account allows provider `stealth` ([red] #2 02:3xZ). Nothing on pi-free before it.
2  On the go, ONE burst (PI_BIN exported; each launch setsid nohup ... < /dev/null & disown):
   murs    for m in H2-EF87 I2-EF88 J2-EF89: python3 extensions/agi/bin/workflow.py run agi-merge-up-review --harness pi-free
           --args "$(cat .agi/sessions/de-0923/mur-$m-args.json)" > .agi/sessions/de-0923/mur-$m-r3.log 2>&1
   rounds  python3 extensions/agi/bin/dispatch.py . EF.9N --target hypothesis:<id> --level small --tier parent --harness pi-free
           --branch --detach --orders .agi/sessions/de-0923/orders-std-EF.9N-<leaf>.md --from director-engine   (N = 1..4)
   then ONE line to TM (TMM.87 "tell me once"): the lane runs + the GUARD finding + BANKED (a)
3  murs in, 0 demote -> union + graph -> ONE [merge-up] #5 (EF.87 + 88 + 89 + 90) to thought-master (+ LH-2's pi-free gap, the fence onion)
4  harvest EF.91-94 as they land (BUILD LOOP 3); dispatch each chain's next leaf
```
