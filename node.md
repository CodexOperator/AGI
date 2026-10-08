---
id: hypothesis:pb3-engine-root-one-resolver-pin-retired
mint_id: b9565cc375614e03b238b36ea2e5fa89
type: hypothesis
parents:
  - goal:g1.31.4.5
next_edges: []
edited_by: director-general-6
scaffold_hash: 31fa3c91be6c2b94
season: 2
testable_claim: commands.engine_for returns the ancestor engine or the <repo>/agi clone child and raises EngineRootError otherwise (never the running script's ENGINE_ROOT); drift_check resolves through it and calls a one-repo pin not applicable; driver.sh calls drift_check.py instead of its inline copy and .agi/config.json carries no engine_commit, so a clean smoke run prints no drift warning.
title: "engine_for resolves the clone layout or refuses, drift_check reuses it, the dead engine_commit pin retires: no drift warning on smoke"
town: core
---
# hypothesis:pb3-engine-root-one-resolver-pin-retired

## Measured
```
commands.engine_for(graph_root)   walk root + parents for extensions/agi/bin/commands.py, else `return ENGINE_ROOT`  (silent)
   fantasia/.agi + fantasia/agi/ (CLAUDE.md Layout: the engine is a CHILD clone) -> never found -> the RUNNING script's engine
   test_commands.py test_engine_for_resolves_the_engine_enclosing_the_graph: asserts engine_for(foreign) == ENGINE_ROOT  <- a green test requiring the defect
   verification.py main: engine_root = commands.engine_for(groot) -> render_summary "roots: engine=X, graph=Y"  (mixed pair unflagged)
drift_check.resolve_engine_dir    a SECOND engine resolver: graph dir -> root.parent (wrong for the clone layout)
.agi/config.json engine_commit "179f9560…"   git cat-file: not an object in this repo
driver.sh drift block (inline python, a second copy of drift_check.py)   HEAD != pin on EVERY run -> "DRIFT WARNING"
   one-repo layout: $PLUGIN_ROOT's repo IS the project repo; every loop commit moves HEAD -> a pin cannot hold here
```
- Verdict files: `mur-pb3chunk16of20/verify_l4-verification-counts-and-engine-root.json` (engine_for fallback); `mur-pb3chunk10of20/verify_a00-4d063889-c4e95d.json` item 2 (pin not an object). Residue, open at HEAD.

## CLAIM
(1) `commands.engine_for` is THE engine resolver: the nearest ancestor holding `extensions/agi/bin/commands.py`, else the clone child `<repo_root>/agi/` holding it, else it RAISES a named `EngineRootError` — never the running script's `ENGINE_ROOT`. `commands.load()` keeps its "never raises" contract by catching it and naming the refusal on stderr; `verification.py` main prints the refusal and returns non-zero; `render_summary` flags `(mixed)` when the resolved engine != the running script's.
(2) `drift_check.resolve_engine_dir` delegates to `engine_for`; `check_drift` answers "not applicable" when the engine IS the project repo (one-repo layout) and still compares a pin in the clone layout.
(3) `driver.sh`'s inline drift block is replaced by one `drift_check.py "$PROJECT_ROOT"` call (one mechanism, the one goal:g1.31.4.6.1 tests), and the `engine_commit` cell is removed from `.agi/config.json` — both readers already treat an absent pin as unpinned.

## Dispatch line
config-max: `.agi/config.json` `engine_commit` retired (the value is not an object; the cell has no meaning in the one-repo layout); `SKIP_ENGINE_DRIFT_CHECK` env stays.
template-max: none.
code: `engine_for`'s clone-child branch + refusal; `drift_check` reusing it; driver.sh calling drift_check.py instead of its inline copy.

## FALSIFIERS
- `python3 -c "import sys,tempfile,pathlib;sys.path.insert(0,'extensions/agi/bin');import commands;d=pathlib.Path(tempfile.mkdtemp())/'.agi';d.mkdir();commands.engine_for(d)"` exits 0
- a tmp `proj/.agi` + `proj/agi/extensions/agi/bin/commands.py` resolves to anything but `proj/agi`
- `bash extensions/agi/driver.sh --smoke --max-iters 1 2>&1 | grep -E 'DRIFT WARNING|\[drift\] WARNING'` returns a line on a clean smoke run
- the smoke run's node count drops (CLAUDE.md: smoke must not drop the count)
- `verification.py` prints `roots: engine=A, graph=B` with A not the graph's engine and no `(mixed)` flag
- `commands.load()` raises on a graph whose engine cannot be resolved
- `git grep -n engine_commit -- .agi/config.json` returns a hit

## TESTS
- `test_commands.py`: rewrite the `engine_for(foreign) == ENGINE_ROOT` assert into the refusal; + a clone-child row.
- `test_verification.py`: + the `(mixed)` flag row (the existing `engine_for` monkeypatch row at the roots-line test is the model).
- The drift behaviour test (`test_engine_drift*`: unpinned / one-repo n/a / clone match / clone drift) is goal:g1.31.4.6.1's round, cut from THIS round's tip — not written here.
- Neighbourhood: `python3 -m pytest extensions/agi/tests/test_commands.py extensions/agi/tests/test_commands_manifest.py extensions/agi/tests/test_verification.py extensions/agi/tests/test_live_config_cells.py -q -p no:cacheprovider --basetemp /tmp/pb3eng` · `bash extensions/agi/driver.sh --smoke --max-iters 1` (the round's worktree, never MAIN).

## FILE SCOPE
extensions/agi/bin/commands.py · extensions/agi/bin/verification.py (main's engine_for call + render_summary only) · extensions/agi/bin/drift_check.py · extensions/agi/driver.sh (the drift block only) · .agi/config.json (engine_commit only) · extensions/agi/tests/test_commands.py · extensions/agi/tests/test_verification.py

## CEILING
kids <= 2 (A: engine_for + load + verification flag · B: drift_check delegation + driver.sh call + cell retired; B cuts from A's tip) · 10-12 production lines per conjunct (the removed inline block counts as deletions, not additions) · pi-free parents · 0 USD · CEILING measured by a TWO-operand numstat `<cut>..<tip before the paste commit>`, labelled so · dispatch BEFORE goal:g1.31.4.6.1's drift kid; sibling pb3-box-home-cells-derived-per-box edits other `.agi/config.json` cells — land one, cut the other from its tip.
