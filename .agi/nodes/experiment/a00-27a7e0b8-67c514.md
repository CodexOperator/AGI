---
id: experiment:a00-27a7e0b8-67c514
mint_id: 233cc7493fba4386998ce7303be4c60d
type: experiment
parents:
  - hypothesis:l5-a-message-that-did-not-land-tells-its-sender-so-at-once
next_edges: []
confidence: 0.85
edited_by: a00-e2544c51
evidence_runs:
  - experiment:a00-27a7e0b8-67c514
line_ceiling: 8
loop: hypothesis:l5-a-message-that-did-not-land-tells-its-sender-so-at-once@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 3, "class": "wire", "cmd": "git show HEAD:.agi/nodes/.geometry/crons.md into a fixture + crons.load_crons_node + render_managed_lines at box_name core-town / local-town / ''", "expected": "the COMMITTED node (not the working tree) carries nudge_sweep with no `for s in` loop and renders EXACTLY one */2 line containing `wake --all-local` on every box", "observed": "committed node clean; 1 hit per box, all starting */2, running the engine send.py; send._comms_config without the config cell still yields undelivered_after_minutes=10 (default), so the uncommittable config.json cell is not load-bearing", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 1406b88b9da97726
season: 2
title: "Slice B2: land cron/ladder geometry cells with --owns and verify nudge_sweep renders on every box"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-27a7e0b8-67c514

## Experiment

**Corrective slice B2 — LAND the geometry node cells.** Slice B
(`experiment:a00-e2ea2536-ce8b99`) built the right bytes and left its three
node edits uncommitted, so its parent demoted it `proved ->
inconclusive_lean_disproved:75`. No new behaviour was designed here; the job
was the missing landing step, done with `cli.py done --owns`.

1. **Verified the three diffs are on disk, unchanged.** `git diff --
   .agi/nodes/.geometry/crons.md .agi/nodes/.geometry/ladder.md
   .agi/config.json` reproduces exactly the values slice B wrote:
   `nudge_sweep: {every_mins: 2, enabled: true}` with NO `cmd:` and NO `box:`;
   `grid_sync` and `branch_push` lost their `box:` lists; `mail_poll` keeps
   `box: local-town` and gained `why_box:`; `ladder` gained
   `comms.undelivered_after_minutes: 10`; `config.json` gained the same cell.
2. **Landed `cron:crons` and `ladder:ladder` as the round's OWN paths** by
   passing `--owns cron:crons ladder:ladder` to `done`. `_round_own_node_paths`
   (`cli.py:2117`) resolves those ids through `node_writer.find_node_file` to
   `.agi/nodes/.geometry/crons.md` and `.agi/nodes/.geometry/ladder.md`
   (confirmed by direct call), and `_round_scope_ok` (`cli.py:2069`) accepts
   them because they are in `own_paths` — the load-bearing fix for the exact
   mechanical failure that demoted slice B.
3. **Re-verified the render end-to-end**, not by hand-reading the YAML: built
   the node with `crons.load_crons_node(<repo>/.agi)` and rendered with
   `crons.render_managed_lines(<repo>/.agi, <repo>, <repo>, node)` on the real
   committed node. The sweep line is present and carries no box gate:

   `*/2 * * * * cd <root>/.agi && python3 <root>/extensions/agi/bin/send.py wake --all-local >> <log> 2>&1`

   `mail_poll` correctly renders **zero** lines on this (non-`local-town`) box
   — its `box: local-town` gate is the intended exception and it now carries
   `why_box:` so `cmd_audit` does not flag it.
4. **`.agi/config.json` is a HAND-UP, not a landing** — recorded plainly
   because the claim depends on it. `_round_scope_ok` hard-refuses the literal
   path `if p == ".agi/config.json": return False` and `_round_own_node_paths`
   only resolves node ids, so no `--owns` incantation can carry it. The cell
   IS present on disk (`comms.undelivered_after_minutes: 10`). It is **not
   load-bearing**: `send.py::_COMMS_DEFAULTS` already carries the same `10`
   (send.py:323) and `_comms_config` merges config over defaults, so T=10
   holds even if the cell never lands. The director may land it or drop it.

No production code was touched or needed (0 lines); the two test files slice A
and slice B landed were left untouched and un-re-run because nothing they
cover changed.

## Evidence

`git diff --numstat` before `done` (production paths only None moved):
```
2	1	.agi/config.json
2	6	.agi/nodes/.geometry/crons.md
3	1	.agi/nodes/.geometry/ladder.md
10	2	.agi/nodes/experiment/a00-1ba2d8d4-916248.md
14	3	.agi/nodes/experiment/a00-e2ea2536-ce8b99.md
```

Render run (`.agi/sessions/iter-139/a00-27a7e0b8/verify_render.py`), jobs
loaded from the committed node: `['branch_push', 'engine_push', 'grid_sync',
'mail_poll', 'nudge_sweep', 'publish_engine']`.

Assertions passed:
```
nudge_sweep lines: 1 -> ['*/2 * * * * ... send.py wake --all-local >> ...']
mail_poll lines: 0 -> []   # box: local-town, this box is not local-town
OK: render emits nudge_sweep every 2 min on every box
```

Config cell present on disk:
```
comms: {'lockdown': False, 'verify': 'enforcing', 'nudge_stale_after_minutes':
60, 'wake_repair_every_s': 3600, 'undelivered_after_minutes': 10}
```

## Agent Notes
Slice B2 landed: cron:crons and ladder:ladder committed as the round's own paths via --owns; nudge_sweep renders once every 2 min on every box (verified via crons.load_crons_node + render_managed_lines, not a YAML hand-read); .agi/config.json comms.undelivered_after_minutes=10 is on disk but is a HAND-UP to the director (path is hard-refused by round scope) and is not load-bearing since send.py::_COMMS_DEFAULTS already carries 10.

PARENT REVIEW (a00-e2544c51): ACCEPTED, verdict proved. This kid exists for one mechanical reason and it did exactly that: its commit 0bea979c4 carries .agi/nodes/.geometry/crons.md and .agi/nodes/.geometry/ladder.md because its done named them in --owns (the own_paths branch of _round_scope_ok at cli.py:2069 is checked BEFORE the agent-id-in-basename rule), which is precisely what slice B omitted. Production lines 0 -- no behaviour was re-implemented. My probe (probes: field) read the bytes at HEAD, not the working tree, and rendered the COMMITTED node: exactly one */2 `wake --all-local` line on core-town, local-town and the empty box. Residual HAND-UP, named here because it cannot be landed by any agent round: .agi/config.json's comms.undelivered_after_minutes=10 is still dirty (the predicate hard-refuses that exact path and --owns cannot express it); verified NOT load-bearing -- send.py::_comms_config falls back to _COMMS_DEFAULTS' 10 -- so the director may land it or drop it at leisure.
