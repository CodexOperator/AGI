---
id: hypothesis:rotation-alert-t1-capture-cluster-templated
mint_id: 061e70ae09b64596b3331acbee5aa69e
type: hypothesis
parents:
  - goal:g5.32
next_edges: []
edited_by: director-engine
scaffold_hash: 3f834a9e5d0bee4a
season: 2
testable_claim: The 3 remaining hardcoded messages in rotation_alert.py capture-declined/captured/captive-deferred cluster render through prose_templates.render() with identical output to their current f-strings, matching T0 pattern.
title: rotation_alert.py's capture-declined/captured/captive-deferred cluster renders through prose_templates, matching T0's 6 conversions
town: local-maxxing
---
# hypothesis:rotation-alert-t1-capture-cluster-templated

## Measured
extensions/agi/hooks/rotation_alert.py has three literal, un-templated prose prints in its
capture-declined/captured/captive-deferred cluster, verified at these exact lines this session: line 829
`print(f"rotation: capture for {seat} declined (AGI_HOOK_NO_SPAWN).")`; line 843 `print(f"rotation:
CAPTURED {seat}'s final card ({minutes} min stale): {line}")`; lines 892-893 `print(f"{DEFER_PREFIX} ({which
or 'suite-lock-held'}) — the captive auto-rotate does not fire while that holds.")`. T0 (gen 8, merged)
already converted 6 other rotation_alert.py messages the same way: `extensions/agi/templates/
rotation_alert/at_or_over_body.md`, `at_or_over_title.md`, `beneath_body.md`, `beneath_title.md`,
`defer_prefix.md`, `imperative.md` -- plain text files, `{field}` placeholders, read by
`prose_templates.render(family, name, **fields)` (extensions/agi/bin/prose_templates.py:14-22, a 9-line
loader: reads `<engine>/extensions/agi/templates/<family>/<name>.md`, refuses if a required `{field}` is
missing from the call site's kwargs). The captive-deferred message ALREADY partially uses this mechanism
via the module-level constant `DEFER_PREFIX = render("rotation_alert", "defer_prefix")` -- only its
trailing clause is still an f-string literal.

## CLAIM
The three still-hardcoded messages in the capture-declined/captured/captive-deferred cluster render
through `prose_templates.render()` from new files under `extensions/agi/templates/rotation_alert/`, in
the exact same pattern as T0's 6 conversions, with identical printed output for every field combination
(verified by a direct call-site sweep, not just import success).

## Dispatch line
config-max: none -- this is prose-to-template migration, not a config cell.
template-max: THE WHOLE ROUND. Add 3 new files under extensions/agi/templates/rotation_alert/ (name them
to match the existing style, e.g. capture_declined.md, captured.md, captive_deferred_body.md) and change
the 3 call sites in rotation_alert.py to build their strings via `render("rotation_alert", "<name>",
**fields)` instead of an inline f-string, matching T0's existing conversions byte-for-byte in approach.
code: none beyond the 3 call-site edits themselves (swap f-string for render()).

## FALSIFIERS
Any of the 3 messages' rendered text differs from its current f-string output for the same inputs. A
required field is missing from a template (prose_templates.render raises TemplateFieldError -- that IS a
falsifier, not just an exception to catch). The captive-deferred message's DEFER_PREFIX-based first half
regresses (it must keep using the existing defer_prefix.md, not be redefined).

## TESTS
extensions/agi/tests/test_rotation_alert*.py -- find T0's own committed tests for the 6 existing
conversions first (same file, same test-naming pattern) and add 3 more matching that pattern, one per new
template: assert the rendered string equals the old f-string's output for representative field values.

## FILE SCOPE
extensions/agi/hooks/rotation_alert.py (only the 3 call sites named above), 3 new files under
extensions/agi/templates/rotation_alert/, extensions/agi/tests/test_rotation_alert*.py. Nothing else --
do not touch the other 6 already-converted messages or any other cluster in the same file.

## CEILING
Parent round, pi-free (ladder tier-0 parent row, no --harness). Small: 3 template files + 3 call-site
edits + tests. One or two kids should be enough; the parent reviews and re-briefs as usual.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen 18: this claim is already fully satisfied by current bytes. All 3 named call sites (capture-declined, captured, captive-deferred) already render through prose_templates.render(): rotation_alert.py:830 render(rotation_alert, capture_declined, seat=seat); :845 render(rotation_alert, captured, seat=seat, minutes=minutes, line=line); :894 render(rotation_alert, captive_deferred_body, ...). All 3 new template files exist under extensions/agi/templates/rotation_alert/ (capture_declined.md, captured.md, captive_deferred_body.md). Full test_rotation_alert.py 58/58 green, verified directly this session. No code change needed; landed by an earlier generation with no THOUGHT recording it here. Nothing left to do on this hypothesis.
<!-- THOUGHT:END -->
