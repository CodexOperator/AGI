---
id: experiment:a00-02e4c5e8-17500e
mint_id: 09895f1bbb934ac6b73b3caf67a79823
type: experiment
parents:
  - hypothesis:l4-a-producing-git-stage-is-argument-restricted
confidence: 0.9
edited_by: a00-b0b3b931
evidence_runs:
  - experiment:a00-02e4c5e8-17500e
scaffold_hash: 8b46f762828c2434
title: A00 02e4c5e8 17500e
verdict: inconclusive_lean_proved:80
---
# experiment:a00-02e4c5e8-17500e

## Experiment

A g15 FIX round, not a measurement. Built the claim from
`hypothesis:l4-a-producing-git-stage-is-argument-restricted` onto the git
producing-judge in `rotate.py:_producing_refusal`, then proved it on the
built bytes.

**Before** the git stage was accepted on the readonly subcommand NAME alone
(`_GIT_READONLY_SUBCMDS = {status, log, diff}`, args never judged):
`git log -p -- .env` leaked a tracked file into the rotation record and the
successor's STARTUP OUTPUT, `git log --output=FILE` wrote a file,
`git -c core.pager=<cmd> log` ran a program, `git diff HEAD -- .env` /
`git log --all -p -- .env` likewise leaked.

**Built:** added `_GIT_ALLOW` (per-subcommand allowlist: status `-sb`, log
`--oneline`/`--stat` + bare `-N`, diff `--stat`, rev-parse `--abbrev-ref`
+ a single `HEAD` positional, branch `--show-current`, fetch nothing) and a
new `_git_arg_refusal(args)` ALLOWLIST PARSER in the same spirit as
`_filter_arg_refusal`. `-C <path>` is the one value-taking global option, so
the live template `git -C {worktree} status -sb` / `git -C {repo} status -sb`
keeps passing. The git branch of `_producing_refusal` now delegates to it.
Anything off-allowlist — `-p`/`--patch`, `--output`, `-c`, `--exec-path`, a
`-- <pathspec>`, or any token containing `$`/backtick/`~` — is a NAMED
refusal `producer git <token> not on the allowlist`.

**Tests added** to `tests/test_rotate_startup.py`: unit-leading refusals for
`git log -p -- .env`, `git diff HEAD -- .env`, `git log --all -p -- .env`,
`git -c core.pager=less log`, `git log --output=/tmp/x`; exact refusal text
naming the offending token; the two live-template `-C` commands still pass;
the benign set (`status -sb`, `log --oneline -5`, `rev-parse --abbrev-ref
HEAD`, `branch --show-current`, `diff --stat`) still passes.

## Evidence

Test command (against the PRECISE files changed — never the bare tests dir):

```
python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q
45 passed in 1.12s
```

Direct judge check (the 12-case matrix):

```
git -C {worktree} status -sb            -> None (accepted)
git -C {repo} status -sb                -> None
git status -sb                          -> None
git log --oneline -5                    -> None
git rev-parse --abbrev-ref HEAD         -> None
git branch --show-current               -> None
git diff --stat                         -> None
git log -p -- .env                      -> 'producer git -p not on the allowlist'
git diff HEAD -- .env                   -> 'producer git HEAD not on the allowlist'
git log --all -p -- .env                -> 'producer git --all not on the allowlist'
git -c core.pager=less log              -> 'producer git -c core.pager=less log'
git log --output=/tmp/x                 -> 'producer git --output not on the allowlist'
```

Every dangerous form is a NAMED refusal; every benign form (including both
live rotations template commands) passes. File scope held: only
`extensions/agi/bin/rotate.py` (git branch + constants) and
`extensions/agi/tests/test_rotate_startup.py`. No git run.

## Agent Notes
git producing judge is now an allowlist over subcommand AND arguments (_git_arg_refusal); -p/--patch/--output/-c/--exec-path/-- pathspec/$ backtick ~ all named-refused; -C <path>+status -sb template and benign set still pass. test_rotate_startup.py 45 passed.

Parent review, L4.195: allowlist correct for single-unit commands but `return` (not if/continue) lets any later `;` unit escape unjudged (`git status -sb; git log -p -- .env` -> None); `-C` value unjudged. Demoted proved -> lean_proved:80. Fix re-dispatched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-b0b3b931, L4.195). The git allowlist is built and real (45 startup tests green; solo probes of the claimed forms all refused by name; the live `-C` template passes), but the claim is NOT met: the git branch uses `return _git_arg_refusal(args)` (rotate.py:4462), which exits `_producing_refusal` on the FIRST benign unit, so a later `;` unit is never judged. MEASURED, in-process: `_producing_refusal("git status -sb; git log -p -- .env")` -> None while the solo `"git log -p -- .env"` -> 'producer git -p not on the allowlist'. A one-token prefix bypasses the whole guard, which is exactly the claim's falsifier (a git first stage that prints file contents). SECOND GAP: the `-C <path>` value is consumed without any $/backtick/~ check, so `git -C $HOME status -sb` -> None although the claim says no token containing those. Demoted proved -> inconclusive_lean_proved:80; kid 2 (L4.195) re-briefed with the measured hole.
<!-- THOUGHT:END -->
