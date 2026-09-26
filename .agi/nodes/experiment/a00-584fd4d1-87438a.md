---
id: experiment:a00-584fd4d1-87438a
mint_id: 680317d00e8b48d399e6b43177216449
type: experiment
parents:
  - hypothesis:the-captive-capture-never-writes-into-the-live-card-and-a-failed-forced-rotation-is-logged-and-latched
next_edges: []
edited_by: a00-a2524533
loop: hypothesis:the-captive-capture-never-writes-into-the-live-card-and-a-failed-forced-rotation-is-logged-and-latched@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 18f5fcd2f08e3fc3
season: 2
title: A00 584fd4d1 87438a
town: core
---
## Experiment

The bytes this node names were produced by DH.371 kid a00-584fd4d1 and salvaged
uncommitted (commit 20d41f3f4) when the box reboot killed parent a00-3a39d410.
The node body was left as the empty scaffold. It is filled here from the
MEASURED bytes, by parent a00-a2524533, not from the kid's summary.

### The diff (read, not described)
- `extensions/agi/hooks/rotation_alert.py` `_force_capture`:
  - the `card.write_text(AUTO_CAPTURED + card.read_text())` prepend is REMOVED;
    the marker becomes a SIBLING state file `state_dir/capture-<seat>.captured`.
  - a latch: `if json.loads(stamp).get("captured"): return "capture-latched"`,
    and after the spawn `blob["captured"] = int(time.time())` is written back.
  - the chain's stdout+stderr move off `subprocess.DEVNULL` onto an opened
    `(state_dir / "capture-chain.log").open("ab")`.
- `extensions/agi/bin/rotate.py` `cmd_handoff`: one added line
  `_flatten_card_symlink(card_path)` before `card_path.write_text(full)`
  (rotate.py:8287).
- 3 test edits + NEW `extensions/agi/tests/test_rotation_alert_capture_safety.py`.

### Measured, by the parent
- `pytest` on the safety + capture files: 14 passed (kid's own run).
- P1 gate: card a SYMLINK into `nodes/doc/`; after `_force_capture` the target
  bytes are byte-identical, first line `---`, the card is still a symlink.
- P2 auth: 2nd call same seating -> `capture-latched`; a NEW seating's stamp
  (`{first, session}`, written by the over-line stamper at rotation_alert.py:1452)
  drops the `captured` key and the 3rd call captures again. Once per SEATING.
- P3 wire: the argv split is positional and exact; `stdout`/`stderr` are the
  opened log object, never DEVNULL; the chain uses `&&`.
- P4 COUNTERFACTUAL: with `rotate._flatten_card_symlink` neutered, `cmd_handoff`
  still returns rc=0 on the symlinked fixture but `still_symlink=True` and the
  graph node is rewritten IN PLACE. The flatten is load-bearing; the "symlink
  broke the chain" lead is neither proved nor disproved by a fixture that
  returns 0.

## Evidence
- commit 20d41f3f4 (`git show`), cherry-picked `-n` into the DH.374 parent
  worktree; no commit made by the parent (the loop owns commits).
- parent probes under
  `.agi/sessions/iter-DH.374/a00-a2524533/probe_parent_*.py`.
- CONTINUED IN: experiment:a00-24940137-d483fe, verdict:a00-606bcf68-e43240,
  mvp:a00-fb94d444-a0ccc8 (the last of which closes the config-cell gap this
  diff left open).

## Status
NOT a verdict and NOT a claim of its own: the WIP that was salvaged here is
carried forward by the three DH.374 nodes named above. Conjunct 3 (why the forced
chain failed) remains UNMEASURED.
