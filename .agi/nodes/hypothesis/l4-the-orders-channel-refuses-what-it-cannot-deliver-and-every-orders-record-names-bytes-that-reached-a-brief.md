---
id: hypothesis:l4-the-orders-channel-refuses-what-it-cannot-deliver-and-every-orders-record-names-bytes-that-reached-a-brief
mint_id: 33ab2b0f9154498e95029bbcf32adaca
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: b54151f2fd76e71a
season: 2
testable_claim: "goal:g15.25 SM.28 (SM review of SL2#31 @a74adb9af, 01:3xZ: the --orders channel (SM.26, accepted :70) has four accept-and-drop or record-without-delivery seams — the class the l4b23 --prompt-file refusal exists to prevent). MEASURED on season2/main @a74adb9af: dispatch.py:1108-1112 accepts --orders at --tier director and drops it rc 0 (file never read, no heading, no note); brief.py:1897-1899 (survival profile) and :1911-1924 (advisor route, measured end-to-end --harness claude-code --ladder-tier 3) return before the parent branch, so the brief carries NO orders while the dry-run report (:1267-1272) prints orders: N lines and the manifest gate (:2510, tier==parent) records {from,sha256,bytes,path} — record says delivered, brief does not; brief.py:1832 truthiness gate renders `## DISPATCH ORDERS` with a blank body for a whitespace-only file and copies/records it; dispatch.py:1974-1975 writes <iter>/orders.md as ONE unmerged file per iter dir while the manifest (:1978-1994) merges parents — a second parent dispatch, even one refused at :2049 rc 1, overwrites it, and a refusal after :1975 leaves orders.md with no manifest.json. CLAIM: (1) --orders at a tier that neither threads nor carries it forward is REFUSED BY NAME, exit 2, naming the tier and the two tiers that accept it — never accepted-and-dropped; (2) an orders record is written ONLY when the assembled brief carries the section: the survival and advisor routes either render the section (same helper, same heading, last segment) or refuse --orders by name before the manifest gate — dry-run line, manifest record and brief agree on every route; (3) the presence gate is text.strip() — a whitespace-only file = absent (no heading, no copy, no record, byte-identical brief) while a non-empty file is still rendered VERBATIM (no strip on render); (4) <iter>/orders.md is per-parent: <iter>/orders.<agent>.md keyed like the manifest parent record, written AFTER the last refusal gate so a refused dispatch leaves no orphan file, and the manifest path cell names it; (5) a missing --orders path is a named refusal (exit 2), not a FileNotFoundError traceback (:1082/:1114), and the recorded path is absolute. FALSIFIERS: any route where the manifest carries orders and the brief does not; any tier that accepts --orders with rc 0 and no section; a heading with a blank body; two parents sharing one orders.md. TESTS (test_dispatch_dry_run.py + test_brief.py, <= 6): tier director → refusal names parent|kid; advisor route with --orders → section present (or refusal) AND manifest agrees, asserted from the manifest file not a stub; whitespace-only → byte-identical + no record; two parents → two files, second refused → first intact; missing path → named refusal. FILE SCOPE: dispatch.py (tier gate, manifest gate, orders file naming, path refusal), brief.py (route helpers + strip gate), the two test files. CEILING: <= 40 production lines, ONE kid — RE-BRIEF before any kid past 2x (SM.26 went 3.1x un-briefed; that is the demote rule, not a suggestion). Wording residue for the kid THOUGHT block, not code: parent --prompt-file refusal is RETAINED beside the thread (:1663-1679); dry-run prints 2 content lines; CRLF is LF-translated before hashing; adapters append skill_prompt after the segments."
title: L4 the orders channel refuses what it cannot deliver and every orders record names bytes that reached a brief
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-orders-channel-refuses-what-it-cannot-deliver-and-every-orders-record-names-bytes-that-reached-a-brief

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.28 reviewed by name (mur-sl2-33): ACCEPT with residue. All five conjuncts MET on the bytes at c36f471ed; kid2 fixed the mechanism, assertions not loosened (refuter reproduced). Residue, outside the parent seam: at kid tier the --orders carry-forward alias keeps a plain truthiness gate (dispatch.py:1093-1094 -> brief.py:1303-1312), so a whitespace-only orders file renders the WHAT THE LAST KID PRODUCED label with an empty body - follow-on, one test.
