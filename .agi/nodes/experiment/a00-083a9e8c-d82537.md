---
id: experiment:a00-083a9e8c-d82537
mint_id: 911c4f38b82a49a1bd70990a63bae73f
type: experiment
parents:
  - hypothesis:l4-the-formation-owner-writes-config-posts-rows-and-the-town-master-cell-through-a-schema-declared-actor-row-grant-never-a-role-literal
next_edges: []
confidence: 0.85
edited_by: a00-ec12fb27
evidence_runs:
  - experiment:a00-083a9e8c-d82537
line_ceiling: 40
loop: hypothesis:l4-the-formation-owner-writes-config-posts-rows-and-the-town-master-cell-through-a-schema-declared-actor-row-grant-never-a-role-literal@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "an actor the claim never authorises (not the resolved seat, not a declared actor_rows/self_row identity) is refused by name for the exact own-row-shaped edit", "class": "auth", "cmd": "write.submit(fixture, posts_edit(rows_with_sanctuary-master.session_id=should-not-land), actor='totally-unresolvable-actor')", "expected": "refused by name; session_id never lands", "observed": "EditError: config nodes (config:posts) may be hand-edited only by admitted roles owner, prime_director; resolution for actor 'totally-unresolvable-actor' gave parent, which is not admitted. (goal:g12); posts.md never carries 'should-not-land'", "result": "refused"}
  - {"conjunct": "the fix is wired to the REAL rotation call site (rotate._successor_row_write), not just an isolated write.submit call or the kid's own inner _write_identity_cells test", "class": "wire", "cmd": "rotate._successor_row_write(fixture, actor='sanctuary-master', seat='sanctuary-master', role='director', session_ref='probe-ref-999', generation=7, window='@999', pid=31337, session_id='wire-probe-uuid', session_name='agi-wireprobe')", "expected": "cells land in posts.md via the real multi-level call chain", "observed": "outcome string returned non-empty; 'wire-probe-uuid', '31337', 'probe-ref-999' all present in posts.md after the call", "result": "wired live"}
  - {"conjunct": "the sanctuary-master seat creates, edits and retires posts rows and their town/quiet cells (testable_claim, no row excluded -- includes its OWN row)", "class": "gate", "cmd": "sanctuary-master edits ONLY its own row's `town` field (rows[0], no other row touched) via write.submit; cross-checked against a locally-patched copy of write.py with the 8-line SM.115 block removed", "expected": "ADMITTED -- this is the hypothesis's own headline grant (posts rows AND their town/quiet cells), and was ADMITTED before this round (confirmed on the patched copy: res.status == updated)", "observed": "REFUSED post-fix: \"a seated role may update only its OWN row and only the declared fields; field 'town' is not in the self-row fields ['session_ref', 'session_name', 'session_id', 'generation', 'window', 'pid', 'pubkey', 'sig_scheme', 'enc_scheme', 'key_history', 'session_label'] declared by the node's schema. (L4.110 prime ruling B)\" -- because `changed=[sanctuary-master]` is all-own-row, the actor_rows entry is skipped ENTIRELY (not just for the fields self_row already covers), so town/quiet/status/role/tier/model/effort/rotated_by/harness/settings become unreachable on the master's OWN row specifically, while still working on every OTHER row", "result": "FALSIFIED for the own-row case: the fix over-applies the director's 'actor_rows is not consulted' instruction to fields actor_rows uniquely granted and self_row does not cover, regressing a previously-admitted capability that the parent hypothesis's own claim names explicitly"}
production_lines: 8
profile: balanced
role: kid
scaffold_hash: d665057f1c529186
season: 2
title: SM.115 prevents actor_rows from refusing the actor own row so self_row governs it
town: core
verdict: inconclusive_lean_disproved:55
---
<!-- BODY:BEGIN -->
# SM.115 — the actor's own row is self_row's, never actor_rows'

## Experiment

**The claim (g15 build order, director-sanctuary brief):** for the actor's
own row (`match_key` == the resolved seat), `self_row` governs and
`actor_rows` is not consulted; `actor_rows` continues to govern OTHER rows
only. SM.108's delivered fix had made `actor_rows` the first gate, and its
fields check runs against the actor's OWN row before `self_row` is ever
reached — so the live `sanctuary-master` rotate-self spawn-row write
(`session_id`/`pid`/`generation`, all `self_row` fields) was refused by
`actor_rows`, whose `posts` field list does not include `session_id`.

### Pre-fix state (measured)

The parent's repro, reproduced with the new tests: on the fixture schema
carrying BOTH a `self_row` entry and the `sanctuary-master` `actor_rows`
grant on `posts`, setting the actor's own row's `session_id` raises:

```
write.EditError: config nodes (config:posts): the actor_rows grant does not
cover this write; field 'session_id' is not granted on `posts` rows (fields
['town', 'quiet', 'status', 'role', 'tier', 'model', 'effort', 'rotated_by',
'harness', 'settings']) (schema-declared actor_rows)
```

`session_id` IS in `self_row.fields`, so this is exactly the write `self_row`
exists to admit. It never ran.

### The fix (write.py `_actor_rows_refusal`, +8 production lines)

Inside the `list_key`+`match_key` branch, after `old_by`/`new_by` are built and
BEFORE the grant's fields/ops loop, compute the set of rows whose bytes this
write changes. When that set is non-empty and EVERY changed row's `match_key`
value equals the resolved seat, `continue` — the entry does not apply, the
loop ends in `return None`, and control falls through to `_enforce_written_by`'s
`self_row` block, which already restricts a seated writer to only its own row
and only the declared fields. A write that touches ANY other row is NOT
"own row only": actor_rows runs exactly as before (SM.108's three residues stay
intact for other rows). `changed` non-empty is required so a no-op write keeps
its previous admission behaviour.

No role literal, no `rotate.py` change, no schema change.

## Evidence

Added three tests to `extensions/agi/tests/test_write_actor_rows.py`:

1. `test_own_row_spawn_write_admitted` — the exact repro: own row's
   `session_id`/`pid`/`generation` -> `res.status == node_writer.UPDATED` and
   the cells are in `nodes/.geometry/posts.md`.
2. `test_other_row_still_limited_to_actor_rows_grant` — regression guard:
   same actor, same list, `session_id` set on `director-belam`'s row -> refused
   BY NAME (`session_id` + `actor_rows`), and the cell did NOT land — proving
   the fix did not widen the grant.
3. `test_rotate_identity_writer_own_row_admitted` — the REAL caller:
   `rotate._write_identity_cells` (the one writer
   `_successor_row_write`/`_backfill_session_ref` drive) writes the identity
   cells -> non-empty outcome and the cells land.

Falsifier run: with the guard disabled (`if False and changed ...`), tests 1
and 3 fail with the exact pre-fix `EditError` above — so the tests measure the
fix, not the fixture.

Suite (the five files the brief names):

```
python3 -m pytest extensions/agi/tests/test_write_actor_rows.py \
  extensions/agi/tests/test_write_master_sensei.py \
  extensions/agi/tests/test_write.py \
  extensions/agi/tests/test_write_self_row.py \
  extensions/agi/tests/test_town_cell_write.py -q
154 passed, 94 warnings in 1.90s
```

Production lines (`git diff --numstat -- extensions/agi/bin/write.py`): `8 0`
against a 40-line ceiling.

### Scope note

Materialised bytes live in `extensions/agi/bin/write.py`, the SHARED repo
tree — not the worktree checkout. The diff above is the one read-only
measurement the brief permits.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT review of experiment:a00-083a9e8c-d82537 (SM.115, kid tier, same shared worktree, uncommitted at review time -- write.py +8/-0, test_write_actor_rows.py +47/0, confirmed via git diff HEAD, isolated from an unrelated sibling kid's mem_cap.py edits also staged in this shared tree). Read the actual bytes (git diff HEAD -- write.py), not the node's own prose or its self-set verdict:proved.

First reproduced the ORIGINAL live regression myself, independently, before this kid ran: sanctuary-master's own-row spawn write (session_id/pid/generation, all self_row fields) was refused by actor_rows because its posts fields list does not include those identity cells -- exactly the director's SM.115 order. The kid's fix is a clean 8-line insertion in _actor_rows_refusal: when every row a write changes on a list has match_key == the actor's own resolved seat, the entry is skipped (continue) so self_row governs; a write touching any OTHER row still gets the full actor_rows treatment.

Ran three probes myself, one per class the gate requires:
auth -- an unresolvable actor attempting the exact own-row-shaped edit is refused by name (goal:g12 written_by refusal); held.
wire -- called rotate._successor_row_write directly (one level above the kid's own _write_identity_cells test, the actual function rotate-self step 3 drives) with fresh literal values on a fixture the kid never touched; the identity cells landed in posts.md through the real multi-level call chain; held.
gate -- constructed the state the kid's own suite never builds: sanctuary-master edits ONLY its own row's `town` field (rows[0], no other row touched) -- this is the parent hypothesis's own headline grant, 'posts rows and their town/quiet cells', with no row excluded. REFUSED post-fix ('town' is not a self_row field). To rule out a pre-existing gap I copied write.py to a scratch file, removed only the 8 SM.115 lines, and reran the SAME edit: ADMITTED (res.status == updated). This is a genuine regression this round introduces, not a pre-existing one -- FALSIFIED.

Near miss: reading the diff for shape alone (an 8-line insertion exactly where the brief asked, exactly matching the director's wording 'actor_rows is not consulted' for the own row) looks correct and IS a faithful, literal implementation of the fix as specified. The gap only surfaces when the state constructed is 'the master edits its own row's town/quiet/status cell alone' -- a shape neither the kid's 3 new tests nor the pre-existing 154-test regression suite ever builds, because no prior test exercised sanctuary-master editing its OWN row via actor_rows (the existing town-cell test uses rows[2], director-belam, never rows[0]). The director's fix instruction was unconditional ('actor_rows is not consulted' for the own row, no exception) and the kid implemented that instruction exactly and faithfully -- the gap is in the fix's own design against the BROADER parent claim, not in the kid's execution of the literal order.

Verdict: the urgent, live-blocking defect (rotation's own-row identity write) is genuinely fixed and wired to the real caller -- that part holds fully. But the fix as delivered makes town/quiet/status/role/tier/model/effort/rotated_by/harness/settings unreachable on the master's OWN row specifically (still reachable on every OTHER row), which contradicts the parent hypothesis's own unqualified claim. Demoted proved -> inconclusive_lean_disproved:55 (confidence 0.85: high confidence in the finding itself; the lean sits near the midpoint because the urgent fix is real while a related capability regressed). Spawning one corrective kid next: the entry should be skipped only for the FIELDS self_row already covers on the actor's own row, not unconditionally for the whole entry, so actor_rows can still admit its OWN granted fields (town/quiet/status/...) on the actor's own row while self_row separately covers the identity cells.
<!-- THOUGHT:END -->

## Agent Notes
SM.115 fix landed in write.py _actor_rows_refusal (+8 lines): when every row this write changed on the list has match_key == the resolved seat, the actor_rows entry is skipped so self_row governs the own row; actor_rows still governs other rows. rotate._write_identity_cells own-row spawn write now ADMITTED; changing another seat's session_id still refused by name. 154 tests pass across the five named files.

tier-parent review a00-ec12fb27 iter115: 3 adversarial probes (auth/wire/gate) run against an independent fixture; auth+wire held, gate FALSIFIED -- sanctuary-master editing ONLY its own row's town field (no other row touched) is now refused (self_row lacks town; actor_rows skipped whole for own-row edits), where it was admitted before this diff (confirmed by removing just the 8 SM.115 lines and rerunning the same edit). Demoted proved -> inconclusive_lean_disproved:55. The urgent session_id/pid/generation rotation-blocking fix is real and wired to rotate._successor_row_write (verified independently). Corrective kid next: exempt only the FIELDS self_row already covers on the actor's own row, not the whole entry.
