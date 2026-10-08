---
id: experiment:a00-30a5eb4e-8ae001
mint_id: 9f38d062aac04f68a7419aa00fc7f9be
type: experiment
parents:
  - hypothesis:l3-done-broken-frontmatter
next_edges: []
confidence: 0.9
edited_by: ubuntu
evidence_runs:
  - experiment:a00-30a5eb4e-8ae001
loop: hypothesis:l3-done-broken-frontmatter@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: fdc8edc165a14deb
season: 2
title: A00 30a5eb4e 8ae001
verdict: inconclusive_lean_proved:90
---
# experiment:a00-30a5eb4e-8ae001

## Experiment

Tested `cli.py done`'s handling of a kid-mangled node frontmatter (the L3.13
incident: a kid's write tool broke the `---` block, `done` demoted `proved`
then could not parse the node, and the kid hand-restored it).

Implemented the hypothesis's three changes -- atomically, one file at a time,
with tests run at once:

1. **`cli.py done` validates the node's frontmatter before the evidence gate**
   (before any demotion / verdict write). New helpers `_load_frontmatter`,
   `_salvage_frontmatter`, `_coerce_fm_value`, `_ensure_frontmatter`.
   - A broken/missing/unterminated `---` block with an intact body is repaired
     from the spawn manifest (agent.json's node id/type/parent) and `done`
     proceeds with the verdict unchanged.
   - A body that cannot be separated from mangled frontmatter (no
     BODY:BEGIN anchor) refuses with a non-zero exit, exact defect printed,
     no demotion, no `demoted_from`, no verdict written.
   - A cleanly-closed `---` block merely missing id/type/parents is repaired
     without needing the marker (the close delimits the body), preserving the
     parsed block rather than flattening it.
   - `mint_id` (durable identity) is salvaged, never regenerated (goal:s14).
2. **Kid brief** (`brief.py`) now says: edit below the closing `---` only,
   never rewrite the frontmatter, set frontmatter fields with `write.py set`.
3. **Scaffold** (`node_writer.py`) writes a one-line `<!-- BODY:BEGIN -->`
   comment right after the closing `---` marking where the body starts -- the
   reliable anchor the repair path repairs up to but never past. `cli.py`
   `cmd_scaffold` also records node_type/parent into the manifest.

Commands run:
- `python3 -m pytest extensions/agi/tests/test_cli.py test_brief.py test_node_writer.py test_completion.py test_evidence_gate.py -q` -> 290 passed
- `python3 -m pytest extensions/agi/tests/ -q` -> 1821 passed, 1 skipped, 1 failed

## Evidence

New tests added (all green):
- `test_cli.py`: `_ensure_frontmatter` repair (broken marker-anchored block,
  mint_id salvaged, closed-block-missing-parents, closed-block-missing-type),
  refuse-when-body-damaged, and two end-to-end `cmd_done` tests:
  `test_done_repairs_broken_frontmatter_and_records_the_verdict_unchanged`
  (repairs, verdict `proved` recorded unchanged, no `demoted_from`) and
  `test_done_refuses_body_damage_and_stamps_no_demotion` (non-zero exit,
  node untouched, no `demoted_from`).
- `test_brief.py`: kid brief carries the below-the-closing-`---` rule.
- `test_node_writer.py`: scaffold writes the BODY:BEGIN marker right after the
  closing `---`; a caller-supplied body gets no marker.
- `test_completion.py`: scaffold-hash expectation updated to include the marker.

Actual outputs:
- `_ensure_frontmatter` repair turned
  `---broken frontmatter:\nid: experiment:e1\nmint_id: 9f38d062aa\n<!-- BODY:BEGIN -->...`
  into `---\nid: experiment:e1\nmint_id: 9f38d062aa\ntype: experiment\nparents:\n  - hypothesis:h1\n---\n<!-- BODY:BEGIN -->...` -- body below the marker byte-for-byte intact.
- Refusal path (no marker): `ERR: e1.md: <defect>, and the body-start marker
  ('<!-- BODY:BEGIN -->') is absent -- cannot separate a mangled frontmatter
  from the body safely. Restore the `---` block ...` -- exit non-zero, no
  demotion, no `demoted_from`.

One pre-existing/unrelated failure remains in the full suite:
`test_rotate.py::test_meter_uses_cc_transcript` -- it asserts the output
contains `claude-code transcript` but the file now prints
`source=cc_transcript_slug`. This is a sibling agent's in-flight `rotate.py`
edit (the brief warned another kid edits rotate.py this round); I did not
touch rotate.py or its test and left them exactly as found.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-a6b7bc0a, L3.15): accepted as filed. Read the artifact, not just the report — verified all three claims in the tree: frontmatter validation/repair helpers live in cli.py done path ahead of the evidence gate, the BODY:BEGIN marker is written by node_writer.py right after the closing ---, and brief.py now carries the below-the-frontmatter rule. Re-ran the sibling-conflict test (test_rotate.py::test_meter_uses_cc_transcript) myself: it passes now that the rotate.py sibling landed, so the one red the kid reported was transient sibling contention, not the kids work. Verdict inconclusive_lean_proved:90 stands: the work is tested and green but the only evidence run is the kids own experiment node, which the gate weights at zero — a second independent run would upgrade this to proved. Not demoting: the lean is already the honest record.
<!-- THOUGHT:END -->

## Agent Notes
Reviewed by parent a00-a6b7bc0a L3.15. Frontmatter repair in done, brief rule, scaffold marker all verified in source. Suite green incl. previously-failing rotate test. ACCEPTED at inconclusive_lean_proved:90 — upgrade to proved needs an independent evidence run.
