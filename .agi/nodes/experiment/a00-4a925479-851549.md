---
id: experiment:a00-4a925479-851549
mint_id: 2b3190ce4a7a49b488e51ffeb1c0496f
type: experiment
parents:
  - hypothesis:heal-reaps-only-exited-bg-sessions-in-kid-worktrees
next_edges: []
confidence: 0.85
edited_by: a00-4a925479
evidence_runs:
  - experiment:a00-4a925479-851549
loop: hypothesis:heal-reaps-only-exited-bg-sessions-in-kid-worktrees@s2
model: stealth/space-bunny-alpha
production_lines: 81
profile: balanced
role: kid
scaffold_hash: 59b4db14a7cef26d
season: 2
title: "heal session-reap: one classification, dry-run default, fake-claude seam"
town: core
verdict: proved
---
# experiment:a00-4a925479-851549 — `heal.py session-reap` BUILT (one verb, one seam)

## What I built
`extensions/agi/bin/heal.py` gains a `session-reap` subcommand, registered in
`main()` next to `watch` / `sweep` / `pin-reap` (one persistent service; no new
`bin/*.py`; `test_bin_help_smoke` still green).

| piece | where | what |
|---|---|---|
| seam | `heal.py:_claude_agents(bin)` | THE ONE place `claude` is spawned: `claude agents --json --all`; `--claude-bin` / `$AGI_CLAUDE_BIN` override |
| worktrees dir | `heal.py:_reap_worktrees_dir(graph)` | cell `paths.core.worktrees_dir`, resolved against the MAIN checkout via `locations.shared_project_root` + `locations.repo_root` |
| one classification | `heal.py:_reap_classify(row, wt, repo_root)` | returns `(sid, reason|None)`; ONE result used for BOTH the print and the live loop |
| one argv | `heal.py:_reap_argv(bin, sid)` | `[bin, "rm", sid]` — bare, NEVER `--discard-unpushed` / `--force-remove-worktree` |

Reasons, by name: `not-interactive` (interactive AND remote-control),
`not-exited`, `repo-root` (the owner's own 710907bf row), `not-a-kid-worktree`
(outside the shared worktrees dir, or a name that fails `^a00-[0-9a-f]{8}$`).

**MODE = THE FLAG.** `--live` is the ONLY way `claude rm` runs; the default
(no flag) is a dry run that prints and returns 0. This verb deliberately does
NOT read `reaper.pin_reap` (the `heal.py:2614 _pin_reap_mode` trap): a reap of
app sessions is an operator verb, and the brief said the flag.

## Commands run
```
python3 -m pytest extensions/agi/tests/test_heal_session_reap.py -q            # 6 passed
python3 -m pytest extensions/agi/tests/test_heal_session_reap.py \
  extensions/agi/tests/test_bin_help_smoke.py extensions/agi/tests/test_heal.py \
  extensions/agi/tests/test_heal_watch.py extensions/agi/tests/test_heal_pin_reap.py \
  extensions/agi/tests/test_heal_sweep.py extensions/agi/tests/test_commands_manifest.py -q
                                                                        # 404 passed, 6 skipped
git diff --numstat -- extensions/agi/bin/heal.py                              # 80 0
```

## Evidence — the five-way fixture (fake `claude` on PATH, argv recorded)
```
reap-candidate kid-exited
skip kid-running: not-exited
skip 710907bf: repo-root
skip kid-interactive: not-interactive
skip kid-remote: not-interactive
dry-run: 1 candidate(s); pass --live to rm
```
Recorded argv, default (no flag): `[["agents","--json","--all"]]` — `rm` never
appears. Recorded argv, `--live`: `[["agents","--json","--all"], ["rm","kid-exited"]]`
— exactly one, and none of `710907bf` / `kid-running` / `kid-interactive` /
`kid-remote` occurs in ANY recorded argv.

A `a00x-nope` worktree (right shape, wrong grammar) is refused by name:
`skip odd: not-a-kid-worktree`, and `["rm","odd"]` is not in the record.

## The falsifiers, one by one
1. five-way fixture -> only the first is a candidate. NOT reproduced.
2. default invokes `claude rm` -> no; the test asserts the full argv list.
3. any test execs the real `claude` -> no: the ONLY binary on PATH in these
   tests is the fake script; `--claude-bin` is the other seam.
4. `--discard-unpushed` / `--force-remove-worktree` ever passed -> no; the argv
   is built in `_reap_argv` and a test reads the bytes of it.

## What the parent must do (I could not)
`.agi/config.json` is not mine to commit, so the cell the code READS FIRST is
**`paths.core.worktrees_dir`** (repo-relative, value `.agi/worktrees`). Until
it exists, `_reap_worktrees_dir` falls back to that literal. Adding the cell
deletes the only path literal this verb carries.

## Production lines
`git diff --numstat` over the production paths (heal.py + the commands
manifest row): **81** (heal.py 80, manifest 1) — at the 2x-ceiling boundary,
measured and recorded. A follow-up can move the four helpers to a small
`_session_reap.py` private module if the next change needs headroom.

## Agent Notes
heal.py session-reap built: one classification drives both print and rm, --live flag is the mode, rm argv built in _reap_argv bare; 6 new tests with a fake claude (recorded argv), 404 passed across heal+manifest suites; needs paths.core.worktrees_dir added by the parent
