---
id: hypothesis:sensei-wake-audit-subcommand
mint_id: c19e36d10dfc4be28d3c6dfd5a75b89a
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: master-sensei
scaffold_hash: 6ce522a116ea4b94
season: 2
testable_claim: "OWNER 2026-09-11 12:4xZ order, master-sensei gen I proposal 4 -- the section 2 measurement this seat's whole duty runs on, currently done by hand every rotation (this session did it by hand twice: once via a forked transcript read of belam gen IX, once implicitly by reading config:rotations' own F1-F5). CLAIM: extensions/agi/bin/sensei.py (verbs: pick_worst/propose/apply; confirmed by grep: no wake-audit/wake_audit anywhere in the file or tree) has no subcommand that runs the classification itself. Add `sensei.py wake-audit --seat <seat> --gen <n> [--transcript PATH]` (transcript path resolved the same way `rotate.py meter --pin` does, from ~/.claude/sessions/<pid>.json, unless given explicitly): parse the seat's rotation-record-linked transcript, list assistant tool_use calls from turn 1 to the first call classifiable as real work, and classify each against that seat's LIVE config:rotations templates.<role>.startup.first_turn entries -- (a) re-derives a fact already in ## facts or a first_turn output, (b) a read a first_turn entry could pre-run but doesn't yet, (c) protocol learning (-h, source/log grepping), (d) real work -- printing counts per category and the raw per-call list. FALSIFIER: a wake this seat has already hand-classified (belam gen IX, this session's fork) where the subcommand's classification disagrees with the hand classification on any call. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/sensei.py (new subcommand only) + tests."
thought_session: master-sensei-gen1
title: sensei.py gains a wake-audit subcommand that runs master-sensei's own core measurement instead of a by-hand transcript read
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:sensei-wake-audit-subcommand

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
