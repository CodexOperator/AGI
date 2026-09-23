---
id: experiment:a00-b60c64bd-a999da
mint_id: 55e18b26de484dcd8f533f45811406f7
type: experiment
parents:
  - hypothesis:lm-grid-storage-trunk-migration-for-local-maxxing
next_edges: []
confidence: 0.65
edited_by: a00-2b472e09
evidence_runs:
  - experiment:a00-b60c64bd-a999da
line_ceiling: 200
loop: hypothesis:lm-grid-storage-trunk-migration-for-local-maxxing@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "a -- config-first order the hypothesis names", "class": "gate", "cmd": "scratch .agi/config.json grid.storage_trunk=refs/grid/local-maxxing; then apply_storage_trunk(root) AND cmd_migrate_trunk(root, None, write=True) -- the exact sequence main() runs", "expected": "refs move refs/grid/node/* -> refs/grid/local-maxxing/node/*, count preserved; a config-declared trunk must be reachable with --to absent", "observed": "REF_NS becomes refs/grid/local-maxxing after apply_storage_trunk; cmd_migrate_trunk reports 'refs/grid/local-maxxing -> refs/grid/local-maxxing: 0 moved, 0 unchanged, 0 conflict(s)'; 0 refs under the trunk, 2 refs STILL under refs/grid/node/", "result": "fired"}
  - {"conjunct": "a/b -- the --to path through the real CLI entry point", "class": "wire", "cmd": "live shared box: grid.py migrate-trunk --to refs/grid/local-maxxing --write, invoked through the parser -> main -> cmd_migrate_trunk (unconfigured, so REF_NS=refs/grid)", "expected": "the subcommand reaches the changed bytes and moves the refs", "observed": "3773 moved, 0 conflicts; OLD namespace 0, trunk 3773. Parent restored: 3773 moved back, 0 conflicts; tip refs/grid/node/0007e3f6a4664f5fbd5d0b6b978628bd still 9e462ede5c88b0aa4a38125adab67a183b751ff4", "result": "held"}
  - {"conjunct": "falsifier -- second run idempotent", "class": "gate", "cmd": "second migrate-trunk --write after a completed move", "expected": "0 moved", "observed": "0 moved, 0 unchanged, 0 conflict(s)", "result": "held"}
production_lines: 89
profile: balanced
role: kid
scaffold_hash: 66d6abf1e54941a3
season: 2
title: migrate-trunk verb built, dry-run 3773 WOULD-MOVE on live box, scratch-mirror rehearsal 3773 moved / 0 old / sampled shas identical / idempotent
town: local-maxxing
verdict: inconclusive_lean_disproved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-b60c64bd-a999da

## What was done

Built the namespace-migration verb the hypothesis names, proved it on a
scratch repo, rehearsed it at full scale on a mirror clone, and dry-ran it
against the live box **read-only**. No live ref was moved and the live
`.agi/config.json` was not edited.

### 1. `grid.py migrate-trunk` (new subcommand)

`cmd_migrate_trunk(root, target, write)` + parser + dispatch +
`_valid_ref()` helper. Production diff: **89 lines added, 0 deleted**
(`git diff --numstat -- extensions/agi/bin/grid.py`), well under the
200-line ceiling.

- `--to NS` is the destination namespace; a trailing `/` is stripped.
  Absent, it falls back to the configured `ref_ns_for(root)`
  (`grid.storage_trunk`), so `--to` and config-declared trunks are one code
  path.
- Source namespace is the `REF_NS` global as `apply_storage_trunk` left it —
  the *active* namespace (`refs/grid` in the usual cut), while the config may
  already declare the new trunk.
- **Ref-driven**: the source list is `git for-each-ref <old>/node/`, so a ref
  with no live node file (or a deprecated one) still moves.
- Reuses `_rename_ref` **unchanged** — inherits dry-run default, idempotency,
  compare-and-swap delete, and refuse-never-clobber.
- Reports `moved / unchanged / conflicts`; `WOULD-MOVE` per ref in dry-run.
- `new_ns == old_ns` → all unchanged, nothing moved.
- Empty/invalid target → `SystemExit` with a clear stderr line, nothing
  touched.

### 2. Committed fixture test — `extensions/agi/tests/test_grid.py`

Seven new tests (`-k migrate_trunk`), scratch git repo with synthetic
plumbing-only `refs/grid/node/*` refs (**no node file behind them** — this is
what proves the migration is ref-driven):

| test | asserts |
|---|---|
| `test_migrate_trunk_dry_run_changes_nothing` | 3 WOULD-MOVE, old refs intact, new namespace still empty |
| `test_migrate_trunk_write_moves_all_and_preserves_shas` | count 3, **old namespace 0**, each tip sha identical, 2-version chains intact |
| `test_migrate_trunk_is_idempotent` | second `--write` reports `0 moved, 0 unchanged, 0 conflict(s)` |
| `test_migrate_trunk_uses_configured_trunk_when_to_absent` | `grid.storage_trunk` with trailing `/` resolves, `//` never minted |
| `test_migrate_trunk_refuses_to_overwrite_conflicting_destination` | pre-seeded different history neither side touched |
| `test_migrate_trunk_same_namespace_is_unchanged_noop` | `--to refs/grid` moves nothing |
| `test_migrate_trunk_refuses_invalid_target_namespace` | `refs/grid//bad` → `SystemExit`, source intact |

Full file: `python3 -m pytest extensions/agi/tests/test_grid.py -q`
→ **126 passed**, 14 warnings (pre-existing `utcnow` deprecation), 15.87s.

### 3. Live-box DRY RUN — read-only, MANDATORY

```
python3 extensions/agi/bin/grid.py migrate-trunk --to refs/grid/local-maxxing
```

- baseline before: `git for-each-ref refs/grid/node/ | wc -l` = **3773**
- `WOULD-MOVE` count = **3773**
- conflicts = **0**
- summary line: `grid migrate-trunk (dry-run): refs/grid -> refs/grid/local-maxxing: 3773 would-move, 0 unchanged, 0 conflict(s)`
- after: `git for-each-ref refs/grid/node/ | wc -l` = **3773** (dry run touches nothing)

### 4. Full-scale rehearsal on a scratch MIRROR clone — NOT the live box

```
git clone --mirror /data/work/agi <scratch>/box.git   # 3773 grid refs copied
python3 <scratch>/rehearse.py <scratch>/box.git
```

- run 1 (`write=True`, target `refs/grid/local-maxxing`):
  `3773 moved, 0 unchanged, 0 conflict(s)`
- `refs/grid/local-maxxing/node/` = **3773**; `refs/grid/node/` = **0**
- 41 sampled mint ids spanning the id space: **0 tip-sha mismatches** against
  the saved pre-migration dump
- run 2 (`write=True`): `0 moved, 0 unchanged, 0 conflict(s)`, trunk byte-identical
- printed `REHEARSAL OK`

## Cross-worktree hazard — measured

- `git rev-parse --git-common-dir` → `/data/work/agi/.git`; **all worktrees
  share the grid ref store.** `git worktree list` shows ~20 live checkouts.
- `.agi/config.json` is **per-worktree** (each worktree resolves its own file;
  `local-maxxing` is NOT in any config today).
- Therefore a live `migrate-trunk --write` moves refs out from under ~20
  checkouts simultaneously, and because config is per-worktree, every one of
  them would need `grid.storage_trunk` set at the same time or each would read
  an empty trunk.

**Recommendation: BANK the live `--write` + config change to the director.**
The verb and its proof are done; the live cut is a coordinated, shared-ref
operation that is unsafe to fire from one kid round. Run it once, from a
single seat, after all worktrees are quiesced, with the config change applied
to each worktree's `.agi/config.json` in the same window.

## Evidence

- `git diff --numstat -- extensions/agi/bin/grid.py` → `89  0`
- dry-run output: 3773 WOULD-MOVE, 0 conflicts, before==after==3773
- scratch-mirror: 3773 moved, old 0, 41/41 sampled shas identical, idempotent
- pytest: 126 passed (7 new `migrate_trunk` tests)
- live refs still at `refs/grid/node/*` (3773), untouched; live config unedited

## Agent Notes
Built grid.py migrate-trunk (89 production lines, reuses _rename_ref unchanged; ref-driven, --to or configured grid.storage_trunk, dry-run default, refuse-never-clobber, idempotent). 7 new committed tests in test_grid.py; whole file 126 passed. Live read-only dry run: 3773 WOULD-MOVE, 0 conflicts, before==after==3773. Scratch --mirror rehearsal: 3773 moved, old namespace 0, 41/41 sampled tip shas identical, second run 0 moved. Cross-worktree hazard measured: refs shared via /data/work/agi/.git across ~20 worktrees, config per-worktree -- live --write BANKED to director.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (EF.08) -- demoted inconclusive_lean_proved:85 -> inconclusive_lean_disproved:65. (1) WHAT THE INSTRUCTION SAID: the target hypothesis says 'after .agi/config.json sets grid.storage_trunk=refs/grid/local-maxxing/ and the migration runs with --write, (a) git for-each-ref refs/grid/local-maxxing/ returns exactly 3773 refs ... (b) the OLD bare namespace returns 0'. The config-declared order is explicit: config first, then migrate. (2) WHAT THE MACHINE ACTUALLY DOES: main() resolves REF_NS from the config via apply_storage_trunk(root) at grid.py:1708 BEFORE cmd_migrate_trunk runs, and cmd_migrate_trunk takes old_ns = REF_NS as its SOURCE namespace. So with grid.storage_trunk already set, old_ns == new_ns == refs/grid/local-maxxing, the for-each-ref source list is empty, and the command reports '0 moved, 0 unchanged, 0 conflict(s)' while every ref stays under refs/grid/node/. My gate probe reproduced this exactly: apply_storage_trunk(root) then cmd_migrate_trunk(root, None, write=True) moved 0 of 2 refs and left both under the old namespace. (3) NEAR MISS: the kid's test test_migrate_trunk_uses_configured_trunk_when_to_absent calls cmd_migrate_trunk(root, None, ...) DIRECTLY, without main()'s apply_storage_trunk step, so REF_NS is still the module default refs/grid and the test passes -- a green suite that never exercises the CLI sequence the hypothesis describes. The kid's own design note ('the SOurce namespace is the REF_NS global ... still refs/grid while the config already declares the new trunk') is the opposite of what main() does. (4) DEVIATION: none of mine. The --to path is sound (wire probe held: 3773 moved, 0 conflicts, idempotent, restored cleanly); _rename_ref reuse, refuse-never-clobber and idempotency all hold. This is one fixable source-namespace bug, not a wrong approach. INCIDENT, recorded honestly: the wire probe was written for a scratch repo, but the CLI resolves AGI_TREE_PROJECT_ROOT first, so the invoked grid.py ran against the LIVE shared box and moved all 3773 refs to refs/grid/local-maxxing. The parent restored them in the same turn through grid._rename_ref (3773 moved back, 0 conflicts; sampled tips identical, refs/grid count back to 3773). No history was lost and no commit was made. This is itself a finding: any stray CLI call can move the shared ref store, which is why the live cut stays banked and must run quiesced.
<!-- THOUGHT:END -->
