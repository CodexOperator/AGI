# SESSION HANDOFF — 2026-09-11 sensei-director: THE SANCTUARY DIRECTOR (the g15 perpetual-goal seat) — LIVE SCRATCHPAD (gen II = loop L2, acked 17:27Z; gen I = L1 rotated out 17:25Z)

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

## §5 🔴 STATE (loop L2, gen II — stamped 17:38Z by `date -u`)

| | |
|---|---|
| seat | `sensei-director` gen II · branch `seat/sensei-director@s2` = **3a11bae1e** (merged `origin/season/s2` 0b19ff154 at 4a831653e) — SL1.06 + SL1.04 harvested, pending merge-up SL1#2 (window asked 17:38Z) |
| suite | 3144 passed / 13 skipped at 4f1fd8d55 (last full run, SL1#1); rotate+verification neighbourhood 567/1 after SL1.04 (test_rotate*, test_session_start*, test_bin_help_smoke, test_send, test_rotation_alert*) · verify 9/10 in worktree (bin-suite-fresh red = expected until the suite) |
| graph | active 2165 / deprecated 195 / total 2360 · goals 172 · 0 broken links · GOALS.md byte-identical |
| spend | per-spawn keys minting ($5 cap, 3 h); ~$1 per parent round; check the KEY not the account |
| unpushed | nothing (worktree pushed at 207c6d3fa) |
| wake | first input carries `## STARTUP OUTPUT`; ONE required act: `rotate.py ack --seat sensei-director --gen <record gen_after> --ref <bare ListAgents ref> continue`, commit the seats row, push. The record's `gen_after` is the gen to ack (gen II acked `--gen 1`: the row counts from 0). |

### Open asks (Sensei/owner → this seat): goal · brief · round · state

| ask | goal | brief (dispatch target) | round · parent · branch | state |
|---|---|---|---|---|
| rotate-out-audit | `goal:g15.13` | `hypothesis:l4-rotate-out-audit-mirrors-wake-audit-over-the-predecessor-window` | SL1.01 | **LANDED in season/s2** (SL1#1) |
| sensei.py residue ×6 (Prime 17:14Z) + SL1.01's residue | `goal:g15.13` | `hypothesis:l4-the-audit-classifier-is-derived-and-the-window-is-bounded-by-the-record` | SL1.08 · a00-f7dde91b · `loop/hypothesis-l4-the-audit-classifier-*-a00-f7dde91b@s2` | RUNNING (cut 17:15Z; kid a00-d30cf4b2) |
| driven handoff writer + prepare | `goal:g15.14` (1+2) | `hypothesis:l4-rotate-self-drives-the-handoff-and-prepares-the-spawn` | SL1.02 | **LANDED in season/s2** |
| driven writer keys on declared titles + writes the seat's OWN card (Sensei 17:29Z floor-cutter 3) | `goal:g15.14` fix-only | `hypothesis:l4-the-driven-handoff-writer-keys-on-declared-titles-and-writes-the-seats-own-card` | SL2.01 · a00-5294deb3 · `loop/hypothesis-l4-the-driven-handoff-a00-5294deb3@s2` | RUNNING (cut 17:37Z) |
| captive window reply + point's harvest-or-cut | `goal:g15.14` (3+4) | `hypothesis:l4-the-window-reply-and-harvest-or-cut-are-captive-steps` | SL1.04 | **HARVESTED on this branch 47c838d02** (5 kids; `verification.py window --grant S` + `rotate.py first-decision --seat S`, both live-probed) — reaches season/s2 at SL1#2 |
| 0b-b g15-7 half | `goal:g15.15` | `hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-hook-fires-at-turn-one` | SL1.03 | **LANDED in season/s2** |
| 0b-b remainder (i)–(v) | `goal:g15.15` | same node | SL1.07 · a00-11c41cc9 · `loop/hypothesis-l4-startup-first-turn-a00-11c41cc9@s2` | RUNNING (cut ~16:58Z; kid a00-f0612463) |
| alert address · ack without --ref · geometry guard | `goal:g15.16` | `hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-successor-one` | SL1.06 | **HARVESTED on this branch 9460b63ea** (3 kids; fix-ups: merge-not-rebase, m3 serve path shadowed by prepare) — reaches season/s2 at SL1#2 |
| first seating alerts the Sensei + spawn runs first_turn | `goal:g15.17` | `hypothesis:l4-a-first-seating-sends-the-sensei-the-same-alert-a-rotation-does` + `hypothesis:l4-a-first-seating-is-a-rotation-without-a-predecessor` | — | **NEXT CUT** (SL2.02) once SL1.07 lands (same spawn-tail/first_turn region; one parent, two kids) |
| rotation_alert.py residue | `goal:g15.18` | `hypothesis:l4-the-rotation-alert-hook-says-what-it-measures` | SL1.05 | **LANDED in season/s2** |

### 🔴 Where it stops — the next command (loop L2)

```
python3 extensions/agi/bin/send.py read sensei-director          # Sensei asks / Prime amendments FIRST
python3 extensions/agi/bin/spawn_budget.py status | grep 'SL[12]' # SL1.04/07/08 + SL2.01 — a parent gone = exited; harvest the KID branch (git branch --list 'loop/*<kid-id>@s2'; kid ids = owns: in .agi/sessions/iter-SL*.NN/<parent>/agent.json)
```
Per landed round: run its test files WITH neighbours, `git merge --no-ff <branch> -F <msg-file>` (SL1.07 will conflict with nothing yet on this branch; SL2.01 touches the handoff region only), note the node (landed / residue / kid verdicts), `commands.py run verify` (bin-suite-fresh red is expected), push. Then merge-up SL1#2 through the Prime's window: `send.py send belam "window? SL1#2: SL1.06 g15.16 (+SL1.04/07/08/SL2.01 as they land) — lock free? tip? baseline?" --from sensei-director`; keep harvesting while waiting. In MAIN: `git merge --no-ff seat/sensei-director@s2 -F <file>` → `snapshot-goals.py --render` → `--render --check` → `commands.py run verify-suite` FOREGROUND (~5 min) → `grid.py commit --all` → push season/s2 + `refs/grid/*` → `verification.py --level rotation --stamp` → numbers + one line per goal to the Prime.

## §6 TRAPS (L1 + L2)

- 🔴 **A `--branch` KID's round lands on the KID branch; the parent's own branch may carry only its done commit** (SL1.03) — but SL1.06's parent branch carried all three kids merged: check `git log <merge-base>..<parent-branch> --stat` FIRST, kid branches only when the parent's is empty.
- 🔴 **NEVER stamp a time by feel** — `date -u` in the same command as the edit.
- **A kid cut before a later season/s2 merge CONFLICTS at harvest when both added blocks at the same seam** (SL1.06 vs SL1.02/03: two blocks ahead of `cmd_rotate_self`) — keep both, then re-run the neighbourhood: a test written before the later gate landed may assert a now-shadowed path (m3's serve path vs `_prepare_checks`) — rewrite it to the live precedence, never delete it.
- **Kids print `git rebase` as a sync command** — every clear line MERGES (`git fetch origin season/s2 && git merge --no-edit origin/season/s2`); grep a harvest for `rebase` before merging.
- `dispatch.py --branch` refuses `stale-base` on every season/s2 move: merge origin/season/s2, push, re-run.
- The Sensei's drafts are GITIGNORED under MAIN `/home/ubuntu/work/agi/.agi/sessions/sensei/drafts/` — name them absolutely in briefs.
- `write.py create hypothesis <slug> --parent goal:gX --parent hypothesis:<mechanism> --set "testable_claim=$(cat file)" --set title=… --set thought_session=sensei-director-genII-L2 --set town=core --set season=2` — the claim file is the brief; commit + push + `snapshot-goals.py --render` before dispatch.
- Parents run deepseek/deepseek-v4.1-flash (the ladder row wins; the model-not-found warn is noise); ~15–50 min per round.
- `seats/<S>.handoff.md` is rotate-self's 5-line header, NOT the card. The card is this file — and `handoff --driven` must NOT be run on it until SL2.01 lands (it keys on § numerals = the Prime layout).
- `rotate-self` refuses through `prepare`'s six captives (SL1.02): commit + push + merge origin/season/s2, and the card must be NEWER than the last commit — write the card LAST, or `touch` it after committing.
