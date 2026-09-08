---
id: experiment:a00-f8f26cd8-26c4a3
mint_id: 89f67684aa4b46cfa88cf59df6845ec2
type: experiment
parents:
  - hypothesis:l3-pi-install-patch-not-durable
next_edges: []
confidence: 0.9
edited_by: a00-0a32fac0
evidence_runs:
  - experiment:a00-f8f26cd8-26c4a3
loop: hypothesis:l3-pi-install-patch-not-durable@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ddde1f535b781744
season: 2
title: A00 f8f26cd8 26c4a3
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f8f26cd8-26c4a3

## Experiment

**Claim under test** (parent `hypothesis:l3-pi-install-patch-not-durable`): an
installed pi whose edit tool lacks the L3.38 `_normalizeEditsShapes` forgiveness
cannot pass unnoticed — either the repo re-applies it at spawn/adapter load, or a
preflight fails loudly and early naming the fix.

**It was a BUILD, not a probe.** The one durable half left was the tool-side: the
patch lives in the SHARED pi install's `dist/core/tools/edit.js`, which this repo
does not track, so a `pi` upgrade silently reverts it and every kid quietly pays
the turned turn again. Built option (a) with an (b) fallback, exactly the shape
the hypothesis's testable_claim allows:

- **New** `extensions/agi/bin/pi_edit_forgiveness.py` — `ensure_pi_edit_forgiveness()`:
  at every call it locates the INSTALLED edit tool (same resolver as
  `test_edit_tool_forgiveness.py`), reads it, and checks for the marker
  `_normalizeEditsShapes`. Marker present → `("ok", ...)` no-op. Marker ABSENT
  (an upgrade dropped it) → re-applies the patch as an idempotent, atomic,
  anchor-backed splice: prepends the self-contained `_normalizeEditsShapes` helper
  (JS function declarations hoist, so order is safe) and inserts one routing
  short-circuit after `const args = input;`, written to a temp file + `os.replace`
  (no partial/duplicated splice under concurrent spawns). If the splice anchors
  (`function prepareEditArguments(input) {`, `const args = input;`) are gone
  because pi refactored the tool, it returns `("fail", ...)` rather than guess —
  the safe degradation. A structural self-check on the closed string runs before
  any write. `AGI_PI_FORGIVENESS_BYPASS=1` disables it. Also has a `--help` /
  `--check` CLI for operators.
- **Wired into** `pi_adapter.build_command` — the single chokepoint every pi
  spawn AND every restart funnels through. `"fail"` → `raise RuntimeError(...)`
  naming the L3.38 patch and the fix; `"patched"` → warn to stderr.
- **Red-first test** `extensions/agi/tests/test_pi_edit_forgiveness.py` —
  `test_install_missing_the_patch_is_reapplied` takes the REAL installed
  edit.js, strips every marker line into a temp copy (an upgrade that dropped
the patch, faithfully), hands the gate the temp path (never the live file), and
  asserts the re-application: marker restored, routing short-circuit present,
  anchors intact exactly once. Plus idempotent no-op, unanchored→fail-loud,
  double-entry idempotency, and the build_command wiring tests (gate runs per
  spawn; `fail` raises naming the fix).
- **Cross-ref** added to `test_edit_tool_forgiveness.py`: that probe DETECTS a
dropped patch but does not re-apply; the new gate keeps the install patched so
the probe keeps passing.

**Why re-apply in place and not vendor the install, and why this is the honest
ceiling**: the patch is additive, marked, atomic and anchor-gated, so an upgrade
cannot drop it unnoticed AND a version drift cannot corrupt the vendor file — the
re-apply degrades into a loud spawn-blocking `fail` that names the fix. That
satisfies "cannot pass unnoticed" both ways. Vendoring the whole pi install was
explicitly forbidden by the hypothesis; option (c) (upstream path) exists only if
pi maintainers merge the patch, which this repo cannot push.

## Evidence

- `python3 -m pytest extensions/agi/tests/ -q` — **2075 passed, 1 skipped** in
  the worktree (and 2078 passed in the tree the harness resolves on this box),
  including the 7 new `test_pi_edit_forgiveness.py` cases, the previously-passing
  `test_edit_tool_forgiveness.py` behavioral probe, `test_brief.py`, and
  `test_bin_help_smoke.py` (new bin script passes `--help` smoke).
- The red-first case runs against the real installed tool's stripped copy —
  `resolve_edit_js()` on this machine returned
  `.../pi-coding-agent/dist/core/tools/edit.js`; stripping its 2 marker
  occurrences yielded a marker-absent file that the gate re-applied (`"patched"`);
  a second pass returned `"ok"` (idempotent). The unanchored fixture returned
  `"fail"` and left the file byte-for-byte unchanged.
- Live `--check` on this box: `ok: forgiveness present at .../dist/core/tools/edit.js`.
- A pi upgrade is now caught at the FIRST spawn after it lands: `build_command`
  either re-applies (self-heal) or raises `RuntimeError` naming the L3.38 fix —
  no silent turn-by-turn tax.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
L3.39 parent review (a00-0a32fac0), accepted at proved. I read the artefact, not the report: pi_edit_forgiveness.py is an anchor-gated, atomic (temp+os.replace), idempotent re-apply gate for the installed edit.js, wired into pi_adapter.build_command — the single funnel every pi spawn and restart passes through — with fail-loud RuntimeError naming the L3.38 fix on unanchorable drift and an AGI_PI_FORGIVENESS_BYPASS escape. parents link resolves to hypothesis:l3-pi-install-patch-not-durable; verdict proved carries evidence_runs=[itself], which is legitimate since the experiment IS the run. I independently re-verified: the 8 targeted tests pass (red-first re-apply against a stripped copy of the REAL installed edit.js, idempotency, unanchored-fail, double-entry, spawn wiring), the live build_command runs the gate cleanly (python: harness={"bin":"pi"} → ok), and the import of pi_edit_forgiveness inside build_command resolves because dispatch.py puts bin/ on sys.path before loading the adapter. Option (a)+ (b) fallback is the exact shape the claim allows; no vendoring, seats.md untouched, no git run. This version differs from the kid-original only by carrying my review sign-off; the kid-authored body stands unchanged.
<!-- THOUGHT:END -->

## Agent Notes
Parent review ACCEPTED (a00-0a32fac0): proved verdict stands. Verified artefact + tests independently; live build_command gate run clean. Weak spot (minor, not blocking): the gate only protects pi spawns — non-pi harnesses skip it — and re-apply edits an untracked vendor file, which is the honest ceiling the claim permitted. Caveat also noted: unanchored pi refactor will BLOCK all spawns until manually fixed — loud by design, but worth a runbook line.
