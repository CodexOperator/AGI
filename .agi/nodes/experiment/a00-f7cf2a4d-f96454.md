---
id: experiment:a00-f7cf2a4d-f96454
mint_id: 07917baf80a347ae89964770d3ccb0cd
type: experiment
parents:
  - hypothesis:l4-sm46b-the-ceiling-clause-is-read-from-the-testable-claim-field-never-from-notes-or-body
next_edges: []
confidence: 0.9
edited_by: a00-8f803a56
evidence_runs:
  - experiment:a00-f7cf2a4d-f96454
line_ceiling: 10
loop: hypothesis:l4-sm46b-the-ceiling-clause-is-read-from-the-testable-claim-field-never-from-notes-or-body@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 probes.py PROBE1 PROBE2 -- T1: node whose frontmatter testable_claim says 'CEILING: <=40 production lines' with a LATER body line 'CEILING: <=777 production lines' and Agent Notes quoting '999 lines'; T2: the live defect node hypothesis:l4-a-kid-checkpoints-... (claim 40, note 20)", "expected": "(40,'clause') for both -- the claim field wins, the later/larger body+notes numbers never do", "observed": "(40, 'clause') for PROBE1; (40, 'clause') for PROBE2 (was (20,'clause') pre-fix)", "result": "held -- could not falsify conjunct 1"}
  - {"conjunct": 2, "class": "wire", "cmd": "python3 probes.py PROBE3 PROBE3b -- run the HARVEST call site live: cli._kid_line_ceiling('.agi', {'target': <live defect node>}, target=<same>) -> 40; and cli._kid_line_ceiling('.agi', {'line_ceiling': 5}, target=<same>) -> 5. Plus: grep for a second clause parser across extensions/agi --_ceiling_clause appears only in spawn_budget.py", "expected": "40 from the harvest path (the changed bytes are live, not a stub), 5 when an answered re-brief set line_ceiling, and exactly one _ceiling_clause definition", "observed": "harvest -> 40; answered re-brief -> 5; grep: one _ceiling_clause def (spawn_budget.py:278) and its only callers are spawn_budget.node_line_ceiling, itself called from cli.py:607 (harvest) and brief.py:2101 (brief)", "result": "held -- could not falsify conjunct 2"}
  - {"conjunct": 3, "class": "gate", "cmd": "python3 probes.py PROBE6 PROBE7 -- node with parseable frontmatter whose testable_claim is a clause-less string but whose BODY says 'CEILING: <=9 production lines', config 'spawn.production_line_ceiling': 17; plus the target node itself (claim ends 'CEILING: <=10 production lines')", "expected": "(17,'default') -- the claim carries no clause so the body's 9 must NOT win; and (10,'clause') for the target", "observed": "(17, 'default') and (10, 'clause')", "result": "held -- could not falsify conjunct 3"}
production_lines: 10
profile: balanced
role: kid
scaffold_hash: d6b780937dffd8c1
season: 2
title: A00 f7cf2a4d f96454
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f7cf2a4d-f96454

## Experiment

g15 build order (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement): fix
`spawn_budget.node_line_ceiling`, do not merely measure it.

Pre-fix, on the live node:

    node_line_ceiling(.agi, hypothesis:l4-a-kid-checkpoints-...) -> (20, 'clause')

20 was a number QUOTED in the node's Agent Notes; the node's own clause (in its
`testable_claim`) is 40. So the brief handed a kid 20 and harvest judged it
against 20.

Change, `extensions/agi/bin/spawn_budget.py` (`node_line_ceiling` only, +10/-1
production lines): when the node has parseable frontmatter carrying a non-empty
`testable_claim`, feed THAT field to `_ceiling_clause`; otherwise (no/parse-
unreadable frontmatter, or field absent/empty) feed the whole text exactly as
before. `_ceiling_clause` is unchanged and remains the one parser. Module-level
`import frontmatter` (stdlib+re only, no cycle; `dispatch.py` already reads it
this way).

Three new tests in `extensions/agi/tests/test_spawn_budget.py`
(`test_node_line_ceiling_reads_only_the_testable_claim_field`): T1 claim wins
over a later notes number (40 not 20); T2 no frontmatter -> fallback body
clause (12); T3 field present with no clause -> config default 40, body's
`CEILING: <=9` must NOT win. Both pre-existing tests were left untouched: they
write frontmatter without `testable_claim`, so they exercise the fallback and
still pass (73 passed in test_spawn_budget.py + test_kid_reports_to_parent.py).

## Evidence

    $ python3 -c "...spawn_budget.node_line_ceiling(Path('.agi'),
        'hypothesis:l4-a-kid-checkpoints-...', {})"
    (40, 'clause')                      # was (20, 'clause')

    $ git diff --numstat -- extensions/agi/bin/spawn_budget.py
    10      1       extensions/agi/bin/spawn_budget.py

    $ python3 -m pytest extensions/agi/tests/test_spawn_budget.py \
        extensions/agi/tests/test_kid_reports_to_parent.py -q
    73 passed

    $ python3 -m pytest extensions/agi/tests/test_spawn_budget.py \
        extensions/agi/tests/test_kid_reports_to_parent.py \
        extensions/agi/tests/test_brief.py -q
    210 passed

production_lines=10, line_ceiling=10 — at the ceiling, not above 2x, so no
re-brief was needed.
Raw output, screenshots, logs.

## Agent Notes
node_line_ceiling now reads the clause from the frontmatter testable_claim field only, whole-text fallback when frontmatter is unparseable or the field is absent/empty; _ceiling_clause unchanged as the one parser. Live check moved (20,'clause') -> (40,'clause'); 3 new tests; 210 passed; 10/1 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-8f803a56 (SM.47), tier parent, target hypothesis:l4-sm46b-...
Verdict: ACCEPT as proved. Reviewed the BYTES (git show 731fd8399 -- extensions/agi/bin/spawn_budget.py extensions/agi/tests/test_spawn_budget.py), not the result file, and ran one parent-run negative probe per claim conjunct (probes below, recorded via write.py `set probes`).

(1) WHAT THE INSTRUCTION SAID. The target's own words: "node_line_ceiling resolves the clause from the node's frontmatter `testable_claim` field ONLY (through the frontmatter reader the engine already has, never a regex over the whole file), falling back to the whole text only when the node has no parseable frontmatter"; "(2) brief and harvest still share that one resolver (no second parser)"; "(3) a node whose testable_claim carries no clause resolves to the config default as today."

(2) WHAT THE MACHINE ACTUALLY DOES. spawn_budget.py:341-342, read from the committed bytes: `text = _node_text(...)`; `fm = None if text is None else frontmatter.read_frontmatter(text)`; `claim = fm.get("testable_claim") if isinstance(fm, dict) else None`; `n = _ceiling_clause(claim if isinstance(claim, str) and claim else text)`. `frontmatter.read_frontmatter` (extensions/agi/bin/frontmatter.py:55) is the engine's existing reader; `frontmatter.py` imports stdlib only, so the new module-level import cannot cycle. I RAN the resolvers, not read them: probes.py PROBE1 (claim <=40, later body <=777, notes 999) -> (40,'clause'); PROBE2 (the live defect node hypothesis:l4-a-kid-checkpoints-...) -> (40,'clause'), was (20,'clause') measured on the pre-fix tree before the kid was spawned; PROBE3 the HARVEST call site live, cli._kid_line_ceiling('.agi', {'target': <that node>}, target=<that node>) -> 40; PROBE3b with {'line_ceiling': 5} -> 5; PROBE6 (clause-less claim, body <=9, cfg 17) -> (17,'default'); PROBE7 (this target node, claim ends "CEILING: <=10") -> (10,'clause'). Grep across extensions/agi: `_ceiling_clause` defined once at spawn_budget.py:278, called only from spawn_budget.py:342; `node_line_ceiling` called from exactly cli.py:607 (harvest) and brief.py:2101 (brief). 73 passed in test_spawn_budget.py + test_kid_reports_to_parent.py, the two existing SM.46 tests untouched and green. 10/1 production lines, at the ceiling.

(3) THE NEAR MISS. A `testable_claim`-only read that DROPS the field-absent fallback satisfies (1)'s "field ONLY" and loses the falsifier list: the two existing SM.46 tests write parseable frontmatter with NO `testable_claim` and the clause in the BODY (test_spawn_budget.py:1272, test_kid_reports_to_parent.py:551), and would go red -> the claim's own named falsifier. The kid kept the fallback and stayed green. I therefore read (1)'s "falling back ... only when the node has no parseable frontmatter" as "no parseable frontmatter OR no usable field", because the strict reading contradicts the falsifier list; the kid's reading is the only one satisfying both, and it is what CONJUNCT 3's "carries no clause -> default" then covers for the field-present-but-clause-less case (PROBE6 proves the boundary: field present + clause-less -> default, body's 9 does NOT win).

(3b) THE RESIDUAL, NAMED. The fallback is not harmless: I censused live nodes (script in the SM.47 scratch dir) and 18 `.agi/nodes/**/*.md` files have parseable frontmatter with NO `testable_claim` field yet resolve a whole-text clause (PROBE4: such a node with a note `CEILING: <=13 production lines` resolves (13,'clause')). Those are goal/, idea/ and experiment/ nodes, not the hypothesis/task nodes a parent re-cuts from -- every L4 hypothesis node carries the field, so the defect this node exists to fix is closed for the population that hits it -- but the hole is open for the other 18. That is a candidate for a follow-up node, not a falsifier of this one.

(4) DEVIATION FROM A STANDING RULE. None taken. The kid stayed inside FILE SCOPE (spawn_budget.py, test_spawn_budget.py), did not touch `_ceiling_clause`'s semantics, added no second parser, and added no test beyond the three asked for.
<!-- THOUGHT:END -->

Parent a00-8f803a56 SM.47 review: ACCEPT, proved. Read the bytes (731fd8399), not the result file. 3 parent-run negative probes, one per conjunct (gate/gate+wire/gate), all held: claim<=40 beats later body<=777+notes 999 -> 40; BRIEF+harvest reach the changed bytes live (cli._kid_line_ceiling -> 40; answered line_ceiling=5 still wins) with exactly one _ceiling_clause parser; clause-less claim -> config default 17, body's 9 does NOT win. 73 tests green, SM.46's two tests untouched. NAMED RESIDUAL (caveat, not a falsifier): 18 live nodes without a testable_claim field still fall back to whole-text last-match, so a note number can win there; follow-up candidate.
