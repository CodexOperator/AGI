---
id: experiment:a00-c258cfe9-012dfb
mint_id: 20cdaaeddb1d42a1b4225ecee04c057a
type: experiment
parents:
  - hypothesis:l4-the-sensei-audit-verbs-write-their-result-into-the-rotation-record-and-name-a-finding-only-over-the-floor
next_edges: []
confidence: 0.9
edited_by: a00-747119ec
evidence_runs:
  - experiment:a00-c258cfe9-012dfb
loop: hypothesis:l4-the-sensei-audit-verbs-write-their-result-into-the-rotation-record-and-name-a-finding-only-over-the-floor@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "live corpus: json.dumps(json.loads(raw),indent=2)+chr(10)==raw over .agi/sessions/rotations/*.json (minus sequence.json)", "expected": "every rotation record round-trips byte-identically -- the write-back's precondition", "observed": "150/150 identical, 0 differ", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "pytest test_wake_audit_rerun_replaces_its_side_and_never_grows", "expected": "a re-run replaces audit.wake; the record never grows or duplicates a side", "observed": "passed (record identical modulo audited_at; audit.wake is an object)", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "sensei.py rotate-out-audit --post master-sensei --no-record; grep -l '\"audit\"' .agi/sessions/rotations/*.json | wc -l", "expected": "--no-record writes nothing: 0 records carry an audit key", "observed": "0 (0 before the probe; unchanged)", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "pytest test_wake_zero_calls_prints_green_and_excess_zero", "expected": "excess 0 prints 'green <post> wake --record <stamp> 0 (floor 0)' and no FINDING", "observed": "passed", "result": "held"}
  - {"conjunct": 2, "class": "auth", "cmd": "pytest test_wake_audit_never_sends_a_dm (monkeypatch _send.send_dm/send_room to raise)", "expected": "the verb names the finding; the dm to the Prime stays a Sensei act", "observed": "returned 0 with the FINDING line; no send call reached", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "pytest test_rotate_status_prints_the_audit_key_from_the_record (rotate.cmd_status on the tmp record)", "expected": "rotate.py status --post S --record latest shows the audit key with NO rotate.py change", "observed": "passed: \"audit\", \"wake\" and \"floor\": 0 in stdout", "result": "held"}
profile: balanced
push_further: "Make the audit run without a hand call: have the rotate/closeout wrapper invoke the verb so a real rotation's record carries audit.out/audit.wake by construction, and assert rotate.py status renders it after an actual rotate-self rather than a tmp fixture."
role: kid
scaffold_hash: 136ee778e15ea584
season: 2
title: A00 c258cfe9 012dfb
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c258cfe9-012dfb

## Experiment

BUILD round (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement):
the target's `testable_claim` is a spec, so this kid measured the PRE-fix
state, implemented the claim in `extensions/agi/bin/sensei.py` (+ its tests),
then proved it on the built bytes. `rotate.py` untouched.

### Pre-fix measurement (this checkout, 2026-09-16)

- `grep -l '"audit"' .agi/sessions/rotations/*.json | wc -l` -> **0**. No
  rotation record carried an audit key; `cmd_wake_audit` / `cmd_rotate_out_
  audit` classified and printed only, writing nothing.
- The write-back's byte-preservation precondition was measured over the live
  corpus BEFORE touching anything: for every `*.json` under
  `.agi/sessions/rotations` (excluding `sequence.json`, which is not a
  rotation record), `json.dumps(json.loads(raw), indent=2) + "\n" == raw`
  held **150/150**. That is the exact call `rotate.py` writes records with
  (rotate.py:4566,5304), so a parse/re-dump of an untouched record is
  byte-preserving and an `audit` key appended last changes no other byte.

### What was built

`sensei.py`:

- Constants `AUDIT_FLOOR = {"wake": 0, "out": 1}` (one dict, one reader) and
  `AUDIT_SIDES`, plus three helpers:
  - `audit_payload(side, calls, counts, transcript, window_start, window_end)`
    -> the `{calls, a, b, c, d, floor, excess, transcript, window_start,
    window_end, audited_at, audited_by}` payload;
  - `audit_finding_line(seat, side, record_stamp, calls, floor)` -> the one
    printed line: `green <post> <side> --record <stamp> <calls> (floor N)` at
    excess 0, else `FINDING <post> <side> --record <stamp> excess <n> over
    floor <N>`;
  - `write_audit_into_record(rec_path, side, payload)` -> read-modify-write of
    the ONE top-level `audit` key (`json.dumps(rec, indent=2) + "\n"`), which
    is byte-preserving for every other key and idempotent on a re-run;
  - `finish_audit(...)` -> writes (unless `--no-record`) and returns the line.
- `wake_audit` now carries the write-back identity on its returned `counts`
  under private keys (`_record_path`, `_transcript`, `_calls`,
  `_window_start`, `_window_end`); `rotate_out_audit` carries
  `window['record_path']`. **The record PATH the audit itself read is the one
  that is written** - never a second selector call that could name a
  different record.
- `cmd_wake_audit` / `cmd_rotate_out_audit` call `finish_audit` and print the
  line; both subparsers gained `--no-record` (dry read, write nothing).
- The verbs send NO dm: the dm to the Prime on a finding stays a Sensei act.

Existing fixtures that call the pure `wake_audit` / `rotate_out_audit`
functions or `_cats(counts)` are unaffected (private keys; error paths still
return `{}`).

### Judgement call (documented deviation)

The claim fixes the floors and the field list but not what `calls` counts.
This build defines `calls` = the number of tool_use calls INSIDE the audit
window (the same number the printed line reports), and `excess =
max(0, calls - floor)`. The alternative - counting only category (d) - is not
named anywhere in the claim, and a second count would let the record and the
line disagree; one count, one reader.

## Evidence

New test file: `extensions/agi/tests/test_sensei_audit_record_writeback.py`
(14 tests) - tmp projects, synthetic transcripts, records written in
rotate.py's canonical byte form. Sensei suite (6 files: `test_sensei.py`,
`test_sensei_audit_record_window.py`, `test_sensei_rotate_out_audit.py`,
`test_sensei_wake_audit.py`, `test_sensei_audit_record_writeback.py`,
`test_write_master_sensei.py`):

    python3 -m pytest extensions/agi/tests/test_sensei.py \
      extensions/agi/tests/test_sensei_audit_record_window.py \
      extensions/agi/tests/test_sensei_rotate_out_audit.py \
      extensions/agi/tests/test_sensei_wake_audit.py \
      extensions/agi/tests/test_sensei_audit_record_writeback.py \
      extensions/agi/tests/test_write_master_sensei.py -q
    -> 179 passed, 8 warnings in 1.25s

Falsifiers held (one per conjunct), each an assertion in that file that
fails if the built bytes are wrong:

- **no byte outside `audit`** - compared twice: parsed (JSON with `audit`
  popped equals the original parsed record) and RAW (`re.sub` removing the
  `audit` block from the rewritten text reproduces the original bytes
  exactly; the regex must match, so a reformat cannot pass silently).
- **a re-run never grows the record** - `audit.wake` is an OBJECT, the record
  length is unchanged modulo the timestamp, and both sides survive.
- **a wake with excess 0 prints green** - `green sanctuary-director wake
  --record 20260911T120000Z 0 (floor 0)`, and `FINDING` is absent.
- **`--no-record` writes nothing** - bytes before == bytes after.
- **every printed line names the record stamp** - `--record <STAMP>` in the
  green and FINDING lines, no generation; and the live CLI probe below.
- **no dm** - `_send.send_dm` / `_send.send_room` monkeypatched to raise; the
  verb still returns 0 and prints FINDING.
- **`rotate.py status --post S --record latest` shows the audit key** -
  `rotate.cmd_status` renders the raw record text (rotate.py:3080-3084), so
  the key falls out with NO rotate.py change; the test asserts `"audit"`,
  `"wake"` and `"floor": 0` appear in that output.

Live CLI probe (this checkout, `--no-record` so nothing in the live graph was
written):

    $ python3 extensions/agi/bin/sensei.py rotate-out-audit \
        --post master-sensei --no-record
    ...
    FINDING master-sensei out --record 20260916T105216Z excess 4 over floor 1

    $ python3 extensions/agi/bin/sensei.py wake-audit \
        --post master-sensei --no-record
    ...
    FINDING master-sensei wake --record 20260916T105216Z excess 6 over floor 0

    $ grep -l '"audit"' .agi/sessions/rotations/*.json | wc -l
    0        # --no-record wrote nothing; the live corpus still has no audit key

Conjunct 3's live read (`rotate.py status --post master-sensei --record
latest`) is exercised in the test against the tmp record; running it live
would be the same code path and would mutate no file.

## Probes

One parent-run negative probe per claim conjunct, each actually run (class
auth/gate/wire), recorded in this node's `probes` frontmatter by `cli.py
done`.

<!-- THOUGHT:BEGIN - authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Built, not measured. The write-back was placed in the `cmd_*` bodies rather
than inside `wake_audit` / `rotate_out_audit` on purpose: the pure functions
keep returning `(code, rows, counts[, window])` so every existing audit test
and any caller that only wants the classification is untouched, and the write
happens exactly once per verb invocation. The record path travels on the
return value (private keys on `counts`, `window['record_path']` on the
rotate-out side) because re-resolving the record a second time could name a
different one - the same ONE-call-site rule the record stamp already follows.
The byte-preservation claim rests on `rotate.py`'s canonical writer, which was
MEASURED over all 150 live records before the first edit (150/150 identical),
not assumed. Deviation recorded in the node body: `calls` = windowed call
count, one number shared by the record and the printed line.
<!-- THOUGHT:END -->

<!-- BODY:END -->

## Agent Notes
Built the claim in sensei.py: both audit verbs write an audit key into the audited rotation record (read-modify-write of that key only, byte-preserving on all 150 live records), print green/FINDING naming the record stamp, --no-record opts out, and no dm is sent. 14 new tests + 179 sensei-suite tests pass.

PARENT SL7.133 review: ACCEPT, kid verdict kept proved. Read the staged diff (sensei.py: AUDIT_FLOOR {wake:0,out:1}, audit_payload/audit_finding_line/write_audit_into_record/finish_audit, --no-record on both subparsers; +14 tests), never the result file. Ran 4 parent negative probes, one per claim conjunct, all HOLD: (1) auth — rotate-out-audit --post no-such-seat refused rc 2 ERR: no seat row, zero bytes written; (2) gate — re-run replaces audit.wake only, a seeded audit.out survives, no byte outside audit changes, --no-record byte-identical; (3) gate — 1-call wake prints FINDING ... excess 1 over floor 0 (never green), 0-call wake prints green ... (floor 0), rc 0, no dm; (4) wire — real sensei.py write lands on disk and real rotate.py status --post S --record latest prints the audit key + floor. Full engine suite 5012 passed, 15 skipped. rotate.py untouched. Scope: sensei.py + tests only.
