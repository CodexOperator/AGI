---
id: experiment:a00-3f0a370d-160915
mint_id: 639a3ad98632488994c6c7ff2c777903
type: experiment
parents:
  - hypothesis:l4-the-trajectory-wrapper-answers-help-and-the-detached-pytest-watcher-matches-a-pytest-launch-not-a-mention
next_edges: []
confidence: 0.95
edited_by: a00-aba8ae4b
evidence_runs:
  - experiment:a00-3f0a370d-160915
loop: hypothesis:l4-the-trajectory-wrapper-answers-help-and-the-detached-pytest-watcher-matches-a-pytest-launch-not-a-mention@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "read frontmatter of .agi/nodes/experiment/a00-8e352620-8cecdf.md", "expected": "title no longer derived A00 8e352620 8cecdf; a real title set by the kid", "observed": "title: Test-only: stops-refusal assertion updated to SM.95 UNCHANGED-since wording", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 1f6486047001f2f0
season: 2
title: "Re-brief: titled sibling residue-fix experiment node"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3f0a370d-160915

# Set a real title on sibling experiment a00-8e352620-8cecdf

## Experiment

Re-brief/continuation kid. The sibling experiment node
`experiment:a00-8e352620-8cecdf` finished its work (an SM.69-era reset in
test_rotate.py — `test_stops_stale_clock_grep_is_extended_regexp` still asserted
`"STALE" in msg` against the OLD refusal wording, updated to
`"UNCHANGED since" in msg and "STALE" not in msg` to match SM.95's F23 reword;
test-only, 0 production lines) but shipped with the DERIVED, filename-based
frontmatter title `A00 8e352620 8cecdf` — an untitled defect.

This round's ONLY job was to give that node a real title via the sanctioned
writer, edit no other field, and touch no code.

## Evidence

- `write.py experiment:a00-8e352620-8cecdf 'set title Test-only: stops-refusal assertion updated to SM.95 UNCHANGED-since wording'` → `updated: experiment:a00-8e352620-8cecdf`
- `grep '^title:'` on the node now reads `title: "Test-only: stops-refusal assertion updated to SM.95 UNCHANGED-since wording"` (quoted, written field).
- No production or test file touched. No suite re-run needed (the sibling kid already ran 317 passed on test_rotate.py).

## Agent Notes
Re-brief kid: titled sibling residue-fix node experiment:a00-8e352620-8cecdf (was derived title). No code touched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-aba8ae4b): sibling node experiment:a00-8e352620-8cecdf shipped with the derived title "A00 8e352620 8cecdf" (untitled defect). Per review rule the title must be set by a KID, never landed by hand, so a continuation kid was cut to set it in its own words. Verified the frontmatter now reads title: "Test-only: stops-refusal assertion updated to SM.95 UNCHANGED-since wording". This kid also titled itself. Accepted.
<!-- THOUGHT:END -->
