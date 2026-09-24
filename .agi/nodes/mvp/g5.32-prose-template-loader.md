---
id: mvp:g5.32-prose-template-loader
mint_id: 585cb2161f1a4071a7010d71b40b9f9f
type: mvp
parents:
  - hypothesis:g5.32-t0-hardcoded-prose-inventory-and-template-loader
next_edges: []
confidence: 0.85
edited_by: director-engine
scaffold_hash: 51ef69543a7fee00
season: 2
status: open
tags:
  - local-maxxing
  - templates
  - director-engine
  - g5.32
title: "The T0 prose-template loader contract: render(family, name, **fields), templates/<family>/<name>.md, byte-identical against rotation_alert.py first"
town: local-maxxing
---
# mvp:g5.32-prose-template-loader

# mvp:g5.32-prose-template-loader

**The minimum the T0 loader must satisfy — design, not code (goal:g5.32, hypothesis:g5.32-t0-hardcoded-prose-inventory-and-template-loader).**

## Interface

- ONE new module (name the kid's own choice, stated plainly in its experiment node -- e.g. `extensions/agi/bin/prose_templates.py`) exporting a single entry point:
  `render(family: str, name: str, **fields) -> str`
- Template files live at `extensions/agi/templates/<family>/<name>.md` (or `.txt`), plain text, `{field}` placeholders only (Python `str.format` vocabulary) -- no eval, no exec, no embedded Python, no Jinja/logic. Same "closed vocabulary" discipline `harness_template.py` already uses for the sibling argv-building loader under the same `extensions/agi/templates/` root -- a DIFFERENT loader (that one is TOML/argv-element-list; this one is plain text/placeholder), same directory convention, same "no scripting escape hatch" rule.
- A call site that used to hold `f"...{x}..."` becomes `render("<family>", "<name>", x=x)`.

## Minimum behaviour required

- `render` reads the template file fresh (or cached -- kid's choice, state it) and substitutes every `{field}` the template names from `**fields`.
- A template naming a field the caller did not pass raises a clear, named error (never silently renders an empty string or `{field}` literal text back to a model).
- For the rotation_alert family specifically: `render("rotation_alert", <name>, **fields)` for each of the six measured call sites (hypothesis's Measured section) returns BYTE-IDENTICAL output to today's hardcoded f-string, for the same field values, for every case the existing `test_rotation_alert.py` suite already exercises.

## Explicitly out of scope

- Any wording change -- this mvp is the mechanism only; a wording change is a separate, later round.
- `harness_template.py` / `extensions/agi/templates/harness/*.toml` -- untouched, different domain (argv construction, not prose).
- Any family other than `rotation_alert` -- T1..Tn migrate the rest of the inventory one family at a time.
- Any human-only string (exceptions, debug logs, test fixtures).

## Falsifier

Any migrated call site's rendered output differs, for any input the current test suite exercises, from the
pre-migration hardcoded output -- byte for byte. A second, parallel prose-loader mechanism appearing instead
of one shared entry point is also a falsifier (the assignment names "ONE loader" explicitly).
