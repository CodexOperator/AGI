---
id: experiment:dg2close-a00-edae0fba-940d3a-check
mint_id: 0ab6beeb062a4ef583b9001c04ca35d6
type: experiment
parents:
  - hypothesis:a00-edae0fba-940d3a
next_edges: []
edited_by: director-general-2
scaffold_hash: c18194e9cf8557da
season: 2
title: "Closing check: does scaffold-time seeding from dispatch context make a hypothesis schema-valid at birth (HEAD 2944fa423)"
town: core
---
# experiment:dg2close-a00-edae0fba-940d3a-check

Closing measurement of `hypothesis:a00-edae0fba-940d3a` at HEAD 2944fa423 (goal:s31 retired 09-30), read-only; code from a `git archive HEAD` tree in /tmp; probe in a /tmp fixture carrying HEAD's real `context/schemas/`.

| # | command | observed |
|---|---|---|
| 1 | `git grep -l 'hypothesis:a00-edae0fba-940d3a' -- .agi/nodes` | 2 experiments, 0 verdict nodes: `experiment:a00-4a304d3b-5931f3` (inconclusive_lean_proved:80) and `experiment:a01-de655bfd-635cd0` (disproved, 0.85, parent-reviewed). The node itself: `verdict: pending`, no `status` field |
| 2 | read `cli.py` `cmd_scaffold` (the dispatch-time scaffold) | calls `node_writer.write_node(root, type, slug, parents, bypass=…)` with NO `extra_fm`: nothing from dispatch context reaches frontmatter beyond what `seed_required` derives |
| 3 | read `node_writer.seed_required` (node_writer.py:1576-1586) | derives exactly one field: `title` from the slug (`_derive_title`); every other missing required field is returned, not filled |
| 4 | probe P1: `write_node(root,'hypothesis','probe-born-valid',['goal:s31'])` under HEAD `[hypothesis].md` (required `[id, type, mint_id, title, testable_claim]`) | `written`, `missing_required = ['testable_claim']`, `title = 'Probe born valid'`, stderr `SCHEMA-WARNING … not derivable at scaffold time (goal:s31)` -> the scaffold is NOT schema-valid at birth |
| 5 | probe P2 / P4 / P6: `completion.is_complete` untouched / body filled / after frontmatter lift | False / True / True; `scaffold_hash` unchanged by the frontmatter fill |
| 6 | `runpy.sh … test_completion.py` (archive tree, flock) | 18 passed |
| 7 | what "dispatch-time context" holds (node's own wording: target goal id, agent iteration tag) | no claim text; the only way to make `testable_claim` present at birth from it is a fabricated value, which the sibling `hypothesis:born-valid-without-touching-frontmatter` lists as its disproof ("any field filled with a placeholder") |
