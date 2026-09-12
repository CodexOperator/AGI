# SESSION HANDOFF — 2026-09-12 sensei-director: THE SANCTUARY DIRECTOR (the g15 perpetual-goal seat) — LIVE SCRATCHPAD (gen VIII = loop L8 04:55Z–, row generation 7; wake was ZERO calls under SL7.06's default)

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

## §3 🔴 STATE — gen VIII (ref `013f1fb9-e3e4-4957-9ee5-e5637a5ec642`, window @316, pid 1353686, loop L8 from 04:55Z; row generation 7, session_ref empty by design) — stamp 05:25Z

| | |
|---|---|
| seat | `seat/sensei-director@s2` = origin/season/s2 (42ce34503) + the g15 landed note + the read-guard brief (never rebased). Nothing harvested-but-unmerged. |
| SL2#14 | **LANDED 05:21Z** merge 42ce34503 = stamp; ALL 11 GREEN suite passed=3782 skipped=15 + ONE declared strict-xfail (test_send.py::test_keygen_commits_and_pushes_own_row_to_bare_remote — SL7.09 owns it; REMOVE the mark when it lands); **2396 / 195 / 2591** (baseline 2373/195/2568); grid 24 versions; pushed. Seven rounds: SL7.02/04/05/06/08/10/11. Numbers line sent 05:24Z; Prime owes mur-SL2.14 by name |
| wake | gen VIII: 0 calls (SL7.06 default answered continue — first live proof). Owner order 03:3xZ: wake 0 / out 1 → line (3) = SL7.12 (brief narrowed, queued behind SL7.09), line (4) after it |
| Prime | belam XIV [92eda4] @314. Owes: mur-SL2.14 by name; reaper restart once after merge-up 44 |
| Sensei | master-sensei gen 2 [f5de36] @309. Asks: A built + landed (SL7.04) · owner order built + landed (SL7.06; Sensei ruled 05:05Z KEEP the ack template entry) · B = SL7.07 (running) · C built + landed (SL7.02). Told 05:06Z: rotate-self ack prose already conditional on the seat; the `loop` twin writes no pending ack so its prose is right for its path |
| credits | 05:07Z 152 / 128.43 used → **$23.57 left**; ~$0.3-0.5 per round; a 403 = ONE line to the Prime, stop. Floor $1.00 |
| trap paid | gen VIII call 4: `send.py read <seat>` (positional) READS THAT SEAT'S INBOX and marks it read — I consumed belam's inbox; dms are `send.py read --dm <seat> --from sensei-director`. Corrected to the Prime 04:58Z; Prime ACCEPTED a g15 line → minted `hypothesis:l4-send-py-read-refuses-a-target-that-is-not-the-resolved-sender-and-peek-stays-open` (SL7.13, after SL7.09/07 harvest) |

### Rounds in flight (harvest each: fetch · merge-base diff · grep -ci rebase · THOUGHT:BEGIN ≤ 1 per new node · read kid nodes · merge --no-ff · neighbourhood tests · note · render · push)

| round · agent · branch | brief | gate · tests | since |
|---|---|---|---|
| **SL7.09** a00-8f0f4ffa `season2/loops/hypothesis-l4-the-successor-key--a00-8f0f4ffa` (kid a00-89d49b37 live) | `hypothesis:l4-the-successor-key-swap-waits-for-the-push-and-a-recovery-record-still-yields-the-join` (g15.26 flip gate (2)(6) + mur-SL2.12 (3) + the edited_by xfail) | MANDATORY two-tree alert fixture VERIFIED never FORGED; xfail flips → remove the strict mark in test_send.py · rotate + send | 04:54Z |
| **SL7.07** a00-a457c3fe `season2/loops/hypothesis-l4-the-spawn-gate-ref-a00-a457c3fe` (kid a00-7d33638d live) | `hypothesis:l4-the-spawn-gate-refuses-both-directions-and-a-hand-seating-commits-its-row-and-answers-the-ack` (Sensei B + flip gate (5)) | both-direction gate fixtures; hand seating leaves MAIN clean, post wakes at 0 · rotate | 04:54Z |

Harvested this gen and LANDED at SL2#14: SL7.08 · SL7.10 · SL7.11 (with the four from gen VII). Round branches now spell `season2/loops/<slug>-<agent>` (L4.305); `git branch --format='%(refname:short)' | grep <agent>` finds either grammar; a `+` prefix in plain `git branch` = checked out in the round's worktree.

### Queue — dispatch in this order, each behind the round that owns its file

1. **SL2#15** when SL7.09 + SL7.07 are harvested: ask belam "window?" → merge on MAIN only on the GO line → render + --render --check → `commands.py run verify-suite` (BACKGROUND it — 5-6 min; read the task output) → grid commit → push season/s2 + refs/grid → `verification.py --level rotation --stamp` → ONE line: 5 numbers **including suite passed/skipped and any named xfail**, merge sha, stamp sha, one line per goal. Baseline now 2396/195/2591, active never lower.
2. **line (3)** NARROWED 05:01Z (bf58b538a) — `hypothesis:l4-the-predecessor-answers-the-ack-and-rotate-out-is-one-signed-call` (rotate-self --stops = one-call rotate-out) — dispatch as SL7.12 AFTER SL7.09 harvests (rotate.py owner); SL7.07 EXCLUDED by name in the brief.
3. **SL7.13** read-guard `hypothesis:l4-send-py-read-refuses-a-target-that-is-not-the-resolved-sender-and-peek-stays-open` (send.py read dispatch only) — after SL7.09 harvests (it touches test_send.py); can run beside SL7.12 (rotate.py) — file-disjoint.
4. **line (4)** `hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up` — re-read against SL7.06 + line (3) before dispatch; after line (3).
5. **Dispatch line:** `python3 extensions/agi/bin/dispatch.py . SL7.<nn> --target <id> --level small --tier parent --harness pi --branch` (commit + push first; exit 3 stale-base = merge origin/season/s2, push, re-run).

### 🔴 Where it stops — the next command (stamp 04:54Z)

```
python3 extensions/agi/bin/spawn_budget.py status | grep -E "tier=parent iter=SL7"   # a parent gone = harvest that round (table above)
F=/home/ubuntu/work/agi/.agi/sessions/inbox/sensei-director.md; awk '/^# read up to here/{f=1;next} f' $F   # then ONE send.py read; dms: send.py rooms
```
A parent that died on a provider error leaves its kids' work STAGED in its worktree: commit the staged index on the round branch, set evidence_runs, write the salvage thought, harvest normally (SL6.07/SL6.01 shape). Kid-verdict dms nudge you every few minutes — peek with the awk line, consume with ONE read, never act on them.

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
