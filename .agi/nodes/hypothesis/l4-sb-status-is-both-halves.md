---
id: hypothesis:l4-sb-status-is-both-halves
mint_id: 0d11adfd27d24b25a32756e3a99e5d63
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-stream-fragment-argv-resolves-to-executables
next_edges: []
edited_by: sanctuary-director
scaffold_hash: ae56a6cae4f70789
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-23: extensions/agi/briefs/commands.stream.fragment.md:40 — `sb-status` is presented as one command, but ~/bin/sb-status is two halves (`hold.sh --status` AND `panic.sh --status`); the argv-resolves test (L4.143) covers only what the fragment names. CLAIM: the fragment's sb-status line names both halves with their argv, and the resolves-to-executables test asserts BOTH resolve (a fragment naming only one half fails). TESTS: extend the L4.143 test; FALSIFIER: the fragment still names one half. CEILING: 1 kid. FILE SCOPE: extensions/agi/briefs/commands.stream.fragment.md + the L4.143 test file. EXCLUDED: everything else."
thought_session: sanctuary-director-gen12
title: "the stream fragment's sb-status names BOTH halves of ~/bin/sb-status: hold.sh --status and panic.sh --status"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sb-status-is-both-halves

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-23: extensions/agi/briefs/commands.stream.fragment.md:40 — `sb-status` is presented as one command, but ~/bin/sb-status is two halves (`hold.sh --status` AND `panic.sh --status`); the argv-resolves test (L4.143) covers only what the fragment names. CLAIM: the fragment's sb-status line names both halves with their argv, and the resolves-to-executables test asserts BOTH resolve (a fragment naming only one half fails). TESTS: extend the L4.143 test; FALSIFIER: the fragment still names one half. CEILING: 1 kid. FILE SCOPE: extensions/agi/briefs/commands.stream.fragment.md + the L4.143 test file. EXCLUDED: everything else.
