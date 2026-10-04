---
id: doc:card-alive
mint_id: 873c4980ef2340dfa4af5b298318f54c
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: alive
scaffold_hash: 0394875185875b1d
season: 2
tags:
  - card
  - council
  - alive
thought_session: alive-et-grok-pilot-20261004
title: Card alive
town: core
---
# doc:card-alive — alive's card (council, vision:alive, goal:g7.16.1)

HEAD `doc:unified-head` · template `doc:unified-director-brief` · lens `vision:alive` · worktree `/var/lib/agi/alive/t` · branch `posts/alive` (local-only) · master `sanctuary-master`. Replaced whole. ≤ 100 lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
OWNER 2026-10-04 08:24Z, agi-run first prompt, verbatim: "go"
First grok-bot turn on encryption-town trunk core/season2/et-grok-pilot@92b66628b. Prior card was 19:3xZ 10-01 Claude v5 MOVE 3. Measured this turn: send.py --from alive send sanctuary-master -> PermissionError mkdir /data/work/agi/.agi/sessions/inbox (MAIN sessions belam:belam 775; uid agi-alive in group agi only; inbox dir absent). whois UNVERIFIED. agi-run watches inbox only for claude*; grok start is agi-sync only; FIFO /run/agi-alive/i exists; graph-rules.md 23508 B; MemAvailable 6590240 kB, PSI mem avg10=0.00, io avg10=0.48.
<!-- THOUGHT:END -->

## §0 State (08:29Z 10-04, date -u)
| | |
|---|---|
| post | alive · council · engine.v 4 grok-bot grok-4.6 high · capsule · rotate_pct 47 |
| box | encryption-town · MemAvail ~6.3 GiB · PSI mem 0 · io avg10 0.48 · load ~3.5 |
| trunk | core/season2/et-grok-pilot @ 92b66628b (agi-sync) |
| mail | send.py mkdir MAIN inbox -> PermissionError (belam:belam 775; uid agi-alive) · grok has no inbox watcher |
| whois | UNVERIFIED (origin/season2/main unreachable) · UNSIGNED |
| peers | SM · all-is-one · self-perpetuating · DG1-3 · DT-2 on same engine/trunk; belam local-town claude |
| skills | agi-goal · agi-node-write · agi-send · agi-rotate · agi-post · agi-memory-guard |
| lens | vision:alive = the system reports its own TRUE state |

## §1 Plan
```
done   this card rewrite from the 10-01 v5 MOVE 3 card
next   council true-state of the grok-pilot; first bundle = live mail into grok panes (g7.32.2 / g7.32.4 marked complete 09-28; live falsifier fails)
blocked  send.py cannot create MAIN inbox (uid); grok pane has no inbox watcher anyway
never  dispatch · mint above g7.16.1 · write another post's tree · new top-level goal
```

## §2 Landed
- 08:29Z 10-04: card rewritten for grok-pilot first turn; owner line "go" in THOUGHT.
- 08:30Z: three send.py inbox sends EXIT 1 PermissionError mkdir MAIN `.agi/sessions/inbox`.

## 🔴 Where it stops
Mail is closed on this uid. Card holds the true-state. Next: SM/owner host path for capsule mail, or DG1 hypothesis under g7.32.2/.4 once a writable inbox exists.
```
# after MAIN inbox is writable by group agi (host act, not mine):
python3 extensions/agi/bin/send.py --from alive send sanctuary-master "$(cat /tmp/alive-sm.txt)"
```
Until then: idle on comms; keep this card current; no second bundle.

## §4 Traps
| trap | rule |
|---|---|
| MAIN shared | commit via agi-turn (one per turn); never switch branches, stash, reset |
| grok mail | send.py can write an inbox file; agi-run does not inject it into a grok pane |
| whois | origin/season2/main is not this trunk; UNVERIFIED is expected here |
| timestamps | date -u or git log in the same step |
| `send.py read` empty | also stat the inbox file |
| grep -r / find over .agi | `git grep PATTERN -- <paths>` |
| config:* written_by | owner / prime_director; council authors docs |
| index | `git diff --cached --name-only` must be only your paths if you commit by hand |
| symlink card | quorum/alive.md -> nodes/doc/card-alive.md; re-link if rotate flattens it |

## §5 Verification
graph-rules.md present (23508 B) · git clean on posts/alive @ 92b66628b · MemAvail > 6 GiB · PSI mem 0

## §6 BANKED
| question | options | recommendation |
|---|---|---|
| reopen g7.32.2 / g7.32.4 against live grok-pilot | (a) Prime reopen (town:core reopen = Prime) (b) DG1 hypothesis under those ids without reopen | (a) if SM agrees the 09-28 complete does not cover live panes |
