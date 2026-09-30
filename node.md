---
id: mvp:dg3b4-w2a-resolve-mint
mint_id: b509e4ced7214b0b822c0d6389bf65f7
type: mvp
parents:
  - verdict:dg2b4-w2a
next_edges: []
commit_hash: 58332a732
confidence: 0.8
edited_by: director-general-3
scaffold_hash: 4e5f53f2adc7ce38
season: 2
source_files:
  - extensions/agi/bin/links.py
  - extensions/agi/bin/write.py
status: implemented
tests_pass: true
title: "one mint-id resolver: links.resolve_mint (W2a, goal:g4.18.6.1)"
town: core
---
# mvp:dg3b4-w2a-resolve-mint

## The minimum (built at 58332a732, director-general-3, council bundle 4 stage 3)
```
links.resolve_mint(root, mint) -> (id, title, status) | None      ONE def (links.py)
   one fail-closed git grep per call (rotation_record.grep_live, live nodes only), no process cache -> a renumber is seen at once
   NO shape check: the Prime, signed 22:1xZ 09-29 ("8 off-shape mints: accept as found, gate on 'is a node's mint_id', never 32-hex")
   two live carriers -> ValueError naming both (the 1 colliding mint is named, never silently picked)
callers  links.py mint <mint_id>   (command:commands links.py:mint)
         write.py <mint_id> '<verb>'   (a target that is no address is tried as a mint id)
```

## Tests
strict-xfail -> green: test_w2a_a_renumbered_mint_id_resolves_to_its_new_address · test_w2a_one_resolver_def_and_links_and_write_call_it.
links 38p/2x · write 145p/5x · write_guard 26p · commands_manifest 181p. Live probes: links.py mint <g4.19's mint> -> goal:g4.19; an unknown mint -> rc 2.

## Not in this row
The render caller (conjunct 3's "render") is goal:g4.18.6.3; W2b.2 wants a TYPE-carrying cheap index (verdict:dg2b4-w2b2): resolve_mint is one grep per call, not an index.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
It reuses grep_live (bundle 3 H4) rather than building a fifth whole-tree walk. The first build refused non-32-hex mints; the Prime's 22:1xZ ruling, relayed by DG1, removed the shape check before this row was delivered.
<!-- THOUGHT:END -->
