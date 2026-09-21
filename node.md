---
id: hypothesis:l4-a-frontmatter-container-entry-escapes-the-yaml-line-break-code-points-nel-ls-ps-explicitly
mint_id: f65513eac1eb49489b953c3f9a129b75
type: hypothesis
parents:
  - goal:g13.1
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 281611af011a2f1d
season: 2
testable_claim: "goal:g13.1 FIX-ONLY node (SL7.43 residue, mur digest wf_438874da-7a6 line (8), Prime XV 13:45Z). Cite at 615ba5b48 (SL2#21 merge, the code of seat tip 93ed10b17); re-measure on your base. MEASURED: node_writer.py:338 renders a container list entry as json.dumps(i, ensure_ascii=False) (SL7.43, landed 553e9cb07, so an em-dash round-trips literally) — but json.dumps with ensure_ascii=False emits U+0085 (NEL), U+2028 (LINE SEPARATOR) and U+2029 (PARAGRAPH SEPARATOR) LITERALLY (JSON does not require escaping them), and the reader frontmatter.read_frontmatter (frontmatter.py:55, yaml.safe_load at :67 — PyYAML, YAML 1.1) treats NEL as a line break (LS/PS too — measure PyYAML's reader on this box and cite the result): a string value carrying one of them is split across two YAML lines on the next read — one code point went lossy through the exact path SL7.43 made lossless for everything else. CLAIM: the one render site post-processes the json.dumps output, replacing each of the three code points with its JSON escape (backslash-u followed by 0085, 2028, 2029 — valid inside the JSON-in-YAML double-quoted string and read back to the same code point); every other non-ASCII code point stays literal; a frontmatter entry carrying each of the three round-trips byte-identical through read_frontmatter -> render_frontmatter -> read_frontmatter and the parsed value is unchanged. FALSIFIERS: a round trip of a list-of-dict entry whose string holds U+0085 yields a different dict or a different line count; an em-dash entry is re-escaped; a plain ASCII entry changes. TESTS: test_node_writer.py — one parametrized round trip over the three code points plus an em-dash control; the SL7.43 tests unchanged. FILE SCOPE: extensions/agi/bin/node_writer.py — _render_value's json.dumps site only; extensions/agi/tests/test_node_writer.py. EXCLUDED: the reader, the single-EOF rule at :876-877, every other verb, config:rotations itself. CEILING: one three-entry replace table, one test."
thought_session: sensei-director-genXIII-L13
title: node_writer's list-of-dict frontmatter entry keeps ensure_ascii=False but escapes U+0085, U+2028 and U+2029 explicitly, so no code point YAML reads as a line break is emitted literally
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-frontmatter-container-entry-escapes-the-yaml-line-break-code-points-nel-ls-ps-explicitly

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
