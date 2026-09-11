# SESSION HANDOFF — 2026-09-11 sensei-director: THE SANCTUARY DIRECTOR (the g15 perpetual-goal seat) — LIVE SCRATCHPAD (gen V = loop L5 from 21:35Z; row generation 4 → the successor acks `--gen 5`; stamp 22:22Z)

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

## §3 🔴 STATE (gen V, ref `588897`, window @306; stamp 23:02Z; was 22:22Z)

| | |
|---|---|
| seat | `seat/sensei-director@s2` synced to origin/season/s2 at the last dispatch; nothing unpushed |
| merge-ups this loop | **SL2#6 LANDED 22:14Z** (0ca5a801b: SL4.06 line (1) + SL5.01 spawn-row commit; 11 green first run; 2275/195/2470). **SL2#7 LANDED 22:52Z** (342285b13 on 59ef1a7a1: SL5.02 mur-39 FIX + SL5.03 lockdown reserved; run 1 red 1/3496 on `test_real_adapter_restart` under review-workflow CPU load — passes alone, no adapter bytes in the merge; run 2 ALL 11 GREEN 3496/14; **active 2281 / deprecated 195 / total 2476**; published under the Sensei's gen-2 rotation, origin 4d36b29ba, stamp there; reported). SL5.01 live-proven: `b829898e5 master-sensei spawn row: gen 2` was committed by rotate-self itself |
| graph | goals **180** (g15.26 minted this loop) · 0 broken links · GOALS.md byte-identical at every commit · +6 experiment nodes landed |
| spend | account read by the Prime 21:5xZ $17.26; deepseek rounds ~$0.5-1 each; floor $1.00 |
| wake | `## STARTUP OUTPUT` → ONE act: `rotate.py ack --seat sensei-director --gen 5 --ref <bare ListAgents ref> continue` (after SL5.01 the spawn row is pre-committed; ack commits its back-fill and prints the push line — run it), then one line to the Prime |

### Open asks (Sensei/owner/Prime → this seat): goal · brief · round · state

| ask | goal | brief | round · agent | state |
|---|---|---|---|---|
| LANDED this loop | g15.25 line (1) SL4.06 + its mur-39 FIX SL5.02 · g15.24 fix (a) SL5.01 · g15.25 lockdown reserved SL5.03 | — | — | on season/s2 (SL2#6 + SL2#7) |
| OWNER GO 'fix and flip': readers refuse a FORGED block under enforcing; reviewed by name before any reader refuses | `goal:g15.26` (reported 22:2xZ with caveats) | `hypothesis:l4-a-reader-refuses-a-forged-block-under-enforcing-and-the-value-flips-after-a-named-review` | **SL5.04** · a00-3a5689fc · `loop/hypothesis-l4-a-reader-refuses-a-a00-3a5689fc@s2` | RUNNING from 22:54Z (base carries SL5.02 + `_comms_config`). Harvest: send neighbourhood; assert informational output byte-identical, FORGED withheld to quarantine, `whois --sig` exit 2, season/s2 value untouched. The VALUE flip is the Prime's after the named review |
| g15.25 line (2) key-gated rotate-self minting the successor key (IN this loop per Prime 22:14Z) | `goal:g15.25` | `hypothesis:l4-rotate-self-is-key-gated-mints-the-successor-key-and-retires-its-own-into-key-history` | **SL5.05** · a00-277de473 · `loop/hypothesis-l4-rotate-self-is-key-a00-277de473@s2` | RUNNING from 22:31Z, parallel with SL5.03 (rotate.py vs send.py). Harvest: rotate neighbourhood + test_write_self_row.py; expect the spawn-row commit to carry pubkey + key_history in ONE commit |
| lines (3) (4) — hand to the next generation | `goal:g15.25` | `hypothesis:l4-the-predecessor-answers-the-ack-and-rotate-out-is-one-signed-call` · `hypothesis:l4-the-meter-hook-rotates-at-threshold-never-mid-merge-up` | — | briefed, not cut this loop (owner: wrap up soon) |
| **mur-SL2.3-5 reviewed by name (Prime XII 22:44Z, wf_8f7f3ca5-8e0): all nine rounds accept_with_residue, no demotion.** Residues: P1 before close, P2 if it fits, P3 next season, two CHEAP now. Silence past SL2#7 = I took P1 + cheap (I did; P2 items folded where the goal already had a P1 round) | g15.14 · g15.21 · g15.24 (+g15.23/g15.13 P2) | `hypothesis:l4-prepare-measures-and-merges-the-same-ref-guard-first-and-check-5-prefers-the-rows-transcript` · `hypothesis:l4-a-spawn-writes-only-onto-a-dead-seat-and-no-season-literal-remains` · `hypothesis:l4-a-failed-ack-commit-exits-non-zero-and-unstages-and-three-tests-assert-what-they-claim` | **SL5.06** a00-4f25c9b5 · **SL5.07** a00-b4ac5831 · **SL5.08** a00-cd127adb | RUNNING from 23:02Z (all three rotate.py, disjoint by EXCLUDED lists; expect both-modified seams at harvest — keep both, re-run the rotate neighbourhood). CHEAP `seeds` on g15.21-26 DONE (4dad57c3b). P3 (wake-window rule g15.13, re-spawn gen record g15.17, `main` reason g15.18, fence-aware wrap g15.22) = next season, in the Prime's dm 22:44Z |
| master-sensei 22:49Z (rotating out): alerts never reach the inbox; a coalesced nudge is a lost wake; nine `detected` records per seating | `goal:g15.23` fix-only #2 | `hypothesis:l4-a-rotation-alert-lands-in-the-inbox-a-coalesced-nudge-still-wakes-and-detected-records-dedupe` | **SL5.09** a00-232c7d9a | RUNNING from 23:02Z (rotate.py `_announce_rotation` + send.py `_nudge_window` + detected writer). Harvest: hook + send neighbourhoods |

### 🔴 Where it stops — the next command

```
python3 extensions/agi/bin/spawn_budget.py status | grep -E "iter=SL5.0[4-9]"   # a parent gone = harvest that round: SL5.04 a00-3a5689fc (send flip) · SL5.05 a00-277de473 (rotate line 2) · SL5.06 a00-4f25c9b5 (rotate prepare) · SL5.07 a00-b4ac5831 (rotate spawn) · SL5.08 a00-cd127adb (rotate ack + tests) · SL5.09 a00-232c7d9a (alerts)
F=/home/ubuntu/work/agi/.agi/sessions/inbox/sensei-director.md; awk '/^# read up to here/{f=1;next} f' $F   # then ONE send.py read
```
Harvest each as it closes (branch `loop/<slug-prefix>-<agent>@s2`; five rounds touch rotate.py — merge serially, re-run the rotate neighbourhood after each) → **merge-up SL2#8** with everything harvested by ~23:40Z (window? → grant); reply to the Prime's 22:44Z with which P1/P2 landed (window? → grant → §1 shape; carry the first-run-red disclosure habit) → numbers to the Prime (+ the g15.26 VALUE flip is its one-line edit after the named review) → card → rotate at 0.4. Lines (3)(4) hand over briefed.

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
