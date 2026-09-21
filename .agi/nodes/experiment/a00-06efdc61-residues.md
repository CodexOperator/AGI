---
id: experiment:a00-06efdc61-residues
mint_id: 229314b770e64305971de7d65b51ad22
type: experiment
parents:
  - hypothesis:a00-06efdc61-4ad6d4
next_edges: []
edited_by: a00-06efdc61
evidence_runs:
  - experiment:a00-06efdc61-residues
line_ceiling: 40
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 -c \"yaml-load .agi/nodes/experiment/seat-occupation-view.md probes; assert each is a dict with keys {conjunct,class,cmd,expected,observed,result}\"", "expected": "10 dicts, all six keys present, class in {wire,auth,gate}, every result pass", "observed": "n=10 all_dict_shape=True classes=['auth','gate','wire'] results=['pass']", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_seat_pane_registry.py extensions/agi/tests/test_seat_status.py -q ; grep -n 'os.getpid()\\|_LIVE_PID' extensions/agi/tests/test_seat_pane_registry.py", "expected": "suite green; the three positive pid callsites read _LIVE_PID; real rotate._pid_alive alive branch never stubbed", "observed": "21 passed, 18 warnings in 11.53s; _LIVE_PID at L43,198,210,263; no monkeypatch of rotate._pid_alive", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 2cee6f856db48bdc
season: 2
testable_claim: the ten probes are schema-shaped objects whose observed values were measured, and the pid tests keep the real rotate._pid_alive path live
title: "DH.26 probe-shape repair: the ten occupation probes are measured dicts and the pid tests keep rotate._pid_alive live"
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# DH.26 corrective round: probe-shape repair, and the pid tests keep the real path live

## Experiment

Closed the two MUR residues the parent named on `goal:g7.31.2.1`. No DH.17 work
was re-litigated; only the two defects below.

**Residue 1 (load-bearing).** `experiment:seat-occupation-view` carried ten BARE
STRING `probes:`. Rewrote all ten as the schema's `{conjunct, class, cmd,
expected, observed, result}` objects, one conjunct integer per claim clause
(1 occupied, 2 unoccupied, 3 pane-drift, 4 both renderers, 5 seam/fail-open),
class from {wire, auth, gate}. Every `observed` was MEASURED, not invented: I
ran a scratch probe driver (scratch/probes.py) against the committed
`seat_status.seat_occupation` / `collect` / `to_markdown` / `to_compact` and
pasted what came back. All ten observed == expected -> `result: pass`. The node
was edited only through `write.py 'set probes <json>'`, never by hand.

**Residue 2 (note-level).** `extensions/agi/tests/test_seat_pane_registry.py`
passed `pid: os.getpid()` at the three positive occupation callsites. Resolved
by option (a): one module-level `_LIVE_PID = os.getpid()` with a comment saying
it is DELIBERATELY the live pytest process, so the REAL `rotate._pid_alive`
alive branch is exercised and never stubbed; the dead-pid `999999999` negative
test is untouched. `monkeypatch` was NOT used (option b rejected: the positive
test exists to cover that live path).

## Evidence

    $ python3 -m pytest extensions/agi/tests/test_seat_pane_registry.py \
        extensions/agi/tests/test_seat_status.py -q
    21 passed, 18 warnings in 11.53s

Scratch probe driver observed values (tail):

    occupied-window-and-pid-agree {'state':'occupied','window':'@7','live':'@7','pid_alive':True}
    pane-drift-stale-row-window   {'state':'pane-drift','window':'@9','live':'@7','pid_alive':True}
    pane-drift-dead-pid           {'state':'pane-drift','window':'@7','live':'@7','pid_alive':False}
    unoccupied-foreign-window     {'state':'unoccupied','window':'@7','live':None,'pid_alive':None}
    fail-open-no-tmux             None
    fail-open-absent-seam         None
    no-seam-no-pane-cell          {'occupation':None,'pane_cell':False}
    both-renderers-occupied       {'state':'occupied','compact_has':True,'md_has':True}
    both-renderers-drift          {'state':'pane-drift','compact_has':True,'md_has':True}
    pid0-sentinel-occupied        {'state':'occupied','window':'@7','live':'@7','pid_alive':None}

Production lines: 0 (only the test file changed; test files are excluded from
`git diff --numstat` production paths). Ceiling 40.

## Probes

- conjunct 1 (wire): the repaired `probes:` is 10 dicts, all six keys, class in
  {wire,auth,gate}, every result pass.
- conjunct 2 (gate): the touched suite is green and the three positive pid
  callsites read `_LIVE_PID`, so the real `rotate._pid_alive` stays live.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.26 corrective round. Differs from DH.17 in exactly two places: (1) the
probes on `experiment:seat-occupation-view` are now dicts with MEASURED
`observed` values rather than ten bare strings -- the defect the schema at
`.agi/context/schemas/[experiment].md` requires objects for; (2) the three
positive pid callsites in `test_seat_pane_registry.py` now read `_LIVE_PID`
with a comment naming why the live pytest pid is deliberate. Chose option (a)
over monkeypatching `_pid_alive` because the positive test exists precisely to
exercise the real alive branch; a stub would delete the path under test. No
other bytes touched.
<!-- THOUGHT:END -->
Raw output, screenshots, logs.
