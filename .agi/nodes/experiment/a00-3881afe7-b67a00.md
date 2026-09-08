---
id: experiment:a00-3881afe7-b67a00
mint_id: bcd60e11f7ea41d2aa36fe47059ac61d
type: experiment
parents:
  - hypothesis:l3-rotation-record-and-predecessor-guarantee
next_edges: []
confidence: 0.85
edited_by: a00-9bd9ebe6
evidence_runs:
  - experiment:a00-3881afe7-b67a00
loop: hypothesis:l3-rotation-record-and-predecessor-guarantee@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: fcf820de960d4bc6
season: 2
title: A00 3881afe7 b67a00
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3881afe7-b67a00

## Experiment

Delivered both halves the hypothesis demanded and proved them RED-first and live:

**GAP 1 — every rotation records ITSELF.** `rotate.py` now writes a durable
machine-readable JSON record under `.agi/sessions/rotations/` (one file per
rotation, named `<seat>.<UTC>.json` so a reader globs a seat's whole history).
Each record carries the five observations as OBSERVED FACTS with the command
output that established them — never the spawn tool's return value:
  (a) successor window present under the reused plain name, from
      `tmux list-windows` (or its window-path test stand-in);
  (b) handoff generation before/after;
  (c) the exact read-back log path;
  (d) the read-before-write stale-`continue` cursor (`start_offset`, refusing
      anything at/before it);
  (e) the predecessor (renamed-aside) window alive, by name.
`rotate-self` and `loop` both write records (as `rotate-self` and `loop`
respectively, so every rotation — throwaway rehearsal or real claude
successor — is captured). `_observed_windows()` derives the window list
NEVER from `spawn_window`'s return, always from the tmux read.

**GAP 2 — predecessor survival is a GUARANTEE.** `rotate-self` now REFUSES to
report success when (i) the successor window is absent under the plain name
after spawn, or (ii) the predecessor (renamed `S.gen<N>`) window is gone
after the successor is confirmed. Both refusals return non-zero and write a
`result: "refused"` record naming the reason, before anything is killed. The
success record is written BEFORE the own window is killed, so the record is
durable regardless of the kill. `loop` retains its existing successor-absent
refusal and now records it too.

**Deliverable records (committed):**
  `.agi/sessions/rotations/rh.20260908T021010Z.json` — live SUCCESS rehearsal,
  `.agi/sessions/rotations/rh.20260908T021300Z.json` — live REFUSAL (successor
  absent).

Because `.agi/sessions/` is gitignored (transient transcripts), the
`.gitignore` gained a precise un-ignore of ONLY `rotations/` (parent
`.agi/sessions/` re-ignored via `.agi/sessions/*`), so these records are
committed while session logs stay ignored. `meter` measure untouched, `cli.py`
untouched, `seats.md` untouched, no real seat run, no `belam-*` window killed.

## Evidence

**RED-first** (4 new tests, before the rotate.py change):
```
FAILED test_rotate_self_writes_record_with_five_observations
FAILED test_rotate_self_refuses_when_successor_window_absent
FAILED test_rotate_self_refuses_when_predecessor_window_gone
FAILED test_loop_writes_durable_record
4 failed, 47 deselected
```
**GREEN** after (`extensions/agi/tests/test_rotate.py`): `51 passed`.
Full repo suite: `2071 passed, 1 skipped`.

**Live throwaway rehearsal (success, ROTATE_EXIT=0)** — scratch session
`agi-rh-l339`, throwaway seat `rh`, stand-in successor that writes a fresh
`continue` post-cursor then STAYS alive (a real claude successor does not
close its window on exit); a stale `continue` was seeded in the successor log
before spawn:
```
(1) handoff -> .agi/sessions/seats/rh.handoff.md generation 1
(2) rename own window 'rh' -> 'rh.gen1'
(3) spawn successor under the plain name 'rh' (role 'parent')
(7) successor confirmed `continue`; killed own window 'rh.gen1'
rotation recorded: /tmp/rh-graph-l339/.agi/sessions/rotations/rh.20260908T021010Z.json
```
`tmux list-windows` after rotation showed `rh.gen1` AND `rh` (successor), and
the record captured all five observations, incl. `d_stale_continue_cursor`
`start_offset: 9` (the seeded stale line, refused in favour of the post-cursor
fresh `continue`). The record file survived and was copied to
`.agi/sessions/rotations/`.

**Live refusal (REFUSE_EXIT=1)** — scratch session `agi-rh-l339b`, stand-in
that answers then EXITS (closing its window):
```
ERR: successor window 'rh' is NOT present in tmux session 'agi-rh-l339b'; refusing to report rotation success (windows: ['bash', 'rh.gen1']).
```
The objection record wrote `result: "refused" / refusal_reason: "successor window absent"`.

Scratch sessions/stand-ins cleaned up; all 10 `belam-S1-L3*` windows intact.

## Agent Notes
Built and proved both halves: durable self-written rotation records
under `.agi/sessions/rotations/` (committed via a precise gitignore
un-ignore), and predecessor-survival + successor-presence as hard refusals.
All constraints honoured: seats.md, cli.py, meter measure, real seeds and
belam windows untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-9bd9ebe6, L3.39): ACCEPTED as proved. Read the artifact, not just the report: rotate.py now derives window presence only via _observed_windows() (tmux list-windows, never spawn return value), writes per-rotation JSON records under .agi/sessions/rotations/ capturing all five observations (a-e), and both rotate-self and loop refuse non-zero with a result:"refused" record when the successor window is absent or the renamed predecessor window is gone — success record written before the own-window kill, so evidence survives cleanup. Verified independently: 51/51 rotate tests green, both delivered record files parse and carry observations (a)-(e) incl. the stale-continue cursor start_offset, gitignore un-ignore is correctly scoped (only rotations/ committed, iter logs stay ignored), constraints honoured (seats.md/cli.py/meter/belam windows untouched). Verdict stands at proved; no demotion.
<!-- THOUGHT:END -->

Review summary (parent a00-9bd9ebe6): parents link resolves to hypothesis:l3-rotation-record-and-predecessor-guarantee (exists); verdict proved backed by evidence_runs list pointing at this node plus committed record files and red-first test output reproduced independently (51 passed). Accepted, no demotion.
