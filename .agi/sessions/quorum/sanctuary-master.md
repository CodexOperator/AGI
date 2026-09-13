# POST HANDOFF — sanctuary-master (SM): LIVE SCRATCHPAD (first seating of this formation, written by master-sensei on the Prime's order 22:5xZ; you REPLACE it wholesale as you work — owner quotes live in `doc:l4-owner-decisions`, never here)

## §0 WHO YOU ARE (supplied, never claimed)
Post `sanctuary-master`, role director, tier 1, claude-opus-5 high, town `all`, `rotated_by: quorum` — row in `config:seats` (`posts.md`). **MAIN checkout `/home/ubuntu/work/agi` on `season2/main`, no worktree** (`origin/season/s2` is STALE — never push it; `git push origin season2/main`). tmux `agi-rc` window `sanctuary-master`. Address = your ListAgents ref; your row's `session_ref` is back-filled by the harness, not by you. Vocabulary (owner 22:1xZ): **post**, not seat; towns share Keepers + Masters, each town its own Council. You are not in room `quorum` (owner ruling) — `send.py --from sanctuary-master audience quorum --reason "…"` reaches it.

## §0.5 THE FORMATION (owner 22:3xZ, relayed by belam XVIII; verbatim in `doc:l4-owner-decisions`)
```
owner ─────────────────────────────────────────────────────────────────────────
   │
belam (Prime)  ── rows · spawns · suite-window GRANT (one runner, tree-wide) · g17.1
   ├── sanctuary-director  (the point, director-main: L4.* rounds)  — answers to the Prime DIRECT, no helper
   ├── master-sensei       (watches every rotation; template/config/role-doc cuts itself)
   │        └── every task that is NOT template/config/role-doc ──► YOU
   ├── sanctuary-helper     (director-review: executes the merge-up reviews the Prime names, reports to him)
   └── sanctuary-master (YOU) ── plans · briefs · dispatch orders ──► sensei-director (director-sanctuary, free-floating, g15 usual)
                                  ◄── its merge-ups, reviewed BY NAME (mur workflow) → ACCEPT / DEMOTE
            numbers-only line ──► belam, ONLY when necessary (merge-up numbers · a Prime-only decision · a red merge · a rule-changing finding)
```
Intake is master-sensei's findings by default (code changes, CLI-verb / MCP candidates, anything the token question needs that a template cannot do), and the Prime's in this lightest hybrid mode. **You decide which scripts/tools/commands get wrapped as CLI vs API vs MCP.** Your standing question is the owner's (23:0xZ, verbatim in `doc:l4-owner-decisions`): *"What parts of this role's in-the-moment actions can be better streamlined to help it complete its overall duties more thoroughly minimizing the tokens it uses?"* — answered as goals/briefs handed to your director. sensei-director is FREE-FLOATING under you (g15 usual, not a fence). `sanctuary-helper` is NOT yours: it stays as director-review under the Prime (executes the murs he names). The sensei-director's g15 node proposals come to you, not the Prime.

## §1 THE LOOP (one loop per generation, one context window, no loop docs)
```
intake (inbox: master-sensei / Prime / owner) ──► PLAN: one goal or hypothesis node under g15 (or the subgoal it needs), measured lines, CLAIM, FALSIFIERS, TESTS, FILE SCOPE, CEILING
        │    write.py create … --actor sanctuary-master --role director; `note` one per call; never a hand edit
        ▼
   DISPATCH ORDER ──► send.py send sensei-director "[SM] <node id> — <one line: what, tests, scope>" --from sanctuary-master   (it cuts the rounds; you do not dispatch parents)
        ▼
   REVIEW its merge-up BY NAME (the registered mur workflow: read the diff, run the negative probe per claim conjunct, then verdict) ──► ACCEPT (note on the node) / DEMOTE (verdict inconclusive_lean_*:N with the measured reason)
        ▼
   numbers line to belam only when necessary; otherwise silence = the loop is healthy
```
Template-first is the house rule (owner 19:0xZ/22:2xZ/22:3xZ): a fix that a template edit can carry goes back to master-sensei as a template line; code only where the trigger/resolver does not exist — and then shaped so the NEXT such change is a template edit. Scripts grown complex enough to want a CLI verb or an MCP call (rotate.py, send.py first) are yours to plan as such.

## §2 NEVER · RULES
Never: write `config:seats` rows or spawn (the Prime's, this formation — your old "only row writer" mandate is superseded 22:3xZ) · touch `moral:*` · `git rm` under `.agi/nodes` (retire = `status: deprecated` + move to `.agi/nodes/deprecated/<type>/`) · `grid.py checkout` · `grid.py commit --all` · rebase · force-push · `git add -A` · write in another post's worktree · run the suite outside a Prime-granted window (`.agi/sessions/verify-suite.lock` absent = free, F7) · AskUserQuestion (the pane has no interactive user).
Rules: **WINDOW RULE** — inside a granted merge-up window no post commits to MAIN; before every MAIN commit check `head -3 .agi/sessions/quorum/sensei-director.md` for GRANTED AND the lock file. Commit own paths only, exact pathspecs; push after every action; `index.lock` → wait. Prayers: the Jesus Prayer as the FIRST tokens of the session and the LAST before rotate-self — never per turn (owner 14:4xZ). Wordy output is a cost (owner 22:3xZ): graph addresses, never filesystem paths; one line where one line says it.

## §3 FLOOR (owner 03:2xZ): wake 0 / out 1
Wake = nothing: pin is spawn-written, ack answered `continue` by the predecessor, inbox/git-state/record are in STARTUP. Out = `rotate.py rotate-self --name sanctuary-master --role director --timeout 900 --force --stops '<one line>'` ALONE — the card is current because you wrote it DURING the work. Meter: `rotate.py meter --post sanctuary-master`; rotate at 0.47 (hook reminds at 0.37/0.41). master-sensei audits both sides of every rotation you make.

## §4 STATE + NEXT (gen 1, 2026-09-12 23:5xZ)
- SM.01 `hypothesis:l4-the-after-join-dm-is-one-line-per-entry-detail-only-on-refusal-or-nonzero-record-named-by-graph-address` (g15.25) — PLANNED @05581d799, ORDERED to sensei-director 23:4xZ. Next: review its merge-up by name → ACCEPT (note on node) / DEMOTE.
- Intake #2 (bare keyed rotate) was ALREADY cut by sensei-director as SL7.113/114/115 (harvested lean_proved:90; 114 landed 157 lines vs 120 ceiling — weigh at review, not a DEMOTE alone). Awaits Prime GRANT SL2#27/28; review by name when it lands: `git diff $(git merge-base season2/main season2/posts/sensei-director)..season2/posts/sensei-director -- extensions/agi/bin/rotate.py extensions/agi/tests/test_rotate_verb_resolvers.py`, negative probe per claim conjunct (rank gate upward refused, equal rank refused, unkeyed refused, dry-run resolves name/timeout/stops).
- SM.02 `hypothesis:l4-spawn-without-name-defaults-to-the-seat-row-name-for-every-non-prime-post` + SM.03 `hypothesis:l4-a-re-seat-after-a-dead-predecessor-rewinds-the-posts-read-cursors-to-the-dead-sessions-seating-time` — PLANNED 23:5xZ, ordered after SM.01 (both from my own seating: belam-S1-L4-XIX window killed; 2 calls hunting consumed dms).
- QUEUE from the Prime (belam XVIII 23:41Z dm, all g15; mint one node per round as the director frees, measure against the tip then): (A) mur-SL2.26 re-cuts SL7.93 (send nudge=False leaves dm unread → heal re-arms; type_input idle/busy; delivery literal), SL7.103 (Prime closeout g17_1_note refuses on in-progress record; _commit_rotation_record never gets record_path), SL7.106 (11 --pin tests hit OpenRouter unstubbed test_rotate.py:1517,1536,1666; conftest.py:488); (B) residues SL7.98 pred_pids `|`-join + dry-run refusal + gen_before row fallback; SL7.96 uuid session_ref treated as ref (seat_status.py:256, send.py:3829), session_name back-fill/clobber; SL7.92/101 GRANT exact-word, two-dot touch-set, failed diff ≠ touches-nothing, TimeoutExpired; SL7.105 heal re-exec on every HEAD move → gate on extensions/agi/bin/** diff; SL7.107 inherited:true on every rebuild, sensei.py to-key `-` guard; (D) suite leg 546 s vs 590 ceiling → --durations round. Order: SM.01 → 02 → 03 → 105 (spend) → 106 (spend) → 98 → 96 → 92/101 → 93 → 103 → 107 → D.
- SL7.117 ordered 23:5xZ (no SM node; director cuts it under g15.25): SL7.114/115 read `templates.<role>.timeout_s` / `.rotate_defaults` — keys write.py cannot write (no dotted nesting, master-sensei --dry-run 23:42Z). Re-cut to top-level `rotate_defaults` map; 0a = `set ranks […]` + `set rotate_defaults {…}`. Must land before the 0a line runs.
- sensei-director state 23:42Z: SM.01 dispatched (a00-2d7d67b8), SL7.116 stops-staleness dispatched (a00-e2759a34), SL2#27 queued for GRANT.
- SL2#27 LANDED @ed00e0796 (11/11, 4553/15, 2728/197/2925): reviewed by name 00:1xZ → 113-115 ACCEPT (notes @01b5ae4bd). Numbers + keygen ask to Prime 00:1xZ. Next merge-up #28 = SM.01 + SL7.116 (160 vs 50 ceiling — weigh: record threading) + 117; review by name when it lands.
- 00:29Z: SM.02 (0.9) + SM.03 (0.8) harvested; post carries SM.01+116+117+SM.02+SM.03 for #28 (queued behind point L4 49; tip 2d0a9170d). SM.04 (SL7.105 re-cut) + SM.05 `hypothesis:l4-the-suite-never-reaches-openrouter-one-autouse-stub-on-openrouter-get-unless-the-real-judge-flag-is-set` (SL7.106 re-cut) minted 00:3xZ, ordered in that order. Next from queue: 98 → 96 → 92/101 → 93 → 103 → 107 → D.
- SL2#28 LANDED @d22584a70 (11/11, 4621/15, 2757/197/2954): reviewed by name 00:5xZ → SM.01/SM.02/116/117 ACCEPT; **SM.03 DEMOTED** (experiment:a00-c387f696-8fdeca proved 0.8 → lean_disproved:60: the INBOX uses the READ_MARKER line, not a .state.json, so rewind never touches it — the motivating case). SM.03b noted on the hypothesis, ordered. Live: SM.04, SM.05.
- OWNER 00:5xZ (typed in my pane, relayed verbatim to Prime): GUI session labels should match posts + roles. Pointer: `--remote-control NAME` rotate.py:810-813; `<post>-<role>-gN` keeps the join key. Prime line rules; I plan it on the Prime's word.
- TRAP: a `send` line in double quotes eats backticks (F4) — single quotes only. TRAP 2: 532c11d68 committed under a live suite lock — the LOCK check printed but did not gate; ALWAYS `test -f .agi/sessions/verify-suite.lock && exit 1` BEFORE git commit, never after.
- 01:0xZ Prime: 532c11d68 ruled non-voiding; GUI labels = PLAN IT (rule: `<post>-<word>-g<N>`, session_label on the row, Prime keeps belam numeral). SM.07 `hypothesis:l4-the-gui-session-label-is-post-word-gen-derived-from-the-row-at-spawn-and-rotate-and-stored-as-session-label` minted; SM.06 (SL7.98) minted @4f34f6172. Order to director: SM.03b → SM.07 (owner-visible first) → SM.06 → SM.08 `hypothesis:l4-prepare-fetches-before-it-measures-behind-…` (master-sensei 01:14Z: prepare counts behind against the stale local ref before its fetch) → SM.09 `hypothesis:l4-the-dirty-tree-gate-on-a-shared-main-checkout-…` (master-sensei 01:15Z: dirty gate blocks on foreign dirt; scope to the merge touch-set) → SM.10 `hypothesis:l4-dispatch-performs-the-stale-base-sync-itself-…` (master-sensei 01:28Z: dispatch exit 3 hands the merge as text; 5 calls → 0) → SM.11 `hypothesis:l4-a-typed-after-join-dm-marks-its-own-inbox-copy-read-…` (master-sensei 01:29Z: typed dm + unread inbox copy = one wasted read per rotation). Then 96 → 92/101 → 93 → 103 → 107 → D.
- 01:16Z: SM.05 harvested (test-only, pin tests 24 green); SM.03b runs as iter **SM.31** (dispatch.py refuses letter ids). sensei-director rotated 17→18 at the Prime's 01:13Z boundary (directors → claude-sonnet-5 max; row 0458ae2c1). Gen 18 harvests SM.31 → dispatches SM.07 → SM.06 → asks SL2#29 (SM.04+SM.05+SM.31). My meter 0.19 window / 0.41 line; rotate at 0.47 line.
- Residue routed: (a) stops-slot staleness gate → sensei-director spawns SL7.116 after SM.01; (b) config:rotations ranks/timeout_s grammar + prime `delivery` SHAPE sentence (rotations.md:113) → master-sensei (template).
- Inbox: sensei-director dms 23:00Z/23:32Z read; master-sensei's 22:4xZ intake lines were NOT in the inbox (came via the card §4) — old dm backlog (alive/liaison/belam-XIII/rooms) is pre-formation history, unread on purpose.
## §5 BANKED
- OWNER 01:2xZ via Prime: posts get tools from the row — SM row `settings: ultracode` (8c9e1e066); successor launch exports CLAUDE_CODE_WORKFLOWS=1 + --settings ultracode → Workflow tool; put the word `ultracode` on the first line of a turn that runs a workflow. Next season rungs 5-8: tool enable/disable from the post template, bound to the post key — plan when the owner opens it.
- master-sensei alternative for SM.09 (worktrees for MAIN posts) — not taken; multiplies the F14 class.

## 🔴 Where it stops
```
waiting: sensei-director merge-up SL2#27/28 (SL7.113-115) + SM.01 round. Next command = review by name (§4 line 2), then `write.py <node> "note ACCEPT …" --actor sanctuary-master --role director`.
trap: `rotate.py meter --post sanctuary-master` → ERR pin not found (bootstrap said meter pending after join); the hook meter line works (0.02 at 23:5xZ) — use the hook, verify pin once after the after_join dm arrives.
```
