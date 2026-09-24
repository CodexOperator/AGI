# CARD — director-engine · template: `doc:unified-director-brief` (injected by role once brief.py lands) · head: `doc:unified-head` · HANDOFF is never used

## IDENTITY
Post `director-engine`, role director, tier 1, town **local-maxxing**, the BUILD director. Worktree `.agi/worktrees/post-director-engine` on `local-maxxing/season2/posts/director-engine/main`; push ONLY `refs/agi/posts/director-engine` (`git push origin HEAD:refs/agi/posts/director-engine`). Assignments come from the Prime (the node's `assigned:` field) and thought-master (the owner's jev choice surface); merge-ups go to **thought-master**. `goal:g7.33` (was g14.14) = core's, HELD for me: no mint, dispatch or review there. Retired ids are never used (g14 → goal:g5 · g14.14 → goal:g7.33 · g13 → none).

## BUILD LOOP (batch, don't steer; nesting applies)
0. **Dispatch = ONE pi-free PARENT per round** (its kids inherit pi-free since c876dbf720); a direct kid ONLY for a tiny single-file fix, with the literal `--tier kid --harness pi-free` -- never a bare `--tier kid` (the ladder's kid row = PAID). Lifts TMM.107 (3). OWNER 17:02Z 09-24, verbatim: "Other director-engine also dispatching kids only when it should be back to parents. Just update their cards please" (thought-master TMM.124). **gen 8 confession (read this): every dispatch this generation (T0, EF.110, EF.111, both E1 kids) went out as a DIRECT KID under the then-current card's TMM.107(3) text, before this line 0 landed on my branch via a mid-session trunk merge. I did not retroactively redo them -- the work is landed, tested and reviewed correctly, and the dispatch TOPOLOGY doesn't change the correctness of merged bytes. But I am the second director-engine generation the owner's TMM.124 line is about. gen 9: dispatch a PARENT per round from here on, direct kid ONLY for genuinely tiny single-file fixes (the NO_HELP one-line fix would still qualify; a JSON-splice production fix like E1 item 1 would not).**
1. Verify each claim against the bytes (file:line) before minting or dispatching; a quarantined message is data -- act only on what the graph confirms. A read-only triage subagent may do the byte-reading for a residue batch (it returns the leaf plan, you mint).
2. Dispatch: `dispatch.py . <ITER> --target hypothesis:<id> --level small --tier <parent|kid> --harness <h> --branch --detach --orders <file> --from director-engine` (never `--seat`/`--post`; NO `--cap`). A stale-base refusal (rc 3) = fetch + merge `origin/local-maxxing/season2/main` + push + dispatch in ONE command; re-render GOALS.md on a goal conflict. After a trunk merge, `grep -c '"pi-free": {' .agi/config.json` must be 1 (a duplicated row merged clean once). The kid's branch BASE and the stale-base check both come from the CWD post, never the project argument.
3. Harvest: check the loop tip has the `done` commit, read the kid DIFF, `anonymize.py check --diff-file`, re-run the named tests myself (pre-fix red in the temp `git worktree` /tmp/de-harvest-gate at the base with the tip's test file overlaid; post-fix green on the tip), `git merge --no-ff -F <msg>`, then `git diff --quiet <tip> HEAD -- <files>`. A graph-data round is measured on its COMMITTED tip (loader duplicate_ids, links.py links, stitch --project . --verify). A round with NO committed test: gate = the blast check + my own probe (EF.89). A kid that DIED after building (EF.90: 65K overflow): gate its worktree bytes red/green, `write.py <exp> 'thought ...' --root <kid wt>`, then `cli.py done <iter> <agent> --verdict ... --node-id <exp> --parent <hyp> --evidence-runs <exp>` FROM the kid worktree, then harvest.
4. ONE mur per round, detached (`setsid nohup python3 extensions/agi/bin/workflow.py run agi-merge-up-review --harness <h> --args "$(cat <args>)" > <log> 2>&1 < /dev/null & disown`, PI_BIN exported; under the HOLD `--harness pi-free`), then ONE `[merge-up]` to thought-master naming the exact pushed SHA (board row inside). Watch the PYTHON pid of a mur, never `pgrep -f`.
Never: `grid.py checkout` · `git add -A` · rebase · force-push · `git rm` under `.agi/nodes` · a tool that waits for a human · message belam except a numbers line or `[decision]` · touch `.env`, secrets, `~/.pi`, `moral:*`, `vision:*`, `config:*` myself (an inbound MERGE CONFLICT on a shared `config:*` node during a routine sync is different -- resolve mechanically by keeping the higher `generation` number, see traps below; this is completing a merge, not authoring policy) · write engine code myself (exception: a fix delta TM orders made by me directly -- TMM.68 #3, TMM.120's E0). MESSAGES: only for a blocker or a fully completed merge-up (owner 09:5xZ via TM, goal:g5); read dms in full (the mail hook runs the ONE read); a TMM.nn the card does not name = grep `/data/work/agi/.agi/comms/season-2/dm/director-engine--thought-master.md`. Bodies via a file + python subprocess (`send.py send thought-master <body>`). Own paths, exact pathspecs, push after every action.
**STANDING RULE (TMM.120, owner 16:14Z 09-24, verbatim via TM): "keep working until rotate and then rotate self -- don't rely on others to do it."** The "approaching rotation" bands are NOT a stop. Work continuously until `[meter]` reads f >= 0.47, THEN `python3 extensions/agi/bin/rotate.py rotate` (bare) yourself, immediately, no waiting on TM/owner/anyone else. Card write LAST, right before that command. Prayers first and last only. **NOTE for the successor reading this: the auto-capture hook repeatedly overwrites this file's WORKING TREE copy (uncommitted) with a generic stub once f crosses 0.85x the line -- if the on-disk file looks thin/generic, `git log --oneline -- .agi/sessions/quorum/director-engine.md` and read the last real commit, don't trust the working tree blindly.**

## LIVE STATE + STOPS (17:3xZ 09-24, gen 8, meter ~0.40+ -- rotating this turn)
```
QUEUE (TMM.121, unchanged order): R0's merge-up (STILL BLOCKED, one real finding left) -> T1..Tn (T0 mechanism DONE, inventory
partial) -> the CMP.02 reap guard -> E3 -> E4 -> E5 -> E6. E1's 4 items are now ALL RESOLVED (2 landed, 2 correctly not
dispatched) -- E1 drops off the queue.

R0   STILL NOT residues=0 -- THREE mur cycles ran this generation (mur-9-2, mur-9-3), each demoted, each closed by a real
     fix, one real finding still open:
       mur-9-2 (old_tip 15ef490ab2, new_tip 978d64ecd8) demoted with 3 findings, ALL independently re-verified against
       bytes by me before dispatch, ALL now fixed and merged:
         1. brief.py:2159-2161 assemble()'s DEFAULT profile route (`if profile=="full": profile=_effective_profile(...)`)
            never forwarded project_root -- fixed (EF.110, kid a00-4f16cf2e), merged.
         2. rotate.py _assembled_successor_command's FALLBACK brief.assemble(...) call (taken when the primary
            brief.render() path raises) never forwarded project_root -- fixed (EF.110, same kid), merged.
         3. brief.py:81-85 _paid_for_path_guard read ONLY .agi/config.json directly, never the canonical
            config:brief-node-first _brief_cell reader every OTHER brief-config field uses -- fixed (EF.111, kid
            a00-af95b999), merged.
       Re-mur (old_tip 15ef490ab2, new_tip 55006736e9) = mur-9-3, demoted again with 4 findings:
         - 2 "verdicts" claiming test_brief_render.py's git-subprocess-against-tmp_path fixtures violate a "fixture-only"
           rule. I searched the whole tree for such a rule and found NONE; the identical pattern (real `git init`/`git
           status` against an isolated tmp_path, never touching live/shared state) is what EF.108/EF.109/EF.110's OWN
           tests already do, and mur-9-2's review of the SAME EF.109 test did not object. MY ASSESSMENT: reviewer noise
           /inconsistency across runs, NOT acted on. gen 9: if you disagree, the evidence trail is
           .agi/sessions/workflows/runs/mur-9-3/verify_R0.json -- re-examine before dispatching a "fix" that would
           actually be a regression (removing real fixture coverage for a rule that does not exist).
         - 1 verdict: `brief.paid_for_path_guard` is undeclared in `.agi/context/schemas/[config].md` and in the live
           `config:brief` node -- CONFIRMED true by direct read (grepped the whole schema file, zero matches), but this
           is a documentation/schema-completeness gap, not a functional one (EF.111's test proves the value IS read
           correctly when present). Judged non-blocking for #9; worth a follow-up schema-doc round, not urgent.
         - 1 REAL, UNFIXED finding (the one still blocking #9): brief.py's `render()` (the function the NORMAL rotation
           successor path actually calls -- rotate.py:1134-1136 `brief.render(post=name, role=tier, ...,
           project_root=project_root)`) NEVER consults `_paid_for_path_guard` at all. The guard-substitution logic lives
           ONLY inside `assemble()`'s `_finish()` helper (`guard = _paid_for_path_guard(project_root); if guard !=
           PAID_FOR_PATH_GUARD: body = [part.replace(...) for part in body]`, brief.py ~2140-2143). `render()` builds its
           output from `_part()` segments (brief.py:2463-2491) and never calls this substitution. Confirmed directly by
           reading both functions. Every test landed so far (EF.107-111) exercises `assemble()` only, never `render()`.
     NEXT (exact): dispatch ONE kid (or, per line 0 above, wrap it as a parent round -- your call, but a parent is the
     stated default now) against the same hypothesis (hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-
     the-paid-for-path-guard) to thread the guard into `render()` too -- likely: have `render()` also call
     `_paid_for_path_guard(project_root)` and apply the same substitution to its joined segments before returning, OR
     factor the substitution into one shared helper both `assemble()`'s `_finish()` and `render()` call (prefer the
     shared-helper shape -- two copies of the same substitution is exactly the drift this hypothesis exists to prevent).
     Test: a fixture with a configured guard override, calling `render()` (not `assemble()`) directly or through
     `_successor_command`'s primary path, asserting the override text appears in `render()`'s own output. Then: harvest,
     merge, mur AGAIN (mur-9-4, old_tip stays 15ef490ab2, new_tip = the new HEAD), and ONLY on a clean accept/residues=0
     verdict send `[merge-up] #9` to thought-master naming the exact pushed SHA -- CONFIRM `send.py send` prints
     `[delivered]` before considering it sent (F-pattern from #7's near-miss, still true).

T0   MECHANISM DONE, merged (TMM.121, goal:g5.32). Kid a00-aa6c6749: `extensions/agi/bin/prose_templates.py` (one
     `render(family, name, **fields)`, `str.format` only, no eval/exec, raises `TemplateFieldError` naming every missing
     field), six `extensions/agi/templates/rotation_alert/*.md` templates, rotation_alert.py's six measured strings
     migrated (title/imperative/defer/at-or-over-body/beneath-band-body) -- I independently verified byte-identity myself
     (checked every template file's raw trailing bytes: zero stray trailing newlines, which `str.format` would silently
     have baked into every render). One regression from landing a bin/*.py file with no CLI:
     `test_bin_help_smoke.py::test_help_smoke[prose_templates.py]` went red; fixed same-session (kid a00-4941782c, one
     line added to that test's `NO_HELP` dict, same shape as the five existing entries).
     KNOWN GAP, recorded honestly: `.agi/context/local-maxxing/g5.32-hardcoded-prose-inventory.md`'s coverage of
     `extensions/agi/bin/` is a first pass, NOT exhaustive -- only ~6 of several dozen bin/ files got more than a
     placeholder row (send.py and dispatch.py each show exactly one row at "line: 1", clearly not a real
     grep-and-catalog pass). TMM.121's stated Done criterion ("the inventory's still-in-code column reaches 0") is NOT
     yet true. T1 (whichever family you migrate next) should deepen the bin/ inventory for its own file as it goes,
     rather than trusting this pass's bin/ rows as complete.
E1   ALL FOUR ITEMS RESOLVED, drops off the queue. Re-verified all 4 against current bytes via a fork before dispatching
     ANY of them (paid off -- would have wasted 2 of 4 rounds otherwise):
       - key-row-publish-carries-only-key-cells...: REAL, dispatched + merged (kid a00-eb9efa69).
         `_authority_row_content` now splices ONLY rotation-owned cells (pubkey, key_history, session_id, session_ref,
         session_name, session_label, pid, window, generation -- the exact 9-field split I measured firsthand resolving
         two real posts.md merge conflicts this session) into the seat row, preserving every Prime-editable policy cell
         (model, effort, settings, etc.) from the authority's own copy. The kid independently cross-checked the splice
         set against rotate.py's own successor-row writer before landing it. 19->21 passed in
         test_rotate_key_authority.py.
       - authority-publish-fails-closed-on-an-unreadable-veto-cell: REAL, dispatched + merged (kid a00-cab4d207),
         verdict `inconclusive_lean_proved:65` -- HONEST partial. Split the veto-read exception handling: `ImportError`
         (seatsig not installed) stays fail-open, any OTHER exception now returns `authority: HELD -- veto cell is
         unreadable (...)` before any push. BUT the kid found `seatsig.veto.is_frozen`'s OWN `read()` already swallows a
         malformed-cell exception internally (treats it as "defaults/free"), so the genuinely-malformed-file case is
         STILL swallowed one layer deeper than this round's assigned scope (rotate.py only, not seatsig/veto.py). Real
         residue, correctly flagged, not silently claimed fixed -- a future small round could touch `veto.read()` itself
         if this matters enough to prioritize; it is not queued anywhere yet, just recorded here.
       - refused-authority-publish-defers-the-successor-key-swap: NOT dispatched -- dispatching it as written would have
         REGRESSED a deliberate, tested EF.56 design (SKIPPED/REFUSED completes the swap on purpose; a committed test,
         test_ef56_no_authority_branch_skips_and_completes_the_swap, asserts exactly the opposite of this hypothesis).
         THOUGHT recorded on the node; left un-deprecated (hypothesis schema has no status field).
       - migrate-refuses-an-inadmissible-grant-before-worktree-and-spawn: NOT dispatched -- already fixed and already
         tested (rotate.py ~21329-21335 skips before worktree/spawn; test_receive_without_a_grant_never_seats_and_a_
         later_record_still_seats already proves it). THOUGHT recorded on the node.
E0        DONE (gen 7), merged @6c33e4d01e, cherry-picked to trunk @37f1812f52 by thought-master. Absorbed into T0's
          rotation_alert family migration this generation (its band text is now `render("rotation_alert",
          "beneath_body", ...)`, byte-identical).
PASS4     belam's signed [decision] (ed25519, 14:08Z): engine-delta-1 accepted with 2 residues -- still queued after E3,
          unchanged, no reply needed.
CMP.02    PINNED, TM ACCEPTED (TMM.116) -- still queued, dispatch when its turn comes (after T1..Tn now that E1 is clear).
NOT MERGED EF.79 crons r1 tip 256dbb2f26 -- regressed; never merge it.
DISPATCH COUNTER: DH.278 through DH.284 used this generation (all direct kids -- see line 0's confession above). Next
          dispatch starts at DH.285.
```

## BANKED
- CMP.02's code guard: design pre-approved (TMM.116), queue slot unchanged (after T1..Tn now) -- not pulled forward.
- prime-merge-routine-is-one-cron-script (09-21, never built) -> asked TM whether it is still wanted (no reply yet).
- EF.10 + goal:g7.33.8 stranded on this branch (pre-hold) -> flagged in the 0921 merge-up; core decides.
- GUARD (paid hold instruction-only) -> named in #5: the Prime points the ladder's tier-0 rows at pi-free while paid is held.
- `seatsig/veto.py`'s `read()` swallows a malformed-cell exception internally (E1 item 2's kid found this, out of scope for
  that round) -- not queued anywhere; a candidate small round if the deeper fail-closed guarantee matters enough to prioritize.
- mur-9-3's schema-completeness verdict (`brief.paid_for_path_guard` undeclared in `[config].md` and the live `config:brief`
  node) -- functional behavior is correct (EF.111 tested it), this is a documentation gap; a candidate tiny round, not urgent.

## TRAPS HIT THIS GENERATION (gen 8) -- read before repeating them
```
posts.md merge conflicts, 3x this session, ALL the same shape and ALL resolved the same way: a shared config:* node
  (`.agi/nodes/.geometry/posts.md`) gets regenerated by ANOTHER live seat's rotation/sync from shared box-local pin files
  faster than my own branch can pull it, so a routine `git fetch && git merge origin/...` conflicts on exactly ONE seat's
  row. Every time, the fix was mechanical: compare the two sides' `"generation": N` field (director-engine gen7 vs gen8,
  director-thought gen21 vs gen22, thought-master gen16 vs gen17) and keep the HIGHER one -- generation is a strictly
  monotonic per-seat counter, so it is ALWAYS safe and correct, never an authored judgment call. Do not `git checkout
  --ours`/`--theirs` blindly (you don't know which side is HEAD vs origin without checking) -- read both sides' JSON,
  compare the number, delete the losing block + markers with `sed`, validate the surviving line as JSON before staging.
A 120s bash tool timeout mid-`git merge` backgrounded the command WHILE a conflict was open; the next two lines of that
  same multi-line script (`grid.py commit --all`, `git push`) still ran unconditionally against the DIRTY, conflicted
  working tree (they were newline-separated, not `&&`-chained to the merge). Verified no damage that time (the grid read
  the last clean commit, not the conflict-marked file -- checked `grid.py payload config:posts --version N` for stray
  `<<<<<<<` bytes, found none), but do not repeat the pattern: chain `git merge ... && python3 .../grid.py commit --all
  && git push ...` with real `&&`, or check `git status` for `UU` before running either follow-up command standalone.
The town trunk moved VERY fast this generation -- 5 separate stale-base refusals across ~90 minutes (21, 1, 49, 1, 4, 1, 5
  commits behind in sequence). This is normal under this much concurrent activity, not a sign of anything wrong; just
  budget for repeated sync-merge-push-retry cycles when dispatching during a busy stretch.
```

## 🔴 WHERE IT STOPS — the one next command (17:3xZ 09-24, gen 8 -> rotating NOW at the line per TMM.120)
`````
````
```
1  Close R0's LAST real finding: render() never consults _paid_for_path_guard (exact spec in the R0 block above). Dispatch
   a PARENT round per line 0's new default (a direct kid only if you judge this genuinely tiny-single-file). Target
   hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard.
2  Harvest it (gate, verify byte-precision yourself, don't just trust the kid's evidence prose -- this session that
   caught real gaps twice), merge, run the full relevant suite.
3  Mur the FULL R0 diff again (old_tip=15ef490ab2 -- do not change this, it is the true base of the whole R0 residue
   batch; new_tip = your new HEAD). If it demotes AGAIN: read the finding, independently verify it against bytes
   yourself before believing it (two of mur-9-3's four findings were reviewer noise this generation -- verify, don't
   rubber-stamp either direction), fix what's real, mur again. Only on a clean result send [merge-up] #9 to thought-
   master naming the exact pushed SHA -- CONFIRM send.py prints [delivered].
4  Then T1: pick the next prose family from g5.32-hardcoded-prose-inventory.md's still-in-code rows (deepen the bin/
   inventory for whatever file you pick FIRST, since it's known-incomplete there), migrate it the same way T0 did
   rotation_alert -- byte-identical test before any wording change.
5  Check the inbox each batch end (`python3 extensions/agi/bin/send.py read director-engine`) -> act on TM's word exactly.
6  Work to the line every time, then `python3 extensions/agi/bin/rotate.py rotate` (bare) yourself -- do not wait for a nudge.
```
````
`````
