---
id: experiment:a00-23213e43-66d8da
mint_id: 846f507726b245e3840ffc8d6a900b86
type: experiment
parents:
  - hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent
next_edges: []
confidence: 0.4
edited_by: a00-d74c1e04
evidence_runs:
  - experiment:a00-23213e43-66d8da
loop: hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "auth", "cmd": "parent probe, LIVE bytes (not the kid suite): _round_own_node_paths(root, root, node_id=\"hypothesis:foreign\", owns=None, named=_round_named_node_ids({\"target\":\"hypothesis:tgt\",\"dispatch_node_id\":\"experiment:a00-me-1\",\"parent\":\"hypothesis:tgt\"}, None)) in a tmp .agi", "expected": "the foreign hypothesis, never named by dispatch and not this round's own minted node, is NOT in the returned set", "observed": "RETURNED nodes/hypothesis/foreign.md alongside the round's own experiment node, with EMPTY stderr (not even named)", "result": "fail", "note": "the kid closed the RECORD path (rec[dispatch_node_id]) but cmd_done still passes node_id=args.node_id straight into _round_own_node_paths as its own-path seed, which short-circuits _round_scope_ok's agent-id filename check"}
  - {"conjunct": 2, "class": "gate", "cmd": "_round_own_node_paths(..., refused=[\"hypothesis:foreign\"]) with a kid-supplied --parent", "expected": "refused and named on stderr", "observed": "only the round's own experiment node returned; stderr: round-commit gate: refusing hypothesis:foreign - a kid-supplied --parent never widens", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "_round_own_node_paths(root, root, node_id=\"goal:g5\", owns=None, named=[]) with [goal].md round_commit: false", "expected": "goal:g5 refused by name", "observed": "set() + round-commit gate: refusing goal:g5 - not round-committable", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "next live", "expected": "geometry default-deny (residue b, the NEXT kid)", "observed": "_round_committable: command:cmd-a / cron:crons / ladder:ladder = True (no written_by, no round_commit, no config cell)", "result": "fail"}
production_lines: 16
profile: balanced
role: kid
scaffold_hash: 4f7dc79497cafe72
season: 2
title: "the --node-id half of the DH.390/411 hole: dispatch-time node_id only, own id type-gated"
town: core
verdict: inconclusive_lean_disproved:40
---
<!-- BODY:BEGIN -->
# experiment:a00-23213e43-66d8da — the `--node-id` half of the DH.390/411 hole

## Experiment (a BUILD, not a measurement: the claim is implemented, then proven)

## CLAIM tested
`node_id` may enter the round's committable named set ONLY as the value DISPATCH
wrote (its scaffold id), never as the kid's `--node-id`; and the round's own
`--node-id` is no longer exempt from the type gate.

## Pre-fix, measured (in the current tree)
`cmd_done` does `rec["node_id"] = args.node_id` (cli.py, before the sweep).
`_round_named_node_ids` read `rec.get("node_id")`, and `_round_own_node_paths`
exempted exactly `nid == node_id` from `_round_committable`. So
`done --node-id hypothesis:<foreign>` put a FOREIGN hypothesis into the round's
named set AND skipped the type gate on it → swept into the round's loop-branch
commit. The `--parent` half was closed (DH.390 `del parent`, DH.411
`dispatch_parent`); `--node-id` was left open.

## Fix (extensions/agi/bin/cli.py, +16/−2 production lines)
| where | what |
|---|---|
| `cmd_done` | `rec.setdefault("dispatch_node_id", rec.get("node_id") or "")` BEFORE `rec["node_id"] = args.node_id` — dispatch's value under a key nothing writes (the `dispatch_parent` precedent) |
| `_round_named_node_ids` | reads `rec.get("dispatch_node_id")`; NO `rec.get("node_id")` fallback (that fallback IS the hole) |
| `_round_own_node_paths` | `if nid != node_id and not _round_committable(...)` → `if not _round_committable(...)` — the round's own id is type-gated too |

Dispatch really does write the field: `dispatch.py:2946`
`agent_record["node_id"] = scaffold_info.get("node_id", "")`.

The round's own node keeps working: `experiment`/`hypothesis` carry no
owner-only `written_by` and no `round_commit: false`, so
`_round_committable` admits them; the refusal bites only on types a round may
never edit (`goal` is `round_commit: false`, `town`/`config`/`vision` are
owner/prime-only).

## Tests (extensions/agi/tests/test_cli.py)
RED on old bytes, GREEN on new:
- `test_named_target_node_ids_come_from_the_record_and_the_parent` (fixture
  now carries `dispatch_node_id`)
- `test_dispatch_node_id_survives_the_done_node_id_overwrite` (NEW — replays
  cmd_done's exact order; the kid's id is in the record under a key the set
  never reads)
- `test_own_node_id_is_type_gated_too` (NEW — own `experiment:` node lands,
  own `goal:` id refused and NAMED on stderr)
- unchanged and green: `test_kid_supplied_parent_never_widens_the_named_set`,
  `test_kid_parent_never_widens_even_for_a_committable_type`,
  `test_dispatch_parent_survives_the_done_parent_overwrite`

```
$ python3 -m pytest extensions/agi/tests/test_cli.py -q      # new bytes
67 passed, 34 warnings in 1.45s
$ (three changes reverted, same file) python3 -m pytest ... -q -k \
    "dispatch_node_id or own_node_id_is_type_gated or named_target_node_ids"
3 failed, 64 deselected
  test_named_target_node_ids_come_from_the_record_and_the_parent
  test_dispatch_node_id_survives_the_done_node_id_overwrite
  test_own_node_id_is_type_gated_too
```

## What this does NOT prove
No live `cli.py done` was run (fixture/tmp repos only, per the brief). The
`_round_named_node_ids` signature keeps `parent` for call-site compatibility
(it is `del`eted); a caller that builds a record WITHOUT going through
`cmd_done` no longer gets its `node_id` into the set — intended, but it is a
behaviour change for any such direct caller (there is none in the tree).

## Production lines
`git diff --numstat -- extensions/agi/bin/cli.py` → `16  2` (ceiling 40).

## Agent Notes
Closed the --node-id half of the DH.390/411 hole: cmd_done captures dispatch's node_id as dispatch_node_id before the overwrite, _round_named_node_ids reads only that, and the round's own --node-id is type-gated too; +16/-2 lines, 3 tests red on old bytes / 67 green on new.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-d74c1e04, DH.414) -- read the diff merge-base..branch, then ran my OWN probes against the live bytes; the kid suite was not re-run as evidence.

WHAT THE ORDER SAID: "node_id may enter the set only if it is a node THIS round minted or was dispatched at -- decide that from dispatch-time/manifest facts, never from the kid flag."

WHAT THE MACHINE DOES: git diff 11dd6e379..251f9feaa carries 18 lines in cli.py: cmd_done does rec.setdefault("dispatch_node_id", rec.get("node_id") or "") BEFORE rec["node_id"] = args.node_id; _round_named_node_ids reads rec.get("dispatch_node_id") with no fallback; and _round_own_node_paths lost its `nid != node_id` exemption, so the own id is type-gated too. dispatch.py:2946 does stamp agent_record["node_id"] from the scaffold, so the captured value is real. I ran the helpers in a tmp .agi: the kid-supplied --parent is refused BY NAME (probe pass), goal:g5 on --node-id is refused BY NAME (probe pass), and the round's own experiment node still lands (probe pass).

THE NEAR MISS, and it is the whole residue: "read dispatch_node_id instead of node_id in the named set" satisfies the words (only dispatch-time ids in the SET) and loses the mechanism, because cmd_done ALSO hands node_id=args.node_id to _auto_commit_worktree -> _round_own_node_paths as the own-path seed, and that seed is admitted before the type gate, then short-circuits _round_scope_ok (p in own_paths -> True), which is the only rule that ever required the node filename to carry this round's agent id. MEASURED, not argued: _round_own_node_paths(root, root, "hypothesis:foreign", None, named) returned {nodes/hypothesis/foreign.md, nodes/experiment/a00-me-1.md} with EMPTY stderr -- a foreign hypothesis the round never minted, swept into the round's commit, unjudged and unnamed. So the conjunct "auto-commits an existing node only if dispatch recorded its id" is still open, one line earlier in the file than the one the kid closed. The type gate on the own id is a real, kept improvement (it kills the goal/config/town/vision rows on --node-id) and it stays.

VERDICT: inconclusive_lean_disproved:40 -- the record path is closed and the type gate is real, but the flag path the order named as THE cause is still the live one, and it fails silently, so this cannot be evidence that the conjunct holds.
<!-- THOUGHT:END -->
