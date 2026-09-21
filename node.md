---
id: experiment:a00-ee5d3690-b88b05
mint_id: e3fa142bb6ca4a63b2e040c26ee4d642
type: experiment
parents:
  - hypothesis:l4-workflow-authoring-is-a-harness-tool
next_edges: []
confidence: 0.8
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-ee5d3690-b88b05
loop: hypothesis:l4-workflow-authoring-is-a-harness-tool@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1cf30acde0b73709
season: 2
thought_session: sanctuary-director-genVII-L4
title: A00 ee5d3690 b88b05
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-ee5d3690-b88b05

## Experiment

Extended `hypothesis:l4-workflow-authoring-is-a-harness-tool` by BUILDING the
`author` verb (hypothesis req (1)-(3)) on the live tree, in the files the
director allowed. `workflow.py` edited in place (build:bin-workflow, THOUGHT
updated).

**What I did** — four engine changes + one workflow rewrite:

1. **`workflow.py author <name> --stages <json|path|stdin>`** (new verb). Takes a
   stage list, writes BOTH halves of a runnable pair in one action: `<name>.json`
   (manifest, real prompts) AND `agi-<name>.js` **generated FROM the manifest**
   (manifest = source, script = derived). The generated script is a genuine
   Claude Code Workflow script — `export const meta {name,description,phases}`,
   `phase('Title')`, `agent(prompt, {label, phase, schema, model, effort})`,
   `pipeline(items, project, accumulate)` — byte-shaped like the reference
   templates, so `run <name> --harness claude-code` hands it to the native
   Workflow tool (owner hard constraint #2). Prompts render through a `fill`
   helper that only expands `{word}` placeholders, leaving inline JSON-schema
   braces untouched — matching pi's `_PLACEHOLDER` exactly. Item list comes from
   `args['<of>']` at runtime, model falls back to `args.model` then manifest
   hint.

2. **Pi chain mechanism (hypothesis asks ONE be established & documented).**
   Verified myself that `_run_stage_pi` renders each stage from `run_args` only
   (nothing passes a prior stage's return onward). Chose option (a): a repeated
   stage whose manifest carries `chained_from: <label>` renders with the PRIOR
   stage's validated return for the SAME repeat key merged into its prompt
   context, so its prompt can name the finding's schema fields directly
   (`{answer}`, `{still_live}`, ...). `_run_stage_pi` now returns `(rc, value)`;
   `run_workflow` keeps `prior_by_key[(base_label, repeat_key)]` and threads it.
   Documented in `render_stage_prompt` docstring and the manifest convention.

3. **register refuses** (hypothesis req (3), "remove or refuse naming author").
   Deriving a manifest from an inline script's labels can only fabricate
   `prompts`, which `validate` now rejects — so register refuses and names
   `workflow.py author`, landing nothing (no half-written pair).

4. **validate strictly stronger** — a manifest stage whose `prompt` contains
   `<TODO` is now a violation ("a manifest carrying a `<TODO` prompt should now
   be a validate violation, which is what makes DISPROVED-BY checkable by the
   registry itself"). No existing invariant weakened.

5. **Rewrote prime-open-questions through the verb** — the old 4-stage
   register-skeleton (all `<TODO` prompts, `.js` whose 4 stage prompts were
   literally `<TODO: author the stage prompt for stage '...'>`, so the pair
   could NOT run on pi) is now ONE repeated `investigate` stage over the
   `questions` args list PLUS ONE repeated `refute` stage (`chained_from:
   investigate`), both with real prompts + real schemas. Stage list authored via
   `workflow.py author prime-open-questions --stages /tmp/poq-stages.json`.

**What happened** — both dry-runs resolve all SIX expanded stages (3
investigate + 3 refute) with non-`<TODO` prompts; `node --check` on the
generated `.js` passes; the authored pair is a sound registry; all 33
`test_workflow.py` + the `bin/--help` smoke suite pass. The ONE mechanism to
establish (prior-stage return into a later stage's prompt) is built and
unit-tested by `test_pi_run_chains_investigate_to_refute` (mock subprocess:
investigate finding reaches the refute prompt for the same repeat key) and
`test_author_lands_runnable_pair_dictated_by_manifest`.

## Evidence

```
$ workflow.py author prime-open-questions --stages /tmp/poq-stages.json \
    --note "L4.105 rewrite: one repeated investigate + one repeated refute ..."
[authored] prime-open-questions -> prime-open-questions.json + agi-prime-open-questions.js (2 stage(s), script derived FROM manifest)

$ workflow.py list
NAME                 SCRIPT                 STAGES  HARNESS
prime-open-questions agi-prime-open-questions.js 2      pi   (was 4)

$ node --check extensions/agi/workflows/agi-prime-open-questions.js
JS PARSE OK

$ workflow.py run prime-open-questions --harness pi --dry-run --args '{3 original questions}'
[dispatch] investigate:commit-guard :: role=kid model=~deepseek/deepseek-v4-flash-latest effort=medium
[dispatch] investigate:seat-branch :: role=kid model=~deepseek/deepseek-v4-flash-latest effort=medium
[dispatch] investigate:suite-lock :: role=kid model=~deepseek/deepseek-v4-flash-latest effort=medium
[dispatch] refute:commit-guard :: role=kid model=~deepseek/deepseek-v4-flash-latest effort=medium
[dispatch] refute:seat-branch :: role=kid model=~deepseek/deepseek-v4-flash-latest effort=medium
[dispatch] refute:suite-lock :: role=kid model=~deepseek/deepseek-v4-flash-latest effort=medium
[summary] workflow=prime-open-questions harness=pi stages=6

$ workflow.py run prime-open-questions --harness claude-code --dry-run --args '{3 original questions}'
[dispatch] investigate:commit-guard :: role=kid model=sonnet effort=medium   ... 3 more investigate + 3 refute
[summary] workflow=prime-open-questions harness=claude-code stages=6

$ pytest extensions/agi/tests/test_workflow.py extensions/agi/tests/test_bin_help_smoke.py -q
91 passed, 1 skipped
```

`workflow.py validate` on the LIVE tree is now rc=1 — but ONLY for the two
PRE-EXISTING register skeletons I cannot touch (files not in the round
write-set): `l3w-route-probe` (emit, critic) and `l4-plan-research` (map,
draft, judge, verify, synthesize), each flagged as "carries a `<TODO` prompt
placeholder — a non-runnable skeleton; author a real prompt with
`workflow.py author`". Their `review`/`drafting`/`deep-search`/authored
`prime-open-questions` peers all pass. The authored pair alone validates
sound (rc=0). This is the intended honesty: the register that used to land
`<TODO` skeletons can no longer (it refuses), and validate now triages
runnable from non-runnable at the registry itself — the exact DISPROVED-BY
check. Both flagged skeletons are prior-art register output (predate this
round), not "registered pairs after this round".

**register refusal (item 3), verbatim stderr:**
`workflow.py: register refused: deriving a stage manifest from an inline script
only fabricates 'prompts', which validate now rejects as <TODO> non-runnable
skeletons. Author a REAL runnable pair instead: 'workflow.py author <key>
--stages <json-or-path>'`

**SKILL.md staleness (prime lands the governing-edit, per brief; I quote,
I do not touch):**
- Line 61: `| bin/workflow.py register <name> --script <path> [--from-run <dir>] | Land an inline script as a registered manifest pair as it runs |`
- Line 68: "...**Register it as it runs** — `workflow.py register <name>
  --script <path>` lands an inline script as a proper `agi-<name>.js` +
  `<name>.json` pair in the same action that runs it ..."
- Recommended replacement wording (for the prime, not landed here):
  *L61*: `| bin/workflow.py author <name> --stages <json|path|stdin> | Write BOTH halves of a runnable pair: <name>.json + agi-<name>.js derived FROM it |`
  *L68*: "**Author it, don't register it** — `workflow.py author <name>
  --stages <path>` writes a real `<name>.json` (real prompts) + `agi-<name>.js`
  generated from it in one action; `register` refuses because it can only
  fabricate `<TODO>` prompt skeletons, which `validate` now rejects as
  non-runnable. A workflow with no authored pair is the failure this closes.
  Dispatch every workflow through `workflow.py run <name>`, the one sanctioned
  route. `review`, `drafting` and `prime-open-questions` are the working
  reference pairs."

**One unexpected artifact to report (left where it is):** a real pi run leaked
once during my first (un-mocked) chain test before I added `mock.patch` — it
vanished from the mock branch and wrote nothing tracked; `.agi/sessions/workflows/review.jsonl`
exists from an earlier review run but is gitignored runtime data, not part of
this round.

## Agent Notes
author verb lands: one action writes manifest+derived Workflow .js; register refuses naming author; validate flags <TODO as violation; pi chaining (chained_from) established+tests; prime-open-questions rewritten to one investigate+one refute, both dry-runs resolve 6 stages non-TODO

DIRECTOR HARVEST REVIEW (sanctuary-director gen VII, L4.105) — ACCEPTED at inconclusive_lean_proved:80, verified in the BYTES after the parent STALLED (L4.75: killed the pi pid, swept twice, committed the staged work under the round's authorship, circumstances in the commit d58086df9). Verified: author_workflow verb writes manifest+derived .js in one action; validate now rejects <TODO skeletons (workflow.py:282/290); prime-open-questions rewritten to one investigate + one refute (0 TODO), both --harness dry-runs resolve; the generated agi-prime-open-questions.js is a genuine Workflow script (meta/phase/agent/pipeline, pipeline labels investigate:/refute:) — meets the owner's native-tooling constraint; pi chaining via chained_from with tests; register refuses naming the author verb; test_workflow.py 33 passed. RESIDUE, separate and NON-BLOCKING: the stricter validate flags the PRE-EXISTING l4-plan-research.json <TODO stages (10 TODO on season/s2 before this round). NOT L4.105's scope, and NO gate runs live validate (test_workflow validates a tmp fixture dir at :305; commands.py verify does not call it) — so it does not break the suite or verify. A later round should author l4-plan-research's prompts via the new author verb; until then `workflow.py validate` on the LIVE registry reports 7 violations by design.
