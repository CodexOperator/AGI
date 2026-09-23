---
id: experiment:a00-0ce1190f-f06cc9
mint_id: c2eb1a75f6924396b4f11484c6d52e65
type: experiment
parents:
  - hypothesis:the-spawned-agents-first-turn-is-the-render
next_edges: []
confidence: 0.85
edited_by: a00-22acfd9e
evidence_runs:
  - experiment:a00-0ce1190f-f06cc9
loop: hypothesis:the-spawned-agents-first-turn-is-the-render@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "import dispatch,adapters,brief; r=dispatch._render_dispatch_brief(root=.agi,tier=kid,role=kid,harness=pi,...); monkeypatch brief.assemble to raise; pi/claude_code/copilot_cli build_command(rendered_brief=r); extract --append-system-prompt[s]/written prompt file", "expected": "the render is carried verbatim as one segment / written prompt for pi+claude_code+copilot_cli and NO second brief.assemble runs; without rendered_brief assemble is called (back-compat)", "observed": "pi: render in argv segments True, exact single-segment match True; claude_code/copilot_cli: render present True with assemble refusing; grok stub accepts; no-kwarg path calls assemble 1x; dry-run RC=0 prints the render (221 lines, begins --- HEAD ---)", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "monkeypatch brief.render to raise brief.FaithRefError('moral:faith ref exploded'); call dispatch._render_dispatch_brief(root=.agi,tier=kid,role=kid,harness=pi,...) capturing stderr; control: raise KeyError", "expected": "FaithRefError is caught, a loud stderr line names 'falling back to brief.assemble', and the return equals the assemble fallback; a non-brief exception still propagates (narrow catch)", "observed": "no propagate True; stderr names fallback True; returned bytes == assemble fallback True; KeyError still propagates True", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "brief.render(role='director'|'prime_director'|'master', extras_text='BODY', project_root=real .agi); control brief.render(role='kid', extras_text=sentinel)", "expected": "each role whose parts lack 'extras' refuses by name (RenderError naming role and extras); kid still lands the extras body", "observed": "director/prime_director/master each refused, role in msg True, 'extras' in msg True; kid lands PROBE-BODY-SENTINEL True", "result": "pass"}
production_lines: 71
profile: balanced
role: kid
scaffold_hash: 4535ab8b033ae264
season: 2
title: Dispatch threads one brief.render into every adapter so the spawned first turn IS the render
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0ce1190f-f06cc9

## Experiment

Built the fix for `hypothesis:the-spawned-agents-first-turn-is-the-render`
(three conjuncts) and proved it on the built bytes.

**1. ONE render, threaded.** `dispatch.py` now computes `_render_dispatch_brief`
ONCE before `build_command` on both the dry-run (`_dry_run_report`) and the live
spawn loop, and passes it as `rendered_brief=`; the live `spawn.json` reuses the
SAME `_brief_text` (no second compute). Every assembling adapter
(`pi_adapter`, `claude_code_adapter`, `copilot_cli_adapter`) grew
`rendered_brief: str | None = None` and, when set, spells `[rendered_brief]`
instead of calling `brief.assemble`; `grok_bot_adapter` (stub) accepts-and-
ignores it. Absent/None keeps the pre-fix assemble path byte-identical.

**2. FaithRefError joins RenderError.** `_render_dispatch_brief` catches
`(_brief.RenderError, _brief.FaithRefError)` and takes the same loud
`brief.assemble` fallback.

**3. extras refuses by name.** `brief.render` raises `RenderError` when
`extras_text is not None` and the role's parts carry no `extras` part, naming
the role and its parts -- an extras body is never silently dropped.

## Evidence

New committed test `extensions/agi/tests/test_dispatch_render_thread.py`
(7 tests). Pre-fix these are RED: no adapter's `build_command` accepted
`rendered_brief` (TypeError), and `render` dropped extras silently. Green now:

- `pytest extensions/agi/tests/test_dispatch_render_thread.py -q` -- 7 passed
- `pytest extensions/agi/tests/test_dispatch.py -q` -- 139 passed
- `pytest test_adapters.py test_claude_code_adapter.py test_copilot_cli_adapter.py test_grok_bot_adapter.py test_harness_dispatch_shapes.py test_dispatch_dry_run.py test_dispatch_render_thread.py -q` -- 169 passed
- `pytest test_brief.py test_brief_render.py -q` -- 176 passed, 1 known-red
  (`test_brief.py::test_g15_rule_with_no_project_root_keeps_the_current_fallback`)

Production lines (added, `git diff --numstat`, tests excluded): 71.

## THOUGHT

(1) Instruction quoted: "the harness adapters' build_command ... take the
rendered text instead of calling brief.assemble a second time, so the spawned
agent's first turn equals the dry-run report and spawn.json byte for byte."

(2) What the machine does: `pi_adapter.build_command` passes
`segs=[rendered_brief]` to `_append_prompt_args`; `claude_code_adapter` and
`copilot_cli_adapter` pass `segments=[rendered_brief]` to `write_system_prompt`
/ `write_prompt`; `dispatch.py` passes the one `_render_dispatch_brief` string
to all of them and records the SAME string in `spawn.json`. Cited to
`extensions/agi/tests/test_dispatch_render_thread.py`, which captures the argv
and the written prompt and asserts the render is carried verbatim.

(3) Near miss: adding a `rendered_brief` kwarg every adapter ACCEPTS and
IGNORES satisfies "takes the rendered text" on paper and leaves
`brief.assemble` as the real source. The test's `_refuse_assemble`
monkeypatch makes that fail loudly: an adapter handed a render must not call
`brief.assemble`.

(4) Deviation: the dry report's `_compact` truncates the now-SINGLE argv brief
segment, hiding the carry-forward label and the orders heading. Added a short
tail + carry-forward preview to `_dry_run_report` so the existing dry-run
witnesses stay green without weakening what they assert.

## Agent Notes
One brief.render threaded into pi/claude_code/copilot_cli/grok adapters and the dry-run+live spawn.json (no second assemble); FaithRefError joins the fallback; extras refuses by name. New test_dispatch_render_thread.py (7, red pre-fix), test_dispatch.py 139, adapters+dry-run+render 169, brief suites 176 green (1 known-red g15).

PARENT REVIEW (a00-22acfd9e): all three claim conjuncts VERIFIED by three parent-run negative probes (1 wire, 2 gate) recorded in this node's `probes:`. Bytes read: dispatch.py one render before build_command + reused in spawn.json; pi/claude_code/copilot_cli use [rendered_brief] and never assemble; grok stub accepts; FaithRefError joins RenderError in _render_dispatch_brief; brief.render refuses extras for a role lacking the part. render != assemble byte-wise (head differs), so the fix is non-vacuous. Accepted as proved. Caveat: restart() funnels through build_command with no rendered_brief, so a RESTARTED agent still re-assembles (outside this node's build_command claim, noted as push_further).
