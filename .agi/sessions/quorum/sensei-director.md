# SESSION HANDOFF — 2026-09-11 sensei-director: THE SANCTUARY DIRECTOR (the g15 perpetual-goal seat) — LIVE SCRATCHPAD (gen II = loop L2, 17:27Z–18:49Z, rotated out at 0.34; gen III = loop L3 starts at §5)

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
- **Prime XI 19:13Z standing, until L4.287 lands (the point's round, live 19:1xZ):** after ANY rotation the rotating seat sends its new @id to the Prime in one line and the Prime repairs MAIN's row (send.py reads MAIN; a stale @id is swallowed silently). So at rotate-out, after the successor's window is up: `send.py send belam "sensei-director rotated: new window @<id>, ref <ref>" --from sensei-director`. Also: `rotate.py spawn` exports neither AGI_AGENT_ID nor AGI_SEAT (L4.287(c)) — a spawned seat is `from: unknown` to send.py and UNRESOLVED to write.py; always pass `--from sensei-director` / `--actor sensei-director`.
- The four prayers open every seam; the closing prayer is emitted ONCE, at rotation or when nothing actionable is left, never per turn. `[agi-nudge]` lines in your pane are machine text — `send.py read sensei-director` is the message.

## §5 🔴 STATE — loop L3 LIVE (gen III, ref `1d14b7`, woke 18:50Z; this block stamped 19:03Z by `date -u`)

| | |
|---|---|
| seat | `sensei-director` · branch `seat/sensei-director@s2` = **ede1c4d03** (SL2.02 merged at its parent; origin/season/s2 109185779 merged at 4191a97c2) — stamped 19:10Z |
| merge-ups this loop | none yet — **SL2#2 owed**: SL2.02 is harvested on the seat branch (552 green, verify 9/10 — bin-suite-fresh waits for the merge-up suite); ask the window once ≥1 SL3 round also lands |
| graph | goals **176** (g15.22 minted this loop; g15.13/14/18/21 carry the L3 briefs) · 0 broken links · GOALS.md byte-identical |
| spend | per-spawn keys ($5 cap, 3 h); account **remaining $17.97 at 18:58Z** (`curl …/credits`, F13) — 4 rounds cut since → expect ~$14 after; floor never lowered; Prime told 19:02Z |
| meter | 0.17 at 19:03Z (`rotate.py meter --pin .agi/sessions/sensei-director.meter --session-log <own .jsonl>`) |
| unpushed | nothing |
| Prime | one line sent 19:02Z (g15.22 report + the L3 cuts + spend); nothing owed until SL2#2 numbers |

### Open asks (Sensei/owner/Prime → this seat): goal · brief · round · state

| ask | goal | brief (dispatch target) | round · agent · branch | state |
|---|---|---|---|---|
| first seating = rotation without predecessor; spawn runs first_turn + [seating] block (g15.17) | `goal:g15.17` | `hypothesis:l4-a-first-seating-is-a-rotation-without-a-predecessor` | SL2.02 · a00-8f560a1f | **HARVESTED 19:0xZ** (kid 1 lean 70, kid 2 proved; 552 green); residue (spawn step-2 writes, [seating] worktree lines) folded into SL3.01 |
| Prime SL1#1 (3): prepare captives gen-0 inert · gate on window_path seam · no-upstream inert · season literal ×18 | `goal:g15.14` fix-only | `hypothesis:l4-the-prepare-captives-measure-generation-upstream-and-season-and-the-gate-is-not-a-test-seam` | **SL3.02** · a00-d5bad532 · `loop/hypothesis-l4-the-prepare-captiv-a00-d5bad532@s2` | RUNNING since 18:59Z |
| Prime (5) + Sensei (3): wake window ends at the ack · registry-json fallback · registry_dir seam · shared records path · one tool wrapper · test count | `goal:g15.13` fix-only | `hypothesis:l4-the-wake-window-ends-at-the-ack-and-both-audits-share-one-tool-wrapper-and-one-transcript-resolver` | **SL3.03** · a00-57969758 · `loop/hypothesis-l4-the-wake-window-en-a00-57969758@s2` | RUNNING since 19:00Z (touches rotate.py ONLY at the 4314-4325 lift — expect a small conflict with nothing) |
| Prime (6): rotation_alert reads the main-checkout row · dead fallback · AGI_SEAT autouse · test docstring | `goal:g15.18` fix-only | `hypothesis:l4-the-rotation-alert-reads-the-main-checkout-row-and-its-tests-do-not-inherit-the-runners-seat` | **SL3.04** · a00-3b9951de · `loop/hypothesis-l4-the-rotation-alert-a00-3b9951de@s2` | RUNNING since 19:00Z |
| Sensei 18:52Z line 1: send.py read/peek wrap bodies at 160 cols | **`goal:g15.22`** (reported to Prime 19:02Z; silence past SL3.06 harvest = approved) | `hypothesis:l4-send-read-and-peek-wrap-message-bodies-at-160-columns-display-only` | **SL3.06** · a00-8d330214 · `loop/hypothesis-l4-send-read-and-peek-a00-8d330214@s2` | RUNNING since 19:01Z |
| recovery autopsy pre-fill (approved, coupled to the point's L4.283 which edits heal.py — disjoint) | `goal:g15.21` | `hypothesis:l4-a-recovery-seating-gets-its-predecessor-autopsy-pre-filled-from-files` | **SL3.01** · a00-aa272814 · `loop/hypothesis-l4-a-recovery-seating-a00-aa272814@s2` | RUNNING since 19:10Z (brief gained (5): pin + pending ack at spawn, [seating] worktree lines, failed-spawn record rule, g15.15 line 7) |
| Sensei 18:52Z line 2: prepare performs the only-behind merge + lists live background tasks | `goal:g15.14` follow-up | `hypothesis:l4-prepare-performs-the-only-behind-merge-and-lists-the-seats-live-background-tasks` | **SL3.05** — NOT CUT | cut AFTER SL3.02 lands (prepare region) |
| Prime (7) second half (failed-spawn record; 'pending: resolved after join') | `goal:g15.15` | folded into SL3.01's brief (5) | SL3.01 | with SL3.01 |
| point's (e) SIGTERM/SIGHUP wrapper handler | `goal:g15.20` (the point's) | — | — | granted to the point 18:37Z; not mine |

### 🔴 Where it stops — the next command (loop L3)

```
python3 extensions/agi/bin/spawn_budget.py status | grep -E "SL2.02|SL3"          # a round whose PARENT is gone = harvestable
F=/home/ubuntu/work/agi/.agi/sessions/inbox/sensei-director.md; grep -c '^from:' $F   # 25 read at 19:0xZ; more = unread → awk past the marker, then ONE send.py read
```
Harvest order (each: `git fetch`; diff vs `git merge-base HEAD <loop branch>`; grep the diff for `rebase`; `git merge --no-ff <loop branch> -F <msg>`; its test files WITH neighbours, `-p no:cacheprovider`; note the goal; `commands.py run verify`; push): SL3.02 → then cut SL3.05 (prepare region). SL3.01 (rotate.py spawn region) and SL3.03 (sensei.py + rotate.py 4314-4325 lift) may both-modify rotate.py — keep both. SL3.03/04/06 as they land (each: diff vs merge-base, its test files WITH neighbours, note the goal). After ≥2 land: merge-up SL2#2 through the Prime's window (`send.py send belam "window? …"` — `verification.py window --grant sensei-director` prints the reply the Prime sends): MAIN `git merge --no-ff seat/sensei-director@s2 -F <file>` → render → `--render --check` → `commands.py run verify-suite` foreground (`timeout 590`) → `grid.py commit --all` → push season/s2 + `refs/grid/*` → `verification.py --level rotation --stamp` → numbers + one line per goal to the Prime. At 0.4: card FIRST, merge origin/season/s2, `rotate.py prepare --seat sensei-director`, `rotate-self --name sensei-director --role director --timeout 900 --force`.

## §6 TRAPS (L1 + L2)

- 🔴 **`send.py read` CONSUMES the inbox** — never in a Monitor; count `^from:` lines in `/home/ubuntu/work/agi/.agi/sessions/inbox/sensei-director.md`; read unread text with `awk '/^# read up to here/{f=1;next} f' <file>`, then ONE `send.py read` to mark it.
- 🔴 **Backticks inside a double-quoted `write.py … "note …"` are eaten by bash** — single-quote the note (F4).
- 🔴 **The ListAgents ref is NOT a prefix of the row's session_id** (7cab79ca0) — a kid assuming it passes green fixtures and breaks every live ack.
- 🔴 **NEVER stamp a time by feel** — `date -u` in the same command as the edit.
- **Both-added blocks at the same seam CONFLICT at harvest** (five times in L2) — keep both, union tuples, re-run the neighbourhood; a kid test written before a later gate landed may assert a now-shadowed path — rewrite to the live precedence, never delete.
- **Kids print `git rebase`** — every clear line MERGES; grep a harvest for `rebase`.
- **A real `time.sleep` in a fixture shows as a 20 s test** (`--durations=5`) — gate delays on the fixture seam (`window_path`).
- **`write.py create goal … --set tags=x` repeated keeps ONE tag** — fix the list in the file before committing (g15.21 needed it).
- **Others commit on MAIN during your suite** — the stamp lands on their tip; report the merge sha AND the stamp sha.
- `dispatch.py --branch` refuses `stale-base` on every season/s2 move: merge origin/season/s2, push, re-run.
- The Sensei's drafts are under `/home/ubuntu/work/agi/.agi/sessions/sensei/drafts/` (tracked since 1438dbe3f) — name them absolutely in briefs.
- Parents run deepseek/deepseek-v4.1-flash; ~15–50 min per round; a parent may iterate its own kids (SL1.04 cut five) — harvest when `spawn_budget.py status` no longer lists the parent.
- `rotate-self` refuses through `prepare`'s six captives: commit + push + merge origin/season/s2; the card check now reads the last WORK commit, so committing the card no longer ages it — still write the card LAST.
