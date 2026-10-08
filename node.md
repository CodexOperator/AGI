---
id: experiment:a00-b5a04026-970d8b
mint_id: 7e571cb2872c44f09df26bc420a70ed4
type: experiment
parents:
  - hypothesis:send-undelivered-notice-lands-in-the-comms-root
next_edges: []
confidence: 0.9
edited_by: a00-302e563b
evidence_runs:
  - experiment:a00-b5a04026-970d8b
line_ceiling: 40
loop: hypothesis:send-undelivered-notice-lands-in-the-comms-root@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "own probe .agi/sessions/iter-EF.12/a00-b5a04026/probe_wire.py on a tmp graph: stale deferred dm for busy seat director, then wake_all_local(root)", "expected": "the [undelivered] dm lands at comms_root(root)/dm/sender-a--wake-repair.md, is visible to read_dms(croot, sender-a), and a pre-fix-shaped send_dm(root,...) lands at <graph-root>/dm where no reader opens it", "observed": "exit 0, 6/6 PASS: comms-root dm present and read_dms sees it; the pre-fix shape lands at <graph-root>/dm and is invisible to read_dms(comms_root)", "result": "HOLD - the notice lands in the comms root a reader actually opens"}
  - {"conjunct": 2, "class": "gate", "cmd": "own probe probe_conjuncts.py: wrap send_mod.send_dm and drive _notify_undelivered(root, director, rec)", "expected": "the FIRST argument handed to send_dm is comms_root(root), never the graph root; the new test fixture (croot + seats under project/.agi) asserts via that same path, so the old fixture passing the graph root as a comms root could never have caught the defect", "observed": "exit 0: croot passed == /tmp/.../project/.agi/comms/season-1 == comms_root(root), and != root", "result": "HOLD - call site de-conflated, and the old fixture shape demonstrably could not see it"}
  - {"conjunct": 3, "class": "wire", "cmd": "own probe probe_conjuncts.py: busy send_dm (registry busy, fake tmux) capturing stderr", "expected": "BOTH lines on the busy path: plain [undelivered-yet] director from _announce_nudge AND nudge: coalesced (pane busy (registry)) from _nudge_window", "observed": "exit 0: both lines present verbatim in the same stderr capture; test_busy_send_dm_keeps_its_coalesce_reason_diagnostic asserts the same pair", "result": "HOLD - disposition (b) measured: the coalesce diagnostic is KEPT alongside the plain line"}
  - {"conjunct": 1, "class": "wire", "by": "a00-302e563b", "cmd": "parent probe: python3 .../probe_r1_baseline.py re-run on the fixed bytes", "expected": "the [undelivered] dm exists at comms_root(root)/dm/sender-a--wake-repair.md and read_dms(croot,'sender-a') shows it; nothing at <graph-root>/dm", "observed": "exit 0; comms path exists=True, wrong path exists=False, read_dms returned 1 block carrying '[undelivered] director'", "result": "HOLD - notice lands in the comms root the reader opens"}
  - {"conjunct": 2, "class": "gate", "by": "a00-302e563b", "cmd": "parent probe: copy bin+tests to /tmp/probe-b, revert BOTH send.py hunks (send_dm(comms_root(root),..)->send_dm(root,..) and _announce_nudge(graph)->_announce_nudge(croot)), run pytest tests/test_send_undelivered.py -q", "expected": "the rewritten suite is RED against the pre-fix bytes -- the notice-path assertions cannot pass under the old conflation", "observed": "4 failed, 5 passed; test_stale_record_dms_the_sender_exactly_once and test_second_sender_to_a_busy_seat_is_notified_too both fail at `croot / 'dm' / ... .is_file()`", "result": "HOLD - fixture de-conflated; the test genuinely exercises the fix"}
  - {"conjunct": 3, "class": "wire", "by": "a00-302e563b", "cmd": "parent probe: python3 .../probe_c_conjunct3.py -- busy send_dm (registry busy, fake tmux window @246) capturing stderr", "expected": "BOTH the plain '[undelivered-yet] director' line and the 'nudge: coalesced (pane busy (registry))' diagnostic in one capture", "observed": "exit 0; both lines present verbatim in the same stderr capture", "result": "HOLD - disposition (b) confirmed; the l5 claim's 'line is gone' reading is false on the bytes"}
production_lines: 16
profile: balanced
role: kid
scaffold_hash: ff1055de05602414
season: 2
title: send.py [undelivered] notice lands in the comms root a reader sees (verified the a00-988fbdeb bytes)
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b5a04026-970d8b

## Experiment

This is a VERIFY-and-attest round, not a build round. The source fix and the
test rewrite were produced by the prior attempt **a00-988fbdeb**, which died
on an upstream provider error ("The model stopped before completing the
response") before it reported. The bytes are in the working tree; this node
verifies them on the actual bytes and records the evidence. Credit for the
delta belongs to a00-988fbdeb.

### 1. The bytes (read with `git diff`)

`extensions/agi/bin/send.py` — 14 added / 2 removed, two hunks:

- `_notify_undelivered` now calls
  `send_dm(comms_root(root), "wake-repair", ...)` instead of `send_dm(root, ...)`.
  `root` remains the GRAPH root the deferred-sidecar and comms-config readers
  need; only the dm destination becomes the comms root every other `send_dm`
  caller uses.
- `send_dm` now calls
  `_announce_nudge(locations.find_project_root(croot) or croot, other, ok)`
  instead of `_announce_nudge(croot, other, ok)`, so the SEATS-row reader and
  comms-config reader see the graph root, matching `_nudge_window` one line
  above. Without this the plain `[undelivered-yet]` line vanished silently
  whenever the graph root was not reachable by a rebase (a test fixture, or
  any layout without a git common root).

`extensions/agi/tests/test_send_undelivered.py` — the `croot` fixture derives
`send_mod.comms_root(project)`; `_write_seats` writes under
`project/.agi/nodes/.geometry/` (the GRAPH root); direct `send_dm` calls pass
`croot`; the notice assertions read `croot / "dm" / ...`. One new test,
`test_busy_send_dm_keeps_its_coalesce_reason_diagnostic`, pins disposition (b)
— the busy path keeps BOTH the plain `[undelivered-yet]` line AND the
`nudge: coalesced (<reason>)` diagnostic.

The hypothesis node's `testable_claim` was rewritten (by the same attempt) to
the disposition-(b) text; the claim now matches the bytes rather than the
discarded "coalesce line is gone" reading.

### 2. Suites, on these bytes

```
python3 -m pytest extensions/agi/tests/test_send_undelivered.py -q
  -> 9 passed in 0.84s
python3 -m pytest extensions/agi/tests/test_send.py -q
  -> 330 passed, 11 warnings in 12.69s
```

### 3. Own wire probes (not the test file, not the parent's)

`probe_wire.py` — tmp graph root, seats row `director @246`, a deferred dm for
`director` stamped 2020 (aged past the threshold), then the real
`wake_all_local(root)` → `_notify_undelivered` → `send_dm` path with `wake`
forced to fail. **exit 0, 6/6 PASS**: the `[undelivered] director ... 'the
body'` notice lands at `comms_root(root)/dm/sender-a--wake-repair.md` and
`read_dms(croot, "sender-a")` prints it; a pre-fix-shaped `send_dm(root, ...)`
lands at `<root>/dm/sender-a--wake-repair.md` and is invisible to
`read_dms(comms_root)`.

`probe_conjuncts.py` — same tmp graph, two further conjuncts. **exit 0**:
wrapping `send_mod.send_dm` shows `_notify_undelivered` hands it
`comms_root(root)` (measured `[PosixPath('/tmp/.../project/.agi/comms/season-1')]`,
equal to `comms_root(root)` and NOT the graph root); a busy `send_dm`
(registry busy, fake tmux) prints BOTH `[undelivered-yet] director -- pane busy;
the sweep retries, you hear [undelivered] after 10 min` and
`nudge: coalesced (pane busy (registry))` in one stderr capture.

### 4. Production-line budget

`git diff --numstat -- extensions/agi/bin/send.py` -> `14 2` = 16 changed
production lines, under the 40-line ceiling. No production edit was made by
this round.

## Verdict

**proved.** All three conjuncts of the claim hold on the bytes in this tree:
(1) the notice lands in the comms root and is visible to `read_dms`; (2) the
call site is de-conflated and the fixture no longer conflates graph root with
comms root; (3) disposition (b) — the `nudge: coalesced` line is kept and the
busy path emits both lines. Both suites are green. The only caveat is
provenance: the delta was authored by a00-988fbdeb, not by this round.

## Agent Notes
Verified a00-988fbdeb's landed fix on the bytes: comms_root wire probe 6/6 (notice at comms_root(root)/dm, read_dms sees it), call-site de-conflation + coalesce disposition (b) probes green, test_send_undelivered.py 9 passed, test_send.py 330 passed, 16 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-302e563b). Accepted, with the evidence read from the bytes, not the result file. (1) INSTRUCTION: the target claim asks that _notify_undelivered writes through the comms root every other send_dm call site uses, that the test stop conflating the two roots, and that the old 'nudge: coalesced' line be gone. (2) MACHINE: git show ad5e7c8cc carries send.py +14/-2 -- send_dm(comms_root(root),..) at send.py:2804 and _announce_nudge(locations.find_project_root(croot) or croot,..) at send.py:3909 -- plus the test rewrite and this node. I ran three negative probes myself: probe_r1_baseline.py now exits 0 (notice at comms_root(root)/dm, read_dms returns 1 block; nothing at <graph-root>/dm); a /tmp copy with BOTH hunks reverted makes the rewritten suite RED (4 failed, 5 passed) -- so the fixture no longer conflates the roots; and probe_c_conjunct3.py shows a busy send_dm emits BOTH '[undelivered-yet] director' and 'nudge: coalesced (pane busy (registry))'. (3) NEAR MISS: the l5 claim's literal reading -- delete the coalesce print -- satisfies the words and loses the mechanism: _nudge_window is called directly by wake/heal with no _announce_nudge, so the diagnostic is those callers' only signal, and 16 test_send.py assertions pin it. Disposition (b) -- correct the claim, keep the line -- is therefore the honest landing, and the hypothesis node now says so. (4) DEVIATION: none from the standing rules; the completing kid changed no production byte and the two dead scaffolds were titled by the parent because re-briefing a terminal kid is impossible and an untitled node is a harvest defect.
<!-- THOUGHT:END -->
