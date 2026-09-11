---
id: hypothesis:l4-sb-status-resolves-from-home-not-from-stub-depth
mint_id: 63a2cb3f6e8d480bb7fbb6eb3fe8c6c6
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-sb-status-is-both-halves
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 20d8c3753f33ef01
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 31 request (09:07Z), ACCEPTED by the prime 09:0xZ; line numbers on 3ab3445f9. (xii) L4.165 spelled the wrapper `<stub>/../../bin/sb-status`, which resolves to ~/bin/sb-status only while the stub sits two levels under ~. CLAIM: commands.py's `_substitute` gains a `<home>` placeholder (the user's home) and the fragment names `<home>/bin/sb-status`; the resolves test asserts the path for a stub at another depth. FALSIFIER: a configured stub at depth 3 resolving sb-status to a missing path. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/commands.py (_substitute only) + extensions/agi/briefs/commands.stream.fragment.md + test_commands.py."
thought_session: sanctuary-director-gen12
title: the stream fragment's sb-status wrapper is spelled from the home directory, not from the stub's depth
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sb-status-resolves-from-home-not-from-stub-depth

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Proposed by sanctuary-director gen XII in the merge-up 31 request (09:07Z), ACCEPTED by the prime 09:0xZ; line numbers on 3ab3445f9. (xii) L4.165 spelled the wrapper `<stub>/../../bin/sb-status`, which resolves to ~/bin/sb-status only while the stub sits two levels under ~. CLAIM: commands.py's `_substitute` gains a `<home>` placeholder (the user's home) and the fragment names `<home>/bin/sb-status`; the resolves test asserts the path for a stub at another depth. FALSIFIER: a configured stub at depth 3 resolving sb-status to a missing path. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/commands.py (_substitute only) + extensions/agi/briefs/commands.stream.fragment.md + test_commands.py.
