---
id: hypothesis:a-post-may-append-a-note-to-its-own-town-board-through-a-verb-scoped-actor-row
mint_id: 17a45103b81e4fe2a09e0fc708c70219
type: hypothesis
parents:
  - goal:g7.33
next_edges: []
edited_by: director-engine
scaffold_hash: a0fe10143a872041
season: 2
testable_claim: "An actor_rows entry {actor: <post>, verb: note} admits exactly one append-only line under the node's ## Agent Notes by that resolved seat and nothing else; no verb entry = the same refusal as today."
title: A post may append a note to its own town board through a verb-scoped actor_rows entry (inert until the grant lines land)
town: core
---
# hypothesis:a-post-may-append-a-note-to-its-own-town-board-through-a-verb-scoped-actor-row

# hypothesis:a-post-may-append-a-note-to-its-own-town-board-through-a-verb-scoped-actor-row

## Measured
- OWNER 06:4xZ 09-28 (via belam [rule] 06:27Z, agi-dispatch §5 row "progress -> board"): every harvest / merge-up / judge that moves a goal = ONE numbers-only line via `write.py town:<town> 'note ...'`.
- 06:3xZ, director-engine: `write.py town:local-maxxing "note ..." --actor director-engine --role director` -> `ERR: town nodes (town:local-maxxing) may be hand-edited only by admitted roles owner, prime_director; resolution for actor 'director-engine' gave director, which is not admitted. (goal:g12)`. thought-master is refused the same way (TMM.323).
- write.py:1658-1668: the generic `actor_rows:` carve-out admits only what `_actor_rows_refusal` (write.py:1122) resolves, and every entry is a FIELD grant: `[town].md:5-7` = `{actor: sanctuary-master, field: master}`, `{actor: thought-master, field: trajectory_standin}`. A body append (`note`) is no field, so no schema line can grant it today.

## CLAIM
An `actor_rows:` entry may name a VERB instead of a field -- `{actor: <post>, verb: note}` -- and it admits exactly one write shape: an APPEND-ONLY line under the node's `## Agent Notes` section by that resolved seat, nothing else (no frontmatter, no other section, no edit or removal of an existing line). The grant lands INERT: this round adds the verb-scoped resolver and its tests; the grant LINES in `[town].md` are belam's to add.

## Dispatch line
config-max: the grant itself = one `actor_rows:` line per post in `.agi/context/schemas/[town].md` (belam's; NOT this round) · template-max: none · code: the resolver in `_actor_rows_refusal` does not know a `verb:` key -- the only code.

## FALSIFIERS
- a `{actor: X, verb: note}` entry admits X to change frontmatter, replace or delete an existing body line, or write outside `## Agent Notes`;
- it admits a seat OTHER than X, or an unresolved actor;
- an existing `field:` grant changes behaviour;
- with no `verb:` entry in the schema, a director's `note` on a town node is still refused with the same message.

## TESTS
A new committed test file for the verb grant (tmp_path project roots only, a dummy schema with one `verb: note` entry) + the existing write.py actor_rows / town-write tests and test_bin_help_smoke.py; TMPDIR + --basetemp under /dev/shm, env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT; never the live town node.

## FILE SCOPE
extensions/agi/bin/write.py (`_actor_rows_refusal` and the carve-out call site at ~:1658-1668 ONLY) · one new test file under extensions/agi/tests/ · the kid's own node. NOT `.agi/context/schemas/[town].md` (the grant lines are belam's).

## CEILING
1 kid · <= 15 production lines net · <= 60 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut. QUEUED behind the EG.9 chain (TMM.323), never ahead of it.
