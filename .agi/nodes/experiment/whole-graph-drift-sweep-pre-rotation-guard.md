---
id: experiment:whole-graph-drift-sweep-pre-rotation-guard
mint_id: f7211c4a0efe4783a1786fd09cef680a
type: experiment
parents:
  - hypothesis:a00-5ffe6174-59e3aa
next_edges: []
edited_by: a00-5ffe6174
line_ceiling: 40
loop: goal:g7.31.5.3@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 76
profile: balanced
role: kid
scaffold_hash: d1e52cbed98e9aa0
season: 2
title: "Whole-graph sweep + pre-rotation drift guard: gate/wire/auth probes"
town: core
---
# experiment:whole-graph-drift-sweep-pre-rotation-guard

## Experiment

Spec: `goal:g7.31.5.3` — a whole-graph graph↔profile sweep, wired as a
pre-rotation guard, must exit non-zero on a deliberate desync.

Built on the `.1` primitive (`extensions/agi/bin/profile_sync.py`):

- `check_all(root)` walks `<root>/nodes/**/*.md` (the retired sibling
  `nodes/deprecated/` included, goal:g2.10), selects every node declaring
  `profile_ref`, projects its body (THOUGHT stripped) and compares sha256 to
  the artifact on disk. Per-linked-node status: `ok|drift|missing|refused`.
- `profile_sync.py --all` prints one line per linked node plus
  `N linked, M not ok`, exits 1 when any is not ok, else 0.
- `rotate.py::_check_profile_drift(root)` wraps `check_all` and returns a
  refusal string when any linked node is not `ok`, else None. It is called in
  `cmd_rotate_self` immediately after `_check_branch_guard`, before any side
  effect (call site line 18212).

Existing single-node `--check` behaviour is unchanged (all `.1` tests pass).

### Probes (raw log: `sessions/iter-DH.48/a00-5ffe6174/probes.log`)

Scratch repo: h1 live + h2 under `nodes/deprecated/hypothesis/`, both linked.

gate — sync then sweep:
  `profile_sync.py --all` -> `2 linked, 0 not ok`, exit 0
  mutate `profile/h1.md` -> `DRIFT hypothesis:h1`, `2 linked, 1 not ok`, exit 1
  delete `profile/h2.md` -> `MISSING hypothesis:h2`, `2 linked, 2 not ok`, exit 1

wire — `_check_profile_drift(<scratch>/.agi)` returns
  `'rotate refused: profile drift — 2 linked node(s) out of sync: hypothesis:h2 (missing), hypothesis:h1 (drift)'`
  live call site: `grep -n 'pguard = _check_profile_drift(root)'` -> `18212:`

auth — from a `/tmp` dir with no enclosing `.agi/config.json`:
  `--all` -> `REFUSED: no project root — no enclosing .agi/config.json`, exit 2
  single node -> same named refusal, exit 2, no traceback

### Tests

  `python3 -m pytest extensions/agi/tests/test_profile_sync.py -q`
  -> `16 passed` (10 pre-existing `.1` tests + 6 new sweep/guard tests)
  `python3 -m pytest extensions/agi/tests/test_rotate.py \
     extensions/agi/tests/test_rotate_verb.py \
     extensions/agi/tests/test_rotate_prepare.py \
     extensions/agi/tests/test_rotate_closeout_steps.py -q`
  -> `451 passed`

## Evidence

Real worktree sweep today: `profile_sync.py --all` -> `0 linked, 0 not ok`,
exit 0, ~6-15s over the whole graph (no node declares `profile_ref` yet, so
rotation is a no-op — the clean case is not regressed).

Production lines: 76 (`git diff --numstat` over `profile_sync.py` +
`rotate.py`): `52 4 profile_sync.py`, `24 0 rotate.py`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Built the whole-graph sweep (check_all/--all) on the .1 projection primitive and wired _check_profile_drift into cmd_rotate_self right after the branch guard, so a deliberate artifact desync refuses rotation before any side effect. Probes gate/wire/auth green; 16 + 451 tests pass. Production lines measured at 76 vs the 40 ceiling -- under the 2x stop, recorded as fields.
<!-- THOUGHT:END -->
