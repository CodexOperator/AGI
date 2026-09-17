---
id: experiment:a00-d001afe7-233268
mint_id: f0c3366056184c2c95ff3c248c005168
type: experiment
parents:
  - hypothesis:l4-the-deliverable-check-diffs-against-the-round-base-in-the-kid-worktree-and-runs-in-the-live-harvest
next_edges: []
confidence: 0.9
edited_by: a00-d99d270a
evidence_runs:
  - experiment:a00-d001afe7-233268
line_ceiling: 160
loop: hypothesis:l4-the-deliverable-check-diffs-against-the-round-base-in-the-kid-worktree-and-runs-in-the-live-harvest@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "probe_conj1_base.py", "expected": "recorded base_branch honored; season_thing.py absent, not master-swept", "observed": "base=season2/main; season_thing.py missing; carried only carried.py+loop work", "result": "refused"}
  - {"conjunct": 2, "class": "gate", "cmd": "probe_conj2_tree.py", "expected": "MAIN foreign dirt not carried; kid-worktree untracked carried", "observed": "main_only.py excluded, kid_only.py included", "result": "refused"}
  - {"conjunct": 3, "class": "wire", "cmd": "probe_conj34_wire.py", "expected": "node deliverables frontmatter trips check with no --deliverables flag", "observed": "cmd_done demoted rc0, missing=[gone.py, season_thing.py]", "result": "refused"}
  - {"conjunct": 4, "class": "gate", "cmd": "probe_conj34_wire.py", "expected": "demoted_from keeps evidence-gate ORIGINAL under both-demote", "observed": "demoted_from=proved", "result": "refused"}
production_lines: 115
profile: balanced
rebrief_answer: proceed
rebrief_request: all five conjuncts implemented and the test_cli suite green at ~115 production lines; the 40-line default ceiling is below the real scope of this fix (base + tree + live wiring + demoted_from + season fixture); authorize a 120-line ceiling for this node id
role: kid
scaffold_hash: 8cd64a8750351c76
season: 2
title: deliverable check diffs the round own fork base in the kid worktree and reads node-declared deliverables so it runs in the live harvest
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d001afe7-233268

## Experiment

hypothesis:l4-the-deliverable-check-diffs-against-the-round-base-in-the-kid-
worktree-and-runs-in-the-live-harvest -- a g15 build order, implemented in
`extensions/agi/bin/cli.py` and proven in `extensions/agi/tests/test_cli.py`.

CONJUNCT 1 (BASE): rewritten `_branch_change_paths` no longer probes
`origin/master|origin/main|master|main`. New `_round_base` resolves the fork
base from the round's OWN session records first (`base_branch` in
`iter-*/<id>/agent.json`, the `iter-*/agent.json` flat spelling, then the
manifest) and falls back to the season main (`origin/season2/main`) derived
from the loop branch via `branches.parse`/`season_main`. Master is gone
entirely. Non-origin recorded bases (e.g. `season2/main`) resolve unchanged;
an unresolvable base falls back to `ls-tree` (full tip tree), never master.

CONJUNCT 2 (TREE): the uncommitted `git diff --name-only`) and untracked
(`git ls-files --others --exclude-standard`) reads now run with `-C
wt` where `wt = root.parent` (the KID WORKTREE top), not the MAIN checkout
`git_common_root`. The committed-vs-base diff still reads from anywhere
shared object store resolves. Measured: the MAIN checkout's foreign dirt
(~57 paths) no longer counts as the round's carried work.

CONJUNCT 3 (LIVE): `cmd_done` now reads a `deliverables:` list from the
kid's own node frontmatter (new `_node_declared_deliverables`) and merges it
with the explicit `--deliverables` flag (union, declared order preserved).
Either source alone trips the same demotion, so the check is ON in the live
harvest without a human passing the flag.

CONJUNCT 4 (demoted_from): the deliverable branch sets `rec["demoted_from"]`
only when the evidence gate did not already set it, so a BOTH-demote keeps
the gate's ORIGINAL verdict instead of overwriting it with the gate's lean.

CONJUNCT 5 (fixture): new season-shaped test
`test_done_deliverable_diffs_against_round_base_in_season_repo`: master is a
real branch and its own fork point; the loop branch forks from
`season2/main` (recorded `base_branch`); one declared path (`season_thing.py`)
lives in the season main so a master-diff carries it (thus a pre-fix
master-resolve would NOT demote it) while the true-base diff correctly
names it missing; `carried.py` stays carried. Asserts
`missing_deliverables == ["gone.py", "season_thing.py"]`, carried not
missing, and (both-demote, `evidence_runs=[]`) `demoted_from == "proved"`
preserved from the gate. The two SM.67 manifest-holder lines added to the
pre-existing deliverable test reflect production (dispatch always writes the
round's iter `manifest.json`; without it `_alarm_dispatcher_on_done` returns
1 and the clean round's `==0` assertion was red at HEAD).

## Evidence

- `python3 -m pytest extensions/agi/tests/test_cli.py -q` -> 51 passed.
- Pre-fix reproduction: debug run on the season fixture showed the master
  probe (`git rev-parse --verify master`) resolves and carries `base.py`,
  `season_thing.py`, `carried.py`; true base `season2/main` carries only
  `carried.py`. The season fixture's `missing_deliverables` assertion fails
  on the master-based resolve and passes on the round-own base.
- Root layout bug found and fixed in session scan: the live
  `iter-*/<id>/agent.json` layout, not the flat `iter-*/agent.json` heal
  spelling -- `_round_base` now scans both.
- Production lines over the 40-line default ceiling (~115 added): recorded
  in `production_lines`/`line_ceiling`/`rebrief_request` so the overage is
  named (the 5-conjunct scope genuinely needs the headroom; work is complete
  and the suite green).

## Agent Notes
Built all five conjuncts: _branch_change_paths diffs against the round OWN fork base (recorded base_branch, else season main; master probe gone) and reads uncommitted+untracked in the kid worktree top, not the MAIN checkout; cmd_done merges the node-declared deliverables list so the check runs in the live harvest; both-demote keeps the evidence-gate original verdict. Season-shaped fixture test fails on master-resolve and passes on round-own base. test_cli.py 51 passed. Production lines ~115 (over the 40 default) recorded in the node with a rebrief_request.

parent review: rebrief answered proceed; ceiling authorized 160 (default 40 was below real scope, production=115 licit); kid done, no resume pending

PARENT REVIEW (a00-d99d270a): ACCEPTED. Probes per claim conjunct, all PASS: c1 BASE probe_conj1_base.py (real linked worktree, recorded base_branch honored over master AND over branch-name origin/fallback; season_thing.py demoted, master-resolve would carry it); c2 TREE probe_conj2_tree.py (MAIN foreign dirt excluded from carried, kid-worktree untracked included -- the plain-repo fixture the kid wrote never exercises this, my worktree probe closes it); c3 LIVE probe_conj34_wire.py (committed cli.cmd_done, node frontmatter deliverables with NO --deliverables flag -> demotion fired); c4 demoted_from probe_conj34_wire.py (both-demote keeps gate ORIGINAL proved); c5 kid season-shaped fixture test_done_deliverable_diffs_against_round_base_in_season_repo green. test_cli deliverable subset 2 passed. No conjunct refuted -> child not demoted.
