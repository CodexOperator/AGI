---
id: hypothesis:pb3-commands-bak-retired-by-move
mint_id: 34c5109df0384026a02e9319edc9f6bd
type: hypothesis
parents:
  - goal:g1.31.1.2
next_edges: []
edited_by: director-general-6
scaffold_hash: dfdcbd95c9a5c91e
season: 2
testable_claim: "`.agi/nodes/.geometry/commands.md.bak` is untracked there and tracked byte-identical at `.agi/nodes/deprecated/command/commands.md.bak` (a move, never git rm), no `.agi/nodes/.geometry` file carries goals-check, and no code reads the .bak."
title: commands.md.bak is retired by git mv to deprecated/command/, bytes unchanged; no .geometry file carries goals-check
town: core
---
# hypothesis:pb3-commands-bak-retired-by-move

## Measured
HEAD 4b343f8e6.
```
.agi/nodes/.geometry/commands.md.bak   tracked (git ls-files = 1)   198 lines   last touched 68ac0e13e (a perf run, not a node write)
  frontmatter        id: command:commands · type: command · mint_id == .geometry/commands.md's   (a second carrier of one mint)
  retired command    goals-check (commands block + a group list)   GOALS.md retired, goal:g7.16.1.4.1
.agi/nodes/.geometry/commands.md       3262 lines, no goals-check                                  the ONE live declaration (commands.py COMMANDS_NODE_REL)
readers of the .bak                    0 code: rotation_record.grep_live and verification's node walk read *.md only;
                                       graph_builder SKIP_SUFFIXES skips .bak; test_links.py pins "a .bak never carries a mint".
                                       Prose only: experiment:a00-dadbc358-c58718 (lists it), card-director-general-6, goal:g1.31.1.2.
.agi/nodes/deprecated/                 build doc experiment hypothesis idea task verdict — no command/ yet
```
Choice: `git mv` to `.agi/nodes/deprecated/command/commands.md.bak`, bytes untouched. Reason: CLAUDE.md "Retire, never delete" + the `deprecated/<type>/` convention keyed by the file's own `type: command`; `git rm` is banned under `.agi/nodes`; editing it to strip goals-check would rewrite a retired record. Not a `*.md` node file, so no counter moves (`active_node_count + deprecated_node_count` unchanged) and find_node_file / grep_live never read it at its new path either.

## CLAIM
(1) `.agi/nodes/.geometry/commands.md.bak` is untracked at that path and tracked, byte-identical (same blob), at `.agi/nodes/deprecated/command/commands.md.bak`.
(2) No tracked `.agi/nodes/.geometry/` file carries `goals-check`.
(3) Nothing reads the .bak: no code path names it; node counts and `links.py links` broken = 0 are unchanged across the move.

## Dispatch line
config-max: none. template-max: none. code: none — one `git mv` by exact path (not a node, so not a write.py verb; `write.py` owns `*.md` nodes only), committed alone, then `grid.py commit --all` (a no-op for a non-node is expected; record it).

## FALSIFIERS
- `git ls-files .agi/nodes/.geometry/commands.md.bak` non-empty, or `git ls-files .agi/nodes/deprecated/command/commands.md.bak` empty.
- `git rev-parse HEAD~1:.agi/nodes/.geometry/commands.md.bak` != `git rev-parse HEAD:.agi/nodes/deprecated/command/commands.md.bak` (bytes changed in the move).
- `git grep -n 'goals-check' -- .agi/nodes/.geometry` hits.
- `git grep -n 'commands\.md\.bak' -- extensions skills src` hits a code reader.
- `active_node_count + deprecated_node_count` (smoke metrics) or `links.py links` broken differ before vs after.
- `git log --diff-filter=D --name-only -1` shows the .bak deleted without an added twin (a `git rm`, not a move).

## TESTS
```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_links.py extensions/agi/tests/test_metrics.py extensions/agi/tests/test_commands.py -q --basetemp /tmp/pb3bak
python3 extensions/agi/bin/links.py links                 # broken = 0, before and after
bash extensions/agi/driver.sh --smoke --max-iters 1       # node count must not drop
```
No new test: the falsifier is the git ls-files / rev-parse pair above, run at the merge-up.

## FILE SCOPE
.agi/nodes/.geometry/commands.md.bak -> .agi/nodes/deprecated/command/commands.md.bak (one rename; nothing else)

## CEILING
kids ≤ 1 · 0 production lines · 0 test lines · pi-free parents · 0 USD · a director-closed node-answer (one commit); over it (any content edit): stop, bank
