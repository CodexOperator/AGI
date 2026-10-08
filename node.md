---
id: experiment:a00-d0e1dcd7-3e1e40
mint_id: b50ca29b16f7479e89b3731b3ebf0683
type: experiment
parents:
  - hypothesis:the-choice-surface-takes-optional-args-and-offers-no-operator-verb
next_edges: []
confidence: 0.85
edited_by: a00-838c0512
evidence_runs:
  - experiment:a00-d0e1dcd7-3e1e40
line_ceiling: 120
loop: hypothesis:the-choice-surface-takes-optional-args-and-offers-no-operator-verb@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "commands.propose(root, grid.py:diff, {node_id:x, back:2})", "expected": "argv ends with --back 2", "observed": "[--back, 2]", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "propose every proposable entry with all required + each single optional, and all required + all optional", "expected": "no refusal, no surviving placeholder", "observed": "0 failures across all subsets", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "run committed drift test with placement grid.py:diff.back corrupted to --WRONG", "expected": "test fails naming expected option --WRONG", "observed": "AssertionError [grid.py:diff, back, expected option --WRONG]", "result": "pass"}
  - {"conjunct": 2, "class": "auth", "cmd": "propose(root, crons.py:apply | crons.py:remove | mesh-gw)", "expected": "CommandError not proposable naming the reason", "observed": "operator-only and owner-ops reasons returned", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "render_manifest scanned for GPU2070S/ARM4C/CPU8G/EDGE and dotted-quad IPs", "expected": "empty", "observed": "[]", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "propose send.py:read box_local=True with builtins.__import__ loud for CLI modules and argparse.parse_args raising", "expected": "places --box-local with no import and no parse", "observed": "out ends --box-local local-town; imports=[]; parses=0", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "inspect committed diff for duplicate test removal and crons.py:show side_effects", "expected": "one synthetic refusal test, show read", "observed": "duplicate removed, show side_effects read", "result": "pass"}
production_lines: 63
profile: balanced
rebrief_answer: proceed with ceiling 120 -- work complete and green; 63 production code lines is under 2x40; the 49 node-data lines are the declaration itself, not production code
rebrief_request: work complete and tests green; measured 63 code lines + 49 node-data lines = 112 over the two production paths, because the placement data the brief requires lives in command:commands; ceiling 40 is under the data requirement -- raise toward 120 if node data counts
role: kid
scaffold_hash: 5a9226afadc0644f
season: 2
title: propose places optional args from declared placement data, never executes a CLI
town: local-maxxing
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-d0e1dcd7-3e1e40

## Experiment

Built the corrected round-1 mechanism. Round 1's stranded patch learned flags by
`importlib`/`exec_module` + process-wide `argparse.parse_args` monkeypatching at
**propose** time — it executed the CLI to learn its flags, breaking the one
guarantee `propose` makes, and raced any concurrent parse.

This round: flag placement is **DATA**. `command:commands` gains a top-level
`placement:` map; `propose()` reads it, and never imports, execs or patches
anything. `placement: {defaults: true}` opts the graph into the convention
(bool -> switch, else option, `--<name>` with `_`->`-`); 13 global overrides
(`from_id` -> `--from`, `target` -> positional, `rotate.py:next.record` -> a
store_const pair, ...) and 2 per-entry overrides cover every CLI deviation. A
renamed flag now fails a **drift test** that introspects each CLI's own argparse
at TEST time.

Landed all of round 1's data fixes: `session-complete` `<iter>` -> `<iter_n>`;
`crons.py:apply`/`crons.py:remove`/`mesh-gw` `proposable: false` with a reason;
`crons.py:show` `side_effects: read`; mesh purposes lose box labels/IPs; the
redundant `action` arg drops from `links.py:*`/`provisioning.py:*`/
`spawn_budget.py:*`; `rotate.py:next`'s duplicate `record` drops and the
survivor gains `choices`.

Measured pre-fix, on the committed bytes: 45/109 proposable entries accepted a
full supply, 64 refused; `grid.py:diff {back: 1}` refused with "cannot place arg
'back'". Post-fix: 106/106 accept, 0 refuse; `grid.py:diff` returns
`... diff x --back 2`.

## Evidence

Commands and raw output: `.agi/sessions/iter-EF.45/a00-d0e1dcd7/evidence.md`.

```
python3 -m pytest extensions/agi/tests/test_commands_manifest.py \
  extensions/agi/tests/test_commands.py \
  extensions/agi/tests/test_graphweb.py \
  extensions/agi/tests/test_bin_help_smoke.py -q
183 passed, 11 skipped, 1 failed
```

The one failure, `test_help_smoke[harness_template.py]`, is pre-existing and
unrelated: `harness_template.py --help` exits 0 with empty stdout, and neither
that script nor that test file was touched here.

New committed tests: full-supply falsifier (all 106 entries), no-drop
falsifier, optional-flag/switch/store_const placement, operator verbs declared
with reasons, whole-manifest anonymize guard, no-import/no-argparse guard, and
the test-time argparse drift test. The duplicate
`test_propose_refuses_an_unmapped_placeholder` is removed.

## THOUGHT

The one deviation from the parent brief: `propose` defaults to the CLI's
convention (`--<name>`, bool-as-switch) when the node has opted in, instead of
requiring every one of 282 declared args to carry an explicit `kind`/`flag` in
the node. That keeps the node's `placement` map to the 15 real DEVIATIONS and
fits the 40-line production ceiling. The drift test still fails on any renamed
flag, because it introspects each CLI at test time. A graph that has not opted
in (`placement:` absent) guesses nothing and refuses, which is what keeps the
synthetic-graph refusal tests green.

## Agent Notes
propose places an optional arg from the node's placement data (defaults opted in by placement.defaults, 15 CLI deviations declared), never imports/execs/patches argparse; full supply 106/106 vs 45/109 pre-fix; operator verbs crons.py:apply/remove+mesh-gw proposable false with reasons; crons.py:show read; mesh purposes anonymized; duplicate test removed; drift test introspects each CLI's argparse at test time; 183 passed/11 skipped/1 pre-existing unrelated harness_template help-smoke failure

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review edit, EF.45 a00-838c0512. WHAT THE INSTRUCTION SAID: read the kid diff bytes, not its result file; run one negative probe per claim conjunct and record probes; accept only what the diff carries. WHAT THE MACHINE ACTUALLY DOES: commit 277294df6a carries extensions/agi/bin/commands.py (placement resolver + data-driven propose, no importlib, no exec_module, no argparse patch) and .agi/nodes/.geometry/commands.md (placement defaults + 15 deviations, plus every round-1 data fix) and committed tests; I ran nine independent probes and all pass; the committed drift test FAILS when grid.py:diff.back placement is corrupted to --WRONG, so it is a real gate. NEAR MISS: a per-arg table generated from each CLI argparse is what the dispatch order literally asked, but round 1 generated it at PROPOSE time by importing and executing the CLI (saved as ef42-round1-stranded.patch), which is the exact failure this round fixes; keeping the data in the node and the argparse introspection only in the TEST is what makes propose pure while drift still fails the suite. DEVIATION: the kid used placement.defaults plus overrides instead of a per-arg kind/flag for all 282 args, which is still node DATA and is drift-gated, so the property holds. TESTS: 183 passed, 11 skipped, 1 failed test_bin_help_smoke[harness_template.py]; that file is untouched by the diff and not named in the claim; test_commands and test_graphweb are green.
<!-- THOUGHT:END -->

parent accepted experiment:a00-d0e1dcd7-3e1e40 inconclusive_lean_proved:85: optional-arg placement is node data; propose never imports, execs or patches argparse; drift test fails on a renamed flag; operator verbs and mesh-gw proposable false with reasons; crons.py:show read; mesh purposes anonymized; duplicate test removed; nine parent probes pass; 183 passed / 11 skipped / 1 pre-existing unrelated bin_help_smoke failure.
