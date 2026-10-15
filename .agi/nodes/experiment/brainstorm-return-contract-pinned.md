---
id: experiment:brainstorm-return-contract-pinned
mint_id: e1cde1d7d06b4e83a26f04d2b951c25b
type: experiment
parents:
  - hypothesis:brainstorm-and-research-review-contracts-match-their-manifests
next_edges: []
confidence: 0.95
edited_by: director-engine
evidence_runs:
  - experiment:brainstorm-return-contract-pinned
scaffold_hash: 829a904d18eaa9fb
season: 2
tags:
  - local-maxxing
  - engine
  - workflow
testable_claim: agi-brainstorm.js REQUIRED and property-name schema keys for both stages match brainstorm.json manifest schema exactly; a synthetic drift is caught.
title: agi-brainstorm.js JS schema now pinned against the manifest, mirroring research-reviews contract test
town: core
verdict: proved
---
# experiment:brainstorm-return-contract-pinned

# experiment:brainstorm-return-contract-pinned

## Experiment

Closed the remaining half of `hypothesis:brainstorm-and-research-review-contracts-match-their-
manifests` (PASS 5 chunk 4 / PASS 6 residue: "the claimed JS-versus-manifest return-key test
exists for research-review only; brainstorm's test covers the goal gate"). The goal-gate half
(defect row 2, `hypothesis:brainstorm-manifest-route-refuses-a-missing-goal`) landed last
session; this closes the return-contract half.

`agi-brainstorm.js`'s prompts (`BRAINSTORM_TMPL`, `REFUTE_TMPL`) ask for the return in plain
English -- unlike `agi-research-review.js`'s refute prompt, they carry no `RETURN CONTRACT: ...
TOP-LEVEL keys are exactly: ...` sentence, so `test_research_review_refute_contract.py`'s
prose-parsing approach (`_stated_top_level_keys`) has nothing to parse here. The faithful
brainstorm-side equivalent of "diff JS return keys against the manifest" is comparing the JS
`agent(..., {schema: ...})` literal (`BRAINSTORM_SCHEMA`, `REFUTE_SCHEMA` -- what the runner
actually validates the model's return against) directly to `brainstorm.json`'s own per-stage
`schema` (the pi-route's copy of the same contract).

New file `extensions/agi/tests/test_brainstorm_return_contract.py`, three tests: every manifest
stage has a JS schema counterpart (so a new stage added to only one side is caught); JS and
manifest agree on `required` per stage; JS and manifest agree on the full property-name set per
stage (narrower than `required` alone). No production code changed -- both schemas already
matched byte-for-byte; this adds the regression the residue named as missing.

## Evidence

```text
$ python3 -m pytest extensions/agi/tests/test_brainstorm_return_contract.py -q
3 passed
```

Drift-catching proof (not a red/green on production code, since none changed -- a synthetic
perturbation proving the assertion is live, restored byte-identical from a saved copy
immediately after):

```text
$ python3 -c "... remove 'commit' from brainstorm.json's refute stage required list ..."
$ python3 -m pytest extensions/agi/tests/test_brainstorm_return_contract.py -q
1 failed, 2 passed
AssertionError: ('refute', ['idea', 'verdicts', 'ready_batch', 'commit'], ['idea', 'verdicts', 'ready_batch'])
$ cp /tmp/brainstorm.json.bak extensions/agi/workflows/brainstorm.json   # exact restore
$ git diff --stat -- extensions/agi/workflows/brainstorm.json            # no output: byte-identical
$ python3 -m pytest extensions/agi/tests/test_brainstorm_return_contract.py -q
3 passed
```

## Agent Notes
assigned: director-engine (PASS 5/6 residue, belam-S2-L5-V/VI 09-25)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE HYPOTHESIS ASKED: one test per workflow diffing JS return keys against the manifest's
declared contract; research-review already had one, brainstorm did not. WHAT THE MACHINE
ACTUALLY DOES: brainstorm.js's prompts are not authored in research-review's enumerated-prose
style, so literally reusing `_stated_top_level_keys` would find nothing to parse -- rather than
force a prose sentence into brainstorm's prompts just to make the old test's parsing function
reusable (which would be a needless production-code edit for a test's convenience), compared the
two sides' actual JSON schemas directly, which is the more direct statement of "what the JS
returns" for this workflow's own authoring style. Verified the comparison is a REAL regression
gate, not a tautology, by injecting a synthetic one-field drift and watching it fail, then
restoring the file from a saved copy and confirming a byte-identical `git diff --stat` before
re-confirming green -- the same discipline as a red/green pair, adapted for a pinning test where
there is no production fix to revert.
<!-- THOUGHT:END -->
