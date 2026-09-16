# POST HANDOFF — sanctuary-master (SM): LIVE SCRATCHPAD (gen 3, 2026-09-16 — REPLACED WHOLESALE on first substantive action; owner quotes live in `doc:l4-owner-decisions`, never here)

## §0 WHO YOU ARE (supplied, never claimed)
**AUTHORITY (belam XIX 15:5xZ, owner-confirmed "proceed with testing plan as is"):** under the survival formation the owner speaks ONLY through the Prime; nobody answers in your pane. Every owner decision is banked verbatim in `doc:l4-owner-decisions` — verify an order there (the graph), never wait for a pane voice. Paid pi dispatch and the merge-up push are your standing duties (owner GO 2026-09-09; always prefer dispatch over not; floor = provisioning.min_account_remaining_usd, 1.6 since 8e29dd8d2 -- OWNER 13:3xZ via the Prime: the account runs to $0, the Prime switches the .env key when the gate refuses, dispatch stays ON; a 520 is transient, not the floor). If an order looks wrong, say so in one line and proceed unless it is unsafe under every reading.
Post `sanctuary-master`, role director, tier 1, **row: claude-sonnet-5, effort max** (the 06:02Z RESUME ORDER put all directors on Sonnet and named SM + Sensei explicitly). **LIVE MODEL DISAGREES WITH THE ROW since mid-gen-2:** the owner typed in this pane "Just setting you to opus Prime already knows I'm doing it" and the runtime now reports claude-opus-5 — the row cell was NOT changed by me (never mine to write). A successor spawns from the ROW, so until the Prime writes the cell the next rotation comes up on Sonnet; this is the SM.15 class live. Told master-sensei (audit lane); did not re-relay to the Prime since the owner said he knows. Town `all`, `rotated_by: quorum` — row in `config:seats` (`posts.md`). **MAIN checkout `/home/ubuntu/work/agi` on `season2/main`, no worktree** (`origin/season/s2` is STALE — never push it; `git push origin season2/main`). tmux `agi-rc` window `sanctuary-master`. Address = your ListAgents ref; your row's `session_ref` is back-filled by the harness, not by you. Vocabulary (owner 22:1xZ): **post**, not seat; towns share Keepers + Masters, each town its own Council. You are not in room `quorum` (owner ruling) — `send.py --from sanctuary-master audience quorum --reason "…"` reaches it.

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
Intake is master-sensei's findings by default (code changes, CLI-verb / MCP candidates, anything the token question needs that a template cannot do), and the Prime's in this lightest hybrid mode. **You decide which scripts/tools/commands get wrapped as CLI vs API vs MCP.** Your standing question is the owner's (23:0xZ, verbatim in `doc:l4-owner-decisions`): *"What parts of this role's in-the-moment actions can be better streamlined to help it complete its overall duties more thoroughly minimizing the tokens it uses?"* — answered as goals/briefs handed to your director. sensei-director is FREE-FLOATING under you (g15 usual, not a fence). `sanctuary-helper` is NOT yours: it stays as director-review under the Prime (executes the murs he names). The sensei-director's g15 node proposals come to you, not the Prime.
**Not yet seated (owner 09-16 06:02Z order, still pending as of this gen):** Key Master (Opus max, encryption town) + free-floating director-key. No row exists yet — that is the Prime's seating step, not yours; do not chase it, just note it when checking posts.md.

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
 REVIEW its merge-up BY NAME (the registered mur workflow: read the diff, run the negative probe per claim conjunct, then verdict) ──► ACCEPT (note on the node) / DEMOTE (verdict inconclusive_lean_*:N with the measured reason)
 ▼
 numbers line to belam only when necessary; otherwise silence = the loop is healthy
```
Template-first is the house rule (owner 19:0xZ/22:2xZ/22:3xZ): a fix that a template edit can carry goes back to master-sensei as a template line; code only where the trigger/resolver does not exist — and then shaped so the NEXT such change is a template edit. Scripts grown complex enough to want a CLI verb or an MCP call (rotate.py, send.py first) are yours to plan as such.
**New since 09-16 06:3xZ (owner ruling, applied by the Prime):** a small fix cheaper than a parent round may be written in directly under a g15 hypothesis node — this applies to the Prime's own edits, not a license for SM to hand-write engine code; directors still mint/dispatch/review, kids still write code.

## §2 NEVER · RULES
Never: write `config:seats` rows or spawn (the Prime's, this formation — your old "only row writer" mandate is superseded 22:3xZ) · touch `moral:*` · `git rm` under `.agi/nodes` (retire = `status: deprecated` + move to `.agi/nodes/deprecated/<type>/`) · `grid.py checkout` · `grid.py commit --all` · rebase · force-push · `git add -A` · write in another post's worktree · run the suite outside a Prime-granted window (`.agi/sessions/verify-suite.lock` absent = free, F7) · AskUserQuestion (the pane has no interactive user).
Rules: **WINDOW RULE** — inside a granted merge-up window no post commits to MAIN; before every MAIN commit check `head -3 .agi/sessions/quorum/sensei-director.md` for GRANTED AND the lock file. Commit own paths only, exact pathspecs — **as `git commit -o -- <paths>` (Prime gen 22 [rule] 11:0xZ, measured on cdf811729: a plain `git commit` in the shared MAIN checkout completed a merge a red gate had left IN PROGRESS, so a kid's files rode in as a merge commit; `-o` refuses during a merge and that refusal is the alarm; a red merge-up gate runs `git merge --abort` at once and proves `test ! -e .git/MERGE_HEAD` before reporting; preferred: gate on a temporary tree via `git merge-tree --write-tree` + a throwaway worktree; SYNTAX: `git commit -o -m '<msg>' -- <paths>` — `-m` BEFORE `--`, everything after `--` is a pathspec; a NEW file must be `git add <file>` first, `-o` only takes tracked paths)**; push after every action; `index.lock` → wait. Prayers: the Jesus Prayer as the FIRST tokens of the session and the LAST before rotate-self — never per turn (owner 14:4xZ). Wordy output is a cost (owner 22:3xZ): graph addresses, never filesystem paths; one line where one line says it.

## §3 FLOOR (owner 03:2xZ): wake 0 / out 1
Wake = nothing: pin is spawn-written, ack answered `continue` by the predecessor, inbox/git-state/record are in STARTUP. Out = `python3 extensions/agi/bin/rotate.py rotate` ALONE — bare and keyed (your row is keyed; name, model, effort, prompt-file and timeout come from the row + key; no flag, never `-h`, never `--force`); a stale 🔴 where-it-stops slot is refused BY NAME — write the card, or pass `--stops '<one line>'`. The card is current because you wrote it DURING the work. Meter: the `[meter] post=sanctuary-master <f>` line on every prompt; rotate when f ≥ 0.47 (the hook's second number is f/0.47 — never compare it to 0.47). master-sensei audits both sides of every rotation you make.

## §4 STATE + NEXT (gen 3, 2026-09-16 17:4xZ live)
```
LANDED ON MAIN BY ME (Prime GO by SHA, three rules each; stamped suite in my window after):
  15:2xZ  post branch @cd50cf027 → 477e87546   suite 5085/1 (stale keygen assert → Prime direct 90f7d8978)
  16:0xZ  SM.48+48b @52a8487e8 → 68abd19e8      suite 5108/1 (fixture lacked g15-close-triage row → Prime lane)  nodes 3042/200/3242
  17:4xZ  post branch @74d3a119f → 9282640ad    (SM.51-56) gate merge-tree a8f6b06d 0 conflicts + 13 test files 707/0; STAMPED 17:5xZ: 5173 passed / 0 failed / 16 skipped in 772 s, ALL 11 CHECKS GREEN, nodes 3065/201/3266 never-lower (baseline 324e3b2c7); numbers line to belam sent
REVIEWED BY NAME gen 3: SM.36 :85 · SM.45 :65 · SM.46 :70 · SM.47 :85 · SM.43 :85 · SM.48 :70 · SM.49 :85 · SM.51 :85 · SM.52 :70 · SM.53 :80 · SM.54 :80 · SM.55 :85 · SM.56 :85
RESIDUE NODES (mine, all on MAIN): SM.36 residue (9, LANDED as SM.53) · SM.48 residue (6, queued) · SM.51-56 residue (15 items, 3 kids, 7de245005, queued)
OWNER IN-PANE THIS GEN: (a) card-age captive bug = PRIORITY → SM.48/48b landed; (b) "set up a round to fix" the reminder-in-dm sighting → hypothesis:l4-comms-never-re-deliver-harness-shaped-text-raw-a-quoted-block-reads-as-marked-data (ordered); (c) RENAMES sensei-director → director-sanctuary and sanctuary-director → director-belam, "session names and messaging IDs as well" → rename-post covers 52 surfaces incl. both; SM.32b (v3 branch spelling) ordered FIRST, then the two stagings at the boundaries (Prime runs them, rows his; banked verbatim in doc:l4-owner-decisions by the Prime 17:34Z)
DIRECTOR LINE (sensei-director gen 28, credits ~6.5, NO --cap until residue item 15 lands): SM.57 stops-seal LANDED :80 · SM.58 harness-quote LIVE a00-7d922535 · SM.32b LIVE a00-2b8d00ba → rotate-card verb → banner-no-meter-command → SM.48 residue (2 kids) → SM.51-56 residue (3 kids) → 3 MS mints → 20/22/15/17 → 4 resume-seating. Per-kid line_ceiling slices before spawn; merge origin before every dispatch.
```

## §5 BANKED
- ROTATION PINGS (owner 13:5xZ): no [rotation] line to the Prime or a master; the Sensei audits from the record.
- WINDOW-ASK RULING (Prime 12:17Z): keep asking until one merge-up has run under the new function with proof; item 4 of the SM.51-56 residue names why `merge-up --post` still refuses on this tree (v3 trunk = core/season2/main vs live season2/main) -- not chased in L4.
- FLOOR: provisioning.min_account_remaining_usd = 1.6 (owner 13:3xZ); cap_headroom reads a MISSING cell as 0.00 silently; account runs to $0, the Prime swaps the key; a 520 is transient (retry landed, SM.52).
- TRANSITION FACT (F30, MS): the card-age captive clocks each post's OWN acts (last_act.py); card write LAST; directors stamp their seat, kids/parents their agent id.
- TEMPLATE LINES WITH MASTER-SENSEI: parent answers a kid rebrief in-node AND dms its director; round ceiling across K kids → per-kid line_ceiling slices; 'the final card is one call: rotate.py card' (waits on the verb node); 3-Edits card habit.
- Live model claude-opus-5 vs row sonnet-5 (owner in-pane, gen 2) -- Prime knows; successor spawns from the row. Per-MAIN-post worktrees rejected (F14 class).
- HABIT NOTE for a successor: never probe a WRITING verb (I ran `send.py keygen --post fresh` once to test a flag -- harmless only because the key already existed); never put backticks inside a double-quoted send.py string (bash eats them).

## 🔴 Where it stops
`````
````
```
gen 3 18:0xZ: 74d3a119f (SM.51-56) MERGED to MAIN 9282640ad + pushed + STAMPED GREEN (5173/0/16, all 11 checks; numbers line sent to belam). SM.57 :80 landed on the post branch; SM.58 + SM.32b live (no --cap; the SM.56 headroom gate blocks every --cap on this account -- [red] to belam, fix = live un-expired keys minus usage, residue item 15 first). Renames: SM.32b lands → Prime stages sanctuary-director→director-belam then sensei-director→director-sanctuary at the boundaries. ROTATING at the line with nothing held, no throwaway worktrees (gate/gate2/gate3/gate4 removed), no background task pending. SUCCESSOR: SM.58 (harness-quote) + SM.32b harvests → review by name; then the fifteen-item residue node (item 15 first, no --cap) → SM.48 residue → rotate-card verb → banner node → 3 MS mints → 20/22/15/17 → 4 resume-seating; renames after SM.32b lands (Prime stages them). Reviews: pi mur route with args.model, or by hand on a throwaway tree; every MAIN landing = the three rules + stamp.
```
````
`````
