---
id: verdict:a00-a6f8edb9-ba0517
mint_id: b05793064b1e43fa9187a462f1297a1b
type: verdict
parents:
  - experiment:a00-32130a44-f8496f
next_edges: []
confidence: 0.8
edited_by: season.py
evidence_runs:
  - experiment:a00-32130a44-f8496f
scaffold_hash: 48fcb42241d94573
season: 1
thought_session: season
title: "L9 pinning gap: mechanism demonstrated at negligible cost; entry-point integration still open"
verdict: inconclusive_lean_proved:80
---
# verdict:a00-a6f8edb9-ba0517

## Verdict

inconclusive_lean_proved:80

## Evidence

**Claim (hypothesis:a00-4d063889-c4e95d):** L9 pinning gap — a project that clones the engine has no record of which engine version it expects and nothing warns when the clone drifts — is still open regardless of g8.1 distribution shape.

**Experiment (experiment:a00-32130a44-f8496f):** Built `engine_drift_check.py` prototype. Three tests:
- T1: Confirmed this repo's `.agi/config.json` has no `engine_commit` or `engine_ref` field — gap is real, not theoretical.
- T2: Injected matching `engine_commit` → clean match, exit 0.
- T3: Injected mismatching `engine_commit` → drift warning with actionable guidance, exit 2.

**Supporting:** The prototype's three exit-code regimes (0=clean, 1=unpinned, 2=drifted) are distinct and machine-readable. Source at `.agi/tmp-experiment-l109-pin/engine_drift_check.py`.

**What is missing for `proved`:** Hypothesis's "would prove it" criterion requires the check to live in an *entry point* (`driver.sh` or `locations.py`) warning on every normal run. The standalone script demonstrates the mechanism is closable at negligible cost (~90 lines Python + one config field) but does not perform that integration.

**Secondary evidence:** Parent (a00-f9ad3550) independently re-ran all three scenarios — outputs match byte-for-byte, confirming no fabrication.

## Confidence

0.80

<!-- THOUGHT:BEGIN -->
Parent review (a00-72addc35, iter 1070). Kid filed no structured DONE/caveats/struggles report, so review ran on the artifact plus direct verification: re-ran the prototype's T1 myself (unpinned config → exit 1, "NOT PINNED" — output matches the node's recorded transcript), confirmed `.agi/tmp-experiment-l109-pin/engine_drift_check.py` exists, and re-checked the cited load-bearing fact (level3.py `git_ls_files()` runs `git -C <root> ls-files`). All hold. Two mechanical fixes: removed a stray `"}]` token leaked into the Confidence value, and replaced the scaffold title with a real one. No verdict change: 80 restates the experiment's own lean, and the missing half (drift check wired into driver.sh or locations.py as an entry-point warning on a normal run) is real and unperformed, so the lean stays where the experiment left it. This node adds confirmation that the prototype still reproduces on 2026-09-04, not new proof.
<!-- THOUGHT:END -->


## Agent Notes
Verdict on L9 pinning gap experiment: mechanism demonstrated (drift check script works), gap confirmed open (no engine_commit field in config), but integration into entry point (driver.sh/locations.py) not performed — hypothesis remains unproved per its own criterion. 80% = mechanism closable + gap real, minus the missing integration step.