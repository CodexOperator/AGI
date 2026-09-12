---
id: hypothesis:l4-sensei-py-calls-lists-a-transcripts-tool-calls-so-no-post-copies-a-scratchpad-script-at-spawn
mint_id: 20c27d913d5f4625b2e0d57ff4a116a1
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 0346094b8be41328
season: 2
testable_claim: "goal:g15 FIX-ONLY node (owner order 15:4xZ relayed by master-sensei gen 4 (15:41Z; verbatim at doc:l4-owner-decisions latest note); cite at seat tip 290644b2b, re-measure on your base. line (2)). MEASURED: sensei.py carries cmd_wake_audit (:1241, parser :1652) but the LISTING script the audit is built from — one line per tool call: n, timestamp, tool, command[:150], with user-turn boundaries marked — lives in a scratchpad and is copied by hand at every master-sensei spawn = one class-(a) call per generation; wake-audit itself under-counts (a fix already routed by the Sensei, EXCLUDED here). CLAIM: a sibling subcommand `sensei.py calls <transcript.jsonl> [--from N] [--to M] [--width 150]` prints exactly that listing from a Claude Code transcript (assistant tool_use blocks in order, user turns as boundaries), no network, no scratchpad; the Sensei's card drops the copy step. FALSIFIERS: the listing differs from the scratchpad script's on the same transcript (count or order); a transcript with no tool calls errors instead of printing zero lines; the subcommand imports anything outside the stdlib + sensei.py's existing helpers. TESTS: test_sensei.py — a fixture transcript with three calls across two user turns lists 3 lines with one boundary; width truncation; empty transcript. FILE SCOPE: extensions/agi/bin/sensei.py — one subcommand + parser entry; extensions/agi/tests/test_sensei.py. EXCLUDED: cmd_wake_audit's counting, the drafts dir, the audit prose. CEILING: one subcommand, three tests."
thought_session: sensei-director-genXIII-L13
title: sensei.py calls <transcript> prints the per-call listing (n · ts · tool · command[:150], user-turn boundaries) that the wake audit reads, next to wake-audit, so no master-sensei spawn copies a scratchpad script
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-sensei-py-calls-lists-a-transcripts-tool-calls-so-no-post-copies-a-scratchpad-script-at-spawn

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
