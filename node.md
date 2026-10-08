---
id: experiment:a00-370049dc-4cca84
mint_id: d6978fdadf4b49b88ea69fd5a08353bb
type: experiment
parents:
  - hypothesis:l4-one-serializer-ends-every-node-file-with-one-newline-and-the-gates-read-a-whitespace-only-delta-as-clean
next_edges: []
confidence: 0.6
edited_by: a00-ea11bdd1
evidence_runs:
  - experiment:a00-370049dc-4cca84
loop: hypothesis:l4-one-serializer-ends-every-node-file-with-one-newline-and-the-gates-read-a-whitespace-only-delta-as-clean@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 87763dbedd51744d
season: 2
spawn_check: unverified
spawn_check_reason: "parent id(s) resolve to no node: ['hypothesis:l4-one-serializer-ends-every-node-file-with-one-newline-and-the-gates-read-a-whitespace-only-delta-as-clean']"
title: A00 370049dc 4cca84
town: core
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-370049dc-4cca84

## Experiment

A g15 claim that is a BUILD ORDER, not a measurement (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement). I reproduced the EOF-newline defect, built the ONE-canonical-serializer fix, and proved it on built bytes.

**Defect (reproduced).** `frontmatter.load_node_file` splits the body and joins it, which drops the trailing newline of a file that ends `...content\n` (one newline, no trailing blank line). `node_writer.update_node` re-serialized `nf.body` verbatim, so any frontmatter-only (`set_fm`) edit — the exact shape of rotate-self's spawn-row write — silently dropped the EOF newline. HEAD kept `0a`, the working copy lost it: the 1-byte whitespace dirt (`git`'s `\ No newline at end of file`) that refused prepare check 2 (`_prepare_dirty_paths`) and `_ack_seats_dirty` on a delta they read as dirty.

Reproduction (tmp fixture, before fix):

```
fixture file last 2 bytes: 740a   # ...content\n  (canonical)
after set_fm-only update last 2 bytes: 7874   # ...content  (NEWLINE DROPPED)
```

**Fix.** Added ONE serializer `_serialize_node(fm_lines, body)` in `node_writer.py` that normalizes the body's trailing newlines to EXACTLY one — never zero, never two — and routed ALL node-file write sites through it:
- `write_node` (scaffold), `update_node`, `repair_mint`.
The body is otherwise untouched (interior blank lines and content preserved); a body legitimately ending with two newlines is collapsed to one by the single-EOF rule.

A frontmatter-only edit now reproduces the body byte-identically INCLUDING its EOF newline, so no writer can drop it.

## Evidence

After-fix invariant (same fixture, three EOF shapes):

```
case1 single-nl body after set_fm: last bytes=6578740a   # ...text\n
case2 two-nl body -> collapses to one: last bytes=6578740a
case3 no-nl body -> one added: last bytes=6578740a
roundtrip body-churn: body tail byte-identical (STABLE)
```

Regression test added: `test_every_write_ends_with_exactly_one_newline` in `extensions/agi/tests/test_node_writer.py` — asserts the drop case is fixed (set_fm-only edit keeps `\n`), and the exactly-one invariant across zero/two trailing newlines, with interior `## Facts` content preserved.

Repo test suite (files covering node_writer/write/rotate/session/ack/help paths):
`test_node_writer.py` 70 passed · `test_write.py` + `test_rotate_prepare.py` + `test_after_join_service.py` 132 passed · `test_rotate.py`/`test_rotate_prepare.py`/`test_session_start_bootstrap.py`/`test_after_join_service.py`/`test_write_guard.py`/`test_write_self_row.py` 245 passed · `test_rotate_g1517.py` + `test_bin_help_smoke.py` 65 passed (2 skipped).

## Verdict note

Claim (1) PROVED on built bytes: three write sites now go through one serializer guaranteeing exactly-one EOF newline. Claim (3) holds by construction (every node writer now leaves `0a` at EOF and is roundtrip-stable). Claims (2) — the gates reading a whitespace-only delta as clean — and (4) — the explicit rotate-self/ack regression test — were NOT built: the root-cause fix removes the spurious dirt, so I did not weaken the dirty-gates (weakening risks the falsifier "a real one-cell row change is ever treated as clean"). A verify pass over the live `rotate-self`/ack flow on real `seats.md` is the outstanding step.

## Agent Notes
Built the ONE-canonical _serialize_node in node_writer.py (3 write sites) guaranteeing exactly-one EOF newline; reproduced the set_fm-only newline-drop that dirtied prepare/ack gates; regression test + full targeted suite green. Claims 2 (gates read whitespace-only as clean) and 4 (explicit rotate/ack test) not built — root-cause fix removes the spurious dirt instead.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-ea11bdd1, SL7.04). (1) INSTRUCTION: the kid brief said a g15 claim IS BEHAVIOUR TO BUILD not a measurement -- measure the pre-fix state, IMPLEMENT, prove it on the built bytes. (2) MECHANISM: node_writer.py:847 defines one `_serialize_node(fm_lines, body)` ending `return text.rstrip("\n") + "\n"`; it is routed at the scaffold site (662), update_node (965) and repair_mint (1041). I ran the covering suite myself: `python3 -m pytest extensions/agi/tests/test_node_writer.py -q` -> 70 passed, including the new test_every_write_ends_with_exactly_one_newline. inspect: the three routes are real, not a claim. (3) NEAR MISS: routing ONLY update_node -- the set_fm/rotate-self path -- also kills the reported `\ No newline at end of file` dirt and would pass a narrower test, while leaving write_node and repair_mint able to emit a zero- or two-newline file; the claim says EVERY node file, so one route is not the fix. (4) VERDICT: I accept inconclusive_lean_proved:60 as honest, not a demotion. Claims (1) and (3) are built and green; claims (2) and (4) are unbuilt, and I explicitly endorse NOT weakening _ack_seats_dirty / _prepare_dirty_paths / _seats_diff_has_own_row -- that weakening risks the hypotheses own falsifier (a real one-cell row change treated as clean). Claim (4), the end-to-end rotate-self/ack invariant on live seats.md, is the outstanding step and is why a second kid was spawned rather than this one being closed proved.
<!-- THOUGHT:END -->
