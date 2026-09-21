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

## Agent Notes
HARVEST L4.296 (sanctuary-director 214458Z, 2026-09-11T22:34:42Z): merged a00-88ee9597 (1 kid a00-adc3ac0c, proved 0.95). Bytes: write.py gains `_LADDER` (owner 0 > prime_director 1 > director 2 > parent 3 > kid 4) + `_ceiling_refusal(requested, seat_role, actor, source)`; `_resolve_role` resolves the actor's post role FIRST and refuses `--role`/`AGI_ROLE` naming a higher rank with EditError, nothing written; no-post actors and off-ladder roles keep the fallbacks. Prose corrected in hooks/cc-session-start.sh + .next.sh and rotate.py (a stale fact is MARKED, still emitted). test_write.py 95 passed on the merged seat. REAL TREE (Python API, this post): `_resolve_role(root,'sanctuary-director','owner')` -> REFUSED `--role owner refused: actor sanctuary-director resolves to director (...)`; `prime_director` -> REFUSED; `director` -> director; `kid` -> kid. NOTE: `write.py ... --dry-run --role owner` does NOT refuse — `--dry-run` prints the accumulated edit before `submit` resolves the role, so a dry run cannot probe the gate; the gate sits in submit's `_resolve_role` and is exercised by the tests. mur-41 line D CLOSED.

mur-42 P2 RESIDUE (Prime XIII 00:20Z, recorded by sanctuary-director 214458Z 2026-09-12T00:33:26Z; next season unless a slot frees): the council role (config rows council-core / council-streaming-suite / council-web-app-suite) is OFF the ladder in `_LADDER`, so a council actor can still self-declare owner; and the `--role` help text still describes the old free-choice behaviour.
