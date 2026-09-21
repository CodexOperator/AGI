---
id: experiment:a00-9dc1a053-g731-spine-audit
mint_id: 2a88f762a9d54a32b4ada56a0b5d5b30
type: experiment
parents:
  - hypothesis:a00-9dc1a053-838077
next_edges: []
confidence: 0.88
deliverables:
  - .agi/nodes/experiment/a00-9dc1a053-g731-spine-audit.md
  - .agi/nodes/hypothesis/a00-9dc1a053-838077.md
edited_by: a00-9dc1a053
evidence_runs:
  - experiment:a00-9dc1a053-g731-spine-audit
line_ceiling: 40
loop: goal:g7.31@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "a", "class": "gate", "cmd": "ls -1 .agi/nodes/goal/g7.31*.md | wc -l; for f in .agi/nodes/goal/g7.31*.md; do grep -c '^## Falsifier' $f; done", "expected": "10 node files; every file reports 1", "observed": "10; all ten report 1", "result": "held"}
  - {"conjunct": "b", "class": "wire", "cmd": "grep -inE grok extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py; git diff --numstat 93493be32..HEAD -- extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py", "expected": "grep exit 1 with zero lines; numstat empty", "observed": "grep exit 1, zero lines; numstat empty", "result": "held"}
  - {"conjunct": "c", "class": "wire", "cmd": "grep -nE 'adapters.resolve|adapters.load|adapter.build_command' extensions/agi/bin/dispatch.py; grep -nE 'harness_template.render|if harness ==' extensions/agi/bin/rotate.py", "expected": "one adapter seam; one render seam; zero if-harness branches", "observed": "dispatch 861/1076/1301/1883/1904/2003/2458/4104; rotate 904/1027/1045; zero if-harness", "result": "held"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 0f4115aa71b8c442
season: 2
testable_claim: "The goal:g7.31 umbrella falsifier holds on 93493be32: exactly 10 g7.31*.md goal nodes each with one ## Falsifier; zero grok hits in dispatch.py/rotate.py with zero bytes changed there; the argv seam is one adapters.resolve/load + adapter.build_command in dispatch.py and one harness_template.render in rotate.py with no if-harness branch."
title: "g7.31 umbrella spine audit on tip 93493be32: 10 nodes, zero grok special-case, one render seam (live re-run)"
town: core
verdict: inconclusive_lean_proved:88
---
<!-- BODY:BEGIN -->
# experiment:a00-9dc1a053-g731-spine-audit

## Experiment

Live umbrella-spine audit of `goal:g7.31` at season2 tip `93493be32`
(worktree `/data/work/agi/.agi/worktrees/a00-9dc1a053`). This re-runs the audit
authored by `a00-d7f8e704`, whose experiment node was left untracked and so was
excluded from its own done commit; this round lands the evidence chain under a
slug that carries its own agent id. Audit only — no source bytes touched, no
grok binary needed.

### (a) structural completeness — count + one Falsifier per node

```
$ ls -1 .agi/nodes/goal/g7.31*.md | wc -l
10
$ for f in .agi/nodes/goal/g7.31*.md; do echo -n "$f "; grep -c "^## Falsifier" "$f"; done
.agi/nodes/goal/g7.31.1.1.md 1
.agi/nodes/goal/g7.31.1.2.md 1
.agi/nodes/goal/g7.31.1.md 1
.agi/nodes/goal/g7.31.2.md 1
.agi/nodes/goal/g7.31.3.1.md 1
.agi/nodes/goal/g7.31.3.2.md 1
.agi/nodes/goal/g7.31.3.md 1
.agi/nodes/goal/g7.31.4.md 1
.agi/nodes/goal/g7.31.5.md 1
.agi/nodes/goal/g7.31.md 1
```

10 nodes (umbrella + 9 descendants); each carries exactly one `## Falsifier`.

### (b) zero grok special-case in the engine seam

```
$ grep -inE 'grok' extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py; echo exit=$?
exit=1
$ git diff --numstat 93493be32..HEAD -- extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py
(empty — zero bytes changed)
```

Zero matching lines on the tip, and the base equals HEAD for both paths, so this
family added no harness special-case.

### (c) the one seam, read not guessed

- `dispatch.py:861` / `:1076` — `_name, harness = adapters.resolve(cfg)`;
  `:1883` / `:1904` resolve the dispatch harness; `:2003` —
  `adapter = adapters.load(dispatch_harness["adapter"])`.
- `dispatch.py:1301` (dry-run mirror) / `:2458` (live spawn) —
  `adapter.build_command(...)`. The argv is built by the adapter, never inlined.
- `rotate.py:1032-1045` — `_build_harness_command` is the ONE seam:
  `return harness_template.render(harness or "claude-code", ...)`, docstring
  *"There is no `if harness == \"...\"` branch here"*.
- `grep -nE 'def _build|grok' rotate.py` → only `_build_claude_command:896`,
  `_build_copilot_command:1014`, `_build_harness_command:1032` — **no grok
  builder**, and `grep -nE 'if harness =='` is empty.

### F2 — leaf falsifier concreteness (umbrella falsifier condition 2)

8 of 9 leaves name an exact command or artifact. The exception is
`g7.31.3.2.md`: *"goes through the named CLIs, not a parallel script
(transcript/experiment proof)"* — no exact command or assertion named. That one
leaf falsifier reads as vibes, so the umbrella claim is a lean, not proved.

### Divergence from the dispatch orders (loudly)

The order to mint the experiment with `--parent goal:g7.31` was **refused by the
spawn gate**: `experiment may not be parented by 'goal' (allowed: build,
experiment, hypothesis, idea, task, verdict)`. The experiment is therefore
parented under this round's scaffold hypothesis (`hypothesis` → `experiment`),
which is the legal chain shape. `--no-spawn-gate` was NOT used.

## Evidence

Raw command transcript: `.agi/sessions/iter-DT.01/a00-9dc1a053/evidence.txt`.
Bodies read: `.agi/nodes/goal/g7.31*.md` (10 files). No production lines
changed (`git diff --numstat 93493be32..HEAD -- extensions/agi/bin/dispatch.py
extensions/agi/bin/rotate.py extensions/agi/bin/adapters/` is empty).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Re-runs a00-d7f8e704 audit live and lands its dangling evidence under an agent-id slug; diverges from orders by reparenting the experiment under the scaffold hypothesis because the spawn gate refuses goal-parented experiments.
<!-- THOUGHT:END -->

## Agent Notes
Live re-run of the g7.31 umbrella spine audit on tip 93493be32: (a) 10 nodes each with one Falsifier; (b) zero grok hits and empty numstat in dispatch.py/rotate.py; (c) one adapters.resolve/load+build_command seam and one harness_template.render seam, no if-harness branch. Lean because g7.31.3.2 names no exact command.
