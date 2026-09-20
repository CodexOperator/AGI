---
id: verdict:a00-3d540aa5-seam-verdict
mint_id: fa3eefe7954b49d1a7d26695d870ee8e
type: verdict
parents:
  - experiment:a00-3d540aa5-seam-exp
next_edges: []
confidence: 0.8
evidence_runs:
  - experiment:a00-3d540aa5-seam-exp
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "grep -Ein grok .agi/nodes/goal/g17.14.2.md", "expected": ">=1 line, the control file contains grok", "observed": "3 lines, exit 0", "result": "detected"}
  - {"conjunct": 2, "class": "auth", "cmd": "python3 -c \"adapters.resolve(cfg, .grok-bot.)\"", "expected": "AdapterError naming grok-bot because the harness is not declared", "observed": "AdapterError: no harness .grok-bot. in config; declared: [.claude-code., .copilot-cli., .pi., .pi-local.]", "result": "refused"}
  - {"conjunct": 3, "class": "wire", "cmd": "python3 -c \"adapters.load(.grok_bot.)\"", "expected": "AdapterError naming the expected adapter path from live module resolution", "observed": "AdapterError: no adapter for harness .grok_bot.: expected .../bin/adapters/grok_bot_adapter.py", "result": "refused"}
profile: balanced
push_further: "on a branch where harnesses.grok-bot IS present (helper-cfg-land), exercise the well-formedness branch: adapter==grok_bot, bin==DEFAULT_BIN, resolve succeeds"
role: kid
season: 2
title: "grok-bot seam holds merge-invariant on this branch: zero grok in dispatch.py and shipped adapters, config row absent and refused by name"
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# verdict:a00-3d540aa5-seam-verdict

## Verdict

`inconclusive_lean_proved:80`

## Evidence

Judging `hypothesis:a00-3d540aa5-fa98ee` against its single backing run,
`experiment:a00-3d540aa5-seam-exp`, whose transcript is
`.agi/sessions/iter-DT.15/a00-3d540aa5/measure.txt`.

**Conjunct 1 — dispatch.py carries no grok literal.** MEASURED.
`grep -Ein grok extensions/agi/bin/dispatch.py` -> 0 lines, exit 1.

**Conjunct 2 — no shipped adapter carries a grok literal.** MEASURED.
One grep across `pi_adapter.py`, `claude_code_adapter.py`,
`copilot_cli_adapter.py` -> 0 lines, exit 1.

**Conjunct 3 — the config row belongs to the subgoal, not the seam.** MEASURED
on this branch, and this is the residue-3 fix: `harnesses` here declares
`['claude-code','copilot-cli','pi','pi-local']`; `harnesses.grok-bot` is
**absent**, and `adapters.resolve(cfg, "grok-bot")` refuses **by name** with
`AdapterError: no harness 'grok-bot' in config; declared: [...]`. The
hypothesis does not assert the row is present, so nothing here contradicts it.
The disproof condition — a grok literal in dispatch.py or a shipped adapter,
or a malformed present row — is not observed.

**Why not `proved`.** The well-formedness half of conjunct 3
(`adapter == "grok_bot"`, `bin == /home/ubuntu/.npm-global/bin/grok-bot`,
resolve succeeds) is a conditional on a row that is absent on this branch, so
it was not exercised. Every conjunct that can be measured here is, but one
branch of one conjunct is untested, and the honest ceiling is a lean.

**Negative control.** The same grep against `.agi/nodes/goal/g17.14.2.md`
hits 3 lines (exit 0), so the two zeros above are live measurements, not a
dead pattern.

## Supersession

`hypothesis:a00-bfd0d94a-d67716` (the false P7, seam gate asserting a config
row absent from this merge target) is superseded by
`hypothesis:a00-3d540aa5-fa98ee` via a machine-readable `supersedes:` edge in
that node's frontmatter — residue 5 cleared with an in-tree edge, not prose.
The superseded node stays live on
`season2/loops/goal-g17.14.2-helper-cfg-land` (`76d141786`) and
`season2/loops/goal-g17.14.1-a00-597f6b8f`.

## What this means for the MUR

The chain is committed in-tree (`hypothesis` + `experiment` + this `verdict`,
all basenames carrying agent id `a00-3d540aa5`), `evidence_runs` names a node
that resolves on the branch, and no file outside `.agi/nodes/**` changed.
The merge-invariant rewording is what lets the claim hold on
`core/season2/main` without the config row being present.

## Agent Notes
Merge-invariant seam verdict: 0 grok hits in dispatch.py and the three shipped adapters, harnesses.grok-bot absent on this branch and adapters.resolve refuses by name; supersession edge to hypothesis:a00-bfd0d94a-d67716 set in frontmatter. Lean not proved because the row-present well-formedness branch is unexercised.

## Agent Notes
merge-invariant seam chain under goal:g17.14.2: 0 grok hits in dispatch.py and the 3 shipped adapters (exit 1), harnesses.grok-bot absent on this branch and adapters.resolve refuses by name, supersedes edge to hypothesis:a00-bfd0d94a-d67716; lean 80 because the row-present well-formedness branch is unexercised
