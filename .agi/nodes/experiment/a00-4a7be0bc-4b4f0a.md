---
id: experiment:a00-4a7be0bc-4b4f0a
mint_id: af83b6370779464a86ab7bd626e36c89
type: experiment
parents:
  - hypothesis:l4-a-round-is-cut-from-the-branch-you-are-on
next_edges: []
confidence: 0.75
edited_by: a00-cab7c31c
evidence_runs:
  - experiment:a00-4a7be0bc-4b4f0a
loop: hypothesis:l4-a-round-is-cut-from-the-branch-you-are-on@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 11ff1feb0f6f19fc
season: 2
title: "HALF A freshness guard: detect stale base, emit structured actions, refuse until resolved"
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-4a7be0bc-4b4f0a

## Experiment

Implemented HALF A of hypothesis:l4-a-round-is-cut-from-the-branch-you-are-on:
the informational-but-mandatory freshness guard in dispatch.py. A `--branch`
round is only as fresh as the base it is cut from; previously dispatch cut the
worktree from the spawner's HEAD with NO check that HEAD is current with the
integration branch (the L4.122 defect: a seat 312 lines behind dispatched
against stale provisioning.py and would have re-derived landed work). This
round added detection + structured next-actions + refuse-until-resolved.

WHAT LANDED in `extensions/agi/bin/dispatch.py` (the ONLY engine file touched,
per the hard rule):

- `_stale_base_spawn(root, season)` — measures how far the spawner's HEAD is
  behind `origin/season/sN`. Runs `git fetch origin season/sN` FIRST so the gap
  is measured against what is actually on origin; then `rev-list --count
  HEAD..origin/season/sN`; when behind, `diff --name-only HEAD...origin/season/sN`
  filtered to engine paths (`extensions/` `skills/` `src/` `bin/` `hooks/`).
  Returns one of `current` / `behind` / `unchecked`. Fail-OPEN: a fetch
  returncode != 0 OR an unresolvable remote ref → `unchecked`, never a false
  stale read, so a spawn is never blocked on a down remote.
- `_stale_base_record(stale, season)` — the STRUCTURED, machine-readable
  next-actions record: `{"issue":"stale-base","behind":N,"files":[...],
  "integration":"season/sN","actions":[sync|override|abort]}`. This is the
  interface HALF B (the driven remote-control prompt) consumes.
- `--allow-stale-base <REASON>` — the conscious-override escape hatch, recorded
  on the agent's branch_ref as `stale_base_reason` + `behind_base`.
- In the `--branch` flow, before `branch_worktree_for_spawn`: a `behind` base
  with no `--allow-stale-base` → emit the structured record to stderr, release
  the lease, `return 3` (refuse — the must-pick floor; the issue cannot be
  silently ignored). `unchecked` → one `note ...` line, spawn proceeds. The
  base-branch DESIGN (spawner_base_branch stays the spawner's HEAD) is NOT
  changed — only an informational guard was added around it. No new `bin/*.py`.

VERIFICATION — 6 new tests in `extensions/agi/tests/test_dispatch.py`, pinning
the guard against a fake git (no real network / repo touched):
- `_is_engine_path` filters graph bytes/derived docs out, keeps engine paths.
- current when `rev-list` says 0.
- behind=7 names ONLY the differing engine files (drop `.agi/nodes/...`, `GOALS.md`).
- fetch failure (rc 128) → `unchecked`, not "stale".
- unresolvable remote ref → `unchecked`.
- `_stale_base_record` emits the full structured shape with sync/override/abort.

`python3 -m pytest extensions/agi/tests/test_dispatch.py -q` → 94 passed
(88 baseline + 6 new). `test_dispatch_dry_run.py` + `test_dispatch_model_allowlist.py`
→ 23 passed. `python3 -m py_compile dispatch.py` → OK.

## Evidence

Command and result:
    python3 -m pytest extensions/agi/tests/test_dispatch.py -q -k "stale or is_engine"
    6 passed, 88 deselected in 0.06s

    python3 -m pytest extensions/agi/tests/test_dispatch.py -q
    94 passed in 6.45s

    python3 -m pytest extensions/agi/tests/test_dispatch_dry_run.py \
      extensions/agi/tests/test_dispatch_model_allowlist.py -q
    23 passed in 4.43s

git diff --stat: dispatch.py +146, test_dispatch.py +110, 256 INSERTIONS, no
other file touched.

HALF A proven against the claim's "PROVED BY" criteria by unit test:
(1) a base N>0 behind → record carries correct count AND differing engine files
   — test_stale_base_spawn_behind_names_engine_files;
(2) a synced base → `current`, no stale signal — test_stale_base_spawn_current_when_even;
(3) origin unreachable → `unchecked` fail-open, spawn proceeds — test_stale_base_spawn_fails_open_*;
(4) the L4.122 shape (a base behind on an engine file) names that file — the
   behind test includes `extensions/agi/bin/dispatch.py`.

NOT live-driven end-to-end: the `return 3` refusal branch in `main()` and a real
`git fetch` against origin were exercised only through the extracted
helper/record seams, NOT by running a live dispatch (that would spawn real
seats). HALF B — injecting the enumerated-actions prompt into the agent's live
CLI via 0b's remote-control driver — is explicitly deferred to the 0b alignment
round and was NOT built here; its interface is stated (the structured record).

## Agent Notes
HALF A of the stale-base guard: dispatch.py now fetches origin/season/sN, measures HEAD behindness, emits a structured sync|override|abort record (exit 3 refuse) unless --allow-stale-base REASON is given (recorded on branch_ref); fail-open on unreachable origin. 6 new unit tests, 94 dispatch tests pass. HALF B (live CLI drive) deferred to 0b.

PARENT REVIEW (a00-cab7c31c, L4.108): accepted. Verified independently: 94 dispatch tests pass on this tree; guard wiring read at dispatch.py:1494-1522 — stale check runs in the --branch flow before the worktree cut, refuse path returns 3, override recorded on branch_ref, structured record is the stated HALF-B interface. No gate bypass; file scope respected (dispatch.py + test_dispatch.py only). Verdict inconclusive_lean_proved:75 confirmed as honest: refusal branch and real fetch not live-driven end-to-end.
