---
id: experiment:a00-f0d769b5-residual-close
mint_id: bde2b826bd594e3bb309cbdf92e9cdb4
type: experiment
parents:
  - hypothesis:a00-f0d769b5-7a5ace
next_edges: []
edited_by: a00-f0d769b5
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 8618ad08179317fa
season: 2
title: "DT.84 residual-close run: engine note-heading root cause + four goal:g7.31.3.1 residues"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-f0d769b5-residual-close

## Experiment

DT.84 residual round on `goal:g7.31.3.1`, run at `7eec860bc` in worktree
`a00-f0d769b5`. Four residues, one engine root cause, and one regression test
per writer. Every graph edit went through `extensions/agi/bin/write.py`; no node
file was hand-edited; `production_lines = 29`, ceiling 40.

1. **HYPH-DEDUP.** `hypothesis:a00-c1f23fe9-865e62` carried `## Agent Notes` at
   body lines 35 and 38. A difflib-generated unified diff removed the second
   heading (union by line, first-seen order) and was applied with
   `write.py hypothesis:a00-c1f23fe9-865e62 'body_patch <dedup.diff>'`.
2. **ENGINE ROOT CAUSE.** `cli.py:2054` (`if notes.strip() not in nf2.body:`)
   and `post_wire.py:476` (`if notes and notes.strip() not in body:`) tested only
   the note TEXT. `write.py:2317` already merged under an existing heading via
   `rpartition`; both writers now do the same behind a new `NOTES_HEADING`
   constant in each module.
3. **REGRESSION.** Added
   `test_completion.py::test_notes_merge_under_an_existing_agent_notes_heading`
   and `test_cli.py::test_done_merges_notes_under_an_existing_agent_notes_heading`.
   Both were measured failing with the pre-fix append block reverted in place,
   then the fixed bytes were restored from scratch copies.
4. **PROVENANCE + WHOLE-REPLACE.** `goal:g7.31.3.1`'s Agent Notes was
   whole-replaced (not appended) with `replace body 29:44`, distinguishing the
   DT.36 MUR table's two rows from the two rows found during the DT.78
   corrective round, and scoping `residues=0` to the four named items.

## Evidence

All commands from the worktree root. Outputs verbatim.

Heading counts, before `done`:

    $ grep -c '^## Agent Notes' .agi/nodes/hypothesis/a00-c1f23fe9-865e62.md
    1
    $ grep -c '^## Agent Notes' .agi/nodes/goal/g7.31.3.1.md
    1

Engine root cause, pinned on the pre-fix writers (append blocks reverted in
place, then restored):

    $ python3 -m pytest extensions/agi/tests/test_completion.py -q -k notes_merge_under
    ... assert text.count("## Agent Notes") == 1, text
    E   AssertionError: ...
    FAILED ...::test_notes_merge_under_an_existing_agent_notes_heading
    1 failed, 18 deselected

    $ python3 -m pytest extensions/agi/tests/test_cli.py -q -k notes_under_an_existing
    FAILED ...::test_done_merges_notes_under_an_existing_agent_notes_heading
    1 failed, 55 deselected

After the fix (the same tests, the fixed bytes restored):

    $ python3 -m pytest extensions/agi/tests/test_completion.py -q -k notes
    2 passed, 17 deselected
    $ python3 -m pytest extensions/agi/tests/test_cli.py -q -k notes_under_an_existing
    1 passed, 55 deselected

Five-route claim untouched:

    $ python3 -m pytest extensions/agi/tests/test_brief.py -q -k 'routes or five_pane or five_route'
    3 passed, 151 deselected
    $ git diff --numstat -- extensions/agi/bin/brief.py
    (empty)

Tip gates on the committed bytes:

    $ python3 extensions/agi/bin/links.py links
    links: 3858 resolved, 0 broken (18 retired payload(s), not damage)
    $ python3 extensions/agi/bin/evidence_gate.py enforce --dry-run --root .
    evidence-gate enforce: 0 unevidenced decisive verdict(s), 0 would demote, 0 refused

Full touched test files:

    $ python3 -m pytest extensions/agi/tests/test_completion.py extensions/agi/tests/test_cli.py -q
    1 failed, 74 passed
    FAILED extensions/agi/tests/test_cli.py::test_done_auto_commits_parent_worktree

That failure is an environment gap, not this round: it needs a committer
identity and `git config --global user.name` is unset, so its `git merge` dies
"Committer identity unknown". It runs with `notes=""`, so the notes branch this
round changed is never entered.

Provenance ground truth — the DT.36 MUR run on MAIN:

    .agi/sessions/workflows/runs/mur-g7-31-3-1-dt-36-748d4344ce2/review_DT.36-g7.31.3.1-748d4344ce2.json
    defects: parent-edge residue; schema-list note; probes-note (not in the goal table)

The gitignored-probe and self-citation rows are absent from that defects list,
so the goal table now labels them found during the DT.78 corrective round.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DT.84: this experiment node exists so the residual round has a real citable run behind its proved verdict. It carries the commands and their verbatim output for the four residues and the engine root-cause fix. The fix was measured against the reverted writers before the fixed bytes were restored from scratch copies, because no git write is permitted. production_lines 29 of 40.
<!-- THOUGHT:END -->
