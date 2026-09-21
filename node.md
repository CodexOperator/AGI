---
id: experiment:a00-eb88bf32-3f7104
mint_id: 5b17b294d053434f94995dade80e9ce6
type: experiment
parents:
  - hypothesis:l4-a-workflow-run-is-named-not-numbered
next_edges: []
confidence: 0.9
edited_by: a00-5af55508
evidence_runs:
  - experiment:a00-eb88bf32-3f7104
loop: hypothesis:l4-a-workflow-run-is-named-not-numbered@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 201e9f19c4aace7b
season: 2
title: A00 eb88bf32 3f7104
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-eb88bf32-3f7104

## Experiment
# experiment:a00-eb88bf32-3f7104

## Experiment

L4.301 FIX-ONLY (mur-42 P1 line (1), Prime XIII 00:20Z, verbatim:
'workflow.py run-key slugs the LEADING token of a merge_up cell -- a
descriptor cell ("42 (point, ...)") minted a 57-char key and defeated the
dedupe'). Landed fix on the shared tree, NOT re-deriving L4.293's dedupe.

Change in `_run_arg_tokens` (workflow.py) + one new helper `_leading_token`:
for a dict cell (`merge_up` else `key`) inside a list, the cell now slugs as
the LEADING token -- everything up to the first whitespace or `(` -- so a
descriptor cell `"42 (point, mur-42 window)"` and the bare integer `42` both
yield `42` and dedupe together; a token with no leading alnum (starts on a
paren/space) contributes nothing. `SL2#2` has no whitespace/paren and keeps
its full shape -> `sl2-2`, unchanged. Scalar/list-of-scalar paths untouched.

Real tree on the merged bytes:
  workflow.py run merge-up-review --args '{"rounds":[{"key":"L4.301",
  "merge_up":"42 (point, mur-42 window)",...},{"key":"L4.302",
  "merge_up":42,...}]}' --dry-run
prints `[run-key] mur-42` as its FIRST line -- descriptor and bare 42 deduped
to ONE token, never mur-42-42.

## Evidence

- workflow.py: new `_leading_token(value)` helper; `_run_arg_tokens` dict-cell
  branch now appends `_leading_token(cell)` (skip on empty) instead of
  `str(cell)`. Dedupe still on the token before slugging.
- test_workflow.py::test_mint_run_key_three_shapes extended:
    * two rounds {merge_up: "42 (point, mur-42 window)"} + {merge_up: 42}
      -> "mur-42" (deduped to one token)
    * {merge_up: "42 (point)"} + {merge_up: 40} -> "mur-42-40" (distinct
      leading tokens stay distinct)
- Suite: `env -u TMUX -u TMUX_PANE python3 -m pytest
  extensions/agi/tests/test_workflow.py -q` -> 48 passed (was 48; test
  extended in place, count unchanged).
- Real-tree dry-run `[run-key] mur-42`, printed first (above).

## Agent Notes
Fixed L4.301: _run_arg_tokens slugs a merge_up/key cell's LEADING token (up to first whitespace or '(', added _leading_token helper) so a descriptor cell '42 (point, mur-42 window)' and bare 42 both mint mur-42 and dedupe; SL2#2 unchanged; test_workflow extended (descriptor+dedupe, distinct tokens stay distinct); 48 passed; real-tree dry-run prints [run-key] mur-42 first.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
(1) INSTRUCTION (L4.301, verbatim): "workflow.py run-key slugs the LEADING token of a merge_up cell -- a descriptor cell (\"42 (point, ...)\") minted a 57-char key and defeated the dedupe"; the build order names the rule "the slug of everything up to the first whitespace or (". (2) THE MACHINE: _leading_token (workflow.py:109-121) strips then cuts at the first isspace() or "("; _run_arg_tokens (workflow.py:171) appends that token in the dict-cell branch BEFORE the seen-set dedupe. Parent reproduced on the merged bytes: env -u TMUX -u TMUX_PANE workflow.py run merge-up-review --args {"rounds":[{"key":"L4.301","merge_up":"42 (point, mur-42 window)"},{"key":"L4.302","merge_up":42}]} --dry-run prints [run-key] mur-42 as its FIRST line (deduped across descriptor + bare 42); test_workflow.py 48 passed. (3) NEAR MISS: a fix that slugs the WHOLE cell (42-point-mur-42-window) and de-collides later satisfies "use the merge_up cell" and loses the dedupe -- extraction must produce the SAME token before the seen-set, which is why _leading_token runs pre-dedupe, not inside _slugify_token. (4) RESIDUE, not in this build order: the seen-set still keys on the RAW leading token, so two raw tokens that slug identically ("42" and "42#") would mint mur-42-42 rather than dedupe.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-5af55508, L4.301): ACCEPTED proved 0.9. Artifact read, not the report: _leading_token at workflow.py:109 and its use at :171 match the build order; descriptor + bare 42 dedupe to one token. Parent reran the real-tree dry-run ([run-key] mur-42 first) and the suite (48 passed). Node parents resolve; evidence_runs is a list naming this experiment. Residue recorded in THOUGHT (raw-token dedupe precedes slugify).
