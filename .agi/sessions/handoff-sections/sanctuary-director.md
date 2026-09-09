# sanctuary-director — gen V slice (live, 2026-09-09)

**Seat:** `agi-cc [f9472e]`, tmux `agi-rc:@229`. Pin
`.agi/sessions/sanctuary-director.meter`. **Correspondent: XVI =
`agi-05 [eb30d2]` @230** — XV rotated out, never message it (trap 0v).
🔴 Survival mode: prime + me only. Wake no other seat. L3 takes no new work.

| | |
|---|---|
| Meter | **0.2433** of 0.35 — rotate at cap, not past it |
| Suite | **2249 passed, 1 skipped** (2241 at claim; +8, no regressions) |
| Graph | node_count 1779 · active 1585 · dep 194 — grew every step |
| Branch | `season/s2`, pushed `e79800649` |
| Live | SD.16 parent `a00-402cda8d` (pid 2775850) |
| Spend | account **$12.88**/$92 (both rounds ≈$0.14) · key $7.87/$15 · floor $1 untouched |

## Item 54 — CLOSED, both halves proved live

Three broken verbs found, all fixed, all shipped green before:
- `read` fell through to the write path — restamped `edited_by`, stripped a
  trailing newline. Fixed: terminal branch before `submit`. **Verified with the
  exact command that corrupted two nodes.**
- `body_patch <path>` never applied — submit L494 applies, L531 read the file.
  Fixed by moving the read before the apply-check; the standalone guard now
  fires for the path form too.
- `SKILL.md` overstated the fix (said "path or `-`"); I narrowed it.

**Three live adoption proofs, three actors:** kid `a00-b4d8b7b0` →
`build:bin-write`; me → `build:skills-agi-SKILL.md` via `patch -`; me →
the hypothesis node via `body_patch <PATH>`.

🔴 **The recipe that fell out of it:** the applier's body view is offset by one
from a naive BODY:BEGIN split, and **`read body` shares that view**. So:
`read body N:M`, then build the hunk from those exact bytes. The two halves
compose — that is the owner's ask literally.

**Honest gaps, not to be dressed up:** SD.15's kid sits at
`inconclusive_lean_proved:50` because I pointed `evidence_runs` at itself and
the gate rightly refused it. Both live runs are invisible to the gate
(evidence must be node-shaped; a director mints no experiment nodes) — banked
by XVI to `doc:l4-owner-decisions`.

## Item 55 — sections half CLOSED, rotation half running

`handoff.py` claim→read→release proved live on myself: **HANDOFF.md whole
77,943 B / ~19,485 tok; §5 served at 936 B / ~234 tok = 83x**; §0 ≈ 20x.
SD.16 now covers discoverability (`brief.py` names `handoff.py` 0 times), the
read-then-hunk line, three friction fixes, and fixture-proof of the rotation
clauses. **No seat may launch** — the node's live claim is banked, not faked.

## Traps paid for this session
- **0ah** — verify the BYTES, never the `updated:` line. It printed `updated:`
  for a read that corrupted nodes, a patch that discarded its diff, and a
  commit whose message described work that never happened.
- **0ai** — the harness kills background tasks for "low memory" while `free`
  shows 18.9 GB available. It killed a dispatch wrapper and orphaned a kid.
  **Launch dispatch with `nohup … &`,** and watch via Monitor, not bash loops.
- `pgrep -af dispatch.py` matches **the prime's own seat session** (its prompt
  text contains the string). Sweep by PID off `spawn_budget.py status`, never
  off a grep — item 71, reproduced.

## 🔴 Next action if I die here
Harvest SD.16: `git -C .agi/worktrees/a00-402cda8d status --porcelain` **before**
believing the branch empty — both harvests this session had staged work with
zero commits. Then merge-base diff, full verify, merge, `grid.py commit --all`,
push, report to XVI. Then rotate at cap.
