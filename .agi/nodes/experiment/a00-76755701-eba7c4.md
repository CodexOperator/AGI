---
id: experiment:a00-76755701-eba7c4
mint_id: f08fe836a8d045a4b23b272b16652009
type: experiment
parents:
  - hypothesis:l4-an-untrusted-lane-earns-tier-by-signed-verdicts
next_edges: []
confidence: 0.8
evidence_runs:
  - experiment:a00-76755701-eba7c4
loop: hypothesis:l4-an-untrusted-lane-earns-tier-by-signed-verdicts@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 9681b091fdbe2a4c
season: 2
title: A00 76755701 eba7c4
town: all
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-76755701-eba7c4

## Experiment — SLICE 3 of 3: the untrusted lane itself (conjunct 2)

Parent's cut (hypothesis:l4-an-untrusted-lane-earns-tier-by-signed-verdicts):
slices 1+2 landed (onboard + sponsor co-signature as an argv value, verified
by rings.verify_ring). This kid builds conjunct (2): dispatch refuses an
untrusted spawner, the merge-up recipe refuses its branch, and its per-spawn
key cap is the row's `budget` cell — every refusal names the tier. FILE SCOPE
honoured: dispatch.py, season.py, provisioning.py, and NEW test file
test_untrusted_lane.py ONLY. send.py/rings.py/veto.py/rotate.py/
verification.py/cli.py/write.py/brief.py untouched.

### (a) dispatch.py — refuse an untrusted spawner
New helper `_refuse_untrusted_spawner(root, seat)` (beside `_resolved_seat`):
resolves the acting post = the resolved seat (--seat > AGI_SEAT, the same
precedence L4 already exposes), reads geometry_config.load_rows, and when the
post's row `tier == 'untrusted'` returns a refusal naming the tier. Called in
main() right after the push-further gate, BEFORE `iter_dir.mkdir`, the
manifest, the runtime-key pre-flight, any spawn-budget lease, session dir or
credential. Exit 2. Fail-open on absent/unknown seat or unreadable config —
a gate that refuses everyone proves nothing.

### (b) season.py merge-kids — refuse an untrusted branch
New helper `_refuse_untrusted_merge(root, branch)`: a branch equalling an
untrusted row's `name` or its `worktree` cell is refused by name, tier named,
and NOT merged. Called at the top of the cmd_merge_kids branch loop, before
`rev-list` / `merge` / suite / commit — so the branch is never touched. The
ownership/base resolution above it is untouched.

### (c) provisioning.py — per-key cap = the row's budget cell
New helper `post_limit_usd(post, cfg, root)`: returns the untrusted row's
`budget` cell as the mint limit, else None (absent/trusted post, or an
untrusted row with NO budget cell → today's default exactly). READING TAKEN:
`budget` IS the mint `limit_usd` (one cell, the owner's 'per-key budget';
stated per the slice-cut). Wired into dispatch: when the acting post resolves
untrusted, `cred_limit` is overridden by the row cell.

### Worktree-only conjunct — honest reading
The untrusted row's `worktree` cell exists and is what the refusals key on,
but NO mechanism in dispatch/season/provisioning confines an untrusted
process's writes to that worktree. That confinement (where it exists at all)
lives in the spawn env (`AGI_TREE_PROJECT_ROOT`), not in these three files.
Stated plainly; no writer-gate invented.

## Evidence

- `python3 -m pytest tests/test_untrusted_lane.py tests/test_onboard.py -q` → 25 passed.
- Unchanged-behaviour suites over the touched files, all green:
  test_season.py + test_untrusted_lane.py 68 passed;
  test_dispatch.py + test_dispatch_model_allowlist.py + test_provisioning.py
  + test_geometry_config.py + test_season_merge_kids.py 213 passed / 5 skipped;
  test_dispatch_dry_run.py + test_dispatch_alarms.py + test_verification_kept_merge.py
  + test_rings.py 71 passed.
- test_untrusted_lane.py has the NEGATIVE CONTROLS the slice demanded:
  trusted seat/branch admitted, trusted post keeps default, unknown/absent
  seat fails open, untrusted-without-budget keeps default.

## Agent Notes
<!-- THOUGHT:BEGIN -->
Slice 3 landed fixture-proved, NOT live-exercised: the gates run against a
tmp geometry config, never a live dispatch/merge. That is exactly the
fixture-proved-but-not-live_exercised state the cut told a kid to report as
lean_proved and say which conjunct. All three conjuncts (a)/(b)/(c) are built
and fixture-green. The residual honesty: (c) is inert in practice because
(a) refuses an untrusted SPAWNER before any mint, so an untrusted post never
reaches its own budget cap through dispatch — the cap exists and is
testable, but the untrusted post is also refused as a spawner, which is the
lane's real point. Also (b) matches branch-to-row by name/worktree ("lurker",
"worktrees/lurker"); the real untrusted round-branch spelling is a
loop/<slug> name, so if the project adopts a different branch spelling this
match may need tightening. No worktree-only write mechanism found or invented
— it is a convention here.
<!-- THOUGHT:END -->

## Agent Notes
SLICE3: untrusted lane built+green in dispatch(seat gate)/season(merge gate)/provisioning(budget cap); 25 new tests w/ negative controls; fixture-proved not live-exercised
