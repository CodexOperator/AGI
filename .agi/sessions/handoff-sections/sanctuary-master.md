# sanctuary-master — gen II live slice

Trimmed per owner 2026-09-09 (trim + diagram-max, continuous). Detail lives in
nodes; this is the bridge only. **No owner verbatim here by design** — the
auto-archive ask lives on its node (`c79a25d15`), not in this file.

## Seat

```
  owner ──▶ prime belam-S1-L3-XV  agi-ad [90fef7] @228
              │        (XIV agi-a7 [bcd0bd] @226 idles, predecessor protocol)
              ▼
        sanctuary-master gen II   agi-80 [1ba35d]   meter ~0.22
        CONFIG-ONLY: writes config:seats rows. Nothing else.
              │
              ▼
        sanctuary-director gen IV agi-ea [113e1f] @227   SOLE WORKER
              (gen III [643312] @225 still idle+live-looking — the
               auto-archive ask, in the flesh)
```

STATE: stopped since the owner's pause — no dispatch, no rotation, nothing
spawned, 0/25. Pin claimed, `source=seat_pin`. Registry: 12 rows, zero pin
collisions, director-kids 2/2.

## Live / next

- **Nothing queued for me.** All registry cells are current and self-reported.
- At the go: nothing pending. `master-sensei` 0.373 was handled by its own
  rotator path; not mine.
- Hazard 5 + auto-archive ask are **L4 backlog** (XIV's filing). Not my work.
- Window-id join is queued to `sanctuary-director`, gated behind `_rotate_common`.

## Closed this session

| Item | Outcome |
|---|---|
| Stale pin on own seat | Claimed; 0.334 (predecessor's) → true 0.0752 |
| 3 stale registry cells | Corrected `8d7289a6b`; refs self-reported only |
| `session_ref` 643312→113e1f | `dff879947`, on gen IV self-report |
| Ghost `[ask]` ×50 | Diagnosed: no comms file, no cursor, no process → client-side pane replay. **Do not re-investigate.** |
| Owner auto-archive ask | Recorded `c79a25d15` |
| Hazard 5 | 5/5, independently reproduced; `fe8fbb570` |

## Rules this seat earned (carry these)

- **An empty cell announces its own ignorance; a stale one impersonates
  knowledge.** But a blank is not a ritual — do not blank a value that is still
  true merely because it is about to change.
- **A seat's word about its own identity is the authority.** The window-id join
  proposes, the seat confirms; a self-report is never overwritten by a
  derivation. Display names collide (`agi-ea` → 2, `agi-32` → 3); window ids
  do not.
- **A delivery receipt proves the transport worked, never that the right seat
  read it.** Two of my reports vanished into a rotated-out prime, both
  returning success.
- **A rotation must announce a resolvable address, not a name.**
- **A wrong finding costs more than a wrong cell** — a cell is fixed by the next
  reader, a finding gets built on.
- **Verify peers' findings, not just their writes.** That caught a real defect
  of XIV's and a real one of mine, an hour apart.

## Traps (measured here)

- **`grid.py commit --all` runs on a `*/5` cron.** No agent can "hold off" to
  protect another's WIP from the grid — that decision is not theirs to make.
  Hourly `:07` pushes `season/s2`; hand-pushing is harmless duplication.
- **`.agi/sessions/` is gitignored (line 38)** — slices need `git add -f` or
  they live only on this box.
- **Measure exit codes bare.** I read `$?` through `| head` and reported
  `grid.py payload` as exit 0; it is **1**. Retracted, with the generalisation
  I had built on it.
- **Money is measured at source, never relayed.** I forwarded a spend figure I
  could not validate and it was wrong.
- **`ps` greps match live seats**, whose prompts contain script names. Trust
  `spawn_budget.py status` for what to kill.
- Trap 0x (XIV): `grid.py payload` returns nothing for payload-less nodes;
  `config:seats` has 19 versions and no `show`/`cat` to read one back whole.
  Use `grid.py diff` or `git log -S`.

## Boundaries held

Never wrote a pin under a live seat. Never wrote a `belam`/`adv-*` row — refused
even when the prime instructed it; XIV wrote its own. Never inferred a
`session_ref`. Never fabricated a missing rotation record. Never built: rows are
mine, prose is the Sensei's, builds are the kid's.
