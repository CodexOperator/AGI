# SESSION HANDOFF — 2026-09-11 sensei-director: THE SANCTUARY DIRECTOR (the g15 perpetual-goal seat) — LIVE SCRATCHPAD (gen V = loop L5 21:35Z–~00:0xZ; gen VI = loop L6 starts at §3; row generation 4 → the successor acks `--gen 5`; stamp 22:22Z)

## §0 WHO YOU ARE (identity is SUPPLIED, never claimed)

Seat `sensei-director` in `config:seats` — the Sanctuary director: the director-kid that watches `goal:g15` and takes the Sensei's asks straight (founding order: owner 15:5xZ, verbatim at `doc:l4-owner-decisions` line 9; its two rules — no loop docs, one loop per generation — same node). Address = your ListAgents ref; window `sensei-director` in tmux; worktree `.agi/worktrees/seat-sensei-director`, branch `seat/sensei-director@s2`; Prime = `belam` (`send.py send belam "<one line>" --from sensei-director`); Sensei = `master-sensei` (rotated 22:5xZ to gen 2 [f5de36] @309 — same seat name); point director = `sanctuary-director` (runs the L4 queue; you do not). Owner quotes live in nodes, never here.

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
Rules: message the Prime ONLY for a goal report, merge-up numbers, a Prime-only decision, a rotation line, a red merge or a rule-changing finding · intake = the Sensei only (anyone else: one line naming the point) · commit + push after every action · a goal-node `note` needs `snapshot-goals.py --render` in the same commit · `write.py <id> "note <text>" --actor sensei-director --role director`, one note per call, backticks only inside single quotes · always pass `--from sensei-director` / `--actor sensei-director` · prefer dispatch over not; $1.00 floor never lowered · meter: `rotate.py meter --pin /home/ubuntu/work/agi/.agi/sessions/sensei-director.meter --session-log <own .jsonl>` (absolute) · at 0.4: card FIRST, merge origin/season/s2, `rotate.py prepare --seat sensei-director`, `rotate-self --name sensei-director --role director --timeout 900 --force`, then `send.py send belam "sensei-director rotated: window @<id>, ref <ref>"` · the four prayers open every seam; the closing prayer once, at rotation.

## §3 🔴 STATE at rotation V → VI (gen V ref `588897`, window @306, loop L5 21:35Z–23:50Z; row generation 4 → the successor acks `--gen 5`)

| | |
|---|---|
| seat | `seat/sensei-director@s2` at the card commit; origin/season/s2 merged (never rebase) |
| merge-ups this loop | **SL2#6** 0ca5a801b (line (1) + spawn-row commit) · **SL2#7** 342285b13 (mur-39 FIX + lockdown reserved; run 2 green) · **SL2#8** 71353b13d + fix-up 924e03bed (FLIP code + line (2); run 2 ALL 11 GREEN 3563/14, **2310/195/2505**, stamp 924e03bed) · **SL2#9** = SL5.07 + SL5.08, window ASKED 23:50Z — if the grant arrives before my rotate-self, I land it (§1 shape); if not, gen VI asks again with the seat tip |
| graph | goals **180** (g15.26 minted; seeds set on g15.21-26) · 0 broken links · GOALS.md byte-identical · +14 experiment nodes landed on the seat this loop |
| spend | deepseek rounds ~$0.5-1 each; 9 rounds cut this loop; floor $1.00 never lowered |
| wake | `## STARTUP OUTPUT` → ONE act: `rotate.py ack --seat sensei-director --gen 5 --ref <bare ListAgents ref> continue` (SL5.01 pre-commits the spawn row; the ack commits its back-fill and prints the push line — run it), then one line to the Prime (belam XII [fda770] @305 at 23:50Z, at 0.43 — may have rotated; `send.py whois <ref> --claim belam`) |
| disclosure | at SL2#8 I amended my own seat-branch fix-up with `--force-with-lease` (my branch only) — against §2's letter; reported to the Prime; do not repeat |

### Open asks (Sensei/owner/Prime → this seat): goal · brief · round · state

| ask | goal | brief | round · agent | state |
|---|---|---|---|---|
| LANDED on season/s2 this loop | g15.25 line (1) SL4.06 + mur-39 FIX SL5.02 + lockdown SL5.03 + line (2) SL5.05 · g15.24 fix (a) SL5.01 · g15.26 FLIP code SL5.04 | — | — | SL2#6/7/8 |
| ON THE SEAT, in SL2#9 | g15.21 (SL5.07) · g15.24 + g15.23/g15.13 P2 (SL5.08) | — | — | window asked; land or hand over |
| Prime mur-SL2.3-5 P1+P2 for g15.14 (prepare same-ref merge + guard first + unregistered --name + check-5 transcript; real merge-gate test; _background_tasks path) | `goal:g15.14` | `hypothesis:l4-prepare-measures-and-merges-the-same-ref-guard-first-and-check-5-prefers-the-rows-transcript` | **SL5.06** a00-4f25c9b5 · branch `loop/hypothesis-l4-prepare-measures-*-a00-4f25c9b5@s2` (slug prefix is TRUNCATED at a fixed width — `git branch \| grep 4f25c9b5`) | RUNNING at the close: 3 kids proved (a00-05237869, a00-9eb242ce, a00-4756043d), parent closing. **Gen VI harvests**: rotate neighbourhood; expect a both-modified seam in `_prepare_checks` / `cmd_prepare` only if the point moved them |
| Sensei alert-path line: rotation-alert into the INBOX, coalesced nudge still wakes, detected records dedupe | `goal:g15.23` fix-only #2 | `hypothesis:l4-a-rotation-alert-lands-in-the-inbox-a-coalesced-nudge-still-wakes-and-detected-records-dedupe` | **SL5.09** a00-232c7d9a · `loop/hypothesis-l4-a-rotation-alert-*-a00-232c7d9a@s2` | RUNNING at the close: 2 kids proved (a00-ec19c056, a00-eea2fd59 lean:60), kid 3 a00-44abc6a6 live. **Gen VI harvests**: hook + send neighbourhoods (rotate.py `_announce_rotation`, send.py `_nudge_window`) |
| g15.26 VALUE flip (comms.verify → enforcing in .agi/config.json) | `goal:g15.26` | — | — | the Prime's one-line edit after mur-SL2.8 names SL5.04; caveat on the goal note (repeated peek re-appends the same FORGED bytes — dedupe by (ts, from, sig) is the fix-only if asked) |
| g15.25 lines (3) (4) | `goal:g15.25` | `hypothesis:l4-the-predecessor-answers-the-ack-and-rotate-out-is-one-signed-call` · `hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up` | → SL6.01 / SL6.02 | briefed in L4, not cut (owner: wrap up) — gen VI cuts them serially after SL5.06/09 land, adding a cut note like SL5.05's (reuse writers, grep by name) |
| mur-SL2.3-5 P3 (next season) | g15.13 wake-window rule · g15.17 re-spawn gen record · g15.18 `main` reason · g15.22 fence-aware wrap | — | — | the Prime's dm 22:44Z has the text; not this loop |
| Prime owes | mur-SL2.6/7/8 reviews by name (SL5.01-05) | — | — | findings → fix-only briefs, measured on the merge-up commit it names |

### 🔴 Where it stops — the next command (stamp 23:50Z)

```
git log --oneline -1 origin/season/s2; git log --oneline -1 seat/sensei-director@s2   # is SL2#9 (SL5.07 + SL5.08) on season/s2? if the seat is ahead in extensions/agi/bin/rotate.py, ask `window?` and land it first (§1 shape)
python3 extensions/agi/bin/spawn_budget.py status | grep -E "iter=SL5.0[69]"   # a parent gone = harvest (SL5.06 a00-4f25c9b5 rotate prepare; SL5.09 a00-232c7d9a alerts)
F=/home/ubuntu/work/agi/.agi/sessions/inbox/sensei-director.md; awk '/^# read up to here/{f=1;next} f' $F   # then ONE send.py read
```
Then merge-up SL2#10 with SL5.06 + SL5.09 → numbers to the Prime → cut lines (3)(4) → card → rotate at 0.4.

## §4 TRAPS (live ones only; fixed-in-code traps deleted)

- 🔴 **'lock FREE' is not the window — the Prime GRANTS it.** Merge on MAIN only on the grant line; once merged, MAIN's HEAD is under the Prime's next push whether or not your suite ran.
- 🔴 **A kid node quoting the literal THOUGHT marker in backticks fails `test_thought_hygiene` only at the merge-up suite** — `grep -c THOUGHT:BEGIN` ≤ 1 per new node at every harvest; reword, never delete.
- 🔴 **`send.py read` CONSUMES the inbox** — peek with the awk line, then ONE read; a Monitor may only count `^from:` lines. Room/dm unread (`send.py rooms`) are a second channel: `send.py peek --dm <seat> --from sensei-director`; rotation-alerts there are machine text.
- 🔴 **seats.md conflicts at every sync on the OTHER rows** — `git checkout --theirs -- .agi/nodes/.geometry/seats.md`, then assert your own row is byte-identical to HEAD's before committing.
- 🔴 **NEVER stamp a time by feel** — `date -u` in the same command.
- 🔴 **`write.py create goal` scaffolds no tags and no `BODY:END`** — write the body after BEGIN to EOF, add the tag block (`goal, subgoal, l4, sensei-director`); a subgoal's parents must be `build`/`goal` only (the hypothesis edge goes into `## Why this exists`).
- **Others commit on MAIN during your suite** — the stamp lands on their tip; report the merge sha AND the stamp sha.
- **The Prime's line numbers are measured on the merge-up commit it reviews** — `git show <sha>:<file> | sed -n` before trusting a `:NNN`.
- **A deepseek parent reads 'ONE registry' as 'one plug point'** — when an order is about module identity, say `is` in the brief (`seatsig.SCHEMES is src.seatsig.SCHEMES`) and name both spellings.
- **Two rounds on the same file at once** — brief each with an explicit EXCLUDED list naming the other's functions; harvest seams then stay disjoint. Seams with the POINT's rounds still happen (L4.291 `_write_identity_cells`, `id_root`): union by hand, name the seam in the merge message, re-run both neighbourhoods.
- **A test that lands from merge-up N monkeypatches a signature your round changed** (SL2#8: `_print_blocks_with_labels` gained `me`) — fix the fake's arity, never the assertion.
- **The round branch name truncates the slug at a fixed width** — `git branch | grep <agent>` before naming it.
- **A stale `index.lock` in the seat worktree** appears while another writer touches the shared `.git` — wait 3 s and retry, never delete it blind.
- **The 18 s test** `test_rotate_selfreap.py::test_reap_belam_oldest_pane_seam_detached_tree` is pre-existing, not a fixture sleep from a round.
- Parents run deepseek-v4.1-flash, ~10-30 min per round; `heal.py`'s `reason=overdue` dm is informational — keep polling, never replace.
- `rotate-self` refuses through `prepare`'s captives: commit + push + merge origin/season/s2; write the card LAST.
