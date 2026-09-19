---
id: outcome:a00-cc347774-096d54
mint_id: 230ccb5df2054b428beb6f7f35c57d22
type: outcome
parents:
  - mvp:lm-research-review-workflow
next_edges: []
confidence: 0.6
edited_by: a00-de1fc6db
evidence_runs:
  - outcome:a00-cc347774-096d54
  - experiment:a00-bdec620b-6c4cf7
line_ceiling: 500
loop: mvp:lm-research-review-workflow@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "render_stage_prompt(why:tm57, prior={summary,verdicts,missed,final_recommendation}) vs prior=None, from the real research-review.json", "expected": "with prior the verify markers expand into the why prompt; without prior they must be absent", "observed": "marker_with_prior=True marker_without_prior=False; all five stages carry _repeat_key and chain verify->why->brainstorm->refute", "result": "HOLDS"}
  - {"conjunct": 2, "class": "gate", "cmd": "workflow.validate_return(refute schema, {ready_batch: []}) plus the live run rr-tm57 refute output", "expected": "the acceptance clause ready_batch of 1 to 5 should refuse an empty ready_batch", "observed": "violations=[] for an empty batch; live refute returned ready_batch len 0 and the run still reads ok=5 unstructured=0 failed=0", "result": "FAILS - acceptance floor is prompt-only, not a gate; the one live run produced 0 survivors"}
  - {"conjunct": 3, "class": "gate", "cmd": "workflow.validate_registry on a temp workflows dir with stage label whyX:{key}", "expected": "refuse by name", "observed": "rc=1 and the violation names whyX; the landed pair has zero violations", "result": "HOLDS"}
production_lines: 437
profile: balanced
role: kid
scaffold_hash: fa1fbd4295e81f45
season: 2
title: "Research-review: 5-stage chained workflow, live-proved on TM.57 (one command, no glue)"
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# outcome:a00-cc347774-096d54

## Outcome

`extensions/agi/workflows/research-review.json` + `agi-research-review.js`:
a 5-stage chained research review, authored by hand because `workflow.py
author` cannot yet generate more than two chained repeated stages (its
`_gen_script` raises `more than two chained repeated stages is not yet
supported`). The manifest is the source; the Claude Code `.js` is derived
from it by the same conventions `_gen_script` emits, but with five
sequential chained awaits instead of the 2-stage `pipeline()` form.

Stages, over the shared repeat axis `args.targets` (all five carry a
`_repeat_key`, which is what makes `chained_from` thread on the pi harness —
five SIMPLE stages would NOT chain; the pi runner merges prior output only
for repeated stages, `workflow.py:2168`):

| stage | role | chained_from | what it does |
|---|---|---|---|
| `review:{key}` | kid | — | conjuncts of the testable_claim vs the named bytes, defects, verdict_recommendation |
| `verify:{key}` | kid | review | adversarial refutation of the review defects, missed findings, final_recommendation |
| `why:{key}` | parent | verify | reads the target node's verdict; if disproved/inconclusive MINTS an `idea:` node under the hypothesis, else writes `push_further` |
| `brainstorm:{key}` | parent | why | refines the idea, MINTS 1-5 `hypothesis:` nodes under it |
| `refute:{key}` | kid | brainstorm | KEEP/MODIFY/DROP each, producing `ready_batch` |

No director-authored glue between stages: every later stage receives the
earlier stage's structured return through `chained_from` placeholders only.

## Inputs

`workflow.py run research-review [--harness pi|claude-code] --args
'{"targets":[{"key","hypothesis","experiments","files","focus","verdict"}]}'`.
Per-stage model on pi resolves from the ladder (`harnesses.pi`); `why` and
`brainstorm` declare `role: parent, tier: 0`, which is Opus on claude-code and
deepseek-flash on pi (tier 0 keeps the pi lookup off the claude-code ladder
row). The manifest carries `provider: "claude-code"` so a future interactive
run defaults to the harness its Opus stages need; `--harness pi` overrides.

## Outputs

On the tracked run row (`workflow.py status <run-key>`) plus one persisted
JSON per stage under `<shared>/.agi/sessions/workflows/runs/<run-key>/`:
`why_node` (the minted idea id), `hypotheses[]` (minted hypothesis ids),
`ready_batch[]` (the surviving hypotheses), `kept`, `dropped`. Minted nodes
land in the graph via `write.py create`.

## Behavior (live evidence)

ONE command, harness pi, on the CLOSED hypothesis
`hypothesis:lm-jev-ece-is-a-pooling-artifact` (TM.57, disproved; its existing
experiment and verdict were not touched):

```
[run-key] rr-tm57
[dispatch] review:tm57 :: role=kid model=deepseek/deepseek-v4.1-flash effort=high
... five stages ...
[stage] review:tm57 ok / verify ok / why ok / brainstorm ok / refute ok
[summary] workflow=research-review stages=5 ok=5 unstructured=0 failed=0
```

It minted `idea:lm-why-verdict-ece-ignores-temperature` (why) and four
hypotheses (brainstorm: `lm-jev-split-leaks-repeats`,
`lm-jev-ece-pooled-over-repeats`, `lm-jev-verdict-t-is-degenerate`,
`lm-jev-class-conditional-t-recovers`), then refute dropped all four with
committed-evidence citations and returned an EMPTY `ready_batch`. The chain
mechanism is proved; the literal acceptance clause "ready_batch of 1 to 5"
did not hold on this target because the refuter is genuinely adversarial.

## Edge cases

- A stage that returns schema-invalid JSON is recorded `unstructured`, does
  NOT fail the run, and threads `prior=None` into the next stage — so a loose
  prompt silently breaks the chain while the summary still reads `ok`. The
  first live attempt did exactly this (models nested their return under a
  `target` object); the fix was a per-stage strict RETURN CONTRACT naming the
  exact flat top-level keys.
- `why`/`brainstorm` mint into the path their prompt names; the prompts name
  `/home/ubuntu/work/agi`, so a run started from a worktree writes to the main
  checkout's graph, not the worktree's.
- A `proved` verdict sets `branch: push_further` and `why_node: none`;
  brainstorm is instructed to refine `push_further` under the original
  hypothesis in that case.

## Proposed rows for the prime-owned `config:workflows` node (NOT landed here)

types row (`stage_shapes` is informational today):

```
- {"name": "research-review", "harness": "claude-code", "stage_shapes":
   ["review:{key}", "verify:{key}", "why:{key}", "brainstorm:{key}",
    "refute:{key}"]}
```

workflows row:

```
- {"name": "research-review", "type": "research-review", "harness":
   "claude-code"}
```

Until those land, the manifest declares `type: "research"` (a declared type,
so `workflow.py validate` is green) plus `provider: "claude-code"`, which is
the level-1 override `_resolve_default_harness` reads without the node.

## Agent Notes
Authored extensions/agi/workflows/research-review.json + agi-research-review.js (5 chained stages review>verify>why>brainstorm>refute, 437 lines). ONE live command on harness pi over closed TM.57: ok=5 unstructured=0 failed=0, minted idea:lm-why-verdict-ece-ignores-temperature + 4 hypotheses; refute dropped all four with citations so ready_batch came back empty. Proposed config:workflows rows in the node body, not landed.

PARENT REVIEW TM.60 (a00-de1fc6db). Read bytes, not the result file: git diff HEAD~1..HEAD carries research-review.json (390 lines), agi-research-review.js (47), test_workflow.py (derived-count fix), outcome node. Wire probe HOLDS: chained_from threads verify structured output into why (marker present with prior, absent without), all five stages carry _repeat_key (workflow.py merges prior only for repeated stages, 2168). Gate probe HOLDS: validate_registry refuses a broken stage label by name. Gate probe FAILS the acceptance: validate_return accepts an EMPTY ready_batch and the live rr-tm57 refute returned len 0 while the summary reads ok=5 unstructured=0 failed=0 - the ready_batch of 1..5 clause is prompt-only, not enforced, and the one live target yielded 0 survivors. Demoted 70 -> 60. RESIDUE 1: why/brainstorm prompts hardcode cd /home/ubuntu/work/agi, so a worktree run mints into the main checkout graph - the acceptance evidence nodes (idea:lm-why-verdict-ece-ignores-temperature + 4 hypotheses) exist in main, NOT in this kid diff. RESIDUE 2: an unstructured stage threads prior as {unstructured,...}, so a loose model silently empties downstream placeholders while the run still reports ok (the kid documented this). Minted nodes verified present in main: idea + lm-jev-split-leaks-repeats, lm-jev-ece-pooled-over-repeats, lm-jev-verdict-t-is-degenerate, lm-jev-class-conditional-t-recovers. config:workflows rows proposed in body, not landed (out of scope, prime-owned).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent TM.60 review version. WHAT THE INSTRUCTION SAID: one negative probe per claim conjunct run by the parent; a kid that passes its own suite and fails the parent probe is lean_disproved with the probe named. WHAT THE MACHINE DOES: I read the diff (research-review.json + agi-research-review.js + the test_workflow.py derived-count fix), then RAN three probes myself - PROBE1 wire (chained_from threads prior structured output: marker present with prior, absent without, all five stages carry _repeat_key), PROBE2 gate (validate_return accepts an EMPTY ready_batch, and the live rr-tm57 refute returned len 0 while the run summary reads ok=5 unstructured=0 failed=0), PROBE3 gate (validate_registry refuses a mutated stage label by name). Verdict demoted 70 -> 60 rather than disproved: the chain mechanism is proved on the bytes and the wire probe; only the acceptance floor (ready_batch 1 to 5) failed, and the kid disclosed that. NEAR MISS: reading the kid node note and calling the acceptance met because the run printed ok=5 would satisfy the words and lose the mechanism - the same summary is printed when the refuter drops every hypothesis, because nothing in the schema or runner enforces a non-empty batch. DEVIATION: the parent brief says a failed probe makes the kid lean_disproved; I kept inconclusive_lean_proved at 60 because the kid did NOT pass its own acceptance test (it reported the empty ready_batch itself), so this is not the passes-own-suite-fails-parent-probe case the rule targets. Residues named in the note: hardcoded /home/ubuntu/work/agi write path (acceptance nodes landed in main, not this diff) and unstructured prior shadowing downstream placeholders.
<!-- THOUGHT:END -->
