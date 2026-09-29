---
id: experiment:dg2b4-wg-baseline
mint_id: 140885c96a7a41d082c52f2076b5d5c4
type: experiment
parents:
  - hypothesis:goals-md-retires-with-every-caller-in-one-row
next_edges: []
edited_by: director-general-2
scaffold_hash: abf11504260cc836
season: 2
title: "W-G baseline: 6 live render/check callers (3 unmeasured: verification goals-check, commands.md cell, rotate render_check); smoke RED at HEAD, render cut -> exit 0, node_count 5132"
town: core
---
# experiment:dg2b4-wg-baseline

## Run (director-general-2, council bundle 4 stage 2, trunk 85246da86, 20:39Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | `git grep -n -e 'snapshot-goals' -e '--render' -e 'goals-check' -- extensions/agi/bin extensions/agi/driver.sh extensions/agi/workflows ':!extensions/agi/tests'` | 6 LIVE callers: driver.sh:238-241 (`--render --strict-goals`, every --smoke) · rotate.py:8754 PRIME step `render` (handler :9369-9389) · rotate.py:8733 WORKTREE step `render_check` (handler :9185-9196) · verification.py:70-73 `goals-check` in LEVELS quick/rotation/full (+ :15, :230, :249) · agi-round-review.js:40-41,50,64 · review.json:12,22,38. The hypothesis measured 3 (+ :9370-9386); `render_check` and `goals-check` were not listed |
| 2 | `git grep -n goals-check -- .agi/nodes/.geometry` ; crons.md, config.json | commands.md:26-32 (`goals-check` argv = `snapshot-goals.py --render --check`), :2754 (side_effects), :3158 (`workflows.verify`); commands.md:1895-1910 `snapshot-goals.py::` cell carries `render/check/from_doc` args (regenerated from argparse). crons.md + config.json: 0 hits (no cron renders; no goals_file cell set) |
| 3 | transitive (verification level quick/rotation) | rotate.py closeout `post_verify`/`suite` (`--level quick`, :9221) and `verify_stamp` (`--level rotation`, :9300) and rotate.py:12211 `VERIFICATION_LEVEL="quick"` all run goals-check; level `rotation`/`full` also runs `smoke` -> driver render |
| 4 | `git grep -n -e --from-doc -e from_doc -e unlink -- extensions/agi/bin/snapshot-goals.py` | :1123 flag, :1135/:1138 branch, :1256 unlink (as measured) + :637 docstring, :879 the render's own ERR text tells the reader to run `--from-doc` |
| 5 | `sed -n 72,85p node_writer.py` ; locations.py | reason comment :76-81 ("regenerates `nodes/goal/` from GOALS.md", :77), tuple :82. locations.py:85-86 DEFAULT_GOALS_FILE, `goals_path` :679-708 (cell read :706), readers: snapshot-goals.py:110/:178, locations.py:1186, verify_unified.py:340, unify.py:711 doc |
| 6 | `git grep -l GOALS.md` code / test / skills | 16 code files · 12 test files (incl. fixtures/make_shadow_fixture.sh) · 5 skills (agi, agi-goal, agi-master-gate, agi-node-write, agi-verify) + CLAUDE.md :4 :18 :27 :36 :46 :109-110 :117 + QUICKSTART.md :14 :106 :160 -- counts as measured. Render citations also at skills/agi/SKILL.md:168, agi-goal:23-24, agi-master-gate:33,35, agi-verify:19,37 |
| 7 | snapshot-goals non-render duties | `write_frontmatter`/`load_existing_nodes`/`_set_project_root` imported by 5 files (backfill-mint-ids, decompose-engine, level3, post_wire, snapshot-build-site) -> the file stays. `report_integrity` (--strict-goals) + `warn_premature_complete` (goal:s26) run ONLY inside cmd_render (:1078-1098): cutting driver.sh:240 drops both from --smoke |
| 8 | `bash extensions/agi/driver.sh --smoke --max-iters 1` in /tmp copy (HEAD archive, .agi/nodes + GOALS.md) | **exit 1, no node count**: render refuses `g4.18.5.1.md has no heading_level` -- 14 goal nodes lack it (g4.18.5.1-3, g4.18.6.1-5, g4.18.7.1-3, g7.16.1.4.1-3, all minted db3e22e55). `--render --check` exit 1 same reason |
| 9 | same smoke with driver.sh:238-241 commented out (probe copy, deleted after) | **exit 0**, `METRIC node_count=5132 active=4901 deprecated=231`; goal-node bytes hash unchanged (459 goal nodes), GOALS.md untouched |
| 10 | `write.py goal:g7.16.1.4.1 'read body 1:80'` | works: today's one goal read = `python3 extensions/agi/bin/write.py goal:<id> 'read body N:M'` (named at CLAUDE.md:4); goal:g4.18.7.3 moves that line with every teacher |
| 11 | baseline suites (one file each, tree copy, behind the lock) | test_snapshot_goals 86 passed · test_rotate_closeout_steps 42 passed · test_node_writer 108 passed (needs .agi/nodes in the copy) |
| 12 | `git show --stat 30f4db55f e662637ac` | both touch ONLY `.agi/nodes/goal/g7.16.1.3.md`: no code caller has been cut yet |

## What it shows
```
GOALS.md render/check  <-- driver.sh:240 (every --smoke; RED now: 14 goals lack heading_level)
                       <-- rotate PRIME "render" :8754   ┐ closeout
                       <-- rotate WORKTREE "render_check" :8733 ┘
                       <-- verification LEVELS goals-check <-- commands.md:26 cell <-- post_verify/suite/verify_stamp, `commands.py run verify`
                       <-- agi-round-review.js:64 + review.json
GOALS.md -> nodes      <-- --from-doc :1123/:1135, unlink :1256 (+ ERR text :879 points at it)
cut driver render  ==>  smoke exit 0, node_count 5132 (floor visible again); loses --strict-goals + s26 warning
```

## Test committed (strict xfail, RED until DG3 builds)
`test_snapshot_goals.py::test_wg_no_live_caller_renders_or_checks_goals_md` -- 6 caller files carry no render/goals-check; driver keeps emit_metrics; GOALS.md absent
`test_snapshot_goals.py::test_wg_from_doc_and_goals_file_retire` -- no --from-doc/from_doc in snapshot-goals.py; no DEFAULT_GOALS_FILE/goals_file in locations.py
`test_snapshot_goals.py::test_wg_reader_lines_only_point_at_the_retirement` -- CLAUDE.md, QUICKSTART.md, 5 skills: every GOALS.md/--render line is a retirement pointer
`test_rotate_closeout_steps.py::test_wg_closeout_has_no_render_step_or_check_gate` -- neither step list nor the seam table holds render/render_check
`test_node_writer.py::test_wg_goal_type_reason_no_longer_cites_goals_md_regeneration` -- node_writer no longer says goals regenerate from GOALS.md
