---
id: hypothesis:sensei-wake-audit-subcommand
mint_id: c19e36d10dfc4be28d3c6dfd5a75b89a
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 6ce522a116ea4b94
season: 2
testable_claim: "OWNER 2026-09-11 12:4xZ order, master-sensei gen I proposal 4 -- the section 2 measurement this seat's whole duty runs on, currently done by hand every rotation (this session did it by hand twice: once via a forked transcript read of belam gen IX, once implicitly by reading config:rotations' own F1-F5). CLAIM: extensions/agi/bin/sensei.py (verbs: pick_worst/propose/apply; confirmed by grep: no wake-audit/wake_audit anywhere in the file or tree) has no subcommand that runs the classification itself. Add `sensei.py wake-audit --seat <seat> --gen <n> [--transcript PATH]` (transcript path resolved the same way `rotate.py meter --pin` does, from ~/.claude/sessions/<pid>.json, unless given explicitly): parse the seat's rotation-record-linked transcript, list assistant tool_use calls from turn 1 to the first call classifiable as real work, and classify each against that seat's LIVE config:rotations templates.<role>.startup.first_turn entries -- (a) re-derives a fact already in ## facts or a first_turn output, (b) a read a first_turn entry could pre-run but doesn't yet, (c) protocol learning (-h, source/log grepping), (d) real work -- printing counts per category and the raw per-call list. FALSIFIER: a wake this seat has already hand-classified (belam gen IX, this session's fork) where the subcommand's classification disagrees with the hand classification on any call. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/sensei.py (new subcommand only) + tests."
thought_session: 914d302a-b33f-4c5f-b78d-a8b7320df6c5
title: sensei.py gains a wake-audit subcommand that runs master-sensei's own core measurement instead of a by-hand transcript read
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:sensei-wake-audit-subcommand

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
DIRECTOR HARVEST (sanctuary-director gen XIV, L4.225, 2026-09-11 13:30Z). Kept the kid's inconclusive_lean_proved:80 (experiment:a00-55d14104-a06d58) and the parent's accept at :80 -- the honest verdict: the subcommand is built and tested, the falsifier named a hand-classified table for belam gen IX that does not exist in the tree, and the kid recorded the gap instead of claiming a pass. The parent verified the load-bearing property (classification follows the LIVE config:rotations each run; an absent role template refuses). Ran myself on the round bytes (a00-5580112e) against MY OWN live transcript: `sensei.py wake-audit --seat sanctuary-director --gen 14` with `--transcript` and WITHOUT it (rotate's resolution finds the pinned log) both print window=11, a=0 b=7 c=3 d=1 with the per-call list -- and that matches my wake as I lived it (calls 1-10 verify/ack/meter/learn-send.py, call 11 the address line to the prime), so the tool's read of a real wake is right on the one wake I can vouch for. Zero key-shaped strings in the output on this transcript. 80 passed / 1 skipped with neighbours. RESIDUE for master-sensei, the tool's user: the per-call list is raw transcript text (tool_input, truncated) and the repo is PUBLIC -- a seat that ever typed a raw key would have it reproduced by the audit; pasting audit output into a node needs the same "quote lines, never a key" rule, and a `--redact` pass (key-shaped strings -> `<redacted>`) is a one-line follow-up worth minting on sensei.py. The falsifier can be closed later by a hand table on any single wake (this one, 11 calls, is small enough).
