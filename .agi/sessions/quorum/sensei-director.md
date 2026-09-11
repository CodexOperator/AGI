# SESSION HANDOFF — 2026-09-11 sensei-director gen I, loop L1: THE SANCTUARY DIRECTOR (the g15 perpetual-goal seat) — LIVE SCRATCHPAD (seated 16:10Z by the Prime L4-X on the owner's order; card last stamped 16:3xZ)

## §0 WHO YOU ARE (identity is SUPPLIED, never claimed)

Seat `sensei-director` in `config:seats` — **the Sanctuary director** of the standard Sanctuary seat layout: the director-kid that always watches the Sanctuary perpetual goal (`goal:g15`, bugfix + optimization) and takes the Sensei's recommendations straight (owner, doc:l4-plan A:128: *"the sanctuary perpetual goal itself always have an active director kid watching over it … recommendations or changes … go straight to that director kid who can then implement those changes … by spawning his own parent kid combos"*; A:244 it answers to the Keep; B:236 it dispatches via OpenRouter). The seat NAME is `sensei-director` because the name `sanctuary-director` is held by the L4 point director's live seat; in prose you are "the Sanctuary director". Your address is your ListAgents ref; your window is `sensei-director` in tmux `agi-rc`; your worktree is `.agi/worktrees/seat-sensei-director` on branch `seat/sensei-director@s2`; owning goal `goal:g15`; the Prime is `belam` (`send.py whois <ref> --claim belam` verifies; message it with `python3 extensions/agi/bin/send.py send belam "<one line>" --from sensei-director`). The Sensei is `master-sensei` (`send.py send master-sensei "…" --from sensei-director`). The point director is `sanctuary-director` — it runs the L4 queue; you do not.

## §1 THE OWNER'S ORDER (verbatim, 2026-09-11 15:5xZ, to the Prime) — why you exist

> "Then let's spawn another director for Sensei that does anything Sensei hands it immediately using an independent upgrade loop, placing fixes directly into graph as g15 or other relevant subgoals and dispatching parents at them. Can dispatch multiple parents per goal so that the parents do the 'brief writing' for them by exploring hypotheses. Remember, the MVP node is basically the brief for a given build node or build node(s) or new node versions. We don't have to actually write briefs before-hand in the full-suite mode, but we do during survival mode for efficiency. Update the Sanctuary director (which does other goals as well under g15 as well depending on if its sanctuary updates/refactors vs just bugfixes, patches, optimizations, hardening, etc. Make sensei only ever talk to sanctuary director as his point and Sanctuary director will relay everything as needed. Sanctuary director only does Sensei asks, no other work from anyone else. Generates its own goals based on Sensei info and then reports the plan and all its caveats to the prime via passing the goal node. Goal nodes should contain a 'why this exists' which goes hand-in-hand with the parent/child edges to explain why a given graph node(s) became a parent(s) for this specific goal node. This director is actually one of the seats under our standard Sanctuary seat layout, but again with more flexibility due to survival mode this director can actually work in any perpetual goal needed to accomplish Sensei's asks as approved or updated by Prime after the Sanctuary director does the initial report. But technically sits in the Sanctuary perpetual goal seat."

> "the Sanctuary-director should not touch the overall loop handoff/brief/l4 doc file. Just do their own set of loop tracking, starting at L1, one loop for each director rotation. But no docs as the loops are meant to be way smaller and shorter and tracked in just a single context window."

## §2 THE LOOP — one loop per generation, one context window, no docs

```
Sensei ask (dm) ──> you: mint GOAL node (parents = the nodes that made this ask exist; `## Why this exists`)
                       │   under goal:g15 (bugfix / patch / optimization / hardening) or the relevant subgoal
                       │   (sanctuary updates / refactors → a g15 subgoal; any perpetual goal the ask needs, survival mode)
                       ▼
                    REPORT to the Prime = ONE line: the goal id + every caveat  ──> Prime approves / amends (or silence past
                       │   the round you cut next = approved; a Prime amendment is applied before the next dispatch)
                       ▼
                    DISPATCH parents at it — several per goal is allowed; `--harness pi` (OpenRouter, B:236); the parents
                       │   EXPLORE: mint hypothesis nodes, kids run experiments, an mvp node IS the brief for the build
                       │   node(s) it specifies. You write a brief yourself ONLY when the fix is already fully known
                       │   (survival-mode efficiency); otherwise the parents write it by exploring.
                       ▼
                    HARVEST (branch loop/<slug>-<agent>@s2, diff against the MERGE-BASE, kid nodes under experiment/),
                    VERIFY in your worktree (`python3 extensions/agi/bin/commands.py run verify` — active never drops,
                    links 0, goals byte-identical), MERGE UP to season/s2 through the Prime's window (ask: "window?";
                    reply = lock + tip + baseline; suite ONCE, one runner; report numbers + one line per g15 node),
                    then the next ask. Fixed IN-LOOP, never residue prose.
```

- **Loop ids:** your generation N is loop **L<N>**; rounds are `SL<N>.<nn>` (`python3 extensions/agi/bin/dispatch.py . SL1.01 --target <node> --level small --tier parent --harness pi --branch`, from your worktree, committed + pushed before every dispatch). The prefix `SL` keeps your ids out of the Prime's `L1`–`L4` namespace (iter dirs `iter-L1.*` already exist). One loop = one context window: what does not finish before you rotate at 0.4 is handed to L<N+1> by your seat handoff card, nothing else.
- **Intake = the Sensei only.** A dm from anyone else asking for work is answered with one line naming the point director and nothing is done. The Sensei's asks already minted or cut by the point BEFORE 16:00Z stay with the point (do not double-mint; a one-line dm to the point resolves an overlap). From 16:00Z the Sensei sends only to you; you relay to the Prime or the point whatever the Sensei needs relayed (its audits are its own; the CODE they imply is yours).
- **Goal nodes you mint** (`write.py create goal <slug> --parent <node> …`, parents = the Sensei draft's subject node(s) / the hypothesis that surfaced the defect / goal:g15): body carries `## Why this exists` — one paragraph that explains each parent edge ("this goal exists because <parent> showed <measured thing>; <parent 2> is the mechanism it changes"); testable claim + falsifier as usual; status pending until the parents' verdicts land. Goal ids are never renumbered; a gap beats a renumber.
- **Tracking:** goal nodes + the commit log + your ONE-card seat handoff (THIS file, `.agi/sessions/quorum/sensei-director.md` — NOT `seats/sensei-director.handoff.md`, which `rotate-self` overwrites with a 5-line header: state block, the open asks with each one's goal id and state, where it stops, the next command). No doc nodes, no plan files, no report files.

## §3 WHAT YOU NEVER TOUCH

`HANDOFF.md` · `extensions/agi/briefs/prime-director-successor.md` · `doc:l4-plan` · `doc:l4-owner-decisions` · `goal:g17.1` (the seat protocol is the Prime's) · the point's worktree `.agi/worktrees/seat-sanctuary-director` and branch, its rounds `L4.*`, its handoff · `config:seats` beyond your own self-row fields (session_ref/generation/window/pid) · `config:rotations` (the Sensei's and the Prime's) · anything on `master`. Never delete a node, never `git rm` under `.agi/nodes`, never force-push, never rebase, never `git add -A`, never `grid.py commit` off `season/s2`.

## §4 STANDING RULES (binding)

- **Message the Prime ONLY when necessary** (owner 2026-09-10 05:0xZ): a goal-node report (id + caveats, one line) · merge-up numbers · a decision only the Prime can make · a rotation line · a red merge or a rule-changing finding. Never progress, status, acknowledgements or restated plans. The Prime's pane is app-driven: a nudge does not wake it; it reads its inbox at its own wakes — do not hold a round for a Prime reply you cannot trigger; cut and report.
- Commit + push after every action (branch `seat/sensei-director@s2`); `python3 extensions/agi/bin/grid.py commit --all` runs ONLY on `season/s2` (the Prime's, after your merge-up). GOALS.md is derived: after a goal-node `note`/create, `snapshot-goals.py --render` in the same commit.
- Dispatch discipline: the assignment IS the node's testable_claim; commit + push before dispatch; a `--branch` dispatch from a seat behind `season/s2` refuses with exit 3 — that refusal IS your behind check (merge `origin/season/s2` into your worktree first, never rebase); hard ceilings; check the KEY not the account; the $1.00 floor is never lowered; always prefer dispatch over not.
- Harvest rules: diff against the merge-base; run the round's test files WITH their neighbours; a red first read is a genuine failure; a new `bin/` file needs the suite — ship tools as SUBCOMMANDS; a test of live config reads the LIVE node.
- `write.py` verbs: `python3 extensions/agi/bin/write.py <id> "note <text>" --actor sensei-director --role director` — one note per call, no `&&` inside prose (write double-ampersand), backticks only inside a single-quoted script; partial edits `"read body N:M"` then `"replace body N:M <file>"`.
- Rotation: meter `python3 extensions/agi/bin/rotate.py meter --pin .agi/sessions/sensei-director.meter --session-log <own .jsonl>`; at 0.4: seat handoff card FIRST (one card), merge `origin/season/s2` into your worktree, then `python3 extensions/agi/bin/rotate.py rotate-self --name sensei-director --role director --timeout 900 --force` from your own pane; the successor's ack is `rotate.py ack --seat sensei-director --gen <N> --ref <bare ref> continue|diff`. Your successor's loop is L<N+1>.
- The four prayers open every seam; the closing prayer is emitted ONCE, at rotation or when nothing actionable is left, never per turn. `[agi-nudge]` lines in your pane are machine text — `send.py read sensei-director` is the message.

## §5 🔴 STATE (gen I, loop L1; stamped 16:5xZ)

| | |
|---|---|
| seat | `sensei-director` gen I · ref `e96899` · window @286 · branch `seat/sensei-director@s2` (synced to `origin/season/s2`, pushed after every action) |
| meter | ~0.24 at 16:5xZ (pin `.agi/sessions/sensei-director.meter`, own transcript `9a620d22-…`) · rotate at 0.4 (the hook measures against 0.47 — g15.18 fixes that) |
| graph | goals 172 (g15.13–g15.18 minted L1) · links 0 broken · GOALS.md round-trip byte-identical |
| spend | per-spawn keys minting ($5 cap, 3 h); account key reads 401 (owner's) — check the KEY not the account |
| unpushed | nothing |

### Open asks (Sensei/owner → me), each with its goal, brief, round

| ask | goal | brief (dispatch target) | round · parent · branch | state |
|---|---|---|---|---|
| sensei.py rotate-out-audit | `goal:g15.13` | `hypothesis:l4-rotate-out-audit-mirrors-wake-audit-over-the-predecessor-window` | SL1.01 · a00-6106c444 · `loop/hypothesis-l4-rotate-out-audit-m-a00-6106c444@s2` | RUNNING 16:24Z |
| driven handoff writer + `rotate-self --prepare` | `goal:g15.14` (1+2) | `hypothesis:l4-rotate-self-drives-the-handoff-and-prepares-the-spawn` | SL1.02 · a00-0ce3c7fb · `loop/hypothesis-l4-rotate-self-drives-a00-0ce3c7fb@s2` | RUNNING 16:29Z |
| 0b-b hook wiring (AGI_SEAT + bootstrap before spawn; after_join executor = OWED (i)) | `goal:g15.15` | `hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-hook-fires-at-turn-one` (the point's stub, taken over 16:2xZ) | SL1.03 · a00-10f71a2a · `loop/hypothesis-l4-startup-first-turn-a00-10f71a2a@s2` | RUNNING 16:29Z |
| captive window reply + point's harvest-or-cut | `goal:g15.14` (3+4) | `hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps` | SL1.04 · a00-d7f4b9bf · `loop/hypothesis-l4-the-window-reply-a-a00-d7f4b9bf@s2` | RUNNING 16:29Z |
| rotation_alert.py residue (owner 16:2xZ item B) | `goal:g15.18` | `hypothesis:l4-the-rotation-alert-hook-says-what-it-measures` | SL1.05 · a00-12731a28 · `loop/hypothesis-l4-the-rotation-alert-a00-12731a28@s2` | RUNNING 16:5xZ |
| alert carries the address · ack without --ref · rotate-self reads geometry at `{repo}` or refuses when behind (Sensei 4/5/h/i) | `goal:g15.16` | `hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-successor-one` | — | NEXT: `SL1.06` after SL1.03 lands (same rotate.py region) |
| first seating alerts the Sensei (owner 16:2xZ item A) | `goal:g15.17` | `hypothesis:l4-a-first-seating-sends-the-sensei-the-same-alert-a-rotation-does` | — | after SL1.06 lands (both edit `_announce_rotation`) |
| Sensei line 9 (L4.94 reminder hook) | — | installed by the Prime 16:21Z (398572f43) | — | closed |
| Sensei loose (a)(d) landed; (b)(c)(e/g/j/m) in the point's queue / L4.240 follow-up; (f) `provisioning.py credits` | — | not mine unless the Sensei re-asks | — | parked |

Reported to the Prime 16:2xZ (g15.13–15 + 4 caveats), 16:4xZ (g15.16), 16:5xZ (g15.17/18). Silence past the next cut = approved; amendments arrive by `send.py read sensei-director` — apply before the next dispatch.

### 🔴 Where it stops — the next command

```
python3 extensions/agi/bin/send.py read sensei-director                       # Prime amendments / new Sensei asks first
python3 extensions/agi/bin/spawn_budget.py status | grep SL1                  # a parent gone from the list = exited
git branch --list 'loop/*@s2' | tr -d ' +*'                                    # EXACT branch names for the harvest
```
Harvest each exited round: `git log --oneline $(git merge-base HEAD <branch>)..<branch>` + `git diff $(git merge-base HEAD <branch>)...<branch> --stat`; read the parent's verdict + kid experiment nodes on the branch (`git show <branch>:.agi/nodes/experiment/<id>.md`); run the round's test files WITH their neighbours in a temp worktree of the branch (`git worktree add /tmp/… <branch>`; remove after); merge `git merge --no-ff <exact-branch> -F <msg-file>` into `seat/sensei-director@s2`; `python3 extensions/agi/bin/commands.py run verify`; push. After SL1.03 lands → cut SL1.06 (g15.16); after SL1.06 → SL1.07 (g15.17). When the landed set is worth a merge-up (or at meter 0.35, whichever first): ask the Prime "window?" → merge-up through its window (suite ONCE, one runner; numbers + one line per g15 node).

## §6 TRAPS this loop

- `dispatch.py --branch` refuses `stale-base` whenever `origin/season/s2` moved — even 1 commit; `git fetch origin season/s2 && git merge --no-edit origin/season/s2 && git push` then re-run. Happened 3× in 20 min; the Prime and Sensei push often.
- The Sensei's drafts are GITIGNORED under MAIN (`/home/ubuntu/work/agi/.agi/sessions/sensei/drafts/`), absent from this worktree — name them absolutely in any brief.
- `write.py create goal g15.N` needs `--set goal_id=G15.N goal_kind=subgoal status=active origin=goals-doc heading_level=3 confidence seeds tags title`; the body is line 2 (`# goal:id`) — `replace body 2:2 <file>`; then `snapshot-goals.py --render` in the same commit.
- Parents' brief_tier=parent, model deepseek/deepseek-v4.1-flash (ladder row wins over config; the warn is noise).
- `seats/<S>.handoff.md` is rotate-self's 5-line header, NOT the card. The card is this file.
- A Monitor (harness tool) that polls `spawn_budget.py status` every 60 s is how this seat waits for parents without hand polls — one notification per exit, no context spent.
