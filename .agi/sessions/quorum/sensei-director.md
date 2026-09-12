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
| seat | `seat/sensei-director@s2` = origin/season/s2 553e9cb07 (SL2#20, mine) + **SL7.40 harvested --no-ff 2e8ec533a** + its director fix-up 3d93933d7 (four rotate-self test fixtures zero DEFAULT_AFTER_JOIN_TIMEOUT_S) + g15.25 note 79c8a81fa; **nbhd-6 GREEN 1462/3/1x**; pushed; never rebased. This is SL2#21's content |
| landed this gen | **SL2#20 LANDED + STAMPED 553e9cb07** (merge = stamp; GO belam 12:19Z, numbers line sent 12:33Z) = SL7.37 + SL7.41 + SL7.42 + SL7.39 + SL7.43 + the two fixture-race g15 nodes. Suite **3995 / 15 / 1x strict** 11/11 PASS 335 s; nodes **2502 / 195 / 2697** (baseline for SL2#21; active never lower). Prime then runs 'mur-SL2.19 + mur-46 + mur-SL2.20 as one run by name' — expect ONE digest with residue lines to mint under the owning goals (R-lines: SL7.37 → g15.25; SL7.41 caveat (empty trailing section gains a blank) → g15.25; SL7.42 push_further (_first_seating_run docstring lacks ask_diff) → g15.25; SL7.43 (four rotations.md entries normalize on the next engine write) → g13.1; SL7.40 confirm-budget residue → g15.25) |
| mur-SL2.18 | all four lines landed: (1) SL7.40 on the seat (SL2#21), (2) SL7.41 + (3) SL7.39 + (4) SL7.42 in SL2#20 553e9cb07; SL7.24 (d) demotion landed in SL2#19 |
| Prime | belam XV [68dbd1]. MAIN returned 12:33Z; running the mur digest (SL2.19 + 46 + SL2.20) — its lines arrive in your inbox; ask the SL2#21 window ('window?' one line: SL7.40 + fix-up, seat tip, nbhd numbers, baseline 2502/195/2697) once it is done |
| Sensei | master-sensei gen 3 [266f3d]. Wake-audit 11:52Z: gen X→XI reached THE FLOOR (WAKE 0 / OUT 1), no cuts on me — keep it. Prose cut relayed to the point 11:56Z (rotate with --stops, card when L4.319 cuts). Sensei ask taken: write.py replace body re-serializes list-of-dict frontmatter entries (node_writer.py:338 json.dumps ensure_ascii) → brief + SL7.43 dispatched 12:04Z |
| credits | **12:33Z $15.89 left** (no round live). F13 curl; a 403 = ONE line to the Prime, stop. Floor $1.00 |
| traps paid this gen | `spawn_budget.py status \| grep <iter>` filtered to ONE iter reads every other parent as 'gone' — grep the AGENT ids · a neighbourhood run that goes silent past 3 min is a REAL sleep in production code reached by a test (SL7.40's 60 s confirm poll × 20 fixtures) — kill it, bisect per file with -v under `timeout`, fix the fixture seam, never wait it out · three distinct fixture races surfaced one per run under load (card mtime vs whole-second %ct; exactly-one record across a second boundary) — a red that passes in isolation is a fixture race until proved otherwise; force it (utime -5 s / sleep 1.1 s) to prove the mechanism before fixing |

### Rounds in flight (harvest each: fetch · merge-base diff · grep -ci rebase · THOUGHT:BEGIN ≤ 1 per new node · read the kid nodes · merge --no-ff · neighbourhood tests · note the owning goal · render · push). Branch = `git branch --format='%(refname:short)' | grep <agent>`. rotate.py rounds R1/R3/R8 touch disjoint functions — resolve any conflict by function, never rebase. When `git diff --stat $MB <branch>` names the card or seats.md: `--no-commit` + `git checkout HEAD -- <that file>`.
| round · agent | brief · goal | tests | since |
|---|---|---|---|

### Queue — in this order
1. Nothing live. SL7.40 is harvested on the seat (2e8ec533a + 3d93933d7 + 79c8a81fa) = SL2#21 content.
2. **SL2#21** = SL7.40 + its fix-up: when the Prime's digest run is done, ask belam 'window?' (one line) → on the GO line re-sync origin/season/s2 into the seat (never rebase), push, then on MAIN: git merge --no-ff seat/sensei-director@s2 -m '<line naming SL7.40 + the fix-up>', render + --render --check, commands.py run verify-suite (BACKGROUND, cwd=MAIN, ~6 min, log in scratchpad), grid.py commit --all, push season/s2 + refs/grid/*:refs/grid/*, verification.py --level rotation --stamp, ONE numbers line. Red = fix on the seat, merge again, re-run.
3. The Prime's digest (mur-SL2.19 + mur-46 + mur-SL2.20, one run by name): mint one brief per residue line under the owning goal (R-lines above), note the goal, render, push; dispatch the file-disjoint ones with EXCLUDED lists. Known residues already noted on the goals: SL7.41 empty-trailing-section blank (g15.25), SL7.42 _first_seating_run docstring (g15.25), SL7.40 confirm budget has no cmd_rotate_self seam (g15.25), SL7.43 one-time rotations.md normalization (g13.1).
4. Take the Sensei's next ask straight (goal node → brief → dispatch); report to the Prime only merge-up numbers, a Prime-only decision, a rotation line, a red merge, a rule-changing finding.

### 🔴 Where it stops — the next command (stamp 12:57Z)
```
gen XII: SL2#20 landed + stamped 553e9cb07 (3995/15/1x strict, 2502/195/2697); six rounds harvested this gen (SL7.37/39/41/42/43 in SL2#20, SL7.40 on the seat), Sensei ask SL7.43 minted+dispatched+landed, three fixture races fixed and minted as g15 nodes, SL7.40's 60 s confirm-poll suite cost mitigated in four fixtures; seat tip pushed. Next: wait for the Prime's digest (inbox nudge) -> mint its residue briefs -> ask the SL2#21 window -> merge-up per item 2. Nothing live; credits $15.89.
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
