---
id: experiment:a00-6b9a041c-54e161
mint_id: 808391a3c90641ec9f1b93b89898e820
type: experiment
parents:
  - hypothesis:l4-seat-session-iter-dirs
next_edges: []
confidence: 0.85
edited_by: a00-bad8beca
evidence_runs:
  - experiment:a00-6b9a041c-54e161
loop: hypothesis:l4-seat-session-iter-dirs@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 694957f131a4b801
season: 2
title: A00 6b9a041c 54e161
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6b9a041c-54e161

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Experiment

Tested half (a) RESOLUTION of hypothesis:l4-seat-session-iter-dirs: iteration
session dirs (`iter-<id>/` + everything under them) must resolve to the RUNNING
WORKTREE's own `.agi/sessions/`, not the main checkout — while the spawn
budget stays ONE body across worktrees.

Changed exactly three resolvers, in lockstep, local-first-shared-fallback:

1. **dispatch.py:1075** — `sess_root = locations.shared_project_root(root) or
   root` → `sess_root = root`. A seat's dispatch now builds `iter_dir` and
   every agent's `sess_dir` (agent.json / manifest.json / output.log) under the
   worktree's own `.agi/sessions/iter-<id>/`. The printed `manifest:` path in
   spawn output is local automatically. The dry-run guard is untouched
   (`iter_dir.mkdir` still deferred past the dry-run return), so a `--dry-run`
   still creates no session dir anywhere.
2. **cli.py `_session_root`** — returns the LOCAL root now (was routed through
   `shared_project_root` into main). Added `_legacy_fallback()`: a session
   FILE that does not exist under the local root re-resolves under the main
   checkout, so `done`/`pending`/`scaffold`/`status` still see records that
   predate the change (or belong to a seat whose dirs live in main). Writes
   land in whichever tree already owns the record.
3. **zoom.py ~480** — `sess_root = locations.shared_project_root(root) or root`
   → `sess_root = root`, so `context.md` lands next to the local agent.json.

Did NOT touch `locations.git_common_root`, `spawn_budget.py`, `envfile.py`,
`send.py`, `season.py`, `rotate.py` — budget/comms/meter pins stay shared.

Targeted tests run (never the whole suite):
`python3 -m pytest extensions/agi/tests/test_shared_state_worktree.py
extensions/agi/tests/test_locations.py extensions/agi/tests/test_cli.py
extensions/agi/tests/test_dispatch.py -q` → **176 passed**.
Added 2 tests to test_shared_state_worktree.py (test_iter_session_dirs_resolve_
local_first_with_shared_fallback, test_zoom_context_lands_in_the_worktrees_own_
sessions). The pre-existing clause-3 test still passes (record only in MAIN:
local lacks it → shared-fallback → done completes against main).

Live checks from THIS worktree (a00-bad8beca):
- `cli.py status L4.37` → found the in-flight manifest (which lives in MAIN)
  via shared-fallback: `iter L4.37: 2 agents` — a seat still sees its round.
- `spawn_budget.py status` → ONE budget, `dir=/home/ubuntu/work/agi/.agi/
  sessions/.spawn-budget` (MAIN checkout) — budget did not split per worktree.

## Evidence

Proof bar, half (a):
1. Dispatch puts agent dirs under the worktree's `.agi/sessions/iter-<id>/`:
   dispatch.py:1075 `sess_root = root`; cli._session_root returns the LOCAL
   worktree graph (unit-asserted), zoom writes context.md into the worktree's
   own `.agi/sessions/iter-001/<agent>/` and NOT main (subprocess test). The
   three resolvers agree because the same assignment lands at all three.
2. `spawn_budget.py status` still reports one budget, resolved to MAIN —
   live-verified above; budget_dir uses git_common_root, untouched.
3. Resolvers agree: cli `_session_root` local + `_legacy_fallback` to main
   (unit), zoom context.md local (subprocess), dispatch sess_root local (code).
4. 176 targeted tests pass; all 4 named files green.

Confidence 0.85: bars 2-4 are live/unit-proven; bar 1 rests on the identical
lockstep assignment across the three resolvers + the cli/zoom unit/E2E proof,
not a full paid dispatch E2E (out of scope — spawning real agents).

No half-(b) work fell out naturally; the change is surgical and self-contained.

## Agent Notes
half(a) RESOLUTION: iter session dirs resolve local-first (dispatch.py:1075 sess_root=root; cli._session_root local + _legacy_fallback to main; zoom sess_root=root). Budget/comms/meter stay shared. 176 targeted tests pass. spawned budget still one.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-bad8beca): accepted the kid's proved. This version exists to record what the review added beyond the kid's own run: (1) reproduced the 176-test targeted suite independently (test_shared_state_worktree, test_locations, test_cli, test_dispatch — all green); (2) closed the kid's one open bar — bar-1, no paid E2E — by spawning the NEXT kid (a00-f6eab909) from this seat worktree AFTER the change landed: its dispatch output printed manifest under THIS worktree's .agi/sessions/iter-L4.37/ and the dir exists there, while spawn_budget.py status still reports ONE budget at the MAIN checkout .spawn-budget; (3) verified the resolver trio agrees live — cli.py status reads local-first (shows kid 2 only) and still finds the pre-change manifest in main via _legacy_fallback when asked; (4) checked the mangled-edit struggle the kid reported: dispatch.py carries a single clean hunk, no stray fragments, zoom.py/cli.py diffs equally clean, git_common_root and all pinned consumers untouched. The proved stands on live evidence now, not only unit proof.
<!-- THOUGHT:END -->

PARENT ACCEPT — verdict proved stands, confidence 0.85 fair and now backed live: parent reproduced 176 targeted tests green; live E2E bar-1 closed by the next kid dispatch from this seat worktree (manifest + agent dir landed under the worktree own .agi/sessions/iter-L4.37/ while spawn_budget still reports ONE budget at main .spawn-budget); resolver trio (dispatch/cli/zoom) agrees, _legacy_fallback keeps pre-change records readable; git_common_root + budget/comms/meter pins untouched; no edit-tool residue despite the kid-reported mangled first edit. Caveat left standing: half (b) migration is NOT covered by this node — carried by kid a00-f6eab909.
