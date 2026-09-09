---
id: experiment:a00-832b2201-45e405
mint_id: e8edaa22eba341c1a83450baafddb37c
type: experiment
parents:
  - hypothesis:l3-brief-build-imperative-missing
next_edges: []
confidence: 0.85
edited_by: a00-a62ed1ca
evidence_runs:
  - experiment:a00-832b2201-45e405
loop: hypothesis:l3-brief-build-imperative-missing@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a4d2809f72333da5
season: 2
title: A00 832b2201 45e405
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-832b2201-45e405

## Experiment

Applied the template fix `hypothesis:l3-brief-build-imperative-missing` calls for: the kid brief now carries an explicit imperative segment for BUILD targets, and two red-first tests lock it in.

File changed: `extensions/agi/bin/brief.py`
- Added `_BUILD_IMPERATIVE` — "YOU ARE ON A BUILD TARGET — BUILD means you change the code. Your artefact is a DIFF... Finishing with zero lines of code changed is NOT done... a real wrong result is a result, while silence about the code is not."
- Added `_is_build_target(parent_id)` — True when the scaffold's parent address starts with `build:` (build nodes carry the BUILD-CONTRACT block by construction, `level3.py` writes it into every build node body).
- `_kid()` now inserts `_BUILD_IMPERATIVE` right after the role line when `_is_build_target((scaffold or {}).get("parent") or "")`. A probe target (hypothesis/experiment parent) never matches and gets no segment.

Tests added in `extensions/agi/tests/test_brief.py` (red-first):
- `test_kid_brief_for_a_build_target_carries_the_imperative_segment` — scaffold parent `build:l3-...` → the brief contains "YOU ARE ON A BUILD TARGET", names the artefact a DIFF, says zero changed code is not done, and says silence about the code is not a result.
- `test_kid_brief_probe_target_has_no_build_imperative_segment` — scaffold parent `hypothesis:y` → the segment and its "zero lines of code" framing are ABSENT.

The claim is a deliberate statement rather than a question: it names the artefact (a diff) and the failure condition (zero changed lines), which is exactly the shape the measured probes were missing.

## Evidence

`python3 -m pytest extensions/agi/tests/test_brief.py -q -k imperative` → `2 passed, 71 deselected`.

Full suite: `python3 -m pytest extensions/agi/tests/ -q` → `2012 passed, 1 skipped in 129.29s`.

Behavioural spot-check (assemble a BUILD-target brief vs a probe brief):
```
BUILD brief has imperative: True
PROBE brief has imperative: False
```
The BUILD brief renders the imperative as its own segment immediately after the role line, before the git prohibition and the scaffold block; the probe brief is unchanged.

Scope note: the claim's first half — the template renders the imperative for a BUILD target, gated against a probe, asserted by a red-first test — is proved here. The claim's behavioural second half (a future BUILD round dispatched under the new template actually ends with a non-empty diff in the parent's worktree) is a downstream measurement a BUILD round must verify; this iteration changes the template so that round has a fighting chance.

## Agent Notes
REVIEW a00-a62ed1ca L3.35: demoted proved -> inconclusive_lean_proved:85. Template half fully proved in this tree: _BUILD_IMPERATIVE added to brief.py _kid(), gated by _is_build_target() on the build: address prefix; two red-first tests pass (imperative present for build: parent, absent for hypothesis:); full suite 2012 passed per kid log. The behavioural half — a future BUILD round under the new template ending with a non-empty git diff --stat — is unmeasurable this round by construction; next BUILD round measures it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Demoted the kid verdict from proved to inconclusive_lean_proved:85 in parent review. The testable claim ends with "measured behaviourally, the next BUILD round dispatched under the new template ends with a non-empty git diff --stat" — a downstream measurement by design; no BUILD round has run under the new template yet. The kid itself scoped this honestly in its Evidence section; the demotion aligns the frontmatter with what the node already says. Parent re-verified everything in the worktree: diff present, gate discriminator exact (build: prefix), both tests pass, probe behaviour unchanged.
<!-- THOUGHT:END -->
