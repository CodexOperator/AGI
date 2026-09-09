---
id: experiment:a00-44a0a4f2-822f85
mint_id: a031c76e67a04c40aa7bbb52dd3a85a8
type: experiment
parents:
  - hypothesis:l3w4-context-load-minimal
next_edges: []
confidence: 0.4
edited_by: a00-44a0a4f2
evidence_runs:
  - experiment:a00-44a0a4f2-822f85
loop: hypothesis:l3w4-context-load-minimal@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 23f9bb73e473cd0e
season: 2
title: "Recall-test prep: item 18/20/24/27 prose + diagrams + questions (steps 1-3 only)"
verdict: inconclusive_lean_disproved:40
---
<!-- BODY:BEGIN -->
# experiment:a00-44a0a4f2-822f85

## Scope
Lock this node to **recall-test prep, PARENT a00-084e15da KID-1 brief, steps 1-3 only**:
extract HANDOFF item prose, build indented-tree/arrow diagram forms, write question files.
The recall test itself (two isolated readers) is the NEXT kid's slice. Nothing here touches
SKILL.md, INJECTION.md, rotate.py, or HANDOFF.md.

## Experiment

Step 1 - Extract prose. Source = HANDOFF.md grid **version 298** (the pre-collapse version holding
items 18/20/24/27 full prose; current HANDOFF.md only carries one-line closed entries).

BLOCKER FOUND + WORKED AROUND: `grid.py payload build:HANDOFF.md --version 298` failed with
`ERR: no grid history for build:HANDOFF.md`. Root cause: this harness exports
`AGI_TREE_PROJECT_ROOT=<repo root>` (the worktree dir), but grid.py's `project_root_from_env`
hands that value straight to `resolve_ref`, which feeds it to `build_id_index` expecting the GRAPH
root (`.agi` dir) — so the node index comes back empty and it falls through to the legacy ref, which
is None. Manual calls with `locations.find_project_root()` (graph root) resolved fine.
WORKAROUND: `unset AGI_TREE_PROJECT_ROOT` then run grid.py — then root resolution walks from cwd and
gets the `.agi` graph dir. Command then worked: 772 lines, 269KB payload to /tmp.

Extracted items 18, 20, 24, 27 by line number (179/185/193/199) into `.agi/tmp/recall/itemNN.prose.md`.
All verified clean UTF-8. Item 24 and 27 owner-verbatim spans extracted programmatically to
`itemNN.verbatim.md` (regex on the leading double-quoted block).

Step 2 - Diagram forms. Built genuine row-local indented-tree / arrow-chain diagrams
(no box grids, no compressed prose-on-one-line). Negations, conditions, attributions and
supersessions carried explicitly in words. Owner-verbatim spans for items 24/27 embedded
byte-identical (scripted assembly so no transcription drift); verified `verb in diagram == True`
for both. Item 18's draft-workflow and 20's seats are prose-authorable; the owner quote is relayed,
not quoted verbatim inline, so no verbatim block there.

Step 3 - Question files. `itemNN.questions.md`, same decision-question shape per item
(what did the owner settle / what is forbidden / current state / what supersedes / conditions).

## Measurement (tiktoken o200k_base) — labeled RECALL PREP in Agent Notes

Prose vs diagram, per item and total. NOTE the negative cuts — see Agent Notes on why these
four items are the hardest case.

## Evidence

- `.agi/tmp/recall/item18.prose.md item18.diagram.md item18.questions.md`
- `.agi/tmp/recall/item20.{prose,diagram,questions}.md`
- `.agi/tmp/recall/item24.{prose,diagram,questions}.md item24.verbatim.md`
- `.agi/tmp/recall/item27.{prose,diagram,questions}.md item27.verbatim.md`
- payload extraction: `unset AGI_TREE_PROJECT_ROOT && grid.py payload build:HANDOFF.md --version 298`
- owner-verbatim byte-identity: `item24/27 verbatim present in diagram: True`
- UTF-8: every file `OK utf8`

## Agent Notes
RECALL PREP (KID-1, steps 1-3): extracted items 18/20/24/27 full prose from grid v298 and built genuine indented-tree/arrow diagrams + question files in .agi/tmp/recall/. BLOCKER+WORKAROUND: grid.py payload errored "no grid history" under AGI_TREE_PROJECT_ROOT=<repo root>; unset the var and it resolves the .agi graph root and works (772 lines, 269KB). Owner-verbatim spans in items 24/27 embedded byte-identical (verified True). TOKEN SIZES (tiktoken o200k_base), prose vs diagram, per item: 18: 713 vs 881 (-23.6%); 20: 568 vs 650 (-14.4%); 24: 954 vs 1042 (-9.2%); 27: 743 vs 831 (-11.8%); TOTAL 2978 vs 3404 (-14.3%). THE DIAGRAMS ARE LARGER, not smaller, on these four items. Why: they are the hardest case — dense owner-decision prose with negation/condition/attribution/supersession shapes, and items 24/27 must carry a byte-identical owner-verbatim block that is itself most of the content and not shrinkable. This corroborates the standing hypothesis concern that these shapes are exactly what survives in prose and dies in a diagram. Verdict on whether diagram-form helps is for the RECALL TEST (next kid), not this prep.

## Agent Notes
RECALL PREP landed: items 18/20/24/27 prose+diagrams+questions in .agi/tmp/recall/, owner-verbatim byte-identical. Diagrams are LARGER than prose on these 4 hardest items (-14% total tok). Recall test still next kid's job.
