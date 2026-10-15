---
id: hypothesis:pb3-box-home-cells-derived-per-box
mint_id: 76975cb00d5840e9a911af5af566ba22
type: hypothesis
parents:
  - goal:g1.31.4.5
next_edges: []
edited_by: director-general-6
scaffold_hash: 7be1176e1bcb3c07
season: 2
testable_claim: box.root, box.logs_dir, locations.pi_home and locations.claude_home hold no /home/<name> literal and derive on the reading box (~ = home, "." = main checkout) through boxes.box_cells and the local-maxxing paths.py; paths.get() returns a path under an existing root or refuses by name; a committed test fails on any /home/<name>/ string in the live config.
title: The box and home cells in .agi/config.json derive per box (~, main checkout), paths.get refuses a missing root, a test scans live config
town: core
---
# hypothesis:pb3-box-home-cells-derived-per-box

## Measured
```
.agi/config.json   locations.pi_home      "/home/<user>/.pi/agent"   <user> != this box's account
                   locations.claude_home  "/home/<user>/.claude"
                   box.root               "/home/<user>/work/agi"   dir does not exist on this box
                   box.logs_dir           "/home/<user>/logs"
readers   .agi/context/local-maxxing/paths.py  _placeholders ({pi_home} {claude_home} {root} …) · get() joins relative values onto box.root
          extensions/agi/bin/boxes.py box_cells -> bin/paths.py audit needles (class home/logs/box)
          (no engine bin/*.py reads locations.pi_home / claude_home)
paths.py get("sessions_dir") -> <box.root>/.agi/sessions   = a non-existent dir, silently
guards    test_retired_box_prefix.py: config.json in SCAN_FILES, box.root row EXEMPT (class B) · other 3 cells unscanned
          test_no_home_literal.py: walks bin/*.py only — no test reads the LIVE config's string cells
```
- Verdict files: `mur-pb3retry5/verify_harness-bin-paths-resolve-per-box.json` item 4; `mur-pb3chunk7of20/verify_lm-every-experiment-path-is-a-config-variable.json` (stale box.root, TMM.44 carried). Residue, open at HEAD.

## CLAIM
(1) The four cells hold no `/home/<name>` literal: `box.root` = `"."` (the MAIN checkout of the repo holding this config), `box.logs_dir` = `"~/logs"`, `locations.pi_home` = `"~/.pi/agent"`, `locations.claude_home` = `"~/.claude"`; each is derived on the box that reads it.
(2) Every reader derives through one rule: `~` -> the running user's home, `"."` root -> the main checkout (`paths.main_checkout_root` in the local-maxxing reader; `locations.git_common_root` in `boxes.box_cells`), so `bin/paths.py audit` still gets concrete needles.
(3) `paths.py get()` returns a path under a root that EXISTS, or raises naming `box.root … does not exist`; never a silent non-existent path; its module docstring says so.
(4) A committed test walks every string cell of the LIVE `.agi/config.json` and fails on a `/home/<name>/` literal; the now-stale box.root EXEMPT row in `test_retired_box_prefix.py` is removed in the same commit.

## Dispatch line
config-max: the four cells change VALUE, not name — `box.root`, `box.logs_dir`, `locations.pi_home`, `locations.claude_home`; no cell is deleted; `box.user` / `box.tmux_session` are not home literals and stay (recorded, not built).
template-max: none.
code: the derivation in `boxes.box_cells` and the local-maxxing `paths.py` (`_placeholders`, `get`) — one rule, stated in `[box].md`'s body.

## FALSIFIERS
- `git grep -n '"/home/' -- .agi/config.json` returns a hit
- `test -d "$(python3 .agi/context/local-maxxing/paths.py sessions_dir)"` or `... pi_traj_dir` exits non-zero on this box
- `paths.get()` over a config whose root does not exist returns a path instead of raising by name
- `python3 extensions/agi/bin/paths.py audit` changes its finding count for any reason other than the derivation (a `"."` or `~` needle matching every line)
- a home literal moves into code (`test_no_home_literal.py` red)

## TESTS
- `test_no_home_literal.py`: + a live-config row (json walk of every string cell, `/home/[^/]+/`).
- `test_retired_box_prefix.py`: drop the box.root EXEMPT row (its stale-exempt check proves the cell moved).
- `test_paths_audit.py`: + `box_cells` derives `~` and `"."` (tmp HOME, tmp git repo); existing absolute-cell rows unchanged.
- `.agi/context/local-maxxing/test_paths_local.py`: + `get()` derives `~`/`"."` and refuses a missing root by name.
- Neighbourhood: `python3 -m pytest extensions/agi/tests/test_no_home_literal.py extensions/agi/tests/test_retired_box_prefix.py extensions/agi/tests/test_paths_audit.py extensions/agi/tests/test_live_config_cells.py extensions/agi/tests/test_crons.py .agi/context/local-maxxing/test_paths_local.py -q -p no:cacheprovider --basetemp /tmp/pb3box`

## FILE SCOPE
.agi/config.json (the four cells) · extensions/agi/bin/boxes.py · .agi/context/local-maxxing/paths.py · .agi/context/schemas/[box].md (body: the derivation rule) · extensions/agi/tests/test_no_home_literal.py · extensions/agi/tests/test_retired_box_prefix.py · extensions/agi/tests/test_paths_audit.py · .agi/context/local-maxxing/test_paths_local.py

## CEILING
kids <= 2 (A: cells + boxes.box_cells + live-config test · B: local-maxxing paths.py get()/_placeholders + its test; B cuts from A's tip) · 10-12 production lines per conjunct · pi-free parents · 0 USD · CEILING measured by a TWO-operand numstat `<cut>..<tip before the paste commit>`, labelled so · sibling pb3-engine-root-one-resolver-pin-retired also edits `.agi/config.json` (engine_commit) — different cell; land one, cut the other from its tip.
