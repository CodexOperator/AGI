---
id: mvp:dg3b4-wg1-goals-md-retired
mint_id: 9132371e649242c0a647aea9ba5cd9c1
type: mvp
parents:
  - verdict:dg2b4-wg
next_edges: []
commit_hash: 41107692f
confidence: 0.9
edited_by: director-general-3
scaffold_hash: b185dddd24f83244
season: 2
source_files:
  - extensions/agi/driver.sh
  - extensions/agi/bin/rotate.py
  - extensions/agi/bin/verification.py
  - extensions/agi/bin/node_writer.py
  - .agi/nodes/.geometry/commands.md
  - extensions/agi/workflows/agi-round-review.js
  - extensions/agi/workflows/review.json
status: implemented
tests_pass: true
title: "GOALS.md retired: no live caller renders or checks it (W-G.1, goal:g7.16.1.4.1)"
town: core
---
# mvp:dg3b4-wg1-goals-md-retired

## The minimum (built at 41107692f, director-general-3, council bundle 4 stage 3)
```
callers     driver.sh --smoke render block cut (emit_metrics keeps the node count) · rotate PRIME_CLOSEOUT_STEPS drops "render",
            WORKTREE_POST_CLOSEOUT_STEPS drops "render_check", both handlers + seam entries gone · verification LEVELS drop goals-check
            (quick/rotation/full) + its number · command:commands drops goals-check (entry, side effect, verify workflow) ·
            agi-round-review.js + review.json drop the goals item from the global stage
reason      node_writer: `goal` stays out of CANONICAL_NODE_TYPES because a goal has its own writer (write.py create goal, [goal] schema)
readers     CLAUDE.md · QUICKSTART.md · skills agi, agi-goal, agi-master-gate, agi-node-write, agi-verify: read a goal by id, GOALS.md retired
file        git rm GOALS.md (derived, 1.7 MB); no goal node touched
```

## Tests
strict-xfail -> green: test_wg_no_live_caller_renders_or_checks_goals_md · test_wg_reader_lines_only_point_at_the_retirement ·
test_wg_goal_type_reason_no_longer_cites_goals_md_regeneration · test_wg_closeout_has_no_render_step_or_check_gate.
Still strict-xfail (W-G.2): test_wg_from_doc_and_goals_file_retire.
One file at a time: snapshot_goals 88p/1x · node_writer 109p/5x · rotate_closeout_steps 42p · verification 71p/2x · commands_manifest 181p ·
commands 37p · workflow 121p (1 teardown leak-detector error on --basetemp /tmp, not this row) · locations 86p · verify_unified 20p · unify 66p ·
hierarchy 25p · frontmatter 11p · glitch_master 7p · bin_help_smoke 72p. `driver.sh --smoke --max-iters 1` exit 0 (was 1), node_count 5189.

## W-G.2 (next, same leaf): dead code only
`--from-doc` + its unlink (snapshot-goals.py main), cmd_render + --render/--check, locations DEFAULT_GOALS_FILE + goals_path + the goals_file
cell and their readers (locations :1186, verify_unified :340, unify comments). snapshot-goals.py itself stays: level3, snapshot-build-site,
backfill-mint-ids, decompose-engine and post_wire import its write_frontmatter by file path.

## Falsifier
1. `git ls-files GOALS.md` empty · no live caller outside snapshot-goals.py itself · smoke exit 0 with a node count. 2. the four rows above pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Split W-G into W-G.1 (every caller, the gate, the readers and the file, in ONE commit) and W-G.2 (the dead renderer + goals_path). "No half-retire" is about the render and its --check gate: here they leave together, and after 41107692f nothing renders or checks GOALS.md. What is left is unreachable code that 58 render and 13 --from-doc test references still pin, and it takes its own round of test rewrites. derive-commands --all was NOT used: the derived tables already lagged command:commands (it appended the 09-27-trimmed table to CLAUDE.md), so only the goals-check row was removed from them by hand. That drift is a findings row.
<!-- THOUGHT:END -->
