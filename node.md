---
id: experiment:a00-183e23e5-066193
mint_id: 545fb0f7f1de4964b17f06246115564c
type: experiment
parents:
  - hypothesis:a-captive-capture-rotates-even-when-its-driven-handoff-refuses
next_edges: []
confidence: 0.9
edited_by: a00-183ce225
evidence_runs:
  - experiment:a00-183e23e5-066193
loop: hypothesis:a-captive-capture-rotates-even-when-its-driven-handoff-refuses@s2
model: stealth/space-bunny-alpha
probes:
  - "WIRE conjunct 1: the hook's own _force_capture imported from a COPY of extensions/agi whose bin/rotate.py is a stand-in (handoff exits 1 with the 100-line guard message, rotate-self records its argv), real bash chain, tmp state_dir, no monkeypatch -> rotate-self stand-in IS invoked after the refusing handoff, marker reads 'handoff rc=1', chain log holds the guard error."
  - "WIRE conjunct 1b: the stand-in rotate-self ALSO refusing (rc=3) -> marker reads 'handoff rc=1' AND 'rotate-self rc=3'; the chain never aborts and names BOTH steps."
  - "WIRE conjunct 2: the hook main() as a SUBPROCESS with AGI_* stripped from env -> stdout carries one 'capture-chain step FAILED: handoff rc=1' line, the marker is gone afterwards, [meter] stays LAST, the NEXT check is silent. NOTE: without the strip, the parent session's AGI_PROJECT_ROOT/AGI_SEAT re-root the hook at the REAL worktree and the probe reads zero lines - that was my probe's defect, not the engine's."
  - "GATE: AGI_HOOK_NO_SPAWN=1 still returns capture-no-spawn and spawns nothing (rotate log never created)."
  - "GATE: a ladder with no capture_chain_log cell still returns capture-no-log before any write."
  - "GATE: the real rotate.py never ran - the hook resolved parents[1]/bin inside the COPY, whose stand-in carries the guard string."
production_lines: 54
profile: balanced
role: kid
scaffold_hash: f0e3e5f51ef3b1be
season: 2
title: the capture chain rotates after a refusing handoff and names the failed step to the seat
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-183e23e5-066193

## What was built

Two conjuncts, one diff, `extensions/agi/hooks/rotation_alert.py` (+54 / -10 production lines).

| conjunct | before | after |
|---|---|---|
| rotate anyway | `n=$1; shift; a=("$@"); "${a[@]:0:$n}" && "${a[@]:$n}"` | `_CHAIN_SCRIPT`: both steps run SEQUENTIALLY, each rc checked |
| name the failure | nothing but `capture-chain.log` | chain appends `<step> rc=<n>` to `capture-<seat>.failed`; `_chain_failure_note(state_dir, seat)` prints ONE line per failed step on the hook's NEXT check and CLEARS the marker |

- `_spawn_capture_chain(fail, chain_log, handoff_argv, rotate_argv)` — the ONE background child (P7: the child waits, the hook never blocks). Argvs still positional: `$1` = failure marker, `$2` = handoff length, `$3..` = the two argvs. handoff BEFORE rotate-self is unchanged, so rotate-self still reads the card handoff wrote.
- Mechanism chosen: (a), the state_dir marker — no new process on the failure path, so P7 is untouched and a `bin/send.py` dm (whose argv would carry the seat) is not needed.
- The marker name is a SIBLING state file (`capture-<seat>.failed`), the same shape as the existing `capture-<seat>.json/.s3/.captured` — no new ladder cell, no new path literal, `paths.py audit` gains no hit.
- `AGI_HOOK_NO_SPAWN` still returns `capture-no-spawn` before the spawn; the fail-closed `capture-no-log` still returns before anything is written. Unchanged bytes, and their tests still pass.

## BEFORE (unmodified tree) — the failing probe

`env -u TMUX -u TMUX_PANE python3 .agi/sessions/iter-DH.391/a00-183e23e5/probe_capture_chain.py`
runs the chain's OWN spawn (script read out of the live bytes) with STAND-IN argvs
(`python3 -c ... sys.exit(1)` as the handoff; a `python3 -c` that touches a file as rotate-self):

```
PROBE 1 — refusing handoff, then rotate-self stand-in
  chain script      : n=$1; shift; a=("$@"); "${a[@]:0:$n}" && "${a[@]:$n}"
  rotate-self ran?  : False          <-- the `&&` SKIPPED the rotation
  failure marker    : (none)
  chain log         : (empty)
PROBE 2 check #1 rc=0 marker present=True
PROBE 2 check #2 rc=0 marker present=True
  line the seat read: (NONE)         <-- the seat read nothing, twice
  named step + rc?   : False
```

## AFTER (built bytes) — same probe, same stand-ins

```
PROBE 1 — refusing handoff, then rotate-self stand-in
  chain script      : f=$1; n=$2; shift 2; a=("$@"); "${a[@]:0:$n}"; c=$?; [ "$c" -eq 0 ] || printf "handoff rc=...
  rotate-self ran?  : True           <-- the seat rotates ANYWAY
  failure marker    : handoff rc=1
PROBE 2 check #1 rc=0 marker present=False
PROBE 2 check #2 rc=0 marker present=False
  line the seat read: ["rotation-alert: capture-chain step FAILED: rotate-self rc=1 — the captive
   capture's driven handoff/rotate-self chain did not complete; see the ladder's capture_chain_log
   for its output."]
  named step + rc?   : True
  second check repeats it?: False    <-- read exactly once, then cleared
  meter last        : True            <-- D1: the [meter] line stays LAST
```

PROBE 2 is the REAL hook as a SUBPROCESS (payload on stdin, `AGI_ROTATION_STATE_DIR` =
tmp), not a call into my own helper.

## probes:

- class **wire** (chain shape, real bash, real `python3 -c` stand-ins, tmp state dir):
  `env -u TMUX -u TMUX_PANE python3 .agi/sessions/iter-DH.391/a00-183e23e5/probe_capture_chain.py`
  — output above, before vs after.
- class **wire** (the seat's read path, hook run as a subprocess): same probe, PROBE 2.
- class **auth**: unchanged — nothing new is spawned on the failure path, and
  `AGI_HOOK_NO_SPAWN` still records into `_CAPTURE_LOGGED` and returns `capture-no-spawn`
  (asserted by the pre-existing `test_force_capture_after_n_minutes_records_argv`).
- class **gate**: the fail-closed `capture-no-log` refusal is still reachable before any
  write (pre-existing `test_capture_fails_closed_when_the_ladder_declares_no_log_cell`).

## Tests

`extensions/agi/tests/test_rotation_alert_capture.py`:
- `test_capture_is_one_ordered_child_handoff_then_rotate_self` — REWRITTEN: it asserted
  `"&&" in argv[2]`, which is the defect itself. It now asserts the one child carries
  `_CHAIN_SCRIPT`, handoff-before-rotate-self ordering, `--stops`, and the marker as `$1`.
- `test_chain_rotates_even_after_a_refusing_handoff` — real bash, refusing handoff stand-in,
  rotate-self stand-in still invoked, marker reads `handoff rc=1`.
- `test_chain_leaves_no_marker_when_both_steps_succeed` — success path unchanged, no marker.
- `test_a_failed_step_is_named_to_the_seat_and_cleared` — a planted marker produces exactly
  ONE line naming step + rc, the marker is gone, the meter stays last, and a second check
  is silent.

```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_rotation_alert_capture.py \
    extensions/agi/tests/test_rotation_alert_capture_safety.py -q   -> 19 passed
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests -k "rotation_alert or capture" -q
    -> 116 passed, 1 skipped, 6570 deselected   (parent baseline 113 passed, 1 skipped)
```

## Guards held

No test or probe runs the real `rotate.py handoff` / `rotate-self`; nothing wrote under the
real `/tmp/agi-rotation-<uid>` (tmp state dir only, `AGI_ROTATION_STATE_DIR`); no git; no
`grid.py`. Production lines measured with the one allowed `git diff --numstat`:
`54  10  extensions/agi/hooks/rotation_alert.py` (ceiling 40, under the 80 stop line; no
re-brief requested).

## Agent Notes
capture chain now runs rotate-self after a refusing handoff (sequential, rc-checked) and names a non-zero step+rc to the seat on the next check; before/after wire probes + 116 passed selector

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-183ce225, iter DH.391) — ACCEPTED as proved on my own probes. (1) WHAT THE BRIEF SAID: "rotate anyway on a refusing handoff" + "any non-zero chain step leaves ONE line the seat READS, naming the step AND its rc". (2) WHAT THE MACHINE ACTUALLY DOES: rotation_alert.py _CHAIN_SCRIPT (L824-830) replaced the single `"${a[@]:0:$n}" && "${a[@]:$n}"` with two sequential steps, each rc tested and appended as `<step> rc=<n>` to the sibling marker capture-<seat>.failed; _chain_failure_note (L842) reads+unlinks it and main (L1468) prints one line per failed step BEFORE _meter, so the [meter] line stays last and the note prints even when the stamp has latched. I drove the built bytes, not the prose: probe output in the probes field — rotate-self stand-in invoked after a handoff that exits 1; marker "handoff rc=1" then "rotate-self rc=3" when both refuse; the hook subprocess printing the line once and clearing it; capture-no-spawn and capture-no-log both still refusing. (3) THE NEAR MISS: a `;` that runs rotate-self but keeps no rc would satisfy conjunct 1 and lose conjunct 2 entirely - the seat would rotate and never learn why the card was not written; the note placed AFTER the latch return (or after the seen==0 early return) would satisfy "prints one line" in a test that plants the marker on a live check and lose the live case, because the marker is written by a DETACHED child that finishes after the hook returns. (4) DEVIATION: none. WEAKNESS CARRIED (a caveat, not a demotion): the note block sits below the `seen == 0` turn-1 early return, so on the FIRST turn of a session the line is deferred, not lost; and the marker is a /tmp file, so a reboot between the failed chain and the next check loses the name (the ladder log still has it). Neither falsifier in the hypothesis is met.
<!-- THOUGHT:END -->
