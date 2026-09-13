---
id: experiment:a00-029a0536-bfd0c2
mint_id: 706bd63ddaa74f95b5fd98f5913215ef
type: experiment
parents:
  - hypothesis:l4-rename-post-renames-every-surface-atomically-at-the-next-rotation-boundary-with-season-long-aliases-point-director-then-sanctuary-director
next_edges: []
confidence: 0.9
edited_by: a00-b4841f18
evidence_runs:
  - experiment:a00-029a0536-bfd0c2
loop: hypothesis:l4-rename-post-renames-every-surface-atomically-at-the-next-rotation-boundary-with-season-long-aliases-point-director-then-sanctuary-director@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 2, "class": "wire", "cmd": "cmd_rename_post(--apply --live --delete-old) with subprocess.run monkeypatched to a recorder", "expected": "the verb EXECUTES the git/tmux renames with the claim's exact argv, tmux by resolved @id", "observed": "git -C <root> worktree move .agi/worktrees/post-old .agi/worktrees/post-new; branch -m season2/posts/old season2/posts/new; push origin season2/posts/new; push origin :season2/posts/old (only under --delete-old); tmux list-windows -> rename-window -t @5 new; list-sessions -> rename-session -t $4 view-new", "result": "held -- the shipped verb can execute every seam surface"}
  - {"conjunct": 2, "class": "gate", "cmd": "cmd_rename_post(--apply, no --live) with subprocess.run monkeypatched", "expected": "default stays print-only, subprocess.run called ZERO times", "observed": "rc 0, subprocess calls = 0; the seams print '[seam-git/seam-tmux] would-run'", "result": "held -- safe default unchanged"}
  - {"conjunct": 2, "class": "gate", "cmd": "rotate._live_git on a monkeypatched rc=128", "expected": "a failed rename cannot be mistaken for success", "observed": "prints 'git branch -m a b -> rc 128' + stderr, raises RuntimeError('... failed (rc 128)')", "result": "held -- loud failure"}
profile: balanced
role: kid
scaffold_hash: 0b5e58c1463e75cf
season: 2
title: A00 029a0536 bfd0c2
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-029a0536-bfd0c2

## Experiment (KID 4 — close the one gap: the shipped verb cannot EXECUTE git/tmux renames)

Kids 1-3 built `rotate.py rename-post` with full-surface enumeration, staging, alias resolution, and the print-only `_seam_git`/`_seam_tmux` defaults. Parent probe confirmed the gap: `cmd_rename_post` called `_apply_surfaces` with NO `run_git`/`run_tmux` injection, so a caller could never make it actually rename the branch/worktree/tmux — there was no `--live`. This run added, in `extensions/agi/bin/rotate.py` + `extensions/agi/tests/test_rename_post.py` ONLY:

1. **`--live` flag** on the `rename-post` subparser (default OFF). With `--live` + `--now`/`--apply`, `cmd_rename_post` injects REAL executors:
   - `_live_git(root, *a)` runs `git -C <root> <args>` via `subprocess.run`, prints `git <args> -> rc N` to stderr, echoes stderr text, and RAISES `RuntimeError` on non-zero rc (a failed rename can't be mistaken for success).
   - `_live_tmux(root, *a)` runs `tmux <args>`, prints `tmux <args> -> rc N`, raises on failure, and RETURNS the command's stdout text so `_resolve_tmux_id` can parse the list-windows/list-sessions listing and rename by a real `@N`/`$N`.
2. **`_apply_staged`** already accepted `run_git`/`run_tmux` and forwards them; docstring now names the privileged injection (`lambda *a: rotate._live_git(root, *a)`) so the Prime at merge-up can run the boundary apply live. Default stays print-only.
3. **Default (no `--live`) is byte-for-byte unchanged**: print-only seams, `subprocess.run` called ZERO times. Proven by `test_default_apply_calls_subprocess_zero_times`.

The live landing is the Prime's / merge-up's, never a fixture's: tests monkeypatch `subprocess.run` and never run real git/tmux.

## Evidence

`python3 -m pytest extensions/agi/tests/test_rename_post.py -q` → **24 passed** (was 20; +4 new KID-4 tests). Exact argv asserted: `git -C <root> worktree move .agi/worktrees/post-old .agi/worktrees/post-new`, `branch -m season2/posts/old season2/posts/new`, `push origin season2/posts/new`, `--delete-old` `push origin :season2/posts/old`, and resolved `tmux rename-window -t @5 new` / `rename-session -t $4 view-new`. Default-path zero-subprocess test passes; live-failure raises `failed (rc 128)`. `--live` flag confirmed in `rotate.py rename-post --help`. Related suites green: test_post_rename + test_rename_post + test_rotate + test_send = 615 passed; + test_rotate_verb = 40 passed.

**Semantics landed:** default = print-only; `--live` = executes; live landing is the Prime's to run.
What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
KID 4 closes the execution gap: rename-post --live injects real git/tmux executors (branch -m+push+push :old on --delete-old, worktree move, tmux rename by resolved @id); default stays print-only, subprocess.run zero times. 24/24 tests pass, 615 broader green.

PARENT REVIEW a00-b4841f18 (kid 4, execution gap): bytes read; three probes run. --live injects real git/tmux executors with the claim's exact argv (branch -m, push new, push :old ONLY under --delete-old, worktree move, tmux rename by the resolved @5/$4); the default path calls subprocess.run ZERO times; a non-zero git rc raises instead of reporting success. Scope: kid 4 proved the execution seam, not the whole target claim. REMAINING for the Prime (named, not built): _apply_staged is still not called from the live cmd_rotate_self successor-spawn seam (~16333), so a default stage is inert until the Prime wires it OR runs `rename-post --apply --live` directly. The live landing (the two real renames: sanctuary-director->point-director then sensei-director->sanctuary-director) is the Prime's merge-up act.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Kid 4 closes the last mechanism gap; the review keeps it scoped. WHAT THE INSTRUCTION SAID: 'apply = one function that renames every surface ... branch via git branch -m + a remote rename ... tmux by @id'. WHAT THE MACHINE DOES: with --live, cmd_rename_post injects _live_git/_live_tmux (rotate.py:3032/3050) and _apply_surfaces drives the exact argv, verified by a monkeypatched recorder; without --live, subprocess.run is never called. THE NEAR MISS: shipping injectable seams that no entry point ever injects -- the fixture proves the recorder, and the live verb could still never rename. NO DEVIATION: --live is opt-in and its live execution is the Prime's, so no kid-ordered round can accidentally run git.
<!-- THOUGHT:END -->
