---
id: hypothesis:g5.32-t0-hardcoded-prose-inventory-and-template-loader
mint_id: 4834f24b95ac474d97fb15b01d30f18a
type: hypothesis
parents:
  - goal:g5.32
next_edges: []
confidence: 0.85
edited_by: director-engine
origin: director
scaffold_hash: 9cb9897084d3038b
season: 2
tags:
  - local-maxxing
  - templates
  - director-engine
  - g5.32
testable_claim: Every model-facing hardcoded string across extensions/agi/hooks/ and extensions/agi/bin/ (hook output, CLI refusals/warnings, nudges, reminders -- not human-only logs/exceptions/fixtures) is listed file:line+family+fields in ONE committed inventory doc, and a single extensions/agi/templates/<family>/ loader exists, proven byte-identical against rotation_alert.py's title/band/imperative/defer strings before any wording change lands.
title: "T0: inventory every model-facing hardcoded string, build the ONE template loader, migrate rotation_alert.py first (assigned: director-engine, goal:g5.32)"
town: local-maxxing
---
# hypothesis:g5.32-t0-hardcoded-prose-inventory-and-template-loader

# hypothesis:g5.32-t0-hardcoded-prose-inventory-and-template-loader

**Assigned: director-engine.** TMM.121, owner order 16:20Z 09-24 via thought-master (verbatim): "make
director-engine do a pass on all the hardcoded prose warnings sent back to models in every build node and
put them all into templates that get loaded in dynamically." First round under goal:g5.32.

## Measured

- `extensions/agi/hooks/rotation_alert.py:291` — `AT_OR_OVER_TITLE = "## ⚠️  ROTATION OWED NOW — at or over the line"`
- `extensions/agi/hooks/rotation_alert.py:298` — `BENEATH_TITLE = "## ⚠️  approaching rotation"`
- `extensions/agi/hooks/rotation_alert.py:293` — `IMPERATIVE = ("ROTATE NOW: (a) write the card wholesale now, (b) run python3 " ...)`
- `extensions/agi/hooks/rotation_alert.py:472` — `DEFER_PREFIX = "rotation deferred: merge-up in flight"`
- `extensions/agi/hooks/rotation_alert.py:1496-1499` — the at-or-over-line f-string body (`_emit(AT_OR_OVER_TITLE, "This session is at or over its rotation line. Rotate NOW. ..." + suffix)`)
- `extensions/agi/hooks/rotation_alert.py:1535-1539` — the beneath-the-line band f-string, freshly worded by E0 (merged `6c33e4d01e`, cherry-picked to trunk `37f1812f52`): `f"Approaching rotation ({fraction:.4f} of {threshold:.3f} window ..." + "Keep working; at the line run rotate.py rotate yourself."`
- These are ALL model-facing (the SessionStart/UserPromptSubmit hook output every agent reads every turn) and ALL inline Python literals today — zero of them are in a template.
- **Corrected 2026-09-25 (director-engine, PASS 5 residue demote):** the six lines above are the ORIGINAL T0 measurement and its migration landed (verdict=proved, commit `18c334c35e`) — but the surface has since grown. `extensions/agi/hooks/rotation_alert.py` now has NINE `render("rotation_alert", ...)` call sites, not six: the original six (lines 293, 294, 297, 299, 1494, 1532) plus three landed later (`capture_declined` L830, `captured` L845, `captive_deferred_body` L894). Verified directly by grep against current bytes, not assumed.
- Precedent already on trunk: `extensions/agi/templates/harness/*.toml` + `extensions/agi/bin/harness_template.py` is a DIFFERENT loader (declarative argv-building vocabulary for spawning a harness process, TOML, closed key vocabulary) under the SAME `extensions/agi/templates/<family>/` directory convention. Reuse the directory convention and the "closed vocabulary, no eval/exec" discipline; do NOT reuse harness_template.py's argv-specific loader code for prose (wrong domain — this is free text with placeholders, not an argv element list).
- No inventory of the rest of the surface exists yet (dispatch.py's stale-base/refusal messages, send.py's nudge/stranded text, cli.py's refusals, other hooks) — this round's FIRST deliverable is that inventory, not just the migration.

## CLAIM

Every model-facing hardcoded string across `extensions/agi/hooks/` and `extensions/agi/bin/` (text a MODEL
reads: hook output, CLI refusals/warnings, nudges, reminders — NOT human-only logs, exceptions or test
fixtures) is listed in ONE committed inventory doc (file:line, family, the fields/placeholders it needs),
AND a single template-loader mechanism exists under `extensions/agi/templates/<family>/` with ONE render
function, proven BYTE-IDENTICAL against `rotation_alert.py`'s existing title/band/imperative/defer strings
(the "rotation_alert" family) before any wording changes are allowed to land. Wording changes are explicitly
OUT OF SCOPE for this round.

## Dispatch line

template-max: every model-facing literal in a build node moves to `extensions/agi/templates/<family>/<name>.md`
(or `.txt`), with `{placeholder}` fields filled at the call site. code: the ONE loader/render function does
not exist yet for prose (only the argv-building one does) and must be written once, reused by every family.

## FALSIFIERS

- A migrated string's rendered output differs from the pre-migration hardcoded output for ANY of the inputs
  the existing tests already exercise (byte-for-byte) — the byte-identical constraint is violated.
- A SECOND loader/render function is introduced instead of extending or sitting beside the one this round adds.
- The inventory omits a model-facing literal that is trivially greppable in `extensions/agi/hooks/` or
  `extensions/agi/bin/` (spot-checked against the six measured lines above — all six must appear as rows).
- A human-only string (an exception message, a debug log line never shown to a model, a test fixture) is
  migrated — out of scope, and pads the inventory with rows that will never close.

## TESTS

- New: one byte-identical render test per migrated string in the rotation_alert family — call the new loader
  with the SAME field values the current call sites pass, assert the output string equals today's f-string
  output exactly (character-for-character), for `AT_OR_OVER_TITLE`, `BENEATH_TITLE`, `IMPERATIVE`,
  `DEFER_PREFIX`, the at-or-over body, and the beneath-band body.
- Existing: `python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q` must stay fully green after the
  migration (57 passed today) — the hook's OWN behavior does not change, only where the strings live.

## FILE SCOPE

- New: `extensions/agi/templates/rotation_alert/*.md` (or `.txt`) — one file per migrated string.
- New: ONE new loader module (e.g. `extensions/agi/bin/prose_templates.py` or a name the kid picks and states
  plainly) with a single `render(family, name, **fields) -> str` entry point.
- New: `.agi/context/local-maxxing/g5.32-hardcoded-prose-inventory.md` — the committed inventory table
  (columns: file, line, family, fields/placeholders, status={still-in-code|migrated}), covering
  `extensions/agi/hooks/*.py` and `extensions/agi/bin/*.py` at least for every literal a grep for
  print/f-string/`_emit`-style calls surfaces.
- Changed: `extensions/agi/hooks/rotation_alert.py` — the SIX measured lines above call the new loader instead
  of holding literals; no other behavior change.
- Nothing else. Do not touch `dispatch.py`, `send.py`, other hooks, or any config: node this round — they are
  inventory ROWS only (status: still-in-code), migrated in T1..Tn.

## CEILING

- kids only (`--tier kid --harness pi-free`, TMM.107(3), no parent tier).
- Loader module: keep it small and boring (a `Path.read_text` + `str.format`-style substitution is enough;
  no template engine dependency, no eval/exec — mirror harness_template.py's "closed vocabulary, no eval" rule
  even though the vocabulary itself is new).
- Production diff on `rotation_alert.py` itself: the six call sites only, no other refactor.
- USD cap: pi-free per-spawn mint ceiling ($1.00), one round.
- The inventory doc is NOT production code and is not line-capped, but stay to the two directories named
  above — a whole-repo sweep is T1..Tn's job, not this round's.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PASS 5 chunk 1 (belam-S2-L5-V, 09-25) demoted a round against this hypothesis for three reasons: "the inventory
misses the claimed surface and its statuses contradict the code; an out-of-scope wording change in
templates/rotation_alert/beneath_body.md; call sites drifted 6 -> 9". Assigned to director-engine to correct
this node in place. Verified each claim against current bytes rather than taking the review on faith:
1. Call-site drift (6 -> 9): CONFIRMED. Corrected in Measured above with exact current line numbers.
2. Statuses contradict the code: CONFIRMED and FIXED directly in
   `.agi/context/local-maxxing/g5.32-hardcoded-prose-inventory.md` — its capture-declined/captured/
   captive-deferred rows said "still-in-code" while the actual call sites already used `render(...)`
   (landed by whatever round added those three templates at 21:43, after the original six at 17:04; the
   inventory table was simply never updated to match). Also flagged, in the inventory doc itself, that its
   `extensions/agi/bin/*.py` coverage is placeholder-depth (stub rows, not a real per-file sweep) — this part
   of "misses the claimed surface" is real and still open, left for a T1 round rather than fabricated here.
3. Out-of-scope wording change in beneath_body.md: DOES NOT REPRODUCE against current bytes. Directly
   computed both the pre-migration f-string (`git show 37f1812f52`) and the current
   `render("rotation_alert","beneath_body", ...)` output with identical inputs (fraction=0.31245,
   threshold=0.47, pct=66) — byte-identical, `MATCH: True`. The call site
   (rotation_alert.py:1532-1534) passes `percent=fraction/threshold * 100`, exactly the pre-migration inline
   expression. Either this was a real defect in an earlier revision that has since been fixed by another
   commit, or the review finding was itself mistaken; either way it is not something a future round should
   spend budget chasing without first re-checking, which is why this THOUGHT records the check rather than
   just the verdict.
No wording changed by this correction pass; only the inventory doc's status cells and this node's own stale
Measured claim. The remaining real gap (bin/ coverage) is not closed here — noted, not hidden.
<!-- THOUGHT:END -->
