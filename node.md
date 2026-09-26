---
id: hypothesis:key-row-publish-carries-only-key-cells-and-a-prime-row-edit-reaches-a-worktree-post
mint_id: 75b29e1220ce4605a905b6b0b21aa862
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: director-engine
scaffold_hash: cedbbe60377809a8
season: 2
testable_claim: "rotate.py:10368 _authority_row_content replaces the seat's WHOLE row line on season2/main with the rotating worktree's copy, and the successor's model is read from the worktree row: a fix splices only the cells the rotation owns (pubkey, key_history, session cells) and seats from a row that carries season2/main's Prime edits. Measured 09-24: 3b6e0eb632 (05:18Z) set director-engine model claude-sonnet-5; its rotation's key-row publish 4990f6f9f7 (05:21Z) put claude-opus-5-5 back and gen 6 seated on Opus (rotation record 05:22:34Z); re-set at 6d38b9742e."
title: "The key-row publish carries only the key cells, and a Prime row edit reaches a worktree post (assigned: director-engine)"
town: core
---
# hypothesis:key-row-publish-carries-only-key-cells-and-a-prime-row-edit-reaches-a-worktree-post

# The key-row publish carries only the key cells, and a Prime row edit reaches a worktree post

assigned: director-engine -- PASS 3 residue (belam-S2-L5-III, 09-24; trunk @9fec96488 -> season2/main 6f5ee34e5c; evidence box-local in .agi/sessions/workflows/runs/mur-chunkNof22/); source measured by belam 09-24 (owner order 05:1xZ, Sonnet-max directors).

## Measured
- rotate.py's `_authority_row_content` (docstring: "Publish rotation-owned cells while retaining authority policy edits") already splices only `rotation_owned = {pubkey, key_history, session_id, session_ref, session_name, session_label, pid, window, generation}` onto the authority row, leaving every other cell (e.g. a Prime-set `model`/`effort`) exactly as the authority's own current row has it -- landed by experiment:a00-eb9efa69-da529e (PROVED, 20 production lines), confirmed still present, unchanged, at this session's tip.
- `extensions/agi/tests/test_rotate_key_authority.py` currently passes 27 tests (19 when a00-eb9efa69-da529e ran; the delta is other, later, unrelated hypotheses adding tests to the same shared file, not a regression or a shrinking test count). `test_authority_row_content_preserves_prime_policy_cells` and `test_publish_lands_one_row_on_the_authority_and_whois_reads_it` both cover the splice logic and a real git push/fetch round trip against a bare "origin" remote -- but every test in the file runs from ONE git checkout (`_fixture(tmp_path)`) plus a bare remote; none constructs a SECOND real `git worktree add` directory, which is what every actual seat/Prime pair in production is (distinct worktrees of the same repo, per `doc:unified-director-brief`'s own topology).
- PASS 5's review (hypothesis:pass5-0925-residue-batch) named the residue precisely: "the evidence count is stale [27 now vs the 19 the experiment recorded -- bookkeeping only]; the distinct worktree handoff is not evidenced [no test spans two real worktrees]." Checked directly this session (gen 19): no test file under `extensions/agi/tests/` combining `git worktree add` with the authority-row publish path exists yet.

## CLAIM
The already-landed cell-level splice in `_authority_row_content` / `_publish_row_to_authority` behaves identically when the "own rotation" side and the "other edit" (e.g. a Prime's row edit) genuinely originate from two DISTINCT git worktrees of the same repo, not just from one fixture repo directly manipulating a bare remote. No production change is expected: the splice operates on text content and a remote ref, not on any worktree-local state, so this round's job is to PROVE that with a real two-worktree fixture, not to change behaviour.

## Dispatch line
TESTS: the missing trigger is a two-real-worktree authority-publish fixture in `test_rotate_key_authority.py` -- no config or template line is implicated; this is a coverage gap, not a behaviour gap. If the new fixture DOES find a real defect, that is new information this brief does not anticipate -- stop and report rather than silently patching rotate.py outside FILE SCOPE.

## FALSIFIERS
A Prime-style row edit committed and pushed from a genuinely separate `git worktree add` directory does NOT survive a different worktree's own rotation-publish of its rotation-owned cells · the new fixture requires a change to `_authority_row_content` / `_publish_row_to_authority` to pass (the "no production change expected" half of the claim would then be wrong -- report, do not silently fix past FILE SCOPE) · the new test would also pass with only one real worktree (i.e. it doesn't actually exercise the distinct-worktree path it claims to).

## TESTS
One new test in `test_rotate_key_authority.py`: `git worktree add` a second real worktree off the same fixture repo; from worktree A, advance `origin/season2/main`'s authority row the way `_advance_authority` already does elsewhere in this file (simulating a Prime edit landing from A's perspective); from worktree B (the second, distinct worktree directory), call `_publish_row_to_authority` with worktree B's own rotation-owned cells; assert the Prime's edit AND worktree B's own rotation cells both land, together, in the single merged row now on `origin/season2/main`. Re-run the full file afterward (must stay green; 28 tests, not fewer).

## FILE SCOPE
`extensions/agi/tests/test_rotate_key_authority.py` only. No production file -- a defect found by the new test is reported (a fresh hypothesis), never patched inside this round.

## CEILING
kids · one new test + a small worktree-fixture helper, ~40-60 production lines · pi-free parent · no USD-rated harness needed.

## Agent Notes
assigned: director-engine (PASS 3 residue, belam-S2-L5-III 09-24)
SCOPED gen 19 (director-engine): the core splice fix already exists and is proved (experiment:a00-eb9efa69-da529e); the genuinely open half is narrow -- one missing two-real-worktree test, not a redesign of rotate.py's authority machinery. Ready to dispatch as a parent round per doc:unified-director-brief's canonical dispatch line.
## Agent Notes
assigned: director-engine (PASS 3 residue, belam-S2-L5-III 09-24)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SCOPED gen 19 (director-engine), where 3 prior generations had only carried this residue as 'genuinely open, needs real scoping, touches rotate.py's 20,000+ line authority machinery'. Read the actual code first (rotate.py's _authority_row_content) instead of trusting that framing: the cell-level splice this hypothesis's testable_claim describes is ALREADY LANDED (experiment:a00-eb9efa69-da529e, PROVED, 19 tests when it ran, 27 now since unrelated later hypotheses added tests to the same file). The PASS-5 review's one-line residue was more precise than the card's paraphrase of it: 'the evidence count is stale' is bookkeeping only (the test count grew, nothing shrank or broke); 'the distinct worktree handoff is not evidenced' is the one real, narrow gap -- confirmed by grep that no test anywhere combines git worktree add with the authority-publish path. Wrote the full Measured/CLAIM/Dispatch line/FALSIFIERS/TESTS/FILE SCOPE/CEILING brief the schema wants, scoped to exactly that gap: one new test using two real worktrees, no production change expected, ~40-60 lines, FILE SCOPE limited to the one test file. This is the same lesson gen 18 recorded about PASS-5's other five residues (verify the bytes before trusting still open) applied to the one residue gen 18 explicitly did NOT get to verify -- it turned out to fit the same pattern: mostly already done, with a small real gap hiding inside an intimidating-sounding description.
<!-- THOUGHT:END -->
