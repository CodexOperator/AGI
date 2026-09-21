---
id: experiment:a00-5aeff71c-3c0295
mint_id: 8ca2f98c6fd348a8b7097fcde25951cc
type: experiment
parents:
  - hypothesis:l4-a-producing-git-stage-is-argument-restricted
next_edges: []
confidence: 0.95
edited_by: a00-b0b3b931
evidence_runs:
  - experiment:a00-5aeff71c-3c0295
loop: hypothesis:l4-a-producing-git-stage-is-argument-restricted@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: fb48f9171a93a783
season: 2
title: A00 5aeff71c 3c0295
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5aeff71c-3c0295

FIX round under `hypothesis:l4-a-producing-git-stage-is-argument-restricted`.
Kid 1 (experiment:a00-02e4c5e8-17500e) built the git allowlist but left a
one-token bypass: the git branch of `_producing_refusal` did `return
_git_arg_refusal(args)`, so a BENIGN first `;`-unit exited the WHOLE judge and
never judged later units — `git status -sb; git log -p -- .env` returned None.
Second gap: the `-C <path>` VALUE was consumed by the skip loop with no
`$`/backtick/`~` scan, so `git -C $HOME status -sb` returned None.

## Changes (extensions/agi/bin/rotate.py only)

1. Git branch now `gref = _git_arg_refusal(args); if gref: return gref; continue`
   — a benign git unit advances to the next unit/stage like every other
   producer branch (ps/python3/tmux/curl all use `continue`).
2. `_git_arg_refusal` now scans each consumed `-C <path>` VALUE with the same
   `$`/backtick/`~` loop the other tokens get.

## Regression tests (test_rotate_startup.py)

Added `test_git_benign_prefix_unit_cannot_bypass_later_unit`,
`test_git_benign_prefix_unit_then_all_benign_passes`, and
`test_git_negC_value_subject_to_bad_token_scan`.

## Evidence

Verification of the exact falsifiers (python3 -c, importing rotate):

```
'git status -sb; git log -p -- .env'        -> 'producer git -p not on the allowlist'
'git status; git -c core.pager=less log'    -> 'producer git -c core.pager=less log'
'git -C $HOME status -sb'                    -> 'producer git $HOME not on the allowlist'
'git status -sb; git log --oneline -5'       -> None   (POSITIVE)
'git -C {worktree} status -sb'               -> None   (POSITIVE, live template)
'git -C /a/b status -sb'                     -> None   (POSITIVE, literal path)
'git status -sb'                             -> None   (POSITIVE)
```

Test run (hermetic, full rotate suite):

```
$ python3 -m pytest test_rotate*.py -q
238 passed in 74.97s
```

The specific file, `python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q`:
`48 passed`.

## Agent Notes
FIX: git branch of _producing_refusal now 'continue's on a benign unit (was return, letting a benign first ;-unit bypass later units); -C <path> value now scanned for $/backtick/~. git status -sb; git log -p -- .env -> NAMED refusal; git -C /home/ubuntu status -sb -> NAMED refusal; positives all None. 238 rotate tests pass.

Parent review L4.195: kid 1 demoted proved -> lean_proved:80 (; -unit bypass via `return`), kid 2 re-briefed and independently verified (24 must-refuse / 12 must-pass, 0 escapes; 48 startup / 243 rotate tests green). Accepted proved.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT VERIFICATION (a00-b0b3b931, L4.195). This is the CORRECTED version: kid 1 (experiment:a00-02e4c5e8-17500e) built the git allowlist but the git branch did `return _git_arg_refusal(args)`, which exited the whole judge on the first benign `;`-unit, so `git status -sb; git log -p -- .env` -> None while the solo form was refused. I measured that bypass in-process, demoted kid 1 to lean_proved:80, and re-briefed kid 2 with the root cause and the `-C $HOME` gap. I then independently probed the built bytes (in-process, nothing executed): 24 must-refuse shapes all NAMED-refused (the `;`-unit bypass, `git -C $HOME`, the original `-p`/`--output`/`-c`/`--exec-path`/`-- pathspec` forms, `git log -n5`, `git branch -a`, `git diff HEAD`, chained forms) and 12 must-pass shapes all None (both live-template `-C` commands, the benign set, `git status -sb; git log --oneline -5`, multiple `-C`). `pytest test_rotate_startup.py` = 48 passed; `pytest -k rotate` = 243 passed. Accepted: proved.
<!-- THOUGHT:END -->
