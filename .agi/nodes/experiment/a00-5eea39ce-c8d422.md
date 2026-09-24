---
id: experiment:a00-5eea39ce-c8d422
mint_id: dfb7f6e144b74e259b0da875875c902c
type: experiment
parents:
  - hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard
next_edges: []
confidence: 0.7
edited_by: director-engine
loop: hypothesis:pi-agents-load-no-context-file-and-the-brief-carries-the-paid-for-path-guard@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 96c435f5ea90e8b1
season: 2
title: A00 5eea39ce c8d422
town: local-maxxing
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-5eea39ce-c8d422

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Verdict HELD at inconclusive_lean_proved:70 against merge-up review Q8 (final=demote, 0 of 3 defects refuted by its verifier) -- the director weighed each against the bytes (09-24 04:5xZ). (1) rotated pi successor bypasses the guard (rotate.py:1132): REFUTED -- pi.toml rotate = false drops pi from rotate._known_harnesses() (rotate.py:1002; in-process: claude-code, copilot-cli), _validate_harness refuses any harness outside it (rotate.py:1030; pi / pi-free / pi-local -> rc 1) and gates the ONLY _assembled_successor_command call (rotate.py:1861 before 1907). Every reachable pi route is dispatch.py _render_dispatch_brief (dispatch.py:1055: the assemble body rides as extras, the fallback is assemble), incl. the workflow.py pi stages (one dispatch.py kid per stage, workflow.py:7). (2) survival test reaches a real process (test_brief_render.py:55): REAL, hygiene -- brief.assemble(profile=survival) with no project_root runs a read-only git status --porcelain (brief.py:753-760); the assertion does not depend on it; RESIDUE: pass a fixture root. (3) no certified terminal evidence: answered on the post branch at 881b528a04 (the director gate: the every-role test red on the base, 234 passed on the tip; Q8 reproduced 234). Latent, named: were pi ever a rotate seat, brief.render at rotate.py:1132 would need the guard -- the config-max residue (the guard text in the brief configuration) closes it.
<!-- THOUGHT:END -->
