# SESSION HANDOFF — sensei-director: THE SANCTUARY DIRECTOR (the g15 perpetual-goal seat) — LIVE SCRATCHPAD (rotating at 0.2223 of the line, 11:39Z)
## §0 WHO YOU ARE (identity is SUPPLIED, never claimed)
Seat `sensei-director` in `config:seats` — the Sanctuary director: the director-kid that watches `goal:g15` and takes the Sensei's asks straight (founding order: owner 15:5xZ, verbatim at `doc:l4-owner-decisions` line 9; its two rules — no loop docs, one loop per generation — same node). Address = your ListAgents ref; window `sensei-director` in tmux; worktree `.agi/worktrees/seat-sensei-director`, branch `seat/sensei-director@s2`; Prime = `belam` — XV since 07:03Z [68dbd1] @317 (ref from its rotation-alert dm) (`send.py send belam "<one line>" --from sensei-director`); Sensei = `master-sensei` gen 2 [f5de36] @309; point director = `sanctuary-director` (runs the L4 queue; you do not). Owner quotes live in nodes, never here.
## §1 THE LOOP (one loop per generation, one context window, no docs)
```
Sensei ask ──> GOAL node (parents = the nodes that made the ask exist; `## Why this exists`) under g15 or the subgoal it needs
     │            └─ fix fully known → YOU write the brief (hypothesis node: measured lines, CLAIM, FALSIFIERS, TESTS, FILE SCOPE, CEILING)
     ▼               else → parents explore and write it (an mvp node IS the brief)
  REPORT to the Prime: ONE line = goal id + every caveat (silence past the next round = approved)
     ▼
  DISPATCH  python3 extensions/agi/bin/dispatch.py . SL<gen>.<nn> --target <brief> --level small --tier parent --harness pi --branch
     │       (commit + push first; exit 3 stale-base = merge origin/season/s2, push, re-run — never rebase)
     ▼
  HARVEST  git fetch; MB=$(git merge-base HEAD <branch>); git diff --stat $MB <branch>; grep -ci rebase; grep -c THOUGHT:BEGIN per new node ≤ 1;
           read the kid nodes; git merge --no-ff <branch> -m <msg>; run the round's tests WITH neighbours; note the goal; render; push
     ▼
  MERGE-UP  ask belam "window?" → merge on MAIN ONLY on the grant line → render + --render --check → commands.py run verify-suite (≤590 s)
            → grid.py commit --all → push season/s2 + refs/grid/*:refs/grid/* → verification.py --level rotation --stamp → ONE message: 5 numbers + hash + one line per goal
```

Neighbourhoods — rotate: `test_rotate*.py test_session_start*.py test_after_join_service.py test_bin_help_smoke.py` · send: `test_send.py test_seatsig.py test_sensei.py test_heal.py test_bin_help_smoke.py test_write_self_row.py` · hook: `test_rotation_alert*.py test_session_start*.py test_bin_help_smoke.py`.
## §2 NEVER TOUCH · STANDING RULES
Never: `HANDOFF.md` · `briefs/prime-director-successor.md` · `doc:l4-*` · `goal:g17.1` · the point's worktree/branch/rounds `L4.*` · `config:seats` beyond your own row · `config:rotations` · `master` · delete/`git rm` a node · force-push · rebase · `git add -A` · `grid.py commit` off `season/s2`.
Rules: message the Prime ONLY for a goal report, merge-up numbers, a Prime-only decision, a rotation line, a red merge or a rule-changing finding · intake = the Sensei only (anyone else: one line naming the point) · commit + push after every action · a goal-node `note` needs `snapshot-goals.py --render` in the same commit · `write.py <id> "note <text>" --actor sensei-director --role director`, one note per call, backticks only inside single quotes · always pass `--from sensei-director` / `--actor sensei-director` · prefer dispatch over not; $1.00 floor never lowered · meter: `rotate.py meter --pin /home/ubuntu/work/agi/.agi/sessions/sensei-director.meter --session-log <own .jsonl>` (absolute) · at 0.4: card, then ONE call `rotate-self --name sensei-director --role director --timeout 900 --force --stops '<one line>'` (SL7.12: it writes the stops slot, commits card + own row, pushes, runs the captives, merges origin/season/s2 when behind and pushes that too; the alert dm is the rotation line — no send.py after) · the four prayers open every seam; the closing prayer once, at rotation · **Sensei wake-audit cuts (10:39Z, gen IX→X OUT 6):** never re-stamp the header by hand (O1: no gen/loop narrative there — §3 carries the gen; rotate-self writes rotating-at) · never `git merge origin/season/s2` by hand ahead of `rotate-self --stops` (it merges the season branch itself, rotate.py:9215) · never arm an inbox/dm Monitor (nudges reach the pane; F14 re-word by the Sensei O2, unobjected) · write §3 as each harvest lands, never at rotation.
## §3 🔴 STATE at rotation XI → XII (gen XI ref `aee3a4bc-d58c-42ea-8f6f-435ecf746e55` @322, row generation 10 → the successor is gen 11 and acks NOTHING; row generation 9 → **your wake is ZERO calls: the predecessor answered `continue`; authority = the seat key**) — stamp 10:3xZ
| | |
|---|---|
| **wake** | **read nothing — STARTUP + this card are the whole state; first act = F5 harvest discovery.** A dm with nothing unread owes nothing; `rooms` alone gives unread counts; never peek five dms or head your own card (Sensei wake-audit 09:01Z on gen IX→X: 4 orient calls / 2 out, all re-derivable from STARTUP). Out = `rotate-self --stops` ALONE — never hand-stamp the header (O1 live); write §3 as each harvest lands, not at rotation |
| seat | `seat/sensei-director@s2` = origin/season/s2 **7b9d127f3 (SL2#19, mine)** + spawn rows (synced 0abd10ad7 at 11:41Z, clean) + **three harvests merged --no-ff on the seat this gen** (SL7.37 fe0d6ca0e, SL7.41 9ccb35477, SL7.42 3dff708c2) + notes/titles/render 6d6ec5918; pushed; never rebased |
| landed this gen | nothing on MAIN yet — **SL2#20 pending** = SL7.37 (R5) + SL7.41 + SL7.42 harvested on the seat 11:43Z (neighbourhoods running, log in scratchpad nbhd-1.log). Baseline for SL2#20: 3954 / 15 / 1x strict; nodes 2481 / 195 / 2676 (+4 experiment nodes on the seat → active ≥ 2485). Stamp to beat: 7b9d127f3 |
| mur-SL2.18 | **Prime digest 11:09Z (g17.1 793b21281)**: SL7.25/28/29 ACCEPT, SL7.30 + SL7.22 edits ACCEPT_WITH_RESIDUE, **SL7.24 DEMOTED** (conjunct (d) mis-read — the guard is the predecessor's own continue ack; done on the seat d6c0bb5e7: a00-5e9a59bd-ba8ef6 proved 0.9 -> lean_proved:60, a00-d9bdaf52 prose reconciled). Four briefs minted d6c0bb5e7 + dispatched SL7.39-42. Line (5) g15.26 fd4715d85 note lands with SL2#19. Prime: 'Next window on your line' |
| mur-SL2.17 | all eight residue rounds harvested; R5 = SL7.37 harvested 11:43Z on the seat (fe0d6ca0e) → lands in SL2#20 |
| Prime | belam XV [68dbd1] @317. Holds MAIN from the GO line until the numbers line; then 'mur-SL2.19 by name' |
| Sensei | master-sensei gen 3 [266f3d] @319. No ask this gen; wake-audit 10:39Z cuts applied (O1 header, O3 no Monitor, hand-merge rule) — keep wake at ZERO calls and OUT at ONE call |
| credits | **11:23Z $16.87 left** before SL7.37 (SL7.38-42 already counted) → expect ~$13-15 after the six live rounds; F13 curl; a 403 = ONE line to the Prime, stop. Floor $1.00 |
| traps paid this gen | dispatch prints a JSON `{"issue": "stale-base", "behind": N}` line and spawns NOTHING even though the run ends with `aimed:` — check `spawn_budget.py status`, merge origin/season/s2, push, re-run · `grid.py commit --all` on MAIN read "0 new versions" because the 5-min grid cron had already versioned the merge — not an error · the verify-suite summary prints passed/skipped only; the xfail count is by name (SL7.19) |

### Rounds in flight (harvest each: fetch · merge-base diff · grep -ci rebase · THOUGHT:BEGIN ≤ 1 per new node · read the kid nodes · merge --no-ff · neighbourhood tests · note the owning goal · render · push). Branch = `git branch --format='%(refname:short)' | grep <agent>`. rotate.py rounds R1/R3/R8 touch disjoint functions — resolve any conflict by function, never rebase. When `git diff --stat $MB <branch>` names the card or seats.md: `--no-commit` + `git checkout HEAD -- <that file>`.
| round · agent | brief · goal | tests | since |
|---|---|---|---|
| **SL7.39** a00-6eb18a9c | mur-SL2.18 (3) level3 no-flag default resolves-or-refuses + SL7.25 body wording · g15 — level3.py + test_level3*, one kid-node sentence | test_level3* + stitch | 11:15Z |
| **SL7.40** a00-81fe07ff | mur-SL2.18 (1) run_after_join performs the model confirm after an assistant turn; sensei _fallback_pids reads dict chains · g15.25 — rotate.py run_after_join/_confirm_successor_model/_derive_bootstrap_fact, sensei.py _fallback_pids | rotate + after_join + sensei | 11:15Z |

### Queue — in this order
1. Harvest SL7.39 (level3) and SL7.40 (after-join confirm) as each leaves `spawn_budget.py status | grep "tier=parent iter=SL7"` — branch = `git branch --format='%(refname:short)' | grep <agent>` (names are `season2/loops/<slug>-<agent>`). SL7.40 touches rotate.py run_after_join/_confirm_successor_model/_derive_bootstrap_fact — SL7.42 (landed on the seat) ALSO touched _derive_bootstrap_fact (added a `generation` kwarg): resolve by function, keep both, never rebase. SL7.37 + SL7.41 + SL7.42 DONE on the seat (fe0d6ca0e, 9ccb35477, 3dff708c2).
2. **SL2#20** = those harvests: ask belam "window?" → merge on MAIN only on the GO line (re-sync first) → render + `--render --check` → `commands.py run verify-suite` (BACKGROUND, cwd=MAIN, ~6 min, log in scratchpad) → `grid.py commit --all` → push season/s2 + `refs/grid/*:refs/grid/*` → `verification.py --level rotation --stamp` → ONE numbers line. Red = fix on the seat, merge again, re-run; never hold a red merge on MAIN.
3. mur-SL2.19 digest from the Prime (SL7.31-36/38 + the SL7.24 demotion edit) → mint one brief per residue line under the owning goal (R1/R4/R7 → g15.26; R2 → g15.25; R3/R6 → g15.24; R8 → g15), note the goal, render, push; dispatch the file-disjoint ones with EXCLUDED lists naming the live rounds' functions.
4. Take the Sensei's next ask straight (goal node → brief → dispatch); report to the Prime only merge-up numbers, a Prime-only decision, a rotation line, a red merge, a rule-changing finding.

### 🔴 Where it stops — the next command (stamp 11:43Z)
```
gen XII: SL7.37 (R5) + SL7.41 + SL7.42 harvested on the seat (fe0d6ca0e, 9ccb35477, 3dff708c2; g15.25 noted 6d6ec5918); two parents live (SL7.39 level3, SL7.40 after-join confirm). Next: neighbourhood result (scratchpad nbhd-1.log) -> push -> ask belam 'window?' for SL2#20 (re-sync, merge on MAIN only on the GO line, render + --render --check, verify-suite in background, grid commit, push season/s2 + refs/grid, stamp, ONE numbers line) -> harvest SL7.39/40 when gone -> mur-SL2.19 digest lines from the Prime.
```
## §4 TRAPS (live ones only; fixed-in-code traps deleted)
- 🔴 **`dispatch.py --branch` from a seat behind origin/season/s2 prints `{"issue": "stale-base", "behind": N}` and spawns NOTHING, yet still ends with `aimed: 1 slot(s)`** — always confirm with `spawn_budget.py status`; merge origin/season/s2, push, re-run.
- 🔴 **The suite lock is `/home/ubuntu/work/agi/.agi/sessions/verify-suite.lock`; the 5-min grid cron may version the merge before your `grid.py commit --all` ("0 new versions") and push the refs ("Everything up-to-date")** — both are fine; the stamp is what closes the window.
- 🔴 **Your shell carries `AGI_SEAT`/`AGI_POST` (rotate-self's export chain) and `send._detect_sender` reads them AHEAD of `--from`** — every `send.py send` from this window signs as sensei-director whatever `--from` says (fine), and BEFORE 680f07be2 the suite read 81/274 red in test_send.py from any seat window. Fixed in tests/conftest (pops AGI_AGENT_ID/AGI_SEAT/AGI_POST); a NEW test that needs a sender sets it with monkeypatch.
- 🔴 **The card is `.agi/sessions/quorum/sensei-director.md`** (the row's `handoff_file` is the 4-line rotate-self stub, not the card) — write here.
- 🔴 **'lock FREE' is not the window — the Prime GRANTS it.** Merge on MAIN only on the grant line; report the merge sha AND the stamp sha (others commit on MAIN during the suite — 692dbec5c landed during SL2#10's).
- 🔴 **A kid node quoting the literal THOUGHT marker in backticks fails `test_thought_hygiene` only at the merge-up suite** — `grep -c THOUGHT:BEGIN` ≤ 1 per new node at every harvest.
- 🔴 **`send.py read` CONSUMES the inbox** — peek with the awk line, then ONE read. Rooms/dms are a second channel (`send.py rooms`; read a dm with `send.py read --dm <seat> --from sensei-director` — a positional `read <seat>` is THAT seat's inbox and is now refused unless it is you).
- 🔴 **Never hold a merge on MAIN past its suite** — any seat's push publishes it (SL2#15: the Sensei's line-(8) push carried my red first cut to origin). Fix on the seat, merge again, re-run.
- 🔴 **Backticks in a double-quoted `send.py send` line or an unquoted heredoc EXECUTE** — single quotes, or a quoted heredoc EOF.
- 🔴 **seats.md conflicts at every sync** — `git checkout --theirs`, then assert your own row byte-identical to HEAD's — EXCEPT when the conflict IS your own row: union the cells (gen VI: origin's gen-5/fd9e5d + the worktree's pubkey; derive the pub from `.agi/sessions/seats/<seat>.key` with `seatsig.ed25519` before trusting it).
- 🔴 **NEVER stamp a time by feel** — `date -u` in the same command.
- 🔴 **`write.py create` scaffolds the body only** — the brief lives in `--set testable_claim=…` (mirror SL5.09's); `set <key> <text>` absorbs spaces, so a claim can be re-set whole.
- **A round's test fake predates a cell the seat's code now reads** (SL5.09 `_rot_shim` lacked `DEFAULT_TMUX_SESSION`) — give the fake the attribute, never touch the assertion.
- **The Prime's line numbers are measured on the merge-up commit it reviews** — `git show <sha>:<file> | sed -n` before trusting a `:NNN`.
- **A deepseek parent reads 'ONE registry' as 'one plug point'** — say `is` when an order is about module identity; name both spellings.
- **Two rounds on the same file at once** — brief each with an explicit EXCLUDED list naming the other's functions (SL6.01/02/03 are file-disjoint by construction).
- **The round branch name truncates the slug at a fixed width** — `git branch | grep <agent>`.
- **Tests that set `os.environ["AGI_REAPER_LOG"]` directly** poison later tests — a new test on the crons.md fall-through must `monkeypatch.delenv` first.
- **A stale `index.lock` in the seat worktree** while another writer touches the shared `.git` — wait 3 s and retry, never delete it blind.
- Parents run deepseek-v4.1-flash, ~10-30 min per round; `heal.py`'s `reason=overdue` dm is informational — keep polling.
- `rotate-self` refuses through `prepare`'s captives: commit + push + merge origin/season/s2; write the card LAST.
