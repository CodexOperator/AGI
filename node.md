---
id: experiment:a00-7ab395d0-77f0ed
mint_id: be62402ad52245d7a950cae2c483f069
type: experiment
parents:
  - hypothesis:l4b23-grid-location-blind
next_edges: []
confidence: 0.9
edited_by: a00-13cf9cc9
evidence_runs:
  - experiment:a00-7ab395d0-77f0ed
  - experiment:a00-0696a133-f021c0
loop: hypothesis:l4b23-grid-location-blind@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 76279c99e8c41573
season: 2
title: A00 7ab395d0 77f0ed
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7ab395d0-77f0ed

## Experiment — GREEN leg of hypothesis:l4b23-grid-location-blind

Per the L4.12 follow-up brief: leave a permanent regression test for the
non-default `location:` payload case, written RED first (watch it fail
against the current code), then make it pass. Previous round
(experiment:a00-0696a133-f021c0, disproved) proved the RED leg empirically
in this repo's config shape: `location=docset` -> `grid.resolve_payload=
False, locations-resolves=True, AGREES NO`. This round lands the fix + test.

## Mechanism (already traced, re-verified by reading code)

- `node_writer.ensure_payload`(node_writer.py:442) / `replace_payload`
  (node_writer.py:487) already call `locations.resolve_payload_path(root,
  ref, location)` — correct, handles arbitrary `locations:`-declared keys
  (and `source_root`/`graph_root`/`repo_root`).
- `grid.resolve_payload` (grid.py:339) took NO `location` parameter; only
  tried `<project>/payloads/<ref>` then `<engine>/<ref>`. Two callers, both
  at grid.py:894 and grid.py:1178, passed only `(root, payload_ref,
  engine_root)`.

## Change (extensions/agi/bin/grid.py)

1. Added `LOCATION_RE` + `parse_location(path)` helper (mirrors
   `parse_payload_ref`): reads the node's `location:` frontmatter field.
2. Gave `resolve_payload` a `location: str | None = None` parameter. When a
   non-default location is given, it resolves via
   `locations.resolve_payload_path(root, ref, location)` — the SAME resolver
   `node_writer` uses — so grid and `write.py create --payload` agree on
   where the payload lives. Returns `(path, <location>)` or None.
3. Default regime (`None` / `source_root`) unchanged: staged-checkout-wins-
   over-engine priority (goal:g6.1) preserved exactly.
4. Threaded `parse_location(p)` into both callers (:894, :1178).
5. Did NOT touch node_writer.py or locations.py (both already correct), and
   did not change the default priority.

## Test added (extensions/agi/tests/test_grid.py)

- `test_non_default_location_payload_resolves_through_locations` — declares
  `locations: {docset: docsets}` in the project config (mirrors this repo's
  own `comms_root: comms/season-2` shape), writes a payload at
  `<root>/docsets/bin/plain.py`, asserts `resolve_payload(root, ref, engine,
  "docset") == (path, "docset")`, and that an absent ref returns None (no
  silent fallback to staged/engine).
- `test_non_default_location_does_not_resolve_to_staged_or_engine` — a
  non-default location is authoritative: a payload present only in staged/
  engine must NOT resolve under `location="docset"`; default call still
  returns `(staged, "staged")`.

## RED-THEN-GREEN, actual output

RED (code temporarily reverted to the 3-arg signature, new tests run):

    test_non_default_location_payload_resolves_through_locations  FAILED
      TypeError: resolve_payload() takes 3 positional arguments but 4 were given
    test_non_default_location_does_not_resolve_to_staged_or_engine FAILED
      TypeError: resolve_payload() takes 3 positional arguments but 4 were given
    2 failed, 104 deselected in 0.36s

GREEN (fix applied):

    python3 -m pytest extensions/agi/tests/test_grid.py -q \
      -k "non_default_location or staged_payload_beats or unresolvable_payload or default"
    4 passed, 102 deselected in 0.18s

Regression sweep (grid + locations + node_writer suites):

    python3 -m pytest extensions/agi/tests/test_grid.py \
      extensions/agi/tests/test_locations.py extensions/agi/tests/test_node_writer.py -q
    250 passed in 15.82s

## Live-breakage audit (brief's report requirement)

Checked every existing build node for a non-default `location:` field:
`grep -rh "^location:" .agi/nodes/build/` finds **9 nodes, all
`location: source_root`**. This repo's config declares `comms_root:
comms/season-2` but no build node uses it yet, so there is no *current* live
breakage — but any future build node recorded under `comms_root` would have
been silently unresolvable through the grid before this fix, and is now
fixed. `parse_location` will pick it up automatically because it reads the
node frontmatter at both call sites (no caller signature change needed).

## Verdict

testable_claim: PROVED red-then-green — the new permanent regression test
failed against the old code (TypeError, location unread) and passes after
the fix; `grid.resolve_payload` and `write.py create --payload`'s
location-aware link_ref now agree for non-default locations. Default
staged-over-engine priority preserved (dedicated test green).

## Agent Notes
GREEN leg: grid.resolve_payload now takes location and resolves non-default payloads through locations.resolve_payload_path (same resolver node_writer uses); added LOCATION_RE + parse_location threaded through both callers; permanent red-then-green regression tests in test_grid.py (RED=TypeError 3-arg, GREEN=pass). Default staged-over-engine priority preserved. 250 tests pass (grid+locations+node_writer). Live audit: all 9 build nodes with location: are source_root; comms_root declared but unused, now supported.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
RED-then-GREEN story now complete: parent review re-ran the two non_default_location tests in the seat tree and confirmed both pass, and confirmed parse_location/resolve_payload(location) + both call sites (:931, :1216) landed. Verdict proved kept (not demoted): evidence_runs cites both this experiment and the prior red-leg disproved experiment, both resolve. 250-test regression sweep accepted on kid report; only the -k non_default_location slice re-run here.
<!-- THOUGHT:END -->

PARENT REVIEW (L4.36 a00-13cf9cc9): accepted as proved. Parents resolve to hypothesis:l4b23-grid-location-blind; verdict taxonomy valid; evidence_runs = [self, experiment:a00-0696a133-f021c0], both exist. Fix verified in tree, tests pass.
