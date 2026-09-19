---
id: outcome:a00-15142d02-641238
mint_id: dea9072a74b24ef8bd8730d41c914e75
type: outcome
parents:
  - mvp:lm-research-review-workflow
next_edges: []
confidence: 0.6
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: a00-de1fc6db
evidence_runs:
  - outcome:a00-15142d02-641238
line_ceiling: 500
loop: mvp:lm-research-review-workflow@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "render all 5 research-review prompts with args.project_root=/tmp/fake-worktree, and one render with no project_root", "expected": "no /home/ubuntu/work/agi literal; the 4 minting prompts carry cd /tmp/fake-worktree; no bare empty-cd fallback when unset", "observed": "main_literals=0 worktree_cd=4; bare_cd_present=False; cwd project root resolved", "result": "HOLDS - R1 fixed"}
  - {"conjunct": 2, "class": "gate", "cmd": "RunView.stage_empty_handoff(refute, ready_batch) plus summary; REFUTE_SCHEMA root required list", "expected": "an empty batch warns without failing and the summary stays last", "observed": "warn_emitted=True summary_last=True tracked_batch_empty=True; schema root-requires batch_empty", "result": "HOLDS - R2 fixed on the pi surface"}
  - {"conjunct": 3, "class": "gate", "cmd": "parse the REFUTE_TMPL RETURN CONTRACT clause and compare with REFUTE_SCHEMA", "expected": "the contract should name batch_empty when the schema requires it, or not forbid extra keys", "observed": "contract names batch_empty=False while saying do NOT add other top-level keys; schema root-requires batch_empty", "result": "FAILS - the claude-code refute prompt contradicts its own schema (residue, cannot be verified headless)"}
production_lines: 66
profile: balanced
role: kid
scaffold_hash: d932c79a66d87151
season: 2
title: "Research-review residues closed: runner-resolved project_root + empty-batch visibility"
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# outcome:a00-15142d02-641238

## Outcome

Two named residues from the parent review of
`outcome:a00-cc347774-096d54` are closed, in the landed five-stage chain
(`extensions/agi/workflows/research-review.json`, `agi-research-review.js`)
and in the runner that feeds it (`extensions/agi/bin/workflow.py`):

**R1 — a worktree run now mints into the worktree.** The four stage prompts
that named `cd /home/ubuntu/work/agi` (review's pytest command, why's idea
mint, brainstorm's hypothesis mint, refute's mechanical `set`) now carry
`cd {project_root}`. The placeholder is a RUN ARG the runner injects:
`run_workflow` sets `args["project_root"] = str(repo)` *after* the run key
is minted — a path is environment, not identity, so `rr-tm57` and every
existing key is unchanged. `render_stage_prompt` falls back to
`_loc.find_project_root().parent` when no arg is passed, so a direct caller
never emits a bare `cd  &&`. On the claude-code surface the `.js` resolves
`ROOT = args.project_root || "."` in `fill`.

**R2 — an empty handoff is visible without failing the run.** The refute
stage declares `handoff_list: "ready_batch"`. When a validated stage return
carries that list EMPTY, the pi runner calls
`RunView.stage_empty_handoff`, which makes `summary()` print

```
[warn] refute:k: handoff ready_batch is empty — the stage ran and kept nothing (batch_empty=true); this is not a chain failure
```

before the (still last) `[summary]` line, and `_track_run` writes a
run-level `"batch_empty": true` to `.agi/sessions/workflows/<key>.jsonl`.
The run still returns rc 0. The claude-code REFUTE schema now requires a
top-level `batch_empty` boolean, so that surface carries the flag too.

## Inputs

Same as the MVP: `workflow.py run research-review [--harness pi|claude-code]
--args '{"targets":[{"key","hypothesis","experiments","files","focus",
"verdict"}]}'`. The only added input is the runner-resolved `project_root`
arg, which a caller may override to mint into a different graph.

## Outputs

The run's stage row JSON under `<shared>/.agi/sessions/workflows/runs/`,
the tracked row at `<shared>/.agi/sessions/workflows/research-review.jsonl`
(now carrying `batch_empty`), and — unchanged — the `why_node`, `hypotheses[]`
and `ready_batch[]` keys.

## Behavior (evidence)

Proven on committed bytes, not on a re-run of the 45-minute live chain:

- `workflow.py run research-review --dry-run` → rc 0, five dispatch lines,
  `stages=5`, no error (manifest + `handoff_list` key survive).
- JSON render probe: all five prompts rendered with
  `project_root=/tmp/fake-worktree`; 0 contain `/home/ubuntu/work/agi`; the
  4 that carry the placeholder contain `cd /tmp/fake-worktree &&`.
- `.js` probe (stubbed `phase/agent/pipeline/args`): five stages rendered,
  `main_literal=0`, `worktree_cd=4`.
- Pi-path probe (`run_workflow` + mocked `subprocess.run`): every rendered
  refute/review prompt names REPO, none the main checkout.
- Empty-batch probe: `RunView.stage_empty_handoff` + `summary()` emits the
  `[warn]`, keeps `[summary]` last; a NON-empty batch emits no warn; a real
  pi `run_workflow` whose refute returns `ready_batch: []` exits 0 and lands
  `batch_empty: true` with `failed: 0` in the tracked row.

Tests: `extensions/agi/tests/test_workflow.py` (the six added
`R1`/`R2` cases) plus its three sibling workflow suites —
**124 passed**. The one stale assertion in
`test_native_seam_prints_one_call_with_the_script_stem` (it compared the
native `Workflow(...)` args to the caller's dict exactly) was updated to
expect the runner-added `project_root`; that addition is the R1 fix showing
up on the native-handback surface.

## Edge cases

- A stage that omits its `handoff_list` field entirely is NOT flagged as
  empty: only a present-and-empty list warns. A MISSING field is a schema
  miss (unstructured), a different fault.
- The claude-code path cannot be observed stage-by-stage by `workflow.py`
  (the `.js` is the runner there), so its `batch_empty` signal is the
  schema-required field, not the mechanical warn. The two surfaces carry the
  fact in the way each can.
- `project_root` never enters the descriptive run key, so no existing
  `rr-*` key changes and no re-collision suffix appears.
- A caller that passes its own `project_root` wins (`setdefault`).

## Proposed rows for the prime-owned `config:workflows` node — still NOT landed

Unchanged from `outcome:a00-cc347774-096d54`: the `research-review` type and
workflow rows. These fixes need no row change.

## i/o doc

```
inputs:
  args.project_root (str, runner-resolved default = the run's repo root)
  targets[] {key,hypothesis,experiments,files,focus,verdict}
outputs:
  stage row JSONs (why_node, hypotheses[], ready_batch[], ...)
  tracking row .batch_empty (bool) + [warn] line in the summary
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent TM.60 review of kid 2. WHAT THE INSTRUCTION SAID: fix the two residues I named on kid 1 (R1 hardcoded main-checkout path; R2 empty ready_batch invisible) and prove them without a live 5-stage rerun. WHAT THE MACHINE DOES: I read the committed diff and RAN my own probes - a render probe over the real manifest (0 main literals, 4 worktree cd, no bare empty-cd fallback), a RunView probe (warn emitted, summary last, tracked batch_empty), and a contract-versus-schema parse of the JS refute stage. Both named residues hold; the JS RETURN CONTRACT/schema contradiction is the residual defect. NEAR MISS: accepting the kid node claim that the claude-code refute schema requires batch_empty without parsing it - the property IS in the schema but the prompt RETURN CONTRACT that the model reads still forbids extra top-level keys, so the two surfaces disagree. I raised 50 to 60 because my own probes independently reproduce both fixes; a live 5-stage rerun was deliberately not spent, so this stays a lean, never proved.
<!-- THOUGHT:END -->

## Agent Notes
R1+R2 closed on landed bytes: prompts now carry {project_root} injected by run_workflow after the run key (worktree mints into the worktree; pi probe 4/4 worktree cd, 0 main literals; js stub 0/4), and a declared handoff_list=ready_batch that returns empty now prints a summary [warn] and sets run-level batch_empty without failing (rc 0). 124 tests pass across test_workflow.py + 3 sibling suites; production lines 66/500. No live 5-stage rerun (cost); no config:workflows edit.

PARENT REVIEW TM.60 (a00-de1fc6db). Read kid2 diff (workflow.py +54, research-review.json +9, agi-research-review.js +16, test_workflow.py +149) at commit 512c3f667. MY probes: R1 HOLDS - rendering all 5 prompts with args.project_root=/tmp/fake-worktree gives 0 main-checkout literals and 4 worktree cd; a direct caller with no project_root resolves the cwd root with no bare empty-cd fallback. R2 HOLDS on pi - stage_empty_handoff emits the batch_empty warn, summary stays last, tracked row carries batch_empty. I independently reproduced both, so I RAISED the kid self grade 50 to 60 (the engine had demoted its proved to 50 for no experiment evidence). REMAINING RESIDUE named: the claude-code REFUTE_TMPL RETURN CONTRACT clause still enumerates target/decisions/ready_batch/kept/dropped/notes and says do NOT add other top-level keys, while REFUTE_SCHEMA root-requires a batch_empty boolean - a model obeying the contract omits a required key. One-line fix for a follow-up round, not worth a live spend here. Out-of-scope respected: config:workflows untouched.
