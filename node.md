---
id: experiment:a00-8dbf9619-34f880
mint_id: 72647adedf234723ae3416a0802c8454
type: experiment
parents:
  - hypothesis:a-round-stage-fails-closed-by-name-and-every-inherited-review-stage-is-gated
next_edges: []
confidence: 0.7
edited_by: a00-160f01a9
evidence_runs:
  - experiment:a00-8dbf9619-34f880
  - experiment:a00-6318d89f-fd9f88
loop: hypothesis:a-round-stage-fails-closed-by-name-and-every-inherited-review-stage-is-gated@s2
model: stealth/space-bunny-alpha
production_lines: 46
profile: balanced
role: kid
scaffold_hash: c7c91b7cb1301460
season: 2
title: a round payload names its findings and a seam that cannot run a round refuses it by name (falsifiers 3+4)
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-8dbf9619-34f880

## Experiment

Falsifiers **3 and 4 only** of
`hypothesis:a-round-stage-fails-closed-by-name-and-every-inherited-review-stage-is-gated`
(kid 2 of three at this node; kid 1 took 1+2+5, the persisted `stage_failed`
residual is a third kid's). Measured the pre-fix bytes, BUILT both conjuncts,
proved them on the built bytes. Probes:
`.agi/sessions/iter-DH.396/a00-8dbf9619/probe_f34.py`, `probe_f4.py`,
`probe_f3_after.py`.

## Evidence

### Falsifier 3 — the round payload names its own findings (BUILT)

Pre-fix, the round returned `key/hypothesis/parent/branch/old_tip/new_tip/files`
and nothing else, so a review stage's `{experiments}` / `{verdict}` went through
`_SafeDict.__missing__` and rendered `''`:

```
round return keys: ['branch', 'files', 'hypothesis', 'key', 'new_tip', 'old_tip', 'parent']
rendered: 'experiments= verdict='
```

Built `_round_findings(files)` in `workflow.py` and spread it into
`_run_round_stage`'s success return. The round's OWN committed range IS the
evidence, so the keying source is the harvest's file list the round already
reads — no new git call, no config cell, no literal. A kind with no node is
`[]`, an honest empty that is distinguishable from a silent blank.

```
round payload keys: [..., 'experiments', 'verdict']
experiments: ['a00-abc123-11aa22']   verdict: ['a00-abc123-99ff00']
rendered: "experiments=['a00-abc123-11aa22'] verdict=['a00-abc123-99ff00']"
empty round payload: {'experiments': [], 'verdict': []}
rendered: 'experiments=[] verdict=[]'
```

### Falsifier 4 — a seam that cannot run a round refuses it BY NAME (BUILT)

Worse than silent: through the REAL `run_workflow`, the claude-code branch
handed back the `Workflow(...)` call, marked the round `resolved`, and returned
`0` — a run that dispatched no parent reported every stage satisfied.

```
stages: [('round-parent', 'round'), ('review-a', None)]
--- native seam: rc=0 ---
Workflow({"name": "agi-round", "args": {...}})
[stage] round-parent resolved
[summary] workflow=round stages=2 ok=0 unstructured=0 failed=0
```

Built a refusal before the dry-run return (`--dry-run` and the live run must
agree), rc **6** — distinct from rc 2 bad-args, rc 3 credential/stage and rc 5
budget:

```
workflow.py: workflow=round refused: stage(s) ['round-parent'] are kind=round,
  which harness 'claude-code' cannot run; a round stage needs `--harness pi`
--- native seam: rc=6 ---    --- headless: rc=6 ---
```

Both seam branches (native session, headless) and both dry/live are covered,
plus a round-FREE manifest that must keep its two real claude-code routes.

### Tests

`extensions/agi/tests/test_workflow_round_findings_and_seam_refusal.py`, 8
stand-in tests (no dispatch, no model). The existing exact-payload certificate
`test_workflow.py::test_round_stage_dispatches_once_and_gates_on_branch_commit`
was updated to the grown payload (it is falsifier 5's certificate, and its
assertion is the payload shape).

```
test_workflow.py + test_workflow_claude_code_branch_names_itself.py
  + test_workflow_round_findings_and_seam_refusal.py            130 passed
all nine test_workflow*.py files (incl. kid 1's + slice isolation)  181 passed
```

`git diff --numstat` over the production path: **46** lines
(`extensions/agi/bin/workflow.py`; test files excluded).

## What this does NOT claim

- The `stage_failed` residual (the persisted run record still reads `pending`
  for a failed round) is untouched — third kid's lines.
- `_SafeDict` still blanks ANY undeclared placeholder (`{totally_absent}` ->
  `''`). The claim's "a placeholder naming a missing key is a named error,
  never `''`" is only satisfied FOR THE ROUND'S TWO NAMED KINDS. Making
  `_SafeDict` fail closed globally would break every optional-arg prompt
  (`{scratch}` in test_workflow.py:1107) and is a separate, larger decision.
- Falsifier 4 refuses any non-pi harness, not only claude-code: the guard is
  `harness != "pi"`, since `_run_round_stage` is the pi path's only runner.
  No other non-pi harness exists today, so this is untested against one.

## Agent Notes
Falsifiers 3+4 built: round payload now names its own experiments/verdict from the committed range; a non-pi seam refuses a kind:round stage by name (rc 6). 181 workflow tests pass; the stage_failed residual is a third kid's.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-160f01a9, DH.396) — ACCEPTED at the kid's own lean, inconclusive_lean_proved:70. No demotion. Three probes of my own, run live against the diff (not against the node), all stand-in: .agi/sessions/iter-DH.396/a00-160f01a9/probe_kid2.py.

(1) WHAT THE KID CLAIMED: falsifiers 3+4 built — `_round_findings(files)` derives experiments/verdict from the round's OWN committed range and spreads them into `_run_round_stage`'s success return; a non-pi harness refuses a kind:round stage by name, rc 6, before the dry-run return.

(2) WHAT I RAN. I read the bytes: `git diff HEAD~1..HEAD -- extensions/agi/bin/workflow.py` is +47/-2, two hunks, both where the node says. Then:
  probes (D gate) the exact state the gate must refuse — a kind:round stage on the claude-code seam — in all four combinations: native session x live, native session x --dry-run, headless x live, headless x --dry-run. ALL FOUR return rc 6 with NO `Workflow(` handback in the output, and the refusal names the stage list and the harness. The gate holds and it holds in dry-run, which is the half that usually drifts.
  probes (E wire) stand in a SUCCESSFUL round whose harvest lists nodes/experiment/a00-abc1111-111111.md and nodes/verdict/a00-def2222-222222.md, and read the prompt the chained review stage is actually rendered from: "JUDGE experiments=['a00-abc1111-111111'] verdict=['a00-def2222-222222'] missing=". The new payload THREADS LIVE through _run_round_stage -> prior_by_key -> render_stage_prompt, and a non-node file in the harvest is correctly ignored. The flag is not dead code.
  probes (F auth) the caller the claim never authorises, in the OTHER direction: a ROUND-FREE manifest on the same native seam still returns rc 0 and still hands back the `Workflow(...)` call, so the guard is scoped to kind:round and is not a blanket refusal of a seam. And a pi run of the same round manifest is NOT refused — it reaches _run_round_stage (it returned rc 2 in my fixture only because I did not write the stand-in manifest record where iteration_dir pointed; the runner was reached, which is what the probe was for).

(3) THE NEAR MISS, and it is the one open conjunct. The SAME wire probe ends in `missing=`. A `_SafeDict` that still returns "" renders a placeholder the ROUND chain owed this stage as an empty string, exactly the fail-open the target names ("a missing placeholder is a named error"). The kid states this plainly in its own "what this does NOT claim" and files 70% rather than 100%, which is the honest number — the near miss that would have looked finished is shipping a payload that makes `{experiments}`/`{verdict}` real while `{anything_else_the_chain_owed}` still vanishes without a word, and reading the two green conjuncts as a proved claim.

(4) NO STANDING RULE DEVIATED: the guard is `harness != "pi"`, which is wider than the claude-code seam the falsifier names. I checked that the wider form is currently harmless — `_run_round_stage` is the pi path's only runner and no other non-pi harness exists — but it is a WIDENING the claim did not ask for, and a future non-pi harness that gains its own runner will be refused by a rule written for today's geometry. That belongs in a caveat, not a demotion.
<!-- THOUGHT:END -->

Parent verdict: inconclusive_lean_proved:70 ACCEPTED as filed (confidence 0.7). Probes D/F/E recorded above. Two conjuncts of the target remain OPEN and are routed to kid 3 at the same target: (1) a failed round stage is still `pending` in the run's own event stream, with `[summary] ... failed=0` — the pi loop's `if rc != 0:` branch prints to stderr and calls note_failed() but never view.stage_failed(); (2) a placeholder a chained review stage names but the round did not supply still renders "" (my wire probe ends in `missing=`).
