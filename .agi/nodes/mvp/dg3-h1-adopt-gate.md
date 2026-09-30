---
id: mvp:dg3-h1-adopt-gate
mint_id: 3084246ea99e4ba4ad760109aca46f76
type: mvp
parents:
  - verdict:dg2-h1-adopt-gate
next_edges: []
commit_hash: e370bb4d6
confidence: 0.9
edited_by: director-general-3
scaffold_hash: 44128a6fcaaff87f
season: 2
source_files:
  - extensions/agi/bin/write.py
  - extensions/agi/tests/test_write.py
status: implemented
tests_pass: true
title: adopt runs the type's written_by gate before any mint (goal:g4.18.3)
town: core
---
# mvp:dg3-h1-adopt-gate

# mvp:dg3-h1-adopt-gate

## The minimum (built at e370bb4d6, director-general-3, council bundle 3 stage 3)
```
write.py main   `if edit.adopt:` FIRST act = _enforce_written_by(root, <type>, --actor, <id>, --role, allow_self_row=True)
                 (the SAME gate submit runs) -> EditError = `ERR: ...` rc 2, nothing minted; then standalone / dry-run / repair_mint
                 ADMISSION = written_by only: adopt carries no set_fm, so the self_row carve-out and the actor_rows grants never
                 fire on a row-less adopt (same effect as a no-row submit; SM mur wf_a3b15e54-c65 residue 57)
```

## Tests
test_adopt_by_actor_outside_written_by_is_refused_nothing_minted (strict xfail -> passes) · test_prime_adopt_of_a_config_node_still_mints · write 141p · write_guard 23p · write_self_row 7p · write_actor_rows 24p

## CEILING
6 prod lines (ceiling 6).

## Falsifier
1. the two tests above pass. 2. no `return` in the adopt branch precedes the gate (write.py `if edit.adopt:`).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Wording made true (residue 57): the gate adopt calls is submit's, but with no set_fm its self_row / actor_rows grants never apply -- admission is written_by alone. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
