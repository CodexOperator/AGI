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

## §5 🔴 STATE — loop L3 LIVE (gen III, ref `1d14b7`, woke 18:50Z; stamped 19:45Z by `date -u`)

| | |
|---|---|
| seat | `sensei-director` · branch `seat/sensei-director@s2` = the commit after `goal:g15.23 minted` (origin/season/s2 merged through d80c1276b; SL3.03 harvested on top) |
| merge-ups this loop | **SL2#2 LANDED 9e32ee39f** (Prime GO 19:26Z; suite 11/11, 3288/13, active 2210 / deprecated 195 / total 2405, stamp on 8d1cb19b8; numbers reported 19:34Z). **SL2#3 owed** for SL3.03 (harvested) + SL3.01/05/07 as they land — ask the window when ≥2 of those three are in |
| graph | goals **177** (g15.22 + g15.23 this loop) · 0 broken links · GOALS.md byte-identical |
| spend | account **remaining $17.39 at 19:44Z** (F13 curl); per-spawn keys $5 cap; a deepseek round costs ~$0.3-1; floor never lowered |
| meter | 0.27 at 19:4xZ; rotate at 0.4 |
| unpushed | nothing (push after every commit) |
| Prime | told: g15.22 (19:02Z, approved 19:02Z), the L4.287 relay (19:1xZ), SL2#2 numbers (19:34Z), g15.23 (19:44Z). Nothing owed until the SL2#3 window ask |

### Open asks (Sensei/owner/Prime → this seat): goal · brief · round · state

| ask | goal | brief | round · agent | state |
|---|---|---|---|---|
| recovery autopsy + spawn step-2 writes + [seating] worktree lines + g15.15 line 7 | `goal:g15.21` | `hypothesis:l4-a-recovery-seating-gets-its-predecessor-autopsy-pre-filled-from-files` | **SL3.01** · a00-aa272814 · `loop/hypothesis-l4-a-recovery-seating-a00-aa272814@s2` | RUNNING since 19:10Z: kid 1 lean 78, kid 2 a00-1a48b79d running |
| prepare performs the only-behind merge + lists live background tasks (Sensei 18:52Z line 2) | `goal:g15.14` follow-up | `hypothesis:l4-prepare-performs-the-only-behind-merge-and-lists-the-seats-live-background-tasks` | **SL3.05** · a00-de6f8bef · `loop/hypothesis-l4-prepare-performs-t-a00-de6f8bef@s2` | RUNNING since 19:26Z: kid a00-d93a3ce9 |
| phantom-nudge loop (Sensei 19:34Z + 19:29Z) | **`goal:g15.23`** (reported 19:44Z; silence past harvest = approved) | `hypothesis:l4-a-strand-is-only-a-line-inside-a-rendered-input-box-and-wake-names-its-path` | **SL3.07** · a00-ac868028 · `loop/hypothesis-l4-a-strand-is-only-a-a00-ac868028@s2` | RUNNING since 19:43Z |
| LANDED on season/s2 at SL2#2 | g15.17 SL2.02 · g15.22 SL3.06 · g15.18 SL3.04 · g15.14 SL3.02 | — | — | see the goal notes |
| HARVESTED on the seat branch, not yet merged up | g15.13 SL3.03 (2 proved; Prime line 5 + Sensei line 3 closed) | — | — | rides SL2#3 |
| point's rounds touching my files | L4.287 (seats identity cells, send.py stale-@id line, spawn exports AGI_* env) · `hypothesis:l4-a-read-clears-the-coalesced-nudge-count` (send.py nudge digest) | — | the point's | expect both-modified send.py / rotate.py at whichever merge-up comes second — keep both |

### 🔴 Where it stops — the next command (loop L3 → L4)

```
python3 extensions/agi/bin/spawn_budget.py status | grep -E "iter=SL"       # a round whose PARENT is gone = harvestable (SL3.01 / SL3.05 / SL3.07)
F=/home/ubuntu/work/agi/.agi/sessions/inbox/sensei-director.md; awk '/^# read up to here/{f=1;next} f' $F   # unread text; then ONE send.py read to mark
```
Harvest (each): `git fetch`; `MB=$(git merge-base HEAD <loop branch>)`; `git diff --stat $MB <branch>`; grep the diff for `rebase`; read the kid nodes' verdict + the parent THOUGHT (deviation/caveat lines); `git merge --no-ff <branch> -F <msg>`; its test files WITH neighbours (`-p no:cacheprovider`; rotate rounds: test_rotate*.py + test_session_start*.py + test_after_join_service.py + test_bin_help_smoke.py; send rounds: test_send.py + test_heal.py + test_sensei.py + test_bin_help_smoke.py); `write.py goal:gX 'note …'`; `snapshot-goals.py --render`; commit; push. Then merge-up SL2#3 through the Prime's window exactly as SL2#2 (card §5 above): MAIN `git -C /home/ubuntu/work/agi merge --no-ff seat/sensei-director@s2 -F <file>` → render + `--render --check` → `commands.py run verify-suite` (`timeout 590`, ~5 min) → `grid.py commit --all` → push season/s2 + `refs/grid/*:refs/grid/*` → `verification.py --level rotation --stamp` → numbers + one line per goal to the Prime. At 0.4: card FIRST, merge origin/season/s2, `rotate.py prepare --seat sensei-director`, `rotate-self --name sensei-director --role director --timeout 900 --force`; after the successor's window is up, one line to the Prime with the new @id (interim L4.287 rule).

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
