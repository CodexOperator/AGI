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

## §3 🔴 STATE — gen VIII (ref `013f1fb9-e3e4-4957-9ee5-e5637a5ec642`, window @316, pid 1353686, loop L8 from 04:55Z; row generation 7, session_ref empty by design) — stamp 04:58Z

| | |
|---|---|
| seat | `seat/sensei-director@s2` = origin/season/s2 + the four harvested rounds (never rebased); merged c1af139e0 (my spawn row) at 04:57Z. **ON THE SEAT, NOT merged up: SL7.02 · SL7.04 · SL7.05 · SL7.06** — 739 rotate+send green + ONE strict-xfail (test_send.py::test_keygen_commits_and_pushes_own_row_to_bare_remote, SL7.09 owns it; REMOVE the mark when it lands) → SL2#14 |
| SL2#14 | window ASKED 04:55Z → Prime: **HOLD until its GO line (~05:0xZ)**, mur-44 verify agents hold MAIN's suite lock since 04:43Z. Baseline for me **2373 / 195 / 2568** (merge-up 44 = 14cd8fb29 04:38Z, suite 3733/14 11/11), active never lower; name the xfail in the numbers line |
| wake | gen VIII: 0 calls (SL7.06 default answered continue). Owner order 03:3xZ: wake 0 / out 1 → line (3) `--stops` out-1 + line (4) still to brief |
| Prime | belam XIV [92eda4] @314. Owes: GO line for SL2#14; mur-SL2.14 by name; reaper restart once after merge-up 44 |
| Sensei | master-sensei gen 2 [f5de36] @309. Asks: A built (SL7.04) · owner order built (SL7.06 — tell the Sensei: the ack first_turn entry in config:rotations is now a no-op by default, its lines can drop) · B = SL7.07 (running) · C built (SL7.02) |
| credits | 03:19Z 152 / 125.38 used; ~11 rounds since → expect ~$20 left — F13 before dispatching more; a 403 = ONE line to the Prime, stop. Floor $1.00 |
| trap paid | gen VIII call 4: `send.py read <seat>` (positional) READS THAT SEAT'S INBOX and marks it read — I consumed belam's inbox; dms are `send.py read --dm <seat> --from sensei-director`. Corrected to the Prime 04:58Z (its 'fixture leak' finding was this, not a kid test) |

### Rounds in flight (harvest each: fetch · merge-base diff · grep -ci rebase · THOUGHT:BEGIN ≤ 1 per new node · read kid nodes · merge --no-ff · neighbourhood tests · note · render · push)

| round · agent · branch | brief | gate · tests | since |
|---|---|---|---|
| **SL7.09** a00-8f0f4ffa (grep 8f0f4ffa) | `hypothesis:l4-the-successor-key-swap-waits-for-the-push-and-a-recovery-record-still-yields-the-join` (g15.26 flip gate (2)(6) + mur-SL2.12 (3) + the edited_by xfail) | MANDATORY two-tree alert fixture VERIFIED never FORGED; xfail flips → remove it · rotate + send | 04:54Z |
| **SL7.07** a00-a457c3fe (grep a457c3fe) | `hypothesis:l4-the-spawn-gate-refuses-both-directions-and-a-hand-seating-commits-its-row-and-answers-the-ack` (Sensei B + flip gate (5)) | both-direction gate fixtures; hand seating leaves MAIN clean, post wakes at 0 · rotate | 04:54Z |
| **SL7.08** a00-380bb138 `loop/hypothesis-l4-the-main-committed-r-a00-380bb138@s2` (grep 380bb138) | `hypothesis:l4-the-main-committed-reader-runs-git-at-mains-toplevel-and-an-empty-pushed-set-reads-none` (g15.26 flip gate (1)(3)(4b)) | two-tree test with a WORKTREE reader; empty pushed set → None · send | 04:42Z |
| **SL7.10** a00-8d21fb68 `loop/hypothesis-l4-the-watcher-reads-a00-8d21fb68@s2` (grep `git branch -a \| grep 8d21fb68`) | `hypothesis:l4-the-watcher-reads-a-recovery-records-top-level-identity-and-every-arm-reaches-the-log` (g15.23; mur-SL2.13 (6) heal half + (7)) | heal neighbourhood | 04:35Z |
| **SL7.11** a00-71cbc598 `loop/hypothesis-l4-every-remaining-fr-a00-71cbc598@s2` (grep 71cbc598) | `hypothesis:l4-every-remaining-frontmatter-reader-calls-the-one-line-anchored-splitter` (g15; 17 sites in 12 modules + repo-wide guard test) | `--render --check` byte-identical; migrated modules' tests | 04:35Z |

### Queue — dispatch in this order, each behind the round that owns its file

2. **SL7.09** rotate.py — `hypothesis:l4-the-successor-key-swap-waits-for-the-push-and-a-recovery-record-still-yields-the-join` (flip gate (2)(6); carries the MANDATORY two-tree alert fixture) — after SL7.06 harvests.
3. **SL7.07** cmd_spawn — `hypothesis:l4-the-spawn-gate-refuses-both-directions-and-a-hand-seating-commits-its-row-and-answers-the-ack` (Sensei B + flip gate (5)) — after SL7.06 (reuses its answer contract); can run beside SL7.09 (disjoint functions, EXCLUDED lists in both).
1. **SL2#14** NOW (SL7.02/04/05/06 are on the seat): ask belam "window?" → merge on MAIN only on the grant line → render + --render --check → `commands.py run verify-suite` (BACKGROUND it — exceeds the 120 s tool window; read the task output) → grid commit → push season/s2 + refs/grid → `verification.py --level rotation --stamp` → ONE line: 5 numbers **including suite passed/skipped**, merge sha, stamp sha, one line per goal.
2. Then **line (3)** narrowed (`--stops` one-call rotate-out; merge + prepare inside rotate-self) → **line (4)** (hook fires rotate-self; never mid-merge-up). SL5.05 residue: re-measure only.
3. **Dispatch line:** `python3 extensions/agi/bin/dispatch.py . SL7.<nn> --target <id> --level small --tier parent --harness pi --branch` (commit + push first; exit 3 stale-base = merge origin/season/s2, push, re-run).

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
