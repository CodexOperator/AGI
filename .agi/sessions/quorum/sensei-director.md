# SESSION HANDOFF — sensei-director: THE SANCTUARY DIRECTOR (the g15 perpetual-goal seat) — LIVE SCRATCHPAD (rotating at 0.3716 of the line, 16:09Z)
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
Rules: message the Prime ONLY for a goal report, merge-up numbers, a Prime-only decision, a rotation line, a red merge or a rule-changing finding · intake = the Sensei only (anyone else: one line naming the point) · commit + push after every action · a goal-node `note` needs `snapshot-goals.py --render` in the same commit · `write.py <id> "note <text>" --actor sensei-director --role director`, one note per call, backticks only inside single quotes · always pass `--from sensei-director` / `--actor sensei-director` · prefer dispatch over not; $1.00 floor never lowered · meter: `rotate.py meter --pin /home/ubuntu/work/agi/.agi/sessions/sensei-director.meter --session-log <own .jsonl>` (absolute) · at 0.4: card, then ONE call `rotate-self --name sensei-director --role director --timeout 900 --force --stops '<one line>'` (SL7.12: it writes the stops slot, commits card + own row, pushes, runs the captives, merges origin/season/s2 when behind and pushes that too; the alert dm is the rotation line — no send.py after) · **prayer in exactly TWO spots per session (owner order 14:4xZ via the Sensei 15:31Z, applied @ 9519087de; rule of record moral:faith §4.1): the very first tokens of the first reply and the very last tokens before rotate-self returns — NEVER at the start or end of a turn in between (a nudge, dm, notification or owner line opens with the work)** · **Sensei wake-audit cuts (10:39Z, gen IX→X OUT 6):** never re-stamp the header by hand (O1: no gen/loop narrative there — §3 carries the gen; rotate-self writes rotating-at) · never `git merge origin/season/s2` by hand ahead of `rotate-self --stops` (it merges the season branch itself, rotate.py:9215) · never arm an inbox/dm Monitor (nudges reach the pane; F14 re-word by the Sensei O2, unobjected) · write §3 as each harvest lands, never at rotation · **the last test result goes in `--stops` ONLY (or in the card row BEFORE the wait) — one of the two, never both** (O1 re-cut, Sensei 12:59Z: OUT 2 = row re-write + --stops carrying the same nbhd result).
## §3 🔴 STATE gen XIII (row generation 12; ref `da16f8db-6b39-4529-b413-41afdeb572b1` @325; the successor is row generation 13 = gen XIV and acks NOTHING) — stamp 14:03Z
| | |
|---|---|
| **wake** | **read nothing — STARTUP + this card are the whole state; first act = F5 harvest discovery.** After a `continue` wake: NO `rooms`, NO dm re-read — act on STARTUP's inbox print alone (W1, Sensei wake-audit 12:59Z on gen 11→12: WAKE 2 = rooms + read --dm, both orient; the one unread was the alert dm STARTUP already showed). Never head your own card (09:01Z cut). Out = `rotate-self --stops` ALONE — never hand-stamp the header (O1 live); write §3 as each harvest lands, not at rotation |
| seat | `seat/sensei-director@s2` = origin/season/s2 ca36c2008 (SL2#23 stamp) + SL7.64 harvest + the Sensei's two 15:56Z briefs; pushed; never rebased |
| landed this gen | **SL2#21 615ba5b48, SL2#22 0cd8c5c87, SL2#23 ca36c2008 — all LANDED + STAMPED** (SL2#23: GRANT 15:53Z, numbers line 16:0xZ; 4104/15 in 417 s — the tests leg creeps 343→391→417 s toward the 590 s ceiling, name it to the Prime if it passes 480). Nodes **2570 / 195 / 2765** (baseline for SL2#24; active never lower). 23 rounds harvested this gen (SL7.44-66 less none), SL7.40 demoted → fixed by SL7.54 (reachable) → SL7.72 makes it LIVE |
| digest | wf_438874da-7a6: **all ten residue rounds SL7.44-53 HARVESTED on the seat** (each 0.85-0.95; nbhds green; 12 kid nodes) = SL2#22 content, window asked 14:32Z. **mur-SL2.21 (wf_36280b2a-e4f, 14:13Z): SL7.40 DEMOTED** — unreachable live (heal's 2-arg _resolve_template call, TypeError swallowed, reach test stubbed); both kids re-verdicted inconclusive_lean_proved:40; fix node hypothesis:l4-run-after-join-reaches-the-successor-confirm-live (five lines incl. the SL7.46 per-process fetch-memo residue) = SL7.54. After it lands the Prime restarts the reaper unit and reads one after_join performed line |
| Prime | belam XVI [49ddab] @326. Restarts the reaper unit after SL2#23 (SL7.54) — its digest of SL2#23 (mur-SL2.23) brings residue lines to mint. SL2#24 window = ask 'window?' once SL7.67-72 are harvested |
| Sensei | master-sensei gen 4 [21497613] @327 (rotated 15:33Z). Owner orders relayed 15:31Z (prayer: two spots per session — applied to §2), 15:41Z (four code lines → SL7.67-70), 15:56Z (meter telemetry branch + after_join LIVE → SL7.71-72). Its next wake-audit of me checks WAKE 0 / OUT 1 |
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
| ~~SL7.54 · a00-a42ba1a5~~ **HARVESTED** (0.8 + lean:75; all five lines; nbhd 680/3/1x) | l4-run-after-join-reaches-the-successor-confirm-live (SL7.40 fix, heal.py + rotate.py) · g15.25 | test_after_join_service.py + rotate nbhd + test_heal.py | 14:32Z |
| ~~SL7.58 · a00-07a38103~~ **HARVESTED** (0.9 + lean:70) | one-resolved-generation (seating record + alert; 0 stays 0) · g15.25 | rotate nbhd | 15:29Z |
| ~~SL7.59 · a00-cfbba4e5~~ **HARVESTED** (proved 0.9) | first-seating tests stub the pushed-seats seam; None miss not pinned · g15.25 | rotate nbhd (fetch counter) | 15:29Z |
| ~~SL7.60 · a00-2fcf014d~~ **HARVESTED** (proved 0.95) | announce/record independent of --no-commit (_ack_stands) · g15.24 | ack nbhd | 15:29Z |
| ~~SL7.61 · a00-cccc0760~~ **HARVESTED** (proved 0.92) | scalar frontmatter path escapes NEL/LS/PS; fixpoint via read_frontmatter · g13.1 | test_node_writer + test_write | 15:29Z |
| ~~SL7.62 · a00-54da3e15~~ **HARVESTED** (proved 0.9) | _split_card_sections fence-run-aware · g15.25 | rotate nbhd | 15:29Z |
| ~~SL7.63 · a00-cc89de77~~ **HARVESTED** (proved 0.9) | keygen --all-live completes swaps when nothing keyed · g15.26 | send nbhd + test_rotate -k keygen | 15:29Z |
| ~~SL7.64 · a00-30e43aee~~ **HARVESTED** (proved 0.9) | level3 env refusal wording + subdir ascent vs docstring · g15 | test_level3 | 15:29Z |
| ~~SL7.65 · a00-f5d4d4aa~~ **HARVESTED** (proved 0.9) | NO_SPAWN branch reachable-or-deleted; recorder no pid 12345 · g15.25 | hook nbhd | 15:29Z |
| ~~SL7.66 · a00-c611a68b~~ **HARVESTED** (proved 0.92) | _merge_region keyless line in place; foreign-deleted before WORK-added · g15.24 | rotate nbhd | 15:29Z |
| ~~SL7.67 · a00-339d2ff2~~ **HARVESTED** (proved 0.97/0.92; notice DELETED not gated; five-reader guard; nbhd 101/3) | config:posts note silent (owner 15:4xZ (1)) · g15 | test_geometry_config + bin smoke | 15:48Z |
| ~~SL7.68 · a00-34c439ff~~ **HARVESTED** (proved 0.9; differential vs old script untested) | sensei.py calls <transcript> (owner (2)) · g15 | test_sensei (nbhd 361/3) | 15:48Z |
| ~~SL7.69 · a00-7561a748~~ **HARVESTED** (lean_disproved 60/70/75 = F13 is the ONE declared hand step; test-only; nbhd 174/3) | role-template hand-setup audit (owner (3)) · g15 | test_rotate_templates | 15:48Z |
| SL7.70 · a00-84f091be | one compact [meter] line on every prompt (owner 2nd order) · g15.25 | hook nbhd | 15:48Z |
| SL7.71 · a00-bbb6f27a | meter telemetry key resolves (measured or labelled est.; join-only if unknowable) — wake half · g15.25 | test_rotate_startup + bootstrap tests | 16:08Z |
| SL7.72 · a00-4125554d | after_join performed LIVE: heal watch when alive, rotate-self's own tail when no watcher; key never absent/{} (Sensei 91-record finding) · g15.25 | test_after_join_service + handover | 16:08Z |
| ~~SL7.55 · a00-8a1a7d46~~ **HARVESTED** (proved 0.82, F20 in config:rotations, nbhd 534/3) | l4-rotate-self-on-a-main-post-commits-its-own-record-and-sequence-json (P3) · g15.25 | rotate nbhd | 14:32Z |
| ~~SL7.56 · a00-1b5b13cb~~ **HARVESTED** (0.9 + lean:80, both dirs swept, nbhd 673/3/1x) | l4-rotate-self-sweeps-dead-hook-latches-before-spawning (P4) · g15.25 | rotate nbhd + hook nbhd | 14:32Z |
| ~~SL7.57 · a00-dd1471d8~~ **HARVESTED** (proved 0.92/0.93, ack nbhd 434/3) | l4-ack-continue-is-refused-on-an-ask-diff-path-with-the-exact-diff-line (P6) · g15.24 | rotate nbhd | 14:32Z |

### Queue — in this order
1. **Harvest SL7.67-72 as they land** (six rounds; owner orders 67-70 live since 15:44Z — 69's kid reported inconclusive_lean_disproved:70 on the template audit, read its reason before merging; 71-72 live since 16:08Z). Re-arm ONE Monitor on `spawn_budget.py status` for the six agent ids in the table (each leaving = harvest). F5 shape; rotate.py rounds by function, never rebase.
2. **SL2#24** = SL7.64 (harvested) + the two 15:56Z briefs + the six harvests: ask belam 'window?' (one line) → GO → re-sync origin/season/s2, push → MAIN merge --no-ff, render + --render --check, verify-suite (background, cwd=MAIN, log in scratchpad; watch the tests leg vs 590 s), grid.py commit --all, push season/s2 + refs/grid/*:refs/grid/*, verification.py --level rotation --stamp, ONE numbers line.
3. The Prime's next digest (mur-SL2.23) → mint one brief per residue line under the owning goal → dispatch; the Sensei's asks straight.

### 🔴 Where it stops — the next command (stamp 16:08Z)
```
gen XIII closed: SL2#21 615ba5b48 + SL2#22 0cd8c5c87 + SL2#23 ca36c2008 landed + stamped (last: 4104/15 in 417 s, nodes 2570/195/2765, baseline for SL2#24); 23 rounds harvested (SL7.44-66), SL7.40 demoted -> SL7.54 reachable -> SL7.72 (live performer) in flight; six rounds LIVE for you: SL7.67-72 (agents in the card table; 69 kid = lean_disproved:70, read why). Next: re-arm ONE Monitor on spawn_budget.py status for the six ids -> harvest each as it lands (F5 shape, rotate.py by function) -> ask belam XVI the SL2#24 window -> merge-up per queue 2 -> mint mur-SL2.23 residues. Last test result: SL2#23 suite 11/11 PASS, SL7.64 nbhd 117/3.
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
