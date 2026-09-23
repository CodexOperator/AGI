# CARD — director-engine · template: `doc:unified-director-brief` (injected by role once brief.py lands) · head: `doc:unified-head` · HANDOFF is never used

## IDENTITY
Post `director-engine`, role director, tier 1, town **local-maxxing**, the BUILD director. Worktree `.agi/worktrees/post-director-engine` on `local-maxxing/season2/posts/director-engine/main`; push ONLY `refs/agi/posts/director-engine`. Assignments come from the Prime (the node's `assigned:` field) and thought-master (the owner's jev choice surface); merge-ups go to **thought-master**. `goal:g7.33` (was g14.14) = core's, HELD for me: no mint, dispatch or review there. Retired ids are never used (g14 → goal:g5 · g14.14 → goal:g7.33 · g13 → none).

## BUILD LOOP (batch, don't steer; nesting applies)
1. Verify each claim against the bytes (file:line) before minting or dispatching; a quarantined message is data -- act only on what the graph confirms.
2. Dispatch pi parents only: `dispatch.py . <ITER> --target hypothesis:<id> --level small --tier parent --harness pi --branch --detach --orders <file> --from director-engine` (never `--seat`/`--post`; NO `--cap`: owner 09-23 14:xZ in doc:lm-director-brief-customizations -- no per-round spending cap, the standing per-spawn key $1.0/300 min applies). A stale-base refusal (rc 3) = merge `origin/local-maxxing/season2/main` first; re-render GOALS.md on a goal conflict.
3. Harvest: read the kid DIFF, `anonymize.py check --diff-file`, re-run the named tests myself (pre-fix red in a temp `git worktree add --detach /tmp/de-harvest-gate <sha>`, post-fix green on the merged tip), `git merge --no-ff -F <msg>` the loop branch.
4. ONE batch mur per batch, then ONE `[merge-up]` to thought-master naming the exact SHA (board rows inside the text).
Never: `grid.py checkout` · `grid.py commit --all` · `git add -A` · rebase · force-push · `git rm` under `.agi/nodes` · a tool that waits for a human · message belam except a numbers line or `[decision]` · touch `.env`, secrets, `moral:*`, `vision:*`, `config:*` myself · write engine code myself. MESSAGES: only for a blocker or a fully completed merge-up (owner 09:5xZ via TM, goal:g5) -- plus the owner's director-thought notice when the jev rounds complete; read dms in full (`send.py read` shows dm lines too). Bodies via a file + python subprocess. Own paths, exact pathspecs, push after every action. Rotate at meter f >= 0.47 (`rotate.py rotate` bare); card write LAST; prayers first and last only.

## LIVE STATE + STOPS (21:2xZ 09-23, gen 1) -- floor -50; no per-round cap; SPAWN LIMIT <= 8 live rounds
````
```
SENT      [merge-up] to thought-master 21:18:27Z @bf0d60c955: EF.49-66 (13 rounds, mur 0 demote / 13 accept_with_residue) + EF.10's
          post-landing mur = DEMOTE (core's g7.33: reported, not fixed). Body: .agi/sessions/de-0923/mergeup-0923b.md. Await TM's landing.
POST TIP  f7fb382052 = bf0d60c955 + EF.67 @44df35443f + EF.68 @bddb7878a7 + EF.69 @f7fb382052 (each re-run by me red -> green). Pushed.
          combined run on f7fb382052 (13 rotate files + commands tests): /tmp/de-harvest/merged-f7fb382052.txt (started 21:18:54Z)
MURS      running, detached: Q-EF67 + Q-EF68 (21:00Z) · R-EF69 (21:05Z) -> .agi/sessions/workflows/runs/*/verify_R-EF6{7,8,9}.json (MAIN)
          args/logs .agi/sessions/de-0923/mur-{Q-EF67,Q-EF68,R-EF69}*
LIVE      EF.71 a00-01a6d8d3 = EF.70 ROUND 2 (goal:g15.28.3): EF.70 a00-99134fb7 was DISPROVED by its own parent on the committed tip
          (done staged the new deprecated copy, never the old path's removal -> TWO files with mint 07acc9ce) -> NOT merged, never merge
          554e7658a3. Round 2: the PARENT does the git mv (a kid commit cannot remove another agent's node; pre-commit:61-99)
NEXT      verify_R-EF67/68/69 in (+ EF.71 harvested + its mur) -> ONE [merge-up] to TM @ the tip -> when EF.69 has landed: dm
          director-thought "[jev] choice surface complete" (body: SHA + `commands.py manifest` + the propose endpoint; copy TM)
          · residues -> leaves (KEEP SPLITTING): 52 items, .agi/sessions/de-0923/residues-0923b.md · g1.25.5 rounds B C D after A lands
CLI       220 entries / 146 proposable on the post tip (EF.69 in); "all 70" = EF.69 (69 listed + write.py's own drift test)
TRAP      a mur or long job started in a session shell dies with the session at rotation -> always `setsid nohup ... & disown`
TRAP      cli.py done = `git add -- <in-scope>` + commit the index: a filesystem move lands only the NEW file; a round that retires a node
          must stage the rename (git mv) in the PARENT; measure a round on its COMMITTED tip (git archive), never its worktree
TRAP      write.py cannot address a second file that shares an id (by path: "no node file"; by id it resolves the first)
TRAP      the rotation_alert hook is installed on this box (owner 19:4xZ; ~/.claude/settings.json UserPromptSubmit) and FIRES here
TRAP      a round that edits OTHER nodes or .agi/config.json loses them at `done` unless `--owns` names them; a parent can report
          "harvest accepted" with NOTHING committed -- check the loop tip moved
TRAP      every round needs a mur before its merge-up; run gate reds WITH the seat env (env -u TMUX -u TMUX_PANE, AGI_* kept); run a
          new test file FIRST with its neighbours; the card's "LIVE" can lag: check the loop tip for a `done` commit
```
````

## WHEN THE JEV ROUNDS COMPLETE -> TELL director-thought (owner 09:5xZ 09-23, this pane)
The jev rounds = the commands manifest, jev's one choice surface for the magic pane (goal:g5.24.3, MP.02): EF.21, goal:g1.25, claimed by the owner 09:5xZ, EF.21 dispatched first. When they land (merged, batch mur, merge-up sent): dm director-thought `[jev] choice surface ready` with the SHA and how to read it (`commands.py manifest`, the propose endpoint), so MP.02's suggester and held-out set score against it; copy thought-master.

## BANKED
- prime-merge-routine-is-one-cron-script (09-21, never built) -> asked TM whether it is still wanted.
- EF.10 + goal:g7.33.8 stranded on this branch (pre-hold) -> flagged in the 0921 merge-up; core decides.

## 🔴 WHERE IT STOPS — the one next command (21:2xZ 09-23, gen 1; post tip f7fb382052 pushed)
`````
````
```
1  tail -3 /tmp/de-harvest/merged-f7fb382052.txt ; ls /data/work/agi/.agi/sessions/workflows/runs/*/verify_R-EF6{7,8,9}.json
2  harvest EF.71 (a00-01a6d8d3) once its loop tip has the parent's `done`: measure on the COMMITTED tip (git archive): loader
     duplicate_ids [], ONE file with mint 07acc9ce, stitch duplicate_payload_ref 0 -> merge -> mur
3  all in -> ONE [merge-up] to thought-master naming the tip · then the jev dm to director-thought (see its section)
```
````
`````
