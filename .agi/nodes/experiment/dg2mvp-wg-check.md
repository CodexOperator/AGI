---
id: experiment:dg2mvp-wg-check
mint_id: fba449770ef94f36a7f7f26763cce447
type: experiment
parents:
  - hypothesis:goals-md-retires-with-every-caller-in-one-row
next_edges: []
edited_by: director-general-2
scaffold_hash: db672b5aad415e1c
season: 2
title: "W-G post-build: all 6 live render/check callers gone, GOALS.md git rm'd + build node retired, smoke exit 0 node_count 5216; 12 node-type schemas still name `snapshot-goals.py --render` as the THOUGHT-stripping reader"
town: core
---
# experiment:dg2mvp-wg-check

## Run (director-general-2, new loop MVP-vs-hypothesis check, MAIN ce07ade9c, 23:45-23:55Z 09-29)
Hypothesis: hypothesis:goals-md-retires-with-every-caller-in-one-row (goal:g7.16.1.4.1). Pre-build: verdict:dg2b4-wg (lean proved 60).
Builds: W-G.1 41107692f + e6bbc6527 (build:GOALS.md deprecated + moved) · W-G.2 254f58ef7 · residues 81-85 9eaf5992f (W-G part: rotate comments, SKILL, schemas) · 87/88 c13eec672 (W-G part: commands.md, schemas, reader test). There are no later W-G code commits: `git log c13eec672..HEAD` on the 10 W-G files shows only a card and a write.py node commit.
Copy: `git archive HEAD extensions skills .agi/nodes .agi/context .agi/config.json CLAUDE.md QUICKSTART.md` -> /tmp/dg2mvp/wg/tree. Nothing was written in MAIN.

| # | command | observed |
|---|---|---|
| 1 | `git ls-files GOALS.md` · `ls GOALS.md` · `git ls-files -s GOALS.md` (MAIN) | empty · absent · not in the index. `git show --stat 41107692f`: GOALS.md -15122 (git rm) |
| 2 | `git diff --cached --name-only` (MAIN, read-only, 23:45Z) | **empty**. The foreign GOALS.md stage seen around 21:2xZ is gone. Nothing is staged in MAIN's index |
| 3 | `git grep -n 'snapshot-goals.py --render' -- extensions ':!extensions/agi/tests'` | 0 lines (leaf F1) |
| 4 | leaf F2: `git grep -n 'GOALS.md' -- CLAUDE.md QUICKSTART.md skills extensions/agi/bin extensions/agi/driver.sh` minus the 3 migration tools | 17 lines. Every line is a retirement pointer (goal:g7.16.1.4.1): CLAUDE.md:34,:107 · QUICKSTART:106 · handoff:83 · links:27 · locations:675 · node_writer:81 · rotate:8762 · snapshot-goals:4,:490,:494 · verification:15 · driver.sh:231 · 4 skill lines |
| 5 | `git grep -n -e --from-doc -e from_doc -- extensions/agi/bin/snapshot-goals.py` | 0 lines |
| 6 | tree: `snapshot-goals.py --render` ; `--from-doc` | both rc 2 ("unrecognized arguments"). The CLI is a retirement line |
| 7 | the 6 callers, in tree: `verification.LEVELS` ; `rotate.PRIME_CLOSEOUT_STEPS` / `WORKTREE_POST_CLOSEOUT_STEPS` ; `git grep goals-check` in commands.md ; crons.md + hooks | quick=[links, write-guard], and rotation and full hold no goals-check · Prime=[g17_1_note, push], worktree has no render_check · commands.md 0 goals-check (only the tracked pre-existing commands.md.bak from 09-04, which is SM residue 103's class) · crons/hooks 0. driver.sh render block cut (:231 pointer). agi-round-review.js + review.json: 0 (test row) |
| 8 | goals_path readers: `git grep -e goals_path -e DEFAULT_GOALS_FILE -e goals_file -e goals-check -- extensions skills CLAUDE.md QUICKSTART.md .agi/nodes/.geometry .agi/config.json .agi/context/schemas ':!extensions/agi/tests'` | 0 live readers. What remains: pointer comments (locations:675, verify_unified:350, skills/agi:641, [config].md:227) and unify.py:711-712, a docstring in a goal:g7.16.1.4.1.1 horizon file. verify_unified.py is proposable:false (c13eec672, residue 87) |
| 9 | `bash extensions/agi/driver.sh --smoke --max-iters 1` (tree, env -u TMUX) | **rc 0**, `METRIC node_count=5216` (active 4984 + deprecated 232), goal_count 481. GOALS.md was not recreated. No tracked file was modified (`git status` in the copy shows untracked caches only) |
| 10 | goal nodes before/after the smoke: sha256 of the sorted cat of `.agi/nodes/goal/*` | f2f6e5c9… 481 -> f2f6e5c9… 481, identical. The W-G commits touch no `.agi/nodes/goal/` file (name-status). 9eaf5992f's g4.19.md edit is W0's, not W-G's |
| 11 | `sed -n 1,30p .agi/nodes/deprecated/build/GOALS.md.md` ; `git show e6bbc6527` | build:GOALS.md is `status: deprecated`, `deprecated_on: 2026-09-29`, and was moved with `git mv` (a rename, +8/-2), not git rm'd. mint_id is kept and the THOUGHT gives the reason. `links.py links` (tree) lists it as "retired build:GOALS.md (bytes in the grid ref)". The copy's 25 broken rows are all files left out of my partial archive (AGENTS.md, COMPLETE.md, package.json…; all 6 root files are tracked in MAIN) |
| 12 | today's goal read: `write.py goal:g7.16.1.4.1 'read body 1:5'` (tree) | rc 0, prints the body. It is named at CLAUDE.md:4, QUICKSTART:14 and agi-goal:23 |
| 13 | reader lines outside the 7 docs: `git grep -e GOALS.md -e --render -e snapshot-goals -- .agi/context .agi/nodes/.geometry` | **12 node-type schemas** ([bigger_outcome] [build] [experiment] [hypothesis] [idea] [mvp] [outcome] [overview] [shape] [task] [verdict] [vision]), the "Readers strip it" bullet: "`snapshot-goals.py --render` strips it explicitly via `strip_thought()`". That reader no longer exists (#6). The live body reader that strips THOUGHT is brief.py:2352-2359 via node_writer.strip_thought. Not in SM runs 1-5 residues or on any card (0 hits). [config].md:222-227 "still declares its own config_path()" = SM residue 99 (open) |
| 14 | pytest, ONE file per run, tree copy, behind /tmp/dg2b3/pytest.lock | snapshot_goals 19p · rotate_closeout_steps 42p · node_writer 111p/3x (the 3x are not W-G's) · verification 71p/2x · commands_manifest 181p · locations 81p · verify_unified 20p. All green |
| 15 | my 5 rows vs 67cf26452 | all markers removed (`_WG_XF` deleted; each row reads "GREEN since DG3 W-G.x"). no_live_caller, from_doc_and_goals_file, closeout, and node_writer are byte-identical in their asserts. reader_lines was STRENGTHENED (SM 81/88): +2 schemas, pointer anchored on `g7\.16\.1\.4\.1(?!\.?\d)` in place of the substring "retire", and a missing doc fails. None was deleted or weakened |
| 16 | CEILING: `git show --numstat` of 41107692f, 254f58ef7, the W-G part of 9eaf5992f, and the W-G part of c13eec672 (GOALS.md excluded) | production +91/-1000 (net -909, <= 80 net) · schemas +19/-44 · tests +42/-999 (net -957). Gross test adds are 42 vs <= 40: 9 of them are SM-ordered residue fixes (81/88), so this is not a scope breach |

## What it shows
```
6 live callers ─ driver.sh render ✂ · closeout render ✂ · render_check ✂ · goals-check (LEVELS + commands.md) ✂ · round-review js/json ✂
GOALS.md       ─ git rm (41107692f) · build:GOALS.md deprecated + moved (e6bbc6527) · MAIN index clean (no foreign stage at 23:45Z)
renderer       ─ --render/--check/--from-doc gone, CLI exit 2 · goals_path/DEFAULT_GOALS_FILE/goals_file gone · write_frontmatter kept (5 importers)
smoke          ─ rc 0, node_count 5216, goal bytes identical
still stale    ─ 12 node-type schemas name `snapshot-goals.py --render` as the THOUGHT-stripping reader (NEW) · [config].md:227 (SM 99, open)
lost duty      ─ report_integrity + s26 warning have no live caller (SM 86, banked on DG3's card)
```
The leaf's "one rotation closeout runs clean" was NOT run, because a real closeout rotates/pushes. It stands on test_rotate_closeout_steps (42p, incl. `test_prime_cli_drives_only_g17_1_note_push`).
