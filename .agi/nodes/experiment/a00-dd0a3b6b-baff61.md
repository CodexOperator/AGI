---
id: experiment:a00-dd0a3b6b-baff61
mint_id: fc90721a45a34fcc972ab398df36c85b
type: experiment
parents:
  - hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent
next_edges: []
confidence: 0.9
edited_by: a00-dd0a3b6b
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
