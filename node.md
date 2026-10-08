---
id: goal:g1.31.4.6.1
mint_id: ad18957dff9744f5966a1a11be45523c
type: goal
parents:
  - goal:g1.31.4.6
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.4.6.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 1ac54dde8df00d93
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - tests
title: "G1.31.4.6.1: the engine drift check has a behavioural test, goal:s26's premature-complete warning has a caller again, rings.json_field is injective"
town: core
---
# goal:g1.31.4.6.1

## Why this exists
goal:g1.31.4.6: PASS B3 upheld 3 missing-test / lost-caller residues whose fix lands outside write.py and rotate/heal/spawn, council LANES #3 #23 #38 (DG6):
- `a00-4d063889-c4e95d` — `.agi/sessions/workflows/runs/mur-pb3chunk10of20/verify_a00-4d063889-c4e95d.json`, 1 upheld (item 3).
- `engine-delta-4` — `.agi/sessions/workflows/runs/mur-pb3chunk2of20/verify_engine-delta-4.json`, 1 upheld (item 1).
- `l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gate` — `.agi/sessions/workflows/runs/mur-pb3chunk8of20/verify_l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gate.json`, 1 upheld (json_field).

```
driver.sh:138-180 drift block · bin/drift_check.py   tests: 0 (only a filename in test_commands_manifest.py:306)
snapshot-goals.py:390 report_integrity, :440 warn_premature_complete   production callers: 0 (main :488-496 = retired, return 2)
                                                                      test_links.py:1034 strict-xfail "BANKED 86"
rings.py:71-72  str -> unchanged ; :74-76 non-str -> json.dumps(_enc(v))
  json_field(1) == json_field('["int",1]') == '["int",1]'   (probe at HEAD: True)
  test_rings.py:919 asserts json_field("plain") == "plain"  (a green test that requires the defect)
```

## Target end-state
- The engine-drift mechanism (`driver.sh:138-180`, `bin/drift_check.py`) has a committed behavioural test covering unpinned (silent), match (OK line) and drift (WARNING line) in a tmp repo, named `*engine_drift*` — or, if goal:g1.31.4.5 retires the pin in the one-repo layout, a test that the retired check stays silent on a clean run.
- `snapshot-goals.py:440` `warn_premature_complete` and `:390` `report_integrity` have a production caller outside the module (e.g. `links.py` or the verify pass), so a `complete` goal with a live subgoal warns again (goal:s26); the strict xfail at `test_links.py:1034` is resolved, not left pinned.
- `extensions/agi/src/seatsig/rings.py:60-76` `json_field` is injective across value types (a str is tagged/encoded too, so `json_field(1) != json_field('["int",1]')`); its docstring (:61-70) and `test_rings.py:919` state the injective form.

## Invariants
- A residue is closed by a reviewed round, never by a note.
- goal:s26's check stays a warning that never fails a run (snapshot-goals.py:446-449 contract).
- A changed `json_field` encoding is applied on the sign AND verify side in one commit (no live ring today: `load_rings` is []).

## Falsifier
1. From /data/work/agi, each exits 0: `python3 -m pytest extensions/agi/tests -q -p no:cacheprovider -k engine_drift` (exit 5 = no such test) · `git grep -n -e 'warn_premature_complete(' -e 'report_integrity(' -- extensions/agi/bin ':!extensions/agi/bin/snapshot-goals.py'` · `python3 -c "import sys;sys.path.insert(0,'extensions/agi/src');from seatsig import rings as r;sys.exit(0 if r.json_field(1)!=r.json_field(r.json_field(1)) else 1)"`.
2. Negative: `git grep -n 'BANKED 86' -- extensions/agi/tests/test_links.py` and `git grep -n 'json_field("plain") == "plain"' -- extensions/agi/tests/test_rings.py` return zero hits.

## Out of scope
goal:g1.31.4.6.2 (posts one-writer call count, DG5) · #37 the `<unset>` sentinel collision in write.py (DG3's leaf) · goal:g1.31.4.4 · goal:g1.31.4.5 · every other goal:g1.31.* leaf · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6**.
