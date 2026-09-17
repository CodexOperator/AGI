# POST HANDOFF — sanctuary-master (SM): LIVE SCRATCHPAD (gen 7, 2026-09-17 — REPLACED WHOLESALE on first substantive action; owner quotes live in `doc:l4-owner-decisions`, never here)

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


## §4 STATE + NEXT (gen 7, 2026-09-17 09:57Z-; live)
```
MAIN gen 7: seated 09:57Z at c5295e50b; row/record read gen 0->1 (SM.93 resolver: no row cell, no record gen_after, header = INFO) -- predecessor card said gen 6; noted, not chased.
STREAM: QUEUE EMPTY per the Prime (09:38Z/09:56Z); closeout (COMPLETE.md) is his; I idle between director lines until he names the next stream.
SM.99 (director re-dispatch of SM.97 tier-gate, kids a00-99dec2b6 parent / a00-d65792f8 kid): HELD by the director 10:32Z, not merged, origin untouched, branch season2/loops/hypothesis-l4-the-done-tier-gate-a00-99dec2b6 @7d2d3cfc4. Kid 2 closes the leak; the new locations.refuse_live_sessions_from_plain_scratch guard reds 4 full-suite tests (test_dispatch sub_floor_notice, test_evidence_gate out_of_range_lean, test_rotate real_judge_optin_stands_the_stub_down, test_stream_master_real_judge_optin survives_conftest_strip) -- each spawns nested pytest from a fixture under an in-tree basetemp; is_live_checkout(out) = shares the git common root, so the fixture reads as live.
SM.100 ORDERED 10:4xZ (a57c7f15f) -> HARVESTED 11:26Z (director tip 52e07e438) -> REVIEWED by name on the merge result 11:4xZ: ACCEPT :80 (note 2f8a23bf6): predicate = refuse iff cwd strictly inside the live .agi/ with no closer config; 6/6 probes (P1 refused, no path; engine subdirs + root + own-config fixture allowed); 47 green (4 named + tier-gate family); GOALS round-trip ok; 9/10 lines. Real SM.99 seam = nested pytest launched with cwd = an engine SUBDIR (not an in-tree basetemp -- claim 1 refuses those at session start). Residue disclosed: bare scratch in-repo OUTSIDE .agi/ is allowed (pytest cannot reach it).
GO by SHA belam 11:31Z -> LANDED 66ef15961 (live-HEAD gate: ONE note/note conflict on the hypothesis node, my ACCEPT note vs the director's -> union in a throwaway tree via git merge-file --union, GOALS round-trip, ff, pushed). Window GRANTED after the landing -> suite 5386/0/16 in 655 s, all 12 green -> --stamp PASS: MAIN STAMPED 3198/202/3400 at 66ef15961 (baseline = .agi/sessions/verify-count.json, untracked, nothing to commit). Numbers line sent 11:5xZ; the director's 1x red named (malformed verdict a00-6e4cec62-f1256a, fixed in-branch).
SUITE: MAIN stamped 3198/202/3400 at 66ef15961 (gen 7, 5386/0/16); live count after SD.13 (+3) and the retire pass (15 -> deprecated) = 3186/217/3403, stamps at the next granted window.
RETIRE PASS LANDED 7b911d6d6 (Prime list 12:0xZ from the kid B survey): 15 g15 experiment-less hypotheses deprecated (13 retired, 2 folded); links 0 broken; GOALS identical; count steady. Recipe that worked: write.py set status deprecated && note ... then git mv to deprecated/hypothesis, commit -o with BOTH old and new paths, verification --level rotation reads the count (refuses the stamp by name on uncommitted node paths).
SD.13 LANDED FOR THE FROZEN POINT (Prime 11:49Z order; f9f0a332b + 5610b617c): kid A test-only _wait_exit poll kept as hygiene, verdict DEMOTED proved -> lean_disproved:35 (Popen.wait already polls to the deadline; red never reproduced); residue 2 (tty-hangup test red under full-suite load) OPEN on hypothesis:l4-suite-freshness-shares-a-stale-run-start-timestamp-and-a-wrapper-wait-races-under-load with the next-cut recipe; kid B survey hypothesis:a00-e1933e6a-176c0e (37 g15 experiment-less rows) = the Prime's retire-list input.
IDS: SM.100 = SM.99 corrective. Next free id SM.101.
```

## §5 BANKED
- AFTER_JOIN DOUBLE DELIVERY (gen 5, still live gen 7 09:59Z): the service prints after_join in the pane AND self-dms it -> one template/config line for master-sensei with the next numbers line.
- ROTATE-OUT SUBJECT = "```" (gen 6->7 c5295e50b): the stops slot opens with a fence, rotate takes line 1 as the commit subject -> template line for master-sensei (skip fence lines / take the first prose line).
- GEN CELL RESET 6->0->1 on SM.93's first rotate for this post (no row cell, no record gen_after): expected under the new resolver; Sensei audit item, no belam line.
- ROTATION PINGS (owner 13:5xZ): no [rotation] line to the Prime or a master.
- WINDOW-ASK (Prime 12:17Z): GO by SHA until one merge-up runs under the new function with proof; `merge-up --post` still refuses here (SM.60 item 4).
- FLOOR: provisioning.min_account_remaining_usd = 1.6; the account runs to $0, the Prime swaps the key; a 520 is transient; OPENROUTER_API_KEY 401 at wake = old key, keys are minted per spawn; a mint WORKSPACE 403 -> [red] to belam.
- SUITE-LOCK PRIORITY (owner 17:5xZ): thought-master lock asks deprioritized; my landings + stamps, the point's and the Sensei's merge-ups first.
- ALL WORKFLOWS ON PI (owner 19:1xZ); MODELS (owner 19:4xZ): parents + kids on ~deepseek/deepseek-v4-flash-latest, never revert.
- CEILING RULE: ~10-12 production lines per conjunct; overage disclosed. MUR: one round per KID slice; rounds[] is the parallel axis.
- BACKTICKS: never a backtick or $( in a double-quoted send/write body -- quoted heredoc to a scratch file, python subprocess.
- HABIT: never grep posts.md raw (write.py config:seats 'read body N:M'); never peek (F25); never probe a WRITING verb; after_join [reap-proof] exit 1 = reaped; review = merge RESULT in a throwaway detached tree, short basetemp, --force remove after; never write a node while a suite you own runs.
- TOWN AXES (Prime 18:27Z, 0bba784ee): the real ref (branch prefix) is the only project axis until plan 5.

## 🔴 Where it stops
````
```
gen 7 IDLE 12:1xZ (0.17 of 0.47): SM.100 landed + stamped 3198/202/3400; SD.13 landed for the point (kid A demoted :35, residue 2 open); retire pass landed 7b911d6d6 (15 deprecated, count 3186/217/3403 steady, links 0, goals identical). Numbers lines sent. NEXT: idle -- the closeout write-up is the Prime's; on the next stream: intake -> plan -> dispatch order to sensei-director (next free id SM.101). Nothing held; no throwaway tree; lock absent; no dm owed.
```
````
