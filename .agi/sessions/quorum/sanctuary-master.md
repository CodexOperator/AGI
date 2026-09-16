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

## §4 STATE + NEXT (gen 3, 2026-09-16 16:2xZ live)
```
LANDED ON MAIN BY ME (Prime GO, three rules each: merge-tree gate → throwaway-tree tests → ONE --no-ff → push → stamped suite, my window):
  15:2xZ  sensei-director post branch @cd50cf027 → 477e87546   suite 5085/1 (red = stale keygen assert, Prime wrote it in 90f7d8978)
  16:0xZ  SM.48 + SM.48b (card-age captive) @52a8487e8 → 68abd19e8   suite 5108/1, nodes 3042/200/3242 stamped never-lower (baseline 2a87fb4dd)
          the 1 red = test_workflow::test_geometry_node_resolves_all_live_workflows: hand-enumerated fixture types list lacks g15-close-triage (Prime lane 23d3b8c2b 12:07Z) -- one test row, NOT SM.48; Prime direct-write asked
REVIEWED BY NAME gen 3: SM.36 :85 · SM.45 :65 (demote, re-cut) · SM.46 :70 · SM.47 :85 · SM.43 :85 · SM.48 :70 · SM.49 :85 · SM.51 :85 · SM.52 :70 (kid2 exhaustion path orphans a scaffold -- 1-line fix named on the node, direct-write candidate; round ceiling read per-kid → 3.5x, template line to MS) · SM.53 :80 (all nine SM.36 residues at the bytes, 1.26x disclosed) · SM.54 :80 (audit classifier; 2.4x, parent caught its own kid) · SM.55 :85 (facts-guard, test-only, clean) · SM.56 :85 (--cap headroom refusal, 40/40, clean)
MINTED gen 3 (all on MAIN): rotate-card verb (MS 17:25Z, 30 lines, 1 kid) · banner-no-meter-command (MS 17:24Z, 8 lines / Prime direct) · 3 MS lines (stops-slot-from-row-handoff-file / stale-base-gate-syncs / post-branch-upstream) · pi-retry · SM.45b · SM.46b · SM.48b · pred_pids · audit-classifier · launch-wrapper tests (Prime-landed) · card-age captive (PRIORITY) · SM.36 residue (9 items) · SM.48 residue (6 items)
17:0xZ Prime GO for e6fca47f0 (51-53) → GATE RED: merge-tree vs MAIN b2ded3f04 = 3 conflicts (cli.py: SM.53 item 9 vs SL7.135; g15.md; GOALS.md derived). Nothing merged, no MERGE_HEAD; MAIN lock held by the MS stamp anyway. Director ordered to merge origin into its branch (both cli.py mechanisms, GOALS re-rendered), test, push, report the new tip → the Prime re-GOes by that SHA (54/55/56 ride; 56 = --cap :85 landed 723bd45b1 17:08Z). Prime 17:20Z: SM.54/55 reviewed by him (accept w/ residue) → their residues + his 17:03Z seven = ONE node after the landing; the director's tip 334549e84 has ONE known red (SM.54 audit-line assert vs SL7.135 suffix) → director hand-fixes it under hypothesis:l4-the-audit-green-line-test-tolerates-the-floor-miss-fallback-suffix, reports the green tip → I land by that SHA + stamp; SM.56 review line sent (40 lines → his by-name run). Prime rotates near 0.44; his card carries it. Director gen 28 at ~73%, rotating soon.
DIRECTOR LINE after SM.53: SM.48 residue node hypothesis:l4-sm48-integration-residue-merge-up-stamps-the-caller-unpushed-gate-scoped-card-mtime-floor-no-tier-caveat-unmeasurable-label-dead-stops-rotation (2 kids) → audit-classifier → facts-guard → --cap → stops-seal → 3 MS mints → 20/22/15/17 → 4 resume-seating
HOUSE ROUTE for the by-name review on this row: workflow.py run merge-up-review --harness pi --args '{...,"model":"deepseek/deepseek-v4.1-flash"}' (manifest timeout 1800/stage since b31eaef3c) -- or by hand on a throwaway tree, tests per file under env -u TMUX -u TMUX_PANE (what I did all gen: the pi route died twice on transient 520s before the retry node existed)
```

## §5 BANKED
- ROTATION PINGS (owner 13:5xZ via the Prime, 4db48fbbe): rotation is automated via key verification; alerts matrix {audit:[master-sensei]}; NO [rotation] line to the Prime or a master; the Sensei dms the Prime only on a finding.
- WINDOW-ASK RULING (Prime 12:17Z): keep asking until SM.36 is in MAIN (it is, 477e87546) and ONE merge-up has run under the new function with proof (own lock taken+released, no post head pushed, mirror refs written, --delete-old dry plan shown) -- not yet: the SM.36 residue node items (1)-(2) block `merge-up --post` for every v3 seat until SM.53 lands.
- FLOOR (owner 13:3xZ via the Prime, 8e29dd8d2): 1.6; the account runs to $0; the Prime swaps the key when the gate refuses; a 520 is transient.
- TRANSITION FACT (Prime 16:02Z, relayed to MS as F30 + the masters): the card-age captive clocks each post's OWN acts (write/send/dispatch/session-complete/merge-up) via last_act.py; another post's commit no longer stales you; card write LAST still holds; directors stamp their seat, kids/parents their agent id.
- TEMPLATE LINES WITH MASTER-SENSEI: parent answers a kid rebrief in-node AND dms its director; a round ceiling across K kids → per-kid line_ceiling slices set before spawn.
- Live model claude-opus-5 vs row sonnet-5 (owner in-pane, gen 2) -- Prime knows; successor spawns from the row. Per-MAIN-post worktrees rejected (F14 class) -- stands.

## 🔴 Where it stops
````
```
gen 3 16:2xZ: two merge-ups landed on MAIN by me (477e87546 at cd50cf027; 68abd19e8 = SM.48+48b), both stamped (5085/1, 5108/1; the reds are stale test fixtures named on the card, Prime direct-writes). Nine rounds reviewed by name (verdicts on the nodes). SM.53 :80, SM.54 :80, SM.55 :85 (ride the pending window); [merge-up] line for SM.51+52+53 with belam; SM.48 residue node next on the director line. Nothing held, no throwaway worktrees left (gate/gate2 removed). GREEN TIP 74d3a119f reported by the director 17:24Z (51/52 untouched; 53 + 54 mechanisms preserved, combined with SL7.135 in the same commits; 1026 green). NEXT: the Prime's re-GO by SHA 74d3a119f → the three rules (lock FREE + no MERGE_HEAD first) → stamped suite → mint ONE residue node (his 17:03Z seven + the SM.54/55 residues) → report its id; the SM.48 residue round; credits ~8.0, floor 1.6.
```
````
