---
id: experiment:a00-beccdfa1-cb4850
mint_id: 9b10d2c0794e4ef1aec766e6a39b55b4
type: experiment
parents:
  - hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard
next_edges: []
confidence: 0.7
edited_by: director-engine
evidence_runs: experiment:a00-beccdfa1-cb4850
loop: hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 10
profile: balanced
role: kid
scaffold_hash: 18724046033278a6
season: 2
title: "CTX.01 round 3: thread project_root through the survival brief; every reachable pi route carries the guard"
town: local-maxxing
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-beccdfa1-cb4850

## Experiment — CTX.01 round 3: finish the test-side of the built claim

The production build already sits in the tree (EF.101/EF.102): `pi.toml` carries one
`--no-context-files` and `brief.py` derives the paid-for path guard from ONE constant. Round 3
closes the two defects the EF.103 union named, and the one production line that made defect (2)
real.

```text
defect (2)  the test passes a fixture root -> assemble's survival branch DROPPED project_root
            -> _survival_state_card resolved the process's real .agi and ran a live
               `git status --porcelain` in this checkout (brief.py:753-760)
build       thread project_root through the survival branch and through _finish -> _prepend_head
```

## Build

```text
extensions/agi/bin/brief.py
  survival branch   _survival_brief(..., project_root=project_root)
  _finish           _prepend_head(..., project_root=project_root)

extensions/agi/tests/test_harness_template.py
  frozen pi argv    + one --no-context-files (the bare render too)

extensions/agi/tests/test_brief_render.py
  survival test     project_root=tmp_path (the fixture root now binds)
```

## Evidence

Probe (scratch, on the built bytes): all `len(TIERS) x len(PROFILES)` = 18 assemble routes
carry the guard; the real dispatch render for a pi kid and parent carries it; pi argv carries
`--no-context-files` exactly once; `brief.py` holds ONE literal source (`Paid-for path guard:`
count 1, `snapshot-build-site.py` count 1). The one unguarded route is
`successor_prompt(profile="full")`, and pi cannot reach it:
`rotate._known_harnesses() == ['claude-code', 'copilot-cli']`, `pi.toml rotate = false`.

```text
C2  ['pi','--provider','p','--model','m','--thinking','medium','--no-context-files',
     '-p','--mode','json','--append-system-prompt','b','t']   count=1
C3  18 routes checked, missing=[]
C4  dispatch kid guard=True len=12150 · dispatch parent guard=True len=17397
C5  successor full guard=False · successor survival guard=True  (all six tiers)
C6  _known_harnesses=['claude-code','copilot-cli'] · pi.toml rotate=False
```

The fixture root now binds the state card (probe stubs `subprocess.run`):

```text
git calls with fixture root: [['git','-C','.../a00-beccdfa1/_fixture_root2','status','--porcelain']]
```

Named suite on the built bytes:

```text
test_adapters + test_harness_template + test_brief + test_brief_render + test_briefing
292 passed, 1 skipped
```

Production measurement (read-only `git diff --numstat`):

```text
8  2  extensions/agi/bin/brief.py     (10 production lines, below the 40-line ceiling)
```

## Residue (named, not built)

`successor_prompt(profile="full")` carries no guard. It is reachable only by a rotate seat
given an explicit `--prompt-file`, and pi is not a rotate seat, so no pi brief loses the rule.
The config-max fix — the guard text in the brief configuration, which would also cover
`brief.render` (rotate.py:1132) — is the CTX.01 residue already routed to TM.

## Agent Notes
EF.103 round 3: threaded project_root through assemble's survival branch and _finish so a fixture root binds _survival_state_card (no live git status); updated the frozen pi argv shape test for --no-context-files; all 18 tier x profile assemble routes and the pi dispatch renders carry the guard from ONE constant; 292 passed 1 skipped; 10 production lines. Residue: successor_prompt(full) is unguarded but unreachable for pi (rotate=false).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Director gate (05:13Z 09-24); verdict set over the parent's inconclusive_lean_disproved:20. Build (1): both frozen pi argv asserts carry --no-context-files once -- the tip's test is RED against the trunk's pi.toml (no flag) and green on the tip, 292 passed / 1 skipped (test_harness_template, test_brief_render, test_brief, test_briefing, test_adapters). Build (2), by another route than ordered: a fixture root (tmp_path) instead of a subprocess stub, plus brief.py threading project_root into _survival_brief -> _survival_state_card (brief.py:783, 816) and _prepend_head, outside the orders' two test files; the survival git status now reads the fixture, not the live checkout, but a real git process still runs and no assertion discriminates the threading. The parent's disproof (a caller-injected duplicate --no-context-files in extra_args renders twice) is no reachable route: no caller passes the flag, it lives only in pi.toml:10. Process: this kid ran on the PAID lane (harness pi, deepseek-v4.1-flash, ~1.35 USD by pi's own accounting) because its parent's spawn dropped --harness pi-free -- [red] to thought-master 05:1xZ; the bytes are judged on their merits.
<!-- THOUGHT:END -->

Parent review: default render and live pi_adapter wire path each emit one --no-context-files; the named suite is 292 passed, 1 skipped. Adversarial untrusted extra_args injected a second --no-context-files, so the absolute once invariant is not proved at the public render boundary. Guard constant wire probe reached all constructible non-advisor tier/profile routes; advisor full requires a real vision node.
