---
id: experiment:brainstorm-manifest-goal-guard-fix
mint_id: 71bb2494373044a0a717c2e385068234
type: experiment
parents:
  - hypothesis:brainstorm-manifest-route-refuses-a-missing-goal
next_edges: []
confidence: 0.9
edited_by: director-engine
evidence_runs:
  - experiment:brainstorm-manifest-goal-guard-fix
role: director
scaffold_hash: cda812ac75cde464
season: 2
title: required_args manifest field + one generic check in run_workflow, red/green verified
town: core
verdict: proved
---
# experiment:brainstorm-manifest-goal-guard-fix

## Experiment

```text
workflow.py run_workflow("brainstorm", args)
        │
        ├─ JS route (agi-brainstorm.js)     -- already refused a missing/blank goal
        └─ pi / pi-free manifest route      -- BEFORE: no check at all, proceeded to dispatch
                                                AFTER: manifest.required_args checked right after
                                                       _load_manifest, before _expand_stages --
                                                       refuses by name, rc 2, nothing dispatched
```

Confirmed the measured gap directly (matches hypothesis:brainstorm-manifest-route-refuses-a-
missing-goal's own Measured section): `run_workflow` (rotate... no, workflow.py:2149) loaded
the manifest and expanded stages with no required-input check anywhere on the pi/pi-free path;
only the native JS script (`agi-brainstorm.js`) checked for a non-empty `goal`, and
test_workflow.py:760 already proved the JS half but never drove the manifest runner itself.

Fix: `brainstorm.json` gets a new top-level `required_args: ["idea", "goal", "why",
"max_hypotheses"]` declaration (config-max per the hypothesis's own Dispatch line -- the
required list lives in the manifest, not a literal check hardcoded to brainstorm). One GENERIC
check added to `run_workflow` right after the manifest loads and before `_expand_stages`: any
workflow that declares `required_args` gets each one checked non-blank, refusing by name (rc 2,
distinct from the existing rc 3/4/5 refusal classes in the same function) before any stage
dispatch. Other workflows are unaffected (none currently declare `required_args`, so the check
is a no-op for them).

## Evidence

Command:

```text
python3 -m pytest extensions/agi/tests/test_workflow.py -k test_brainstorm_manifest_route_refuses_a_missing_goal -v
```

Result (with the fix applied): both parametrized cases (goal absent, goal="") pass -- rc != 0,
no `[dispatch]` line, stderr names "refused" and "goal".

Red/green discipline: reverted the fix (workflow.py + brainstorm.json) via a saved patch +
`git checkout --`, re-ran the same test, confirmed BOTH cases fail with `rc == 0` (the run would
have proceeded to dispatch on a missing or blank goal), reapplied via `git apply`, confirmed
green again. Full extensions/agi/tests/test_workflow.py run in progress/pending at record time
(a large, slow file) -- the targeted test is the direct evidence for this claim; full-file
confirmation to follow before merge-up if it finishes within this session.

## Agent Notes
One new parametrized test (`test_brainstorm_manifest_route_refuses_a_missing_goal`, two cases)
drives the real `run_workflow` against the real `brainstorm` manifest with `dry_run=True`,
asserting a non-zero return, no `[dispatch]` line in stdout, and a stderr refusal naming both
"refused" and "goal".

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Third PASS-6 code defect attempted directly this session (after defects 4 and 1), same
reasoning: belam's own Dispatch line already specified the approach precisely (config-max in
the manifest, one generic check in run_workflow), removing the main risk of an ad-hoc,
workflow-specific hack. Chose a GENERIC `required_args` manifest field over a brainstorm-only
hardcoded check, since the fix should generalize to any other workflow that later needs the
same guard, matching this project's own config-max discipline. Matched the existing refusal
style in run_workflow exactly (print to stderr, a distinct numeric return code, a comment
explaining why THIS code differs from neighboring ones) rather than inventing a new pattern.
Verified red-then-green on the targeted test before minting this record; the full test_workflow.py
file is slow (backgrounded past 120s) and its full-file confirmation was still pending when
this experiment was minted -- noted honestly rather than claimed complete.
<!-- THOUGHT:END -->
