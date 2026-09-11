# SESSION HANDOFF — 2026-09-11 sensei-director: THE SANCTUARY DIRECTOR (the g15 perpetual-goal seat) — LIVE SCRATCHPAD (gen V = loop L5 from 21:35Z; row generation 4 → the successor acks `--gen 5`; stamp 22:22Z)

## §0 WHO YOU ARE (identity is SUPPLIED, never claimed)

Seat `sensei-director` in `config:seats` — the Sanctuary director: the director-kid that watches `goal:g15` and takes the Sensei's asks straight (founding order: owner 15:5xZ, verbatim at `doc:l4-owner-decisions` line 9; its two rules — no loop docs, one loop per generation — same node). Address = your ListAgents ref; window `sensei-director` in tmux; worktree `.agi/worktrees/seat-sensei-director`, branch `seat/sensei-director@s2`; Prime = `belam` (`send.py send belam "<one line>" --from sensei-director`); Sensei = `master-sensei`; point director = `sanctuary-director` (runs the L4 queue; you do not). Owner quotes live in nodes, never here.

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

## §3 🔴 STATE (gen V, ref `588897`, window @306; stamp 22:28Z; was 22:22Z)

| | |
|---|---|
| seat | `seat/sensei-director@s2` synced to origin/season/s2 at the last dispatch; nothing unpushed |
| merge-ups this loop | **SL2#6 LANDED 22:14Z**: 0ca5a801b on c508dc585 (SL4.06 g15.25 line (1) + SL5.01 g15.24 fix (a) + the three line (2)-(4) briefs), suite FIRST RUN ALL 11 GREEN 3485/14, **active 2275 / deprecated 195 / total 2470** (floor 2266/195/2461), stamp on 4d168471c, reported |
| graph | goals **180** (g15.26 minted this loop) · 0 broken links · GOALS.md byte-identical at every commit · +3 experiment nodes landed |
| spend | account read by the Prime 21:5xZ $17.26; deepseek rounds ~$0.5-1 each; floor $1.00 |
| wake | `## STARTUP OUTPUT` → ONE act: `rotate.py ack --seat sensei-director --gen 5 --ref <bare ListAgents ref> continue` (after SL5.01 the spawn row is pre-committed; ack commits its back-fill and prints the push line — run it), then one line to the Prime |

### Open asks (Sensei/owner/Prime → this seat): goal · brief · round · state

| ask | goal | brief | round · agent | state |
|---|---|---|---|---|
| LANDED this loop (SL2#6) | g15.25 line (1) SL4.06 · g15.24 fix (a) SL5.01 | — | — | on season/s2 |
| mur-39's four orders on line (1) | `goal:g15.25` | same brief as SL4.06 (fix-only orders noted at f53cad72e) | **SL5.02** · a00-821727e6 | **HARVESTED 22:28Z** into the seat (kid proved; prime gate before minting, CR reader defect fixed, one registry verified in-process, RFC verify asserted; 316 green). In merge-up SL2#7 |
| OWNER 22:1xZ (doc:l4-owner-decisions:657-658): reserve a `lockdown` BOOLEAN + seam now, build next season | `goal:g15.25` | `hypothesis:l4-lockdown-is-a-reserved-boolean-that-warns-and-encrypts-nothing-until-it-is-built` (`comms` block in .agi/config.json: `lockdown: false`, `verify: "informational"`; one `_comms_config` helper; true = one warning per send/read, no cipher) | **SL5.03** · a00-5fa9dd23 · `loop/hypothesis-l4-lockdown-is-a-rese-a00-5fa9dd23@s2` | RUNNING from 22:21Z, parallel with SL5.02 (disjoint seams by brief). Harvest: send neighbourhood |
| OWNER GO 'fix and flip': readers refuse a FORGED block under enforcing; reviewed by name before any reader refuses | `goal:g15.26` (reported 22:2xZ with caveats) | `hypothesis:l4-a-reader-refuses-a-forged-block-under-enforcing-and-the-value-flips-after-a-named-review` | → **SL5.04** | NOT CUT: serial after SL5.02 + SL5.03 land + merge-up SL2#7 (needs the fix bytes + `_comms_config`). The VALUE stays informational on season/s2; the Prime flips it after the review |
| g15.25 line (2) key-gated rotate-self minting the successor key (IN this loop per Prime 22:14Z) | `goal:g15.25` | `hypothesis:l4-rotate-self-is-key-gated-mints-the-successor-key-and-retires-its-own-into-key-history` | **SL5.05** · a00-277de473 · `loop/hypothesis-l4-rotate-self-is-key-a00-277de473@s2` | RUNNING from 22:31Z, parallel with SL5.03 (rotate.py vs send.py). Harvest: rotate neighbourhood + test_write_self_row.py; expect the spawn-row commit to carry pubkey + key_history in ONE commit |
| lines (3) (4) — hand to the next generation | `goal:g15.25` | `hypothesis:l4-the-predecessor-answers-the-ack-and-rotate-out-is-one-signed-call` · `hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up` | — | briefed, not cut this loop (owner: wrap up soon) |
| owed by the Prime to me | mur-SL2.3/4/5 (review workflow running 22:08Z) | — | — | findings become fix-only briefs; measure its line numbers on the merge-up commit it names |

### 🔴 Where it stops — the next command

```
python3 extensions/agi/bin/spawn_budget.py status | grep -E "iter=SL5.0[35]"   # a parent gone = harvest that round (SL5.03 a00-5fa9dd23 send/config.json; SL5.05 a00-277de473 rotate.py)
F=/home/ubuntu/work/agi/.agi/sessions/inbox/sensei-director.md; awk '/^# read up to here/{f=1;next} f' $F   # then ONE send.py read
```
**Merge-up SL2#7 as soon as SL5.03 is harvested** (carries SL5.02 + SL5.03; window? → grant → §1 shape). Then cut SL5.04 (flip, needs `_comms_config` from SL5.03 on the base). Harvest SL5.05; merge-up SL2#8 (SL5.04 + SL5.05); card; rotate at 0.4.

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
- **Two rounds on the same file at once** — brief each with an explicit EXCLUDED list naming the other's functions; harvest seams then stay disjoint.
- **The 18 s test** `test_rotate_selfreap.py::test_reap_belam_oldest_pane_seam_detached_tree` is pre-existing, not a fixture sleep from a round.
- Parents run deepseek-v4.1-flash, ~10-30 min per round; `heal.py`'s `reason=overdue` dm is informational — keep polling, never replace.
- `rotate-self` refuses through `prepare`'s captives: commit + push + merge origin/season/s2; write the card LAST.
