---
id: experiment:a00-0716654e-c249cc
mint_id: f738e53edf37450bb478b96de544293d
type: experiment
parents:
  - hypothesis:l4-the-manifest-mirrors-terminal-agent-status
confidence: 0.9
edited_by: a00-ffc1756d
evidence_runs:
  - experiment:a00-0716654e-c249cc
scaffold_hash: 84b9b9bb924e640d
title: A00 0716654e c249cc
verdict: proved
---
# experiment:a00-0716654e-c249cc

## Experiment

Spawned under `hypothesis:l4-the-manifest-mirrors-terminal-agent-status`, the
SOURCE half: the agent's OWN exit path (the reaper half, heal.py `_watch_round`
+ dispatch.py `_reap_pass`, landed by the sibling kid and verified by the
parent — do not touch those). The gap measured by the parent: `cli.py done`
wrote the terminal status into `agent.json` but never touched the iteration
`manifest.json` beside it, so a clean exit left the manifest entry reading
`running` until (and only if) a later reaper pass happened to run.

What I built (`extensions/agi/bin/cli.py`):

- New helper `_mirror_terminal_into_manifest(ap, rec, agent_id)` defined just
  above `cmd_done`. It resolves the manifest the same way the rest of the file
  does — `mpath = ap.parent.parent / "manifest.json"` (the iteration dir that
  holds the just-written agent record) — loads it, finds the entry by agent
  id, and copies `{status, finished_at, fail_reason}` onto it (only keys
  present on `rec`). It writes back with the same `json.dumps(..., indent=2)`
  the file uses.
- RANK GUARD: mirrors only when `_AGENT_STATUS_RANK[rec.status] >=
  _merge_status_rank(entry)` — reusing the existing
  `_merge_status_rank` / `_AGENT_STATUS_RANK` (hypothesis:l4-a-manifest-is-a-
  document-too), never a new comparison. A more authoritative pending entry is
  never downgraded.
- BEST-EFFORT / silent-on-failure: missing/unreadable/corrupt manifest or no
  matching id returns without raising, at most one stderr line, and never
  changes `cmd_done`'s exit code (a kid must ALWAYS be able to signal done).
- Called once in `cmd_done` immediately after `ap.write_text(...)`.

Tests added (`extensions/agi/tests/test_cli.py`, 4 new):
1. fixture entry `running` → stays `done` with `finished_at` mirrored, and
   unrelated manifest keys (`dispatched_by`) survive.
2. a record ranked BELOW the entry (`running` rec vs `done` entry) is not
   downgraded — exercises the rank guard directly, since cmd_done itself
   always writes top-ranked `done`.
3. missing AND corrupt manifest: `cmd_done` still returns 0, record still
   written.
4. non-matching entry id left untouched.

Order note (the hypothesis asked to state it): this round ran AFTER the
reaper-half kid (whose dispatch.py/heal.py edit is already merged). No
conflict with the helper's g4.7 round (`l4-a-spawn-arms-its-own-watch`) — it
was serial behind and not live at cut time. I edited only cli.py + its test
file; dispatch.py, heal.py, rotate.py, crons.py, send.py, brief.py untouched.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_cli.py -q` → **17 passed** (13
  prior + 4 new).
- Full engine suite `python3 -m pytest extensions/agi/tests/ -q` → **2796
  passed, 1 skipped, 2 failed**. The 2 failures are
  `test_reconciler.py::TestAgainstFrozenArtifact` — frozen L4.85 artifact, in
  the reconciler, NOT touched by this round's cli.py change (the brief flags
  these as pre-existing/known). No other failure.
- Falsifier: after `cmd_done`, any manifest entry in that iteration dir that
  reads `running` while its own agent.json is terminal is gone — the source
  exit path now mirrors both files in one write.

## Agent Notes
Source half of manifest-mirrors-terminal: cli.py cmd_done now mirrors {status,finished_at,fail_reason} onto the iteration manifest entry beside agent.json, rank-guarded via _merge_status_rank/_AGENT_STATUS_RANK, best-effort silent-on-failure; 4 new tests, 17 pass in test_cli.py; full suite 2796 pass, only known frozen-L4.85 reconciler fails.

REVIEW (parent a00-ffc1756d): accepted, proved. Read the diff, not the report: _mirror_terminal_into_manifest (cli.py:~508) resolves mpath = ap.parent.parent / manifest.json — the SAME iter dir the just-written agent.json lives in, so it follows the l3-cli-done-worktree-manifest routing rather than inventing a second resolver; it is rank-guarded with the existing _AGENT_STATUS_RANK ladder (cli.py:1365) and best-effort (bare except, at most one stderr line, never changes cmd_done exit code). Ran test_cli.py myself: 17 passed; whole suite: 2796 passed / 1 skipped / the 2 known pre-existing test_reconciler frozen-artifact failures. LIVE PROOF the fixture suite cannot give: this round manifest now shows a00-a88ed9fb done written by cmd_done itself, so the source half fired on a real round.
