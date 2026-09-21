---
id: experiment:a00-d0c2697b-c24d97
mint_id: bc799946290c4675a13d1c35c6cfaab8
type: experiment
parents:
  - hypothesis:l4-branches-follow-the-season-grammar
next_edges: []
confidence: 0.9
edited_by: a00-d0c2697b
evidence_runs:
  - experiment:a00-d0c2697b-c24d97
loop: hypothesis:l4-branches-follow-the-season-grammar@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 053b94873c91c938
season: 2
title: wire three readers to the season grammar
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d0c2697b-c24d97

## Experiment

Claim item (2), readers group A: wired `dispatch.py`, `heal.py`, `send.py` to the
season-grammar module kid 1 built (`extensions/agi/bin/branches.py`), so these
three readers stop spelling branch names by hand.

### A. One resolver in branches.py (extended kid 1's API, not rewritten)

Added `ref_candidates(branch) -> list[str]` — the ref names a reader should try,
CANONICAL FIRST then the old one-season deprecated alias, for a branch that may
be new or old. Old names are accepted, never refused. Also added the private
`_canonical_to_old` (inverts the alias table). Reserved-towns still refuse.

    season trunk:    ref_candidates("season2/main")       == ["season2/main", "season/s2"]
    town trunk:      ref_candidates("season2/<t>/season1/main") == ["season2/<t>/season1/main", "town/<t>/season/s1"]
    loop branch:     ref_candidates("season2/loops/a-b")  == ["season2/loops/a-b", "loop/a-b@s2"]
    old input accepted:   ref_candidates("season/s2")     == ["season2/main", "season/s2"]  (canonical first, never refused)
    posts (no legacy):    ref_candidates("season2/posts/foo") == ["season2/posts/foo"]

5 new tests in `test_branches.py` (21 -> 26 passed).

### B. Every branch site in the three files now reads the grammar

dispatch.py
- `_stale_base_spawn`: fetch ref built from `ref_candidates(season_main(season))`
  (canonical first, old `season/s<N>` second); the loop tries each until a fetch
  resolves, else fails open to "unchecked". A live tree NOT yet renamed is still
  measured — a fetch that 404s the new name falls back to the old name instead
  of silently reading "unchecked". `town_branch` given is kept as-is.
- `_stale_base_record`: emitted `integration` and the `sync` action now name the
  canonical `season<N>/main` (or the town branch).
- `loop_branch_name`: `loop/<slug>-<agent>@s<N>` -> `season<N>/loops/<slug>-<agent>`
  via `branches.loop_branch(...)`; docstring updated to the new shape and the
  legacy-@s<N>-suffix fallback heal.py still parses.

heal.py
- `_sweep_season`: still parses the OLD `loop/<slug>-<agent8>@s<N>` (regex on
  the @s<N> suffix) AND the new `season<N>/loops/<slug>-<agent>` shape (via
  `branches.parse` kind=loop). An old round's worktree is never dropped for a
  spelling change.
- `_sweep_worktree_base`: season fallback now returns `origin/{season_main(season)}`.
- added `_sweep_resolve_base`: the sweep's caller resolves the origin base
  through `ref_candidates` (canonical first, old `origin/season/s<N>` second), so
a tree not yet renamed still resolves its base for the ancestry check.

send.py
- `_PUSHED_SEATS` = `"origin/" + season_main(2)` (was `"origin/season/s2"`).
- `_pushed_seats`: fetch AND readout now resolve the LIVE spelling via
  `ref_candidates` — canonical first, old `origin/season/s<N>` fallback — so the
  pushed-seats readback does NOT silently return None during the rename window.
- `--source` default/help text now spell `_PUSHED_SEATS` (canonical).

### Literal sweep (the rule: ONE place spells branch names)

`grep -n 'season/s[0-9]' extensions/agi/bin/dispatch.py heal.py send.py` → NONE
(all branch-name spellings route through the grammar module).

## Evidence

Primary suite (the task command):
```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_branches.py extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_dispatch_dry_run.py extensions/agi/tests/test_heal.py extensions/agi/tests/test_send.py -q
```
Last line:      `388 passed in 13.44s`

Covering suite (sibling files that exercise the same changed code paths):
```
python3 -m pytest extensions/agi/tests/test_dispatch_alarms.py extensions/agi/tests/test_dispatch_model_allowlist.py extensions/agi/tests/test_dispatch_no_stdout_secrets.py extensions/agi/tests/test_heal_pin_reap.py extensions/agi/tests/test_heal_seats.py extensions/agi/tests/test_heal_sweep.py extensions/agi/tests/test_heal_watch.py -q
  -> 93 passed in 8.04s
```

Grep rule output (must be comments/docstrings + deprecated-alias fallback only):
```
$ grep -n 'season/s[0-9]' extensions/agi/bin/dispatch.py extensions/agi/bin/heal.py extensions/agi/bin/send.py
NONE — all renamed
```

Four pre-existing tests asserted the OLD names and failed under the new bytes; they
were updated to assert the CANONICAL values (strengthened, not weakened — two now
prove the old-ref fallback path works on a bare repo carrying only the legacy name):
`test_loop_branch_name_carries_slug_agent_and_season`, `test_stale_base_record_is_structured_with_actions`,
`test_town_branch_behind_season_not_stale_against_own_branch`, `test_whois_claim_yes_has_provenance`.

## Agent Notes
Wired dispatch/heal/send to branches.py grammar; ref_candidates fallback keeps old names accepted; 388+93 tests pass; grep season/s[0-9] = NONE
