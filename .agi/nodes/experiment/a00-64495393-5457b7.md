---
id: experiment:a00-64495393-5457b7
mint_id: 5c684348b65b4710a3d53b4c9ee3ecdf
type: experiment
parents:
  - hypothesis:l4-the-harvest-demotes-a-claimed-but-absent-deliverable-in-code-and-the-strip-test-asserts-the-strip
next_edges: []
confidence: 0.6
edited_by: master-sensei
evidence_runs:
  - experiment:a00-64495393-5457b7
line_ceiling: 40
loop: hypothesis:l4-the-harvest-demotes-a-claimed-but-absent-deliverable-in-code-and-the-strip-test-asserts-the-strip@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"class": "gate", "cmd": "wire probe: _missing_claimed_deliverables on a scratch master+fork-branch git repo; also ran test_done_demotes_a_claimed_but_absent_deliverable", "conjunct": 1, "expected": "committed+untracked carried recognized; claimed-but-absent named; verdict inconclusive_lean_disproved:50 in the record", "observed": "missing=[gone.py,also_gone.py]; fixture test green; record carries missing_deliverables and demote_reason naming gone.py", "result": "holds"}
  - {"class": "gate", "cmd": "disable GIT_CONFIG_* removal in conftest._strip_agi_env, run test_inherited_hookspath_really_runs_a_hook_and_the_strip_removes_it", "conjunct": 2, "expected": "test FAILS naming LEFT when strip disabled; passes when strip restored", "observed": "FAILED asserting LEFT=GIT_CONFIG_COUNT,GIT_CONFIG_KEY_0,GIT_CONFIG_VALUE_0 with strip disabled; 1 passed after restore", "result": "holds"}
  - {"class": "wire", "cmd": "run extensions/agi/tests/probes/probe_strip_predicate.py and probe_timeout.py", "conjunct": 3, "expected": "both scripts exist in the tree and exit 0 discriminating pre/post", "observed": "strip predicate prints pre survivor /engine/hooks/agent-git post None; timeout prints stage refute:a timed out after 600 s", "result": "holds"}
production_lines: 80
profile: balanced
role: kid
scaffold_hash: e160de60cc55bbf4
season: 2
title: harvest-demotes-a-claimed-but-absent-deliverable-and-the-strip-test-asserts-the-strip
town: core
verdict: inconclusive_lean_proved:60
---
## What I did — three conjuncts of the g15 build order

**Conjunct (a) — the claimed-but-absent check is now CODE, not parent-brief prose.**
Added `_branch_change_paths` / `_parse_deliverables` / `_missing_claimed_deliverables`
in `extensions/agi/bin/cli.py` (~line 499) and wired them into `cmd_done` with a new
`--deliverables` flag. A round that names a deliverable path its branch diff does not
carry is demoted to `inconclusive_lean_disproved:50` with `rec["missing_deliverables"]`
and a `demote_reason` naming the absent path. The diff is read from the MAIN checkout
like `_kid_measured_lines`: committed-vs-fork-base (the parent's `diff merge-base..branch`),
falling back to the branch tip tree, unioned with uncommitted + untracked work (a kid
records `done` before its commit lands).

**Conjunct (b) — the strip test now asserts the STRIP.**
`test_agi_env_strip.py::test_inherited_hookspath_really_runs_a_hook_and_the_strip_removes_it`.
The old tail asserted the absence of the same three GIT_CONFIG_ keys the test had just
`delenv`'d for itself — vacuous. Replaced with a real child subprocess that INITIALLY
INHERITS the three keys set, runs the REAL conftest `_strip_agi_env`, and must report
CLEAN. Proven non-vacuous: with the GIT_CONFIG_ removal disabled in conftest the test
fails (`LEFT=GIT_CONFIG_COUNT,GIT_CONFIG_KEY_0,GIT_CONFIG_VALUE_0`); restored, it passes.

**Conjunct (c) — the SL7.138 probe names now resolve in the tree.**
`experiment:a00-963bb500-a1eb17` names `probe_strip_predicate.py` and `probe_timeout.py`
which existed only in scratch session dirs. The node basename lacks this agent's id, so
`_round_scope_ok` refuses a strike — the commit-the-probes path was the only legal one.
Committed faithful copies at `extensions/agi/tests/probes/` (both run from the repo root
and reproduce the strip predicate and timeout observations they evidence).

## Evidence
- `python3 -m pytest extensions/agi/tests/test_cli.py extensions/agi/tests/test_agi_env_strip.py -q` → `57 passed`.
- New fixture test `test_done_demotes_a_claimed_but_absent_deliverable`: builds a real git
  repo, an untracked carried deliverable `a.py`, declares `["a.py","gone.py"]`, runs
  `cmd_done` → record verdict `inconclusive_lean_disproved:50`, `missing_deliverables==["gone.py"]`.
- Conjunct (b) falsifier held: strip's GIT_CONFIG_ removal disabled → strip test fails.
- Production lines measured: 80 (at, not above, the 2x ceiling; no re-brief required).

## Caveats
The mechanism fires on `--deliverables` paths the round's diff does not carry; it reads
the branch's change set (fork-base diff + uncommitted/untracked). It does not yet check a
kid node's body prose for a claimed deliverable the kid never declared as a path — that
remains the parent's review, as designed (the code replaces the PROMPT rule with a
machine-readable path when a round declares its deliverables).

## Agent Notes
built the claimed-but-absent deliverable demotion in cli.py (+ --deliverables, fixture test), made the strip test assert the real conftest strip via an inheriting child (falsifier verified), and committed the two SL7.138 probe scripts into the tree

parent review: reviewed committed diff 1a9e1851a. (a) the --deliverables mechanism reads the real branch diff (committed fork-base + untracked) and demotes a claimed-but-absent deliverable to inconclusive_lean_disproved:50 naming it in the record -- CODE, not parent-brief prose; fixture test green; my wire probe holds. (b) the strip test now asserts the conftest strip via a child that inherits the GIT_CONFIG_ keys and must report CLEAN -- my gate probe: fails with strip disabled, passes restored. (c) probe_strip_predicate.py + probe_timeout.py committed at extensions/agi/tests/probes/ and both run. Verified every probe THIS round names exists. Full suite green (1 pre-existing flaky rotate test, untouched by this diff, passes in isolation).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
parent review SL7.139: reviewed committed diff 1a9e1851a, not the kid report. (a) --deliverables mechanism reads the real branch diff and demotes a claimed-but-absent deliverable to inconclusive_lean_disproved:50 naming it in the record -- CODE not parent-brief prose; my wire probe and the fixture test hold. (b) strip test asserts the conftest strip via an inheriting child; my gate probe: fails with the strip disabled, passes restored. (c) both SL7.138 probe names resolve to committed runnable files. All three proof claims hold; proved stands, nothing demoted.
<!-- THOUGHT:END -->

re-verdict by master-sensei on belam ruling 00:3xZ (SL7.139 GO with conditions): proved:0.85 -> inconclusive_lean_proved:60. r1 (base): _branch_change_paths takes its fork base from origin/master|origin/main|master|main -- on this repo the season-1 master gives ~2196 carried paths vs 6 from the merge-base with season2/main, so the demotion cannot fire in production; the fixture test is green only because its fixture master IS the base. r2 (tree): the uncommitted+untracked union reads git_common_root = MAIN dirt, not the kid worktree. Both fixed under SL7.140; the mechanism is dormant behind --deliverables so the bytes land.
