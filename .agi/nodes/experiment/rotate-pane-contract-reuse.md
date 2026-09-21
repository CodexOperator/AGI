---
id: experiment:rotate-pane-contract-reuse
mint_id: 62dbb61d045e401a8b014eeb9577c3e1
type: experiment
parents:
  - hypothesis:a00-62e2a798-0a7456
next_edges: []
edited_by: a00-f4f7eb39
line_ceiling: 40
loop: goal:g7.31.2.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "pytest -q test_rotate_pane_contract.py::test_pane_name_reused_across_rotate_self", "expected": "captured spawn name == plain seat name; predecessor renamed <seat>.prev", "observed": "seen[name]==adv-alive; windows.txt: adv-alive + adv-alive.prev", "result": "pass"}
  - {"conjunct": 2, "class": "gate-negative", "cmd": "grep -Ein grok extensions/agi/bin/rotate.py; no _build_*_command; call _build_harness_command", "expected": "zero grok matches; no per-harness builder; seam returns rendered argv", "observed": "exit 1 zero matches; argv=[claude, --remote-control, S, ...]", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: a44173d253f10c40
season: 2
title: "Rotate pane-contract reuse proven: same spawn_window seam, zero per-harness argv builders, grok refused by name"
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:rotate-pane-contract-reuse

## Experiment

New file `extensions/agi/tests/test_rotate_pane_contract.py` (4 tests,
comment-labelled by falsifier class). Fixtures modelled on
`test_rotate_boundary_rename.py` (faked `spawn_window` capturing `name=`,
throwaway tmp_path, no live tmux). No existing file edited. No guessed
`grok-bot.toml` added.

Base tip: `5d8d4c914`.

## Evidence

### Command tails

```
$ python3 -m pytest extensions/agi/tests/test_rotate_pane_contract.py -q
4 passed, 22 warnings in 1.89s

$ python3 -m pytest extensions/agi/tests/test_rotate_boundary_rename.py \
    extensions/agi/tests/test_rotate_templates.py \
    extensions/agi/tests/test_harness_template.py -q
83 passed, 34 warnings in 43.12s

$ grep -Ein 'grok' extensions/agi/bin/rotate.py
(no output; exit 1)

$ python3 -c "import sys; sys.path.insert(0,'extensions/agi/bin'); import rotate; \
    print(rotate._known_harnesses()); print(rotate._validate_harness(None,'grok-bot'))"
('claude-code', 'copilot-cli')
(1, '')
ERR: no harness 'grok-bot' in config; declared: ['claude-code', 'copilot-cli']
```

### Test 1 (wire) — `test_pane_name_reused_across_rotate_self`

Drives `rotate.cmd_rotate_self` with a faked `rotate.spawn_window` capturing
`name=`. Observed: `seen['name'] == 'adv-alive'` (the plain seat name, not a
numeral, not a bespoke path), the successor window `adv-alive` is present, and
the predecessor window is renamed to `adv-alive.prev`. This is the pane
contract: one `spawn_window` seam, successor holds the SAME plain name.

Divergence from the inherited brief: the brief said the predecessor is renamed
to `S.gen<N>`. The MEASURED tip renames to `<seat>.prev` for a non-prime seat
(rotate.py ~18644 non-staged, ~18750 in the staged-rename branch; goal:g15.25
makes non-prime posts generation-less on every surface). Both rename branches
are now COVERED in `test_rotate_pane_contract.py`: conjunct 1 drives the
non-staged `_rename_own_window` path (`test_pane_name_reused_across_rotate_self`),
and conjunct 4 drives the staged-rename branch end to end
(`test_staged_rename_spawns_successor_under_new_name_and_prev`: a real
`.agi/sessions/seats/adv-alive.rename.json` staged through committed
`rotate.cmd_rename_post`, then `cmd_rotate_self` applies it at (0.9) and the
successor spawns under the post-rename name `adv-renamed`, with the window
renamed to `adv-alive.prev` and the stage consumed). These tests assert the
MEASURED, documented rename; the docstring at rotate.py:18122 still says
`S.gen<N>` and is stale prose.

### Test 2 (gate/negative) — `test_rotate_has_no_per_harness_argv_builder`

No `_build_claude_command` / `_build_copilot_command` / `_build_pi_command` /
`_build_grok*_command` in `rotate.py`; zero case-insensitive `grok` matches.
The ONE seam is called rather than grepped: `_build_harness_command(
"claude-code", ...)` returns `['claude', '--remote-control', 'S',
'--permission-mode', 'bypassPermissions', '--debug-file', 'd.log', 'hello']`
— i.e. its body really reaches `harness_template.render`.

### Test 3 (auth/gate, the honest edge) — `test_grok_seat_is_refused_by_name_no_template`

`rotate._known_harnesses()` is `('claude-code', 'copilot-cli')` (pi.toml is
`rotate = false`). There is no `templates/harness/grok-bot.toml`.
`_validate_harness(None, "grok-bot")` returns `(1, "")` and names the refusal
on stderr: `ERR: no harness 'grok-bot' in config; declared: [...]`. So a
grok-bot seat CANNOT rotate on this tip — it is refused BY NAME, not seated
through a second argv builder. The prerequisite is `goal:g7.31.1`.

### Test 4 (wire) — `test_staged_rename_spawns_successor_under_new_name_and_prev`

The staged-rename branch (`_apply_staged` at the (0.9) boundary, gated on
`.agi/sessions/seats/<seat>.rename.json`): a stage is written through the
committed `rotate.cmd_rename_post`, `cmd_rotate_self` applies it before the
spawn, and the successor arrives under the post-rename name `adv-renamed`
while the predecessor window is renamed to `adv-alive.prev` (non-live seams
rename the name the window ACTUALLY carries, `old`) and the stage is consumed.
This is the coverage the earlier round cited but did not write.

### Verdict

Both conjuncts of falsifier 1 hold on the built bytes: the successor reuses
the same pane contract through the single template seam, and THERE IS NO
second argv builder (for grok or anyone). The one honest boundary is that a
grok seat cannot yet be SEATED at all (no template) — a prerequisite gap, not
a reinvention. `inconclusive_lean_proved:85`.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.45 CORRECTIVE (kid a00-f4f7eb39; base tip c6c22734d). (1) Instruction: state the delta this version actually records, so that no uncommitted intermediate is presented as the previous version, and set edited_by to mine, leaving the body byte-identical. (2) Machine: this version changes exactly edited_by from the committed a00-3c0140ac to a00-f4f7eb39 and this THOUGHT block; the body is untouched. (3) Measured correction to the brief: the brief said HEAD carried edited_by a00-afc164be and the DH.33 DELTA text. Measured at HEAD, that is false: HEAD already carries edited_by a00-3c0140ac and the DH.45 CORRECTIVE text signed by a00-3c0140ac. The previous version the grid will record is therefore the last committed one, a00-3c0140ac, and not the uncommitted intermediate a00-33653715. (4) History, stated accurately: the DH.33 DELTA text (kid a00-30f4b181) was first replaced by an uncommitted corrective from a00-33653715 and then by a00-3c0140ac, which is what the grid committed. Those steps are history only; no uncommitted intermediate is named as the previous version. (5) Near miss: presenting a prior agent edit as this version delta, or citing an uncommitted intermediate as the predecessor. The authored block is read by grid.py diff, by the grid version snapshot of node.md, or by a human opening the node file -- never by zoom.py, which loads the node with body=False. (6) Deviation: the brief premise was stale, so the delta target was corrected to the measured committed predecessor.
<!-- THOUGHT:END -->
