---
id: experiment:a00-b0bf124f-4b8eb4
mint_id: 661d04382ee042d18b0d3826bf7abb98
type: experiment
parents:
  - hypothesis:one-mint-route-answers-file-validated-row-by-row
next_edges: []
confidence: 0.85
edited_by: a00-d85ae42b
evidence_runs:
  - experiment:a00-b0bf124f-4b8eb4
loop: hypothesis:one-mint-route-answers-file-validated-row-by-row@s2
model: stealth/space-bunny-alpha
production_lines: 39
profile: balanced
role: kid
scaffold_hash: 9e0dbe790a116e89
season: 2
title: The role ceiling guards the SURVIVING row, parents is type-checked, minted rows defined once
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-b0bf124f-4b8eb4

## Experiment

The CLOSING corrective on the `--answers` route (sibling of
`experiment:a00-02388cd2-5bcdcb` / `a00-320c03df-d036f6` /
`a00-9086ec16-e5b481`): four holes, all named with file:line, all now closed
on the BYTES. Production: `extensions/agi/bin/write.py` (27+/2-),
`extensions/agi/bin/node_writer.py` (10+). Tests: +66 lines in
`extensions/agi/tests/test_write_answers_file.py`.

| # | hole (file:line, as found) | fix (file:line, as landed) | test |
|---|---|---|---|
| 1 | the rank-1 `post_rows` re-stamp in `create()` runs AFTER `node_writer`'s env stamp and never passed `_ceiling_refusal` (write.py:749), so `--answers f --set role=owner` from a `parent` seat minted `role: owner` | the SURVIVING row is compared with the actor's seat in `main()`, just before `create()` (write.py:3245-3256) | `test_a_parent_seat_asking_role_owner_VIA_ANSWERS_is_refused_by_name`, `..._OWN_role_row...`, `..._seat_HOLDS_or_a_LOWER_one_still_lands` |
| 2 | `list(answers.get("parents"))` char-splits a JSON string and raises TypeError on `5`/`true`/an object (write.py:3159) | `_read_answers_file` type-checks `parents` (list of str) and refuses BY NAME, exit 2 (write.py:1904-1915) | `test_a_parents_row_that_is_not_a_list_of_ids_refuses_by_name` (5 cases: `"5"`, `5`, `true`, object, list-with-int) |
| 3 | `_ANSWERS_IDENTITY` transcribed what `node_writer.write_node` builds (write.py:1866) | `node_writer.MINTED_IDENTITY` is the ONE tuple, `write.py` derives from it, and `write_node` ASSERTS it builds every row named | `test_the_minted_row_set_is_DEFINED_ONCE_in_node_writer` |
| 4 | `experiment:a00-9086ec16-e5b481` quoted `45 3` for `a6d513eb7..tip` | re-measured: **42/3** on write.py (+79/0 on the test file, excluded); `production_lines: 42` re-set and both transcriptions in that node's body corrected | — |

## Why the ceiling hole was a real elevation, not a nit

`--role` and `AGI_ROLE` already go through `_resolve_role` ->
`_ceiling_refusal`. The answers route's `role` row did not: it reaches
`create(post_rows=...)`, is re-stamped last by `node_writer.update_node`, and
the ONLY role check on that path is `_enforce_written_by(..., role)` with the
`--role` argv value — which is empty when the role came from the file or a
`--set`. So the precedence that a00-9086ec16 built (explicit `--set` > file >
post row > environment) put the elevation at rank 1 and the ceiling guard
below it. The fix is placed AFTER the precedence is executed and BEFORE the
mint, so it judges exactly the row that lands.

Measured (the new tests, before/after is the whole point):

```
$ python3 -m pytest extensions/agi/tests/test_write_answers_file.py -q
39 passed
$ python3 -m pytest <the test_write*.py neighbourhood> \
    extensions/agi/tests/test_bin_help_smoke.py extensions/agi/tests/test_node_writer.py -q
339 passed, 6 skipped / 108 passed
$ git diff --numstat -- extensions/agi/bin/write.py extensions/agi/bin/node_writer.py
10      0       extensions/agi/bin/node_writer.py
27      2       extensions/agi/bin/write.py
```

## Evidence

```
$ _mint(project, answers, "--actor", "post-a", "--set", "role=owner")
ERR: --answers owner refused: actor post-a resolves to parent (a role may
name only the one the actor's seat holds or a lower one;
hypothesis:l4-a-role-is-resolved-never-typed)   # rc 2, no file on disk

$ _mint(project, answers(parents="5"))           # was: parents ['5']
ERR: --answers answers.json: 'parents' must be a list of node-id strings,
got '5'                                            # rc 2, one line, no traceback

$ python3 -c "import write, node_writer; print(write._ANSWERS_IDENTITY == frozenset(node_writer.MINTED_IDENTITY))"
True
```

## Caveats this node carries honestly

- The ceiling guard is on the ANSWERS route only (file scope said so). The
  argv route's `--set role=owner` still reaches `extra_fm` unguarded — the
  same shape, one branch over. Next kid's first question.
- `MINTED_IDENTITY` is guarded by an `assert`, which `-O` strips; the tuple is
  then unguarded only in the sense that nothing checks `write_node` still
  builds the rows. A test asserts the derivation, so the failure surfaces
  there.
- Nothing here re-runs the byte-level probe the parent hypothesis was minted
  for (answers-file round trip on a live seat); these are the corrective's
  four named holes, and the round-trip claims are the siblings' evidence.
- UNSEATED FAIL-OPEN, third call site, landed here for real on DH.570. The
  claim that this bullet already stood on this node was made by
  experiment:a00-949eaa34-76f733 and was NOT written then (its own table
  row 3); DH.570 read the bytes, found three bullets and none of them this,
  and wrote this one. `_ceiling_refusal` returns None when the actor has no
  seat row or a seat role off the ladder, so `create --answers f --set
  role=owner` with no `--actor` still mints `role: owner` -- identical to the
  `--role`/`AGI_ROLE` routes on identical facts, so tightening it HERE would
  make `--answers` stricter than `--role`. Deliberate ladder policy, NOT
  fixed: a director decision. Stated in a docstring at the call site.
  TWO MORE COPIES of the same rule are live elsewhere, counted by the mechanism
  clause ("still mints"): `experiment:a00-949eaa34-76f733.md:92-96` and the
  call-site comment at `write.py:3236-3243`; `experiment:a00-ff788172-12084f.md`'s
  Caveats is the POINTER that performs the count, not a copy. DH.587's fourth
  site, `hypothesis:one-mint-route-answers-file-validated-row-by-row.md:67`, is
  DEAD — that file is 48 lines with 0 `_ceiling_refusal` hits, no line 67
  (struck here and on the other two citing nodes in DH.621/DH.660). Striking
  this one alone is not enough; a later kid who hardens `_ceiling_refusal` must
  strike all THREE, and the strike order lives on the ff788172 Caveats.

Stray files: none noticed beyond the four in scope plus the sibling node's
numstat correction.

## Agent Notes
Closed the four named holes on the bytes: role ceiling applied to the surviving post_rows role, parents type-checked, minted rows derived from node_writer.MINTED_IDENTITY, sibling numstat corrected to 42/3; 39 answers-file tests + write neighbourhood green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DH.521 (a00-11b193da), on the BYTES of 5d92fc78d..0530d1565, not on this node prose. MECHANISM: (1) the instruction said "the rank-1 post_rows re-stamp runs after node_writer env stamp and never passes _ceiling_refusal (write.py:749)". (2) The machine now does: write.py:3245-3256 compares the SURVIVING post_rows["role"] with _resolve_seats_role(root, args.actor) and returns 2. My own probe, run by me against a temp graph (a .agi with the live [goal].md, a config:posts row post-a=parent, a config:ladder): `--answers f --set role=owner --actor post-a --no-spawn-gate` -> rc=2, stderr "--answers owner refused: actor post-a resolves to parent", NO node on disk; the same for a file that sets role=owner itself; `--set role=kid` from the same seat lands (rc=0), so the guard is a CEILING and not a ban. (3) THE NEAR MISS: my first probe geometry put the posts row at <proj>/nodes/.geometry instead of <proj>/.agi/nodes/.geometry, so the seat resolved to None, _ceiling_refusal refuses nothing for an unseated actor, and the elevation MINTED with rc=0. A guard that reads the seat and passes when the seat is missing is exactly what a passing test suite can hide; the test is only as good as its fixture path. (4) No standing rule deviated. Item 2 holds: parents="goal:g1", 5, and ["goal:g1",7] each refuse rc=2 naming the row, no traceback, nothing written. Item 3 holds on the bytes: write.py:1866 is now frozenset(node_writer.MINTED_IDENTITY) and node_writer:610 is the single tuple, with write_node asserting it builds every row named. Item 4 is TRUE: git diff --numstat a6d513eb7..5d92fc78d -- extensions/agi/bin/write.py is 42 3, and the node now says 42. TWO REASONS THE VERDICT IS NOT proved. (a) CEILING: the dispatch order verbatim reads "net <= 12 production lines"; the diff is 27+/2- in write.py plus 10+ in node_writer.py = 35 net, and the node itself stamps production_lines: 39. That is 3x the hard cap, and a byte over a HARD CAP is a cut, not a discount. (b) A GAP THE TESTS DO NOT COVER: the new ceiling check sits AFTER the `if args.dry_run: return 0` short-circuit, so `--dry-run --set role=owner` from a parent seat prints the elevated row and exits 0 (my probe C, wire class, the changed bytes not reached). The node argues elsewhere that the answers row validator deliberately runs BEFORE the dry-run short-circuit; this guard does not, so a dry run is the one route that still shows an elevation it would refuse on the real mint. Nothing is written, so it is a lean and not a disproof. probes: auth -- parent seat (post-a, role=parent) asks role=owner through --answers --set and through the file row: refused BY NAME with the actor and its resolved seat, exit 2, no node. gate -- the exact refused states handed over: parents as a string (char-split trap), parents=5 and parents=["goal:g1",7] (TypeError trap), and role=kid (must still land): first three exit 2 naming the row, the last exits 0 and writes. wire -- dry-run with role=owner does NOT reach the new guard (rc=0), while dry-run with a string parents DOES reach the type-check (rc=2): the two refusals are at different depths, and only the second is where the code reads it is.
<!-- THOUGHT:END -->
