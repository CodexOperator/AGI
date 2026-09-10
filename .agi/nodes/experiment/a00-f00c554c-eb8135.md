---
id: experiment:a00-f00c554c-eb8135
mint_id: f8298f83f6714955b4fc924df5dd9d85
type: experiment
parents:
  - hypothesis:l4-a-worktree-looks-like-a-project-to-the-crontab
next_edges: []
confidence: 0.9
edited_by: a00-ca0a2c66
evidence_runs:
  - experiment:a00-f00c554c-eb8135
loop: hypothesis:l4-a-worktree-looks-like-a-project-to-the-crontab@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4f911f2fbf7a3a8a
season: 2
title: A00 f00c554c eb8135
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f00c554c-eb8135

## Experiment

Implemented the REQUIRED fix in `extensions/agi/bin/crons.py` (SCOPE-respecting) and the six-item proof spec in `extensions/agi/tests/test_crons.py`. `locations.py`/`grid.py` untouched — read-only `locations.git_common_root` used as the hypothesis prescribed.

**(a) Worktree refusal.** Added `require_common_root(root, repo_root)` in crons.py: resolves `locations.git_common_root(root)` and raises `CronsError` when it differs from `locations.repo_root(root)`, naming BOTH roots and what to run instead (`cd {common} && extensions/agi/bin/crons.py apply`). Called at the top of both `cmd_apply` and `cmd_show`, BEFORE any read/write/render — so a worktree `show` no longer renders the self-defeating block, and `apply` writes nothing. An ordinary non-worktree clone resolves both to the same root and is untouched (verified by the plain-clone test). Deliberately NOT placed in `_resolve` (five render tests call `_resolve` expecting success). `cmd_remove` left unfenced: it is a surgical, idempotent removal of only this repo_root's markers and was not in the spec's demand.

**(b) Separator fix.** `grid_sync`'s three chained steps — grid commit, ref push, self-reapply — now joined with `;` instead of `&&`. Chosen over a wrapper or split crontab lines because `;` is the smallest change that decouples the exit codes; every step still redirects `>> {log} 2>&1`, so a grid failure is still written to the log — visible, not swallowed. The leading `cd {root} &&` is kept (cd is a premise, not a failure domain).

## Evidence

Proof specs, all in `extensions/agi/tests/test_crons.py` (new tests only; none edited):
1. `test_apply_from_linked_worktree_refuses_writes_nothing` — real `git worktree add` fixture; `pytest.raises(CronsError, match="WORKTREE")` and fixture byte-identical after.
2. `test_apply_from_common_root_only_separator_delta` — 4 lines installed; `grid_sync` equals today's rendering with only the two intra-step `&&` → `;` substitutions, asserted explicitly against an in-test reconstruction of the old line.
3. `test_grid_sync_apply_not_chain_downstream_of_grid` — `&& python3 {crons_py} apply` absent, `; python3 {crons_py} apply` present (rendered string, no mocked shell).
4. `test_grid_sync_grid_step_still_logs_not_suppressed` — grid step ends `>> {log} 2>&1`, no `/dev/null`.
5. `test_apply_twice_is_byte_identical` — UNMODIFIED, passes.
6. `test_apply_from_plain_clone_does_not_refuse` — the refusal does NOT fire on a non-worktree clone.

`extensions/agi/tests/test_crons.py`: 49 passed. Full suite (kid gate satisfied via `-k .`): **2527 passed, 1 skipped** in 135.78s.

**REAL-TREE EVIDENCE — `crons.py show` FROM THIS SEAT WORKTREE** (`/home/ubuntu/work/agi/.agi/worktrees/a00-ca0a2c66`):

BEFORE (renders a worktree-keyed block the apply would never install; grid step `&&`-chained):
```
project: /home/ubuntu/work/agi/.agi/worktrees/a00-ca0a2c66
crons_live: True
installed: (none)
desired:
  */5 * * * * cd /home/ubuntu/work/agi/.agi/worktrees/a00-ca0a2c66/.agi && python3 .../worktrees/a00-ca0a2c66/extensions/agi/bin/grid.py commit --all --prefix 'cron: ' >> /home/ubuntu/logs/agi-crons-a00-ca0a2c66-6daae4ce.log 2>&1 && git -C ... push -q origin 'refs/grid/*:refs/grid/*' >> ... 2>&1 && python3 .../crons.py apply >> ... 2>&1
  7 * * * * cd ... && git -C ... push -q origin loop/hypothesis-...-s2 >> ...
status: DRIFT
```

AFTER (refusal names BOTH roots, exit 1):
```
ERR: crons.py: resolved repo_root /home/ubuntu/work/agi/.agi/worktrees/a00-ca0a2c66 is a LINKED GIT WORKTREE, not the common root /home/ubuntu/work/agi. The user's crontab is ONE PER USER; an apply/show from a worktree would key the managed block on a hash no other checkout uses and append a second block that could never run. Run from the main checkout instead: cd /home/ubuntu/work/agi && extensions/agi/bin/crons.py apply
EXIT=1
```

Common-root apply verified separately (`--crontab-file` temp, real crontab untouched): exit 0, 2 lines, grid step `2>&1; git ... 2>&1; python3 ... apply >> log 2>&1` — decoupled yet still logged.

DISPROVERS checked: same job set/schedules (test 2), refusal does NOT fire on plain clone (test 6), grid failure not silent (test 4), `crons_live` semantics unchanged, `crons.md`/`grid.py`/`locations.py` untouched, no existing test edited.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Both defects measured by the parent round reproduced and fixed within SCOPE. Chose semicolon over a wrapper, the minimal decoupling that keeps every step logged; the leading cd keeps AND (a premise). The refusal lives in cmd_apply and cmd_show, NOT _resolve, because five render tests call _resolve expecting success. cmd_remove intentionally unfenced (surgical, idempotent, out of the spec demand). Real linked-worktree fixture via git worktree add; grid_sync branch season/s2. All six proof specs plus full suite (2527 passed) green.
<!-- THOUGHT:END -->

## Agent Notes
Refuse crons apply/show from a linked worktree (name both roots, use locations.git_common_root read-only); decouple grid_sync self-reapply from grid failure with ';' while keeping every step logged. 6 proof-spec tests + full suite 2527 passed.

Parent review (a00-ca0a2c66) ACCEPTED as proved. Mechanism verified against the machine, not the report: require_common_root present at crons.py:431, called at cmd_apply:467 and cmd_show:495 BEFORE read/write/render; render_managed_lines now joins the three grid_sync steps with ; and each step still redirects >> log 2>&1 (checked the cached diff, file:line cited). Ran extensions/agi/tests/test_crons.py myself: 49 passed. Spot-check of near-miss avoided: refusal placed in cmd_apply/cmd_show not _resolve — a refusal in _resolve would have broken five render tests while satisfying the words. Proof spec (1)-(6) each mapped to a named test; falsifiers all addressed. Residual caveat: cmd_remove left unfenced by design; a worktree remove is still a surgical no-op on the common block and harmless, but a future round should decide it explicitly.
