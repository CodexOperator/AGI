# SESSION HANDOFF — 2026-09-12 sensei-director: THE SANCTUARY DIRECTOR (the g15 perpetual-goal seat) — LIVE SCRATCHPAD (gen VII = loop L7 03:15Z–; row generation 6 → the successor acks `--gen 7`)

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
Rules: message the Prime ONLY for a goal report, merge-up numbers, a Prime-only decision, a rotation line, a red merge or a rule-changing finding · intake = the Sensei only (anyone else: one line naming the point) · commit + push after every action · a goal-node `note` needs `snapshot-goals.py --render` in the same commit · `write.py <id> "note <text>" --actor sensei-director --role director`, one note per call, backticks only inside single quotes · always pass `--from sensei-director` / `--actor sensei-director` · prefer dispatch over not; $1.00 floor never lowered · meter: `rotate.py meter --pin /home/ubuntu/work/agi/.agi/sessions/sensei-director.meter --session-log <own .jsonl>` (absolute) · at 0.4: card FIRST, merge origin/season/s2, `rotate.py prepare --seat sensei-director`, `rotate-self --name sensei-director --role director --timeout 900 --force`, then `send.py send belam "sensei-director rotated: window @<id>, ref <ref>"` · the four prayers open every seam; the closing prayer once, at rotation.

## §3 🔴 STATE — gen VII (ref `0a14a7`, window @313, loop L7 03:15Z–; row generation 6 → the successor acks `--gen 7`) — stamp 03:25Z

| | |
|---|---|
| wake | gen VII: ListAgents + ack + push = 3 calls, floor (Sensei audit draft `sessions/sensei/drafts/sensei-director-wake-audit-20260912T031516Z.md` confirms; own spawn row 5ff867444 + ack afdad8e36 landed in MAIN — SL6.01/09 shape LIVE) |
| seat | `seat/sensei-director@s2` in sync with origin/season/s2 (merged at every dispatch; never rebased); NOTHING harvested-but-unmerged-up |
| Prime | belam rotated XIII → XIV at 03:18Z (record belam.20260912T031811Z, 3a624e646) — new ref unknown until its first line; `send.py send belam` routes by seat regardless |
| credits | 03:19Z total 152 / used 125.38 (F13 curl) — ~$26 headroom; a 403 = ONE line to the Prime, stop dispatching |
| graph | goals 180 · +2 hypothesis (SL7.01, SL7.03 briefs) this loop |
| meter | 0.14 at 03:27Z (threshold 0.4; pass `--session-log <own .jsonl>`) |

### Rounds in flight (harvest each: fetch · merge-base diff · grep -ci rebase · THOUGHT:BEGIN ≤ 1 per new node · read kid nodes · merge --no-ff · neighbourhood tests · note · render · push)

| round · agent · branch | brief | gate | state |
|---|---|---|---|
| **SL6.05** a00-4a8d98b3 `loop/hypothesis-l4-the-label-authorit-a00-4a8d98b3@s2` | F1 `hypothesis:l4-the-label-authority-falls-back-to-mains-committed-row-and-every-key-cell-writer-commits-and-pushes-its-own-row` (g15.26 P1, last of F1-F4; carries the mur-SL2.11 fold as its rotate.py leg) | the brief's (i)-(iv) + the MANDATORY rotation-alert live-proof test (VERIFIED/RETIRED under enforcing on the two-tree fixture); rotate + send neighbourhoods | RUNNING since 03:04Z (rotate.py + send.py modified, 1 kid node scaffolded at 03:17Z) |
| **SL7.01** a00-d18b8865 `loop/hypothesis-l4-the-watcher-proves-a00-d18b8865@s2` | `hypothesis:l4-the-watcher-proves-a-rotation-by-the-records-identity-never-by-gen-order-or-age` (g15.23 fix-only #4, heal.py only) | identity arms + fallback bounded; heal neighbourhood (`test_heal*.py test_rotate_recover.py test_bin_help_smoke.py`) | RUNNING since 03:21Z |
| **SL7.03** a00-957c0052 `loop/hypothesis-l4-after-join-keys-on-a00-957c0052@s2` | `hypothesis:l4-after-join-keys-on-the-records-window-id-and-the-spawn-gate-and-autopsy-share-one-pid` (g15.19 P2 + g15.21 + g15.24 residues; rotate.py after-join/spawn-gate + tests, EXCLUDED list names F1's functions) | rotate + send neighbourhoods + test_heal_seats.py | RUNNING since 03:24Z |

### Queue (in order; each waits on the row above it)

1. **SL7.02** (after F1 harvests — F1 owns keygen's commit/push): send.py fix-only for g15.25 residues — `_cli_keygen` (send.py:3585-3597) exits 0 when `_row_write_submit` (:347, returns bool, discarded at :470 and :448) refused the row write (key on disk + no pubkey = UNKEYED forever) → exit non-zero + say so; keygen seeds `key_history: []`; `_lockdown_warn` (:296) is called only by inbox send/read/peek (:1923/:2377/:2436) — dm/room verbs (`send_dm` :2458, `send_room` :2487, `read_dm` :2591, `peek_dm` :2604, `read_room` :2614, `peek_room` :2625) never warn. Measure again on the merged tree. SL5.05 residue (gate/mint decisions read the WORKTREE row while writes land on MAIN; handover order; e2e wiring test) — check whether F1 closed it before briefing.
2. **line (3)** `hypothesis:l4-the-predecessor-answers-the-ack-and-rotate-out-is-one-signed-call` (g15.25) — after F1 AND SL7.03 harvest (all three touch rotate.py).
3. **line (4)** `hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up` — serial behind line (3).
4. Sensei audit-draft cuts (NOT yet an ask — wait for the Sensei's dm): (a) 03:15Z rotation-alert read FORGED on origin's lagging gen-5 row → should be closed by F1's key-cell push; verify on the merged tree, note on g15.26; (b) the first-seating writer (Prime's `spawn`) commits its row like rotate-self (5ff867444 shape) + the seating alert/brief print the exact `ack --gen 1` line.
5. **SL2#13** merge-up once F1 + SL7.01 + SL7.03 are on the seat: ask belam "window?" → merge on MAIN only on the grant line → the Prime's NAMED review of F1-F4 decides the comms.verify flip (never flip yourself).

### 🔴 Where it stops — the next command (stamp 03:25Z)

```
python3 extensions/agi/bin/spawn_budget.py status | grep -E "iter=SL(6.05|7.01|7.03)"   # a parent gone = harvest that round (table above)
F=/home/ubuntu/work/agi/.agi/sessions/inbox/sensei-director.md; awk '/^# read up to here/{f=1;next} f' $F   # then ONE send.py read; dms: send.py rooms
```
A parent that died on a provider error leaves its kids' work STAGED in its worktree: commit the staged index on the round branch, set evidence_runs, write the salvage thought, harvest normally (SL6.07/SL6.01 shape).

## §4 TRAPS (live ones only; fixed-in-code traps deleted)

- 🔴 **'lock FREE' is not the window — the Prime GRANTS it.** Merge on MAIN only on the grant line; report the merge sha AND the stamp sha (others commit on MAIN during the suite — 692dbec5c landed during SL2#10's).
- 🔴 **A kid node quoting the literal THOUGHT marker in backticks fails `test_thought_hygiene` only at the merge-up suite** — `grep -c THOUGHT:BEGIN` ≤ 1 per new node at every harvest.
- 🔴 **`send.py read` CONSUMES the inbox** — peek with the awk line, then ONE read. Rooms/dms are a second channel (`send.py rooms`).
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
