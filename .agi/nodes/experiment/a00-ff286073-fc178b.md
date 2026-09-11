---
id: experiment:a00-ff286073-fc178b
mint_id: d82436a066ae4af792e135be1920e434
type: experiment
parents:
  - hypothesis:l4-the-merge-protocol-block-is-gated-on-the-held-state
next_edges: []
confidence: 0.9
edited_by: a00-13c8d0ae
evidence_runs:
  - experiment:a00-ff286073-fc178b
loop: hypothesis:l4-the-merge-protocol-block-is-gated-on-the-held-state@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 17dc8b32701bdada
season: 2
title: A00 ff286073 fc178b
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ff286073-fc178b

## Experiment

Target: `hypothesis:l4-the-merge-protocol-block-is-gated-on-the-held-state` —
the DEFAULT cell test was NOT hermetic. `_branch_parent_text(monkeypatch)`
with `merge_kids=None` deleted `AGI_MERGE_KIDS` and let `_merge_kids_cell()`
fall through to `_resolve_graph_root(None)`, which resolves the LIVE
checkout's `.agi/config.json`. So `test_merge_kids_held_default_...` and
`test_held_block_never_instructs_running_merge_kids` did NOT test "cell
absent → held"; they tested "whatever the ambient config currently says".
Measured: ambient `spawn.merge_kids` is currently ABSENT (held), so the two
tests passed — but the moment the prime set `spawn.merge_kids: live` they
would flip red for a reason unrelated to behaviour.

Fix (test-only; no `brief.py` behaviour change, no `.agi/config.json` touch):

- `_branch_parent_text(monkeypatch, merge_kids=None, config_cell=_ABSENT_CELL)`
  now writes a temp `.agi` dir whose `config.json` carries
  `{"spawn": {"merge_kids": <config_cell>}}` — or carries NO `spawn` key when
  `config_cell` is the `_ABSENT_CELL` sentinel — and monkeypatches
  `brief._resolve_graph_root` to return that dir. `AGI_MERGE_KIDS` still
  overrides, as in production.
- `test_merge_kids_held_default_renders_held_block` and
  `test_held_block_never_instructs_running_merge_kids` now pass
  `config_cell=_ABSENT_CELL`: the cell-ABSENT config renders HELD — pinned,
  not ambient.
- The explicit-env cases (`live`/`held`) pin `config_cell=_ABSENT_CELL` too,
  proving the env override wins over an absent cell.
- NEW `test_merge_kids_live_config_cell_no_env_renders_runnable`: config cell
  = `live` with env UNSET renders the runnable
  `season.py merge-kids <kid-branch>` instruction at DEFAULT.
- Falsifier kept: the held block never renders a runnable
  `season.py merge-kids <kid-branch>` command.

## Evidence

Hermetic independence from the ambient config is by construction: each call
confines `brief._resolve_graph_root` to a private temp root, so the ambient
`.agi/config.json` is unreachable by the reader. The cell-ABSENT default test
renders HELD and the cell-`live` config test renders RUNNABLE while sharing
no state — if either leaked to the ambient they'd both depend on the one
value and could not both hold.

Full file run:

```
$ python3 -m pytest extensions/agi/tests/test_brief.py -q
........................................................................ [ 61%]
.............................................                            [100%]
117 passed in 4.00s
```

No source code changed — only `extensions/agi/tests/test_brief.py`.
<!-- BODY:END -->

## Agent Notes
Made the merge-kids DEFAULT-cell test hermetic: _branch_parent_text now pins brief._resolve_graph_root to a temp config dir (cell value or ABSENT sentinel) instead of leaking to the live checkout's .agi/config.json; added config-driven live test; falsifier kept. 117 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-13c8d0ae, L4.196): accepted, verdict proved. WHAT THE INSTRUCTION SAID: make the default-cell test hermetic so it tests an ABSENT cell rather than the live checkout config, with the held falsifier kept and no brief.py behaviour change. WHAT THE MACHINE DOES (verified by running): _branch_parent_text monkeypatches brief._resolve_graph_root to a temp dir whose config.json carries the cell or no spawn key; a config with no cell renders MERGE-KIDS IS HELD with no runnable command, a config with live renders the runnable season.py merge-kids <kid-branch> instruction at DEFAULT with no env, in the SAME test run; pytest test_brief.py + test_season_merge_kids.py -> 129 passed. NEAR MISS: a test that monkeypatches the cell reader itself would pass while proving nothing -- pinning the config the reader READS is the mechanism, and the two directions passing together is what makes the ambient config unable to be the source of both. DEVIATION: test-only change, brief.py untouched, .agi/config.json untouched as the claim excluded it.
<!-- THOUGHT:END -->
