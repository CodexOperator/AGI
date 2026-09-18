---
id: hypothesis:l4-the-formation-owner-writes-config-posts-rows-and-the-town-master-cell-through-a-schema-declared-actor-row-grant-never-a-role-literal
mint_id: ed0a902a5ca7496aa61b30a7f3f14705
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 807f0c4ab44b7810
season: 2
testable_claim: "write.py resolves EVERY actor-row grant declared on a schema (a list `actor_rows:` whose entries carry {actor, list_key|field, match_key, fields, ops, deny_roles}; master_sensei_row migrates in as the first entry unchanged in behaviour) keyed on the RESOLVED seat name, never a role literal or a caller string: with the [config] entry {actor: sanctuary-master, list_key: posts, match_key: name, fields: [town, quiet, status, role, tier, model, effort, rotated_by, harness, settings], ops: [create, set, retire]} the sanctuary-master seat creates, edits and retires posts rows and their town/quiet cells, and with the [town] entry {actor: sanctuary-master, field: master} it sets a town master cell; any other seat (a kid, a parent, the sensei-director) is refused BY NAME; the prime/owner written_by path is unchanged; the town branches cell stays refused by name at mint and read. Falsifier: a seat other than the declared actor lands a posts row or a master cell; or the declared actor lands a field outside the grant; or master-sensei template writes change behaviour (test_write_master_sensei.py reds)."
title: "SM.102 (formation carve-out, owner 09-18 00:1xZ): the formation owner writes config:posts rows and the town master cell through a schema-declared actor-row grant, generalized from master_sensei_row so the NEXT grant is a schema line"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-formation-owner-writes-config-posts-rows-and-the-town-master-cell-through-a-schema-declared-actor-row-grant-never-a-role-literal

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.102 BRIEF (sanctuary-master gen 7, 09-18 00:2xZ; owner 00:1xZ via the Prime, verbatim in doc:l5-owner-decisions: the sanctuary master has control over posts -- setting up, taking down, rearranging formations via the graph; each master owns its town branch until council activation). TODAY: [config].md written_by [owner, prime_director] + self_row + master_sensei_row (write.py ~924-960 resolves ONE hard-named key); [town].md written_by [prime_director, owner], no master field, branches REFUSED by name (derived: the branch prefix IS the town axis). CLAIM: see testable_claim. SHAPE (template-first): write.py reads a schema list `actor_rows:` generically (the master_sensei_row resolver becomes the loop body; the old key stays readable as a one-entry alias so nothing breaks), so a future grant = ONE schema line. TEMPLATE HALF (master-sensei cuts, after L5 CLOSED): [config].md actor_rows entry for sanctuary-master over `posts` (fields measured from the live posts.md row keys, never guessed; ops create/set/retire; deny_roles [kid, parent]); [town].md `master: {type: str}` field + actor_rows entry {actor: sanctuary-master, field: master}; branches refusal untouched. CODE HALF (one kid, ceiling 20 production lines): the generic resolver + the top-level-field grant + create/retire ops on a list row. TESTS (one file, test_write_actor_rows.py): (1) sanctuary-master seat sets a posts row town cell + creates a row + retires one -> written; (2) sensei-director / a kid on the same edit -> refused by name; (3) sanctuary-master sets a field outside the grant -> refused; (4) town master cell written by sanctuary-master, branches cell still refused at mint + read; (5) test_write_master_sensei.py green unchanged. NEGATIVE PROBES at review: each of 2-4 with its positive twin. FILE SCOPE: extensions/agi/bin/write.py, the two schemas, one new test file. DISPATCH: after the Prime's L5 CLOSED dm, from this worktree, one kid. UNTIL THEN the formation acts go to the Prime as [decision] lines with the exact edit (he applies verbatim). FIRST FORMATION ACT after the close (queued): the owner map as `master` cells -- core + sanctuary: sanctuary-master; local-maxxing: thought-master; streaming-suite: stream-master (idle, the Prime holds); web-app-suite: none (the Prime holds); season2/main + season1/main + master = the Prime (a ladder/doc fact, not a town cell).
