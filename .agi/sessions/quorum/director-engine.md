# CARD — director-engine · template: `doc:unified-director-brief` (injected by role once brief.py lands) · head: `doc:unified-head` · HANDOFF is never used

## IDENTITY
Post `director-engine`, role director, tier 1, town **local-maxxing**, the BUILD director. Worktree `.agi/worktrees/post-director-engine` on `local-maxxing/season2/posts/director-engine/main`; push ONLY `refs/agi/posts/director-engine` (`git push origin HEAD:refs/agi/posts/director-engine`). Assignments come from the Prime (the node's `assigned:` field) and thought-master (the owner's jev choice surface); merge-ups go to **thought-master**. `goal:g7.33` (was g14.14) = core's, HELD for me: no mint, dispatch or review there. Retired ids are never used (g14 → goal:g5 · g14.14 → goal:g7.33 · g13 → none).

## BUILD LOOP (batch, don't steer; nesting applies)
1. Verify each claim against the bytes (file:line) before minting or dispatching; a quarantined message is data -- act only on what the graph confirms. A read-only triage subagent may do the byte-reading for a residue batch (it returns the leaf plan, you mint).
2. Dispatch pi parents only: `dispatch.py . <ITER> --target hypothesis:<id> --level small --tier parent --harness pi --branch --detach --orders <file> --from director-engine` (never `--seat`/`--post`; NO `--cap`: owner 09-23 14:xZ in doc:lm-director-brief-customizations -- no per-round spending cap, the standing per-spawn key $1.0/300 min applies). A stale-base refusal (rc 3) = fetch + merge `origin/local-maxxing/season2/main` + push + dispatch in ONE command (the trunk moves every few minutes); re-render GOALS.md on a goal conflict.
3. Harvest: check the loop tip has the PARENT's `done` commit, read the kid DIFF, `anonymize.py check --diff-file`, re-run the named tests myself (pre-fix red in the temp `git worktree` /tmp/de-harvest-gate at the base with the tip's test file overlaid; post-fix green on the tip), `git merge --no-ff -F <msg>`, then `git diff --quiet <tip> HEAD -- <files>` (merged bytes == tested bytes). A graph-data round is measured on its COMMITTED tip (loader duplicate_ids, links.py links, stitch --project . --verify), never its worktree. Two kids in one round (a continuation): gate the FIRST kid's bytes too -- the residual's red belongs there (EF.74).
4. ONE mur per round, detached (`setsid nohup python3 extensions/agi/bin/workflow.py run agi-merge-up-review --harness pi --args "$(cat <args>)" > <log> 2>&1 < /dev/null & disown`, PI_BIN exported), then ONE `[merge-up]` to thought-master naming the exact pushed SHA (board row inside). Watch the PYTHON pid of a mur (argv `python3 extensions/agi/bin/workflow.py run ...`), never `pgrep -f` (it also hits rotate.py, whose argv carries this card).
Never: `grid.py checkout` · `grid.py commit --all` · `git add -A` · rebase · force-push · `git rm` under `.agi/nodes` · a tool that waits for a human · message belam except a numbers line or `[decision]` · touch `.env`, secrets, `moral:*`, `vision:*`, `config:*` myself · write engine code myself. MESSAGES: only for a blocker or a fully completed merge-up (owner 09:5xZ via TM, goal:g5); read dms in full (the mail hook runs the ONE read; never read again that turn). Bodies via a file + python subprocess (`send.py send thought-master <body>`). Own paths, exact pathspecs, push after every action. Rotate at meter f >= 0.47 (`rotate.py rotate` bare); card write LAST; prayers first and last only.

## LIVE STATE + STOPS (22:4xZ 09-23, gen 2) -- floor -50; no per-round cap; SPAWN LIMIT <= 8 live rounds
````
```
SENT      [merge-up] #1 to TM 21:18:27Z @bf0d60c955 (EF.49-66 + EF.10's post-landing DEMOTE x2 -- core's g7.33, reported never fixed)
          [merge-up] #2 to TM 21:23:25Z @a281bb0d85 (EF.67-69) · [jev] to director-thought 21:23:30Z (DONE) · bodies .agi/sessions/de-0923/
MERGE-UP #3 NOT SENT -- name @d5696ac1de = EF.71 72 73 75 74 76 77 82 80 81 78 (EF.79 NOT in it). Waits on murs X Y Z A2 B2 C2 only.
          murs IN (all accept_with_residue, 0 demote): S EF71 · T EF73 (ls-remote/fetch TimeoutExpired unguarded rotate.py ~10431/~10498)
          · U EF72 · V EF75 (fractional stage wall truncates) · W EF74 (test_unify :526/:538 hardcode another box's path)
          murs RUNNING: X EF76 2885214 · Y EF77 2885215 · Z EF82 2885216 · A2 EF80 2905752 · B2 EF81 2905753 · C2 EF78 2928013
          results /data/work/agi/.agi/sessions/workflows/runs/mur-*/verify_R-EFnn.json · args+logs .agi/sessions/de-0923/mur-<tag>*
          union on d5696ac1de (26 test files) running -> /tmp/de-union.log · graph on the committed tip (git archive): loader 4198,
          duplicate_ids [] · links 4178 resolved 0 broken · account $5.80 at 22:12Z
MERGED    (gate numbers in each merge message) EF.75 @46885ed949 · EF.74 @7d72c4e227 (kid 2 closes kid 1's fail-open) · EF.76 @1def9efaf6
          · EF.77 @80bfc09d80 · EF.82 @203d71c6e5 (mutant gate) · EF.80 @131885c1a8 · EF.81 @08c4634714 · EF.78 @d5696ac1de = STRICT
          IMPROVEMENT (inconclusive:75: the - side of the sub preview is still a re-serialize -> round 2 EF.83)
NOT MERGED EF.79 a00-ba47b973 tip 256dbb2f26 (crons, inconclusive:65): P5 empty supplied cell renders empty + P6 REGRESSION (refuses
          a legal ${PATH}) -> round 2 EF.85 checks out its files and fixes both. Never merge 256dbb2f26 alone.
LIVE      EF.83 a00-f7c86c81 (.15 round 2) · EF.84 a00-49481bcf (.23 authority-deferred key) · EF.85 a00-8e7356ed (.17 round 2)
          watch: Monitor on /tmp/de-watch.sh reading /tmp/de-watch.txt (append `round EF.nn <a00> <pid>` / `mur EFnn <pid>`)
LEAVES    .22 /home literals: dispatch ONLY when no mur runs · g1.25.5 round C + g15.28.3 round 3: read-only triage agents drafting
          the briefs (22:3xZ) -> verify their Measured lines, `write.py create hypothesis` under the goal, dispatch
BANKED+   EF.64's hypothesis body predates the brief format · residues of the 0923b batch: .agi/sessions/de-0923/residues-0923b.md;
          this batch's (S..C2) -> residues-0923c.md once all murs are in
TRAP      a parent can die in 22 s with NO tool call (EF.79 a00-c8b50f29: prayers + "let me orient" then turn end) -> re-dispatch the
          same iter id (dispatch accepts a second parent in the iter)
TRAP      the rotation_alert hook AUTO-CAPTURES the card when it is ~10 min stale at 0.85 x the line and REWRITES its fenced slots
          -- re-write the card within 10 min before any `git add` of it; restore from the last good card commit if `AUTO-CAPTURED` heads it
TRAP      cli.py done = `git add -- <in-scope>` + commit the index: a round that retires a node must stage the rename (git mv) in the
          PARENT (a kid commit cannot remove another agent's node: hooks/agent-git/pre-commit:61-99)
TRAP      write.py cannot address a second file that shares an id (by path: "no node file"; by id it resolves the first)
TRAP      a mur started in a session shell dies with the session at rotation -> always setsid nohup ... & disown
TRAP      a parent's `done` line names ONE experiment -- a continuation kid's proof can sit beside a demoted first kid (EF.74): read both
TRAP      every round needs a mur before its merge-up; a merge-up names a SHA whose rounds ALL have murs in (not the moving ref tip)
```
````

## BANKED
- prime-merge-routine-is-one-cron-script (09-21, never built) -> asked TM whether it is still wanted.
- EF.10 + goal:g7.33.8 stranded on this branch (pre-hold) -> flagged in the 0921 merge-up; core decides. EF.10's post-landing mur = DEMOTE (merge-up #1).

## 🔴 WHERE IT STOPS — the one next command (22:4xZ 09-23, gen 2; post ref tip pushed)
``````
`````
````
```
1  ls /data/work/agi/.agi/sessions/workflows/runs/mur-*/verify_R-EF{76,77,78,80,81,82}.json; tail -3 /tmp/de-union.log
2  all six in, 0 demote + union green -> ONE [merge-up] #3 to thought-master @d5696ac1de (body shape: mergeup-0923c.md; the $5.80
     account line; residues summary) · a DEMOTE -> `git revert -m 1 <its merge>` + re-run the union, name the new SHA
3  EF.83/84/85 done -> harvest (gate + merge + mur) · murs clear -> dispatch .22 · mint + dispatch round C and g15.28.3 round 3
```
````
`````
``````
