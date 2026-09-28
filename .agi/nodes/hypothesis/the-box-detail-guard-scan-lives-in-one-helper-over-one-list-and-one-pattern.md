---
id: hypothesis:the-box-detail-guard-scan-lives-in-one-helper-over-one-list-and-one-pattern
mint_id: 84053ea2d82944fd820c9a251e644b5c
type: hypothesis
parents:
  - hypothesis:the-anonymize-guard-scans-the-injected-command-lines-not-only-the-manifest
next_edges: []
edited_by: director-engine
scaffold_hash: 40ac6c93efbf58bd
season: 2
testable_claim: test_commands_manifest.py scans for box detail only through _box_detail(root), which holds the file's one label list and one dotted-quad pattern and scans render_manifest(root) exactly as the guard does today; the live guard stays green.
title: The box-detail guard's scan lives in one helper over one list and one pattern (0-credit leaf 1/2 of g1.25.5 C2, green pin)
town: local-maxxing
---
# hypothesis:the-box-detail-guard-scan-lives-in-one-helper-over-one-list-and-one-pattern

## Measured
- the C2 hypothesis (parent) claims ONE helper over both renders plus a mutant test that fails against the manifest-only guard; its
  scope is test_commands_manifest.py only; its ordering gate is C1 (its Measured cites commands.py lines from before EF.89).
- test_commands_manifest.py:856 -- `_BOX_LABELS`; the guard test_rendered_manifest_names_no_box_detail (859-869) scans
  `commands.render_manifest(root)` only (:865): labels at :866, the file's only dotted-quad pattern at :867-868.
- commands.py:262-264 -- render_manifest = json.dumps(manifest(root)); the live render is 151829 B with 0 labels, 0 dotted quads.
- on 66e3dd68c7: `-k "box_detail or operator_verbs or no_spend_spawn"` = 3 passed; C1's gate (:848-855) ends just above :856.
## CLAIM
Test-only, a green pin: `_box_detail(root) -> list[str]` sits right after `_BOX_LABELS` and returns the :866-868 hits (labels, then
"ip:"+address) over `render_manifest(root)` -- the code MOVED, not copied; the guard body becomes
`hits = _box_detail(root); assert hits == [], hits`. Same text scanned, same hits; :848-855 byte-identical.
## Dispatch line
config-max: none / template-max: none / code: none in bin/ -- about 10 test lines
## FALSIFIERS
- a second copy of the list or the pattern, or the helper scanning anything but the manifest (widening is the sibling leaf)
- the guard fails, or a line outside :856-875 changes
## TESTS
test_commands_manifest.py::test_rendered_manifest_names_no_box_detail asserts `_box_detail(root) == []` on the live node -- green
before and after (a pin). Neighbours: test_commands_manifest.py, then test_commands.py, one at a time under env -u TMUX -u TMUX_PANE.
## FILE SCOPE
extensions/agi/tests/test_commands_manifest.py -- read :20-37, :103-106, :846-875
extensions/agi/bin/commands.py -- read :262-264 (read-only)
## CEILING
1 kid under a pi-free parent (STANDARD round: --tier parent --harness pi-free, --harness pi-free on every kid spawn; TMM.89) · 0 production lines · 0 USD · FIRST of two; never while C1's continuation is in flight

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
TMM.89 (owner 02:3xZ via TM: "No more special usd0 runs") retired the pi-local kid lane this CEILING was written for; the round now runs the STANDARD way on the free lane. Only the CEILING harness moved: claim, tests and file scope unchanged.
<!-- THOUGHT:END -->
