# Spawn-seating audit — belam 20260911T175816Z + sanctuary-helper 20260911T181834Z (both seated by `rotate.py spawn`, no rotation record)

Owner 16:2xZ: a new seat is audited like a rotation. Both seatings today were RECOVERIES — the predecessor died without rotating (Prime: 17:45:46Z; helper: 16:06:42Z, Epoch mismatch 409) and the point spawned the successor by hand with `rotate.py spawn`. No record, no STARTUP OUTPUT, no facts, no pending ack.json, no wrapper. This is the third measurement of the same shape (sensei-director first seating 161009Z: 22 of 40 calls were what the template gives free).

## belam 175816Z (Prime XI, `[49c09b]` @289) — wake 22 calls to ack+commit (d 5 · a 2 · b 6 · c 9)

| calls | what | class | pre-fillable by |
|---|---|---|---|
| 1 | ListAgents | d | (the ref; legitimate) |
| 2, 13 | HANDOFF.md 1-80, 80-125 by hand | b | prime_director `handoff-head` first_turn entry (proposed 140328Z) — spawn runs no first_turn |
| 3-9 | records dir, tmux windows, seats row, launch script, `ps` for rotate.py, ack/pending files — "was I rotated or spawned; does a wrapper wait?" | c (7) | spawn prints ONE `[seating]` line: spawned by <seat> at <ts>, predecessor pid <p> died <ts>, no record/no wrapper, ack required |
| 10 | meter + inbox | b | first_turn `inbox` |
| 11 | belam row in worktrees vs main | a | F2 |
| 12 | rotate.py 1362-1440 (ack grammar) | c | F6/F8 — not in its input because spawn runs no `facts` |
| 14-17 | belam.log forensics on X's death | d-ish (4) | spawn (recovery form) prints the autopsy: last non-heartbeat log lines before the pid vanished + reaper lines |
| 18-19 | hypothesis reads (pin-is-the-lease, keeps-the-window) | c | — |
| 20 | `ack --gen 11 --ref 49c09b diff --text -` | d | the decision (diff: X's handoff was stale by the death gap) |
| 21-22 | HANDOFF edit + commit | d | — |
| 23-24 | lock path grep (F7) | c | facts, again absent |

Later: 35-42 and 68-73 (~14 calls) more autopsy of X and of the helper gen 4 death, feeding goal:g17.1's SEAT PROTOCOL note and the g15.19 recovery decision — the Prime's genuine work, but the EVIDENCE (log tail, reaper log, launch script, ps chain) is mechanical.

## sanctuary-helper 181834Z (gen 5, `[47d190]` @290) — wake 32 calls to ack+commit (d 4 · a 3 · b 2 · c 12 · merge-repair 11)

| calls | what | class |
|---|---|---|
| 1-7 | fetch + merge origin/season/s2 into the worktree + resolve conflicts in seats.md and one hypothesis node | repair (7) — the worktree carried an unresolved merge from gen 4's death; spawn did not say so |
| 8 | ToolSearch SendMessage | a (F11) |
| 9 | ListAgents | d |
| 10 | tmux windows + pane pid | a (F8) |
| 11-15 | rotations.md grep ×2, ack json ls, `rotate.py -h` + `ack -h`, records ls, `git show` | c (5) — "which gen, is there a record" |
| 16, 22, 24 | ps ppid chain, ps for rotate-self | a/c (3) |
| 17-19, 23, 25 | rotate.py source 1495-1560, 234-260, 3300-3345, 1360-1460; locations.py | c (5) |
| 20-21 | record + launch script | c (2) |
| 26-30 | rows in other checkouts; second fetch/merge; seats.md conflict (the point wrote the row in MAIN, the worktree had its own) → `checkout --theirs` | repair (5) |
| 31-32 | ack + commit | d |
| 33-35 | `peek` ×3 to read one long inbox message (head / sed / awk slices) | b (3) — `read` once |

## The one root cause, measured three times

`rotate.py spawn` seats a successor with none of what rotate-self gives: no `startup.first_turn` (so no `facts`, no `inbox`, no `predecessor-log`), no meter pin, no pending ack.json, no `[seating]` line naming its own shape. Cost: prime 17 of 22, helper 17 of 32 (+11 merge repair that a `[seating]` worktree-state line would have named), sensei-director 22 of 40. Floor for a spawn seating is the same 3 (ListAgents · ack --ref · commit) once spawn does what rotate-self does at step 2.

The brief compounds it: `prime-director-successor.md` line 5 promises "the seat row, pin and verification already recorded … the ONE instruction left is the ACK" — true under rotate-self, false under spawn; the Prime spent calls 3-9 testing the promise. Prose fix applied by master-sensei this pass (a "no STARTUP OUTPUT below = you were spawned" block).

## Proposals (routed to sensei-director as g15 lines)

1. CODE — `rotate.py spawn` runs the seat's template `startup.first_turn` (the `--tier` names the template), pins the meter, writes the row + pending ack.json exactly as rotate-self step 2 does, and prints a `[seating]` block: spawned-by, predecessor pid + death ts, record: none, wrapper: none, worktree state (behind N, unresolved merge: yes/no). Removes ~17 calls per recovery seating (measured ×3).
2. CODE — recovery autopsy pre-fill: `rotate.py spawn` (or `rotate.py autopsy --seat S`) prints the predecessor's last 10 non-heartbeat debug-log lines before its pid vanished + the reaper-log lines for that pid + the launch script path. Removes the 4+14 forensic calls; the Prime still decides `continue|diff` and what the SEAT PROTOCOL says. Captive/driven: the tool gathers, the LLM judges.
3. CODE — `sensei.py wake-audit`: the wake window ends at the `rotate.py ack` call (or the row commit right after it), not at the first classifier-(d) call; on both seatings today it cut at call 1-2 (`git status`, `sed HANDOFF.md`) and reported a=0 b=1 for a 22/32-call wake. Anything before the ack is wake by F8's definition.
4. PROSE (relay to the point, owner of the quorum scratchpads): `.agi/sessions/quorum/sanctuary-director.md` and `sanctuary-helper.md` get the same "no STARTUP OUTPUT = spawned" block as prime-director-successor.md now carries, until proposal 1 lands.
5. PROSE (F19 candidate for `## facts`, once spawn runs facts): "one `send.py read <seat>` reads the whole inbox; never `peek | head/sed/awk` slices (helper 181834Z calls 33-35)."

## rotate-out side

None — both predecessors died. The cost of a death is the successor's autopsy (proposal 2) and the point's respawn by hand; g15.19 (graceful recovery) is the point's round L4.283.
