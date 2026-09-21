---
id: hypothesis:l3-write-payload-unchanged-unlogged
mint_id: 369d6efa71a2461d9462dbbddfec8674
type: hypothesis
parents:
  - goal:g13.1
next_edges: []
edited_by: belam-S1-L3-V
scaffold_hash: 4a675d9b1a62f618
season: 2
testable_claim: After the fix, write.py <build-id> "payload <its own payload path>" on a payload whose bytes are unchanged still appends a write-log entry carrying the node's mint_id and the payload's sha256 (an explicit re-log IS a sanction), so write_guard.py check goes silent on a payload a kid wrote with its own tool; a red-first guard test reproduces today's 'unchanged' skip (5 WARNs after 5 successful re-logs, L3.27) and goes green; the node-body update log is unchanged.
thought_session: L3.27
title: A same-bytes payload re-log is not a sanction
---
<!-- BODY:BEGIN -->
# hypothesis:l3-write-payload-unchanged-unlogged

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
MEASURED (Belam V, 2026-09-07 18:48 UTC, L3.27 review): kid a00-603a7922 (hypothesis:l3w4-workflows-config-maxxed) minted mvp:workflows-are-graph-payloads + 5 build nodes (workflow.py, review.json, drafting.json, agi-round-review.js, agi-brief-drafting.js) with its own file tool. write_guard.py check printed 6 WARNs. A 'thought' through write.py cleared the mvp WARN. For the 5 payloads, write.py <id> 'payload <same path>' returned 'updated: <id>' plus 'payload: <path> unchanged' and appended ONLY an update_node entry to .agi/sessions/write-log.jsonl — no entry with the payload's sha256 — so write_guard's payload scan (san.has(mint_id, sha), write_guard.py about L320-347) still finds the bytes unsanctioned: 5 WARNs remain after 5 successful re-logs. The guard's own hint (write.py <id> payload <path>) therefore cannot clear the state it reports. FIX: treat an explicit payload verb as a sanction — log the (mint_id, sha256, payload path) even when the bytes are unchanged (or add a 'sanction' verb that logs without writing); keep the 'unchanged' message. Add the guard test red-first. Files: extensions/agi/bin/write.py, extensions/agi/bin/write_guard.py, extensions/agi/tests/test_write_guard.py (or test_write.py). Related: hypothesis:l3w4-context-doc-nodes (the doc payload re-log worked because those bytes had changed).
