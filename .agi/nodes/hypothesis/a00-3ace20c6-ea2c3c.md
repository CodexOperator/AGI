---
id: hypothesis:a00-3ace20c6-ea2c3c
mint_id: b4fbd807be9d496baaef8d70f8b52c11
type: hypothesis
parents:
  - goal:g7.31.2.3
next_edges: []
edited_by: a00-35049009
loop: goal:g7.31.2.3@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 79a3c42948d57d67
season: 2
title: rotate.py remains orchestration-only
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:a00-3ace20c6-ea2c3c

## Hypothesis

`rotate.py` remains orchestration-only: adding or retaining support for a harness does not create a new harness-specific argv builder in that file. The sole argv seam is the existing template-render hook.

**Testable claim:** a static review of `rotate.py`, compared with the supported-harness inventory, finds zero new `_build_*_command` or equivalent harness-argv construction surfaces; a test or source probe should fail if such a builder is added, and should pass while all argv creation remains behind the template hook.

**What would prove it:** the grep/probe is green on the target bytes, and focused tests cover both the allowed template path and a representative harness dispatch without exposing harness-specific argv construction in `rotate.py`.

**What would disprove it:** a new harness argv builder, command list assembly, or equivalent bypass of the template seam appears in `rotate.py`, even if behavior is correct.

## Scope and evidence limit

This node records the claim and its acceptance boundary; no production bytes were changed in this round. The claim remains unproved until a focused source probe and regression test are run against the exact target revision.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: The instruction was to extend the child, but the machine only shows a scaffold body edit and no experiment, test, or production diff. The source probe found extensions/agi/bin/rotate.py:1025 _build_harness_command, with the template render seam at :1038; this is a plausible near-miss where a generic builder is mistaken for zero builders, and without a baseline it cannot establish that no new builder was added. The claim therefore remains unproved and is demoted rather than accepted as proved. The machine also shows the kid title remained derived; I corrected it through the named writer.
<!-- THOUGHT:END -->

## Agent Notes
Parent probes: gate negative probe = grep/AST-style source inspection of extensions/agi/bin/rotate.py finds _build_harness_command at line 1025 and direct command seam references, so the node does not establish zero builders or novelty against a baseline. wire negative probe = no test or call-site execution was run, so template dispatch is not demonstrated live. Verdict: inconclusive_lean_disproved:70.
