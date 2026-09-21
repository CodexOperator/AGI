---
id: experiment:a00-dab18263-f2f8c4
mint_id: d89f28cd9b05414f93e31a85aad5a43e
type: experiment
parents:
  - hypothesis:l5-an-across-k-kids-ceiling-is-divided-onto-each-kid-node-by-the-spawn-never-by-parent-arithmetic
next_edges: []
confidence: 0.8
edited_by: a00-26b0aa18
evidence_runs:
  - experiment:a00-dab18263-f2f8c4
line_ceiling: 12
loop: hypothesis:l5-an-across-k-kids-ceiling-is-divided-onto-each-kid-node-by-the-spawn-never-by-parent-arithmetic@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 24
profile: balanced
role: kid
scaffold_hash: 98d009b4d3195d24
season: 2
title: SM.141 the spawn divides an across-K ceiling onto each kid node at mint
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-dab18263-f2f8c4

## Experiment

G15 claim is behaviour to build, not a hypothesis to measure. Built the
three conjuncts of the target and proved them on the built bytes.

What was measured pre-fix: `spawn_budget._ceiling_clause` returned only N
(int), `node_line_ceiling` returned `(N, source)` -- the WHOLE clause number
-- with no notion of `across K kids`, and the parent brief (brief.py ~L1836)
told the PARENT to run `write.py <kid-node> 'set line_ceiling N'` with
`N = ceiling / K` by hand. That prose failed twice (SM.135 slice 2: 44 set on
each of 2 kids -> 81+54 = 135 lines, 3.07x; SM.52: 60-across-2 read as 60
and ran a kid to 212). Nothing divided the number in code.

What was built (production lines = 24, the ceiling's own 2x):

1. `spawn_budget._ceiling_clause` is still THE ONE parser and now returns
   `(N, K) | None`. Its docstring states the grammar verbatim:
   `CEILING: <=N production lines across K kids`; a clause with no
   `across K kids` means K=1, byte-identical to today. `_CEILING_KIDS_RE`
   reads K from the SAME clause segment the number came from.
2. `spawn_budget.node_line_ceiling` now returns `(slice, K, source)` where
   `slice = ceil(N/K)` -- the number the KID is measured against. brief.py
   and cli.py `_kid_line_ceiling` both read that same resolver, so the
   brief a kid gets and the harvest that judges it name one number.
3. `dispatch.main` does the division AT MINT, for `--tier kid` with a
   target: `node_line_ceiling(child_graph, target, cfg)`; when `K > 1` the
   slice is merged into `extra_fm` as `line_ceiling` BEFORE
   `_scaffold_node_for_agent` writes the node and before the brief is
   assembled. K=1 writes no field (byte-identical to today). A parent that
   hand-sets a smaller value later is safe: `node_writer` REUSE_SCAFFOLD
   never rewrites an existing node.
4. The parent-brief sentence that told the parent to do the arithmetic is
   replaced with one line saying the spawn did it and the kid node's
   `line_ceiling` is the number to read.

## Evidence

Red-first tests, then the same assertions green on the built bytes:

- `test_spawn_budget.py::test_across_k_kids_clause_sets_its_slice_as_the_kid_ceiling`
  -- parser returns `(44, 2)` for `CEILING: <=44 production lines across 2
  kids` and `(26, 1)` for a K-less clause; the resolver returns `(22, 2,
  "clause")` for the across-2 node.
- `test_dispatch.py::test_dispatch_mints_an_across_k_ceiling_slice_on_the_kid_node`
  -- drives the REAL `dispatch.main()` live (network/provisioning/Popen
  stubbed, `--detach`): the minted kid experiment node carries
  `line_ceiling: 22` under the across-2 clause, and carries NO field under a
  K-less clause. Falsified by deleting the `extra_fm` write.
- `test_brief.py::test_parent_brief_says_the_spawn_already_sliced_the_ceiling`
  -- the new sentence is present and the old `GETS ITS SLICE` / `N = ceiling
  / K` instruction is gone.

Suite: `python3 -m pytest extensions/agi/tests/test_spawn_budget.py
 extensions/agi/tests/test_brief.py extensions/agi/tests/test_dispatch.py -q`
 -> **344 passed** in 20.85s.

## Agent Notes
Built the claim on the built bytes: _ceiling_clause now returns (N,K) with the grammar verbatim in its docstring, node_line_ceiling returns (slice=ceil(N/K), K, source), dispatch.main writes line_ceiling=slice onto the kid experiment node at mint for K>1 (K=1 writes nothing), and the parent brief's do-the-arithmetic sentence is replaced by one saying the spawn did it. 344 passed in test_spawn_budget.py + test_brief.py + test_dispatch.py; production lines 24.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW by parent a00-26b0aa18 (iteration 155). Accepted: proved, on the built bytes.

WHAT THE INSTRUCTION SAID. The target is a g15 build order: the spawn, not the
parent, must divide an `across K kids` ceiling onto each kid node at mint; the
parser returns K beside N; the parent-brief sentence that ordered the parent to
do the arithmetic must be replaced by one saying the spawn did it.

WHAT THE MACHINE ACTUALLY DOES (cited to the bytes now in the tree, not to the
result file). spawn_budget._ceiling_clause returns `(N, K) | None` with the
grammar `CEILING: <=N production lines across K kids` stated verbatim in its
docstring (spawn_budget.py:279-296); node_line_ceiling returns
`(ceil(N/K), K, source)` (spawn_budget.py:330-350). dispatch.main divides at
mint for `--tier kid` with a target and merges `line_ceiling=slice` into
`extra_fm` only when K > 1, BEFORE `_scaffold_node_for_agent` writes the node
and before the brief is assembled (dispatch.py:2441-2448). brief.py:1836-1838
replaces the do-the-arithmetic sentence with `AN across K kids CEILING IS
ALREADY DIVIDED FOR YOU ... read that node field, never divide it yourself`.
cli.py:750 reads `node_line_ceiling(...)[0]` so the harvest and the brief name
one number.

PROBES RUN BY THE PARENT (three, one per conjunct; scripts under
.agi/sessions/iter-155/a00-26b0aa18/):
- Probe A (gate, parser): battery of the ONE parser. K-less `<=44 production
  lines` -> (44,1); `<=44 production lines across 2 kids` -> (44,2);
  `across 0 kids` -> (44,1); `<=45 across 3 kids` -> (45,3); across-K in the
  NEXT sentence -> (50,1) because the regex reads only the clause segment;
  `<=abc` and `HARD CEILING: 2 kids` -> None. PASS.
- Probe B (gate, harvest resolution): mint a kid scaffold the way dispatch
  does with `extra_fm line_ceiling=22`, hand-set 10, then
  cli._kid_line_ceiling reads the node field FIRST and returns 10. PASS.
  CAVEAT FOUND, recorded not falsifying: a same-slug re-mint through
  node_writer.write_node(REUSE_SCAFFOLD) DOES overwrite a frontmatter-only
  hand-set (10 -> 99), because `_is_untouched_scaffold` compares only the BODY
  (node_writer.py:495-509). Unreachable through dispatch: `_scaffold_node_for_agent`
  slugs each scaffold with a fresh uuid4 (dispatch.py:4058), so no two mints
  share a file. It stays a latent trap for any future deterministic-slug mint.
- Probe C (wire): brief._parent(...) joined output carries the new sentence and
  NEITHER old phrase (`GETS ITS SLICE`, `N = ceiling`). The wire reaches the
  assembled parent brief, not just the source string. PASS.

NEAR MISS. A parser that reads `across K kids` from the WHOLE node text rather
than the matched clause segment satisfies the words `returns the K beside N`
and loses the mechanism: this node quotes `across 2 kids` inside its own claim
and declares K=1, so a whole-text read would slice it by 2. The segment-scoped
read (same segment the number came from) is what makes the last-clause-wins
rule true.

DELIVERABLE CHECK. The diff carries all three files named in the file scope
(spawn_budget.py, dispatch.py, brief.py) and the three test files; every caller
of the arity change is updated. The kid node carries a real title, not the
derived one. production_lines 24 == 2x its 12-line ceiling, not over, so no
re-brief is owed.
<!-- THOUGHT:END -->

PARENT REVIEW a00-26b0aa18: accepted proved. Read the changed bytes in
spawn_budget.py, dispatch.py, brief.py and the three test files. Ran one
negative probe per conjunct: (A) parser battery incl. across-0 -> K=1 and
across-K-in-next-sentence -> K=1; (B) harvest reads a hand-set smaller
line_ceiling first (10 over 22); (C) the assembled parent brief carries the new
sentence and neither old phrase. All PASS. Caveat: a same-slug
REUSE_SCAFFOLD re-mint would overwrite a frontmatter-only hand-set because
_is_untouched_scaffold inspects only the body; unreachable via dispatch (fresh
uuid4 slug per mint), recorded as a latent trap.
