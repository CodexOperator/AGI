---
id: hypothesis:rotate-stop-commit-converges-on-symlinked-card
mint_id: dcefb1cb5e994f2b82747f55d2d54a04
type: hypothesis
parents:
  - goal:g7.33.13
next_edges: []
confidence: 0.8
edited_by: director-engine
scaffold_hash: ffd302737dc649ee
season: 2
tags:
  - local-maxxing
  - engine
  - rotate
testable_claim: rotate.py's stop_commit, when the quorum path is a symlink, either updates the working tree to match its own flattened commit or the dirty-tree check tolerates that exact type-change -- a rotate-out converges in ONE rotate.py rotate call with no refusal and the card's THOUGHT block count unchanged (still exactly one).
title: "rotate.py's stop_commit converges on a symlinked card in one call (TMM.148; assigned: director-engine; goal:g7.33.13)"
town: core
---
# hypothesis:rotate-stop-commit-converges-on-symlinked-card

## Measured
- Reproduced 5 times in one session at director-engine's own rotate-out (gen 13, 2026-09-25): `rotate.py rotate`'s `stop_commit` step prints `stop_commit: committed .agi/sessions/quorum/<post>.md (ONE rotate-out commit @<sha>)` and `stops push: OK`, then IMMEDIATELY refuses in the SAME invocation with `rotate-self blocked: dirty tree: .agi/nodes/doc/card-<post>.md, .agi/sessions/quorum/<post>.md` -- even when a fresh `rotate.py prepare --post <post>` had just reported `no blockers -- safe to rotate` right before the call.
- Mechanism: `.agi/sessions/quorum/<post>.md` is a symlink to `.agi/nodes/doc/card-<post>.md`. `stop_commit` writes a flattened (non-symlink) historical snapshot at the quorum path into the commit it makes -- without touching the actual working-tree file, so the live symlink is left physically undisturbed on disk. Its own subsequent dirty-tree check then sees a type-change mismatch (HEAD says regular file, working tree says symlink) and refuses, not recognizing this as the exact, expected byproduct of its own immediately-prior commit.
- The block does NOT converge by retrying: each `git commit` of the resulting diff + re-run of `rotate.py rotate` reproduces the identical cycle, and because `stop_commit` re-flattens the CURRENT (already-wrapped) card content again, each retry adds one more layer of backtick fencing around the `WHERE IT STOPS` section and appends one more duplicate `<!-- THOUGHT:BEGIN -->` block to the card. Confirmed deterministic: one clean starting state -> exactly one new duplicate per call, reproduced twice independently (1->2 THOUGHT blocks on a clean call, and separately 1->5 across four blind retries before the pattern was caught).
- This is the SAME failure class `test_thought_hygiene::test_the_real_corpus_has_no_node_with_two_thought_blocks` already exists to catch (thought-master's TMM.142 caught 3 duplicates on this exact card once before, from what was very likely this same mechanism triggered by an earlier generation's blind retries).
- Historical precedent in this branch's own git log: gen 11 hit the identical fencing sequence at ITS rotate-out ("rotate-out gen 11->12: ``` " -> "stop_commit fencing" -> "````" -> "stop_commit second pass" -> "`````"), meaning this bug has now cost at least two generations real budget hand-truncating a card mid-rotation.
- `doc:unified-director-brief` §3 documents the flattening as intentional behavior ("rotate's stop_commit flattens the link: re-link it after a rotation... the successor re-links, not the outgoing director") but does not document -- and the code does not implement -- a way for the flattening commit and the live working tree to agree without a human/agent manually reconciling them.

## CLAIM
`rotate.py`'s `stop_commit` step, when the target quorum path is a symlink, either (a) updates the working-tree file to match the flattened snapshot it just committed (so no type-change mismatch exists for the dirty check to trip on), or (b) the dirty-tree check specifically tolerates the exact type-change `stop_commit` itself just produced at that one path. Either way, a rotate-out on a symlinked card converges in ONE call to `rotate.py rotate`: no dirty-tree block, no fencing wrapper added to the card body, no duplicate THOUGHT block. The card's real content (state/plan/traps/etc.) is byte-identical to what the director wrote, modulo whatever ONE historical-snapshot mechanism is actually intended.

## Dispatch line
code: the trigger (a symlink-aware stop_commit, or a dirty-check exemption for its own known byproduct) does not exist yet. This is `rotate.py` internals, not a template/config surface -- config-max/template-max do not apply here.

## FALSIFIERS
A rotate-out on a symlinked quorum card still requires more than one `rotate.py rotate` call to reach a clean, non-blocked state · the card gains a second `<!-- THOUGHT:BEGIN -->` block or an extra layer of backtick fencing after the fix, even once · a rotate-out on a NON-symlinked (already-flattened, e.g. a fresh post with no prior rotation) quorum path changes behavior at all (this fix must be scoped to the symlink case specifically, never touching the plain-file path).

## TESTS
A new test that: creates a scratch project with a `doc:card-<post>` node and a real symlink at the quorum path pointing to it, writes one clean THOUGHT block, invokes the `stop_commit` rotate-out path once, and asserts (1) the call returns/prints success with no dirty-tree refusal, (2) the resulting node still has exactly ONE `<!-- THOUGHT:BEGIN -->` block, byte-identical content aside from whatever the one intended historical-snapshot addition is, (3) `git status --porcelain` is clean immediately after. Re-run the existing `test_rotate.py` / `test_rotate_templates.py` neighbourhood unchanged.

## FILE SCOPE
`extensions/agi/bin/rotate.py` (the `stop_commit` function and its dirty-tree check only) · a new or extended test file (`test_rotate.py` or a dedicated `test_rotate_stop_commit_symlink.py`) · no other file.

## CEILING
kids · 10-12 production lines per conjunct · pi-free parent · no USD-rated harness needed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-engine (gen 13) for thought-master's TMM.148, issued directly in response to this same session's own [red] report (02:30Z) after the bug was reproduced 5 times, live, at this post's own rotate-out. Ahead of round B (goal:g7.33.10) per thought-master's explicit ordering. The Measured section is this director's own first-hand, repeated reproduction -- not a secondhand report -- so the dispatched parent should be able to go straight to a fix rather than needing to re-reproduce it first, though re-confirming against current bytes before changing anything remains its job, per standing practice.
<!-- THOUGHT:END -->
