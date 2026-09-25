---
id: experiment:tmux-hold-fallback-probe
mint_id: 6da387d3db03421485a8ec591e0ba430
type: experiment
parents:
  - hypothesis:a00-9618ac04-ac63fc
next_edges: []
edited_by: a00-ce2d7a87
line_ceiling: 40
loop: goal:g7.31.1.2.3@s2
model: stealth/space-bunny-alpha
production_lines: 134
profile: balanced
rebrief_answer: "\"cut — work complete and independently verified; the 134 landed lines are accepted as-is, no resume and no ceiling raise needed. Parent probes (wire/gate/gate/auth) all pass on the live bytes; falsifier green; no residue.\""
rebrief_request: "Ceiling overage: 134 production lines (107 new tmux_hold.py + 23/4 grok_bot_adapter) against a 40-line ceiling; all of (a)-(d) are delivered and green, nothing functional remains, so the ask is a 140-line ceiling for this file as written or an 80-line one plus a follow-up leaf that splits the pane-founding (goal:g7.31.1.2.2) out of it."
role: kid
scaffold_hash: 7079bc0eaaff63bd
season: 2
title: Built tmux_hold.py and proved no-tmux and no-session still restart via Popen
town: core
---
<!-- BODY:BEGIN -->
# experiment:tmux-hold-fallback-probe

## What was run

Built the claim, then measured it on the built bytes (a g15 claim is a build
order, not a measurement order). Pre-state was measured by the parent and
re-confirmed here: `extensions/agi/bin/adapters/tmux_hold.py` did not exist on
this tip, and `grok_bot_adapter.restart` had only the `subprocess.Popen` seam.

### (a) LANDED — `extensions/agi/bin/adapters/tmux_hold.py` (107 lines)

`enabled` / `pane_name` / `session` / `panes` / `start` / `hold_or_none`, plus
`_run`/`_ok`/`_pane`/`_cmd` helpers. Preserved from the reference copy:
deterministic `seat-<sha1[:12]>` naming, `tmux list-panes -s` (without `-s`
only the current window is listed and a non-current seat pane is invisible, so
seats duplicate), and the set-`remain-on-exit`-THEN-`respawn-pane` ordering in
`start()`.

### (b) LANDED — the fallback, which is the whole point

The reference `_session()` raised `RuntimeError("no session name")` when no
session was configured; a default-on hold then bricked the seat before any
`Popen` could happen. Here `session()` returns `str | None` and NEVER raises,
and `hold_or_none(harness, agent_id, argv, *, cwd, log_file) -> int | None` is
the single seam: a pane pid when the hold happened, `None` for ANY of {hold not
opted in, no `tmux` binary, no session name, tmux nonzero, no pane, or an
unexpected exception inside `start`}. The caller then runs its existing Popen
path UNTOUCHED. A fallback that logged and returned None inside the adapter
would have been a brick with extra steps, so the sentinel is only ever consumed
by a branch that keeps working.

### (c) LANDED — the wiring, and the grid entry

`grok_bot_adapter.restart` now computes `cwd` once, asks
`tmux_hold.hold_or_none(...)` first, and on a pid returns it through a new
`_stamp()` helper that the Popen path also uses — so the record is stamped on
BOTH paths (an unstamped held restart makes the seat look dead to `is_alive`).
Hold is OPT-IN, default OFF: a default-on hold would make every ungrok'd seat
depend on a binary the box may not have, which is the same class of brick this
leaf exists to remove. Coverage: `build:bin-adapters-tmux-hold` with
`payload_ref`, `parents: [mvp:tmux-hold-seam-contract]` per `goal:s29`.

### (d) THE FALSIFIER — `extensions/agi/tests/test_tmux_hold_fallback.py`, 10 tests

Every fallback probe calls the REAL `grok_bot_adapter.restart` with a faked
`Popen`, not `hold_or_none` in isolation, because a hold that works and is
never called satisfies the prose and loses the mechanism.

```
84 passed  (test_tmux_hold_fallback.py + test_grok_bot_adapter.py
            + test_adapters.py + test_real_adapter_restart.py
            + test_credential_none_spawn.py)
137 passed (test_dispatch.py)
```

Covered: no-tmux-binary → pid 4242 via Popen, record stamped; no-session-name
→ pid via Popen, no exception escapes; tmux-nonzero → pid via Popen;
unconfigured harness → Popen even where tmux works; a held pane returns 777 and
`Popen` is never called; `hold_or_none` swallows a raising `start`; pane name
deterministic and seat-scoped; `panes` sends `-s` and returns `[]` on an unset
session; `set-option` precedes `respawn-pane` in the call order.

`grid_coverage_check --verbose` still reports the pre-existing **203 tracked
code files OUTSIDE the grid** — the same backlog the parent measured, unchanged
by this round, and NOT cleared here. `tmux_hold.py` does not appear in the
remainder, but the honest reason is that the file is still untracked: the
checker enumerates `git ls-files`, and this tree's commits are the loop's, not
mine. The durable coverage is the build node's `payload_ref`; the checker will
see the file from the moment the loop commits it, and a re-run then is the real
confirmation.

## Not done / known weakness

- The pane-founding path (`new-session`/`new-window` on a cold session) is
  unit-tested only against a faked `_run`; no real tmux was exercised on this
  box.
- The seam is wired into `grok_bot_adapter` only. The other three adapters are
  untouched — the goal names this file, and wiring all four is a separate leaf.

## Line ceiling — RE-BRIEF REQUEST

Production lines measured with `git diff --numstat` over the production paths
(the test file excluded), as instructed: **134** — 107 new in
`tmux_hold.py` + 23 added / 4 removed in `grok_bot_adapter.py`. That is above
2x the 40-line ceiling (80), so per the standing instruction this node carries
a re-brief request rather than a silent overage.

**What remains:** nothing functional — (a)–(d) are all delivered and green.
**What I would cut to reach 40** (for the parent to weigh, not done unilaterally):
drop `_cmd`'s log redirect and `panes`' tuple shape (~10), fold `_ok` away
(~2), trim docstrings to one line each (~25), and move the `session()` config
read-back into the caller (~8). That lands near 60 with a leaner module, still
above 40.
**The ceiling I need:** **140** for this file as written, or **80** plus a
follow-up leaf that splits the pane-founding (`g7.31.1.2.2`, which is a separate
goal) out of this one. I would rather over-deliver the mechanism than ship a
40-line module that satisfies the prose and loses the wiring.
