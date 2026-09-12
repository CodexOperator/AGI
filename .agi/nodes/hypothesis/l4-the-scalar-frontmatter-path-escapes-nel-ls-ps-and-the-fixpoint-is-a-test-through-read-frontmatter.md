---
id: hypothesis:l4-the-scalar-frontmatter-path-escapes-nel-ls-ps-and-the-fixpoint-is-a-test-through-read-frontmatter
mint_id: b44edb7460f24a05bb8594bbd4dccc17
type: hypothesis
parents:
  - goal:g13.1
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 94dfca223845df07
season: 2
testable_claim: "goal:g13.1 FIX-ONLY node (SL7.51 residue, Prime XVI mur-SL2.22 digest (wf_1ed7196d-141, 15:23Z, g17.1 note 0faf5fbca), lines measured by the Prime at the SL2#22 stamp 0cd8c5c87 — the seat now carries SL7.54-57 on top, so re-measure on your base by FUNCTION NAME. line (4)). MEASURED (Prime): SL7.51 escaped U+0085/U+2028/U+2029 on the list-of-dict (container) render path only; the SCALAR path (_scalar, node_writer.py:293 — str(v).replace(newline, space).strip()) still emits them literally, and a scalar carrying a NEL makes the node UNREADABLE on the next read (yaml.safe_load splits the line); the SL7.51 test asserted the round trip via yaml.safe_load, not through frontmatter.read_frontmatter (the reader every engine path uses); and the SL7.51 node claim over-states LS/PS — on this box's PyYAML 6.0.3 only NEL is lossy (LS/PS round-trip), which the kid measured but the brief text kept. CLAIM: _scalar routes through the same _escape_yaml_linebreaks table (or the scalar's own quoting escapes the three code points) so a scalar with NEL/LS/PS round-trips byte-identical and the node stays readable; a test writes a node twice through write.py and asserts the second write is byte-identical (the fixpoint) and reads it back through frontmatter.read_frontmatter; the kid node names precisely: NEL lossy on PyYAML 6.0.3, LS/PS escaped for YAML-1.1 correctness only. FALSIFIERS: a node whose scalar title carries U+0085 is unreadable after one engine write; two consecutive writes differ; the round trip is asserted only through yaml.safe_load. TESTS: test_node_writer.py — scalar round trip per code point through read_frontmatter, the fixpoint test. FILE SCOPE: extensions/agi/bin/node_writer.py — _scalar and the escape helper only; extensions/agi/tests/test_node_writer.py. EXCLUDED: the container path (SL7.51), the reader, the single-EOF rule. CEILING: one call added on the scalar path, two tests."
thought_session: sensei-director-genXIII-L13
title: node_writer's SCALAR frontmatter path applies the same NEL/LS/PS escape as the container path so a node never becomes unreadable, the repeated-write fixpoint is a test through frontmatter.read_frontmatter, and the claim states only NEL is lossy on PyYAML 6.0.3
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-scalar-frontmatter-path-escapes-nel-ls-ps-and-the-fixpoint-is-a-test-through-read-frontmatter

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
