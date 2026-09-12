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

## §3 🔴 STATE — gen VII (ref `0a14a7`, window @313, loop L7 03:15Z–; row generation 6 → the successor acks `--gen 7` — OR, once SL7.06 lands, nothing: the predecessor answers) — stamp 04:17Z

| | |
|---|---|
| wake | gen VII: 3 calls, floor (Sensei audit). Owner order 03:3xZ (rule-changing): **wake 0 / out 1 for every post** — my g15 lines: SL7.06 (ack answered by the predecessor) → line (3) narrowed to `--stops` rotate-out → line (4) hook-driven |
| seat | `seat/sensei-director@s2` in sync with origin/season/s2 at e1f6acafc (never rebased); NOTHING harvested-but-unmerged-up |
| merge-ups this loop | **SL2#13 LANDED 04:08Z** e1f6acafc (F1 SL6.05 + SL7.01 + SL7.03; ALL 11 GREEN 3659/14, **2358/195/2553**, stamp e1f6acafc, grid via cron). F1-F4 all on MAIN → the flip waits on mur-SL2.13 by name |
| Prime | belam XIV [92eda4] @314 since 03:18Z. mur-SL2.12 (03:37Z): SL6.06/08/09 ACCEPT 3/3 with residue, six lines routed (see queue); **flip HELD on F1 → SL2#13 → mur-SL2.13** |
| Sensei | master-sensei gen 2 [f5de36] @309. Asks A (EOF newline) → SL7.04 live · B (first-seating writer commits its row + exact `ack --gen 1` line) queued · C (FORGED at the seam → UNVERIFIABLE) folds into the send.py round |
| credits | 03:19Z total 152 / used 125.38 → 26.5 left; Prime saw 26.53 at 03:25Z. Five parents live = ~$2-3. A 403 = ONE line to the Prime, stop dispatching. Floor $1.00 |
| meter | ~0.30 at 04:17Z (threshold 0.4; pass `--session-log <own .jsonl>`) |

### Rounds in flight (harvest each: fetch · merge-base diff · grep -ci rebase · THOUGHT:BEGIN ≤ 1 per new node · read kid nodes · merge --no-ff · neighbourhood tests · note · render · push)

Landed at SL2#13: F1 · SL7.01 · SL7.03. HARVESTED on the seat, not merged up: **SL7.04** (g15.25 ask A, 991 green). Still running (harvest → SL2#14):

| round · agent · branch | brief | gate · tests | since |
|---|---|---|---|
| **SL7.05** a00-36201455 `loop/hypothesis-l4-one-line-anchored--a00-36201455@s2` | `hypothesis:l4-one-line-anchored-frontmatter-reader-and-the-suite-runner-refuses-a-held-lock-before-spawning` (g15, Prime (4)+(5)) | 17 sites migrated, byte-identical reads; held lock = one refusal line · metrics/evidence_gate/spawn_gate/completion/cli/stitch/verification tests | 03:40Z |
| **SL7.06** a00-d60a3c54 `loop/hypothesis-l4-the-predecessor-an-a00-d60a3c54@s2` | `hypothesis:l4-the-predecessor-answers-continue-by-default-and-ask-diff-hands-the-successor-exactly-one-call` (g15.25, **OWNER ORDER** wake 0; folds Prime (3) + F1's carried fold (ii)(iii)) | default rotation = record success with ZERO successor calls on the fake tmux; --ask-diff prints the one line; own-row-only spawn commit · rotate + send | 03:49Z |
| **SL7.02** a00-439a2564 `loop/hypothesis-l4-keygen-exits-on-a--a00-439a2564@s2` | `hypothesis:l4-keygen-exits-on-a-refused-row-every-comms-verb-warns-under-lockdown-and-a-lagging-origin-row-never-reads-forged` (g15.25/g15.26; Sensei C + Prime (1)(2)) | seam fixture (origin key A, MAIN key B gen+1 → VERIFIED main-committed; gitless → UNVERIFIABLE); boundary pin; keygen exit · send | 03:50Z |

### Queue (in order)

1. **SL2#14** once SL7.04/05/06/02 are harvested on the seat: ask belam "window?" → merge on MAIN only on the grant line → render + --render --check → `commands.py run verify-suite` (background it: it exceeds the 120 s tool window — read the task output file) → grid commit → push season/s2 + refs/grid → `verification.py --level rotation --stamp` → ONE line (5 numbers + merge sha + stamp sha + one line per goal). mur-SL2.13 by name decides the flip (never flip yourself).
2. **SL7.07** (SL7.03 landed): Sensei B — `cmd_spawn` first-seating writer commits its row (5ff867444 shape; SL7.06 makes the default answer continue, so the seating alert/brief prints no ack line unless --ask-diff) — check SL7.06's clause (4) first: it may already cover the first seating.
3. **line (3)** narrowed (`--stops` one-call rotate-out; merge + prepare inside rotate-self) after SL7.06 → **line (4)** (hook fires rotate-self; never mid-merge-up). SL5.05 residue (mint decisions read the worktree row): `_geometry_resolution_root` already picks the integration tree when the worktree's geometry is behind — re-measure, brief only if still open.
4. When SL7.02 reports the exact lines: rewrite the F2 hypothesis title + g15.26 wording (`never` → `unless the next two lines are a ts:/from: header`).

### 🔴 Where it stops — the next command (stamp 04:17Z)

```
python3 extensions/agi/bin/spawn_budget.py status | grep -E "tier=parent iter=SL(6.05|7)"   # a parent gone = harvest that round (table above); all four → SL2#14
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
