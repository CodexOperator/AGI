---
id: hypothesis:g141-c-guard-env-is-read-by-one-validating-parser-never-eval
mint_id: c4772904426f45abb4bdaf1a94126be7
type: hypothesis
parents:
  - goal:g1.41
next_edges: []
confidence: 0.8
edited_by: director-general-1
scaffold_hash: 76171befa0582e8b
season: 2
testable_claim: "(C) the four guard scripts (guard-init.sh, ram-main.sh, ram-tier.sh, session-sweep.sh) read the ```sh guard.env block of config:guard through ONE sourced loader (new guard/guard-env.sh, function guard_env_load <node>) and no `eval` remains in them: (c1) the loader accepts only blank lines, # comments and GUARD_<NAME>=<value> lines whose value is bare [A-Za-z0-9._:/@%+,-]* or single-quoted of that set plus space, = and > and the literal token $HOME; any other line (a command substitution, a backtick, ; | & < > ( ) \\ a double quote or any other $) makes the script exit non-zero naming the node and the line number BEFORE any mount, unit write, sudo or systemctl call, and runs nothing; (c2) $HOME inside a value becomes the invoking user's HOME by string replacement, never eval; (c3) for the 20 live assignments of trunk guard.md the value every script's cell() returns is byte-identical before and after, under HOME=/x/y"
title: "G1.41 C (root piece): the guard scripts read config:guard's guard.env block through ONE validating loader, never eval -- seven eval lines in four files, a merged post edit can no longer run as root in guard-init.sh"
town: core
---
# hypothesis:g141-c-guard-env-is-read-by-one-validating-parser-never-eval

## Measured
- Seven `eval` lines in extensions/agi/guard/ at trunk b71225b92d: guard-init.sh:181 (`eval "$GUARD_ENV_TEXT"`), ram-main.sh:19 + :20, ram-tier.sh:21 + :22, session-sweep.sh:14 + :15 (a block eval and, in each cell(), a second `eval "printf '%s' \"${!v:-...}\""`). sanctuary-health:19 sources /etc/sanctuary-guard/health.env: a root-held file, NOT graph-fed, out of scope.
- WHO runs it as root: guard-init.sh dies unless `[ "$(id -u)" = 0 ]` for apply|uninstall (:150) and its own usage line is `sudo .../guard-init.sh` (:14): root evaluates the block of the checkout it lives in, else /data/work/agi/.agi/nodes/.geometry/guard.md (:172-176). ram-main/ram-tier/session-sweep run as the INSTALLING user (unit `User=$u`, ram-main.sh:89) and call sudo only for mounts.
- THE PATH IS A MERGE, not a write: on this box guard.md is belam:belam 664 in a 775 belam dir (read as director-general-1: not writable). A post's committed edit to the fenced block arrives in the trunk checkout by merge-up, where it is reviewed as prose; the next `sudo guard-init.sh` then evaluates it as root.
- The live block (trunk guard.md, 96 lines) holds 20 assignments: 18 are bare (`GUARD_RAM_MAIN_local_town=/data/work/agi`), 2 are single-quoted values with a literal `$HOME` (GUARD_SWEEP_PAIRS_local_town, GUARD_TIER_DIRS_local_town: '$HOME/.claude $HOME/.pi'). So the inner eval of cell() is a FEATURE (it expands $HOME); the fix keeps that as plain substitution.
- Tests today that read these scripts: test_guard_init_cells.py, test_session_sweep.py, test_ram_write_charge.py, test_ram_worktrees.py; none feeds a hostile block. Script sizes: guard-init 48,977 B, ram-main 8,139, ram-tier 4,539, session-sweep 5,330.

## CLAIM
(C) the four guard scripts (guard-init.sh, ram-main.sh, ram-tier.sh, session-sweep.sh) read the guard.env block of config:guard through ONE sourced loader (new guard/guard-env.sh, function guard_env_load <node>) and no `eval` remains in them: (c1) the loader accepts only blank lines, # comments and GUARD_<NAME>=<value> lines whose value is bare [A-Za-z0-9._:/@%+,-]* or single-quoted of that set plus space, = and > and the literal token $HOME; any other line (a command substitution, a backtick, ; | & < > ( ) a backslash, a double quote or any other $) makes the script exit non-zero naming the node and the line number BEFORE any mount, unit write, sudo or systemctl call, and runs nothing; (c2) $HOME inside a value becomes the invoking user's HOME by string replacement, never eval; (c3) for the 20 live assignments of trunk guard.md the value every script's cell() returns is byte-identical before and after, under HOME=/x/y.

## Dispatch line
config-max: none (the block IS the config; no cell moves, none is added) / template-max: none / code: the shared loader (new file, one function, about 15 lines) and the removal of the seven eval lines.

## FALSIFIERS
A scratch node via GUARD_ENV_NODE whose block adds ONE hostile line, each of: `GUARD_RAM_DIR_local_town=$(touch $M)` · a backtick form · `GUARD_X=1; touch $M` · a function definition · a single-quoted value holding `$(touch $M)` · a value with a second `$VAR`. Run ram-main.sh status, ram-tier.sh sync (empty cells), session-sweep.sh --dry-run and guard-init.sh --dry-run (as a non-root user; nothing mounts) with sudo / systemctl / mount stubs on PATH that log argv: marker $M absent, rc != 0, the message names the node + line, 0 stub argv logged. NEG on the trunk's four scripts: the marker EXISTS for ram-main, ram-tier, session-sweep (and guard-init up to its root check). (c2): under HOME=/x/y the loaded GUARD_TIER_DIRS_local_town is '/x/y/.claude /x/y/.pi'. (c3): the 20 live values, read through each script's cell(), diff-clean against the trunk's. `git grep -nE '\beval\b' -- extensions/agi/guard/*.sh | grep -vE ':[0-9]+:[[:space:]]*#'` prints 0 lines. Mutants, each RED: loader accepts $( · accepts a backtick · accepts ; · $HOME not substituted · the check runs AFTER the first stub call · a script keeps its own eval · the line number missing from the refusal.

## TESTS
a new guard-env.t.sh (shell; goal:g7.16.1.11.16) with the stubs above; test_guard_init_cells.py, test_session_sweep.py, test_ram_write_charge.py, test_ram_worktrees.py stay green (named in the report).

## FILE SCOPE
extensions/agi/guard/guard-init.sh · ram-main.sh · ram-tier.sh · session-sweep.sh · NEW guard/guard-env.sh · extensions/agi/guard/GUARD.md (one line) · the test file (DG2) · the round's experiment node. NEVER the live .agi/nodes/.geometry/guard.md (the block is belam's config), never ram-write.sh, never sanctuary-health.

## CEILING
1 parent (goal:g1.41) · kids <= 1 (DG5, claude-code Sonnet) · <= 24 production lines changed across the four scripts + the loader (a TWO-operand numstat <cut>..<tip before the paste commit>) · no paid agent run beyond the builder.

## Limits (DG1; none blocks the build)
- HOST: none. The units run the scripts by path ($HERE/ram-main.sh), and the loader sits in the same directory, so no unit reinstall is needed; belam re-runs `sudo guard-init.sh` only when he wants it.
- NOT closed here: a root run whose env carries a hostile GUARD_ENV_NODE (sudo scrubs the environment by default; a `sudo -E` would not) and sanctuary-health's root-held health.env source; both named for belam.
