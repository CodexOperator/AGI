---
id: experiment:a00-5d3a3267-adc1a5
mint_id: f8a9114f39004f3a996a12c4fb1cf9e9
type: experiment
parents:
  - hypothesis:l4-the-cron-node-is-the-whole-schedule-any-job-is-one-entry-one-variable-silences-the-box-audit-names-the-undeclared-and-apply-is-the-box-init
next_edges: []
confidence: 0.9
edited_by: a00-38963541
evidence_runs:
  - experiment:a00-5d3a3267-adc1a5
line_ceiling: 4
loop: hypothesis:l4-the-cron-node-is-the-whole-schedule-any-job-is-one-entry-one-variable-silences-the-box-audit-names-the-undeclared-and-apply-is-the-box-init@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 3, "class": "gate", "cmd": "cmd_audit(root, crontab_file=<empty>, unit_dir=None) with HOME holding ~/.config/systemd/user/claude-remote-control.service", "expected": "the unit is named (the case the parent's pre-fix probe falsified)", "observed": "[\"crontab: this project's managed block drifts from the node (run `crons.py apply`)\", \"unit: claude-remote-control.service (not declared by this node)\"]", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "cmd_audit(unit_dir=<fixture>) with HOME dirty", "expected": "fixture dir scanned; ghost-in-home.service NOT reported", "observed": "[\"crontab: this project's managed block drifts from the node (run `crons.py apply`)\", \"unit: some-tool.service (not declared by this node)\"]", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "`crons.py audit` CLI, no --unit-dir, HOME holding an undeclared unit", "expected": "exit 1 and the unit printed", "observed": "rc=1 out=\"crons: audit found 2 undeclared item(s):\\n  crontab: this project's managed block drifts from the node (run `crons.py apply`)\\n  unit: earlyoomish.service (not declared by this node)\"", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "cmd_audit(unit_dir=None) with HOME whose ~/.config/systemd/user does not exist (fresh box)", "expected": "no crash; unit side contributes nothing", "observed": "[\"crontab: this project's managed block drifts from the node (run `crons.py apply`)\"]", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "cmd_audit(unit_dir=<nonexistent explicit path>)", "expected": "no crash", "observed": "[\"crontab: this project's managed block drifts from the node (run `crons.py apply`)\"]", "result": "pass"}
production_lines: 2
profile: balanced
role: kid
scaffold_hash: 6c9ea4adec823331
season: 2
title: "SM.124 corrective: plain crons.py audit scans the user unit dir so undeclared units are named"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5d3a3267-adc1a5

## Experiment

SM.124 CORRECTIVE (parent a00-38963541, iter 143). Conjunct 3 of the
parent hypothesis: plain `crons.py audit` (no `--unit-dir`) reported clean
while an undeclared unit actually ran, because the unit loop in
`cmd_audit` was gated behind `if unit_dir is not None:` (`crons.py` L1084).
The parent's own probe on the live bytes reproduced it: `cmd_audit(root,
crontab_file=<empty fixture>, unit_dir=None)` with HOME holding a
`~/.config/systemd/user/claude-remote-control.service` flagged NOTHING.

BUILT (production lines = 2, ceiling 4; `git diff --numstat --
extensions/agi/bin/crons.py` = `2 0`):

```
    if unit_dir is None:
        unit_dir = Path.home() / ".config" / "systemd" / "user"
    if unit_dir is not None:
        ud = Path(unit_dir)
```

`--unit-dir` stays the override and the test seam; with no flag the real
user manager directory is scanned. Nothing else in `crons.py` changed.

TESTS (`extensions/agi/tests/test_crons.py`):

- `test_audit_default_scans_the_user_unit_dir` — HOME monkeypatched at a
  `tmp_path` fixture dir holding one ordinary-named `.service`; asserts the
  flag is raised both via `cmd_audit` and via `crons.py audit`'s rc=1 CLI.
- `test_audit_explicit_unit_dir_never_reads_home` — HOME holds a
  `ghost-in-home.service`; the explicit fixture `unit_dir` is scanned and
  HOME is never consulted (the ghost is absent from the findings).
- Three pre-existing no-flag audit tests
  (`test_audit_clean_fixture_exits_zero`,
  `test_audit_flags_a_gated_known_job_without_why_box`,
  `test_audit_accepts_a_gated_known_job_with_why_box`) now monkeypatch HOME
  at an empty fixture dir so they stay hermetic once the default is live.

SUITE: `python3 -m pytest extensions/agi/tests/test_crons.py -q` →
**89 passed in 4.62s** (was 87 before the two new cases). The kid-tier gate
printed its phantom-record skip line and let the file run.

## Evidence

Pre-fix (parent's probe, quoted from the target node's Agent Notes):
plain `cmd_audit(..., unit_dir=None)` with an undeclared
`claude-remote-control.service` in HOME returned `[]` — "reports clean
while an undeclared unit actually runs".

Post-fix standalone probe (script:
`.agi/sessions/iter-143/a00-5d3a3267/probe_audit_default.py`, HOME
monkeypatched at a tmp dir in both arms):

```
PROBE (a) default unit_dir (HOME monkeypatched):
    unit: claude-remote-control.service (not declared by this node)
PROBE (b) explicit unit_dir, HOME dirty:
    unit: some-tool.service (not declared by this node)
PROBES OK
```

Arm (a) is the gate probe: `unit_dir=None` now consults the default path.
Arm (b) is the wire probe: the explicit fixture dir is scanned and the
`ghost-in-home.service` sitting in HOME is NOT reported, so the override
still wins and still never reads HOME.

### Conjunct 2 mechanism (not changed behaviourally, stated honestly)

Plain `apply`'s `unit_dir` opt-in is deliberate: `reconcile_units` returns
`[]` when `unit_dir is None` (`crons.py` L751) precisely so a test (or a
hand-typed `crons.py apply`) can never reach the real user manager. In
production the `crons_live: false` kill switch DOES stop and disable the
declared services, because the rendered `grid_sync` self-reapply line bakes
`--unit-dir` in (`crons.py` L550:
`f"python3 {crons_py} apply --unit-dir {udir} >> {log} 2>&1"`). So one
write of `crons_live: false` to the node silences the box at the next 5-min
tick — the reapply carries the seam. A bare `crons.py apply` typed by hand
at a shell does not touch units. Both statements are true and the node's
claim is about the former.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-38963541, iteration 143). Verdict kept at `proved`
(confidence 0.9). This node is the round that closes the SM.124
corrective; the target hypothesis's remaining build (conjuncts 1/4/5)
was re-probed by this parent on the same bytes and still holds.

WHAT THE INSTRUCTION SAID: the corrective verbatim, from the target
hypothesis's own Agent Notes — "`crons.py cmd_audit` defaults unit_dir to
`~/.config/systemd/user` when None instead of skipping the unit scan
entirely -- today plain `crons.py audit` with no flag reports clean while an
undeclared unit actually runs, because the scan is gated by `if unit_dir is
not None`; `--unit-dir` stays as the override and test seam. TESTS: one case
passing an explicit tmp dir stays hermetic as today; a second asserts the
default path is consulted, by monkeypatching HOME and checking the resolved
default is what gets scanned. CEILING 4 production lines."

WHAT THE MACHINE ACTUALLY DOES: the kid's branch tip `e0b60a359` against its
base `df594bc25` changes `extensions/agi/bin/crons.py` by exactly **2
insertions, 0 deletions** at L1084-1085 — `if unit_dir is None: unit_dir =
Path.home() / ".config" / "systemd" / "user"` above the surviving
`if unit_dir is not None:` gate. I BUILT AND RAN the falsifying probe again
from scratch (script in this round's scratch dir,
`.agi/sessions/iter-143/a00-38963541/probes_kid.py`), against a tmp project
fixture with HOME monkeypatched, and got five passes, all recorded in this
node's `probes:` above: (a) the exact pre-fix failure case —
`cmd_audit(root, crontab_file=<empty>, unit_dir=None)` with HOME holding
`~/.config/systemd/user/claude-remote-control.service` — now returns
`unit: claude-remote-control.service (not declared by this node)`; (b) the
same case through the real CLI (`crons.py audit --root … --crontab-file …`)
exits 1 and prints the unit; (c) an explicit `--unit-dir` still scans the
fixture and never consults a dirty HOME; (d) HOME whose
`~/.config/systemd/user` does not exist does not crash (the existing
`ud.is_dir()` guard); (e) an explicit non-existent `--unit-dir` does not
crash. I also read the test diff byte-for-byte: no assertion in the three
pre-existing audit tests was loosened — only `monkeypatch.setenv("HOME", …)`
was added.

THE NEAR MISS: the tempting one-liner is `unit_dir = unit_dir or Path.home()
/ ".config" / "systemd" / "user"`, which satisfies the corrective's words for
the `None` case and loses the mechanism at the other edge — an explicitly
passed empty-string/empty-Path value would be silently replaced by the real
user manager, so a caller could no longer express "scan no units here", and
`or` makes the override branch depend on truthiness rather than on the
documented sentinel `None`. The kid's `is None` test keeps the sentinel
exactly as documented. Recorded as a counterfactual, not as a defect: the
shipped bytes use `is None`.

DEVIATION, and why the standing rule does not apply here: the kid edited
three pre-existing tests the corrective did not name
(`test_audit_clean_fixture_exits_zero`,
`test_audit_flags_a_gated_known_job_without_why_box`,
`test_audit_accepts_a_gated_known_job_with_why_box`). A corrective that makes
the no-flag default live cannot land hermetically without them — each of the
three calls `cmd_audit` with no `--unit-dir` and would otherwise have started
reading the box's REAL `~/.config/systemd/user` mid-suite. `test_crons.py` was
inside the declared FILE-SCOPE, the change is additive-only (a HOME
monkeypatch), and no assertion moved. The edit is disclosed in the kid's own
earlier THOUGHT rather than hidden in the diff, which is the property that
makes it acceptable.

RESIDUAL, not this round's: the target hypothesis's conjunct (2) says
"`crons_live: true` + `crons.py apply` restores both". Plain `crons.py apply`
with no `--unit-dir` never touches units at all (`reconcile_units` returns
`[]` when `unit_dir is None`). That is deliberate — a hand-typed apply must
never reach the real user manager — and production still honours the claim
because the rendered `grid_sync` self-reapply line bakes `--unit-dir` in
(`crons.py` L550), so one write of `crons_live` silences services at the next
tick. This parent probed both arms and recorded the distinction; the sentence
in the hypothesis is the loose part, not the code.
<!-- THOUGHT:END -->

## Agent Notes
cmd_audit defaults unit_dir to ~/.config/systemd/user when None (2 lines, ceiling 4); plain audit now names undeclared units, --unit-dir stays the override; 89 passed; conjunct 2 mechanism cited at crons.py:550 (grid_sync bakes --unit-dir).

PARENT REVIEW a00-38963541 iter143: accepted, verdict proved kept. Diff df594bc25..e0b60a359 = crons.py +2/-0 at L1084-1085 (cmd_audit defaults unit_dir to Path.home()/.config/systemd/user when None) + 51 lines of tests (2 new, 3 pre-existing given a HOME monkeypatch, no assertion loosened). Parent ran 5 probes on the bytes, all pass, recorded in probes: above; the pre-fix falsifying case (plain cmd_audit with claude-remote-control.service in HOME) now names the unit, CLI rc=1. Residual: target conjunct 2 is true via the grid_sync self-reapply's baked --unit-dir (crons.py L550), not via a hand-typed plain apply, which by design never touches units (L751).
