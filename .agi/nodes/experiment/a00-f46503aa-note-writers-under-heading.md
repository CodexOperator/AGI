---
id: experiment:a00-f46503aa-note-writers-under-heading
mint_id: feb74af564214479bcb18ddecb5a6695
type: experiment
parents:
  - hypothesis:a00-f46503aa-25f7eb
next_edges: []
edited_by: a00-f46503aa
line_ceiling: 40
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 39
profile: balanced
role: kid
scaffold_hash: c6637d31926252f1
season: 2
title: "DT.87 run: note writers insert under the heading, committed provenance, goal residue table"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-f46503aa-note-writers-under-heading

## Experiment

DT.87 residual round on `goal:g7.31.3.1`, run in worktree `a00-26b402eb`.
R1–R5, all four production files changed through the engine (no hand edits),
every node edit through `write.py`. This node is the citable run behind
`hypothesis:a00-f46503aa-25f7eb`.

1. **R1 — committed provenance.** The two DT.84 nodes cited
   `.agi/sessions/workflows/runs/mur-g7-31-3-1-dt-36-748d4344ce2/review_...json`,
   which `git check-ignore` confirms is hidden by `.gitignore:100`
   (`.agi/sessions/*`), so a fresh checkout cannot verify it. Both citations
   were replaced with the committed DT.36 table (commit `88da0784c`, resolved
   by `git log -1`) and its two rows pasted.
2. **R2 — note lands under the heading.** `cli.py` and `post_wire.py`
   appended the note at END OF BODY; with `## Agent Notes` mid-body and a
   THOUGHT block last, the note landed after the block. Both now call one
   shared `node_writer.merge_agent_notes`, which inserts after the heading
   LINE.
3. **R3 — write.py predicate.** `write.py` still used `if NOTES_HEADING in
   body:` (substring), so an inline mention of the heading inside THOUGHT
   prose was treated as a section. It now uses the same line-anchored helper.
4. **R4 — dedup and stale cites.** `NOTES_HEADING` is now declared once in
   `node_writer.py` and aliased by the other three writers; the stale `3858`
   counts in the two DT.84 nodes were aligned to the live `3860`; the
   hypothesis Mechanism prose was rewritten to the shipped shape.
5. **R5 — goal Agent Notes.** Whole-replaced (not appended) with a 12-row
   diagram-max residue table: DT.36 (2), DT.78 (2), DT.84 (2), DT.87 (6),
   exactly one row open (DT.36 schema-list note, OOS).

## Evidence

Pre-fix measurement: the append blocks in the three writers were reverted in
place to their pre-DT.87 shapes (post-fix copies saved first in
`.agi/sessions/iter-DT.87/a00-f46503aa/prefix-june/`, restored byte-for-byte
after), then:

    $ pytest extensions/agi/tests/test_completion.py -q -k trailing_thought
    FAILED ...::test_the_note_lands_under_the_heading_not_after_a_trailing_thought
    E   assert 517 < 335   # the note landed AFTER <!-- THOUGHT:END -->
    1 failed, 20 deselected

    $ pytest extensions/agi/tests/test_cli.py -q -k trailing_thought
    FAILED ...::test_done_places_the_note_before_a_trailing_thought_block
    1 failed, 56 deselected

    $ pytest extensions/agi/tests/test_write.py -q -k 'inline_mention or before_a_trailing'
    FAILED ...::test_an_inline_mention_of_the_heading_is_not_a_section
    E   assert len(headings) == 1   # pre-fix: 0 line-anchored headings, note bare
    FAILED ...::test_a_note_lands_before_a_trailing_thought_block
    2 failed, 117 deselected

Post-fix the same four pass. Full touched test files:

    $ python3 -m pytest extensions/agi/tests/test_completion.py extensions/agi/tests/test_cli.py extensions/agi/tests/test_write.py -q
    1 failed, 196 passed
    FAILED extensions/agi/tests/test_cli.py::test_done_auto_commits_parent_worktree

The one failure is a pre-existing environment gap (`git config --global
user.name` unset, so its `git merge` dies on committer identity); it runs with
`notes=""`, so it never enters the branch this round changed.

Tip gates and the R1 verification:

    $ git check-ignore -v .agi/sessions/workflows/runs/mur-g7-31-3-1-dt-36-748d4344ce2/review.json
    .gitignore:100:.agi/sessions/*	.agi/sessions/.../review.json
    $ git log -1 --format='%h %s' 88da0784c
    88da0784c director-belam §3d: g7.31.3.1 residue table after MUR DT.36 accept_with_residue
    $ grep -c '^## Agent Notes' .agi/nodes/goal/g7.31.3.1.md
    1
    $ grep -c '^## Agent Notes' .agi/nodes/hypothesis/a00-f0d769b5-7a5ace.md
    1
    $ git diff --numstat -- extensions/agi/bin/brief.py
    (empty)
    $ python3 extensions/agi/bin/links.py links
    links: 3860 resolved, 0 broken (18 retired payload(s), not damage)
    $ python3 extensions/agi/bin/evidence_gate.py enforce --dry-run --root .
    evidence-gate enforce: 0 unevidenced decisive verdict(s), 0 would demote, 0 refused

## Production lines

`git diff --numstat` over the four production files: 39 added, 32 removed
(`node_writer.py` 19/0, `cli.py` 7/12, `post_wire.py` 6/10, `write.py` 7/10).
Ceiling 40.
