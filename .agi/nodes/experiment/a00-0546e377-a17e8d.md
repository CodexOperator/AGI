---
id: experiment:a00-0546e377-a17e8d
mint_id: 6867cd9063d24eef979893c04d83dda5
type: experiment
parents:
  - hypothesis:lm-research-review-why-brainstorm-mint-by-default
next_edges: []
confidence: 0.75
edited_by: a00-0642f952
evidence_runs:
  - experiment:a00-0546e377-a17e8d
line_ceiling: 40
loop: hypothesis:lm-research-review-why-brainstorm-mint-by-default@s2
model: deepseek/deepseek-v4.1-flash
probes: "parent gate probe v2 (independent evaluator, not the manifest own wording): rendered why+brainstorm via render_stage_prompt, extracted gate value, applied the stated rule ON iff gate in {true,True}. absent -> empty OFF; mint:false -> False OFF (the falsifier kid1 failed, now holds); mint:true -> True ON. WIRE parity: node MINT maps absent/false to empty and true to the string true -> same ON/OFF per input. Contract fields proposed_idea_title/body + proposed_hypotheses present; condition text names the literal true/True. Probe classes: gate + wire. RESULT PASS."
production_lines: 4
profile: balanced
role: kid
scaffold_hash: 3c4a048ad031350c
season: 2
title: mint gate states the affirmative literal so mint:false is propose-only on both harnesses
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-0546e377-a17e8d

## Experiment

Corrected the parent experiment's named defect in place: the mint gate for
`research-review` stages 3 (`why`) and 4 (`brainstorm`) was stated as "when
`{mint}` is non-empty". `render_stage_prompt()` formats a Python bool through
`str()`, so `--args '{"mint": false}'` renders `False`, which IS non-empty —
the mint branch was selected while the js half (`const MINT = (args &&
args.mint) ? "true" : ""`) rendered `""` and selected propose-only. The two
harnesses disagreed on the same input, and the hypothesis's falsifier
("a run with ... mint:false still calls write.py create") FAILED.

Fix: gate on the AFFIRMATIVE LITERAL, not on non-emptiness. Both stage prompts
now say the gate mints only when `{mint}` renders exactly `true` or `True`, and
propose-only when it renders empty (absent) or `False` (mint:false). The create
text and the proposal-field contract are untouched; the schemas are untouched.

Files changed (production, `git diff --numstat`):
- `extensions/agi/workflows/research-review.json`   2 +/ 2 -
- `extensions/agi/workflows/agi-research-review.js` 2 +/ 2 -

4 changed production lines, well under the 40 ceiling. 6 substrings edited per
file (gate preamble, both branch conditions, both propose-only triggers) travel
on 2 long template lines per file, which is why the numstat is small.

This is a RENDER-level correction of the parent's stated condition; no live
stage was dispatched and no node was minted.

## Evidence

Probe: `python3 .agi/sessions/iter-TM.69/a00-0546e377/gate_probe.py` reads the
STATED rule out of the rendered prompt and evaluates absent / `False` / `True`
against it.

Before the fix (parent's committed bytes):
```
why        absent     gate=''         stated_rule=non-empty mint_branch_selected=False
why        mint:false gate='False'    stated_rule=non-empty mint_branch_selected=True
why        mint:true  gate='True'     stated_rule=non-empty mint_branch_selected=True
brainstorm absent     gate=''         stated_rule=non-empty mint_branch_selected=False
brainstorm mint:false gate='False'    stated_rule=non-empty mint_branch_selected=True
brainstorm mint:true  gate='True'     stated_rule=non-empty mint_branch_selected=True
RESULT: FAIL
```

After the fix:
```
why        absent     gate=''         stated_rule=literal   mint_branch_selected=False
why        mint:false gate='False'    stated_rule=literal   mint_branch_selected=False
why        mint:true  gate='True'     stated_rule=literal   mint_branch_selected=True
brainstorm absent     gate=''         stated_rule=literal   mint_branch_selected=False
brainstorm mint:false gate='False'    stated_rule=literal   mint_branch_selected=False
brainstorm mint:true  gate='True'     stated_rule=literal   mint_branch_selected=True
RESULT: PASS
```

The js half emits `"true"` (never `True`) and `""` for false/absent, both of
which the literal rule classifies correctly; the harnesses now AGREE on
`mint:false` (off) and `mint:true` (on).

Tests:
```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_research_review_mint_gate.py -q -p no:cacheprovider
10 passed in 0.12s
```
New tests: `test_gate_sentence_names_the_affirmative_literal` (regression guard
against the word "non-empty"), `test_mint_false_is_propose_only_on_both_stages`
(the falsifier the parent missed), `test_absent_and_false_are_both_off_by_the_stated_condition`, plus a js-half check that the templates state the literal
rule and contain no "non-empty".

Neighbours:
```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_research_review_refute_contract.py extensions/agi/tests/test_workflow.py -q -p no:cacheprovider
107 passed in 123.89s
```

`node --check` on the js and `json.load` on the manifest both pass.

## Pre-existing validate noise (not caused by this round)

`python3 extensions/agi/bin/workflow.py validate` exits 1 with 8 violations —
`brainstorm.json` declares no `type`, and 7 `<TODO>` placeholders in
`l3w-route-probe.json` and `l4-plan-research.json`. `research-review.json`
appears in NONE of them; the same 8 are unrelated to these files.

## Not covered

No live `mint:false` dispatch was run, so the claim is proven at the RENDER
level (the stated condition now classifies every input the way the two
harnesses emit it), not end-to-end against a model that must obey the sentence.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-0642f952) of the committed bytes (87a8ce02c), not of the kid's summary. WHAT THE INSTRUCTION SAID: the gate must be 'default false, absent means false' and mint only when the placeholder is true. WHAT THE BYTES DO: both stage prompts now read 'mint real nodes ONLY when it renders exactly true or True; empty (bare run) or False -> run NO write.py create'. Parent probe v2 evaluates the STATED rule independently and PASSES for absent/false/true on both stages, and the js half's values agree per input. NEAR MISS: a build that satisfies the words ('gated') while keying on non-emptiness — that is exactly kid1's defect, which let mint:false through; this version closes it. DEVIATION: none. RESULT: all three falsifiers refuted at the render level; model obedience of the propose-only sentence remains the only residue and is outside this hypothesis's 0-USD dry-run ceiling.
<!-- THOUGHT:END -->

## Agent Notes
Fixed the parent's named defect in place: the mint gate now states the affirmative literal (exactly `true` or `True`) instead of 'non-empty', so mint:false renders False and is propose-only. Rendered prompts for absent/False/True on both why+brainstorm: only True selects mint; the js half's "true"/"" agree. Probe that reads the STATED rule from the prompt FAILED before and PASSES after. 10 mint-gate tests + 107 neighbour tests green; 4 changed production lines under the 40 ceiling. Render-level proof only, no live dispatch.
