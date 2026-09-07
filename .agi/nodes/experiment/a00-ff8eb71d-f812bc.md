---
id: experiment:a00-ff8eb71d-f812bc
mint_id: c8f7f757f3cc4481b17c696021d12d18
type: experiment
parents:
  - hypothesis:loop-scoped-iteration-ids-cannot-clobber
next_edges: []
confidence: 0.65
edited_by: season.py
evidence_runs:
  - experiment:a00-ff8eb71d-f812bc
  - experiment:a01-095ada3e-1662a8
scaffold_hash: a1b600a51763d1bf
season: 1
thought_session: season
title: A00 ff8eb71d f812bc
verdict: inconclusive_lean_disproved:65
---
# experiment:a00-ff8eb71d-f812bc

## Experiment

Traced (no live dispatch run — code trace + one manifest read) whether
loop-scoped iteration ids (`L<loop>.<nn>`) exist anywhere end to end, and
whether a fresh `driver.sh` run would clobber existing session data.

1. `grep -n "iter\b|ITER|session" extensions/agi/driver.sh` — the outer loop
   is `for i in $(seq 1 "$MAX_ITERS")`. `i`/`n` always starts at 1 on every
   invocation; there is no persisted "next free id" state anywhere in
   driver.sh.
2. `grep -rn "iter_n\|next_iter\|last_iter" bin/*.py driver.sh` — `iter_n` is
   a plain caller-supplied CLI arg in cli.py/dispatch.py/heal.py/post_wire.py/
   zoom.py/viewport.py. None of them allocate it; all of them trust the
   integer driver.sh hands them.
3. `grep -rn "L[0-9]+\.\|loop_id|LOOP_ID" bin/*.py driver.sh` — zero hits
   where `L<loop>.<nn>` is parsed or formatted by code. Every match is a
   comment/prose reference to a work session (e.g. "L1.08"), never a real
   identifier. The loop-scoped id in `testable_claim` does not exist in the
   engine today; `L1.01..L1.10` in this session's commit subjects is a
   director-typed convention only.
4. Read `.agi/sessions/iter-001/manifest.json` directly — it is NOT empty
   scaffold data, it holds a real agent record from 2026-09-01/02
   (`a00-a54f694b`, `hypothesis:a00-a54f694b-b20b78`). `ls .agi/sessions`
   shows both `iter-001..iter-108` (old, low numbers) and `iter-1002..1039`
   (current run) coexisting on disk right now — confirming the low-number
   range is not free space, it is real history.
5. Read `dispatch.py:314-354` (the manifest-write path) — goal:s28 already
   added merge-by-agent-id: on write it reads the existing manifest at
   `iter_dir/manifest.json` if present and appends new agent records to
   `manifest["agents"]` rather than replacing the list. `sess_dir.mkdir(...,
   exist_ok=True)` similarly never errors or truncates on collision.

## Evidence

- `driver.sh:239` — `for i in $(seq 1 "$MAX_ITERS")`, no allocator.
- `dispatch.py:340-354` — read-old-manifest-then-merge-agents (goal:s28),
  confirmed present in current code, not aspirational.
- `.agi/sessions/iter-001/manifest.json` — 2986 bytes, one real agent record
  dated 2026-09-01/02, still on disk and readable now (goal:g7's
  "nothing the loop produces is ever [lost]" holds for this file, today).
- `grep -c` for `L[0-9]+\.` as a parsed identifier across `bin/*.py` and
  `driver.sh`: 0 matches that are code; all matches are comments.

## Result

Split verdict on the compound claim:

- **"cannot clobber an existing manifest"** — TRUE for the one path tested:
  goal:s28's merge-by-agent-id means a fresh dispatch into `iter-001` today
  would *append* a new agent to the existing record, not delete or
  overwrite the 2026-09-01 entry. This part of the hazard is already fixed.
- **"iteration ids are loop-scoped (L<loop>.<nn>) end to end"** — FALSE.
  Nothing in `cli.py`/`dispatch.py`/`heal.py`/`zoom.py`/`driver.sh` formats,
  parses, or allocates an `L<loop>.<nn>` id. The only place that string
  shape exists is hand-typed commit subjects and node prose. `driver.sh`
  still restarts every run at `iter-1`, colliding in *name* (though not, per
  the point above, destructively) with whichever low iter-NNN a past run
  already used.

So the hypothesis is half-built: the narrow data-loss hazard (manifest
overwrite) already has a guard (s28); the broader claim in the
`testable_claim` — a real loop-scoped id end to end — is not implemented
anywhere. A test "point the driver at a populated sessions dir" would go
green for manifest merge and red for "ids are loop-scoped," because that
mechanism doesn't exist to test.


## Agent Notes
Traced driver.sh/dispatch.py/cli.py/heal.py/zoom.py: no L<loop>.<nn> id is parsed or allocated anywhere in code -- iter numbering is always seq 1..MAX_ITERS with no persisted state. goal:s28's manifest merge-by-agent-id does already stop the narrow overwrite hazard on re-dispatch into an existing iter dir, confirmed against real iter-001 data from 2026-09-01.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a01-99b43724, iter 1039) accepted this run's split verdict
unchanged and only added `evidence_runs`. The one contested fact -- whether a
re-dispatch into an occupied `sessions/iter-NNN/` destroys the existing
manifest -- was re-checked at source, because the sibling run
`experiment:a01-095ada3e-1662a8` concluded the opposite from the same file.
This node is the correct one: `dispatch.py:335-350` reads the old manifest and
carries `agents` and `started_at` forward (goal:s28), and `cli.py:522-526`
only reads a manifest, never writes one. The sibling stopped at the
`mkdir(exist_ok=True)` on line 315. The two runs agree on the other half --
no `L<loop>.<nn>` id exists in code -- so both are cited here as evidence for
the lean, and the sibling was demoted to a lean of the same sign.
<!-- THOUGHT:END -->