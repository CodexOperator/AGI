# sanctuary-master — generation II live slice

Written defensively under the owner's token stop, per the standing order
("if you are over your cap, write your handoff slice to disk NOW, then hold").
Not a rotation. This seat is at ~0.16-0.19 and holding, not rotating.

## State

- **Seat:** sanctuary-master gen II, session `1e15de95` (agi-80 `[1ba35d]`),
  window `agi-rc:sanctuary-master-II`. Main checkout, NOT the worktree.
- **Pin claimed and honest.** `.agi/sessions/sanctuary-master.meter` reads
  `1<TAB>1e15de95-...`. `meter --seat` now resolves `source=seat_pin` rather
  than falling back to a heuristic that returns another seat's number.
- **Nothing running.** 0/25 live across repeated sweeps. This seat never
  spawned anything, so nothing of its own can return as `-r1`.
- **No dispatch, no rotation, no seat row written.** `config:seats` is
  byte-identical to how generation I left it.
- Committed and pushed: `f35b21dca` (hazard 5), `c79a25d15` (owner feature ask).

## The one thing to do first at the go

`master-sensei` meters **0.373**, over the 0.35 cap, running ~7h, slice already
on disk. DM it its own number so it rotates informed:
`rotate-self --prompt-file`, never `loop`.

## Queued, unstarted — one pass, this seat only

Correct three cells in `config:seats`, all self-reported or provably dead,
none inferred:
1. `sanctuary-director.session_ref` = `281d53` is DEAD — that session rotated
   away at 13:14:19Z. **Blank it, do not guess the successor's ref.** Ask
   gen II to self-report.
2. `sanctuary-master.session_ref` — fill `1ba35d` (own ref, self-reported).
3. `sanctuary-master.worktree` — currently `.agi/worktrees/seat-sanctuary-master`,
   but this generation runs in the MAIN checkout (`git rev-parse --show-toplevel`
   = `/home/ubuntu/work/agi`) and wrote its pin there. Empty means main checkout,
   so the cell should be empty.

## Findings this session

**HAZARD 5 — the rotation record and the generation stamp are complementary,
and NO seat has both.** Landed on `hypothesis:l3-seat-pin-generation-never-increments`.
`cmd_rotate_self` writes the handoff early (rotate.py:2120) and the record late
(2163/2199/2211), all behind the wait for successor confirmation; `cmd_loop`
writes the record and never the handoff.

Measured: `alive`, `sanctuary-master`, `sanctuary-director` -> generation stamp,
NO record. `self-perpetuating`, `all-is-one`, `belam` -> record, NO stamp.

**Generation I blamed a stop sweep killing its rotate-self mid-wait. That cause
is WRONG and a fix aimed at it would miss.** Two independent disproofs: `alive`
rotated at 12:39:57Z, seven minutes BEFORE the sweep, same gap; and
`sanctuary-director` rotated at 13:14:19Z, after every sweep, clean and
sanctioned, with no kill anywhere near it — same gap. **Three of three
`rotate-self` rotations lack their record. Base rate 100%: this is the normal
outcome under interruption, not an unlucky signal.**

Fix direction: write the record BEFORE the wait, in the same write as the
generation stamp, and amend on confirmation. "Rotation started, successor
unconfirmed" is true and recoverable; no record is indistinguishable from no
rotation. **A fact split across a wait is a fact any signal can bisect — two
writes at two TIMES are two writers, even inside one function.**

NOT fixed here: this seat is config-only. Hand-writing the missing records was
considered and REFUSED — a fabricated rotation artefact reads as evidence,
which is the failure the node exists to describe.

**THE GHOST `[ask] how do I rotate?` — FULLY DIAGNOSED, DO NOT RE-INVESTIGATE.**
Fired 30+ times at this seat. Generation I answered it four times before
checking. Ruled out, by measurement, both in-graph sources: it is in NO comms
file (not the quorum room, not quorum-requests, not mail-alert, not any DM —
it appears only inside gen I's own report quoting it); room cursors are
advancing normally; and NO process on this box generates it (no looping
`send.py`, no watcher). **Therefore it is a client-side replay in the Claude
Code pane, not an agent, script, or graph queue.** Nothing in the repo can
stop it. The lever is the owner's: clear the stuck input in the terminal, or
reattach the window. Under a token stop it is a real drain, because every
firing costs a full context resend regardless of reply length.

**THE HANDOFF SAID "WORKING TREE CLEAN, 0 UNPUSHED". IT WAS NOT.**
`extensions/agi/bin/rotate.py`, `extensions/agi/bin/write.py` and
`extensions/agi/tests/test_rotate.py` carried uncommitted edits belonging to
another agent. Caught only because `git diff --stat` showed four files instead
of one after this seat's own edit. **Committed a single explicit path and
deliberately skipped `grid.py commit --all`**, which would have versioned
another agent's half-finished payloads under this seat's name. A reflexive
`commit -a` there is the trap.

**A `ps` grep loose enough to catch dispatched agents also matches the LIVE
SEATS.** `master-sensei`'s own session matched a scan here only because
`rotate.py` appears in its prompt text. Trust `spawn_budget.py status` for what
to kill; a grep sweep would take the seat system with it.

## Boundaries held

- Never wrote a pin under a live seat. Claimed only its own.
- Row is this seat's; prose is the Sensei's; build is the kid's. No build, ever.
- Refused to infer any `session_ref` from tmux. A blank cell is honest; a
  guessed ref gets trusted and is worse than none.
- Did not fabricate missing rotation records.
- `belam`'s row still reads `rotated_by: quorum`, contradicting owner 7b.
  Owner's row — flagged, never touched.

## Trap: "erasing is safe, it's in the grid" assumes a PAYLOAD — verified

Found by `belam-S1-L3-XIV`, verified here as custodian rather than taken on
report. `CLAUDE.md` teaches that replacing a thought is safe because every prior
version is one command away. **That guarantee is real for `build:HANDOFF.md`,
which has a `payload_ref`, and reader-dependent for every payload-less node —
the class most `.geometry` config nodes fall in, INCLUDING `config:seats`, the
registry this seat is custodian of.**

Measured:
- `grid.py versions config:seats` -> **19**. The grid IS versioning `node.md`.
- `grid.py payload config:seats` -> `ERR: no payload recorded ... the node
  either carries no payload_ref or has not been committed since payloads began`.
  The documented recovery route returns nothing.
- `grid.py` verbs are `{init, commit, log, diff, versions, payload, checkout,
  status, migrate-refs, migrate-mint-refs, sync, cron}` — **there is no `show`
  or `cat`**, so no way to print `node.md` whole at version N.

So the history is NOT lost; it is recoverable only by reconstructing from
`grid.py diff`, by a reader nobody names. Nineteen versions exist and none can
be read back whole.

🔴 **CORRECTION — I CLAIMED `grid.py payload` EXITS 0. IT DOES NOT. IT EXITS 1.**
Caught by `belam-S1-L3-XIV`, re-measured bare here rather than taken on report:

- `payload config:seats >/dev/null 2>&1; echo $?` -> **1**
- `payload config:seats --version 19 >/dev/null 2>&1; echo $?` -> **1**
- `payload config:seats 2>&1 | head -1 >/dev/null; echo $?` -> **0**

**The 0 was `head`'s.** `$?` after a pipeline reports the LAST command's status,
so my measurement captured the reader's success and discarded the writer's
failure. I had piped through `head` because the error line is long — the natural
way to look at a noisy command, and wrong in the direction that makes a defect
look worse than it is.

**SO THE TRAP IS MILDER THAN I RECORDED IT.** An automated recoverability check
— "can I read this back before I overwrite it" — **does** work: it gets a
nonzero exit and fails correctly. Trap 0x stands as originally written (the
documented reader does not see payload-less nodes; use `grid.py diff` or
`git log -S`). **My escalation of it does not stand.**

**AND THE BRIDGE I DREW IS WITHDRAWN.** I claimed this was item 4 of
`l3-seat-pin-generation-never-increments` ("a guard that prints an error and
exits 0 is caught by a human and missed by every script") reappearing in the
recovery path, and called `ERR:` + exit 0 "a recurring shape on this box". That
generalisation rested on this one measurement and the measurement was mine and
wrong. **Item 4 is about the PIN REFUSAL path, which I have not tested** — it
may stand entirely on its own evidence; nothing here bears on it. Right now the
shape has one unconfirmed instance and one disproved one. **Measure the pin path
bare before treating it as a pattern.**

**THE LESSON, and it is the sharper half:** a wrong finding is more expensive
than a wrong cell, because a cell gets corrected by whoever reads it next and a
finding gets built on. This is the same family as trap 0m (`pgrep -fc` printing
"0" and exiting 1, so the `||` fired and the loop captured "0\n0"). Banked by
XIV as trap 0y: **measure bare, or set `pipefail`.** Shell exit status is a
place this box keeps getting cut — and this instance appeared inside a FINDING
rather than inside the system, which is the first of its kind today.

RULE, from XIV and endorsed: **check where a thought actually lives before
overwriting it.** `git log -S '<phrase>' -- <file>` is the reliable finder —
XIV looked in `8d7289a6b` for this seat's three-cell thought and it was not
there; it was in `b98d1ea7b`.
