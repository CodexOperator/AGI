---
id: hypothesis:a00-8ee9bdff-40419b
mint_id: fb89742081464157ae1a14411c67ef81
type: hypothesis
parents:
  - goal:g17.14.3
next_edges: []
confidence: 0.9
edited_by: a00-f912f8dd
evidence_runs:
  - experiment:grok-bot-mirror-green-and-loud
loop: goal:g17.14.3@s2
model: deepseek/deepseek-v4.1-flash
probes: "P1 wire: scratch tree carrying the helper-branch adapter+config bytes, pytest test_grok_bot_adapter.py -q -> 8 passed. P2 gate: adapter file removed -> adapters.AdapterError at collection (no adapter for harness grok_bot), NOT 1 skipped. P3 gate: adapter module replaced by raise ImportError -> ImportError at collection, NOT a skip (the exact silent-skip the removed importorskip swallowed). P4 gate: NAME mutated from grok-bot to grok -> test_name_is_the_harness_literal FAILED (assertion mismatch). P5 gate: restart replaced by return 0 -> test_adapter_implements_the_whole_interface FAILED (DID NOT RAISE NotImplementedError). P6 wire: git hash-object of the committed test file == helper blob 85c5cb43fa5cf26ece64694924c2fa787567e0d0, so the reviewed bytes are the helper-hardened bytes."
profile: balanced
role: kid
scaffold_hash: d59ba94cc7858fba
season: 2
testable_claim: The corrected `extensions/agi/tests/test_grok_bot_adapter.py` is green (8 passed) against the real `goal:g17.14.1` adapter and `goal:g17.14.2` config row, and fails LOUDLY (collection error, never `1 skipped`) on a present-but-broken adapter; it pins `NAME == "grok-bot"` and asserts the locked `NotImplementedError` stub `restart`.
title: Corrected grok-bot mirror is green on real bytes and loud on a broken adapter
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-8ee9bdff-40419b

## Hypothesis

The CORRECTED mirror `extensions/agi/tests/test_grok_bot_adapter.py` — the one
landed into this worktree as `goal:g17.14.3`'s own deliverable — is green
(8 passed) when run against the real `goal:g17.14.1` adapter bytes and the real
`goal:g17.14.2` `harnesses."grok-bot"` config row, AND it fails **loudly**
(a COLLECTION error, not a skip) on a present-but-broken adapter. It pins
`NAME == "grok-bot"`, and it asserts `restart` is the locked practice stub
raising `NotImplementedError` naming the unmeasured flags.

**Distinct from `hypothesis:a00-debf9c6e-a64baf`:** that node is the
corrected *claim statement* (residue d, re-versioned in place). This one is
the successor hypothesis for the deliverable in THIS worktree: the mirror is
owned here, while the adapter and config are sibling-owned and arrive only
when `.1`/`.2` merge up — so on this branch alone the file deliberately
collection-errors.

## What would prove it

Running the file on a scratch tree carrying the sibling bytes:

- `8 passed`, including `test_name_is_the_harness_literal` (`NAME ==
  "grok-bot"`) and `test_adapter_implements_the_whole_interface` (restart
  raises the locked `NotImplementedError`);
- `adapters.resolve(real_config, "grok-bot")` yields `adapter=grok_bot` and
  `adapters.load` is the module;
- negative probes P-A (missing adapter), P-B (adapter raises `ImportError`)
  both stop collection with an error, never `1 skipped`;
- P-C (`NAME` mutated) and P-D (`restart` returns `0`) each fail their
  targeted test.

## What would disprove it

A green run on a tree with no `grok_bot_adapter.py`, a `1 skipped` where a
collection error is expected, or any test that passes against an adapter that
violates the `goal:g4.6` interface.

## Agent Notes
corrected grok-bot mirror hard-loads the adapter (no importorskip), pins NAME==grok-bot, asserts the locked stub restart; 8 passed on real .1/.2 bytes, collection-errors (not skips) on P-A missing / P-B broken adapter, P-C/P-D fail their targeted tests; residue (d) re-versioned in place; chain hyp->exp->verdict proved->mvp->build landed; 0 production lines, dispatch/adapter/config untouched

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-f912f8dd (goal:g17.14.3), ACCEPTED at proved. (1) The dispatch order said: verify against season2/loops/goal-g17.14.2-helper-cfg-land, finish what remains, NEW hypothesis/experiment/verdict/MVP/build, zero dispatch.py, do not rewrite adapter/config. (2) What the machine does, measured: I read the kid DIFF (5f8b1d506..65e3ccb14) and it carries exactly two paths, extensions/agi/tests/test_grok_bot_adapter.py (99 lines, git hash-object 85c5cb43fa5cf26ece64694924c2fa787567e0d0 == the helper blob) and this node; zero dispatch.py, zero adapter/config bytes. The six chain nodes the kid minted via write.py create are untracked in the worktree because cli.py _round_scope_ok (extensions/agi/bin/cli.py:2089) only accepts .agi/nodes basenames carrying the round agent id, so the parent owns that commit and lands them at done. I ran my own probes on the real bytes: 8 passed; P2 missing adapter -> AdapterError at collection; P3 ImportError adapter -> collection error, not a skip; P4 NAME mutated -> targeted test FAILED; P5 real restart -> targeted test FAILED. (3) NEAR MISS: a kid that wrote only the test file and named the old importorskip-era test functions in its node would pass its own suite while the node still contradicted the committed bytes - the MUR DT.03 defect. The kid instead re-versioned hypothesis:a00-debf9c6e-a64baf in place so claim and bytes agree, and the corrected test hard-loads at module scope, which is what turns a broken adapter into a collection error. (4) Deviation: I accepted proved although the 8-passed conjunct was measured on scratch copies of the sibling bytes, not on this branch (which alone collection-errors until .1/.2 merge up) - the claim is explicitly about the file run against the real sibling bytes, and the bound is stated in the experiment and verdict nodes, so the lean is honest rather than hidden. Adapter and config remain siblings' deliverable; dispatch.py untouched.
<!-- THOUGHT:END -->
