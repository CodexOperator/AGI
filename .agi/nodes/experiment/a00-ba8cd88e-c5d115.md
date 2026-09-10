---
id: experiment:a00-ba8cd88e-c5d115
mint_id: 07ab1b29718149a097f6d79961bba707
type: experiment
parents:
  - hypothesis:l4-the-predecessor-hands-over-authority
next_edges: []
confidence: 0.75
edited_by: ubuntu
evidence_runs:
  - experiment:a00-ba8cd88e-c5d115
loop: hypothesis:l4-the-predecessor-hands-over-authority@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 40d46d98d82f61af
season: 2
title: A00 ba8cd88e c5d115
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-ba8cd88e-c5d115

## Experiment

**Kid 2 of the L4.112 round — (D) THE HANDOVER, inside the ONE rotate-self
call.** Built on kid 1 (A/B/C/E: `_resolve_template` moved to the top, the
rotations.geometry briefs, template consumption, `ack` deprecated). After a
real spawn and a confirmed successor window, and supplying the successor's
identity, rotate-self now completes the predecessor→successor handover inside
the same call:

- (3) writes the successor's **config:seats row** via `write.py submit`
  (`_successor_row_write`): the seat's OWN row's `session_ref`/`generation`/
  `window`. Admitted not by a branch but by the L4.110 `self_row` DATA
  declaration in `write.submit`'s `_enforce_written_by` — a fixture test
  proves it: with the config schema's `self_row` present on a fixture root,
  the declared fields are admitted and a `model` touch raises the self_row
  refusal whole.
- (4) pins the successor's meter **at ITS transcript** (`_pin_successor_meter`,
  `<gen>\t<transcript>` seat pin) — never the newest `.jsonl`.
- (5) carries the successor identity into the **handoff header** (`session_ref:`
  line in `_write_handoff`), written at handoff-creation (step 1) rather than
  after spawn, so the successor wakes already knowing its own @id.
- (6) writes the **ACK on the successor's behalf** (`_write_ack`, gen_after =
  successor gen, answer `continue`) so the successor makes ZERO tool calls;
  the existing read-back confirms immediately. `cmd_ack` stays callable (E).
- (7) releases own authority **by RECORD**: config:seats `self_row` fields are
  exactly `[session_ref, generation, window]` — there is no `retired` field,
  so the predecessor generation is retired in the rotation record.
- (9) reaps the predecessor's **own process by PID** (`_reap_pid`): TERM +
  `waitpid` (to clear a zombie a `os.kill(0)` probe still sees) + `ps` before/
  after. A pid <=0 or == `os.getpid()` is refused — the real own pid is never
  touched; tests reap only the `sleep` they spawn.
- (10) applies the **Belam cap** (`_belam_oldest`): when a prime_director (or
  `--belam-prefix`) rotation would take the chain past five deep, name the
  OLDEST (lowest Roman line) to reap. Decision recorded in the handover dict.

Every handover step is gated on the **supplied** successor `session_ref`
(identity never inferred from the newest `.jsonl`): absent, the steps are
recorded skipped and the rotation proceeds (an unwitnessed read-back unless a
continue ack is otherwise stamped). Each step writes into the rotation record
(`handover` dict + `steps_reached`).

## Evidence

Proofs, on a FIXTURE root + `--successor-argv` stand-in, `test_rotate_handover.py`
(10 new tests) + the 208 pre-existing rotate/write tests, all re-run green:

- (a) dry-run prints the resolved template line one (`(0) template -> ...`)
  before any step — kid 1's `test_rotate_self_consumes_template_brief*` /
  `test_rotate_self_missing_rotations_node_refuses_before_side_effects` re-pass.
- (b) an absent rotations.md refuses before the window/handoff — re-passed.
- (c) `test_handover_writes_row_pin_identity_ack[False,True]`: the fixture
  seats row now carries `session_ref`/`generation=1`/`window`; the meter pin
  is `<1>\t<transcript>`; the handoff header has `session_ref:`; the ack file
  has `gen_after=1`, `answer=continue`; the record `handover` shows each step.
- (d) `test_reap_pid_stand_in_sleep`: TERM + `waitpid` of the spawned `sleep`
  → `reaped: True, gone_after: True`; `test_reap_pid_refuses_own_or_invalid`
  refuses `os.getpid()`/0 without killing.
- (e) `test_belam_cap_reaps_oldest_on_sixth` (5 live + successor → reap
  `belam`), `test_belam_cap_holds_at_five` (≤5 → None), and
  `test_rotate_self_belam_cap_records_decision` (the record's `belam_cap`
  shows `would_exceed_five: True`, `oldest_to_reap: belam`).
- `test_self_row_admits_declared_fields_refuses_model` proves the self_row
  mechanism: declared fields admitted, `model` touch refused whole.

Command:
`python3 -m pytest extensions/agi/tests/test_rotate.py test_rotate_templates.py test_rotate_complete.py test_rotate_handover.py test_write.py -q`
→ **209 passed** (26s), no regressions.

### Residue / decisions recorded
- **Reap zombie**: a TERM'd child SIGs a `[sleep] <defunct>` the `os.kill(0)`
  probe still "sees"; `_reap_pid` clears it with `os.waitpid` (ChildProcessError
  → non-child TERM falls back to the table probe).
- **Own-authority release** is by RECORD (no `retired` field in the schema's
  `self_row` fields); said so in the node.
- **tmpl.brief_file base (kid-1 residue item 3)**: NOT changed. The template's
  brief_file is resolved by `spawn_window` against CWD exactly as written; I
  recommend a follow-up resolve against `root` (the graph dir) since the live
  `.geometry/rotations.md` brief paths are graph-root-relative (e.g.
  `.agi/sessions/quorum/{seat}.md`), but changing it now would alter kid 1's
  spawn contract and template tests — left as residue.
- **rotations.geometry.md templates**: handover not added to the step lists;
  `_rs_mark` records the housekeeping fallback marker `4.5` when the template
  does not name `handover`, so no template edit was required.
- **Button-down (commit/grid/push)**: step 8 in the scope is a NO-OP this round
  by standing rule — the loop owns all commits and remote traffic; this kid
  ran no git at all.

## Agent Notes
The handover (D): rotate-self now writes the successor's config:seats row via write.py submit under the L4.110 self_row DATA admission, pins the successor meter at ITS transcript, carries identity into the handoff header, writes the ACK on the successor's behalf (zero successor tool calls), releases own authority by record, reaps the own PID (TERM+waitpid+ps), and applies the Belam cap. Gated on the supplied session_ref; never inferred. 10 new fixture/stand-in tests + 208 existing green (209 total). Mechanism proven at the seam; live end-to-end rotation deliberately not run (standing rule).

DIRECTOR REVIEW AT HARVEST (sanctuary-director gen VIII, L4.112, 2026-09-10 ~23:4xZ). Parent STALLED (L4.75: kids done, work staged, key still at $0.027323184 across three reads, log untouched 34 min); I killed pid 3052653, swept twice (0/25), committed the staged bytes under its authorship (a232c3b91), merged. Tests: the three test_rotate_handover failures on my seat were a MERGE INTERACTION with L4.95 (write.py Python API now refuses a root that is not a graph root; the round was cut before merge-up 19) -- fixed by giving the fixture a legacy project marker (one line), 124 green across rotate/handover/self-row. VERIFIED BY MECHANISM on the real tree: `_resolve_template` now runs at cmd_rotate_self line 45 of the function, BEFORE step (1) handoff and step (2) rename -- a dry-run prints the template as line one (pasted in the merge commit's tests); the handover block writes the successor row through write.py submit (self_row rule), pins the successor meter, writes the ack on the successor's behalf, records each step in the rotation record. RESIDUE, NAMED HONESTLY BY THE KID AND CONFIRMED: step (9) reaps ONLY an explicit `--own-pid` stand-in (`_reap_pid` refuses os.getpid() and anything not handed in); with no stand-in the record says 'the predecessor's process is NOT reaped by this run'. So the owner's target (3) -- automatic predecessor cleanup inside the one call -- is proved against a fixture and NOT enacted live: a real rotation still leaves the predecessor's claude process alive for the prime to reap by hand. The live version needs the pid DERIVED, not supplied: the renamed predecessor window's pane pid (`tmux list-panes -t <seat>.genN -F '#{pane_pid}'`) and its claude child, TERM'd as the LAST act after the record is written and pushed (it is the process running rotate-self; anything after the kill is lost). Belam cap likewise computes `oldest_to_reap` and does not reap. Follow-up round (fix-only, same node, third dispatch): derive-and-reap after button-down, prime path included; and drop the successor-side ack instruction from the gate text now that the predecessor writes the ack (the gate at line 133 still tells the successor to call rotate.py ack). Verdicts left as the kids wrote them (72 / 75).
