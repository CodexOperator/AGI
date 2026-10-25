---
id: doc:v8a-submit-guard-census
mint_id: 83f7ea325f4147318abd95a48bf4ea9c
type: doc
parents:
  - goal:g7.16.1.11.46.23
next_edges: []
edited_by: director-general-1
season: 3
tags: []
title: V8a submit guard census
town: local-maxxing
---
# doc:v8a-submit-guard-census — every guard ahead of write.submit, measured for an engine.v 4 actor (goal:g7.16.1.11.46.23, tip 2b)

v2 (director-general-1 10-25, re-cut after the council's 3/3 acceptance of v1 at 20:37Z): v1 carried two wrong rows, found while starting the code. (a) C7 (actor_rows grants) IS reachable from a live writer: rotate.py:22624, the migrate tick, writes another post's row through the grant. (b) The write sites are not 3 shapes but 6: section 1 lists every one, and section 8 lists the callers a `write\.py +[a-z:]` grep misses. Rows C5, C7 and the in-process classes below are corrected accordingly; the R-land rows R1-R5 are the council's 20:37Z rows.

Council [decision] alive 19:21:59Z 10-25, 3/3: (B), not (A); the census is one table, written once. Method: a fixture graph = the trunk's real `.agi/context/schemas` + `.agi/nodes/.geometry` + `.agi/config.json` (trunk 3138d08b8e bytes) in a scratch dir; `write.submit(FX, Edit('config:posts') with set_fm['posts'] = the row list, actor=, role=)` exactly the shape of the 3 live sites; each row is one attempt, ADMIT/REFUSE read off the call and `wrote=` off the file bytes. The harness is `matrix.py` in the post's scratchpad (S1-S18 below are its lines); the committed mutant tests land with tip 2b.

## 1 · What the live writers do (the only callers of submit outside tests): 3 writers, 6 call shapes
| call site | shape | writes | actor |
|---|---|---|---|
| send.py:634 (keygen, one seat) | set, own row | pubkey, sig_scheme, enc_scheme, key_history of the actor's own row | the post itself |
| send.py:594 (keygen --all-live) | set, MANY rows, prime-only | the same four cells on every live un-keyed row | a prime_director |
| send.py:6476 (spawn-mint) | CREATE one new row | a whole new row (tier untrusted, pubkey, charter, worktree ...) | the sponsor, a role the schema admits (written_by / an actor_rows `create` grant) |
| seatsig/countersign.py:253 | set, ONE NAMED OTHER row | tier + promoted_by | the countersigner, by a role in written_by |
| rotate.py:10091 via :18296, :22624 (session cells) | set, own row | window, pid, session_id, session_name, session_ref, generation | the seat itself |
| rotate.py:10091 via :22624 (seating cells) | set, ANOTHER post's row, by GRANT | box, worktree | the master the [config].md actor_rows grant names (resolved by _migrate_seating_actor from schema data); the EditError at :22642 is that grant refusing |
All six: `set_fm[list_key] = the whole row list`, no body, no payload, no sub, no replace. Every edit-shape refusal below row C1 is unreachable from them.
HOW THE REPLACEMENT IS SHAPED (tip 2b, extensions/agi/bin/config_rows.py): the SITE declares what it intends to write ({row: (op, key set)}), and the helper refuses unless the old-to-new row diff equals the declaration exactly (a keygen that touches another row, a countersign that adds a key: refused); then the actor is admitted by schema data, never a literal: (W) the role the actor's OWN posts row holds is in `written_by`, or (S) own row and keys within `self_row.fields`, or (A) an `actor_rows` grant covering actor + list + op + keys, deny list honoured. A caller-passed role is never read: it cannot be forged up.

## 2 · The table (FIRES = measured on the fixture for an engine.v 4 actor, role director, the real posts.md rows)
Classes: (i) KEPT as a narrow check on the node_writer path · (ii) COVERED by a named surviving mechanism + a lane where the same input is still refused · (iii) DROPPED with a reason; a DROPPED row on a config/RULES path gets a MECHANICAL replacement (R-land below), never silence.

| # | guard (write.py) | measured | FIRES for a v4 actor | class | what stays / replaces | mutant |
|---|---|---|---|---|---|---|
| C1 | edit-shape refusals: empty edit, stdin, sub, replace, patch, payload, body-opens-frontmatter, thought marker, set-active parked grep (:2583-2820) | not reachable from set_fm-only edits | no (no site) | (iii) | no live caller builds one; the CLI that did retires with write.py; the test files that drive submit pin them (section 5) and retire with it | n/a (unreachable) |
| C2 | outside-ref gate (link_ref/payload_ref, :2597) | the 3 sites set no ref | no | (iii) | `links.py schema` still reports it dry | n/a |
| C3 | _resolve_api_root (:2586) wrong root | node_writer.update_node on a root with no node file returns REJECTED (node_writer.py:1423 shape, find_node_file None) | refuses, writes nothing | (ii) | node_writer.find_node_file / REJECTED 'no node file' | a bad root -> REJECTED, file bytes unchanged |
| C4 | role resolution: ceiling on a forged AGI_ROLE / --role, UNRESOLVED identity (:1006) | S11 actor 'nobody' REFUSE (UNRESOLVED); S12 own row + role=prime_director REFUSE (ceiling) | yes | (i) | config_rows.py reads NO caller role: the role is the actor's own posts row's `role` (exact seat, or the old longest-prefix-with-boundary rule, a tie refuses), `owner` for the literal actor owner, else UNRESOLVED and refused. A forged role cannot widen anything because none is read | an unresolved actor -> REFUSE; a passed role is ignored |
| C5 | written_by role gate (config [owner, prime_director]) (:1866); reached by send.py:594, :6476 and countersign.py:253 (all non-self_row shapes) | S2 other post's row REFUSE; S4 other post model REFUSE; S3 own non-self_row field (model) REFUSE; S7 prime ADMIT; S10 literal owner ADMIT | yes | (i) for the 3 writers; (iii)+R-land for every other writer | (W) in config_rows.py: the role the actor's own row holds, read from posts rows, must be in the schema's written_by (data); the site's declared diff must match exactly | S2/S3/S4 shapes through config_rows.write_rows -> REFUSE; a caller-passed forged role -> REFUSE |
| C6 | self_row carve-out (S1 own pubkey ADMIT; S16/S18 ADMIT even with the veto frozen/missing) | S1 ADMIT | yes | (i) | (S) in config_rows.py: own row, keys within `self_row.fields`, none of the protected cells | S1 shape -> ADMIT, S3 shape -> REFUSE |
| C7 | actor_rows grants (sanctuary-master posts fields; master-sensei templates) | S5 SM quiet ADMIT; S6 SM pubkey REFUSE (not granted) | YES for the posts grant: rotate.py:22624 writes box/worktree of another post's row through it (v1 said unreachable: WRONG) | (i) for the posts grant at that site; (iii)+R-land for the master-sensei templates entry and any other writer | (A) in config_rows.py reads actor_rows from [config].md data; SM's own edits go by git (agi-at / land), where R-land reads the same grant | master actor writing `pubkey`, or a non-master writing box/worktree on another row -> REFUSE; an SM-authored land changing `pubkey` -> refused by R-land |
| C8 | rung-3 veto freeze (outside self_row; unreadable cell HOLDS) | S15 frozen: prime other row REFUSE; S17 veto cell missing: REFUSE; S16/S18 own self_row ADMIT | yes, 0 active gates on the live cell today | (iii)+R-land | R-land refuses a config-row land while config:vetoes has an unanswered active_gate for scope prime or the cell is unreadable; the sites are self_row writes, never gated | frozen cell + a land touching another post's row -> refused |
| C9 | town_cell vocabulary on a row's `town` | S8 prime town='nowhere' REFUSE | yes | (iii)+R-land | towns.py already exports accepted_towns(root) / row_town(root); R-land runs it on the changed rows | a land with town 'nowhere' -> refused |
| C10 | ring gate (_ring_pubkey_for_post :1674, ring_fresh, ring_decision cell) | `grep -c '^ring:' .agi/context/schemas/*.md` = 0 declarations (aio verified 3138d08b8e; re-read here) | no: opt-in per schema, 0 schemas declare one | (iii): SUPERSEDED | rings.py (verify_decision) stays as a library for veto and countersign; test_write_ring_cli (30 tests) retires | n/a (nothing declared) |
| C11 | set schema gate (_enforce_set_schema_gate :2424): type, regex, refuse: annotations | S13 posts='notalist' REFUSE ('must be a list value'); S14 an unknown list key ADMIT | yes for types; unknown keys ADMIT today | (i) | the narrow check validates the ONE thing the sites write: `posts` is a list of dicts, each with a string `name`; every other schema judgment stays `links.py schema` (dry) | posts = a string -> REFUSE |
| C12 | master_sensei facts-body carve-out (config:rotations templates, :1601) | body-only; no site writes a body | no | (iii) | no caller; its tests retire | n/a |

## 3 · R-land: the one mechanical replacement for every DROPPED config/RULES row (C5, C7, C8, C9)
Council rows (alive [decision] 20:37:08Z 10-25, 3/3; aio withdrew B'1): R-land = ONE sh+jq repo script called with BASE TIP, built as tip 2c (extensions/agi/guard/, data from the schema, never literals), carrying:
- R1 (aio): the author is the SIGNER, resolved by `git verify-commit --raw` against allowed-signers at BASE, never %an/%ae. MUTANT: signed by DG1's key, author 'belam', edits belam's row -> REFUSED.
- R2 (sp): ADDED and DELETED rows need a written_by role or an actor_rows grant; a rename counts as delete + add; a post never mints its own row. MUTANT: a post adds a row named after itself -> refused.
- R3 (sp): anything unreadable (posts, seats or vetoes at BASE or TIP, or a jq parse failure) -> `R-land: unread (<cell> at <rev>)`, refused; never a pass on an empty diff.
- R4 (sp, a MUST): THREE call sites, the same script with the same BASE TIP: SM's gate, belam's verify-land, AND the reference-transaction prepared phase on posts/belam + core/season3/main (belam's direct commits are not lands; only the hook sees them). MUTANT: a belam direct commit editing another post's row with no grant -> the ref update is refused. The agi-master-gate and skill edits are RULES and land with belam.
- R5 (true-state line, 3/3): R-land is enforced at every trunk move except a deliberate core.hooksPath bypass. A hook guards against MISTAKES; it is not a wall.
The rule R-land applies per changed row of config:posts/seats: the signer is (a) the row's own post with every changed key in `self_row.fields`, (b) a role in `written_by`, or (c) an `actor_rows` grant covering the key and op; refused while config:vetoes holds an unanswered active_gate for scope prime or cannot be read; a changed row's town must be in towns.accepted_towns(root). The hub question is closed on the bytes: the only hub this clone names is `origin = https://github.com/CodexOperator/AGI.git`, where no pre-receive hook runs, so B'1 is out and belam's probe only confirms it.
Rows C5/C7/C8/C9 stay (iii)+R-land until tip 2c lands; until then they are enforced by the land review only, and that is said here, not hidden.

## 4 · B'2 false data (a line that claims a rule and nothing enforces it)
After the retire, with R-land landed: [config].md `written_by`, `self_row`, `actor_rows`, `master_sensei_row`, `town_cell` are enforced by R-land. [moral].md `written_by: owner` is enforced by engine-grow.md:112 (`'owner' if t=='moral'`). [town].md and [vision].md `written_by` are enforced by R-land only if it reads written_by for every type (it does, by schema, not by a config literal); `master_sensei_row` has no live writer and is OWNER-edit material (.agi/context/schemas is RULES): banked in card-belam §6 with the recommendation to delete the declaration with this leaf's RULES land. Until R-land lands, none is claimed as enforced.

## 5 · The tests (measured: `git grep -lE "(write|write_mod|_w)\.(submit|Edit\b|verb_[a-z_]+)\(" -- extensions/agi/tests` = 17 files; the brief's "21" counted files that merely import write; 57 files import write in all)
| fate | files (direct submit/Edit/verb_ calls) | pins |
|---|---|---|
| RETIRE whole with write.py (9) | test_write.py (202 tests), test_write_guard.py (38; it tests build:bin-write-guard, whose one purpose, warning on node changes made outside write.py (QUICKSTART:179), disappears: bin-write-guard is RETIRED with write.py, not kept), test_write_actor_rows.py (24), test_write_master_sensei.py (17), test_write_ring_cli.py (30), test_write_schema_checked.py (13), test_write_sub.py (12), test_write_dotted_key.py (3), test_body_patch.py (6) | C1, C2, C3, C7 (actor_rows: the rule moves to R-land's mutants), C10, C11, C12 |
| MOVE their refusals to mutants (3) | test_write_self_row.py (8) -> the narrow-check mutants (C5/C6, tip 2b); test_write_veto_gate.py (3) -> R-land mutants (C8); test_town_cell_write.py (6) -> R-land mutants (C9, towns.accepted_towns) | C5, C6, C8, C9 |
| STAY, setup call repointed to node_writer.update_node / retire_node (5) | test_veto_fail_closed.py (3 direct calls; veto.py stays), test_post_rename.py (3), test_formation_readback.py (1), test_rotate_handover.py (2), test_retire_place.py (6; retire = status + move, already node_writer.retire_node) | their own subject |
Not direct callers, import write for other names, repoint in tips 2a/2b: test_rotate.py, test_send.py, test_geometry_config.py, test_rings.py, test_migrate_channel.py and about 35 more (57 importers in all). Counts are by file; test-function counts are `grep -c "def test_"`.

## 6 · Measured lines (the fixture run)
S1 own self_row pubkey ADMIT · S2 other post's pubkey REFUSE (own row only) · S3 own model REFUSE (prime/owner-only field) · S4 other post model REFUSE · S5 SM quiet ADMIT · S6 SM pubkey REFUSE (not granted) · S7 belam model ADMIT · S8 belam town 'nowhere' REFUSE (vocabulary) · S10 literal owner ADMIT · S11 actor 'nobody' REFUSE (UNRESOLVED) · S12 own row with a forged role REFUSE (ceiling) · S13 posts='notalist' REFUSE (type) · S14 unknown list key ADMIT · S15 frozen veto, belam other row REFUSE · S16 frozen veto, own self_row ADMIT · S17 veto cell missing, belam other row REFUSE (HOLDS) · S18 veto cell missing, own self_row ADMIT.

## 7 · Status of the asks
1. belam's pre-receive probe: unchanged, confirms B'1 is out; not blocking.
2. R-land as a repo script called at three sites: DECIDED by the council 20:37Z (R4).
3. Order: code tip 2b (config_rows.py, the six shapes, mutants), then 2c (R-land R1-R5). GO given 20:37Z.

## 8 · Callers a `write\.py +[a-z:]` grep misses (the leaf's falsifier 1 undercounts; step 3 gets its own table by file:line)
Runtime shell-outs to write.py by path variable, not by that spelling: council_report.py:119, failures.py:361, metrics_cell.py:119, rotate.py:9831 (`with_name("write.py")`), season.py:63 `WRITE_PY` and :274 (its cell pass, 16 mentions), sensei.py:2465. Prose that tells a kid or agent to run it: brief.py (14 lines, :1060, :1547-1560, :1601, :1955, :1978, :2088-2089), workflow.py:1704, 9 workflow JS/JSON prompts, the .geometry exec lines (12), crons.services.fragment.md:35, write_guard.py (its own advice strings). Falsifier 1 gains the pattern `WRITE_PY|["']write\.py["']|/write\.py` in the step-3 tip, with a mutant (a caller built from a variable reads RED).
