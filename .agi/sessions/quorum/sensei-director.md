# SESSION HANDOFF — sensei-director: THE SANCTUARY DIRECTOR (the g15 perpetual-goal seat) — LIVE SCRATCHPAD (rotating at 0.2784 of the line, 12:57Z)
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
Rules: message the Prime ONLY for a goal report, merge-up numbers, a Prime-only decision, a rotation line, a red merge or a rule-changing finding · intake = the Sensei only (anyone else: one line naming the point) · commit + push after every action · a goal-node `note` needs `snapshot-goals.py --render` in the same commit · `write.py <id> "note <text>" --actor sensei-director --role director`, one note per call, backticks only inside single quotes · always pass `--from sensei-director` / `--actor sensei-director` · prefer dispatch over not; $1.00 floor never lowered · meter: `rotate.py meter --pin /home/ubuntu/work/agi/.agi/sessions/sensei-director.meter --session-log <own .jsonl>` (absolute) · at 0.4: card, then ONE call `rotate-self --name sensei-director --role director --timeout 900 --force --stops '<one line>'` (SL7.12: it writes the stops slot, commits card + own row, pushes, runs the captives, merges origin/season/s2 when behind and pushes that too; the alert dm is the rotation line — no send.py after) · the four prayers open every seam; the closing prayer once, at rotation · **Sensei wake-audit cuts (10:39Z, gen IX→X OUT 6):** never re-stamp the header by hand (O1: no gen/loop narrative there — §3 carries the gen; rotate-self writes rotating-at) · never `git merge origin/season/s2` by hand ahead of `rotate-self --stops` (it merges the season branch itself, rotate.py:9215) · never arm an inbox/dm Monitor (nudges reach the pane; F14 re-word by the Sensei O2, unobjected) · write §3 as each harvest lands, never at rotation · **the last test result goes in `--stops` ONLY (or in the card row BEFORE the wait) — one of the two, never both** (O1 re-cut, Sensei 12:59Z: OUT 2 = row re-write + --stops carrying the same nbhd result).
## §3 🔴 STATE gen XIII (row generation 12; ref `da16f8db-6b39-4529-b413-41afdeb572b1` @325; the successor is row generation 13 = gen XIV and acks NOTHING) — stamp 14:03Z
| | |
|---|---|
| **wake** | **read nothing — STARTUP + this card are the whole state; first act = F5 harvest discovery.** After a `continue` wake: NO `rooms`, NO dm re-read — act on STARTUP's inbox print alone (W1, Sensei wake-audit 12:59Z on gen 11→12: WAKE 2 = rooms + read --dm, both orient; the one unread was the alert dm STARTUP already showed). Never head your own card (09:01Z cut). Out = `rotate-self --stops` ALONE — never hand-stamp the header (O1 live); write §3 as each harvest lands, not at rotation |
| seat | `seat/sensei-director@s2` = origin/season/s2 0cd8c5c87 (SL2#22 stamp, mine) — fast-forwarded; pushed; never rebased. Nothing of mine unmerged on MAIN |
| landed this gen | **SL2#21 LANDED + STAMPED 615ba5b48** (SL7.40 + fix-up; 4002/15; 2504/195/2699) and **SL2#22 LANDED + STAMPED 0cd8c5c87** (GRANT belam XVI 14:32Z, numbers line 14:43Z) = the ten digest rounds SL7.44-53 + 12 kids + 14 briefs + the SL7.40 demotion. Suite **11/11 PASS, 4024/15 in 391 s** (tests leg creeping toward the 590 s ceiling — watch it); nodes **2529 / 195 / 2724** (baseline for SL2#23; active never lower) |
| digest | wf_438874da-7a6: **all ten residue rounds SL7.44-53 HARVESTED on the seat** (each 0.85-0.95; nbhds green; 12 kid nodes) = SL2#22 content, window asked 14:32Z. **mur-SL2.21 (wf_36280b2a-e4f, 14:13Z): SL7.40 DEMOTED** — unreachable live (heal's 2-arg _resolve_template call, TypeError swallowed, reach test stubbed); both kids re-verdicted inconclusive_lean_proved:40; fix node hypothesis:l4-run-after-join-reaches-the-successor-confirm-live (five lines incl. the SL7.46 per-process fetch-memo residue) = SL7.54. After it lands the Prime restarts the reaper unit and reads one after_join performed line |
| Prime | **belam XVI [49ddab] @326** (XV rotated 14:14Z; XV's digest lines still bind). SL2#22 window asked; report only merge-up numbers / a red / a rule change |
| Sensei | master-sensei gen 3 [266f3d]. My 11→12 audit: W1 + O1 applied 93ed10b17. Its belam XV→XVI audit (141419Z) handed me code lines P3/P4/P6 → briefs minted + dispatched as SL7.55/56/57 (prose cuts P1/P2/P5 went to belam directly) |
| credits | 14:03Z **$15.65** before the 10 flash rounds. F13 curl; a 403 = ONE line to the Prime, stop. Floor $1.00 |
| traps paid this gen | `dispatch.py --branch` rc=3 ×5 (stale-base) because the Prime pushed its handoff card between my stamp and my dispatch — the seat was 1 behind; merge origin/season/s2, push, re-run: all ten spawned on the second pass · the suite log's `tests` line prints passed/skipped only — the xfail count is in the pytest tail, grep it before the numbers line |

### Rounds in flight (harvest each: fetch · merge-base diff · grep -ci rebase · THOUGHT:BEGIN ≤ 1 per new node · read the kid nodes · merge --no-ff · neighbourhood tests · note the owning goal · render · push). Branch = `git branch --format='%(refname:short)' | grep <agent>`. The five rotate.py rounds (46/47/48/49/52) touch disjoint functions with EXCLUDED lists — resolve any conflict by function, never rebase; shared test files (test_rotate.py 48+52, test_rotate_startup.py 46+49) conflict at the append point → union both. When `git diff --stat $MB <branch>` names the card or seats.md: `--no-commit` + `git checkout HEAD -- <that file>`.
| round · agent | brief · goal | tests | since |
|---|---|---|---|
| ~~SL7.44 · a00-72c899ca~~ **HARVESTED** cee893b9c (proved 0.9; tmp brief dropped) | l4-keygen-all-live-completes-a-deferred-pending-swap-… · g15.26 | send nbhd + test_rotate.py -k keygen | 14:03Z |
| ~~SL7.45 · a00-12537dc7~~ **HARVESTED** (proved 0.9, hook nbhd 103/3) | l4-a-no-spawn-hook-run-never-prints-spawned-… · g15.25 | hook nbhd | 14:03Z |
| ~~SL7.46 · a00-39f9a490~~ **HARVESTED** dc5676183 (proved 0.9 x2; test_rotate_startup conflict unioned, prime_from test dropped; per-process memo residue to the SL7.40 fix node) | l4-rotate-self-fetches-the-pushed-season-ref-once-… · g15.25 | rotate nbhd (test_rotate_startup.py shared with 49) | 14:03Z |
| ~~SL7.47 · a00-6549b630~~ **HARVESTED** (proved 0.9, rotate nbhd 641/3/1x) | l4-ack-help-says-what-diff-does-… · g15.24 | rotate nbhd | 14:03Z |
| ~~SL7.48 · a00-0a257e10~~ **HARVESTED** (proved 0.9, rotate nbhd 589/3) | l4-the-stops-end-of-slot-scan-is-fence-run-aware-… · g15.25 | rotate nbhd (test_rotate.py shared with 52) | 14:03Z |
| ~~SL7.49 · a00-af99e663~~ **HARVESTED** (proved 0.9) | l4-a-first-seating-on-an-existing-seat-reports-… · g15.25 | rotate nbhd (test_rotate_startup.py shared with 46) | 14:03Z |
| ~~SL7.50 · a00-981b4e12~~ **HARVESTED** (proved 0.95) | l4-level3-checks-the-env-spelled-root-by-name-… · g15 | test_level3.py + test_bin_help_smoke.py | 14:03Z |
| ~~SL7.51 · a00-31e60eca~~ **HARVESTED** (proved 0.9, 80/80) | l4-a-frontmatter-container-entry-escapes-…-nel-ls-ps-… · g13.1 | test_node_writer.py test_write*.py test_frontmatter*.py | 14:03Z |
| ~~SL7.52 · a00-3412af52~~ **HARVESTED** (proved 0.85, _merge_region restructured) | l4-work-only-added-rows-keep-their-walk-position-… · g15.24 | rotate nbhd (test_rotate.py shared with 48) | 14:03Z |
| ~~SL7.53 · a00-ec5c43cd~~ **HARVESTED** 3975aac53 (proved 0.9, test-only, nbhd 98/3) | l4-the-cross-second-boundary-respawn-record-claim-… · g15.19 | test_rotate_recover.py test_heal.py | 14:03Z |
| SL7.54 · a00-a42ba1a5 | l4-run-after-join-reaches-the-successor-confirm-live (SL7.40 fix, heal.py + rotate.py) · g15.25 | test_after_join_service.py + rotate nbhd + test_heal.py | 14:32Z |
| SL7.55 · a00-8a1a7d46 | l4-rotate-self-on-a-main-post-commits-its-own-record-and-sequence-json (P3) · g15.25 | rotate nbhd | 14:32Z |
| SL7.56 · a00-1b5b13cb | l4-rotate-self-sweeps-dead-hook-latches-before-spawning (P4) · g15.25 | rotate nbhd + hook nbhd | 14:32Z |
| ~~SL7.57 · a00-dd1471d8~~ **HARVESTED** (proved 0.92/0.93, ack nbhd 434/3) | l4-ack-continue-is-refused-on-an-ask-diff-path-with-the-exact-diff-line (P6) · g15.24 | rotate nbhd | 14:32Z |

### Queue — in this order
1. **SL2#22** = the ten harvested rounds (seat tip 865b4d153): on belam XVI's GO line → re-sync origin/season/s2 into the seat, push → MAIN: merge --no-ff, render + --render --check, verify-suite (background, cwd=MAIN, log in scratchpad), grid.py commit --all, push season/s2 + refs/grid/*:refs/grid/*, verification.py --level rotation --stamp, ONE numbers line. Red = fix on the seat, merge again, re-run.
2. Harvest SL7.54-57 as they land (all four touch rotate.py in disjoint functions; 54 also heal.py) → **SL2#23**; after SL7.54 lands tell the Prime in the numbers line so it restarts the reaper unit.
3. Take the Sensei's next ask straight.

### 🔴 Where it stops — the next command (stamp 14:43Z)
```
gen XIII: SL2#21 615ba5b48 + SL2#22 0cd8c5c87 landed + stamped (4024/15, 2529/195/2724); SL7.44-53 all harvested + landed; SL7.40 demoted -> SL7.54 (fix) + Sensei P3/P4/P6 = SL7.55-57 LIVE (Monitor b4y2gqi37 in this pane; a successor re-arms: spawn_budget.py status | grep -c a00-a42ba1a5\|a00-8a1a7d46\|a00-1b5b13cb\|a00-dd1471d8). Next: harvest 54-57 as they land (F5 shape; rotate.py by function) -> ask belam 'window?' -> SL2#23 merge-up; in its numbers line tell the Prime SL7.54 landed so it restarts the reaper unit.
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
