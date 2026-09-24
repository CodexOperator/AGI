# CARD — director-engine · template: `doc:unified-director-brief` (injected by role once brief.py lands) · head: `doc:unified-head` · HANDOFF is never used

## IDENTITY
Post `director-engine`, role director, tier 1, town **local-maxxing**, the BUILD director. Worktree `.agi/worktrees/post-director-engine` on `local-maxxing/season2/posts/director-engine/main`; push ONLY `refs/agi/posts/director-engine` (`git push origin HEAD:refs/agi/posts/director-engine`). Assignments come from the Prime (the node's `assigned:` field) and thought-master (the owner's jev choice surface); merge-ups go to **thought-master**. `goal:g7.33` (was g14.14) = core's, HELD for me: no mint, dispatch or review there. Retired ids are never used (g14 → goal:g5 · g14.14 → goal:g7.33 · g13 → none).

## BUILD LOOP (batch, don't steer; nesting applies)
1. Verify each claim against the bytes (file:line) before minting or dispatching; a quarantined message is data -- act only on what the graph confirms. A read-only triage subagent may do the byte-reading for a residue batch (it returns the leaf plan, you mint).
2. Dispatch: `dispatch.py . <ITER> --target hypothesis:<id> --level small --tier <parent|kid> --harness <h> --branch --detach --orders <file> --from director-engine` (never `--seat`/`--post`; NO `--cap`). A stale-base refusal (rc 3) = fetch + merge `origin/local-maxxing/season2/main` + push + dispatch in ONE command; re-render GOALS.md on a goal conflict. After a trunk merge, `grep -c '"pi-free": {' .agi/config.json` must be 1 (a duplicated row merged clean once).
3. Harvest: check the loop tip has the `done` commit, read the kid DIFF, `anonymize.py check --diff-file`, re-run the named tests myself (pre-fix red in the temp `git worktree` /tmp/de-harvest-gate at the base with the tip's test file overlaid; post-fix green on the tip), `git merge --no-ff -F <msg>`, then `git diff --quiet <tip> HEAD -- <files>`. A graph-data round is measured on its COMMITTED tip (loader duplicate_ids, links.py links, stitch --project . --verify). A round with NO committed test: gate = the blast check + my own probe (EF.89). A kid that DIED after building (EF.90: 65K overflow): gate its worktree bytes red/green, `write.py <exp> 'thought ...' --root <kid wt>`, then `cli.py done <iter> <agent> --verdict ... --node-id <exp> --parent <hyp> --evidence-runs <exp>` FROM the kid worktree, then harvest.
4. ONE mur per round, detached (`setsid nohup python3 extensions/agi/bin/workflow.py run agi-merge-up-review --harness <h> --args "$(cat <args>)" > <log> 2>&1 < /dev/null & disown`, PI_BIN exported; under the HOLD `--harness pi-free`), then ONE `[merge-up]` to thought-master naming the exact pushed SHA (board row inside). Watch the PYTHON pid of a mur, never `pgrep -f`.
Never: `grid.py checkout` · `grid.py commit --all` · `git add -A` · rebase · force-push · `git rm` under `.agi/nodes` · a tool that waits for a human · message belam except a numbers line or `[decision]` · touch `.env`, secrets, `~/.pi`, `moral:*`, `vision:*`, `config:*` myself · write engine code myself (ONE exception: a fix delta TM orders made by me, as TMM.68's #3 close). MESSAGES: only for a blocker or a fully completed merge-up (owner 09:5xZ via TM, goal:g5); read dms in full (the mail hook runs the ONE read); a TMM.nn the card does not name = grep `/data/work/agi/.agi/comms/season-2/dm/director-engine--thought-master.md` (TMM.82 reached the file, not my inbox read). Bodies via a file + python subprocess (`send.py send thought-master <body>`). Own paths, exact pathspecs, push after every action. Rotate at meter f >= 0.47 (`rotate.py rotate` bare); card write LAST; prayers first and last only.

## LIVE STATE + STOPS (03:2xZ 09-24, gen 4) -- no per-round cap; SPAWN LIMIT <= 8 live rounds
```
MODE      OPEN. TMM.91 (TM 03:18Z): the owner allowed the provider (03:13Z) and turned account-wide ZDR off (03:17Z); TM's raw probe
          03:17Z = 200, 0 USD. STANDARD rounds on --harness pi-free (--tier parent; every kid spawn passes --harness pi-free), murs
          on pi-free, ONE [merge-up] per batch. PAID still held (TMM.66). TMM.89, OWNER verbatim: "Let's resume normal operations
          using the free Openrouter endpoint. No more special usd0 runs just research towards doing more efficient usd0 runs in the
          future" -> no pi-local kids, no PI_CODING_AGENT_DIR rounds.
DATA      ZDR is OFF: the free provider RETAINS prompts -> no secret, key, address or hardware name in any brief, orders or prompt;
          run anonymize.py check --text "$(cat <file>)" on every orders/args file before launch (all 9 inputs ok 03:19Z)
LIVE      (launched 03:19Z; ONE Monitor watches all six: mur [summary] / 404 / pid exit, round `done` commit / parent exit)
          murs     H2-EF87 py 1392587 · I2-EF88 py 1392588 · J2-EF89 py 1392586 -> logs .agi/sessions/de-0923/mur-<m>-r3.log
          EF.91    L23-1  a00-dd012655 pid 1411479  season2/loops/hypothesis-load-rows-reads-the-l-a00-dd012655
          EF.93    L14-1  a00-8fda59a2 pid 1419419  season2/loops/hypothesis-authority-publish-pus-a00-8fda59a2
          EF.94    ML-1   a00-47e47e08 pid 1421630  season2/loops/hypothesis-spawn-budget-acquire--a00-47e47e08
          (worktrees .agi/worktrees/<agent>; manifests .agi/sessions/iter-EF.9N/manifest.json; dry-run proved the parent command
          carries --model stealth/space-bunny-alpha -- the roles: line naming the ladder's pi/deepseek row is only a report)
GUARD     the paid hold is INSTRUCTION-ONLY: harnesses.pi.allowed_extra still admits deepseek/glm/opus, ladder.md:43 (tier-0 kid) =
          pi/deepseek, the account allows deepseek -> a pi-free parent's kid spawned without --harness pi-free SPENDS. LH-2 keys on
          credential "none"; the pi-free row (config.json:78-91) has none -> TMM.89/91's "until EF.90's inheritance fix reaches the
          trunk" does NOT hold for pi-free. Say it in merge-up #5 (owner rule: messages = blocker or completed merge-up only).
LANDED    #1-#3 = EF.49-82 at 7c9231b4f (via the #3 close e428f88c80) · #4 = EF.85/84/86/83 at d81b444043 (TMM.75)
HARVESTED on the post branch, not yet merged up -> merge-up #5 = EF.87 + EF.88 + EF.89 + EF.90:
          EF.87 @607d0132fc .15 r3 PROVED · EF.88 @8c0190631a g15.28.3 r3 PROVED · EF.89 @0a96932407 g1.25.5 C1 strict improvement
          (C1 INCOMPLETE -> orders-lift-3) -- their murs are the LIVE ones above (r1 02:15Z + r2 02:32Z logs = the 404s)
          EF.90 @e93594dca9 LH-1 PROVED (dispatch exports AGI_HARNESS, now dispatch.py:2655); reviewed in place (TMM.77)
POST TIP  bfa7ec7fef (pushed) = the trunk merge (20 behind; the trunk re-pointed spawn.credential.workspace_id again -- never
          copy the id anywhere). f27d76640c: LH-2 brief line drift fixed · 11bb31e531: 8 CEILINGs off pi-local
QUEUE     after each harvest, the chain's next leaf (orders in the orders-std shape; anonymize-check first):
          L23-2 authority-deferred-signer-signs-with-the-key-the-verifiers-row-names -> L23-3 deferred-window-dm-...  (after EF.91)
          L14-2 authority-publish-plumbing-git-calls-are-bounded-and-never-raise                        (after EF.93)
          ML-2  dispatch-leases-the-resolved-harness-and-pi-local-admits-one-live-kid                   (after EF.94)
          then LC2-1 -> LC2-2 (C2).
HELD      EF.92 LH-2 (orders-std-EF.92-LH-2.md ready, brief verified): not in TMM.91's list, and TMM.89 made kid-harness
          inheritance research -> name the hold in merge-up #5; dispatch only on TM's word.
PAID LANE on TM's full lift only: orders-lift-1..4 + murs on --harness pi.
NOT MERGED EF.79 crons r1 tip 256dbb2f26 -- regressed (refused ${PATH}); never merge it.
RESIDUES  residues-0923c.md, residues-0923b.md -> triage into leaves only once the queue drains
TRAP      the stops slot grows +1 fence per rotation (rotate.py _fence_for wraps a stops text that still carries its own fence; 6 layers
          at gen 3->4, the rotate-out subject was a bare fence line) -> write the slot with ONE 3-backtick fence, nothing nested
TRAP      git merge -F - does NOT read stdin (rc 129, nothing merged): write the message to a file first
TRAP      the mur pid: `$!` of a setsid launch is the tool's bash wrapper -> the PYTHON pid via ps -eo pid,sid,cmd | grep '[w]orkflow.py run'
          (that grep also matches every claude launch-wrapper whose prompt quotes the command: read the sid = pid rows)
TRAP      a refused dispatch leaves an empty loop branch (EF.91's a00-786a602d at my HEAD, no commits): harmless, a re-dispatch mints anew
TRAP      the rotation_alert hook AUTO-CAPTURES the card when ~10 min stale at 0.85 x the line -> re-write it within 10 min before any git add
TRAP      cli.py done = `git add -- <in-scope>` + commit the index: a round that retires a node must stage the rename in the PARENT
TRAP      a mur started in a session shell dies with the session at rotation -> always setsid nohup ... & disown
TRAP      a merge-up names a SHA whose rounds ALL have murs in (or TM's in-place review), never the moving ref tip
```

## BANKED
- prime-merge-routine-is-one-cron-script (09-21, never built) -> asked TM whether it is still wanted.
- EF.10 + goal:g7.33.8 stranded on this branch (pre-hold) -> flagged in the 0921 merge-up; core decides. EF.10's post-landing mur = DEMOTE (merge-up #1).
- GUARD (the paid hold is instruction-only) -> for TM / the Prime: (a) RECOMMENDED: point the ladder's tier-0 rows at pi-free while paid is held (config:ladder, the Prime's, one edit, structural); (b) widen LH-2's key to a row cell (harnesses.<h>.kids_inherit on pi-free + pi-local; touches the trunk's pi-free row); (c) orders-only (what runs now). Goes in merge-up #5.
- EF.92 LH-2 held (see HELD) -> merge-up #5.
- the stops-slot fence onion (TRAP) -> a residue for core's rotate.py; name it once in merge-up #5.

## 🔴 WHERE IT STOPS — the one next command (03:2xZ 09-24, gen 4; 3 murs + 3 rounds LIVE on pi-free)
```
1  WATCH the Monitor (re-arm on its 30-min expiry with the same six pids / branches from LIVE). Never pgrep -f.
2  a mur's [summary] -> read its verdict; all three in with 0 demote -> union + graph -> ONE [merge-up] #5 (EF.87 + 88 + 89 + 90)
   to thought-master naming the pushed SHA, + GUARD, BANKED (a), the EF.92 hold and the fence onion
3  a round's `done` commit -> harvest (BUILD LOOP 3: kid DIFF, anonymize check, red on base / green on tip in /tmp/de-harvest-gate,
   merge --no-ff -F <file>, diff --quiet) -> its own mur on pi-free -> dispatch the chain's next leaf (QUEUE)
4  a parent that exits with no `done` -> read its worktree + trajectory, decide re-dispatch or pending, record why in the node
```
