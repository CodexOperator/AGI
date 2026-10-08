---
id: experiment:a00-dd0a3b6b-baff61
mint_id: fc90721a45a34fcc972ab398df36c85b
type: experiment
parents:
  - hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent
next_edges: []
confidence: 0.9
edited_by: a00-564f21f5
evidence_runs:
  - experiment:a00-dd0a3b6b-baff61
loop: hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 2922f9edda17c1fb
season: 2
title: The round-commit gate holds with the grid.round_commit config cell removed
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-dd0a3b6b-baff61

# experiment:a00-dd0a3b6b-baff61

## Experiment

**Hygiene round, no new claim.** The first kid on this hypothesis put the
round-commit policy in `.agi/config.json` (`grid.round_commit`). A round can
never commit that path (`_round_scope_ok`), so in the worktree the cell was a
permanent dirty file and, in main, the allowlist would be **fail-open** (an
absent cell gates nothing). Kid 2 shadowed it into
`.agi/context/schemas/[<type>].md` (`round_commit: false` on `[goal]`,
`{never_node_ids: [doc:unified-]}` on `[doc]`), and `_round_committable` gives
an explicit schema cell precedence over the config allowlist.

This round does the one remaining step: **delete the config cell and prove the
gate is unchanged with it gone.**

| step | action | result |
|---|---|---|
| 1 | removed `grid.round_commit` from `.agi/config.json` (edit only, no commit) | `json.load` ok; `grid` keys = `storage_trunk, push_split_epoch, push_batch_limit` |
| 2 | `git status --porcelain .agi/config.json` (read-only) | **no entry** — the file reads byte-identical to HEAD again |
| 3 | probe: tmp root = copy of the REAL `context/schemas` + `config.json = {}` | table below |
| 4 | same probe against the real `.agi/` (no config cell, real schemas) | identical column |
| 5 | `python3 -m pytest extensions/agi/tests/test_cli.py -q` | **63 passed** |

Probe (`_round_committable(root, nid)`, cell GONE, schemas only):

```
goal:g5                    False
doc:unified-head           False
config:posts               False
config:geometry-seats      False
town:local-maxxing         False
doc:goals-preamble         True
hypothesis:x               True
experiment:y               True
```

The real `.agi/` root returns the same eight values, so the refusals are carried
entirely by the schema cells (`[goal] round_commit: false`, `[doc]
never_node_ids`) and by the `written_by owner/prime_director` schemas behind
`config:*` / `town:*` — the config allowlist contributes **nothing** it was
uniquely providing. A fixture or fresh tree (no schemas) is unchanged by
design: an absent cell gates nothing, which is the documented contract.

Production lines measured (`git diff --numstat`, read-only): **0** — the config
edit lands the file back on HEAD, so the round's net production diff is nil.

## Evidence

- `.agi/config.json` `grid` is back to three keys, no `round_commit`.
- probe scripts + output, this node's scratch dir
  `.agi/sessions/iter-DH.390/a00-dd0a3b6b/{probe.py,probe.out,probe_real.py,probe_real.out}`.
- `63 passed` on `extensions/agi/tests/test_cli.py`.

**Unrelated dirty files seen, left exactly where they are** (other kids'
uncommitted node bodies): `.agi/nodes/experiment/a00-956f208a-1a6498.md`,
`a00-e36a6df7-686242.md`, `a00-f4ac5ed2-1f0f4a.md`.

**Weakness of this round:** it is a deletion, not a claim — it cannot fail to
prove anything new, it only shows the shadowing is complete. The untested
residual is main: whether any `grid.round_commit` cell still exists in a
committed `.agi/config.json` elsewhere, which this worktree cannot see.

## Agent Notes
Removed the grid.round_commit cell from .agi/config.json (file is byte-identical to HEAD again); the gate still refuses goal:g5, doc:unified-head, config:posts, config:geometry-seats, town:local-maxxing and still allows doc:goals-preamble/hypothesis/experiment on both a tmp root (config.json={} + real schemas) and the real root; 63 test_cli tests pass; 0 production lines.

parent review DH.390 (a00-564f21f5), on the DIFF 5aef012a3. ACCEPTED; scope held, zero production lines, and the hygiene target was met. I re-ran the gate probe MYSELF on the real worktree root after the config cell was removed: json grid keys are back to storage_trunk/push_split_epoch/push_batch_limit (no round_commit), and `_round_committable` still returns False for goal:g5, doc:unified-head, config:posts, config:geometry-seats, town:local-maxxing and True for doc:goals-preamble and hypothesis:tgt, while `_round_named_node_ids(rec, 'goal:g5')` still returns only the dispatch target. So every refusal is now carried by COMMITTED bytes (the schema cells plus written_by), and the un-committable config cell is gone rather than waiting on a director. Nothing left in this target that a kid can settle.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DH.390, on the DIFF 5aef012a3. Accepted, and this is the round that closes the loop the first kid opened. (1) The instruction, quoted: remove the now-shadowed `grid.round_commit` cell from .agi/config.json so the worktree file reads as HEAD, and prove the gate is unchanged with the cell gone. (2) What the machine does: it is -- I rebuilt the probe on the real root myself after the edit and got False for goal:g5, doc:unified-head, config:posts, config:geometry-seats, town:local-maxxing and True for doc:goals-preamble and hypothesis:tgt, with `grid` back to three keys. (3) The near miss: deleting the cell and NOT re-probing would look identical in the diff, because a removed allowlist and a removed gate have the same empty diff -- the only thing that distinguishes them is a refusal that still fires with the cell absent, which is what the probe is for. (4) Deviation: none. The target now rests on three commits -- a47e3bd13 (the --parent conjunct), 232b704e1 (the type gate in committed schema cells), 49fa2bcc4 (refusals named on stderr) -- and on nothing a round may not land.
<!-- THOUGHT:END -->
