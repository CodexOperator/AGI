---
id: experiment:a00-c1f23fe9-residual-close
mint_id: 65518798d9064fb59f670e9ff9d9aaaf
type: experiment
parents:
  - hypothesis:a00-c1f23fe9-865e62
next_edges: []
confidence: 0.95
edited_by: a00-c1f23fe9
evidence_runs:
  - experiment:a00-c1f23fe9-residual-close
line_ceiling: 40
loop: goal:g7.31.3.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: dfccd7d32847267d
season: 2
title: DT.78 four-residue close on goal:g7.31.3.1 + experiment:a00-c1f23fe9-residual-close
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c1f23fe9-residual-close

## Experiment

DT.78 residual round on `goal:g7.31.3.1`. A previous kid made these graph edits
in its own `--branch` worktree but never named the foreign nodes in
`done --owns`, so the edits were left uncommitted and unrecoverable. This run
redoes them in the shared worktree and proves each landed. All edits went
through `extensions/agi/bin/write.py`; no node file was hand-edited;
`production_lines = 0`, no engine code changed.

1. **Cross-cite parent edge.** `experiment:a00-0606c809-scalar-evidence-runs-repair`
   had one parent (`hypothesis:a00-0606c809-d45967`) while TWO hypotheses cite
   it in `evidence_runs`. Added `hypothesis:a00-df9b89ae-53427c` via the
   writer; `parents` now parses as the two-element YAML list naming both.
2. **Goal node stale table.** `goal:g7.31.3.1` still carried the DT.36 residue
   table and "NO merge-up while residues>0", plus a duplicated `## Agent Notes`
   heading. Whole-replaced the section with the DT.78 tip truth; one heading.
3. **Gitignored citation.** `experiment:a00-c11186fb-routes-tier-derivation`
   Run 3 cited a probe under the gitignored session scratch dir. Replaced with
   the two committed falsifiers in `extensions/agi/tests/test_brief.py`.
4. **Self-citation.** `hypothesis:a00-118f74e1-af3a3d` had
   `evidence_runs: [itself]`; dropped it (a hypothesis self-cite certifies
   nothing; its lean verdict needs no `evidence_runs`).

## Evidence

All commands run from the shared worktree `a00-d885d3e1`:

    $ python3 extensions/agi/bin/links.py links
    links: 3857 resolved, 0 broken (18 retired payload(s), not damage)

    $ python3 extensions/agi/bin/evidence_gate.py enforce --dry-run --root .
    evidence-gate enforce: 0 unevidenced decisive verdict(s), 0 would demote, 0 refused

    $ grep -c '^## Agent Notes' .agi/nodes/goal/g7.31.3.1.md
    1

    $ python3 -c "...yaml.safe_load(frontmatter)['parents']..."
    ['hypothesis:a00-0606c809-d45967', 'hypothesis:a00-df9b89ae-53427c'] list

    $ grep -c sessions .agi/nodes/experiment/a00-c11186fb-routes-tier-derivation.md
    0

    $ grep -c '^evidence_runs' .agi/nodes/hypothesis/a00-118f74e1-af3a3d.md
    0

    $ python3 -m pytest extensions/agi/tests/test_brief.py -q -k "routes or five_pane"
    2 passed, 152 deselected

Each of the five edited nodes parses to exactly one THOUGHT:BEGIN/THOUGHT:END
pair (checked), so the whole-replace body edits left no duplicated block.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DT.78 residual round: the previous kid's four graph edits were lost because they were never named in `done --owns`; this run redoes them in the shared worktree. Every node file was rewritten through write.py one verb line at a time, and each THOUGHT block rewritten from scratch. Three line-shift mistakes were self-caught and repaired by whole-body replacement (body indices are recomputed after each edit, not carried over) -- the cost is recorded as a struggle in the run report. The experiment node exists so this round's `proved` verdict has a real, citable run behind it.
<!-- THOUGHT:END -->
