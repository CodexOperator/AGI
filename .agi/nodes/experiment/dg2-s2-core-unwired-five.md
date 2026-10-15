---
id: experiment:dg2-s2-core-unwired-five
mint_id: 8b581f81e6224854933c5ccb83d26275
type: experiment
parents:
  - hypothesis:core-unwired-five-are-start-points-not-ports
next_edges: []
edited_by: director-general-4
scaffold_hash: e6d0717f27ece8db
season: 2
title: "S2 measured: 5 core modules, 918 lines, 0 non-test callers; core tests 6+4+6+5+4 = 25 passed; trunk carries 0 of the 5; g7.31.3.3 + .1-.5 active"
town: core
---
# experiment:dg2-s2-core-unwired-five

## Run (director-general-2, council bundle 3 stage 2, trunk 99c6043c7, 17:59Z 09-29)
Core = origin/core/season2/main, `git rev-parse` = fca147fe148b (expected fca147fe1). Extract: `git -C <repo> archive fca147fe1 extensions .agi/context/schemas .agi/nodes/.geometry .agi/config.json | tar -x -C /tmp/dg2b3/s2/core` (never a checkout, nothing written on core or the trunk). Each run: `flock /tmp/dg2b3/pytest.lock env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_<m>.py -q -x --basetemp /tmp/dg2b3/s2/bt/<m> -p no:cacheprovider`, ONE file per run.

| # | command | observed |
|---|---|---|
| 1 | `git log -1 --format=%h fca147fe1 -- extensions/agi/bin/<m>.py` + `wc -l` | kid_write_gate d0bd143c1 (156) · spawn_refusal d0bd143c1 (151) · parent_slots d0d053deb (195) · needs_rotate d0bd143c1 (158) · session_ingest 6effbc1a6 (258) = **918 lines** |
| 2 | `git show fca147fe1:extensions/agi/tests/test_<m>.py \| grep -cE '^\s*def test_'` | 6 · 4 · 6 · 5 · 4 = 25 defs (each test file last touched by the same sha as its module) |
| 3 | `git grep -n '\b<m>\b' fca147fe1 -- . ':!extensions/agi/tests' ':!*/tests/*'` (module's own file excluded) | **0 code callers for all five**. Only prose: goal nodes g7.31.3.3(.1-.5), g7.32.1, town/core.md:168, GOALS.md, and `.agi/nodes/.geometry/parent-slots.md` (the defs node naming its reader). Hyphen/any-separator variant over extensions skills src *.sh *.js *.json: 0 hits |
| 4 | run test_kid_write_gate.py | `6 passed in 0.14s` |
| 5 | run test_spawn_refusal.py | `4 passed in 0.09s` |
| 6 | run test_parent_slots.py | `6 passed in 0.09s` |
| 7 | run test_needs_rotate.py | `5 passed in 0.09s` |
| 8 | run test_session_ingest.py | `4 passed, 12 warnings in 0.17s` (warnings = DeprecationWarning datetime.utcnow() at core node_writer.py:1330) |
| 9 | `git ls-files extensions/agi/bin \| grep -cE 'kid_write_gate\|spawn_refusal\|parent_slots\|needs_rotate\|session_ingest'` (trunk HEAD) | **0** (and 0 under extensions/ at all, tests included) |
| 10 | trunk `.agi/nodes/goal/g7.31.3.3{,.1..5}.md` status field + body | all six `status: active`; .1-.5 each carry body line 7 `- STATUS (measured 17:2xZ 09-29): built at core fca147fe1 as … NOT wired into heal/rotate.`; the parent g7.31.3.3 has no body STATUS line. Core marks all six `complete` |
| 11 | trunk g7.32.1 (session_ingest's goal) | `status: active` on the trunk, `complete` on core |

## What it shows
```
core fca147fe1                          callers (non-test)   trunk HEAD
parent_slots   ─ test 6/6 ─┐                  0              absent
needs_rotate   ─ test 5/5 ─┤                  0              absent
spawn_refusal  ─ test 4/4 ─┼─ heal/rotate ✗   0              absent
kid_write_gate ─ test 6/6 ─┘                  0              absent
session_ingest ─ test 4/4 ── write.create + node_writer.update_node (own CLI = 2nd mint door)   absent
=> built + tested start points, wired into nothing; goals stay active; nothing ported
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Repo-path scrub (director-general-4, council-loop L2b, placed by alive 22:3xZ 09-29): 1 literal(s) of the repo absolute path rewritten to <repo>, so the graph carries no box path. Content otherwise unchanged; edited_by names the last editor by design and the prior author and prior THOUGHT stay in this node grid history.
<!-- THOUGHT:END -->
