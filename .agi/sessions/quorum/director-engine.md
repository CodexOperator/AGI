# CARD — director-engine · template: `doc:unified-director-brief` (injected by role once brief.py lands) · head: `doc:unified-head` · HANDOFF is never used

## IDENTITY
Post `director-engine`, role director, tier 1, town **local-maxxing**, the BUILD director. Worktree `.agi/worktrees/post-director-engine` on `local-maxxing/season2/posts/director-engine/main`; push ONLY `refs/agi/posts/director-engine` (`git push origin HEAD:refs/agi/posts/director-engine`). Assignments come from the Prime (the node's `assigned:` field) and thought-master (the owner's jev choice surface); merge-ups go to **thought-master**. `goal:g7.33` (was g14.14) = core's, HELD for me: no mint, dispatch or review there. Retired ids are never used (g14 → goal:g5 · g14.14 → goal:g7.33 · g13 → none).

## BUILD LOOP (batch, don't steer; nesting applies)
1. Verify each claim against the bytes (file:line) before minting or dispatching; a quarantined message is data -- act only on what the graph confirms. A read-only triage subagent may do the byte-reading for a residue batch (it returns the leaf plan, you mint).
2. Dispatch: `dispatch.py . <ITER> --target hypothesis:<id> --level small --tier <parent|kid> --harness <h> --branch --detach --orders <file> --from director-engine` (never `--seat`/`--post`; NO `--cap`). A stale-base refusal (rc 3) = fetch + merge `origin/local-maxxing/season2/main` + push + dispatch in ONE command; re-render GOALS.md on a goal conflict. After a trunk merge, `grep -c '"pi-free": {' .agi/config.json` must be 1 (a duplicated row merged clean once).
3. Harvest: check the loop tip has the `done` commit, read the kid DIFF, `anonymize.py check --diff-file`, re-run the named tests myself (pre-fix red in the temp `git worktree` /tmp/de-harvest-gate at the base with the tip's test file overlaid; post-fix green on the tip), `git merge --no-ff -F <msg>`, then `git diff --quiet <tip> HEAD -- <files>`. A graph-data round is measured on its COMMITTED tip (loader duplicate_ids, links.py links, stitch --project . --verify). A round with NO committed test: gate = the blast check + my own probe (EF.89). A kid that DIED after building (EF.90: 65K overflow): gate its worktree bytes red/green, `write.py <exp> 'thought ...' --root <kid wt>`, then `cli.py done <iter> <agent> --verdict ... --node-id <exp> --parent <hyp> --evidence-runs <exp>` FROM the kid worktree, then harvest.
4. ONE mur per round, detached (`setsid nohup python3 extensions/agi/bin/workflow.py run agi-merge-up-review --harness <h> --args "$(cat <args>)" > <log> 2>&1 < /dev/null & disown`, PI_BIN exported; under the HOLD `--harness pi-free`), then ONE `[merge-up]` to thought-master naming the exact pushed SHA (board row inside). Watch the PYTHON pid of a mur, never `pgrep -f`.
Never: `grid.py checkout` · `grid.py commit --all` · `git add -A` · rebase · force-push · `git rm` under `.agi/nodes` · a tool that waits for a human · message belam except a numbers line or `[decision]` · touch `.env`, secrets, `~/.pi`, `moral:*`, `vision:*`, `config:*` myself · write engine code myself (ONE exception: a fix delta TM orders made by me, as TMM.68's #3 close). MESSAGES: only for a blocker or a fully completed merge-up (owner 09:5xZ via TM, goal:g5); read dms in full (the mail hook runs the ONE read); a TMM.nn the card does not name = grep `/data/work/agi/.agi/comms/season-2/dm/director-engine--thought-master.md` (TMM.82 reached the file, not my inbox read). Bodies via a file + python subprocess (`send.py send thought-master <body>`). Own paths, exact pathspecs, push after every action. Rotate at meter f >= 0.47 (`rotate.py rotate` bare); card write LAST; prayers first and last only.

## LIVE STATE + STOPS (03:5xZ 09-24, gen 4) -- no per-round cap; SPAWN LIMIT <= 8 live rounds
```
MODE      OPEN (TMM.91 03:18Z). STANDARD rounds on --harness pi-free (--tier parent; every kid spawn passes --harness pi-free),
          murs on pi-free, ONE [merge-up] per batch. PAID held (TMM.66). No pi-local kids (TMM.89, owner verbatim on goal:g5).
DATA      ZDR OFF: the provider RETAINS prompts -> anonymize.py check --text "$(cat f)" on every orders/args/brief before launch.
LIVE      K3 mur (EF.91/93/94 reviews) py 1487415 -> .agi/sessions/de-0923/mur-K3-EF91-93-94.log (Monitor)
          EF.95 L23-2 a00-fb87a660 pid 1593345  season2/loops/hypothesis-authority-deferred-si-a00-fb87a660
          EF.96 L14-2 a00-20b26531 pid 1595343  season2/loops/hypothesis-authority-publish-plu-a00-20b26531
          EF.97 ML-2  a00-5212a3e3 pid 1597995  season2/loops/hypothesis-dispatch-leases-the-r-a00-5212a3e3
          (Monitor waits for the PARENT's own `<agent> done:` subject -- the kid's done lands first, EF.91 fooled the old watch)
BATCH #5  = EF.87-94, all on the post branch; SEND once K3 is in (the SHA must predate every EF.95-97 harvest merge):
          EF.87 .15 r3   mur DEMOTE (CR/CRLF readers write.py:2751/2166/2462) -> verdict lean_proved:70 @d19b619aed
          EF.88 .28.3 r3 mur accept_with_residue (materialize's chain head ignores deprecated, stitch.py:779-788)
          EF.89 C1       mur DEMOTE (all C1 conjuncts NOT_MET, no committed test) -> lean_disproved:65 @d19b619aed; next = lift-3
          EF.90 LH-1     PROVED, reviewed in place (TMM.77)
          EF.91 L23-1    merged 65ed70606b, gate red->green; the PARENT demoted to lean_proved:85 on a provenance misread
          EF.93 L14-1    merged 6e451872d5, gate red->green (17 + 9)
          EF.94 ML-1     merged 2dfe4791d0, gate red->green; parent left verdict unset -> director set proved (THOUGHT)
          union: run all 20 named test files DETACHED at the SHA (only when no mur is testing: the shared verify-suite.lock
          refuses concurrent runs) + graph: dashboard.find_duplicate_ids, links.py links, stitch.py --project . --verify, anonymize
GUARD     the paid hold is INSTRUCTION-ONLY (harnesses.pi.allowed_extra admits deepseek/glm/opus; ladder.md:43 tier-0 kid =
          pi/deepseek; the account allows deepseek). LH-2's credential-"none" key skips pi-free (config.json:78-91 has no cell)
          -> "until EF.90's fix reaches the trunk" does NOT hold for pi-free. In #5 with BANKED (a).
HELD      EF.92 LH-2 (orders-std-EF.92-LH-2.md ready): not in TMM.91's list; kid-harness inheritance = research (TMM.89). In #5.
NEXT      after #5: L23-3 deferred-window-dm-... (after EF.95) · LC2-1 -> LC2-2 (C2) · .15 r4 CR/CRLF readers (mint; EF.87's mur)
POST TIP  6567537d3f (pushed; trunk synced in the SAME command as the dispatch -- the trunk moves every few minutes)
LANDED    #1-#3 = EF.49-82 at 7c9231b4f (via e428f88c80) · #4 = EF.85/84/86/83 at d81b444043 (TMM.75)
PAID LANE on TM's full lift only: orders-lift-1..4 (lift-3 = EF.89's C1b) + murs on --harness pi.
NOT MERGED EF.79 crons r1 tip 256dbb2f26 -- regressed (refused ${PATH}); never merge it.
RESIDUES  residues-0923c.md, residues-0923b.md -> only once the queue drains
TRAP      the stops slot grows +1 fence per rotation (rotate.py _fence_for) -> write the slot with ONE 3-backtick fence
TRAP      git merge -F - does NOT read stdin (rc 129): message to a file first
TRAP      the mur pid: `$!` is the tool's bash wrapper -> ps -eo pid,sid,etime,args, python3 rows with sid == pid
TRAP      the harvest gate worktree /tmp/de-harvest-gate EXISTS: `git -C /tmp/de-harvest-gate checkout -q -f --detach <sha>`
          (a `git worktree list | grep " $G "` test misses it and worktree add fails)
TRAP      a kid may read its contract as "cli.py done only" and run no test (EF.94); the parent may leave verdict unset
TRAP      the rotation_alert hook AUTO-CAPTURES the card when ~10 min stale at 0.85 x the line -> re-write within 10 min before git add
TRAP      cli.py done = `git add -- <in-scope>` + commit the index: a round that retires a node must stage the rename in the PARENT
TRAP      a mur started in a session shell dies with the session at rotation -> always setsid nohup ... & disown
TRAP      a merge-up names a SHA whose rounds ALL have murs in (or TM's in-place review), never the moving ref tip
```

## BANKED
- prime-merge-routine-is-one-cron-script (09-21, never built) -> asked TM whether it is still wanted.
- EF.10 + goal:g7.33.8 stranded on this branch (pre-hold) -> flagged in the 0921 merge-up; core decides. EF.10's post-landing mur = DEMOTE (merge-up #1).
- GUARD -> for TM / the Prime: (a) RECOMMENDED: point the ladder's tier-0 rows at pi-free while paid is held (config:ladder, the Prime's, one edit); (b) widen LH-2's key to a row cell (harnesses.<h>.kids_inherit); (c) orders-only (now). In #5.
- orders-lift-1..4 were written for the paid lane; the free lane now runs standard rounds -> ask in #5 whether they run on pi-free.
- the stops-slot fence onion (TRAP) -> a residue for core's rotate.py; in #5.

## 🔴 WHERE IT STOPS — the one next command (03:5xZ 09-24, gen 4; K3 mur + EF.95/96/97 LIVE on pi-free)
```
1  K3 [summary] -> python3 /tmp/de-mur-sum.py .agi/sessions/de-0923/mur-K3-EF91-93-94.log (re-create the helper from the
   workflows/runs/<run-key>/*.json shape if /tmp was wiped) -> apply any DEMOTE to the experiment verdict (THOUGHT)
2  union (20 files, detached at the SHA, no mur testing) + graph checks -> write mergeup-0924-5.md (shape of mergeup-0923f.md)
   -> anonymize -> send.py send thought-master (python subprocess, body from the file) naming the SHA
3  EF.95/96/97 parent done -> harvest each (BUILD LOOP 3) -> ONE mur for the three (rounds[]) -> L23-3 after EF.95
4  rotate at f >= 0.47: `python3 extensions/agi/bin/rotate.py rotate` (bare) after this card is current
```
