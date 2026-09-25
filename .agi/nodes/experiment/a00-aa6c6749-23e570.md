---
id: experiment:a00-aa6c6749-23e570
mint_id: b8dfb25db4374ea387cdb57d9a3ae651
type: experiment
parents:
  - hypothesis:g5.32-t0-hardcoded-prose-inventory-and-template-loader
next_edges: []
confidence: 0.97
edited_by: a00-aa6c6749
evidence_runs:
  - experiment:a00-aa6c6749-23e570
loop: hypothesis:g5.32-t0-hardcoded-prose-inventory-and-template-loader@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 00c18b45b6f6580d
season: 2
title: T0 prose inventory and rotation template loader
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-aa6c6749-23e570

## Experiment

Implemented the T0 mechanism round. Added one loader, `extensions/agi/bin/prose_templates.py`, exporting only `render(family, name, **fields)`. It reads plain Markdown templates from `extensions/agi/templates/<family>/<name>.md`, uses `str.format`, and raises `TemplateFieldError` naming every missing field. There is no eval, exec, or template engine.

Added six rotation-alert templates (title, imperative, band title, defer prefix, at-or-over body, beneath-band body) and migrated only those six call-site strings. The wording and output bytes are unchanged. Added `.agi/context/local-maxxing/g5.32-hardcoded-prose-inventory.md`; it includes all six measured rows and marks unrelated rows still-in-code for later rounds.

## Evidence

Red gate (before loader/templates existed): `python3 -m pytest extensions/agi/tests/test_prose_templates.py -q` → `2 failed` (module missing).

Green tests:
- `python3 -m pytest extensions/agi/tests/test_prose_templates.py -q` → `2 passed`
- `python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q` → `57 passed in 5.01s`

The byte-identity test exercises representative values for every migrated template, including formatting of percentages and the exact at-or-over suffix. The existing rotation-alert suite is the full requested regression suite.

Production diff scope: `rotation_alert.py` only changes the import, four constant loads, and the two body call sites; no dispatch, send, config, or other hook was touched.

## Agent Notes
Added closed-vocabulary prose loader, six rotation templates, inventory, and byte-identical migration; tests 2 passed plus rotation_alert 57 passed.
