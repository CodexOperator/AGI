---
id: hypothesis:l4-the-stops-slot-is-located-by-title-only-created-when-absent-and-dry-run-prints-the-resolved-slot
mint_id: 7282f4fbc2fa4820bf8c8fb025d3b486
type: hypothesis
parents:
  - goal:g15.25
  - hypothesis:l4-the-predecessor-answers-the-ack-and-rotate-out-is-one-signed-call
next_edges: []
edited_by: sensei-director
scaffold_hash: 0936cd29e1f3af64
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node, mur-SL2.16 (Prime XV 08:06Z, by name) line (1) — the SL7.12 demotion. Cite lines at 2451606d0 (the Prime's measurement); re-measure on your base. MEASURED: `_locate_where_it_stops` step 3 (rotate.py 4835-4839) falls back to ANY `## ` header carrying the numeral §3 when no where-it-stops TITLE matches, and `_write_stops_section` (10147) REPLACES that block in place instead of creating the slot at the card end — on `.agi/sessions/quorum/master-sensei.md` (`## §3 FLOOR`, an owner fence) and `stream-master.md` (`## §3 STANDING RULES`) one `rotate-self --stops` would overwrite owner-verbatim and push it in the same call; `--dry-run` prints only the card path, never the slot it resolved; and the `###`-path end-of-block scan (10138) treats ANY `#`-prefixed line — a `# comment` inside a code fence — as the next heading, truncating the replaced block. Interim guard on MAIN 0a84197ba appended a titled slot to both cards; this node makes the guard unnecessary. CLAIM: (a) the numeral fallback is DELETED: the slot is located by TITLE only (`where it stops` / `Where it stops` in a `##`/`###` header, as `_locate_where_it_stops` steps 1-2 do), and when no titled slot exists `_write_stops_section` CREATES one at the card end (`### 🔴 Where it stops — the next command (stamp <HH:MMZ>)` + the stops line) — never a replace of an untitled block; (b) `--dry-run` prints the RESOLVED action: `stops slot: <header line> (replace)` or `stops slot: none — will append at end`, plus the card path; (c) the end-of-block scan on the `###` path stops only at a real markdown heading OUTSIDE a fence (track ``` fences; a `#`-prefixed line inside a fence is content); (d) tests: a fixture card whose only §3 header is `## §3 FLOOR` followed by owner-verbatim → after `--stops`, that block is byte-identical and a titled slot exists at the end; a card with a titled `###` slot whose block contains a fenced `# comment` → the whole block up to the next real heading is replaced; `--dry-run` output asserted for both. FALSIFIERS: any `## §3 …` block without the title changes bytes; a fenced `#` line ends a block; `--dry-run` prints no resolved slot; any existing SL7.12 test changes assertion beyond the numeral-fallback one. TESTS: test_rotate*.py test_session_start*.py test_bin_help_smoke.py with neighbours. RULES: merge, never rebase; the interim guard slots on MAIN stay (harmless titled slots); FILE SCOPE: rotate.py `_locate_where_it_stops`, `_write_stops_section`, the `###` end-of-block scan, the rotate-self --dry-run print; tests. EXCLUDED: `_stops_push`, captive-4, `--stops-file`/stdin (line (2) sibling), cmd_rotate_self's ask_gate/read-backs (SL7.18), the own-row cut (SL7.20), cmd_spawn (SL7.21), hooks (SL7.23), the record entries (brief I). CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genIX-L9
title: "the where-it-stops slot is located by TITLE only (the numeral fallback deleted), created at the card end when absent, --dry-run prints the resolved slot, and a fenced # line never ends a block"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-stops-slot-is-located-by-title-only-created-when-absent-and-dry-run-prints-the-resolved-slot

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
