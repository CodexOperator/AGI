---
id: experiment:brainstorm-manifest-goal-guard-fix
mint_id: 71bb2494373044a0a717c2e385068234
type: experiment
parents:
  - hypothesis:brainstorm-manifest-route-refuses-a-missing-goal
next_edges: []
confidence: 0.9
edited_by: a00-9619f32e
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
Parent review (a00-9619f32e, DH.377) — ACCEPTED, verdict proved holds.

(1) WHAT THE INSTRUCTION SAID, quoted. "Run one negative probe per claim
conjunct yourself and record them as `probes:`; a kid that passes its own
suite but fails your probe is lean_disproved." So the kid's two passing
parametrized cases are its CLAIM; my evidence is the five probes below, run
by me from
/.../post-director-engine/.agi/sessions/iter-DH.377/a00-9619f32e/probe_parent.py.

(2) WHAT THE MACHINE ACTUALLY DOES. The changed bytes I read, not the summary:
extensions/agi/bin/workflow.py:2246-2261 — `_missing_args` is computed from
`manifest.get("required_args")`, each entry tested with
`not str(args.get(a) or "").strip()`, printed to stderr as
`workflow=<key> refused: missing required non-empty arg(s) [...]` and
`return 2`, positioned AFTER `_load_manifest(repo, key)` and BEFORE
`_expand_stages`. extensions/agi/workflows/brainstorm.json:4 declares
`"required_args": ["idea", "goal", "why", "max_hypotheses"]` (config-max, the
list is in the manifest, not a literal in the code). The claimed test is
really in the bytes: extensions/agi/tests/test_workflow.py:786-805,
parametrized on goal-absent and goal="".
Probes, all green, run against the live `run_workflow` (dry_run, pi and
pi-free):
  probes: P1 gate — goal key absent: rc=2, stderr names workflow + "goal" +
  "refused", zero [dispatch] lines.
  probes: P2 gate — goal "", "   ", "\t\n": rc=2 and no dispatch on all three
  (the `.strip()` is real, not a falsy-only test).
  probes: P3 wire — the byte is on the live path AND is not over-broad: a
  fully populated brainstorm (idea/goal/why/max_hypotheses) returns rc=0
  with no refusal and DOES reach `[dispatch] brainstorm :: ...` /
  `[dispatch] refute :: ...`. This is the probe the kid's own suite cannot
  make: a guard that refused every run would pass both its cases.
  probes: P4 auth — a workflow the claim never authorises touching,
  `research-review` (declares no required_args), still runs rc=0 and
  dispatches; the new guard is a no-op there, so no collateral damage.
  probes: P5 gate — order: with `_expand_stages` wrapped, a refused run calls
  it 0 times, so the refusal genuinely precedes stage expansion, not just
  dispatch printing.
Also checked the inheritance path by reading it: `_load_manifest` merges with
`{**inherited, **raw}`, so a manifest that `extends` brainstorm inherits
required_args rather than silently dropping the guard. And grep found no
in-repo caller other than the workflow.py CLI entry, so no internal caller
that omits `goal` is newly broken.

(3) THE NEAR MISS. A `return 2` placed AFTER `_expand_stages`, or after the
first `[dispatch]` print, would satisfy the kid's suite verbatim (rc != 0, no
`[dispatch]` in the captured buffer) while a run had already expanded stages
— that is what P5 exists to catch. The second near miss is subtler: a guard
that refuses unconditionally, or a `if "goal" not in args` test that misses
whitespace-only values, both pass the kid's two cases; P3 and P2 are what
separate them from the real fix.

(4) IF I DEVIATED FROM A STANDING RULE. None material. I read the changed
bytes in the checkout rather than a `git diff` because this dispatch's own
orders forbid running git at all ("Do not commit. Do not push. Do not run git
at all"); the checkout bytes plus five executed probes are the evidence I
substitute for the diff, and both descriptors in the node body match the
bytes on disk.
<!-- THOUGHT:END -->

Parent DH.377 review: ACCEPTED. probes: P1 gate (goal absent -> rc=2, names workflow+goal, zero [dispatch]); P2 gate (goal "", "   ", "\t\n" -> rc=2, no dispatch); P3 wire (full valid args -> rc=0 AND reaches [dispatch], so the guard byte is live and not over-broad); P4 auth (research-review, which declares no required_args, still rc=0 and dispatches — no collateral damage); P5 gate (_expand_stages wrapped: 0 calls on a refused run, refusal precedes stage expansion). Verdict proved stands.

Parent DH.377 review addendum: probes: P6 wire, END-TO-END through the CLI (`workflow.py run brainstorm --harness pi --args ... --dry-run`, the only sanctioned dispatch route, not the in-process function) — goal absent and goal="  " both print the refusal and exit 2 with zero [dispatch] lines. Also closed the kid's own pending residue: full extensions/agi/tests/test_workflow.py = 121 passed in 135.79s, so the new generic required_args check regresses nothing in that file.
