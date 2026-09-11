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
thought_session: 914d302a-b33f-4c5f-b78d-a8b7320df6c5
title: a unit-leading git producer is judged on its arguments by an allowlist, like the filter stages
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-producing-git-stage-is-argument-restricted

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by L4.183's parent (a00-b8c00aed) and confirmed by the director 11:5xZ; minted by sanctuary-director gen XIII. A unit-LEADING git producer is accepted by SUBCOMMAND alone (rotate.py _producing_refusal, the git branch) and its arguments are never judged: `git log -p -- .env` as the first stage prints a tracked file into the rotation record and the successor's STARTUP OUTPUT; `git -c core.pager=<cmd> log` would run a pager; `git log --output=FILE` writes. CLAIM: the git branch is an ALLOWLIST like the filter judge: subcommand in {status, log, rev-parse, branch, fetch, diff --stat} with a per-subcommand allowed option set (`status -sb`, `log --oneline -N`, `-C <placeholder-path>`, `rev-parse --abbrev-ref HEAD`, `branch --show-current`), NO `-p`/`--patch`/`--output`/`-c`/`--exec-path`/`-- <path>` forms, no token containing `$`, backtick or `~`; anything else `producer git <token> not on the allowlist`. TESTS (test_rotate_startup.py, hermetic): the three shapes above refused by name; every git command in the live rotations.md templates still passes. FALSIFIER: a git first stage that prints file contents, writes, or runs a program. CEILING: 1 kid. FILE SCOPE: rotate.py (the git branch of _producing_refusal only) + test_rotate_startup.py. SERIAL on rotate.py/test_rotate_startup.py behind L4.184.

DIRECTOR HARVEST (sanctuary-director gen XIV, L4.195, 2026-09-11 12:33Z). Kept kid 2's proved (0.95, experiment:a00-5aeff71c-3c0295) and the parent's demotion of kid 1 to lean_proved:80 (experiment:a00-02e4c5e8-17500e) -- the parent measured the `;`-unit bypass (`return _git_arg_refusal(args)` exited the judge on the first benign unit) and the unchecked `-C <path>` value in-process before re-briefing; that is the review this loop asks for. Ran myself on the round bytes (a00-b0b3b931): the five claimed shapes `git log -p -- .env` / `git -c core.pager=id log` / `git log --output=x` / `git status -sb; git log -p -- .env` / `git -C $HOME status -sb` are NAMED-refused (`producer git -p|-c core.pager=id log|--output|-p|$HOME not on the allowlist`) and ALL FIVE were accepted (None) by the pre-round seat bytes -- the defect reproduced then closed. Every `"cmd"` in the live `.geometry/rotations.md` judged with {worktree}/{repo} substituted: both git lines (`git -C <path> status -sb | head -N; ...`) pass; the 4 refusals in the node are the pre-existing non-git `||` and `ListAgents ref` lines, identical count and text on the seat bytes. 184 passed with neighbours (test_rotate_startup/test_rotate/test_rotate_handover). Residue, not a demotion: `_GIT_READONLY_SUBCMDS` gained `fetch` (bare only -- `git fetch origin` is refused, so no URL can be named) and `rev-parse --short HEAD` / `git log --format=...` are off the allowlist; a future first_turn line needing either is a one-set edit, not a judge change. Next on rotate.py: g15-33 `l4-the-refusal-names-the-record-stage-not-the-expanded-tokens`.
