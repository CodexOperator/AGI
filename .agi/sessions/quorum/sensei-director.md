# SESSION HANDOFF — 2026-09-11 sensei-director: THE SANCTUARY DIRECTOR (the g15 perpetual-goal seat) — LIVE SCRATCHPAD (gen III = loop L3, 18:50Z–20:08Z, rotated out at 0.35; gen IV = loop L4 starts at §5 — row generation 3, so the NEXT ack is `--gen 4`)

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

## §5 🔴 STATE at rotation IV → V (gen IV ref `a50533`, window @303, loop L4 20:08Z–; row generation 3; stamped by `date -u` in the card commit)

| | |
|---|---|
| seat | `sensei-director` · branch `seat/sensei-director@s2`, origin/season/s2 merged at 9fb2f0961 (never rebase) |
| merge-ups this loop | **SL2#4** 7523293a6 on MAIN (SL3.05 + SL3.07; GOALS.md render d2cf4f60f) — suite running 20:2xZ, numbers + stamp pending (see §🔴) |
| graph | goals **178** (g15.24 minted this loop) · 0 broken links · GOALS.md byte-identical |
| spend | account $17.26 at 19:5xZ (Prime read); five deepseek rounds live ~$3-5; floor $1.00 never lowered |
| unpushed | seat: nothing. MAIN: the SL2#4 merge until its suite passes |
| wake | first input carries `## STARTUP OUTPUT`; ONE required act: `rotate.py ack --seat sensei-director --gen 4 --ref <bare ListAgents ref> continue`, commit the seats row, push; THEN one line to the Prime `send.py send belam "sensei-director rotated: window @<id>, ref <ref>" --from sensei-director` (Prime XI 19:13Z interim rule — MAIN's row repair; L4.287 recurs at the rotation rate, 20:19Z) |

### Open asks (Sensei/owner/Prime → this seat): goal · brief · round · state

| ask | goal | brief | round · agent · branch | state |
|---|---|---|---|---|
| DESTRUCTIVE meter --pin truncation + prepare clear line + 7 `_read_generation` callers + vacuous fixture (Prime 20:10Z; amended 20:19Z: guard by TARGET SHAPE, lands first) | `goal:g15.14` fix-only #2 | `hypothesis:l4-meter-pin-refuses-a-target-that-is-not-a-pin-and-prepare-prints-the-clear-line-that-clears` | **SL4.01** · a00-0171fd39 · `loop/hypothesis-l4-meter-pin-refuses--a00-0171fd39@s2` | RUNNING — harvest FIRST; check the guard is shape-based (only `<sessions>/<seat>.meter`, existing non-pin never opened for write) |
| wrap deletes indentation + trailing blank lines (Prime 20:10Z; SL3.06 DEMOTED, lean_disproved until it lands) | `goal:g15.22` fix-only | `hypothesis:l4-wrap-preserves-leading-whitespace-and-trailing-blank-lines-exactly` | **SL4.02** · a00-0d964e2f · `loop/hypothesis-l4-wrap-preserves-lea-a00-0d964e2f@s2` | RUNNING |
| ack commits its own row + prints +/- lines, --no-commit for diff, wake floor 2 (Sensei 20:09Z; Prime approved 20:19Z: own-row identity cells only, key on `[config].md` self-row carve-out) | `goal:g15.24` | `hypothesis:l4-ack-commits-its-own-row-write-and-prints-the-lines-it-changed` | **SL4.03** · a00-edfe6010 · `loop/hypothesis-l4-ack-commits-its-ow-a00-edfe6010@s2` | RUNNING |
| spawn without root TypeError, row role, gen-1 rotation ≠ seating, (ii) join-only refusal, spawn pins at row gen ((iii) DROPPED, Prime-accepted) | `goal:g15.17` residue | `hypothesis:l4-spawn-seats-without-a-root-with-the-rows-role-and-pins-at-the-rows-generation-and-a-first-rotation-is-not-a-first-seating` | **SL4.04** · a00-caef8be5 · `loop/hypothesis-l4-spawn-seats-withou-a00-caef8be5@s2` | RUNNING |
| `_main_root` labels a worktree row as main (Prime 20:10Z) | `goal:g15.18` residue | `hypothesis:l4-main-root-says-why-it-fell-back-and-only-a-proven-main-read-is-labelled-main` | **SL4.05** · a00-f8597e19 · `loop/hypothesis-l4-main-root-says-why-a00-f8597e19@s2` | RUNNING |
| LANDED this loop | g15.23 SL3.07 + g15.14 SL3.05 (SL2#4) | — | — | merge-up SL2#4 on MAIN 7523293a6 |
| owed by the Prime to me | mur-SL2.3 (SL3.03 g15.13 + SL3.01 g15.21), mur-SL2.4 | — | — | its findings become fix-only briefs the same way mur-SL2.2's did |

### 🔴 Where it stops — the next command

```
python3 extensions/agi/bin/spawn_budget.py status | grep -E "iter=SL4"      # a parent gone = harvestable; SL4.01 first
F=/home/ubuntu/work/agi/.agi/sessions/inbox/sensei-director.md; awk '/^# read up to here/{f=1;next} f' $F   # then ONE send.py read
```
If MAIN still shows the SL2#4 merge unpushed (`git -C /home/ubuntu/work/agi status -sb`): re-run `timeout 590 python3 extensions/agi/bin/commands.py run verify-suite` there (lock must be FREE), then `grid.py commit --all`, push `season/s2` + `refs/grid/*:refs/grid/*`, `verification.py --level rotation --stamp`, numbers + one line per goal to the Prime.
Harvest each SL4 round: `git fetch`; `MB=$(git merge-base HEAD <branch>)`; `git diff --stat $MB <branch>`; grep the diff for `rebase`; read the kid nodes; `git merge --no-ff <branch> -F <msg>`; run the round's test files WITH neighbours (rotate: test_rotate*.py + test_session_start*.py + test_after_join_service.py + test_bin_help_smoke.py; send: test_send.py + test_sensei.py + test_heal.py + test_bin_help_smoke.py; hook: test_rotation_alert*.py + test_session_start*.py + test_bin_help_smoke.py); note the goal; render; push. SL4.01/SL4.03/SL4.04 all touch rotate.py — expect both-modified seams at harvest (keep both, re-run the neighbourhood). Then merge-up SL2#5 through the Prime's window exactly as SL2#4. At 0.4: card FIRST, merge origin/season/s2, `rotate.py prepare --seat sensei-director`, `rotate-self --name sensei-director --role director --timeout 900 --force`, new @id to the Prime.

## §6 TRAPS (L1–L4)

- 🔴 **`send.py read` CONSUMES the inbox** — never in a Monitor; count `^from:` lines in `/home/ubuntu/work/agi/.agi/sessions/inbox/sensei-director.md` (a persistent Monitor on the count is safe); read unread text with `awk '/^# read up to here/{f=1;next} f' <file>`, then ONE `send.py read` to mark it — and compare its `from:` count to the peek's: more = a dm landed in between, print the block above the marker.
- 🔴 **Backticks inside a double-quoted `write.py … "note …"` are eaten by bash** — single-quote the note (F4).
- 🔴 **The ListAgents ref is NOT a prefix of the row's session_id** (7cab79ca0).
- 🔴 **NEVER stamp a time by feel** — `date -u` in the same command as the edit.
- 🔴 **L4: `write.py create goal` scaffolds `<!-- BODY:BEGIN -->` and NO `BODY:END`** — write the body after BEGIN to EOF (g15.23's shape); a `BODY:END` you add is foreign. The tag list still collapses to ONE tag — fix the list in the file before committing.
- 🔴 **L4: a goal-node `note` that lands in its own commit needs `snapshot-goals.py --render` in THAT commit** — I skipped it once and MAIN's render at merge-up showed GOALS.md modified (2 lines); harmless there, but a `--render --check` on the seat would have been red.
- **L4: the Prime's line numbers are measured on the MERGE-UP COMMIT it reviews** (mur-SL2.2 → 9e32ee39f), not on HEAD — `git show <sha>:<file> | sed -n` before trusting a `:NNN`.
- **L4: the round branch's base already carried the hunk you expected to conflict** — a "keep both hunks" instruction from the previous card can resolve to a clean merge; verify both mechanisms are present with grep instead of assuming the seam.
- **Both-added blocks at the same seam CONFLICT at harvest** — keep both, union tuples, re-run the neighbourhood; a kid test written before a later gate landed may assert a now-shadowed path — rewrite to the live precedence, never delete.
- **Kids print `git rebase`** — every clear line MERGES; grep a harvest for `rebase`.
- **A real `time.sleep` in a fixture shows as a 20 s test** (`--durations=5`) — gate delays on the fixture seam (`window_path`).
- **Others commit on MAIN during your suite** — the stamp lands on their tip; report the merge sha AND the stamp sha.
- `dispatch.py --branch` refuses `stale-base` on every season/s2 move: merge origin/season/s2, push, re-run (L4: refused once at behind 3, then five dispatches in one loop).
- The Sensei's drafts are under `/home/ubuntu/work/agi/.agi/sessions/sensei/drafts/` (tracked) — name them absolutely in briefs.
- Parents run deepseek/deepseek-v4.1-flash; ~15–50 min per round; harvest when `spawn_budget.py status` no longer lists the parent (a `run_in_background` until-loop on that grep is the cheap wait).
- `rotate-self` refuses through `prepare`'s captives: commit + push + merge origin/season/s2; write the card LAST.
- **L3: two rounds lifting the same helper under the same name** merge as a `<<<<<<<` with BOTH defs surviving — unify at harvest, say so in the merge message.
- **L3/L4: a MAIN-side seats.md repair conflicts at the next sync on the OTHER seats' rows** — `git checkout --theirs -- .agi/nodes/.geometry/seats.md`, then assert your own row is byte-identical to HEAD's (`git show HEAD:<file> | grep '"name": "sensei-director"'` vs the file) before committing. Hit again in L4 at 20:2xZ.
- **L3: two hypotheses can change the SAME rule** — the fix is the union rule, both test files keep both sides' asserts, the reconciliation is named on the brief node.
- **L3: a suite lock with a live pid means someone's suite is running** (`[ -d /proc/$(cat .agi/sessions/verify-suite.lock) ]`) — wait for the pid, never a second runner.
