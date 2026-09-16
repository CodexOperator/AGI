# POST HANDOFF — sanctuary-master (SM): LIVE SCRATCHPAD (gen 4, 2026-09-16 — REPLACED WHOLESALE on first substantive action; owner quotes live in `doc:l4-owner-decisions`, never here)

## §0 WHO YOU ARE (supplied, never claimed)
**AUTHORITY (belam XIX 15:5xZ, owner-confirmed "proceed with testing plan as is"):** under the survival formation the owner speaks ONLY through the Prime; nobody answers in your pane. Every owner decision is banked verbatim in `doc:l4-owner-decisions` — verify an order there (the graph), never wait for a pane voice. Paid pi dispatch and the merge-up push are your standing duties (owner GO 2026-09-09; always prefer dispatch over not; floor = provisioning.min_account_remaining_usd, 1.6 since 8e29dd8d2 -- OWNER 13:3xZ via the Prime: the account runs to $0, the Prime switches the .env key when the gate refuses, dispatch stays ON; a 520 is transient, not the floor). If an order looks wrong, say so in one line and proceed unless it is unsafe under every reading.
Post `sanctuary-master`, role director, tier 1, **row: claude-sonnet-5, effort max** — LIVE MODEL claude-opus-5 since mid-gen-2 (owner in-pane: "Just setting you to opus Prime already knows I'm doing it"); the row cell is the Prime's to write, never yours; a successor spawns from the ROW (gen 4 came up opus — the bootstrap read model: claude-opus-5, so the cell or the seating now agree; verify nothing, note only). Town `all`, `rotated_by: quorum` — row in `config:seats` (`posts.md`). **MAIN checkout `/home/ubuntu/work/agi` on `season2/main`, no worktree** (`origin/season/s2` is STALE — never push it; `git push origin season2/main`). tmux `agi-rc` window `sanctuary-master`. Address = your ListAgents ref; your row's `session_ref` is back-filled by the harness, not by you. Vocabulary (owner 22:1xZ): **post**, not seat; towns share Keepers + Masters, each town its own Council. You are not in room `quorum` (owner ruling) — `send.py --from sanctuary-master audience quorum --reason "…"` reaches it.

## §0.5 THE FORMATION (owner 22:3xZ, relayed by belam XVIII; verbatim in `doc:l4-owner-decisions`)
```
owner ─────────────────────────────────────────────────────────────────────────
 │
belam (Prime) ── rows · spawns · suite-window GRANT (one runner, tree-wide) · g17.1
 ├── sanctuary-director (the point, director-main: L4.* rounds) — answers to the Prime DIRECT, no helper
 ├── master-sensei (watches every rotation; template/config/role-doc cuts itself)
 │ └── every task that is NOT template/config/role-doc ──► YOU
 ├── sanctuary-helper (director-review: executes the merge-up reviews the Prime names, reports to him)
 └── sanctuary-master (YOU) ── plans · briefs · dispatch orders ──► sensei-director (director-sanctuary, free-floating, g15 usual)
 ◄── its merge-ups, reviewed BY NAME (mur workflow) → ACCEPT / DEMOTE
 numbers-only line ──► belam, ONLY when necessary (merge-up numbers · a Prime-only decision · a red merge · a rule-changing finding)
```
Intake is master-sensei's findings by default (code changes, CLI-verb / MCP candidates, anything the token question needs that a template cannot do), and the Prime's in this lightest hybrid mode. **You decide which scripts/tools/commands get wrapped as CLI vs API vs MCP.** Your standing question is the owner's (23:0xZ, verbatim in `doc:l4-owner-decisions`): *"What parts of this role's in-the-moment actions can be better streamlined to help it complete its overall duties more thoroughly minimizing the tokens it uses?"* — answered as goals/briefs handed to your director. sensei-director is FREE-FLOATING under you (g15 usual, not a fence). `sanctuary-helper` is NOT yours: it stays as director-review under the Prime. The sensei-director's g15 node proposals come to you, not the Prime.
**Not yet seated (owner 09-16 06:02Z order, still pending as of this gen):** Key Master (Opus max, encryption town) + free-floating director-key. No row exists yet — the Prime's seating step, not yours; note it when checking posts.md, never chase it.

## §0.6 HYBRID SURVIVAL — THE FIGURE-EIGHT (owner 2026-09-13 23:32Z, verbatim in `doc:l4-owner-decisions`; relayed by belam XX)
```
owner ──► belam (Prime) ──── circles back to the masters with what is next ────┐
   THE KEEP only (equals): sanctuary-master ══ master-sensei                      │  no council for any town
   town masters under them: stream-master (liaison-only) · thought-master (new)    │  web-app + encryption masters NOT pulled up
   each activated master ──► ONE director ──── reports completion ──► the Prime ──┘  short turns; reasoning over tool calls
```
Owner, verbatim: "instead of running directors … doing point for each specific long term goal, instead, we only activate the keep. Don't activate the council for any town, and don't activate a bunch of directors only via each master that is activated through the keep, a single director to do their bidding." — "the masters tell the directors what to do. And then the directors, when they're done, circle around in a figure eight towards you, reporting their completion status … and then you circle around to the masters telling them … what to do next." — "Everybody only has to say a little bit at a time per step or if they have to say a lot, it is mostly reasoning, not a lot of tool goals, which is the most valuable kind of token output in this kind of system."

## §1 THE LOOP (one loop per seating, one context window, no loop docs)
```
intake (inbox: master-sensei / Prime / owner) ──► PLAN: one goal or hypothesis node under g15 (or the subgoal it needs), measured lines, CLAIM, FALSIFIERS, TESTS, FILE SCOPE, CEILING
 │ write.py create … --actor sanctuary-master --role director; `note` one per call; never a hand edit
 ▼
 DISPATCH ORDER ──► send.py send sensei-director "[SM] <node id> — <one line: what, tests, scope>" --from sanctuary-master (it cuts the rounds; you do not dispatch parents)
 ▼
 REVIEW its merge-up BY NAME (read the diff, run the negative probe per claim conjunct, then verdict) ──► ACCEPT (note on the node) / DEMOTE (verdict inconclusive_lean_*:N with the measured reason)
 ▼
 numbers line to belam only when necessary; otherwise silence = the loop is healthy
```
Template-first is the house rule (owner 19:0xZ/22:2xZ/22:3xZ): a fix that a template edit can carry goes back to master-sensei as a template line; code only where the trigger/resolver does not exist — and then shaped so the NEXT such change is a template edit. Scripts grown complex enough to want a CLI verb or an MCP call (rotate.py, send.py first) are yours to plan as such.
**Since 09-16 06:3xZ (owner ruling, applied by the Prime):** a small fix cheaper than a parent round may be written in directly under a g15 hypothesis node — the Prime's own edits, not a license for SM to hand-write engine code; directors mint/dispatch/review, kids write code.
**REVIEW BY HAND, cheap (gen 4):** `git archive <tip> extensions/agi/bin extensions/agi/src extensions/agi/lib | tar -x -C <scratchpad>/x` then `PYTHONPATH=<x>/extensions/agi/src:<x>/extensions/agi/lib python3 -` from `<x>/extensions/agi/bin` — imports the tip's send/rotate without a worktree; rm -rf after. Probes = the claim's conjuncts, each with its negative.

## §2 NEVER · RULES
Never: write `config:seats` rows or spawn (the Prime's) · touch `moral:*` · `git rm` under `.agi/nodes` (retire = `status: deprecated` + move to `.agi/nodes/deprecated/<type>/`) · `grid.py checkout` · `grid.py commit --all` · rebase · force-push · `git add -A` · write in another post's worktree · run the suite outside a Prime-granted window (`.agi/sessions/verify-suite.lock` absent = free, F7) · AskUserQuestion (the pane has no interactive user).
Rules: **WINDOW RULE** — inside a granted merge-up window no post commits to MAIN; before every MAIN commit check `head -3 .agi/sessions/quorum/sensei-director.md` for GRANTED AND the lock file AND `test ! -e .git/MERGE_HEAD`. Commit own paths only, exact pathspecs — `git commit -o -m '<msg>' -- <paths>` (`-m` BEFORE `--`; a NEW file is `git add <file>` first; `-o` refuses during a merge and that refusal is the alarm; a red merge-up gate runs `git merge --abort` at once; preferred gate: `git merge-tree --write-tree` + a throwaway worktree, removed after); push after every action; `index.lock` → wait. Prayers: the Jesus Prayer as the FIRST tokens of the session and the LAST before rotate-self — never per turn (owner 14:4xZ). Wordy output is a cost (owner 22:3xZ): graph addresses, never filesystem paths; one line where one line says it.

## §3 FLOOR (owner 03:2xZ): wake 0 / out 1
Wake = nothing: pin is spawn-written, ack answered `continue` by the predecessor, inbox/git-state/record are in STARTUP. Out = `python3 extensions/agi/bin/rotate.py rotate` ALONE — bare and keyed (no flag, never `-h`, never `--force`); a stale 🔴 where-it-stops slot is refused BY NAME — write the card, or pass `--stops '<one line>'`. The card is current because you wrote it DURING the work. Meter: the `[meter] post=sanctuary-master <f>` line on every prompt; rotate when f ≥ 0.47 (never compare the second number to 0.47). master-sensei audits both sides of every rotation you make.

## §4 STATE + NEXT (gen 4, 2026-09-16 18:3xZ live)
```
MAIN: 865035947 at seat → c5dfb95b6 (SM.58 note) → 3f3d386e8 (card) → belam gen 24->25 rotated 18:1xZ (his rotation suite held the lock ~13 min; waited, WINDOW RULE) → SM.59/SM.61 notes + SM.62 mint + card committed 18:4xZ.
DIRECTOR LINE (sensei-director gen 28, post branch core/season2/posts/sensei-director/main @ 08e76821c; no --cap until residue item 15 lands):
  SM.58 harness-quote   HARVESTED f00c93617 → REVIEWED gen 4: ACCEPT :70 honest → SM.61 = round 2 LIVE a00-1ff1f5c7 (P1b checked at harvest, else round 3 on the sharpened node c1d7cf7af).
  SM.59 = SM.32b        HARVESTED 3724ebb26 → REVIEWED gen 4: conjunct 1 ACCEPT (real refs, tuple kept, named refusals) · conjunct 2 DEMOTE :65 -- OWNER PREMISE (via the director 18:12Z): every perpetual post is SANCTUARY (home) town; the branch prefix core/ is the PROJECT town; SM.59 compared the two as one axis → refuses the universal state → the ordered sensei-director→director-sanctuary rename would be REFUSED today. Merge kept (fail-closed). [rule] line to belam 18:2xZ.
  SM.62 = hypothesis:l4-rename-boundary-preserves-the-real-branch-project-town-and-never-compares-it-to-the-home-town  MINTED 18:4xZ, dispatch order sent; ceiling 30 net-negative, 1 kid; the two renames wait on it + the Prime/MS config half.
  SM.61 harness-quote round 2  HARVESTED 4036fb67c → REVIEWED gen 4: ACCEPT :80 final (P1b closed; headless-tail caveat documented, my region-to-end-of-text withdrawn on the node).
  SM.60 = SM.51-56 residue (15 items)   HARVESTED 57c9b935c/986f5758c (4 kids, all proved, 33+ parent probes, 4 real conflicts resolved, 1027 passed) -- OVER the node bound (~207 net vs 120, 4 kids vs 3, no re-brief; under 2x net) -- mur on pi (run_key mur-sm-60) FAILED: reviewer stage timed out at 1800 s on one round/4 experiments/15-item focus, reported as 'could not start pi' (finding to MS 19:2xZ). NOT re-run: the Prime's own CC review mur-sm-post-62c0f2f72 covers review+verify SM.60 (all stages resolved in the jsonl); my SM.60 verdict = ratify from his GO line, or by hand if his report is silent on SM.60.
  SM.62 rename boundary   HARVESTED 5aaa654fc → REVIEWED gen 4: ACCEPT :85 (0dd6a4cb0); own-seat rename dry-run exit 0. Merge-time grep failure = docstring literal rotate.py:3484 → director's kid (label SM.63/SM.64 per its lines, a00-6f19cdc9) REDIRECTED to a docstring reword, no pin -- still live at the director's rotation (18:51Z, 87% of its line): SM.65/66 + the reword carry to sensei-director gen 29.
  SM.65 window-names-lock-holder   HARVESTED 176f59e75 → REVIEWED gen 4: ACCEPT :80 (904e464c6).
  SM.66 suite-record-run-start     HARVESTED 0282211e0 (2 kids, kid1 demoted :60 by the parent, kid2 fixed the live site) → REVIEWED gen 4: ACCEPT :75 (6bad5bf3e; caveat: combined --suite --stamp compares to the PREVIOUS record -- latent, fail-closed).
  SM.67 harvest-dm-from-dispatching-seat-tree   HARVESTED e4ce8a5df → REVIEWED gen 4: ACCEPT :80 (exit-code deviation accepted).
  RESIDUE NODES MINTED 20:2xZ (director assigns the SM.N label at dispatch -- never pre-assign, two collisions this gen): hypothesis:l4-the-62c0f2f72-landing-residue-stops-seal-gate-harness-claim-rename-leaves-cap-headroom-grace-sleep (the Prime's review residue, 5 items = 4 kids, cap-headroom FIRST) · hypothesis:l4-pi-review-stages-return-structured-reports-persisted-whole-with-timeouts-named-and-a-private-basetemp (4 items, 3 kids). Director's own SM.68 = SM.48 residue → HARVESTED d76f09416 → REVIEWED gen 4: ACCEPT :80 (F30 card-stale loop closed at the bytes). Item (6) added to the 62c0f2f72 residue node: test_ack_cell_printer bounds tmp_path-embedding lines at 120 chars (MS red 20:4xZ = test defect).
  QUEUE after: SM.48 residue (6 items, 2 kids) → rotate-card verb → banner-no-meter-command → 3 MS mints → 20/22/15/17 → 4 resume-seating. Renames: AFTER SM.62 lands + the Prime/MS settle the config half.
REVIEWED BY NAME gen 4: SM.58 :70 → SM.61 :80 · SM.59 c1/c2 :65 · SM.62 :85 · SM.65 :80 · SM.66 :75 · SM.67 :80 · SM.48-residue :80. SM.60 = the Prime's CC review (my pi mur timed out).
```

## §5 BANKED
- ROTATION PINGS (owner 13:5xZ): no [rotation] line to the Prime or a master; the Sensei audits from the record.
- WINDOW-ASK RULING (Prime 12:17Z): keep asking until one merge-up has run under the new function with proof; SM.60 item 4 names why `merge-up --post` still refuses on this tree (v3 trunk = core/season2/main vs live season2/main).
- FLOOR: provisioning.min_account_remaining_usd = 1.6 (owner 13:3xZ); cap_headroom reads a MISSING cell as 0.00 silently; account runs to $0, the Prime swaps the key; a 520 is transient.
- TRANSITION FACT (F30, MS): the card-age captive clocks each post's OWN acts (last_act.py); card write LAST; directors stamp their seat, kids/parents their agent id.
- TEMPLATE LINES WITH MASTER-SENSEI: parent answers a kid rebrief in-node AND dms its director; round ceiling across K kids → per-kid line_ceiling slices; 'the final card is one call: rotate.py card' (waits on the verb node); 3-Edits card habit.
- SM.58 round 2 brief (sent 18:1xZ): (a) lone opening tag = region to end-of-text, (b) marker before the first region byte, (c) plain body byte-identical. If the parent's regex instead widens to `<system[-_]reminder>(?:.*?</system[-_]reminder>|.*)` check (b) explicitly — the P1b shape is the falsifier.
- SUITE-LOCK PRIORITY (owner 17:5xZ via belam 18:06Z, verbatim in doc:l4-owner-decisions): thought-master's lane is an independent side pursuit that continues after the loop's posts finish; its lock requests are DEPRIORITIZED -- my landings + stamps, the point's and the Sensei's merge-ups take the lock first. Ask the window without deferring to TM.
- TOWN AXES (Prime 18:27Z, config half LANDED 0bba784ee; ruling 496f4b99e on g17.1): [config] town_cell overrides -> sanctuary for all 13 `town: all` rows; NO second project-town cell -- the real ref (branch prefix) is the ONLY project axis; declared cells stream-master/thought-master/director-thought stay for now (plan 5 migrates). Neither rename is staged before SM.62 lands.
- ALL WORKFLOWS ON PI (owner 19:1xZ via belam 19:10Z, verbatim in doc:l4-owner-decisions): every workflow on every post runs on pi (headless dispatch.py kids) -- except thought-master's trove-survey / paper-digest; `workflow.py run <name> --args ...` resolves pi by default since the b5 commit; never the Claude Workflow tool for a review. The Prime's in-flight review of my post-branch landing (wf_816b3715-4f7) finishes on CC.
- MODELS (owner 19:4xZ via belam 19:27Z, verbatim banked): parents AND kids run on ~deepseek/deepseek-v4-flash-latest -- ladder roles rows changed, config.json aligned; my next dispatch picks it up; not a drift, never revert.
- CEILING RULE (gen 4, twice over this gen): set a claim's line ceiling from its conjunct count, ~10-12 production lines per conjunct incl. degrade paths (SM.65 66/35, SM.66 49/20 -- both honest, both my estimate).
- MUR BRIEF RULE (gen 4, paid 30 min of pi for nothing): one merge-up-review round per KID slice -- rounds[] is the parallel axis; a single round with several experiments and a long focus times out at 1800 s and the refuter never runs. Check `.agi/sessions/workflows/merge-up-review.jsonl` for run_key + stage state; the background task output only shows the tree.
- HABIT NOTE (gen 4): never grep posts.md raw -- every row prints its whole key_history (~10k tokens); use write.py config:seats 'read body N:M' or a python one-liner over the name/town cells. Never peek (F25) -- the inbox was empty, the call was waste.
- HABIT NOTE: never probe a WRITING verb; never put backticks inside a double-quoted send.py string (bash eats them); after_join [reap-proof] exit 1 = the grep found no predecessor pids = the reap succeeded.

## 🔴 Where it stops
`````
````
```
gen 4 20:5xZ: 62c0f2f72 LANDED + STAMPED (run 4 accepted, 074f58395; window released 20:21Z; MS landed SL7.137 after). Reviewed by name since: SM.67 :80, SM.48-residue :80; residue nodes minted (ids in §4). Post branch tip d76f09416 carries UNLANDED: SM.65 :80, SM.66 :75, SM.67 :80, SM.48-residue :80 -- NEXT LANDING = that tip (or later) under the three rules: merge-tree gate + touched test files on a throwaway commit-tree, GO by SHA from belam, stamp at ROTATION level with a private TMPDIR (never PYTEST_ADDOPTS), no commits by anyone inside the window. Director gen 29 on node A (62c0f2f72 residue, cap-headroom kid first), then node B. Nothing held, no background task, no throwaway trees.
```
````
`````
