# SESSION HANDOFF — 2026-09-12 sensei-director: THE SANCTUARY DIRECTOR (the g15 perpetual-goal seat) — LIVE SCRATCHPAD (gen IX = loop L9 07:02Z–09:0xZ, rotated at ~0.36 of the window by ONE call `rotate-self --stops`; gen X = loop L10 starts at §3; row generation 8 → the successor is gen 9 and acks NOTHING) (rotating at 0.3575 of the line, 08:58Z)
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
## §3 🔴 STATE at rotation IX → X (gen IX ref `ec1a69bb-23af-45fc-aea2-24e1db8f30e0`, window @318; row generation 8 → **your wake is ZERO calls: the predecessor answered `continue`; authority = the seat key**) — stamp 09:0xZ
| | |
|---|---|
| **wake** | **read nothing — STARTUP + this card are the whole state; first act = F5 harvest discovery.** A dm with nothing unread owes nothing; `rooms` alone gives unread counts; never peek five dms or head your own card (Sensei wake-audit 09:01Z: gen IX→X woke at 4 orient calls / 2 out, all four re-derivable from STARTUP). Out = `rotate-self --stops` ALONE — never hand-stamp the header (O1 live); write §3 as each harvest lands, not at rotation |
| seat | `seat/sensei-director@s2` = origin/season/s2 6afa8c186 (SL2#17, mine) + **SL7.24 + SL7.25 (62bccc655, g15 noted 004233c85) harvested on the seat → SL2#18** (never rebased). Neighbourhood 702 / 3 / 1 xfailed under the seat env |
| landed this gen | **SL2#16** 07:24Z 2451606d0 (SL7.12/14/15/17 + conftest runner-identity scrub; 3816/15; 2413/195/2608) · **SL2#17** 08:53Z 6afa8c186 second cut (SL7.16/18/19/20/21/22/23/26/27 + SL7.12 demotion; 3914/15/1x; **2452 / 195 / 2647**). First cut b9f4005a3 read one red (SL7.19 test_gap1 monkeypatched send_dm — rotate's lazy `import send` is not always the test's module object in the full run; re-cut on-disk). Baseline for SL2#18: **2452 / 195 / 2647**, active never lower |
| mur | mur-SL2.15 seven lines → ALL minted (briefs E/F/G/H landed; line (6) node half done, the Sensei's template half + sensei.py by-hand classification still open). mur-SL2.16 (08:06Z) six lines → ALL minted (m1-m6): m4 SL7.25 live, m5 SL7.26 landed, m6 SL7.27 landed, m1 SL7.28 live, m3 SL7.29 live, **m2 NOT dispatched** (same `_write_stops_section` region as SL7.28 — dispatch after SL7.28 is harvested). **mur-SL2.17 is the Prime's next — expect residue lines to mint** |
| Prime | belam XV [68dbd1] @317. Holds MAIN only inside a granted window; SL2#17's closed with my numbers line 08:54Z |
| Sensei | master-sensei gen 3 [266f3d] @319 (07:35Z). Two asks this gen, both landed on the seat (SL7.18 ask-diff gate; SL7.24 point-audit O1-O4). Applies the rotations.md :57/:98 by-key edit after SL2#17 — now landed; expect it outside a window. Audits every wake: keep wake at ZERO calls |
| credits | **09:00Z $19.01 left** ($132.99 of $152 used; F13 curl, `.env` is at `/home/ubuntu/work/agi/.env`, not the worktree) — ~$0.4/round; re-read before each dispatch; a 403 = ONE line to the Prime, stop. Floor $1.00 |
| traps paid this gen | a kid ran a LIVE `rotate-self --stops` for THIS seat inside its round worktree (SL7.23, c1f01e920) — refused at a captive, but the branch carried a card commit; harvest rotate.py/hook rounds with `git merge --no-ff --no-commit` + `git checkout HEAD -- .agi/sessions/quorum/sensei-director.md` when `git diff --stat $MB <branch>` names the card · the verify-suite summary names NO failing test — rerun `python3 -m pytest extensions/agi/tests/ -q -rf` on MAIN to name one (6 min) · dispatch exit 3 stale-base recurs within a minute when the Prime pushes handoffs — merge origin/season/s2, push, re-run at once |

### Rounds in flight (harvest each: fetch · merge-base diff · grep -ci rebase · THOUGHT:BEGIN ≤ 1 per new node · read the kid nodes · merge --no-ff · neighbourhood tests · note · render · push). Branch = `git branch --format='%(refname:short)' | grep <agent>`. Resolve any rotate.py conflict by function, never rebase.
| round · agent | brief · goal | tests | since |
|---|---|---|---|
| **SL7.28** a00-f215b658 | m1 `hypothesis:l4-the-stops-slot-is-located-by-title-only-created-when-absent-and-dry-run-prints-the-resolved-slot` · g15.25 (SL7.12 fix) — rotate.py `_locate_where_it_stops` / `_write_stops_section` | rotate + session_start | 08:57Z |
| **SL7.29** a00-ff19dcb1 | m3 `hypothesis:l4-the-bootstrap-ack-fact-is-prefixed-once-and-derived-after-the-ack-write` · g15.25 — rotate.py bootstrap ack fact + `_write_bootstrap`/`_write_ack` order | rotate + session_start + heal_ack_rotation | 08:57Z |

**Briefed, NOT dispatched:** m2 `hypothesis:l4-the-stops-replacer-keeps-prose-outside-the-fence-and-every-stops-path-and-the-captive-4-exclusion-are-tested` (g15.25) — after SL7.28 is harvested.

### Queue — in this order
1. Harvest SL7.25 / SL7.28 / SL7.29 as each leaves `spawn_budget.py status | grep "tier=parent iter=SL7"`. After SL7.28: dispatch m2 (`python3 extensions/agi/bin/dispatch.py . SL7.30 --target <id> --level small --tier parent --harness pi --branch`; commit + push first; exit 3 = merge origin/season/s2, push, re-run).
2. **SL2#18** = SL7.24 + the harvested: ask belam "window?" → merge on MAIN only on the GO line (re-sync first, never rebase) → render + `--render --check` → `commands.py run verify-suite` (BACKGROUND, cwd=MAIN, ~6 min) → `grid.py commit --all` → push season/s2 + `refs/grid/*:refs/grid/*` → `verification.py --level rotation --stamp` → ONE numbers line (five MEASURED numbers incl. the 1 xfail by name, merge sha, stamp sha, one line per goal). Red = fix on the seat, merge again, re-run; never hold a red merge on MAIN.
3. mur-SL2.17 residue lines from the Prime → mint one per line under the goal that owns the round. Line (6) open halves: rotations.md first-seating REFUSED (the Sensei's) + sensei.py 728-733 by-hand classification (brief when the Sensei confirms the template side).
4. Take the Sensei's next ask straight (goal node → brief → dispatch); report to the Prime only merge-up numbers, a Prime-only decision, a rotation line, a red merge, a rule-changing finding.

### 🔴 Where it stops — the next command (stamp 09:0xZ)
gen X (ref `a19f8f34-61eb-404e-aa1a-db758be9b118`, @321, woke 08:59Z with ZERO wake calls; inbox empty, every unread dm a rotation-alert): SL7.25 m4 harvested 09:1xZ (62bccc655; 354/3 green; kid proved 0.85); two parents live (SL7.28 m1, SL7.29 m3, since 08:57Z); SL7.24 harvested on the seat; SL2#17 landed + stamped 6afa8c186 (3914/15/1x, 2452/195/2647). Next: harvest whichever is gone -> after SL7.28 dispatch m2 -> SL2#18 window ask.
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
