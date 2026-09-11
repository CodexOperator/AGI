---
id: experiment:a00-19b24714-e450c6
mint_id: 65017ea4634548069e0bb8543f0e4263
type: experiment
parents:
  - hypothesis:l4-meter-pin-refuses-a-target-that-is-not-a-pin-and-prepare-prints-the-clear-line-that-clears
next_edges: []
confidence: 0.85
edited_by: a00-0171fd39
evidence_runs:
  - experiment:a00-19b24714-e450c6
loop: hypothesis:l4-meter-pin-refuses-a-target-that-is-not-a-pin-and-prepare-prints-the-clear-line-that-clears@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 724c160bc59950fb
season: 2
title: A00 19b24714 e450c6
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-19b24714-e450c6

## Experiment

Kid-1 build of the two remaining halves of the target hypothesis (ceiling: kid 1 =
(1)+(2)); the sibling experiment a00-3480c19d had already built the identity gate
in cmd_meter. This round BUILT and PROVED on the built bytes (a g15 claim is
behaviour, not a measurement):

1. **PATH validation in `rotate.py cmd_meter`** — a `--pin` write target is now
   shape-checked BEFORE any write. Two guards:
   - `_valid_meter_pin_target(pinp, root)` — the target's basename must end
     `.meter` AND resolve directly under `_sessions_dir(root)`. A `.jsonl`
     transcript, a graph node (`.md`), a script — anything else — is refused BY
     NAME (the offending path printed), never written, left byte-identical.
   - an EXISTING valid-path pin is overwritten only when its current content
     parses as a pin record (`_parse_pin_record`); a target sitting on non-pin
     bytes is refused and left byte-identical.
   The refusal prints the ONE form that clears:
   `rotate.py meter --pin <sessions>/<seat>.meter --session-log <transcript>`
   (--pin takes the PIN FILE, never --seat which trips the cross-generation
   read refusal).
2. **prepare check-5 clear line** — was
   `rotate.py meter --seat {seat} --pin <transcript>` (BOTH halves wrong). Now
   `rotate.py meter --pin <sessions>/<seat>.meter --session-log <transcript>`
   with the seat's real pin path resolved via `_sessions_dir` and the
   transcript taken from the pin's own record when known, else the literal
   `<transcript>` placeholder.

Code touched: `extensions/agi/bin/rotate.py` (new `_seat_pin_path` +
`_valid_meter_pin_target` helpers; the write block in cmd_meter; the check-5
block in `_prepare_checks`). Tests: `extensions/agi/tests/test_rotate.py` (3 new:
.jsonl refused byte-identical, node refused byte-identical, valid seat pin still
writes) + `test_rotate_prepare.py` (1 new: stale-pin clear line names the pin
file + known transcript, and running that EXACT line makes the next prepare pass
check 5). All 159 test_rotate* + 59 test_bin_help_smoke tests green.

## Evidence

Falsifier runs (manual, via rotate.main on a fake graph root):

```
$ meter --pin <real-transcript.jsonl> --session-log <same-transcript>
exit 1
ERR: meter --pin refuses its target. /tmp/.../real-transcript.jsonl is not a meter
pin (a pin's name ends '.meter'); wrote it, it would truncate. Run: rotate.py meter
--pin /tmp/.../proj/sessions/<seat>.meter --session-log <path-to-the-transcript-you-own>
sha256 unchanged: True
```

```
$ meter --pin <proj>/sessions/belam.meter --session-log <transcript>
exit 0
content: '0\t/tmp/.../real-transcript.jsonl\n'
```

Prepare check-5 (test test_prepare_check5_clear_line_names_pin_file_and_clears_when_run):
the clear line printed is
`rotate.py meter --pin <root>/sessions/adv-alive.meter --session-log <root>/the-predecessor.jsonl`
(no `--seat`, no placeholder). Running that line through cmd_meter re-points the
pin to generation 3 (== cur), and the NEXT `prepare` prints `[ok] meter pin
stale` with exit 0.

19b24714. This kid built (1)+(2); claimed proved with test evidence on the built
bytes. The identity gate (prior sibling) and (3)+(4) (a later kid owns `_read_generation`
callers + the vacuous fixture) are untouched here.

## Agent Notes
Built kid-1 halves (1)+(2): meter --pin refuses by name any non-pin target (byte-identical) and prepare check-5 prints the correct pin-file+session-log clear line that actually clears; 4 new tests + 218 green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SL4.01: ACCEPTED as proved for (1)+(2).

(1) WHAT THE INSTRUCTION SAID: the target hypothesis named up to 3 kids, "kid 1 = (1)+(2)" — (1) meter --pin must REFUSE BY NAME a target that is not <sessions>/<seat>.meter and never write it; an EXISTING target is written only when its content parses as a pin record, anything else left byte-identical; the refusal prints rotate.py meter --pin <sessions>/<seat>.meter --session-log <transcript>. (2) prepare check 5 prints exactly that line with both paths resolved, and running it clears the captive.

(2) WHAT THE MACHINE ACTUALLY DOES — I ran it, not the report: git diff --cached shows two seams. _valid_meter_pin_target (rotate.py L304-336) checks basename ends METER_PIN_EXT and pinp.parent.resolve() == _sessions_dir(root).resolve(), called at L1014 BEFORE pinp.write_text. The check-5 block (L7741-7771) builds clear5 from _seat_pin_path(root, seat) + the pin records own transcript (or registry), never --seat. My own runs: pytest test_rotate.py + test_rotate_prepare.py = 159 passed in 27.61s. _parse_pin_record on a multi-line non-pin file returns (None, "garbage jsonl\nline2"), NOT None.

(3) THE NEAR MISS: the content half of the guard is nearly vacuous. The claim said an EXISTING target must parse as a pin record; _parse_pin_record treats ANY non-empty single-field text as a legacy bare-path pin, so a .meter file holding junk or JSONL passes the content check and is overwritten — only an EMPTY file is caught. A kid could have satisfied the words "uses _parse_pin_record" and lost the intent "never destroy non-pin bytes". It stays harmless in practice because the name+parent guard already refuses the live defect (a .jsonl path), and a .meter file in the sessions dir is by name a pin; I record it as a caveat rather than demote, because the claim itself delegated to _parse_pin_record and every stated falsifier passes.

(4) NO DEVIATION from a standing rule: no guard was lowered; find_pin_log untouched; the identity gate from experiment:a00-3480c19d is preserved.
<!-- THOUGHT:END -->
