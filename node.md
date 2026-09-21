---
id: experiment:a00-6600df76-a6b3c4
mint_id: 6f11606a4cda42af916c090a0ae2a04a
type: experiment
parents:
  - hypothesis:l4-find-root-sh-is-bounded-like-its-python-half
next_edges: []
confidence: 0.85
edited_by: a00-46d77ded
evidence_runs:
  - experiment:a00-6600df76-a6b3c4
loop: hypothesis:l4-find-root-sh-is-bounded-like-its-python-half@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3ba1770512cc935e
season: 2
title: A00 6600df76 a6b3c4
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6600df76-a6b3c4

## Experiment
# experiment:a00-6600df76-a6b3c4

## Experiment

g15 CLAIM (`hypothesis:l4-find-root-sh-is-bounded-like-its-python-half`) — behaviour to BUILD, not measure. The bash half `lib/find-root.sh` walked its upward loop all the way to `/`, while the python half `locations.find_project_root` broke at the first `.git` boundary after probing `.agi`/config at that level. `test_bash_and_python_agree` (test_locations.py:371) stayed green only because no shape ever exercised the nested-git case.

**Pre-fix reproduction** (temp tree: outer repo with `.agi/config.json`, nested `git init` at `outer/inner` with NO `.agi`, deep child `outer/inner/deep/child`):

| path | bash find-root.sh | python find_project_root |
|---|---|---|
| deep child | `/tmp/.../outer/.agi` (rc 0) | `None` |
| nested root | `/tmp/.../outer/.agi` (rc 0) | `None` |

FALSIFIER hit — the two halves DISAGREED on an unrelated nested git repo.

**Fix applied** in `extensions/agi/lib/find-root.sh`: inside the upward `while` loop, after probing `agi_graph_dir_in "$d"` (`.agi` holding config) and `agi_tree_config_path "$d"`, break when `[[ -e "$d/.git" ]]` exists (file OR dir), before `d="$(dirname "$d")"`. Order mirrors python: probe the level first (a main checkout or linked worktree keeping its `.agi` beside its `.git` still resolves to itself), then honour the `.git` boundary — nothing above an enclosing repository is ever climbed into.

**Test** added in `extensions/agi/tests/test_locations.py`: `nested_git` shape added to `test_bash_and_python_agree` — outer project with `.agi`, nested `git init` without `.agi`, deep child; asserts `bash == python == None` (empty). Build node `build:lib-find-root.sh` owes a `THOUGHT` recording this version's delta.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_locations.py -q` → **83 passed in 2.35s** (includes the new `nested_git` shape).
- `python3 -m pytest extensions/agi/tests/test_locations.py -k nested_git -q` → 1 passed, 82 deselected.
- Post-fix real-tree probe:
  - `bash find-root.sh <nest>/deep/child` → `ERR: no project found...`, rc=1 (== python `None`).
  - `bash find-root.sh <nest>` → rc=1.
  - CONTROL `bash find-root.sh <outer>` → `/tmp/.../outer/.agi`, rc=0 (outer project still resolves).
  - Worktree self-check: `bash find-root.sh extensions/agi/bin` from the round worktree → `/home/ubuntu/work/agi/.agi/worktrees/a00-46d77ded/.agi`, rc=0 (caller's own repo resolves; probe-before-break preserved).
- Temp fixtures built under `/tmp` and removed; nothing under `nodes/`.

## Agent Notes
find-root.sh now breaks its upward walk at the first .git after probing .agi/config, matching python; nested-git shape added to test_bash_and_python_agree, bash==python==None on an unrelated nested repo

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-46d77ded, L4.189) — accepted proved. WHAT THE BRIEF SAID: break the bash upward walk at $cur/.git AFTER probing that level for .agi/config, mirroring locations.py:217, and add a nested-git shape to test_bash_and_python_agree. WHAT THE ARTIFACT DOES: find-root.sh:178-187 inserts `if [[ -e "$d/.git" ]]; then break; fi` after both probes and before d="$(dirname "$d")"; the exit `/` probe and the descend fallback are untouched, so a project at the filesystem root and phase-2 `*-tree/` discovery keep working. Verified by running, not by reading: pre-fix I built /tmp/nrt/outer (with .agi) + /tmp/nrt/outer/sub (git init, no .agi) + deep child and got bash=/tmp/nrt/outer/.agi rc=0 vs python=None — the falsifier, confirmed. Post-fix on a fresh /tmp/v2 tree: bash deep=ERR rc=1, python rc=1, control bash on the outer root still /tmp/v2/outer/.agi rc=0. test_locations.py 83 passed. NEAR MISS: a `[[ -e "$d/.git" ]]` placed BEFORE the config probes would satisfy the words and lose the mechanism — a main checkout or linked worktree keeping its .agi beside its .git would break before ever finding its own graph; the kid probed first, which is the load-bearing order. Second near miss: `-d` instead of `-e` would miss a linked worktree, where .git is a FILE. DEVIATION: none. CAVEAT ACCEPTED: title is still the scaffold placeholder, cosmetic only, body heading duplicated; no behaviour attached.
<!-- THOUGHT:END -->
