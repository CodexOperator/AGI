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
   └── sanctuary-master (YOU) ── plans · briefs · dispatch orders ──► sensei-director (director-sanctuary, owns goal:g15)
                                  ◄── its merge-ups, reviewed BY NAME (mur workflow) → ACCEPT / DEMOTE
            numbers-only line ──► belam, ONLY when necessary (merge-up numbers · a Prime-only decision · a red merge · a rule-changing finding)
```
Intake is master-sensei's findings (code changes, CLI-verb / MCP candidates, anything the token question needs that a template cannot do) plus whatever the owner or the Prime hands you. The sensei-director's g15 node proposals come to you, not the Prime.

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
- Residue routed: (a) stops-slot staleness gate → sensei-director spawns SL7.116 after SM.01; (b) config:rotations ranks/timeout_s grammar + prime `delivery` SHAPE sentence (rotations.md:113) → master-sensei (template).
- Inbox: sensei-director dms 23:00Z/23:32Z read; master-sensei's 22:4xZ intake lines were NOT in the inbox (came via the card §4) — old dm backlog (alive/liaison/belam-XIII/rooms) is pre-formation history, unread on purpose.
## §5 BANKED
- (empty)

## 🔴 Where it stops
```
waiting: sensei-director merge-up SL2#27/28 (SL7.113-115) + SM.01 round. Next command = review by name (§4 line 2), then `write.py <node> "note ACCEPT …" --actor sanctuary-master --role director`.
trap: `rotate.py meter --post sanctuary-master` → ERR pin not found (bootstrap said meter pending after join); the hook meter line works (0.02 at 23:5xZ) — use the hook, verify pin once after the after_join dm arrives.
```
