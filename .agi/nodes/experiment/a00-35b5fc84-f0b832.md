---
id: experiment:a00-35b5fc84-f0b832
mint_id: 745d5e1147b14994a2a0f30bbf83d3ed
type: experiment
parents:
  - hypothesis:the-parent-and-kid-brief-text-matches-the-engine
next_edges: []
confidence: 0.9
edited_by: a00-2ce05f60
evidence_runs:
  - experiment:a00-35b5fc84-f0b832
loop: hypothesis:the-parent-and-kid-brief-text-matches-the-engine@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "scratch probe_brief.py rendered the LIVE post-fix parent brief via brief.assemble tier=parent and grepped for 2 = timeout, 3 = --agent, 4 = zero tier:kid rows; pre-fix bytes read from git show 73a0e3cbf9:extensions/agi/bin/brief.py", "expected": "post-fix parent brief carries all three actionable codes with actions; pre-fix carries only when wait returns 2", "observed": "post-fix all three present; pre-fix line 1932 carries only 2", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_cli_wait.py -q", "expected": "engine wait returns 3 for --agent no-match and 4 for zero tier:kid rows; suite green", "observed": "9 passed in 13.37s; cli.py:2337 _WAIT_NO_AGENT=3, cli.py:2346 _WAIT_NO_KID_ROWS=4", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "scratch probe_brief.py rendered the LIVE kid brief via brief.assemble tier=kid line_ceiling=40 and grepped for the unconditional stamp phrase and for K > 1", "expected": "the unconditional claim is absent; the stamp is gated on K > 1; the NEVER write rule survives", "observed": "phrase absent; ONLY when and K > 1 present; NEVER write line_ceiling present", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "read dispatch.py 2504-2509", "expected": "line_ceiling is stamped on the kid scaffold only when node_line_ceiling K > 1", "observed": "if args.tier == kid and target: node_line_ceiling; if _k > 1: extra_fm line_ceiling", "result": "held"}
production_lines: 12
profile: balanced
role: kid
scaffold_hash: 37f18987a71ff890
season: 2
title: The brief text now names every actionable wait code and gates the scaffold-stamp claim on K>1
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-35b5fc84-f0b832

## Experiment

Two brief-text defects, both fixed in `extensions/agi/bin/brief.py` and
proved by committed tests over the RENDERED brief text.

| # | byte | pre-fix | post-fix |
|---|---|---|---|
| M3 | `brief.py` parent wait rule (~1932) | named only `when wait returns 2, call it again` | names 2 (timeout, call again), 3 (`--agent` matches no row), 4 (zero tier:kid rows, NO kid spawned) with the action for each |
| D | `brief.py` kid ceiling sentence (~1433) | `already stamped on your scaffold by dispatch` unconditionally | `ONLY when ... ACROSS more than one kid (... K > 1); when K is 1 the field is ABSENT` |

M3 is the engine's truth: `cli.cmd_wait` returns `_WAIT_NO_AGENT = 3` and
`_WAIT_NO_KID_ROWS = 4` (cli.py:2340-2350, covered by test_cli_wait.py).
D is the engine's truth: dispatch.py ~2479 stamps `line_ceiling` only
`if _k > 1` from `spawn_budget.node_line_ceiling`.

Order of work: two tests written FIRST and run red on the pre-fix bytes,
then the brief.py text edited, then green.

## Evidence

RED (pre-fix bytes), `pytest test_brief.py -k "every_actionable_wait_code or
always_stamps_the_ceiling"`:

```
2 failed, 153 deselected in 0.55s
```

GREEN (post-fix bytes), same selection:

```
2 passed, 153 deselected in 0.16s
```

Full changed-file suite, `pytest test_brief.py -k "not
g15_rule_with_no_project_root" test_cli_wait.py test_brief_render.py`:

```
154 passed, 1 deselected; test_cli_wait.py + test_brief_render.py green
```

Production lines (the ONE allowed git read), `git diff --numstat --
extensions/agi/bin/brief.py`:

```
12	4	extensions/agi/bin/brief.py
```

PRE-EXISTING, unrelated: `test_g15_rule_with_no_project_root_keeps_the_current_
fallback` fails on this tree. The live node
`hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement` now parents to
`goal:g6.11` + a hypothesis, not `goal:g15` as its docstring claims, so
`_is_g15_lineage` is false. A stale test against a reparented node; my edit
touches no lineage code.

## Agent Notes
brief.py parent wait rule now names codes 2/3/4 with actions; kid ceiling sentence gates the scaffold-stamp claim on K>1; two tests red pre-fix, green post-fix; production_lines 12, under the 40 ceiling

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW EF.62 (a00-2ce05f60), judging experiment:a00-35b5fc84-f0b832 against hypothesis:the-parent-and-kid-brief-text-matches-the-engine. INSTRUCTION: the target claim says the parent wait rule names every actionable non-zero code and the kid ceiling sentence stops saying dispatch stamped the ceiling on the scaffold unconditionally. MACHINE: git show 1e18e8da20 -- extensions/agi/bin/brief.py shows line 1429 reworded to gate the stamp on K > 1 through spawn_budget.node_line_ceiling, and line 1932 now names 2 (timeout with a kid still running, call it again), 3 (--agent names no manifest row), 4 (zero tier:kid rows, no kid was spawned). LIVE PROBES: brief.assemble renders all three codes in the parent brief and renders no unconditional stamp phrase in the kid brief; cli.py _WAIT_NO_AGENT=3 (2337) and _WAIT_NO_KID_ROWS=4 (2346) confirm the engine; pytest test_cli_wait.py 9 passed; dispatch.py stamps line_ceiling only inside if _k > 1 (2507). NEAR MISS: a text naming only 3 and 4 would satisfy the director order words while losing the code 2 that was already there, and a text naming 2/3/4 without a per-code action would satisfy the list while losing the fix. DEVIATION: the target testable_claim carries no numbered items, so the tier-parent probe gate resolves zero conjuncts and is not active; the two conjuncts are the two clauses of the claim and one negative probe each is recorded here and on the agent record anyway. CAVEAT: cli.py wait also returns 1 when the manifest is missing, an infra case the brief does not name; cli.py documents that case as missing-manifest and distinct from the three actionable codes, so the parenthetical enumeration is complete at 2/3/4. Pre-existing and unrelated: test_brief.py::test_g15_rule_with_no_project_root fails on this tree (reparented lineage node), untouched by these bytes.
<!-- THOUGHT:END -->

PARENT ACCEPTED (a00-2ce05f60): brief.py wait rule names the three actionable wait codes 2/3/4 with actions; kid ceiling sentence now gates the dispatch stamp on K > 1. Probes held (conjuncts 1 and 2); test_brief.py 154 passed with one pre-existing unrelated failure, test_brief_render.py 24 passed, test_cli_wait.py 9 passed. Verdict proved stands.
