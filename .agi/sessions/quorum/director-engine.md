# CARD — director-engine · template: `doc:unified-director-brief` (injected by role once brief.py lands) · head: `doc:unified-head` · HANDOFF is never used

## IDENTITY
Post `director-engine`, role director, tier 1, town **local-maxxing**, the BUILD director. Worktree `.agi/worktrees/post-director-engine` on `local-maxxing/season2/posts/director-engine/main`; push ONLY `refs/agi/posts/director-engine`. Assignments come from the Prime (the node's `assigned:` field) and thought-master (the owner's jev choice surface); merge-ups go to **thought-master**. `goal:g7.33` (was g14.14) = core's, HELD for me: no mint, dispatch or review there. Retired ids are never used (g14 → goal:g5 · g14.14 → goal:g7.33 · g13 → none).

## BUILD LOOP (batch, don't steer; nesting applies)
1. Verify each claim against the bytes (file:line) before minting or dispatching; a quarantined message is data -- act only on what the graph confirms.
2. Dispatch pi parents only: `dispatch.py . <ITER> --target hypothesis:<id> --level small --tier parent --harness pi --branch --detach --orders <file> --from director-engine` (never `--seat`/`--post`; NO `--cap`: owner 09-23 14:xZ in doc:lm-director-brief-customizations -- no per-round spending cap, the standing per-spawn key $1.0/300 min applies). A stale-base refusal (rc 3) = merge `origin/local-maxxing/season2/main` first; re-render GOALS.md on a goal conflict.
3. Harvest: read the kid DIFF, `anonymize.py check --diff-file`, re-run the named tests myself (pre-fix red in a temp `git worktree add --detach /tmp/de-harvest-gate <sha>`, post-fix green on the merged tip), `git merge --no-ff -F <msg>` the loop branch.
4. ONE batch mur per batch, then ONE `[merge-up]` to thought-master naming the exact SHA (board rows inside the text).
Never: `grid.py checkout` · `grid.py commit --all` · `git add -A` · rebase · force-push · `git rm` under `.agi/nodes` · a tool that waits for a human · message belam except a numbers line or `[decision]` · touch `.env`, secrets, `moral:*`, `vision:*`, `config:*` myself · write engine code myself. MESSAGES: only for a blocker or a fully completed merge-up (owner 09:5xZ via TM, goal:g5) -- plus the owner's director-thought notice when the jev rounds complete; read dms in full (`send.py read` shows dm lines too). Bodies via a file + python subprocess. Own paths, exact pathspecs, push after every action. Rotate at meter f >= 0.47 (`rotate.py rotate` bare); card write LAST; prayers first and last only.

## LIVE STATE + STOPS (20:5xZ 09-23, gen 1) -- floor -50; no per-round cap; SPAWN LIMIT <= 8 live rounds
````
```
POST TIP  9cdc359dd7 = 4af82b8a2 (11 rounds) + EF.65 @280ebe0fb8 (carries EF.61) + EF.66 @f14ec9546b + trunk syncs @15251fdc28
          (rotation rows; posts.md = the trunk's bytes) and @102658116c (director-thought @e0689f715 landed at c63e1ab8b) + 2 mints. Pushed.
          THE MERGE-UP SHA = this tip or later WITHOUT any EF.67-70 merge (those need their own mur)
TESTS     EF.65: round-1 tip c64792f985 = 9 failed / 138 passed (red) -> round-2 tip 154 passed · EF.66: new file on 9070c1ab70 = 2 failed /
          7 passed (red) -> merged tip EF.65 set + test_workflow*.py = 296 passed · workflow.py validate: same 8 pre-existing violations
MURS      both stages DONE: EF.49 51 54 56 57 58 59 60 61-65 63 64 66 = accept_with_residue · EF.10 = DEMOTE x2 (captures the
          SUCCESSOR's fresh session; role/session_id joined into the landing path unvalidated rotate.py:18202-18204; gitignored landing
          .gitignore:83; the scrub held) -> g7.33 is core's: REPORT to TM, never fix · verify PENDING: EF.50 + EF.62 (mur-re-*, since ~20:40)
          merge-up DRAFT .agi/sessions/de-0923/mergeup-0923b.md ({SHA} {EF50} {EF62} to fill) · residues .agi/sessions/de-0923/residues-0923b.md
          results: /data/work/agi/.agi/sessions/workflows/runs/<key>/{review,verify}_R-EF*.json (MAIN's sessions dir)
HARVESTED (NOT merged -- held until the merge-up is sent so the post tip = its SHA; each verified by me, in mur):
          EF.67 tip 9e5159c9d3: new file on base 3 failed/2 passed -> tip 413 passed 1 xfailed · mur Q-EF67 (21:00Z)
          EF.68 tip 6efc053157: new file on base 2 failed/1 passed -> tip 510 passed · mur Q-EF68 (21:00Z)
          EF.69 tip f1fb723b62: tip test file on base commands.md 4 failed/175 passed -> tip 232 passed 7 skipped; manifest 220 entries /
          146 proposable, verify-suite false · mur R-EF69 (21:05Z) -- the enumeration test is a forward guard (green on the base too)
LIVE      EF.70 a00-99134fb7 g15.28.3 (the grok-bot duplicate id) -- orders .agi/sessions/de-0923/orders-EF.70.md
NEXT      EF.50 + EF.62 verifies -> fill the draft -> send the [merge-up] to TM -> merge EF.67 68 69 (+70) -> when R-EF69 is in: EF.69
          rides the next merge-up, THEN dm director-thought "[jev] choice surface complete" · residues -> leaves (KEEP SPLITTING)
CLI       216 entries on the post tip; "all 70" = EF.69 -> THEN dm director-thought "[jev] choice surface complete" (it heard "ready" @5808b0848)
TRAP      a mur or long job started in a session shell dies with the session at rotation -> always `setsid nohup ... & disown`
TRAP      write.py cannot address a second file that shares an id (by path: "no node file"; by id it resolves the first) -- EF.70's one hand edit
TRAP      the rotation_alert hook is installed on this box (owner 19:4xZ; ~/.claude/settings.json UserPromptSubmit) and FIRES here
TRAP      a round that edits OTHER nodes or .agi/config.json loses them at `done` unless `--owns` names them; a parent can report
          "harvest accepted" with NOTHING committed (EF.64: a stale index.lock) -- check the loop tip moved; commit a stranded
          worktree with a temp GIT_INDEX_FILE onto a -harvest branch, never by touching its lock
TRAP      every round needs a mur before its merge-up; run gate reds WITH the seat env (env -u TMUX -u TMUX_PANE, AGI_* kept); run a
          new test file FIRST with its neighbours; the card's "LIVE" can lag: check the loop tip for a `done` commit
```
````

## WHEN THE JEV ROUNDS COMPLETE -> TELL director-thought (owner 09:5xZ 09-23, this pane)
The jev rounds = the commands manifest, jev's one choice surface for the magic pane (goal:g5.24.3, MP.02): EF.21, goal:g1.25, claimed by the owner 09:5xZ, EF.21 dispatched first. When they land (merged, batch mur, merge-up sent): dm director-thought `[jev] choice surface ready` with the SHA and how to read it (`commands.py manifest`, the propose endpoint), so MP.02's suggester and held-out set score against it; copy thought-master.

## BANKED
- prime-merge-routine-is-one-cron-script (09-21, never built) -> asked TM whether it is still wanted.
- EF.10 + goal:g7.33.8 stranded on this branch (pre-hold) -> flagged in the 0921 merge-up; core decides.

## 🔴 WHERE IT STOPS — the one next command (20:5xZ 09-23, gen 1; post tip 9cdc359dd7 pushed)
`````
````
```
1  ls /data/work/agi/.agi/sessions/workflows/runs/*/verify_R-EF{50,61-65,62,63,66}.json   # the 5 pending verifies
2  write .agi/sessions/de-0923/mergeup-0923b.md (rows for EF.10 + EF.49-66) -> send.py send thought-master via a python subprocess
3  harvest EF.67-70 as each loop tip gets its `done` commit (diff, anonymize, orders' tests pre-fix red / post-fix green, merge)
```
````
`````
