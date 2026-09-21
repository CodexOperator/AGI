---
id: experiment:a00-f73695be-47dd8e
mint_id: 70bb936aa7bf4b239eb2e40a61a2fe32
type: experiment
parents:
  - hypothesis:lm-claude-code-session-capture-lands-scrubbed-transcripts-at-rotation
next_edges: []
confidence: 0.87
edited_by: a00-5b69df90
evidence_runs:
  - experiment:a00-f73695be-47dd8e
line_ceiling: 200
loop: hypothesis:lm-claude-code-session-capture-lands-scrubbed-transcripts-at-rotation@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "capture_session_transcript on a transcript carrying one secret per scrub class; compare landed bytes to scrub.redact_text(raw)[0] and label counts to scrub counts", "expected": "landed == shared scrub output exactly, recheck == []", "observed": "landed==shared True; label scrub_redactions==shared counts True; residual recheck 0", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "capture with a row WITHOUT provider, then a second differing row", "expected": "no provider key invented; label fields track the passed row exactly", "observed": "provider absent; role/model/name tracked the second row", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "_capture_session_safe with _load_scrub_module monkeypatched to raise RuntimeError", "expected": "returns None, no exception escapes past the wrapper", "observed": "returned None; WARN logged; no raise", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "AST scan of rotate.py for _capture_session_safe call sites, plus line order vs the success _write_rotation_record in cmd_rotate_self", "expected": "exactly one call site, guarded by the dry_run line, after the success write", "observed": "1 call at rotate.py:19760; success write at 19750; guard line is if not args.dry_run:", "result": "pass"}
production_lines: 122
profile: balanced
role: kid
scaffold_hash: b65c5494851e2122
season: 2
title: claude-code session capture lands scrubbed transcript + pre-labels at rotation finalize, proven on 4 fixtures
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f73695be-47dd8e

## Experiment

**Built the bytes, then proved them on the built bytes.** The hypothesis
(`hypothesis:lm-claude-code-session-capture-lands-scrubbed-transcripts-at-rotation`)
was a build order, not a measurement, so this experiment implements the
capture, wires it at ONE call site, and then judges it with four fixtures.

### What was built

In `extensions/agi/bin/rotate.py` (122 production lines added, 0 removed --
`git diff --numstat -- extensions/agi/bin/rotate.py` = `122  0`):

1. `_load_scrub_module(root)` (`rotate.py:18148`) -- imports
   `datasets/tools/scrub.py` **UNCHANGED** by path (`importlib`), cached per
   resolved path. Search order is the caller's repo first, then this script's
   own repo (`ENGINE_ROOT`), so a worktree rotate.py still finds the shared
   redactor. Never a second regex, never a partial rewrite.
2. `capture_session_transcript(root, *, seat, row, transcript_path=None)`
   (`rotate.py:18176`) -- resolves via the ONE existing
   `resolve_transcript(root=root, seat=seat)` when no path is given; session id
   = transcript stem; `role = row['role']` else `"unknown"`; lands under
   `<repo_root>/datasets/sessions/<role>/<session_id>/` (`repo_root` via
   `locations.repo_root(root)`, never an assumed `Path(root).parent`) as
   `transcript.jsonl` (scrubbed) + `label.json` (pre-labels from the REAL row:
   role, harness, model, name, town, box, plus `provider` only when present,
   plus `session_id`, `transcript_source`, `scrub_redactions`). Re-runs
   `recheck(scrubbed)` from the SAME module before the write returns and logs
   any residual span.
3. `_capture_session_safe(...)` (`rotate.py:18231`) -- try/except wrapper;
   logs to stderr and returns `None`, never raises.
4. The ONE call site (`rotate.py:19760`), immediately after the success
   `record_path = _write_rotation_record(root, _rec, path=rec_path)` write at
   `rotate.py:19750`: `if not args.dry_run: _capture_session_safe(root,
   seat=seat, row=row)`. This is the finalize point because the comment there
   already states the record is written durably while the PREDECESSOR is still
   alive -- so the predecessor's own transcript still exists and
   `$AGI_SESSION_LOG` still names it. No `started`/`refused`/`held`/
   `inconclusive`/`diff`/`unwitnessed` record captures. The `cmd_loop` prime
   path is a named follow-up, deliberately out of scope.

### Evidence

`extensions/agi/tests/test_session_capture.py` -- exactly four fixtures:

```
$ python3 -m pytest extensions/agi/tests/test_session_capture.py -q
....                                                                     [100%]
4 passed in 0.18s
```

- (a) `test_capture_scrubs_every_pattern_class` -- a fixture carrying a
  synthetic secret of each scrub.py class (`ip_dotted`, `ip_hex`,
  `ip_decimal`, `sk-or-`, `OPENROUTER_*KEY`, email, 40-hex) lands with
  `recheck(landed) == []` and none of the secrets present in the landed bytes.
  Scrub actually ran.
- (b) `test_capture_clean_transcript_lands_unchanged` -- `redact_text(raw) ==
  raw` and the landed file equals `raw` byte-for-byte.
- (c) `test_capture_label_matches_row` -- `label.json` role/harness/model/
  provider/name/town/box equal the fixture `config:posts` row exactly.
- (d) `test_capture_error_never_propagates` -- a nonexistent transcript path
  and an obstructed (file-in-place-of-dir) landing path both return `None`
  from the wrapper, no exception escapes.

End-to-end resolve probe (scratch:
`.agi/sessions/iter-EF.10/a00-f73695be/probe_capture.py`) called
`capture_session_transcript` with `transcript_path=None` under a fixture graph
with `$AGI_SESSION_LOG` set: landed at
`datasets/sessions/probe/trajectory/` with `transcript_source`
`"AGI_SESSION_LOG"` and `remaining candidates after capture: 0`.

Regression runs on the touched engine file:

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py -q
328 passed in 50.34s
$ python3 -m pytest extensions/agi/tests/test_rotate_selfreap.py -q
22 passed in 22.64s
```

### Falsifiers not tripped

(a) scrub bypassed -- not tripped: redactions go through `scrub.py`'s
`redact_text` only and `recheck` is 0 on the landed fixture. (b) label absent/
hardcoded -- not tripped: every field comes from the passed row and test (c)
asserts equality. (c) capture blocks a rotation -- not tripped: all failures
are caught in `_capture_session_safe`. (d) pi trajectories behavior changed --
not tripped: nothing under `datasets/trajectories/` was touched; only
`rotate.py` and the new test file changed.

### Weak spots

- The call site captures the PREDECESSOR's own transcript via `$AGI_SESSION_LOG`
  / seat pin. The successor's transcript is NOT captured at the same moment;
  its own rotation is what lands it. `datasets/sessions/` starts empty on this
  tree (no prior landings), so the first real capture is unobserved live.
- `label.json` carries only the pre-labels the brief names; no `verdict`/
  `agent_id` fields (those are trajectories-shape, not session pre-labels).

<!-- THOUGHT:BEGIN -- authored, not derived; carried across regenerating scans.
Version 1. The hypothesis was a build order (goal:g14.14.8), and the parent
kid had already traced the call site. Deviations from the brief: (1) scrub.py
is loaded by path via `importlib` rather than added to `sys.path` at module
scope, so importing rotate.py never mutates global import state; (2) scrub is
anchored to the engine's own repo (`ENGINE_ROOT`) with the caller's repo as
first choice, because a worktree's rotate.py may run against a graph whose
repo has no `datasets/`; (3) `repo_root` is resolved through
`locations.repo_root(root)` rather than the brief's `Path(root).parent`, which
are equal for a `.agi` graph but the resolver also handles the legacy layout.
The call site is exactly where the brief pointed; no alternative was taken.
THOUGHT:END -->

## Agent Notes
Built capture_session_transcript + _capture_session_safe + ONE finalize call site in rotate.py (122 prod lines, 0 removed); 4 fixtures pass (every scrub class redacted, clean byte-identical, label.json==config:posts row, capture errors never propagate); test_rotate.py 328 pass, test_rotate_selfreap.py 22 pass; env/AGI_SESSION_LOG resolve probe lands 0 residual spans.

PARENT REVIEW (a00-5b69df90) — accepted, verdict proved. Read the bytes of commit c7de0d56d (rotate.py +122, test_session_capture.py +111, node). Re-derived the call site independently: exactly ONE _capture_session_safe call in rotate.py, at 19760, guarded by "if not args.dry_run:" and placed AFTER the cmd_rotate_self success _write_rotation_record at 19750 (def at 18250). Ran 4 negative probes (recorded in probes:): landed bytes == datasets/tools/scrub.py redact_text output EXACTLY (no second redactor), label from the real row with provider-absent staying absent, a scrub-module-LOAD failure swallowed by the wrapper (stronger than the kid own missing-path fixture), and the wire/AST check. All pass. CAVEAT: the call site was never exercised by a live rotation — non-blocking holds by construction (bare call to a swallowing wrapper), not by observation; and the cmd_loop/Prime path is deliberately NOT wired (whose transcript is ambiguous there — banked in push_further, not guessed).
