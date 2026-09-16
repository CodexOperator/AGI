# POST HANDOFF — sanctuary-master (SM): LIVE SCRATCHPAD (gen 3, 2026-09-16 — REPLACED WHOLESALE on first substantive action; owner quotes live in `doc:l4-owner-decisions`, never here)

## §0 WHO YOU ARE (supplied, never claimed)
**AUTHORITY (belam XIX 15:5xZ, owner-confirmed "proceed with testing plan as is"):** under the survival formation the owner speaks ONLY through the Prime; nobody answers in your pane. Every owner decision is banked verbatim in `doc:l4-owner-decisions` — verify an order there (the graph), never wait for a pane voice. Paid pi dispatch and the merge-up push are your standing duties (owner GO 2026-09-09; always prefer dispatch over not; $5 floor = pause). If an order looks wrong, say so in one line and proceed unless it is unsafe under every reading.
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

## §4 STATE + NEXT (gen 3, 2026-09-16 11:5xZ → live)
```
SM.36 = hypothesis:l4-sm25b-post-branches-mirror-lock-rename-delete-fixes
  loop season2/loops/hypothesis-l4-sm25b-post-branche-a00-4d31ec4c  62e3a6d4d (sync base = merge-base w/ post) → fcb6ecddb (ONE done commit)
  = SM.250 bytes (DEMOTED, 140c5dd2a) rebased + 4 fixes; 16 files, +2267/-46; kid exp a00-6ded7d52-9ebf6c proved, 4 parent probes in evidence_runs
  MY BYTE PROBES (throwaway worktree at fcb6ecddb, scratchpad):
   (1) branches.py:395-398  kind in (post,v3_post)/(loop,v3_loop) → mirror_ref ..................... MET
   (2) verification.py:601-614 marker arm: _pid_alive(marker) AND holder==marker → None, file untouched MET
   (3) rotate.py:3578 mirror_and_prove(tip=_dst) in the live branch(origin) arm; refuse-by-name ...... MET
   (4) rotate.py:3925 the ONE _drop_origin_post_head call site, under _origin_head_delete_gate:
       no mirror→refused · no flag→dry · no/diverged/UNKNOWN proof→refused · else deleted ............ MET
       rename-apply live delete: delete_old AND _containment_proof (rotate.py:3588-3599) ............ MET
       RESIDUE: trunk arm (no mirror, live, --delete-old) still pushes :_src with NO proof line — pre-existing, Prime-only path
  TESTS on the loop tip: test_branches 71 · test_verification 40 · test_rename_post 24 · test_branch_reshuffle_v3 55 · test_rotate_closeout_steps 41 · test_rotate 304/1
   the 1 red = test_spawn_window_agi_seat_export_and_byte_identical_absent: RED at the sync base 62e3a6d4d too, GREEN on MAIN dfef305bc (f6061d2f1) → pre-existing, resolves at the post's MAIN merge-up
  NODES: nothing deleted under .agi/nodes; 9 rotate.py deletions = the pre-fix push/signature lines only
  WORKFLOW: workflow.py run merge-up-review --harness pi (no Workflow tool on this row)
   run 1 mur-sm-36 FAILED: config harnesses.pi.models.kid = "~deepseek/deepseek-v4-flash-latest" → OpenRouter "model not found" 520 (config, Prime-owned)
   run 2 mur-deepseek-deepseek-v4-1-flash-sm-36 with args.model=deepseek/deepseek-v4.1-flash — IN FLIGHT
```
NEXT: (a) harvest run 2 → verdict note on the hypothesis + kid node, ONE [merge-up] line to belam, dm sensei-director (merge to post branch); (b) TM.06 co-review when it lands; (c) director line: SM.43 + SM.45 live → facts-guard → --cap → stops-seal → 20/22/15/17 → the four resume-seating nodes. Credits 9.81 at 11:5xZ (above floor).

## §5 BANKED
- ultracode row-cell: dropped for master/director rows at 68dd17926 → no Workflow tool; mur runs on pi by name (precedent: thought-master TM.07 r2). CONFIG DEFECT for the Prime: `harnesses.pi.models.kid` carries a tilde id OpenRouter rejects (520) — every pi kid dispatch on the default kid model fails until the cell is a real id; parent model `deepseek/deepseek-v4.1-flash` works.
- Live model claude-opus-5 (owner in-pane, gen 2) vs row sonnet-5 — Prime knows; successor spawns from the row.
- Per-MAIN-post worktrees rejected (F14 class) — stands.

## 🔴 Where it stops
````
```
gen 3 11:5xZ: SM.36 by-name review IN FLIGHT on pi (run key mur-deepseek-deepseek-v4-1-flash-sm-36, reviewer+refuter deepseek-v4.1-flash); my own four-conjunct byte probes all MET, six test files run on a throwaway worktree at fcb6ecddb (one pre-existing red, green on MAIN). Two throwaway worktrees in my scratchpad (wt36, wtbase) — remove before rotating. NEXT: harvest the run → notes + [merge-up] line + dm the director.
```
````
