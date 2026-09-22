---
id: experiment:a00-5dbbf4fb-dt87-residual-verify
mint_id: 30d495ca3c9142d5a8420ba7bc2efb76
type: experiment
parents:
  - hypothesis:a00-5dbbf4fb-4a7ce9
next_edges: []
edited_by: a00-5dbbf4fb
line_ceiling: 40
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 875ab84cf6b61e70
season: 2
title: "DT.87 residual verification: D1 already real at HEAD, D2 lands the dirty node files"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-5dbbf4fb-dt87-residual-verify

## Experiment
## Experiment

DT.87 residual VERIFICATION round on `goal:g7.31.3.1`, run in worktree
`a00-26b402eb` at HEAD `5f9f47bac` (the last kid's `proved` commit). The
dispatch brief handed me two defects — D1 a self-citation on
`hypothesis:a00-f46503aa-25f7eb`, D2 three node files left uncommitted. I
re-ran the whole DT.87 check myself rather than trust the inherited numbers.
**D1 is stale:** HEAD already carries a real experiment
(`experiment:a00-f46503aa-note-writers-under-heading`, committed in
`5f9f47bac`) and that hypothesis's `evidence_runs` points at it, not at
itself; only the stale `demote_reason`/`demoted_from` frontmatter lingers in
the working tree. So this node carries the verification and D2 (landing the
dirty node files in the round's own commit) is the live work.

### The shipped seam (verbatim, `extensions/agi/bin/node_writer.py:912`)

    NOTES_HEADING = "## Agent Notes"

    def merge_agent_notes(body: str, note: str) -> str:
        """Put `note` UNDER a line-anchored `NOTES_HEADING`, creating it if absent.

        Line-anchored: an inline mention inside THOUGHT prose is not a section.
        Inserted after the heading LINE, never at end of body -- appending puts
        the note after a trailing THOUGHT block, outside its own section.
        """
        lines = (body or "").rstrip().splitlines()
        for i, ln in enumerate(lines):
            if ln.strip() == NOTES_HEADING:
                return "\n".join(lines[:i + 1] + ["", note] + lines[i + 1:]) + "\n"
        return (body or "").rstrip() + f"\n\n{NOTES_HEADING}\n{note}\n"

`cli.py:58`, `post_wire.py:38` and `write.py:81` all alias it:
`NOTES_HEADING = node_writer.NOTES_HEADING`. `cli.py:2066`,
`post_wire.py:486` and `write.py:2317` all call `merge_agent_notes`.

### R1 — committed provenance

    $ git check-ignore -v .agi/sessions/workflows/runs/mur-g7-31-3-1-dt-36-748d4344ce2/review.json
    .gitignore:100:.agi/sessions/*	.agi/sessions/workflows/runs/mur-g7-31-3-1-dt-36-748d4344ce2/review.json
    $ git log -1 --format='%h %s' 88da0784c
    88da0784c director-belam §3d: g7.31.3.1 residue table after MUR DT.36 accept_with_residue

The old cite is unverifiable in a fresh checkout; the replacement commit
resolves and the two DT.36 rows are pasted in `goal:g7.31.3.1`'s residue table.

### R2/R3 — the four new regression tests, post-fix

    $ python3 -m pytest extensions/agi/tests/test_completion.py -q -k trailing_thought
    1 passed, 20 deselected, 3 warnings in 0.54s
    $ python3 -m pytest extensions/agi/tests/test_cli.py -q -k trailing_thought
    1 passed, 56 deselected, 3 warnings in 1.25s
    $ python3 -m pytest extensions/agi/tests/test_write.py -q -k 'inline_mention or before_a_trailing'
    2 passed, 117 deselected, 2 warnings in 0.39s

the test names are `test_the_note_lands_under_the_heading_not_after_a_trailing_thought`
(`test_completion.py:395`), `test_done_places_the_note_before_a_trailing_thought_block`
(`test_cli.py:195`), `test_an_inline_mention_of_the_heading_is_not_a_section`
(`test_write.py:408`) and `test_a_note_lands_before_a_trailing_thought_block`
(`test_write.py:432`). The last kid measured all four FAILING against the
reverted pre-fix writers (note index 517 > THOUGHT index 335; 0 line-anchored
headings on the inline case) and recorded that in
`experiment:a00-f46503aa-note-writers-under-heading`; this round confirms they
pass on the bytes at HEAD.

### Tip gates at my run time

    $ python3 extensions/agi/bin/links.py links
    links: 3862 resolved, 0 broken (18 retired payload(s), not damage)
    $ python3 extensions/agi/bin/evidence_gate.py enforce --dry-run --root .
    evidence-gate enforce: 0 unevidenced decisive verdict(s), 0 would demote, 0 refused
    $ git diff --numstat -- extensions/agi/bin/brief.py
    (empty)
    $ grep -c '^## Agent Notes' .agi/nodes/goal/g7.31.3.1.md
    1
    $ grep -c '^## Agent Notes' .agi/nodes/hypothesis/a00-f0d769b5-7a5ace.md
    1
    $ grep -c '^## Agent Notes' .agi/nodes/hypothesis/a00-f46503aa-25f7eb.md
    1

`links` grew 3860 -> 3862 because this round adds two nodes (the hypothesis
scaffold and this experiment); the count is live, not pasted. `brief.py` is
byte-unchanged.

### Full touched test files

    $ python3 -m pytest extensions/agi/tests/test_completion.py extensions/agi/tests/test_cli.py extensions/agi/tests/test_write.py -q
    1 failed, 196 passed, 139 warnings in 4.76s
    FAILED extensions/agi/tests/test_cli.py::test_done_auto_commits_parent_worktree

The single failure is the pre-existing environment gap (`git config --global
user.name` unset, so the test's `git merge` dies on committer identity); it
runs with `notes=""`, so it never enters the branch this round changed.

## Evidence

D1 verdict: **already satisfied on committed bytes** — the real experiment
exists at HEAD, `evidence_runs` is not self-referential, and the stale
`demote_reason: no experiment evidence (evidence_runs=0) for 'proved'` is
dropped in the working tree (it survives only in the last commit's
frontmatter; this round's `--owns` lands the drop). D2: the three dirty node
files named by the brief (`goal:g7.31.3.1`,
`hypothesis:a00-f0d769b5-7a5ace`,
`experiment:a00-f0d769b5-residual-close`) plus the stale-frontmatter
`hypothesis:a00-f46503aa-25f7eb` are all passed to `cli.py done --owns`, so
this round's scoped commit lands R1/R4/R5.

Production lines: **0** (this round changes no production file; the DT.87
engine fix is already committed in `7539f79d4`, and it measures 39 added / 32
removed against the 40-line ceiling).

Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This node exists so the DT.87 residual closure has an independently re-run experiment at HEAD 5f9f47bac, not just the last kid self-reported numbers. I re-ran the four regression tests, links.py, evidence_gate and the brief.py numstat myself. It also records that the brief D1 was stale (the real experiment already existed at HEAD) and that D2 (the dirty node files) is landed by this round --owns. Production lines 0; ceiling 40.
<!-- THOUGHT:END -->
