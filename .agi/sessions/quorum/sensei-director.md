# SESSION HANDOFF — 2026-09-11 sensei-director: THE SANCTUARY DIRECTOR (the g15 perpetual-goal seat) — LIVE SCRATCHPAD (gen VI = loop L6 00:04Z–; row generation 5 → the successor acks `--gen 6`; stamp 00:3xZ)

## §0 WHO YOU ARE (identity is SUPPLIED, never claimed)

Seat `sensei-director` in `config:seats` — the Sanctuary director: the director-kid that watches `goal:g15` and takes the Sensei's asks straight (founding order: owner 15:5xZ, verbatim at `doc:l4-owner-decisions` line 9; its two rules — no loop docs, one loop per generation — same node). Address = your ListAgents ref; window `sensei-director` in tmux; worktree `.agi/worktrees/seat-sensei-director`, branch `seat/sensei-director@s2`; Prime = `belam` — XIII [ff648e] @311 since 00:07Z (`send.py send belam "<one line>" --from sensei-director`); Sensei = `master-sensei` gen 2 [f5de36] @309; point director = `sanctuary-director` (runs the L4 queue; you do not). Owner quotes live in nodes, never here.

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

## §3 🔴 STATE — gen VI (ref `fd9e5d`, window @310, loop L6 from 00:04Z; row generation 5 → the successor acks `--gen 6`)

| | |
|---|---|
| seat | `seat/sensei-director@s2` — in sync with origin/season/s2 at 692dbec5c (merged, never rebased); pushed |
| merge-ups this loop | **SL2#10 LANDED 00:28Z** 6e484c126 (SL5.06 g15.14 prepare P1+P2 · SL5.09 g15.23 alert path #2), ALL 11 GREEN 3590/14, **2322/195/2517**, stamp on the Prime's 692dbec5c; Prime-verified PASS 10/10 on b6f93d971, floor raised; MAIN's sensei-director row now carries pubkey b3a8e407 |
| wake | 17 calls (floor 4): the ack refused twice on MAIN's dirty seats.md — the hunk was my OWN spawn row (L4.291 writes MAIN, SL5.01 commits the worktree copy) → SL6.01 fixes the source |
| graph | goals **180** · 0 broken links · GOALS.md byte-identical · +6 experiment +3 hypothesis this loop |
| spend | 3 deepseek rounds cut 00:30Z (~$0.5-1 each); floor $1.00 never lowered |
| meter | 0.18 at 00:31Z (`rotate.py meter --pin /home/ubuntu/work/agi/.agi/sessions/sensei-director.meter --session-log ~/.claude/projects/-home-ubuntu-work-agi--agi-worktrees-seat-sensei-director/337a6ec8-97e4-400e-ab03-e425633dd553.jsonl` — the pin alone errs) |

### Open asks: goal · brief · round · state

| ask | goal | brief | round · agent | state |
|---|---|---|---|---|
| Sensei wake-audit 00:08Z/00:10Z (source → belt → small) + Prime XIII (a) pubkey rides the ONE writer | `goal:g15.24` fix-only (b) | `hypothesis:l4-the-spawn-row-write-and-its-commit-land-in-one-tree-and-the-ack-stages-only-its-own-row` | **SL6.01** a00-5010cd64 · `loop/hypothesis-l4-the-spawn-row-writ-a00-5010cd64@s2` | RUNNING 00:30Z — rotate.py only; harvest = rotate neighbourhood; expect a seam with SL6.02 in NO file |
| Sensei side finding: reaper wrote `detected` for gen 4 after the success record | `goal:g15.23` fix-only #3 | `hypothesis:l4-the-watcher-reads-mains-row-and-the-latest-rotation-record-before-declaring-a-crash` | **SL6.02** a00-fcdbdec1 · `loop/hypothesis-l4-the-watcher-reads--a00-fcdbdec1@s2` | RUNNING 00:30Z — heal.py only; harvest = hook + send + heal (test_heal_watch `_rot_shim` may need attrs the seat's heal.py reads — fix the fake) |
| Prime XIII (b): sig against an unkeyed row reads UNKEYED, never FORGED | `goal:g15.26` gate | `hypothesis:l4-a-sig-against-a-row-with-no-key-on-file-reads-unkeyed-never-forged` | **SL6.03** a00-fd7ca60b · `loop/hypothesis-l4-a-sig-against-a-ro-a00-fd7ca60b@s2` | HARVESTED 00:45Z on the seat (353 green, 1 kid proved) — lands at SL2#11. RULING: comms.verify stays informational until (a)+(b) land AND a mur-SL2.x reviews them by name — never flip |
| Prime XIII 00:33Z P2: cmd_spawn --seat ignores the row's model/effort/settings (owner: 'No surprise fable please.') | `goal:g15.15` | `hypothesis:l4-cmd-spawn-with-a-seat-takes-the-rows-model-effort-and-settings-never-the-tier-default` | SL6.04 WITHDRAWN | LANDED by the Prime at 6463e6aef (owner's order); record `experiment:l4-record-cmd-spawn-seat-row-is-the-model-source-landed-by-the-prime-at-6463e6aef` proved |
| g15.19 P2 (recorded, not cut): run_after_join_for_seat feeds an empty succ_transcript/succ_ref — key on the record's window_id | `goal:g15.19` | — | — | brief after the P1 rounds land |
| g15.25 lines (3) (4) | `goal:g15.25` | `hypothesis:l4-the-predecessor-answers-the-ack-and-rotate-out-is-one-signed-call` · `hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up` | → SL6.04 / SL6.05 | queued behind SL6.01-03 (line (3) touches the ack path SL6.01 owns — cut only after SL6.01 lands) |
| Prime owes | mur-SL2.6-10 reviews by name (SL5.01-09) | — | — | findings → fix-only briefs, measured on the merge-up commit it names |

### 🔴 Where it stops — the next command (stamp 00:31Z)

```
python3 extensions/agi/bin/spawn_budget.py status | grep -E "iter=SL6.0[123]"   # a parent gone = harvest (SL6.01 rotate.py · SL6.02 heal.py · SL6.03 send.py)
F=/home/ubuntu/work/agi/.agi/sessions/inbox/sensei-director.md; awk '/^# read up to here/{f=1;next} f' $F   # then ONE send.py read
```
Then harvest each landed round (§1 shape), merge origin/season/s2 first, ask belam "window?" for SL2#11 → cut lines (3)(4) → card → rotate at 0.4.

## §4 TRAPS (live ones only; fixed-in-code traps deleted)

- 🔴 **The ack's dirty gate reads MAIN's seats.md, not the worktree's** (`_shared_graph_root`, L4.291) — `git status` in the seat says clean while the ack refuses. Until SL6.01 lands: a worktree post's own spawn row sits uncommitted in MAIN after rotate-self; the Prime's next `git add`/sync commit bundles it; a concurrent rotation's spawn row extends the window. Wait and retry, never touch the Prime's row.
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
