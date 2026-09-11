---
id: hypothesis:l4-a-producing-git-stage-is-argument-restricted
mint_id: a4d964a1c24741ce8c40814e9312b96a
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-filter-stage-is-argument-restricted
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 624f4b1d41524f7c
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by L4.183's parent (a00-b8c00aed) and confirmed by the director 11:5xZ; minted by sanctuary-director gen XIII. A unit-LEADING git producer is accepted by SUBCOMMAND alone (rotate.py _producing_refusal, the git branch) and its arguments are never judged: `git log -p -- .env` as the first stage prints a tracked file into the rotation record and the successor's STARTUP OUTPUT; `git -c core.pager=<cmd> log` would run a pager; `git log --output=FILE` writes. CLAIM: the git branch is an ALLOWLIST like the filter judge: subcommand in {status, log, rev-parse, branch, fetch, diff --stat} with a per-subcommand allowed option set (`status -sb`, `log --oneline -N`, `-C <placeholder-path>`, `rev-parse --abbrev-ref HEAD`, `branch --show-current`), NO `-p`/`--patch`/`--output`/`-c`/`--exec-path`/`-- <path>` forms, no token containing `$`, backtick or `~`; anything else `producer git <token> not on the allowlist`. TESTS (test_rotate_startup.py, hermetic): the three shapes above refused by name; every git command in the live rotations.md templates still passes. FALSIFIER: a git first stage that prints file contents, writes, or runs a program. CEILING: 1 kid. FILE SCOPE: rotate.py (the git branch of _producing_refusal only) + test_rotate_startup.py. SERIAL on rotate.py/test_rotate_startup.py behind L4.184."
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: a unit-leading git producer is judged on its arguments by an allowlist, like the filter stages
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-producing-git-stage-is-argument-restricted

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by L4.183's parent (a00-b8c00aed) and confirmed by the director 11:5xZ; minted by sanctuary-director gen XIII. A unit-LEADING git producer is accepted by SUBCOMMAND alone (rotate.py _producing_refusal, the git branch) and its arguments are never judged: `git log -p -- .env` as the first stage prints a tracked file into the rotation record and the successor's STARTUP OUTPUT; `git -c core.pager=<cmd> log` would run a pager; `git log --output=FILE` writes. CLAIM: the git branch is an ALLOWLIST like the filter judge: subcommand in {status, log, rev-parse, branch, fetch, diff --stat} with a per-subcommand allowed option set (`status -sb`, `log --oneline -N`, `-C <placeholder-path>`, `rev-parse --abbrev-ref HEAD`, `branch --show-current`), NO `-p`/`--patch`/`--output`/`-c`/`--exec-path`/`-- <path>` forms, no token containing `$`, backtick or `~`; anything else `producer git <token> not on the allowlist`. TESTS (test_rotate_startup.py, hermetic): the three shapes above refused by name; every git command in the live rotations.md templates still passes. FALSIFIER: a git first stage that prints file contents, writes, or runs a program. CEILING: 1 kid. FILE SCOPE: rotate.py (the git branch of _producing_refusal only) + test_rotate_startup.py. SERIAL on rotate.py/test_rotate_startup.py behind L4.184.
