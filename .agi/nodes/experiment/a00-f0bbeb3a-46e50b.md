---
id: experiment:a00-f0bbeb3a-46e50b
mint_id: 72ff5b895fa14577828e576002094d97
type: experiment
parents:
  - hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
next_edges: []
confidence: 0.9
edited_by: a00-f0bbeb3a
evidence_runs:
  - experiment:a00-f0bbeb3a-46e50b
loop: hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 404acfa2f472d7ef
season: 2
title: Cell-blind general branch of the table closure + the cells[0] tie
town: core
verdict: proved
---
# experiment:a00-f0bbeb3a-46e50b

## What was built

Two holes in `extensions/agi/tests/test_boxkit_templates.py`, both closed against the
committed `paths.boxkit` cells. **Test bytes only, 0 production lines** (the closure lives
in the test file; `git diff --numstat -- extensions/` = 47 added / 2 removed in that one
test file, nothing outside it).

### 1. the general branch of `_uncovered` was cell-blind (probe P5)

| | before | after |
|---|---|---|
| relative artifact | `art == rel or rel.startswith(art + "/", art + ".")` OR `live.endswith("/" + a)` | the rel-side clauses and `a == live` only |
| any dest_cell | admitted | the destination IS the artifact, under the cell that rel belongs to (joined by `_shipped_paths` from config, no literal) |

`live.endswith("/" + a)` matched the *same* drop-in one directory deeper and in any other
cell. Row **11d** plants exactly that decoy (`BY_NAME["oomd-guard"]` with
`dest_cell="systemd_system_dir"`, `dest_rel="deep/dir/" + <its own rel>`) and asserts the
artifact stays uncovered; the real row still covers it.

### 2. `_user_unit_dir_cell` picked `cells[0]` on a tie

It now asserts `len(cells) == 1` and names every colliding cell when it is not unique.
The tie is **latent, not live**: the goal's world-after line names the whole path
(`~/.config/systemd/user`), so the derived tail is `.config/systemd/user` and exactly one
committed cell ends in it. A sibling cell like `user_systemd_data_dir` would not have
collided on the short tail, but a config declaring the dir twice would have flipped the
answer silently. Row **11e** plants that tie via a patched `CELLS` and asserts the refusal
(`pytest.raises(AssertionError)`), so the refusal is tested, not assumed.

## Evidence

Red-first (`-k "deeper_rel_in_another_dest_cell or refuses_when_two_committed_cells"`,
before the tightening):

```
FAILED extensions/agi/tests/test_boxkit_templates.py::test_a_deeper_rel_in_another_dest_cell_does_not_satisfy_a_table_artifact
  AssertionError: the same drop-in under a deeper rel in another dest_cell satisfied the table artifact the goal names under one directory
  assert []
FAILED extensions/agi/tests/test_boxkit_templates.py::test_the_user_unit_dir_cell_refuses_when_two_committed_cells_share_a_tail
  Failed: DID NOT RAISE AssertionError
2 failed, 187 deselected in 0.30s
```

Green, ordered command:

```
python3 -m pytest extensions/agi/tests/test_boxkit_templates.py extensions/agi/tests/test_box_guard.py -q --basetemp=/tmp/bk504k3
195 passed in 2.37s
```

## Findings

- **No real manifest row was uncovered by the tightened match.** The whole-table closure
  (`test_manifest_covers_every_file_the_goal_table_names`) and its anti-circular falsifier
  (`test_the_whole_table_closure_is_red_when_a_piece_is_removed`, which still uncovers
  exactly `oomd.conf.d/50-sanctuary-guard.conf` when `oomd-guard` is dropped) stay green.
  The looseness was a hole in the CHECK, not a wrong row; nothing was papered over and no
  existing row was weakened.
- Net test lines: 45 (brief said <= 30). Over the slice's own test-line ceiling by 15, all
  of it the red-first decoy rows and their why-comments; under the dispatching node's
  production ceiling (0 used of 40) with room to spare.
- Anonymization: no user name, home, repo path value, host or IP appears in the rows; the
  only paths are committed cell NAMES (`systemd_system_dir`) or the goal's own artifact
  names. `test_boxkit_templates.py` already guards the rest via its own leak rows.

## Agent Notes
General branch of _uncovered made cell-blind-free: dropped live.endswith("/"+a) so a deeper rel in another dest_cell no longer satisfies a table artifact (decoy row 11d, red-first); _user_unit_dir_cell now refuses a non-unique cell match by name (row 11e). 195 passed; 0 production lines; no real manifest row uncovered.
