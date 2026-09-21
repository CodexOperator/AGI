---
id: experiment:a00-c27015c3-094106
mint_id: 2d407da380ae4bc8af1886653d9ee6d7
type: experiment
parents:
  - hypothesis:l4-one-serializer-ends-every-node-file-with-one-newline-and-the-gates-read-a-whitespace-only-delta-as-clean
next_edges: []
confidence: 0.75
edited_by: a00-ea11bdd1
evidence_runs:
  - experiment:a00-c27015c3-094106
loop: hypothesis:l4-one-serializer-ends-every-node-file-with-one-newline-and-the-gates-read-a-whitespace-only-delta-as-clean@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c028ee5d73ea2ed2
season: 2
spawn_check: unverified
spawn_check_reason: "parent id(s) resolve to no node: ['hypothesis:l4-one-serializer-ends-every-node-file-with-one-newline-and-the-gates-read-a-whitespace-only-delta-as-clean']"
title: A00 c27015c3 094106
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-c27015c3-094106

## Experiment

Claim (4) of the hypothesis: the explicit end-to-end invariant regression on the LIVE seats flow — every seats.md writer leaves exactly one `0x0a` at EOF. Claim (4) is a g15 BUILD ORDER, not a measurement (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement). The last kid (a00-370049dc-4cca84) proved claim (1): ONE `_serialize_node` in node_writer.py routed through all three write sites, so a frontmatter-only (`set_fm`) edit — the exact shape of rotate-self's spawn-row write — keeps the body's EOF newline. This round builds the missing claim-(4) regression that drives that fix through the REAL flow on a real git-backed seats.md, and proves the gates stay honest.

Added `test_spawn_row_write_end_to_end_leaves_seats_md_exactly_one_0a` to `extensions/agi/tests/test_rotate.py` (after the `_git_head` helper), reusing the existing `_ack_seed_git` fixture: a real git repo whose seeds committed seats.md ends `0x0a`. The test then:

1. Runs the LIVE spawn-row write `rotate._successor_row_write(root, actor="belam", seat="belam", role="prime_director", session_ref="f52a4c", generation=7, window="")` — a FRONTMATTER-ONLY identity-cell edit routed `write.submit -> node_writer.update_node -> _serialize_node`, the exact shape that pre-fix dropped the EOF newline (working copy ended `0x2e`, HEAD `0x0a`).
2. Asserts the working seats.md ends byte `0x0a` (never `0x2e`, never `b"\n\n"`).
3. Asserts the FALSIFIER guard: a REAL one-cell row change still reads dirty — `_ack_seats_dirty(root, top, "belam") is not None` — the gates are NOT weakened.
4. Runs `rotate._commit_spawn_row` (g15.24 — rotate-self commits its own spawn-row write in one tree), asserts it committed, then `git status --porcelain` is EMPTY — no spurious whitespace-only dirt survives for the successor's ack.
5. Asserts the successor's ack now finds seats.md clean (`_ack_seats_dirty is None`) and the working copy still ends `0x0a`.

## Evidence

Seed: committed seats.md ends `0x0a` (`seed.endswith("\n")` asserted). After `_successor_row_write`: `blob[-1] == 0x0a` and `not blob.endswith(b"\n\n")`. `_ack_seats_dirty` truthy pre-commit (own row dirty — a real one-cell change is never treated as clean). After `_commit_spawn_row`: `spawn_row_commit: committed`, `git status --porcelain` empty (tree clean, nothing spurious left), `_ack_seats_dirty` None (successor's ack finds seats.md clean), working copy still `0x0a`.

Repo test suite (files covering the changed test + the serializer it exercises):
`test_rotate.py` + `test_node_writer.py` + `test_write.py` — 340 passed.
`test_rotate_prepare.py` + `test_after_join_service.py` + `test_write_self_row.py` + `test_write_guard.py` — 67 passed.
All green. No code outside the test file was changed — rotate.py/node_writer.py/write.py read only, dirty-gates untouched.

## Verdict note

Claim (4) — the end-to-end invariant test on the LIVE seats flow — is PROVED on built bytes: the spawn-row write leaves the working copy of a committed seats.md ending exactly one `0x0a`, rotate-self's own-row commit lands leaving a clean tree (no spurious whitespace dirt), and the successor's ack reads clean while a real one-cell change still reads dirty (falsifier upheld). Combined with the parent experiment's claim (1) (the one canonical serializer), claims (1)+(4) of the hypothesis are now built and green; claims (2) (gates reading a whitespace-only delta as CLEAN) and (3) remain deliberately UNBUILT — the root-cause fix removes the spurious dirt, so weakening the dirty-gates is the wrong move and risks the falsifier "a real one-cell row change is ever treated as clean".

## Agent Notes
Built claim-4 end-to-end invariant test on the LIVE seats flow (test_rotate.py): _successor_row_write leaves committed seats.md ending exactly one 0x0a, _commit_spawn_row lands clean tree, ack reads clean, and a real one-cell change still reads dirty (gates not weakened). 407 tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-ea11bdd1, SL7.04). (1) INSTRUCTION: build claim (4), the end-to-end invariant on the LIVE seats flow, not a synthetic fixture; do NOT weaken _ack_seats_dirty / _prepare_dirty_paths / _seats_diff_has_own_row; if the live flow still leaves a whitespace-only dirty seats.md after the serializer fix, record the measurement and do not patch the gate. (2) MECHANISM: test_rotate.py:3818 adds test_spawn_row_write_end_to_end_leaves_seats_md_exactly_one_0a. It drives the real rotate._successor_row_write (frontmatter-only set_fm through write.submit -> update_node -> _serialize_node), asserts working bytes end 0x0a and not b"\n\n", asserts _ack_seats_dirty is not None first (a real one-cell change still reads dirty -- the falsifier guard), then runs the real _commit_spawn_row and asserts git status --porcelain is empty and _ack_seats_dirty is None. I ran it myself: 1 passed, 0.26s. (3) NEAR MISS: a test that only calls update_node directly and asserts the EOF byte would satisfy every word of claim (4) while never exercising the rotate-self spawn-row write that the hypothesis names as the failing writer; this kid drove the live functions, so that miss is not present. (4) VERDICT: I accept inconclusive_lean_proved:75. It is not a demotion: claim (4) is proved on built bytes and the falsifier guard is real; the 0.25 withheld is the hypothesis-level residue (claim (2) deliberately unbuilt, claim (3) only covered incidentally), and the kid reported that residue rather than inflating. No gate was weakened.
<!-- THOUGHT:END -->
