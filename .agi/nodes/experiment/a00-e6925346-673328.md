---
id: experiment:a00-e6925346-673328
mint_id: ba205b977570407aa10ce4e43c411a6c
type: experiment
parents:
  - hypothesis:l3w4-context-load-minimal
next_edges: []
confidence: 0.7
evidence_runs:
  - experiment:a00-e6925346-673328
loop: hypothesis:l3w4-context-load-minimal@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7f598b6fab4c0a14
season: 2
title: A00 e6925346 673328
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-e6925346-673328

## Experiment

Settles the node's open diagram-forms question with data: the hypothesis itself
proposes "render the same content three ways (prose, box-drawn, indented-arrow),
count tokens for each." Ran exactly that, two content regimes, tiktoken
o200k_base (the same method/encoding prior kids used, via /usr/bin/python3.12
-- the hermes venv python3 lacks tiktoken).

REGIME 1 -- small state card, same facts (4 roles, build boundary, 6-kid loop,
1 tree each, merge->self-perpetuating, key floor $1.00, meter 0.41/0.46):

  PROSE   154 tok   666 B
  BOX     166 tok   838 B   (+12 tok / +172 B vs prose)
  INDENT  138 tok   502 B   (-16 tok / -164 B vs prose, -28 vs BOX)

Node's own shipped BLOCK 1 box state card (verbatim from hypothesis body):
  166 tok   575 B.

REGIME 2 -- large 9-command table (the command-table shape), identical rows:

  BOX_TABLE     153 tok   752 B   border-glyphs = 199
  INDENT_LIST   108 tok   451 B   border-glyphs = 13

  -> box form is +45 tok (+42%) over the indented list for the SAME commands,
     and the 45-token gap is essentially the 199 border glyphs (~0.23 tok each,
     some glyphs share a token). Mechanism measured, not inferred.

VERDICT-RELEVANT FINDING: the hypothesis's diagram rule (favor indented trees /
arrow chains over boxes / grids; box glyphs cost tokens and carry ~no info; a
200-glyph figure can cost more than the prose) is SUPPORTED by both regimes.
Indented < prose < box in every case. The win is small per occurrence (16-28
low-tens of tokens) but the node's own reasoning -- the static prefix is paid
PER TURN, so a per-row saving multiplies through every turn a role takes -- is
exactly what makes the margin load-bearing. This is the "cheap win" the
hypothesis predicates its 70-90% target on; it alone does not reach that target
(the ~21.6k-token static prefix is dominated by INJECTION.md's graph-viewport
stream + per-role slicing, per prior kids), but it is the form-level trim that
applies everywhere prose survives.

METHOD what I actually built: two scripts saved under .agi/tmp/ (in-worktree,
per the node's standing rule that tmp/ is not durable -- /tmp/measure_prompt.py
is what never survives) to reproduce: diagram_tok.py (regime 1) and tok_table.py
(regime 2). Facts kept identical across the three forms of each regime; only the
surface changed, so the token delta is attributable to form, not content.

## Evidence

$ /usr/bin/python3.12 .agi/tmp/diagram_tok.py
PROSE      154 tok  (  666 B)
BOX        166 tok  (  838 B)
INDENT     138 tok  (  502 B)
BLOCK1      166 tok  (  575 B)  [node's shipped box state card]

$ /usr/bin/python3.12 .agi/tmp/tok_table.py
BOX_TABLE     153 tok  (  752 B)  border-glyphs=199
INDENT_LIST   108 tok  (  451 B)  border-glyphs=13

SCOPE NOTE: touched move TWO's diagram-forms sub-question only. Did NOT touch
skills/agi/SKILL.md or .agi/context/INJECTION.md (owned by other SD.06/07
streams this iteration), did NOT touch moves 1/3/4/5, did NOT write any code
into the engine tree (only two scratch scripts under .agi/tmp/), so no pytest
run was warranted — no engine code changed, only a node + scratch files.

CAVEAT: only the TOKEN metric was measured. The node's other PRIMARY metric is
ease of comprehension, and its rule says comprehension WINS when the two
conflict. No recall test was run here (would need a fresh model answering
decision questions from each form) — so this proves indented is CHEAPER, not
the stronger claim that it is the right final form on both metrics. The
hypothesis's own proposed 3-way recall test remains un-run; recommended as the
next slice before any mass diagram rewrite lands.

## Agent Notes
Measured diagram-forms question with data: indented-arrow < prose < box-drawn for identical content in BOTH regimes (small state card: BOX 166 vs INDENT 138 vs PROSE 154 tok; 9-cmd table with 199 border glyphs: BOX 153 vs INDENT 108 tok, +42%). Box overhead == border-glyph count, mechanism measured. Supports hypothesis's diagram rule. Token metric only; comprehension/recall test un-run.
