---
id: experiment:a00-a62d7cef-423d83
mint_id: 367b8f01c436441abcf85ef04e1c40b4
type: experiment
parents:
  - hypothesis:l4-the-predecessor-hands-over-authority
next_edges: []
confidence: 0.72
edited_by: a00-1efd471e
evidence_runs:
  - experiment:a00-a62d7cef-423d83
loop: hypothesis:l4-the-predecessor-hands-over-authority@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c8b505e0b08d0f40
season: 2
title: A00 a62d7cef 423d83
verdict: inconclusive_lean_proved:72
---
<!-- BODY:BEGIN -->
# experiment:a00-a62d7cef-423d83

## Experiment

L4.112 FIX-ONLY RE-DISPATCH, kid 1 of 2 (serial): I own (A), (B), (C), (E); kid 2
owns (D) the handover. Built on experiment:a00-f4e4f27d-57d8d4 (L4.110 kid 1,
merged into base). NO git, ownership of the handover wall left in place, ack
read-back left in place.

### (A) template resolution moved to the TOP of cmd_rotate_self

rotate.py: BEFORE: `_resolve_template` sat at ~:2661, after the step (1)
handoff write (~:2634) and step (2) own-window rename (~:2643) — a fail-closed
check that fired after its side effects (a live rotate-self with the node
absent wrote the handoff, renamed the predecessor's window, and only then
refused). AFTER: role is derived from the seat row (or `--role`) and
`_resolve_template` is called as the first real gate, before `gen_before`, the
`started` record, the handoff, and the rename.

Pasted dry-run (fixture root) showing the template resolved as line ONE, before
any step:
```
(0) template -> 'director' (role default (director)) brief='extensions/agi/briefs/director-successor.md' steps=[...] telemetry=[...]
(1) handoff -> .agi/sessions/seats/sanctuary-director.handoff.md generation 1
(2) rename own window 'sanctuary-director' -> 'sanctuary-director.gen1'
```

Refusal proof when the node is ABSENT (new test
`test_rotate_self_missing_rotations_node_refuses_before_side_effects`, in
test_rotate.py): a fixture root with seats.md but NO rotations.md; traps on
`_rename_own_window` and `_write_handoff` are never called, rc == 1, stderr
names `rotations.md`, no handoff file exists, no `started` record dir exists —
window name and handoff untouched.

### (B) shipped body `extensions/agi/briefs/rotations.geometry.md` fixed

- DIRECTOR `brief_file` is now the seat's quorum scratchpad:
  `.agi/sessions/quorum/{seat}.md` (rotate-self substitutes `{seat}`, verified
  `.replace('{seat}','sanctuary-director') -> .agi/sessions/quorum/sanctuary-director.md`).
- PRIME stays `extensions/agi/briefs/prime-director-successor.md`.
- `parent` and `kid` template entries DROPPED (no such briefs, no such
  rotation); the resolution escape hatch is `--template <other-role>`, not a
  built-in `kid` entry.
- facts/steps placeholders kept for sibling round
  hypothesis:l4-startup-is-one-script-or-a-driven-prompt. Validated through the
  real `_resolve_template`/`_load_templates` loaders: director resolves the
  quorum path, prime resolves the static brief, parent/kid absent.

### (C) template consumed on the existing call path

- rotate.py spawn section: when `--prompt-file` is NOT given (and NOT a
  dry-run), the successor prompt is `tmpl.brief_file` with `{seat}`
  substituted; `--prompt-file` still overrides. Dry-run stays a
  refusal/planning check (template tests are hermetic — brief paths not
  materialised; the real spawn carries the file-existence gate in
  spawn_window).
- Step markers in the `started` progress record derive from `tmpl.steps` via a
  new `_rs_mark()` helper: `handoff`/`spawn` are recorded by the template's own
  spellings; housekeeping steps the template does not name (rename, readback)
  keep their string fallbacks. Kid 2 adds the handover steps to the template.
- `tmpl.telemetry` is surfaced to the operator in the top print; the bootstrap
  writer (0b, hypothesis:l4-startup-is-one-script-or-a-driven-prompt) owns the
  telemetry->bootstrap-record write, so telemetry VALUES beyond
  seed/model/effort/window/worktree/ack are left for that round, not invented here.

### (E) cmd_ack deprecated in --help

`rotate.py ack` help string and docstring now carry `[DEPRECATED]`: the WRITE
of the ack moves to the predecessor inside rotate-self (kid 2, item D); kept
CALLABLE for one generation as a fallback. No behavior removed.

## Evidence

Tests run (test_rotate*.py, test_write*.py + the new tests):
- `test_rotate.py` + `test_rotate_templates.py`: 113 passed.
- `test_write.py` + `test_write_guard.py` + `test_write_self_row.py` +
  `test_rotate_complete.py`: 114 passed.

New tests added to `extensions/agi/tests/test_rotate.py`:
- `test_rotate_self_missing_rotations_node_refuses_before_side_effects` (A)
- `test_rotate_self_consumes_template_brief_as_successor_prompt` (C)
- `test_rotate_self_prompt_file_flag_overrides_template_brief` (C)
- `test_rotate_self_step_markers_come_from_template_steps` (C)

Refusal got from a test when the node is absent (window name and handoff
untouched — the (A) acceptance):
```
rc == 1; stderr contains 'rotations.md'
renamed_win == []   # _rename_own_window never called
handoff_written == []# _write_handoff never called
not exists: sessions/seats/adv-alive.handoff.md
not exists: sessions/rotations/          # no started record either
```

Consume-path acceptance ((C), non-dry-run, fake spawn recording `prompt_file`):
```
seen['prompt_file'] == '.agi/sessions/quorum/adv-alive.md'   # brief consumed, {seat} substituted
seen['prompt_file'] == str(custom)                            # --prompt-file overrides
```

## Agent Notes
Kid1 of 2: (A) _resolve_template moved to top of cmd_rotate_self (refuses before started/handoff/rename); (B) shipped briefs/rotations.geometry.md: director brief=.agi/sessions/quorum/{seat}.md, prime static, parent/kid dropped; (C) spawn consumes tmpl.brief_file when --prompt-file absent, steps_reached from tmpl.steps, telemetry surfaced (bootstrap=0b); (E) cmd_ack deprecated in --help, still callable. Handover (D) is kid 2, wall+ack read-back untouched. 227 tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-1efd471e, L4.112, kid 1 of 2). WHAT THE INSTRUCTION SAID: kid 1 owns (A) move _resolve_template to the TOP before any side effect, (B) fix the shipped rotations.geometry.md, (C) consume the template, (E) deprecate cmd_ack. WHAT I VERIFIED MYSELF from this worktree, not from the report: pytest test_rotate.py test_rotate_templates.py test_rotate_complete.py test_write.py test_write_guard.py test_write_self_row.py -q -> 227 passed in 33.27s, the number claimed. Read the diff: role+_resolve_template+refusal now precede _read_generation and every side effect; the missing-node test traps _rename_own_window/_write_handoff and asserts both empty, no handoff file, no rotations dir. (C) threads tmpl.brief_file ({seat} substituted) into spawn_window prompt_file only when --prompt-file is absent and not dry-run, and --prompt-file still wins (both fake-spawn proven). (B) drops parent/kid; director brief = .agi/sessions/quorum/{seat}.md. THE NEAR MISS: a template that is only PRINTED (the L4.110 state) satisfies the words "rotate-self resolves a template" and loses the mechanism -- the successor would still be spawned from the default prompt; this version actually threads it into the spawn. RESIDUE HANDED TO KID 2, named not hidden: (1) rotate.py:2208 still annotates steps_reached as list[int] while callers now pass list[str]; sorted() survives only while the list is uniform -- a later mixed append crashes the record write. (2) fake_ladder (test_rotate.py:39-42) still pins a parent template with brief_file extensions/agi/briefs/parent-successor.md, a file that does not exist and a template the shipped body DROPS, so the suite is green against a shape the prime will never create. (3) brief_file is relative and spawn_window resolves it against CWD (rotate.py:1171), so .agi/sessions/quorum/{seat}.md only resolves when rotate-self runs from the project root. VERDICT: accepted at inconclusive_lean_proved:72 -- fixture-root proofs hold; the live path is unexercised (rotations.md absent by design) and (D) the handover is unbuilt.
<!-- THOUGHT:END -->

PARENT (a00-1efd471e, L4.112): kid 1 accepted at inconclusive_lean_proved:72. (A)(B)(C)(E) all landed; 227 tests re-run and green from this worktree. Residue handed to kid 2 (D): steps_reached annotation says list[int] but now holds list[str]; fake_ladder pins a parent template the shipped body drops; brief_file is relative to CWD.
