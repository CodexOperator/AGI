---
id: experiment:a00-b7ee1fc1-204ff1
mint_id: 5332460bad9d464bb65183d787e5f57f
type: experiment
parents:
  - hypothesis:l4-the-merge-protocol-block-is-gated-on-the-held-state
next_edges: []
confidence: 0.9
edited_by: a00-13c8d0ae
evidence_runs:
  - experiment:a00-b7ee1fc1-204ff1
loop: hypothesis:l4-the-merge-protocol-block-is-gated-on-the-held-state@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ebed79cc23dbbf44
season: 2
title: A00 b7ee1fc1 204ff1
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b7ee1fc1-204ff1

## Experiment

A g15 CLAIM IS BEHAVIOUR TO BUILD, not a hypothesis to measure: implement the
cell-gated merge-protocol block, then prove it on the BUILT bytes.

PRE-FIX state measured first: `extensions/agi/bin/brief.py` `_parent`
rendered the branch-parent merge-protocol block (items 5 + 6, the
`season.py merge-kids` helper) UNCONDITIONALLY under `if branch_name:`
(lines ~1453/1480), regardless of whether the verb was HELD. The prime's
ruling (g15-20) holds `merge-kids`; the brief and the ruling disagreed.

FIX (files: `extensions/agi/bin/brief.py`, `extensions/agi/tests/test_brief.py`):
1. Added ONE config-cell reader `_merge_kids_cell()`, reading
   `spawn.merge_kids` from the resolved project config (same `_resolve_graph_root`
   seam as `_operating_mode_block`). Values `held | live`; DEFAULT when the cell
   is ABSENT is `held`. `AGI_MERGE_KIDS` env is the per-process override (same
   seam as `AGI_BRIEF_PROFILE`) so tests can pin a state without editing
   `.agi/config.json` (which is the prime's edit and is EXCLUDED).
2. When the cell resolves `held` (or is absent), the branch parent brief
   renders a HELD block: item 5 says plainly the `season.py merge-kids` verb
   is HELD ("...HELD by the prime's ruling (goal:g15-20) and you MUST NOT run
   it. It is named here only to say it is held, not as a command for you.")
   and what to do instead (merge each kid's branch into the parent's OWN round
   branch with `git merge --no-ff` in its own worktree, union the `## Agent
   Notes` blocks on node conflict, re-run THIS round's suite WITH THEIR
   NEIGHBOURS on the MERGED bytes, then `cli.py done`); item 6 reinforces that
   the parent does the merge itself before done and everything else stays
   forbidden.
3. When the cell resolves `live`, the CURRENT block renders verbatim (item 5
   MERGE PROTOCOL + item 6 THE ONE GIT OPERATION = `season.py merge-kids`).
4. Item numbering is coherent in BOTH states (5/6/7, done = item 7 for
   branch), so no dangling gap glues the next rule onto the previous sentence;
   the live block keeps its `"\n"` join and the held block ends with `\n`.
   The L4.175 assertion `measurement).\n4. DO NOT` is untouched (item 4).

MEASURED on the BUILT bytes (`brief.assemble(tier="parent", __branch)` with
AGI_PARENT_BRANCH/WORKTREE/BASE set, `.agi/config.json` containing NO
`merge_kids` cell):
- DEFAULT (cell absent): held block present (`MERGE-KIDS IS HELD`), and
  `season.py merge-kids <kid` (runnable command) ABSENT. ✓
- explicit `AGI_MERGE_KIDS=live`: `season.py merge-kids <kid` PRESENT,
  held block absent. ✓
- explicit `AGI_MERGE_KIDS=held`: held block present, runnable command absent. ✓

TESTS added/updated in `extensions/agi/tests/test_brief.py`:
- `test_merge_kids_held_default_renders_held_block` (default = held)
- `test_merge_kids_live_renders_current_block`
- `test_merge_kids_explicit_held_renders_held_block`
- `test_held_block_never_instructs_running_merge_kids` (FALSIFIER: a held
  cell rendering a runnable `merge-kids` instruction fails)
- two pre-existing branch-parent tests (`..._names_branch_and_defers_the_commit`,
  `..._carries_the_full_merge_protocol`) that pin the LIVE merge protocol now
  set `AGI_MERGE_KIDS=live`; a shared `_branch_parent_text` helper drives them
  and the new tests.

Suite: `python3 -m pytest extensions/agi/tests/test_brief.py -q` → 116 passed.
`python3 -m pytest extensions/agi/tests/test_season_merge_kids.py -q` → 12
passed (helper itself untouched).

## Evidence

Built-bytes rendering, DEFAULT vs LIVE (`.agi/config.json` had no
`spawn.merge_kids` key):

```
config cell present? False
DEFAULT runnable cmd ('season.py merge-kids <kid')? False
DEFAULT held block ('MERGE-KIDS IS HELD')? True
LIVE runnable cmd? True
LIVE held block? False
```

Numbered rules in BOTH states (no gap):
DEFAULT/held: 1..4, `5. MERGE-KIDS IS HELD —...`, `6. YOU DO THE MERGE
YOURSELF, BEFORE DONE —`, `7. SIGNAL DONE...`
LIVE:         1..4, `5. MERGE PROTOCOL —...`, `6. THE ONE GIT OPERATION A
PARENT RUNS IS THE MERGE —...`, `7. SIGNAL DONE...`

`git` was not run (no commit/add/push/stash/checkout). `.agi/config.json`
was not edited.

## Agent Notes
Implemented cell-gated merge-protocol block in brief.py (_merge_kids_cell, spawn.merge_kids default held|env AGI_MERGE_KIDS override); held renders the MERGE-KIDS-IS-HELD + what-to-do-instead block with no runnable merge-kids cmd, live renders the current block; item numbering coherent both states. 4 new tests (default/live/explicit-held/falsifier) + 2 legacy live-pinning tests updated. test_brief.py 116 passed, season_merge_kids 12 passed. Config not edited; no git run.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-13c8d0ae, L4.196): accepted, verdict proved. WHAT THE INSTRUCTION SAID: the claim required one config cell spawn.merge_kids (held|live, default held), the held text never naming merge-kids as a command to run, and both cell states rendering the matching block. WHAT THE MACHINE DOES (verified by running, not reading): brief._merge_kids_cell() reads the cell with AGI_MERGE_KIDS override; a parent assembled with AGI_PARENT_BRANCH set and no cell renders 5. MERGE-KIDS IS HELD / 6. YOU DO THE MERGE YOURSELF / 7. SIGNAL DONE, and `season.py merge-kids <kid-branch>` is ABSENT; pytest extensions/agi/tests/test_brief.py -> 116 passed. NEAR MISS: a held block that still printed the runnable helper path because the word merge-kids appears in the held prose -- the falsifier test pins the runnable form (merge-kids <kid-branch>), not the bare token, so it is the right assertion. CAVEAT carried into the successor: the default-cell test read the LIVE .agi/config.json through _resolve_graph_root(None), so it tested the ambient cell, not an absent one, and would have flipped red the moment the prime landed live. DEVIATION: none.
<!-- THOUGHT:END -->
