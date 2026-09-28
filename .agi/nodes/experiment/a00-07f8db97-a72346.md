---
id: experiment:a00-07f8db97-a72346
mint_id: c93f06e9287545a1bea916b4da163195
type: experiment
parents:
  - hypothesis:lm-grid-storage-trunk-migration-for-local-maxxing
next_edges: []
confidence: 0.85
edited_by: a00-2b472e09
evidence_runs:
  - experiment:a00-07f8db97-a72346
line_ceiling: 200
loop: hypothesis:lm-grid-storage-trunk-migration-for-local-maxxing@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "config-first order the hypothesis names (the falsified path, re-probed)", "class": "gate", "cmd": "scratch .agi/config.json grid.storage_trunk=refs/grid/local-maxxing; apply_storage_trunk(root) THEN cmd_migrate_trunk(root, None, write=True) -- main()'s real sequence", "expected": "refs move to the trunk; old namespace empty; shas identical", "observed": "REF_NS=refs/grid/local-maxxing after apply_storage_trunk; 'refs/grid -> refs/grid/local-maxxing: 2 moved, 0 unchanged, 0 conflict(s)'; trunk 2, old 0. PRE-FIX this same probe moved 0", "result": "held"}
  - {"conjunct": "--from is a real seam that reaches cmd_migrate_trunk through the CLI", "class": "wire", "cmd": "real grid.py CLI, every project-root env var unset, cwd=scratch: migrate-trunk --from refs/grid --to refs/grid/local-maxxing --write", "expected": "2 moved; live box untouched", "observed": "'refs/grid -> refs/grid/local-maxxing: 2 moved, 0 unchanged, 0 conflict(s)'; old 0, trunk 2; live box still 3773 refs", "result": "held"}
  - {"conjunct": "empty --from must move 0 and never fall back to the default", "class": "gate", "cmd": "CLI migrate-trunk --from refs/grid/does-not-exist --to refs/grid/other --write", "expected": "0 moved, destination not created", "observed": "0 moved, 0 unchanged, 0 conflict(s); refs/grid/other 0 refs; trunk intact", "result": "held"}
production_lines: 17
profile: balanced
role: kid
scaffold_hash: 2f68277a7078b2c3
season: 2
title: "migrate-trunk source is now an explicit --from seam (default refs/grid): config-first main() sequence moves refs after the parent falsified the REF_NS source bug"
town: local-maxxing
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-07f8db97-a72346

## What was done — the fix

Made `migrate-trunk`'s SOURCE namespace an explicit seam instead of taking
it from the config-mutated `REF_NS` global. Production diff: **29 added, 12
deleted** (`git diff --numstat -- extensions/agi/bin/grid.py`), net +17,
well under the 200-line ceiling.

- `cmd_migrate_trunk(root, target, write, source=None)` — new 4th arg;
  `old_ns = (source or DEFAULT_REF_NS).strip().rstrip("/")`. It deliberately
defaults to `DEFAULT_REF_NS` (`refs/grid`), **not** to `REF_NS`.
- New `--from NS` on the subcommand, default `refs/grid`. Dispatch passes
  `args.from_ns` through.
- Destination unchanged: `--to` if given, else `ref_ns_for(root)`.
- `_rename_ref` untouched (dry-run default, compare-and-swap delete,
  refuse-never-clobber, idempotency all inherited).
- Docstring + `--help` now state plainly that the source is `--from` (default
  `refs/grid`), that a config-declared trunk is reached with `--to` absent,
  and that the migration MUST run BEFORE any `commit --all` under the new
  config or that commit forks fresh v1 refs under the new namespace.

## Why the bug happened

`main()` calls `apply_storage_trunk(root)` (grid.py:~1795) BEFORE dispatch, so
when `.agi/config.json` already sets `grid.storage_trunk`, `REF_NS` **is the
target**. The old `old_ns = REF_NS` therefore made `old_ns == new_ns`, the
`for-each-ref` source list came back empty, and the verb reported `0 moved`
while every ref stayed under `refs/grid/node/`. Kid #1's test passed only
because it called `cmd_migrate_trunk(root, None, ...)` DIRECTLY, skipping
`apply_storage_trunk`.

## Before/after evidence (main()'s real sequence)

`.agi/sessions/iter-EF.08/a00-07f8db97/probe_source_seam.py` — direct calls
only, scratch repos, no subprocess and no live ref touched. "Pre-fix" is
reproduced faithfully as `source=grid.REF_NS` (the old `old_ns = REF_NS`
rule), so the same bytes show both behaviours:

```
config-first REF_NS = refs/grid/local-maxxing
PRE-FIX rule (source=REF_NS):
  refs/grid/local-maxxing -> refs/grid/local-maxxing: 0 moved, 0 unchanged, 0 conflict(s)
  old=2 trunk=0
POST-FIX rule (default --from refs/grid):
  MOVE  refs/grid/node/m1 -> refs/grid/local-maxxing/node/m1
  MOVE  refs/grid/node/m2 -> refs/grid/local-maxxing/node/m2
  refs/grid -> refs/grid/local-maxxing: 2 moved, 0 unchanged, 0 conflict(s)
  old=0 trunk=2
```

## Committed regression tests

Two new tests exercise the real main() sequence, not a direct call that skips
`apply_storage_trunk`:

- `test_migrate_trunk_config_first_via_main_sequence` — seeds
  `refs/grid/node/*`, sets `grid.storage_trunk`, calls
  `grid.apply_storage_trunk(root)` FIRST, then `grid.cmd_migrate_trunk(root,
  None, write=True)`; asserts 2 refs under the trunk, old namespace empty,
  tip shas identical. **Fails on the pre-fix rule** (probe shows old=2,
  trunk=0 failing the `new == 2` / `old == []` assertions).
- `test_migrate_trunk_from_override_with_config_set` — config set and already
  resolved into `REF_NS`, an explicit `source="refs/grid"` still moves.

All 7 previous `migrate_trunk` tests stay green (they now run through the same
new default and move refs as intended).

## Test run

```
python3 -m pytest extensions/agi/tests/test_grid.py -q
128 passed, 14 warnings (pre-existing utcnow deprecation) in 13.55s

python3 -m pytest extensions/agi/tests/test_grid.py -q -k migrate_trunk
9 passed
```

## Safety

No `grid.py` subprocess was run from this round (the shell exports
`AGI_TREE_PROJECT_ROOT` at the LIVE worktree). No live ref moved, no live
`.agi/config.json` edited, no git mutation beyond the one read-only
`git diff --numstat` measurement. The live `--write` + config change remain
**banked to the director** (shared ref store across ~20 worktrees, per
kid #1's cross-worktree finding).

## Evidence

- fix: `cmd_migrate_trunk` source seam + `--from`, 29/12 numstat lines
- probe: pre-fix 0 moved (old=2,trunk=0) / post-fix 2 moved (old=0,trunk=2)
- pytest: 128 passed full file, 9 passed `-k migrate_trunk`


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (EF.08) -- ACCEPTED at inconclusive_lean_proved:85. (1) WHAT THE INSTRUCTION SAID: fix the source-namespace resolution the parent's gate probe falsified -- the hypothesis's config-first order (set grid.storage_trunk, then migrate) must move the refs -- and add a regression test that exercises main()'s REAL sequence (apply_storage_trunk then cmd_migrate_trunk), not a direct call that skips it. (2) WHAT THE MACHINE ACTUALLY DOES: the diff 24a5dffff..4ebf8c52c adds a 4th argument `source` to cmd_migrate_trunk, `old_ns = (source or DEFAULT_REF_NS).strip().rstrip('/')`, a `--from` (dest=from_ns) defaulting to DEFAULT_REF_NS, and dispatch `cmd_migrate_trunk(root, args.to, args.write, args.from_ns)`. My own re-probe of the exact failing sequence now moves 2/2 refs to the trunk with the old namespace empty and tips identical; my independent CLI wire probe (all project-root env vars unset) moves 2 refs through parser -> main -> cmd_migrate_trunk. (3) NEAR MISS: defaulting `--from` to the config-resolved ref_ns_for(root) instead of the module constant DEFAULT_REF_NS -- same no-op by a different spelling; the kid avoided it. An empty --from does NOT fall back to the default (gate probe: 0 moved). (4) DEVIATION: none. The kid called cmd_migrate_trunk(root, None, write=True, source='refs/grid') in one test rather than passing an argv --from, which is the correct function-level seam. STILL BANKED, and this is why the lean is not 'proved': the target's live half -- the real --write on this shared box plus the config change, and conjuncts (e) cron and (f) remote push -- was NOT run. Kid #1 measured the hazard (refs shared via /data/work/agi/.git across ~20 worktrees; config per-worktree) and the parent agrees: bank the live cut to the director. kid #1's human-less incident (a stray CLI call moved 3773 live refs and the parent restored them) is the strongest evidence for that bank.
<!-- THOUGHT:END -->

## Agent Notes
Fixed migrate-trunk source-namespace resolution: added --from (default refs/grid, NOT config-resolved REF_NS) and a source seam on cmd_migrate_trunk; production diff 29/12 numstat, net +17 under the 200 ceiling. Probe on scratch repos shows pre-fix rule (source=REF_NS) 0 moved / old=2 trunk=0 vs post-fix default 2 moved / old=0 trunk=2 through apply_storage_trunk-then-migrate. Two committed regression tests exercise the real main() sequence; full test_grid.py 128 passed, -k migrate_trunk 9 passed. Live --write + config change still banked to director.
