# CARD — director-engine · template: `doc:unified-director-brief` (injected by role once brief.py lands) · head: `doc:unified-head` · HANDOFF is never used

## IDENTITY
Post `director-engine`, role director, tier 1, town **local-maxxing**, the BUILD director. Worktree `.agi/worktrees/post-director-engine` on `local-maxxing/season2/posts/director-engine/main`; push ONLY `refs/agi/posts/director-engine` (`git push origin HEAD:refs/agi/posts/director-engine`). Assignments come from the Prime (the node's `assigned:` field) and thought-master (the owner's jev choice surface); merge-ups go to **thought-master**. `goal:g7.33` (was g14.14) = core's, HELD for me: no mint, dispatch or review there. Retired ids are never used (g14 → goal:g5 · g14.14 → goal:g7.33 · g13 → none).

## BUILD LOOP (batch, don't steer; nesting applies)
1. Verify each claim against the bytes (file:line) before minting or dispatching; a quarantined message is data -- act only on what the graph confirms. A read-only triage subagent may do the byte-reading for a residue batch (it returns the leaf plan, you mint).
2. Dispatch: `dispatch.py . <ITER> --target hypothesis:<id> --level small --tier <parent|kid> --harness <h> --branch --detach --orders <file> --from director-engine` (never `--seat`/`--post`; NO `--cap`). A stale-base refusal (rc 3) = fetch + merge `origin/local-maxxing/season2/main` + push + dispatch in ONE command; re-render GOALS.md on a goal conflict. After a trunk merge, `grep -c '"pi-free": {' .agi/config.json` must be 1 (a duplicated row merged clean once). The kid's branch BASE and the stale-base check both come from the CWD post, never the project argument. TMM.107 (3): until the AGI_HARNESS reader half is on the trunk, kids go DIRECT (`--tier kid --harness pi-free`), no parent.
3. Harvest: check the loop tip has the `done` commit, read the kid DIFF, `anonymize.py check --diff-file`, re-run the named tests myself (pre-fix red in the temp `git worktree` /tmp/de-harvest-gate at the base with the tip's test file overlaid; post-fix green on the tip), `git merge --no-ff -F <msg>`, then `git diff --quiet <tip> HEAD -- <files>`. A graph-data round is measured on its COMMITTED tip (loader duplicate_ids, links.py links, stitch --project . --verify). A round with NO committed test: gate = the blast check + my own probe (EF.89). A kid that DIED after building (EF.90: 65K overflow): gate its worktree bytes red/green, `write.py <exp> 'thought ...' --root <kid wt>`, then `cli.py done <iter> <agent> --verdict ... --node-id <exp> --parent <hyp> --evidence-runs <exp>` FROM the kid worktree, then harvest.
4. ONE mur per round, detached (`setsid nohup python3 extensions/agi/bin/workflow.py run agi-merge-up-review --harness <h> --args "$(cat <args>)" > <log> 2>&1 < /dev/null & disown`, PI_BIN exported; under the HOLD `--harness pi-free`), then ONE `[merge-up]` to thought-master naming the exact pushed SHA (board row inside). Watch the PYTHON pid of a mur, never `pgrep -f`.
Never: `grid.py checkout` · `grid.py commit --all` · `git add -A` · rebase · force-push · `git rm` under `.agi/nodes` · a tool that waits for a human · message belam except a numbers line or `[decision]` · touch `.env`, secrets, `~/.pi`, `moral:*`, `vision:*`, `config:*` myself · write engine code myself (exception: a fix delta TM orders made by me directly -- TMM.68 #3, TMM.120's E0). MESSAGES: only for a blocker or a fully completed merge-up (owner 09:5xZ via TM, goal:g5); read dms in full (the mail hook runs the ONE read); a TMM.nn the card does not name = grep `/data/work/agi/.agi/comms/season-2/dm/director-engine--thought-master.md`. Bodies via a file + python subprocess (`send.py send thought-master <body>`). Own paths, exact pathspecs, push after every action.
**STANDING RULE (TMM.120, owner 16:14Z 09-24, verbatim via TM): "keep working until rotate and then rotate self -- don't rely on others to do it."** The "approaching rotation" bands are NOT a stop. Work continuously until `[meter]` reads f >= 0.47, THEN `python3 extensions/agi/bin/rotate.py rotate` (bare) yourself, immediately, no waiting on TM/owner/anyone else. Card write LAST, right before that command. Prayers first and last only. **NOTE for the successor reading this: the auto-capture hook repeatedly overwrites this file's WORKING TREE copy (uncommitted) with a generic stub once f crosses 0.85x the line -- if the on-disk file looks thin/generic, `git log --oneline -- .agi/sessions/quorum/director-engine.md` and read the last real commit, don't trust the working tree blindly.**

## LIVE STATE + STOPS (16:2xZ 09-24, gen 7, meter ~0.435 -- rotating this turn)
```
BIG NEW ASSIGNMENT (TMM.121, owner 16:20Z verbatim): "make director-engine do a pass on all the hardcoded prose warnings sent
back to models in every build node and put them all into templates that get loaded in dynamically" -> goal:g5.32 (mvp +
hypotheses go under it). Scope: text a MODEL reads (hook output, CLI refusals/warnings, nudges, reminders) -- NOT human-only
logs/exceptions/fixtures. Where: extensions/agi/templates/<family>/, ONE loader, placeholders filled at the call site, no
second copy in code. Rule: byte-identical first (a test per family pins old render == new render; wording changes land
separately); new template files = an mvp parent (goal:s29); a changed engine file = [build:<id>, goal:g5.32]. Done = the
inventory's "still in code" column reaches 0 + a guard test per migrated family. NOT STARTED -- first step is T0 (the
inventory itself: every model-facing literal, file:line + family + fields, committed) + the loader + migrating
rotation_alert.py's band text into it (T0 absorbs E0, already done as code -- see below).

QUEUE (TMM.121, latest, supersedes TMM.115/112): R0's merge-up (blocked, see below) -> T0 (inventory+loader+rotation_alert
migration) -> E1 (4 items) -> T1..Tn (one family per batch) -> the CMP.02 reap guard -> E3 -> E4 -> E5 -> E6 (a coalesced-nudge
sweep: a nudge to a busy pane never re-fired for 24,136s, no [undelivered] -- named by TM, not yet investigated).

R0        Code is DONE and merged @5acc65705a (EF.107+EF.108). mur R0 finished: review=accept, verify=accept_with_residue with
          ONE real, CONFIRMED residue (not refutable, unlike R-EF106's): test_brief_render.py's SURVIVAL-PROFILE fixture-root
          assertions (the `for profile in ("survival","ultimate_survival")` loop, ~line 55-62) pass `project_root=tmp_path` but
          only assert the guard sentinel, never that the survival-state-card actually reflects the FIXTURE's git state rather
          than the live checkout's (brief.py:743-768 runs `git -C` against project_root). EF.108's new test covered the
          CONFIG-GUARD path's project_root threading, not this SURVIVAL-CARD path -- genuinely two different call sites, only
          one got a positive assertion. Full verify result: .agi/sessions/workflows/runs/mur-9/verify_R0.json. DO NOT send
          [merge-up] #9 until this closes (TMM.115: residues=0, no override -- this one is real).
          NEXT: dispatch ONE tiny test-only kid (target same hypothesis as EF.107/108) -- build a fixture project_root with a
          DISTINCT git/file marker, call brief.assemble(tier="kid", profile="survival"/"ultimate_survival", project_root=...),
          assert the fixture's marker appears in the survival-state-card section, not the live repo's. Then gate, merge on top
          of 5acc65705a, mur the FULL combined diff (old_tip=15ef490ab2) again, THEN [merge-up] #9 -- confirm [delivered].
E0        DONE, merged directly (TM-ordered code delta) @6c33e4d01e: rotation_alert.py's below-the-line band message now
          appends "Keep working; at the line run rotate.py rotate yourself." One test
          (test_b2_band_message_says_keep_working_not_stop) gated red without the fix / green with it, 57 passed in the file.
          NOTE: TMM.121 says T0 "absorbs" E0 -- when T0's inventory+loader lands, this literal moves into a template; until
          then the direct string is correct and tested as-is, don't touch it again for T0's sake alone.
E1        4 items, hypothesis nodes already on the trunk (synced), claims read directly (not yet dispatched):
          - key-row-publish-carries-only-key-cells-and-a-prime-row-edit-reaches-a-worktree-post: rotate.py:10368
            _authority_row_content replaces the WHOLE seat row instead of splicing only the cells the rotation owns
            (pubkey/key_history/session), so a worktree publish can revert a Prime row edit (measured: 3b6e0eb632 reverted by
            4990f6f9f7, gen 6 seated on the wrong model as a result).
          - authority-publish-fails-closed-on-an-unreadable-veto-cell: rotate.py ~10415, an unreadable/missing veto cell
            should refuse the publish by name, not proceed.
          - refused-authority-publish-defers-the-successor-key-swap: rotate.py ~17579, a REFUSED/SKIPPED or non-origin
            publish should defer the successor-key swap, never complete it.
          - migrate-refuses-an-inadmissible-grant-before-worktree-and-spawn: rotate.py ~21335, admissibility must resolve
            BEFORE the worktree is cut / spawn runs.
          Dispatch as ONE small batch (same pattern as R0) once #9 is out -- direct kid, --tier kid --harness pi-free.
PASS4     belam's signed [decision] (ed25519, 14:08Z): engine-delta-1 accepted with 2 residues (legacy parents w/o
          AGI_HARNESS not covered; dry-run output doesn't name the inherited AGI_HARNESS source) -- queued after E3, per
          belam's own stated default, no reply needed.
CMP.02    PINNED and reported (.agi/sessions/de-0923/cmp02-pinned.md), TM ACCEPTED (TMM.116): the guard (reap refuses a hash
          absent from a box-local mint ledger, no override; revoke keeps an explicit override since a leaked key must stay
          killable from anywhere; two tests) keeps its queue slot -- dispatch when its turn comes, not before.
#7+#8     LANDED on the town trunk @c876dbf720. #7's own [merge-up] never reached TM's dm last time (file written, send never
          confirmed) -- ALWAYS confirm a send.py send prints [delivered] before considering a report sent.
LANDED    #1-#8 (trunk c876dbf720). R0 code merged to the post @5acc65705a but NOT yet landed to the trunk (residue open).
RESIDUES  Only the ONE named above (R0's survival-card fixture-root assertion). Older, unrelated, still open: cli.py done
          leaves a kid's .agi/config.json edit unstaged · dispatch --branch bases a kid on the CWD post · write.py --dry-run
          admits an edit the real write refuses · rotate-self's seat row comes from the shared main checkout · .15 r4 CR/CRLF
          readers · ML-3 · .23 · .14 · stitch materialize's chain head · rotate's stops-slot fence.
NOT MERGED EF.79 crons r1 tip 256dbb2f26 -- regressed; never merge it.
RULE      TMM.103: a PARENT's spawn line pins its kid's project to the parent's own worktree. TMM.107(3): kids go DIRECT.
```

## BANKED
- CMP.02's code guard: design pre-approved (TMM.116), queue slot unchanged (after E1) -- not pulled forward.
- prime-merge-routine-is-one-cron-script (09-21, never built) -> asked TM whether it is still wanted.
- EF.10 + goal:g7.33.8 stranded on this branch (pre-hold) -> flagged in the 0921 merge-up; core decides.
- GUARD (paid hold instruction-only) -> named in #5: the Prime points the ladder's tier-0 rows at pi-free while paid is held.

## 🔴 WHERE IT STOPS — the one next command (16:2xZ 09-24, gen 7 -> rotating NOW at the line per TMM.120)
`````
````
```
1  Dispatch ONE tiny test-only kid closing R0's last real residue (the survival-profile fixture-root assertion -- exact spec
   in the R0 block above), same target hypothesis, --tier kid --harness pi-free --branch --detach.
2  Harvest it (gate red/green), merge on top of 5acc65705a, mur the FULL R0 diff again (old_tip=15ef490ab2), confirm
   residues=0 this time -- then ONE [merge-up] #9 to thought-master, CONFIRM it prints [delivered].
3  Start T0 (TMM.121): inventory every model-facing hardcoded string across build nodes (file:line, family, fields) into a
   committed doc/table, design the extensions/agi/templates/<family>/ loader, migrate rotation_alert.py's band text into it
   FIRST (byte-identical render test required before any wording change), then E1 (4 items above), then T1..Tn.
4  Check the inbox each batch end (`python3 extensions/agi/bin/send.py read director-engine`) -> act on TM's word exactly.
5  Work to the line every time, then `python3 extensions/agi/bin/rotate.py rotate` (bare) yourself -- do not wait for a nudge.
```
````
`````
