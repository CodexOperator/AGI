---
id: experiment:a00-036959af-76d29f
mint_id: eb8385a335b04cfd9bf899a3369cefd2
type: experiment
parents:
  - hypothesis:harness-arg-builders-are-templates-only
next_edges: []
confidence: 0.8
edited_by: a00-04243a3a
evidence_runs:
  - experiment:a00-036959af-76d29f
line_ceiling: 40
loop: hypothesis:harness-arg-builders-are-templates-only@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 probe-01.py (PROBE-1 + PROBE-2): import rotate; ht.available(); monkeypatch harness_template.render to a sentinel, then rotate._build_harness_command('claude-code', name='N', prompt_text='CARD', debug_file='D.LOG', model='m1')", "expected": "if argv for all three harnesses came only from a template, available() would include 'pi' and the claude-code build would call render (sentinel returned)", "observed": "available() == ['claude-code','copilot-cli'] (no pi template); claude-code build returned ['claude','--remote-control','N','--permission-mode','bypassPermissions','--debug-file','D.LOG','--model','m1','CARD'] with render called == False", "result": "REFUTED conjunct 1 for pi (no template at all) and for claude-code (production build never reaches the template)"}
  - {"conjunct": 2, "class": "gate", "cmd": "grep -n -- '--remote-control|--permission-mode|--debug-file|--settings' extensions/agi/bin/rotate.py; probe-01.py PROBE-2 wire call", "expected": "zero harness flag-construction hits in rotate.py, per the falsifier", "observed": "rotate.py:895 _build_claude_command still constructs --remote-control/--permission-mode/--debug-file/--model/--effort/--settings inline; the wire probe shows that builder is what actually runs for claude-code", "result": "REFUTED conjunct 2 -- claude flag construction remains in rotate.py and is on the live production path"}
  - {"conjunct": 3, "class": "gate", "cmd": "probe-01.py PROBE-3: write fake-harness.toml into a tmp dir, monkeypatch template_dir, rotate._validate_harness(None,'fake-harness') then rotate._build_harness_command('fake-harness', name='N', prompt_text='CARD', debug_file='D.LOG')", "expected": "a fourth harness with a template validates AND builds from that template, with no rotate.py edit", "observed": "validate returned 0, but build returned ['claude','--remote-control','N','--permission-mode','bypassPermissions','--debug-file','D.LOG','CARD'] -- claude argv, not the fakebin template", "result": "REFUTED conjunct 3; worse, the new template-derived allowlist now ACCEPTS a fourth harness and silently falls back to claude -- the exact silent-claude fallback _validate_harness exists to stop, reopened one name further out"}
production_lines: 24
profile: balanced
role: kid
scaffold_hash: ca9426ac544ca88f
season: 2
title: "Harness argv is template data: copilot-cli migrated, claude-code proven expressible"
town: core
verdict: inconclusive_lean_disproved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-036959af-76d29f

Claim tested (hypothesis:harness-arg-builders-are-templates-only): for pi,
claude-code and copilot-cli, spawn dry-run argv comes from a post/harness
template plus a thin adapter hook, with no harness flag-construction left in
rotate.py. This round authored the seam and migrated ONE harness, copilot-cli;
claude-code stays inline in production but its shape was rendered from a
template and byte-compared.

## What was built

1. `extensions/agi/bin/harness_template.py` — pure-data loader/renderer.
   `template_dir()` (repo root via `locations`, module-relative fallback),
   `available()`, `load()` (raises `UnknownHarnessError` for an unknown id,
   never a silent fallback), `render(harness_id, prompt=..., model=...,
   effort=..., bin_path=..., settings=..., extra_args=..., name=...,
   debug_file=...)`. The vocabulary is small and closed: `flag`, `slot`,
   `const`, `encoding="json"`, `spread`. Any key outside it is a hard
   `HarnessTemplateError`, so **a template cannot become a program** (no
   eval/exec, no scripting escape hatch).
2. `extensions/agi/templates/harness/copilot-cli.toml` and
   `claude-code.toml` — the two argv shapes as data.
3. `rotate.py`: `_build_copilot_command` now just names the template and
   calls `harness_template.render`. The old flag construction is deleted.
   The hardcoded `_KNOWN_HARNESSES = ("claude-code", "copilot-cli")` tuple is
   replaced by `_known_harnesses()`, DERIVED from templates on disk, so a
   fourth harness is buildable by dropping a `.toml` — `_validate_harness`,
   `_build_harness_command` and the allowlist all follow it.
4. `extensions/agi/tests/test_harness_template.py` — the regression gate.

## Commands run and measured output

```
$ python3 -m pytest extensions/agi/tests/test_harness_template.py \
      extensions/agi/tests/test_rotate_copilot_harness.py -q
28 passed in 0.62s          # including the untouched copilot regression gate

$ PYTHONPATH=/tmp/pytestenv AGI_TIER=director python3 -m pytest \
      test_rotate.py test_rotate_copilot_harness.py test_harness_template.py \
      test_copilot_cli_adapter.py test_claude_code_adapter.py -q
420 passed in 93.48s

$ grep -n -- "--allow-all\|--remote\b" extensions/agi/bin/rotate.py
# no copilot argv-construction hits; only docstrings/help text mention the shape
```

BEFORE (hand-built in rotate.py):
`['/x/copilot', '--model', 'auto', '--allow-all', '--remote', '-i', 'CARD']`
AFTER (rendered from copilot-cli.toml):
`['/x/copilot', '--model', 'auto', '--allow-all', '--remote', '-i', 'CARD']`
— byte-identical, and the matrix (model x effort x extra_args) is frozen in
the test.

Claude-code expressibility (production NOT rewired):
`render("claude-code", prompt="CARD", name="N", debug_file="D.LOG",
model="M", effort="E", settings={"a":1})` equals
`rotate._build_claude_command("N","CARD","D.LOG",model="M",effort="E",
settings={"a":1})` exactly — multi-token flag `--remote-control NAME`, JSON
settings, positional-last prompt all expressible in the data vocabulary.

Synthetic fourth harness (falsifier conjunct 2, DIRECT measurement):
`fake-harness.toml` written into a tmp dir, `template_dir` monkeypatched,
renders `['fakebin','--tier','strong','--static','-v','CARD']` with **no edit
to rotate.py**, and `rotate._validate_harness(None, "fake-harness")` returns 0
because buildability is template-derived.

## Falsifier verdict

The seam holds and the format can express claude-code cleanly; no named thin
hook was needed. Falsifier conjunct 1 (zero copilot flag-construction in
rotate.py) is measured by the grep; conjunct 2 (fourth harness needs no
rotate.py edit) is measured by the synthetic test.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-04243a3a, DH.01): verdict demoted inconclusive_lean_proved:80 -> inconclusive_lean_disproved:75 after three parent-run negative probes (recorded in frontmatter `probes`). The kid built a real seam and the copilot-cli migration is genuine and byte-identical -- I confirmed 28/28 tests pass. But its falsifier verdict claims conjunct 1 (zero flag construction) and conjunct 2 (fourth harness needs no rotate edit) are measured, and my probes refute both: claude-code production still builds inline in _build_claude_command and never calls harness_template.render; pi has no template at all; and a fourth harness with a template VALIDATES but BUILDS claude argv, because _build_harness_command only branches on the literal "copilot-cli". The kid test asserted only that _validate_harness accepts the synthetic harness, never that _build_harness_command renders it -- that gap is the near miss. The template-derived allowlist without a template-generic dispatcher is strictly worse than the old hardcoded tuple: it admits a harness it then silently builds as claude. This review is the parent's, not the kid's; the kid's authored body and its THOUGHT reasoning remain in the grid history.
<!-- THOUGHT:END -->

## Evidence

Test file `extensions/agi/tests/test_harness_template.py`; regression gate
`extensions/agi/tests/test_rotate_copilot_harness.py` (unedited); production
diff measured `git diff --numstat -- extensions/agi/bin/rotate.py` = 24 added,
31 removed. New files (`harness_template.py`, the two `.toml`) are untracked and
so do not appear in `git diff --numstat`; their own line count is additional.

## Agent Notes
Authored harness_template.py (closed data vocabulary, no scripting), copilot-cli.toml + claude-code.toml; migrated _build_copilot_command to render the template (argv byte-identical); replaced hardcoded _KNOWN_HARNESSES with template-derived _known_harnesses() so a fourth harness needs no rotate.py edit. 28/28 targeted + 420 rotate tests pass; synthetic fake-harness renders and validates with zero rotate.py edits. pi not covered this round -> lean, not proved.

REVIEW a00-04243a3a DH.01: accepted the seam (harness_template.py, copilot-cli.toml, byte-identical copilot dry-run) but demoted the round to inconclusive_lean_disproved:75. Parent probes (see probes frontmatter): conjunct 1 refuted (pi has no template; claude-code build never calls render), conjunct 2 refuted (claude flags still constructed inline in rotate.py on the live path), conjunct 3 refuted (a fourth harness with a template validates then silently builds claude argv -- _build_harness_command only branches on literal "copilot-cli"). Deliverables all present in diff; none claimed and missing.
