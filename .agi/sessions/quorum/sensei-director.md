# SESSION HANDOFF — 2026-09-12 sensei-director: THE SANCTUARY DIRECTOR (the g15 perpetual-goal seat) — LIVE SCRATCHPAD (gen VIII = loop L8 04:55Z–06:4xZ, rotated at 0.4 by `rotate-self --stops` (SL7.12, first live use); gen IX = loop L9 starts at §3; row generation 7 → the successor is gen 8 and acks NOTHING)

## §0 WHO YOU ARE (identity is SUPPLIED, never claimed)
Seat `sensei-director` in `config:seats` — the Sanctuary director: the director-kid that watches `goal:g15` and takes the Sensei's asks straight (founding order: owner 15:5xZ, verbatim at `doc:l4-owner-decisions` line 9; its two rules — no loop docs, one loop per generation — same node). Address = your ListAgents ref; window `sensei-director` in tmux; worktree `.agi/worktrees/seat-sensei-director`, branch `seat/sensei-director@s2`; Prime = `belam` — XIV since 03:18Z (ref: its first line to you) (`send.py send belam "<one line>" --from sensei-director`); Sensei = `master-sensei` gen 2 [f5de36] @309; point director = `sanctuary-director` (runs the L4 queue; you do not). Owner quotes live in nodes, never here.
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
## §3 🔴 STATE at rotation VIII → IX (gen VIII ref `013f1fb9-e3e4-4957-9ee5-e5637a5ec642`, window @316, loop L8 04:55Z–06:4xZ; row generation 7 → **your wake is ZERO calls: the predecessor answered `continue` (SL7.06 default, landed SL2#14); your session_ref cell stays empty by design; authority = the seat key**) — stamp 06:4xZ
| | |
|---|---|
| seat | `seat/sensei-director@s2` = origin/season/s2 (d0a35a27f, carries the FLIP — comms.verify ENFORCING) + **SL7.12 + SL7.14 harvested, NOT merged up → SL2#16** (never rebased). 568 send+rotate + 434 rotate/heal/sensei green; zero xfails. **SL7.15 and SL7.17 parents FINISHED at 07:00Z — harvest both FIRST THING** (table below); SL7.16 still running |
| landed this gen | **SL2#14** 05:21Z 42ce34503 (SL7.02/04/05/06/08/10/11; 11/11, 3782/15; 2396→ measured 2395/195/2590) · **SL2#15** 06:31Z 718b4308e (SL7.07/09/13 + briefs A-D; 11/11, 3796/15; **2407 / 195 / 2602**). mur-SL2.14: 7/7 ACCEPT, nine g15 lines → briefs A-D minted (SL7.14-17) + SL7.05 clause (2) narrowed + line (8) done by the Sensei. **mur-SL2.15 (07:00Z): 3/3 ACCEPT; 🔴 FLIP LANDED 6741ea746 06:57:50Z — comms.verify = ENFORCING** (every send must be signed; an UNSIGNED/UNKEYED dm now prints; a REFUSED rotation alert in the Sensei's read = the Prime rewinds to informational). **Seven residue lines TO MINT — verbatim in g15's 07:0xZ note** (two-tree alert fixture for SL7.14; deferred key swap orphans the minted key on push FAILED; _seats_ownrow_content pairs by index; value-agnostic edited_by predicate; cmd_spawn commits the predecessor's --pid + discards the join; sensei.py by-hand classification + SL7.13 kid-2 node still describes the snapshot detector; two _record_join copies → one by import). Group by file: rotate.py lines (2)(3)(4)(5)(7) — behind SL7.15/16/17; send/test line (1) — behind nothing (SL7.14 landed on the seat); (6) partly the Sensei's (rotations.md) |
| wake / out | gen VIII wake 0 (first live proof of the owner order). Out = ONE call (`rotate-self --stops`, SL7.12) — if it refused and I fell back to the 4-call path, the record says so |
| Prime | belam XIV rotated at 07:0xZ (--ask-diff) → **XV takes SL2#16**; ask ITS ref from the rotation-alert dm (`send.py read --dm belam --from sensei-director`) or `send.py whois`. Window rule now on g17.1: no post commits MAIN inside a granted window |
| Sensei | master-sensei gen 2 [f5de36] @309. All asks landed (A SL7.04, B SL7.07, C SL7.02, owner order SL7.06). Waiting on SL7.16 (brief C) for the rotations.md:56 by-key form — the template edit is the Sensei's; the round reports the line |
| credits | 06:33Z **$21.86 left** before SL7.14-17 (~$0.4 each → ~$20); a 403 = ONE line to the Prime, stop. Floor $1.00 |
| traps paid this gen | `send.py read <seat>` reads THAT seat's inbox (dms = `read --dm`) — now REFUSED by SL7.13's gate · unquoted heredoc / double-quoted send line runs backticks · metrics.py counts the cwd's graph — measure with cwd=MAIN · a leak detector on a shared live dir guards the RESOLVER, never diffs the directory (SL7.13's snapshot fired on live dms) |

### Rounds in flight (harvest each: fetch · merge-base diff · grep -ci rebase · THOUGHT:BEGIN ≤ 1 per new node · read kid nodes · merge --no-ff · neighbourhood tests · note · render · push). All four are mur-SL2.14 briefs; B/C/D share rotate.py in DISJOINT functions (EXCLUDED lists in each) — expect small merge conflicts at harvest, resolve by function, never rebase.

| round · agent · branch | brief | gate · tests | since |
|---|---|---|---|
| **SL7.15** a00-e9b20f31 `…hypothesis-l4-the-ack-no-op-checks-…-a00-e9b20f31` | B `hypothesis:l4-the-ack-no-op-checks-gen-after-a-completed-rotation-rotates-the-ack-file-and-a-heal-recovery-still-takes-its-identity` (g15.25 lines (3)(9)) | gen-aware no-op; ack file rotated on success; heal crash-recovery end-to-end takes identity; bootstrap ack fact from the file · rotate + heal | 06:36Z |
| **SL7.16** a00-91bb3a6a `…hypothesis-l4-prime-authority-…-a00-91bb3a6a` | C `hypothesis:l4-prime-authority-resolves-by-key-when-the-prime-rows-session-ref-is-empty-and-a-placeholder-with-a-fallback-never-refuses` (g15.25 line (4), F18 code half) | whois --key/--seat; placeholder fallback never refuses; config:rotations READ-ONLY (report the :56 line to the Sensei) · rotate + send | 06:36Z |
| **SL7.17** a00-70b89d45 `…hypothesis-l4-prepare-check-2-…-a00-70b89d45` | D `hypothesis:l4-prepare-check-2-reads-the-index-blob-and-the-writers-marker-guard-is-the-readers-regex` (g15 lines (5)(6)) | index-only real change reads dirty; create --set marker guard = reader regex; frontmatter test off the live graph; stitch pre-check gone; render --check byte-identical · rotate/write/stitch/frontmatter | 06:36Z |

Harvested this gen: SL7.08 · SL7.10 · SL7.11 (SL2#14) · SL7.07 · SL7.09 · SL7.13 (SL2#15) · **SL7.12 + SL7.14 06:55Z (on the seat → SL2#16; SL7.14 re-specced three SL7.02 whois-quarantine tests: an unresolvable --sig ref reads UNVERIFIABLE — name it in the numbers line for mur)**. Round branches spell `season2/loops/<slug>-<agent>`; `git branch --format='%(refname:short)' | grep <agent>`.

### Queue — in this order

1. Harvest whichever of SL7.15-17 is gone (`spawn_budget.py status | grep "tier=parent iter=SL7"`), then **SL2#16** = SL7.12 + SL7.14 + the harvested (ask the window EARLY — mur-SL2.15 may hold the lock; the Prime says HOLD/GO): ask belam "window?" → merge on MAIN ONLY on the GO line → render + --render --check → `commands.py run verify-suite` (BACKGROUND, ~5 min) → grid commit → push season/s2 + refs/grid → `verification.py --level rotation --stamp` → ONE line: five MEASURED numbers (cwd=MAIN) incl. suite passed/skipped, merge sha, stamp sha, one line per goal. Baseline 2407/195/2602, active never lower. NEVER hold a merge on MAIN longer than the suite; if the suite is red, fix on the seat, merge again, re-run (SL2#15 shape).
2. **line (4)** `hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up` — re-read against SL7.12's `--stops` (the hook fires `rotate-self --stops`), brief the stops text source, dispatch AFTER SL7.15/16/17 harvest (rotate.py owners) — hooks/rotation_alert.py + rotate.py pre-spawn region.
3. When the Prime FLIPS (after mur-SL2.15): expect a live-prove ask through the Sensei; the flip round is the Prime's.
4. **Dispatch line:** `python3 extensions/agi/bin/dispatch.py . SL7.<nn> --target <id> --level small --tier parent --harness pi --branch` (commit + push first; exit 3 stale-base = merge origin/season/s2, push, re-run).

### 🔴 Where it stops — the next command (stamp 06:4xZ)
gen IX: harvest SL7.15 (a00-e9b20f31, brief B) and SL7.17 (a00-70b89d45, brief D) FIRST — both parents finished 07:00Z; SL7.16 (a00-91bb3a6a, brief C) running; then SL2#16 = SL7.12 + SL7.14 + the harvested: window from belam XV (the Prime rotated 07:0xZ), merge on MAIN only on the GO, suite in the background, MEASURED numbers with cwd=MAIN (baseline 2407/195/2602; name the SL7.14 whois-quarantine re-spec). comms.verify is ENFORCING since 6741ea746. Seven mur-SL2.15 lines to mint are verbatim in g15 note 07:0xZ (rotate.py lines behind SL7.15/16/17; the two-tree alert fixture line behind nothing). Then line (4).
## §4 TRAPS (live ones only; fixed-in-code traps deleted)
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
