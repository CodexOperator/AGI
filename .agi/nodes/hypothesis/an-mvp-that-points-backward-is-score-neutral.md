---
id: hypothesis:an-mvp-that-points-backward-is-score-neutral
mint_id: 26e6de7bb1db44de80b24526bde4e796
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.85
edited_by: director
evidence_runs:
  - experiment:mvp-forward-backward-audit
scaffold_hash: efafa44d05812d01
scale: engine
testable_claim: An mvp minted for work already done (no forward-pointing source_files/build; body describes a finished change) does not raise outcome_coverage; the 9 mvps minted 2026-09-03 in iters 1012-1019 are audited against [mvp].md and any backward-pointing one is deprecated or excluded from scoring_mvp_count
thought_session: L1.08
title: An mvp that points backward is score neutral
verdict: proved
---
# hypothesis:an-mvp-that-points-backward-is-score-neutral

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
"Wave 3 of loop L1 (iters 1012-1019, 2026-09-03) minted 9 mvp nodes in one wave (mvp_count 39 -> 48; 47 after wave 4) and outcome_coverage rose 0.224 -> 0.255. [mvp].md says an mvp points forward -- it specifies a file that must satisfy something -- and the corpus proved it (source_files 0/26 on earlier mvps). If any of the 9 describe work already finished they are closures minted for score, the exact motion goal:g3 says cannot move scoring. Experiment: read each of a00-84f78e77, a00-bd00f723, a00-d164603e, a00-e284d9f5, a00-eeaa5239, a00-fc01ce13, a01-0e64d6a7, a01-708d8467, a01-e989877e against [mvp].md; classify forward/backward; for backward ones deprecate, or make metrics.py exclude mvps with no forward payload from scoring_mvp_count, with a red-on-purpose test. If all 9 are genuine, report that -- it is the finding."

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"Audited all 9 mvps against [mvp].md's forward-pointing rule, in-tree (grep for each named artifact, not the node body alone). 7 forward: no artifact exists yet, each body proposes a design or an unbuilt script/test. 2 backward: mvp:a00-e284d9f5-869c8c (derive-commands.py exists and its THOUGHT reports the artifact already verified -- script runs, --check exits 0, table matches) and mvp:a00-eeaa5239-8e388f (its THOUGHT reports the wiring already verified in-tree at post_wire.py:365/371 with 1382/1382 tests passing). Both underlying changes are real and worth keeping, so deprecation was not used -- the structural fix instead: metrics.py::goal_attribution now excludes an mvp from scoring_mvp_count when it has no source_files/payload_ref/build-child AND its body matches a verification-of-shipped-code pattern (_BACKWARD_MVP_RE: 'verified in-tree', 'the mechanism is real', an X/Y-pass or all-N-pass test count), emitting the excluded count as backward_mvp_count. Checked against the full 48-mvp corpus: exactly these 2 match, 0 false positives. scoring_mvp_count 47->45, outcome_coverage 0.245->0.234, backward_mvp_count=2. Confirmed the guard is load-bearing by reverting it and watching 3 of 7 new fixture tests go red (scoring_mvp_count, outcome_coverage, and the METRIC line all wrong), then restoring it green. Full suite 1389 passed, 0 failures."
<!-- THOUGHT:END -->