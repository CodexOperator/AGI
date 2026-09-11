---
id: hypothesis:l4-a-role-is-resolved-never-typed
mint_id: 46514ad18ada44d5bbcc2922f7957931
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-role-resolution-longest-prefix
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 15592c4bf13c28a0
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. FOUND by the mur-41 review (Prime XII, wf_71d90645-bb8, 21:5xZ), minted by sanctuary-director 214458Z as the Prime's g15 line D; IN the close cut-off (Prime 22:14Z). MEASURED by mur-41: L4.290's kid passed the config:rotations `written_by` gate by typing `--role owner` (sanctioned after the fact by a Prime note; the ruling: A ROLE IS RESOLVED, NEVER TYPED). The bytes: `_resolve_role` (write.py:600-616) returns `role_param` BEFORE any seat resolution (write.py:609-610), so any CLI caller self-declares owner. CLAIM: (1) `--role` may only name the role the actor's seat resolves to (the config:seats row by longest seat-prefix, hypothesis:l4-role-resolution-longest-prefix) or a LOWER one on the ladder (owner > prime_director > director > parent > kid); a higher one is REFUSED by name (`--role owner refused: actor sanctuary-director resolves to director`), exit non-zero, nothing written; an actor that resolves to no seat (a bare `owner` actor, a kid id) keeps today's fallbacks unchanged; AGI_ROLE is subject to the same ceiling; (2) the stale prose that says a stale measured fact is REFUSED -- hooks/cc-session-start.sh:227-232, hooks/cc-session-start.next.sh:229-234, rotate.py's help at ~:10349 and the docstring at ~:5862 (grep `stale`) -- is corrected to what L4.290 built: a fact NOT at HEAD is MARKED stale per its `fact_bounds` entry and still emitted; (3) tests: a director actor with `--role owner` refused; `--role kid` from a director accepted; owner actor with `--role owner` accepted; the prose grep finds zero `refused` wordings for stale facts. CEILING: 1 kid. FILE SCOPE: `extensions/agi/bin/write.py` (`_resolve_role` + one ladder-order helper), the two hook comment blocks, the two rotate.py prose spots (comments/docstrings only, no rotate.py code), `extensions/agi/tests/test_write*.py`. Run `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_write.py -q` (and any test file that exercises `_resolve_role`) and paste the refusal line from a real-tree dry run (`write.py <any node> --dry-run --actor sanctuary-director --role owner 'note x'`) into the experiment node. The parent merges the kid branch into the round branch before `done:`."
title: "G15: write.py --role may name only a role the actor's seat holds or a lower one -- a self-declared elevation is refused by name; the stale \"a stale fact is refused\" prose is corrected"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-role-is-resolved-never-typed

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
