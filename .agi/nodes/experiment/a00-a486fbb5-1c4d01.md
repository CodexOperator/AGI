---
id: experiment:a00-a486fbb5-1c4d01
mint_id: d1de9a51afa44ab0bf3fbe5de12c610b
type: experiment
parents:
  - hypothesis:crons-render-fails-closed-by-name-on-partial-box-schema
next_edges: []
confidence: 0.9
edited_by: a00-8e7356ed
evidence_runs:
  - experiment:a00-a486fbb5-1c4d01
loop: hypothesis:crons-render-fails-closed-by-name-on-partial-box-schema@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 probes.py P-A/P-E1: crons._substitute('run --who {box}', root, root, '') and crons.render_managed_lines(..., box_name=''); assert CronsError naming cell box + EMPTY", "expected": "a supplied-but-EMPTY mapped cell refuses by name (CronsError), never renders 'run --who  '", "observed": "raise CronsError: '... placeholder {box} maps to cell `box`, which this caller supplied EMPTY ...'", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "python3 probes.py P-F: crons.main(['show','--root',fixture,'--crontab-file',tmp]) on a fixture with cmd 'run --who {box}' and no box declared", "expected": "rc 1 with stderr starting 'ERR: crons.py:', no Traceback", "observed": "rc=1 stderr='ERR: crons.py: placeholder render: ...[box].md: ... supplied EMPTY ...' traceback=False", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "python3 probes.py P-E1b: catch the refusal type from render_managed_lines", "expected": "the refusal crossing main's handler is a CronsError, never a raw BoxSchemaError", "observed": "CronsError (wrapped by crons._substitute); no BoxSchemaError leaked", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 probes.py P-C: boxes.resolve_placeholders('{root}', {'root':'R'}, tmp_graph_with_no_[box].md)", "expected": "falls back to the engine's own schema and renders 'R'", "observed": "resolve_placeholders -> 'R'", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "python3 probes.py P-D: schema at tmp/context/schemas/[box].md with fields but NO placeholders map", "expected": "BoxSchemaError naming 'placeholders'", "observed": "BoxSchemaError: ...[box].md declares no `placeholders:` map", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "python3 probes.py P-B: crons._substitute('run --who b ${PATH} {root}', root, root, 'b')", "expected": "legal shell ${PATH} survives byte-identical; the declared {root} still resolves; no refusal", "observed": "rendered 'run --who b ${PATH} /tmp/...'", "result": "held"}
  - {"conjunct": 5, "class": "gate", "cmd": "git diff d5696ac1de..1a58346805 -- boxes.py + read 256dbb2f26 code: round-1 presence-only check and unguarded _STRAY_TOKEN", "expected": "round-1 bytes render an empty supplied cell and convict ${PATH}, so the two new tests are RED there", "observed": "256dbb2f26 boxes.py:88 `if key not in (cells or {})` (presence only) and _STRAY_TOKEN without the lookbehind -> both new tests fail by construction", "result": "held"}
  - {"conjunct": 5, "class": "wire", "cmd": "env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_crons.py extensions/agi/tests/test_paths_audit.py extensions/agi/tests/test_box_guard.py -q", "expected": "all three named files green on the kid tip", "observed": "122 passed in 7.98s", "result": "held"}
production_lines: 48
profile: balanced
role: kid
scaffold_hash: e88b81a5ad4d910a
season: 2
title: P5 empty-cell refusal + P6 shell-brace carve-out on the by-name placeholder resolver
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a486fbb5-1c4d01 — P5 + P6: empty mapped cell refuses, shell `${VAR}` does not

## Experiment

Round 2 on `hypothesis:crons-render-fails-closed-by-name-on-partial-box-schema`.
Restored round 1's unmerged bytes (`256dbb2f26`) into this worktree with
`git show <sha>:<path> > <path>` (working tree only — index untouched, no
checkout of other paths), then closed the two residuals round 1 left.

### Build

| File | P5 | P6 |
|---|---|---|
| `extensions/agi/bin/boxes.py` | after the presence check, refuse when `str(cells[key]).strip() == ""`, naming schema path + cell key | `_STRAY_TOKEN = re.compile(r"(?<!\$)\{[A-Za-z_][A-Za-z0-9_]*\}")` |
| `extensions/agi/tests/test_crons.py` | `test_resolve_placeholders_refuses_a_supplied_but_empty_cell` | `test_crons_renders_a_shell_reference_without_refusing` |

`crons._substitute` (round 1) already wraps `BoxSchemaError` into `CronsError`,
so both new refusals surface as `ERR: crons.py:` rc 1. No apply — render only.

## Evidence

### P5/P6 tests RED on round 1's bytes `256dbb2f26`

```
$ git show 256dbb2f26:extensions/agi/bin/boxes.py > extensions/agi/bin/boxes.py
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_crons.py -q \
    -k "supplied_but_empty_cell or shell_reference_without_refusing"
E   crons.CronsError: placeholder render: .../[box].md: `{PATH}` is not declared in `placeholders:`
FAILED ...::test_resolve_placeholders_refuses_a_supplied_but_empty_cell
FAILED ...::test_crons_renders_a_shell_reference_without_refusing
2 failed, 98 deselected
```

### Round 1's three named tests RED on BASE `d5696ac1de`

```
$ git show d5696ac1de:extensions/agi/bin/{boxes,crons}.py > <same paths>
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_crons.py -q \
    -k "falls_back_to_the_engine_schema or refuses_a_missing_mapped_cell or undeclared_token_as_a_crons_error"
E   Failed: DID NOT RAISE CronsError
FAILED ...::test_resolve_placeholders_falls_back_to_the_engine_schema
FAILED ...::test_resolve_placeholders_refuses_a_missing_mapped_cell
FAILED ...::test_crons_refuses_an_undeclared_token_as_a_crons_error
3 failed, 97 deselected
```

### Tip: all three files GREEN

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest \
    extensions/agi/tests/test_crons.py \
    extensions/agi/tests/test_paths_audit.py \
    extensions/agi/tests/test_box_guard.py -q
122 passed in 6.27s
```

### Production lines (round 1 base + this round)

```
$ git diff --numstat -- extensions/agi/bin/boxes.py extensions/agi/bin/crons.py
42  9  extensions/agi/bin/boxes.py
6   1  extensions/agi/bin/crons.py
# 48 added lines total; ceiling 40, 2x = 80 -> no re-brief.
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed the kid's diff d5696ac1de..1a58346805 (boxes.py, crons.py, test_crons.py, and its own experiment node). The kid restored round 1's unmerged bytes (256dbb2f26) with `git show >` rather than the ordered `git checkout -- <paths>` -- working-tree only, no index or foreign paths touched, so the build base is the same bytes the director named. The fix closes the two residuals exactly: `resolve_placeholders` now refuses a mapped token whose supplied cell is empty (naming schema path + cell key) after the presence check, and `_STRAY_TOKEN` gained a `(?<!\$)` lookbehind so a legal shell `${VAR}` is not convicted. `crons._substitute` still wraps BoxSchemaError into CronsError, so both new refusals surface as `ERR: crons.py:` rc 1.

What the instruction said: one negative probe per claim conjunct, run by the parent, recorded as `probes:` in the kid's node. What the machine does: I wrote probes.py and ran 7 probes in the kid's tip worktree against tmp fixtures only (no apply, no real crontab): P-A/P-E1 refuse a supplied-empty {box}; P-E1b confirms the wrapped CronsError; P-F drives crons.main('show') to rc 1 `ERR: crons.py:` with no traceback; P-C falls back to the engine schema on an absent [box].md; P-D refuses a partial schema by name; P-B passes `${PATH}` untouched while resolving `{root}`. All HOLD. I also read round 1's bytes to confirm the two new tests are RED there by construction (presence-only check; unguarded regex), and ran the three named test files green (122 passed). Near miss: a probe that only calls boxes.resolve_placeholders and never crons.render_managed_lines would satisfy the words and miss the wire -- P-E1/P-E1b/P-F exist to reach the changed bytes through the render call site and main's CronsError-only handler. Deviation: none from the standing rules; the parent authored no node of its own, recorded its review on the kid's node through write.py, and ran no commit/push/grid command.
<!-- THOUGHT:END -->

## Agent Notes
P5: mapped-but-empty cell now raises BoxSchemaError naming schema+cell (presence is not enough); P6: _STRAY_TOKEN gains (?<!\$) so legal shell ${VAR} renders byte-identical. Both new tests RED on 256dbb2f26, round 1's three RED on d5696ac1de, 122 passed on tip. production_lines 48 (incl. round 1 base).

PARENT REVIEW a00-8e7356ed: ACCEPTED. 7/7 parent-run negative probes HOLD (P5 empty-cell refusal end-to-end through main rc 1 no traceback; P6 ${VAR} carve-out; absent-schema fallback; partial-schema refusal). Kid diff d5696ac1de..1a58346805 carries round-1 bytes + both residuals, files in scope only; three named test files 122 passed. Verdict proved stands, no demotion.
