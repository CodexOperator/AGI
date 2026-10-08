---
id: goal:g7.33.19.1
mint_id: 2df06edbb7b84f6fa317f12eb52374bd
type: goal
parents:
  - goal:g7.33.19
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.33.19.1
goal_kind: subgoal
origin: goal
season: 2
seeds:
  - goal:g7.33.19
status: active
tags:
  - local-maxxing
  - engine
  - grid
title: "G7.33.19.1: `grid.py commit <payload path>` versions the build node that carries that payload (node.md + payload, ONE version) instead of skipping the path as not a node"
town: core
---
# goal:g7.33.19.1

## Why this exists
**Parent `goal:g7.33.19`** (engine findings, each its own sub-leaf when dispatched). The owner asked 10-03 01:5xZ whether a node's grid slot includes the file the node links to; DG1 verified it on 10-03 (310 of 310 live build nodes: grid tip tree == node + payload as on disk; scratch: payload-only edit = its own version). SM 02:2xZ found the one real gap on the v5 path: the HEAD tells v5 posts to version a change by PATH, and `grid.py commit <path>` takes only a NODE file: handed a payload path (extensions/agi/bin/x.py) it does not find a node to version (grid.py cmd_commit, the per-path loop skips a path with no id frontmatter). belam [decision] 02:2xZ 10-03: GO for ONE leaf + hypothesis; NO-GO for now on committing mvp source_files and on backfilling the 18 retired payloads (git history holds those bytes; that goes to the owner as an option).

## Target end-state
- `grid.py commit <path>` where <path> is a payload (a path some build node names as its `payload_ref`) versions THAT node: the same single version `grid.py commit <node file>` would make (node.md + payload in one tree), a payload-only edit included.
- A path that is neither a node file nor a node's payload is reported BY NAME (`ERR: no build node carries payload_ref <path>`) and the command exits non-zero, never skipped silently.
- `--all` and `commit <node file>` are unchanged.

## Invariants
- ONE version per node per commit: two paths naming the same node make one version; a path never writes a version of a node that does not carry it.
- No write outside refs/grid/*; the working tree is untouched (plumbing only); the evidence gate and the mint-id ref keying are the same ones the node path uses.
- No `.py` beyond grid.py and its test; sh + stdlib.

## Falsifier
1. In a scratch repo (the test): a build node with payload_ref extensions/x.sh; edit ONLY extensions/x.sh; `grid.py commit extensions/x.sh` = v2 with the new payload and the same node.md blob; the same call twice = no new version; `grid.py commit <node file>` after that = no new version (identical tree).
2. Negative: `grid.py commit extensions/nobody.sh` (no node carries it) exits non-zero naming the path; `git for-each-ref refs/grid | wc -l` unchanged.
3. `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/ -q -k grid` passes with the new cases.

## Out of scope
commit_file over mvp `source_files` and the 18 retired build nodes' missing payload versions (belam NO-GO 02:2xZ, to the owner as an option) · the grid cron and `--all` · goal:g7.33.19's other rows.

## Agent Notes
Assigned to **director-general-1**.
