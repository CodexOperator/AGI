---
id: hypothesis:a-box-label-in-an-about-a-reason-shadows-fails-the-guard
mint_id: eb47020fa216472f90a1d844d80bbb50
type: hypothesis
parents:
  - hypothesis:the-anonymize-guard-scans-the-injected-command-lines-not-only-the-manifest
next_edges: []
edited_by: director-engine
scaffold_hash: 4d4337a8488ad40a
season: 2
testable_claim: Once _box_detail also scans the render_for_injection lines, it names a box label and an address planted in a tmp node's about that a manifest reason shadows, though the manifest carries neither.
title: "The guard helper also scans the injected command lines: box detail in a reason-shadowed about fails it (0-credit leaf 2/2 of g1.25.5 C2)"
town: local-maxxing
---
# hypothesis:a-box-label-in-an-about-a-reason-shadows-fails-the-guard

## Measured
- commands.py:228 -- `purpose = purpose or reason or <about>` (the about arrives at :249-252): an about behind a reason never
  reaches render_manifest.
- commands.py:526-559 -- render_for_injection prints every `commands:` about (:549-550, :555-556); briefing.py:274-276 and
  :336-337 put those lines into INJECTION.md; test_commands.py:177-193 checks only content, on a synthetic node.
- commands.md: 2 of 23 `commands:` entries are shadowed today (mesh-gw: about :194 / reason :2743; verify-suite: :116 / :3004); the
  live manifest carries neither about. The frontmatter (:1-3146) has 0 labels and 0 quads, so the widened live guard stays green.
## CLAIM
`_box_detail` loops over `render_manifest(root)` AND `"\n".join(commands.render_for_injection(root))` with the same list and
pattern. A new test writes a tmp node in the `_synthetic` shape (:109-140): `commands: probe` with an argv and an about carrying
`_BOX_LABELS[0]` plus an RFC 5737 TEST-NET-1 address joined from its parts at runtime, and a shadowing
`manifest: probe: {side_effects: read, proposable: false, reason: ...}`; it asserts "probe" is in manifest(graph), render_manifest
carries neither token, and `_box_detail(graph)` names both. Nothing changes in bin/ or in the live node.
## Dispatch line
config-max: none / template-max: none -- the abouts stay the node's / code: none in bin/ -- the guard reads the second render
commands.py already produces; about 30 test lines
## FALSIFIERS
- the test passes on the sibling leaf's bytes, or fails after; the live guard fails (fix the data, never exempt a token)
- a token outside tmp_path (live node, commit message, dm), a literal dotted quad or box label committed, or a second list / pattern
- a change outside FILE SCOPE; test_commands.py red
## TESTS
test_commands_manifest.py::test_the_guard_names_box_detail_in_an_about_a_reason_shadows(tmp_path), inserted right after the guard:
red on the sibling leaf's bytes (record that run as a probe), green after. Neighbours: test_commands_manifest.py, test_commands.py.
## FILE SCOPE
extensions/agi/tests/test_commands_manifest.py -- read :109-140 + the helper and guard (~:856-880)
extensions/agi/bin/commands.py -- read :223-264, :526-559 (read-only)
.agi/nodes/.geometry/commands.md -- read :188-195, :2740-2743 (read-only)
## CEILING
1 kid under a pi-free parent (STANDARD round: --tier parent --harness pi-free, --harness pi-free on every kid spawn; TMM.89) · 0 production lines · 0 USD · SECOND (after the helper leaf merges); never while C1's
continuation is in flight

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
TMM.89 (owner 02:3xZ via TM: "No more special usd0 runs") retired the pi-local kid lane this CEILING was written for; the round now runs the STANDARD way on the free lane. Only the CEILING harness moved: claim, tests and file scope unchanged.
<!-- THOUGHT:END -->
