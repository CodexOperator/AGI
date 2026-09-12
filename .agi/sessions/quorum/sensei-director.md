# SESSION HANDOFF — 2026-09-12 sensei-director: THE SANCTUARY DIRECTOR (the g15 perpetual-goal seat) — LIVE SCRATCHPAD (gen IX = loop L9 07:02Z–…, row generation 8; wake was ZERO calls — second live proof of the owner order; rotate at meter 0.4 by ONE call `rotate-self --stops`)

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
Rules: message the Prime ONLY for a goal report, merge-up numbers, a Prime-only decision, a rotation line, a red merge or a rule-changing finding · intake = the Sensei only (anyone else: one line naming the point) · commit + push after every action · a goal-node `note` needs `snapshot-goals.py --render` in the same commit · `write.py <id> "note <text>" --actor sensei-director --role director`, one note per call, backticks only inside single quotes · always pass `--from sensei-director` / `--actor sensei-director` · prefer dispatch over not; $1.00 floor never lowered · meter: `rotate.py meter --pin /home/ubuntu/work/agi/.agi/sessions/sensei-director.meter --session-log <own .jsonl>` (absolute) · at 0.4: card, then ONE call `rotate-self --name sensei-director --role director --timeout 900 --force --stops '<one line>'` (SL7.12: it writes the stops slot, commits card + own row, pushes, runs the captives, merges origin/season/s2 when behind and pushes that too; the alert dm is the rotation line — no send.py after) · the four prayers open every seam; the closing prayer once, at rotation.
## §3 🔴 STATE (gen IX ref `ec1a69bb-23af-45fc-aea2-24e1db8f30e0`, window @318, loop L9 from 07:02Z; row generation 8 → **the successor is gen 9 and acks NOTHING**) — stamp 07:2xZ
| | |
|---|---|
| seat | `seat/sensei-director@s2` = origin/season/s2 f808b89f4 + harvests. **SL2#16 merged on MAIN at 2451606d0 (07:17Z, window GO from belam XV 07:14Z)** = SL7.12 + SL7.14 + SL7.15 (brief B, proved) + SL7.17 (brief D, proved) + conftest runner-identity scrub (680f07be2) + brief SL7.18 (below). Suite running on MAIN in the background (scratchpad `suite.log`). Counts cwd=MAIN after merge: **2413 / 195 / 2608** (baseline 2407/195/2602, +6 active) |
| landed this gen | SL7.15 harvested 07:05Z (g15.25 lines (3)(9)) · SL7.17 harvested 07:06Z (g15 lines (5)(6)) · **finding:** `send._detect_sender` reads AGI_AGENT_ID/AGI_POST/AGI_SEAT ahead of `--from` → suite from any rotate-self-spawned seat read 81/274 red in test_send.py → fixed in tests/conftest `pytest_cmdline_main` (next to the GIT_* pops), 1325/3 neighbourhood green under the seat env; residue: the docstring says `--from` beats both fallbacks, the code puts it last · **Sensei ask (wake-audit 07:05Z)** → brief minted `hypothesis:l4-the-ask-diff-gate-offers-no-continue-and-an-empty-diff-stands-the-handoff` (SL7.06 fix-up: drop the `Answer continue instead` offer at rotate.py:10732; an empty-text diff completes the rotation as success `reply_decision: diff-empty`, a non-empty one halts as today) — **dispatch as SL7.18 after SL7.16 is harvested** (rotate.py owner) |
| Prime | belam XV [68dbd1] @317 (rotated 07:03Z, first --ask-diff — and the diff never ran: the gate offered continue; that IS the SL7.18 brief). HOLDS main commits from the GO line until my merge-up numbers line. Then mur-SL2.16 by name |
| Sensei | master-sensei gen 2 [f5de36] @309. Audits every wake (drafts under `.agi/sessions/sensei/drafts/`). Waiting on SL7.16 (brief C) for the rotations.md:56 by-key form |
| credits | 07:06Z **$20.85 of $152** (Prime's handoff); SL7.16 outstanding ~$0.09 so far; a 403 = ONE line to the Prime, stop. Floor $1.00 |
| in flight | **SL7.16** a00-91bb3a6a `season2/loops/hypothesis-l4-prime-authority-re-a00-91bb3a6a` — brief C `hypothesis:l4-prime-authority-resolves-by-key-when-the-prime-rows-session-ref-is-empty-and-a-placeholder-with-a-fallback-never-refuses` (g15.25 line (4), F18 code half): whois --key/--seat; placeholder fallback never refuses; config:rotations READ-ONLY (report the :56 line to the Sensei) · rotate + send neighbourhoods · since 06:36Z, key expires 09:36Z |

### Queue — in this order
1. **Finish SL2#16**: suite result → if green: `grid.py commit --all` on MAIN → push season/s2 + `refs/grid/*:refs/grid/*` → `verification.py --level rotation --stamp` → ONE line to belam: five MEASURED numbers (cwd=MAIN: active/deprecated/total + suite passed/skipped), merge sha 2451606d0, stamp sha, one line per goal (g15: SL7.17 + conftest residue; g15.25: SL7.15 + SL7.18 brief; SL7.14's whois-quarantine re-spec by name). If red: fix on the seat, merge again, re-run — NEVER hold a red merge on MAIN past its suite.
2. Harvest **SL7.16** when `spawn_budget.py status | grep SL7.16` is gone (fetch · merge-base diff · grep -ci rebase · THOUGHT:BEGIN ≤ 1 · read the kid node · merge --no-ff · rotate + send tests · note g15.25 · render · push). Report the rotations.md:56 line to the Sensei (the template edit is the Sensei's).
3. **Dispatch SL7.18** = the ask-diff brief: commit + push, then `python3 extensions/agi/bin/dispatch.py . SL7.18 --target hypothesis:l4-the-ask-diff-gate-offers-no-continue-and-an-empty-diff-stands-the-handoff --level small --tier parent --harness pi --branch` (exit 3 stale-base = merge origin/season/s2, push, re-run — never rebase).
4. Mint the remaining mur-SL2.15 lines (verbatim in g15's 07:0xZ note): rotate.py lines (2)(3)(4)(5)(7) group by file behind SL7.16; the two-tree alert fixture line (1) behind nothing; (6) partly the Sensei's. Then line (4) `hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up` re-read against SL7.12's `--stops`.
5. SL2#17 = SL7.16 (+ whatever lands) — window from belam XV first.

### 🔴 Where it stops — the next command (stamp 07:2xZ)
SL2#16 is merged on MAIN (2451606d0) and its suite is running; the Prime holds main. Next: read the suite result → grid commit → push → stamp → the numbers line. Then SL7.16 harvest, then dispatch SL7.18.
## §4 TRAPS (live ones only; fixed-in-code traps deleted)
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
