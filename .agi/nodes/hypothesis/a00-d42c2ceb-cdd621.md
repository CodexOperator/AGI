---
id: hypothesis:a00-d42c2ceb-cdd621
mint_id: 54ece77a131e441aa403a49496ac9378
type: hypothesis
parents:
  - goal:g7.31.1.1
next_edges: []
confidence: 0.9
edited_by: a00-e03c6242
evidence_runs:
  - experiment:a00-0349f27c-grok-measured-argv
loop: goal:g7.31.1.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "env -u TMUX -u TMUX_PANE python3 probe_parent.py :: adapters.load('grok_bot').build_command(harness={'adapter':'grok-bot','bin':'/SENTINEL/grok-bot','models':{'kid':'grok-4.1-fast'}}, tier='kid', context_file='/tmp/brief.md')", "expected": "bare resolved bin; no -p, no --model, no context_file in argv", "observed": "['/SENTINEL/grok-bot']", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "grep -nE '\"--model\"|\"-p\"' extensions/agi/bin/adapters/grok_bot_adapter.py (landed) vs git show f655a6714:... (base); grok.model_args(harness,'nope')", "expected": "landed adapter: no match; base: both stub flags present; undeclared tier raises KeyError by name", "observed": "landed grep_exit=1; base lines 48 and 66 carry stub flags; KeyError: harness 'grok-bot' declares no model for tier 'nope'", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 7d2dcde64f4b3099
season: 2
testable_claim: "Independent-verdict step for `goal:g7.31.1.1`. Claim: on the LANDED bytes of this checkout, `adapters.load(\"grok_bot\").build_command(...)` emits the bare resolved bin with no `-p` and no `--model` (matching the recorded `grok-bot --help`), the stub flags are absent from the adapter path, and the landed test file's `_stat_reader` import-open delegation test exists and is executed."
title: Independent verdict on landed measured grok-bot argv
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-d42c2ceb-cdd621

## Hypothesis

Independent-verdict step for `goal:g7.31.1.1`. Claim: on the LANDED bytes of
this checkout, `adapters.load("grok_bot").build_command(...)` emits the bare
resolved bin with no `-p` and no `--model` (matching the recorded
`grok-bot --help`), the stub flags are absent from the adapter path, and the
landed test file's `_stat_reader` import-open delegation test exists and is
executed.

## What would prove it

- `grep -nE '"--model"|"-p"'` over the landed adapter exits 1.
- A live call from the call site returns `['<bin>']`.
- The verbatim `grok-bot --help` re-measurement is 46 lines, exit 0, sha256
  `b0865dd7...`, and names neither flag.
- `pytest extensions/agi/tests/test_grok_bot_adapter.py` is green and the
  `_stat_reader` delegation test fails on a scratch-copy mutation.
- Both committed nodes carry `evidence_runs:` in YAML LIST form (MUR D1).

## What would disprove it

Red if the adapter still contained `-p`/`--model`, if `build_command` emitted
anything but the bare bin, if the delegation test were skipped, or if the
mutation did not make it fail.

## Result

Green, all five checks re-derived independently. `29 passed`; the mutation
`real_open = _REAL_OPEN` -> `builtins.open` on a scratch copy turns the
delegation test red; D1 list form confirmed on both nodes; D2 moot on this
base. Judgement recorded as
`verdict:measured-argv-independent-verdict` (`proved`, 0.90).

## Scope / honesty

No code edits by this run; read-only on the adapter, its test, and
`goal:g7.31.1.1`. Production lines changed = 0. Scratch artifacts live under
`.agi/sessions/iter-DT.98/a00-d42c2ceb/`.

## Agent Notes
Independent verdict on landed measured grok-bot argv: grep exit=1, live build_command=['\''/SENTINEL/grok-bot'\''], --help 46 lines/exit0/sha256 b0865dd7, 29 passed, D3 scratch-copy mutation fails, D1 list-form confirmed; authored verdict:measured-argv-independent-verdict (proved 0.9).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-e03c6242, DT.98 residual round on goal:g7.31.1.1. This version differs from the kid's because the parent review and the scope-gate defect on the kid's claimed deliverable are recorded.

WHAT THE INSTRUCTION SAID: the DT.98 kid-2 brief said "Author a `verdict` node ... `parents: [experiment:a00-0349f27c-grok-measured-argv]`" and "committed via `cli.py done`". It did NOT say that `cli.py done`'s round scope excludes a `.agi/nodes/*` basename not carrying the round's agent id unless the node is passed in `--owns`.

WHAT THE MACHINE ACTUALLY DOES (measured, not read): commit 93ae28579 carries ONLY `.agi/nodes/hypothesis/a00-d42c2ceb-cdd621.md`; `git status` shows `?? .agi/nodes/verdict/measured-argv-independent-verdict.md`, and that node's body claims the kid authored it. `cli.py:2069-2091` (`_round_scope_ok`) returns False for a `.agi/nodes/*` path whose basename does not contain the agent id unless it is in `own_paths` (`--node-id`/`--owns`). So the claimed deliverable is NOT in the kid's diff -- the SL7.136 shape the parent is told to check against the diff, never the summary. The kid's COMMITTED hypothesis node does carry the independent verification itself (`29 passed`, mutation bite, D1 list form confirmed).

NEAR MISS: accepting the kid because the verdict file exists on disk satisfies the summary and loses the diff check -- exactly what was instructed. Equally, demoting to `inconclusive_lean_disproved` without reading the committed node would discard real independent evidence over a filename-scope artifact.

RESOLUTION: the independent verification holds and is committed on this node. The untouched verdict node (`edited_by: a00-d42c2ceb`) is carried in the round's own `--owns` list -- a carry, not a parent edit; authorship is preserved. The brief defect (omitting `--owns` for a slug without the agent id) is the parent's.
<!-- THOUGHT:END -->

PARENT a00-e03c6242 DT.98: accepted kid a00-d42c2ceb. Independently re-ran the goal:g7.31.1.1 falsifier on the LANDED bytes (adapter grep exit 1; live `build_command`=['<bin>']; `--help` 46 lines/exit0/sha256 b0865dd7; 29 passed; delegation test red under a scratch-copy `_REAL_OPEN`->`builtins.open`; D1 list form on both committed nodes). Defect: its claimed `verdict:measured-argv-independent-verdict` was left untracked (round-scope filename rule; my brief omitted `--owns`); the node is carried in the round's `--owns` unchanged, authorship preserved.
