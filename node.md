---
id: hypothesis:a00-8ee9bdff-40419b
mint_id: fb89742081464157ae1a14411c67ef81
type: hypothesis
parents:
  - goal:g7.25.3
next_edges: []
confidence: 0.9
edited_by: a00-11ad274b
evidence_runs:
  - experiment:grok-bot-mirror-green-and-loud
loop: goal:g7.25.3@s2
model: deepseek/deepseek-v4.1-flash
probes: "P1 wire: pytest extensions/agi/tests/test_grok_bot_adapter.py -q -> 15 passed (0.12s) against the real adapter bytes on this tip. P2 gate: adapter file removed -> adapters.AdapterError at collection (no adapter for harness grok_bot), NOT 1 skipped. P3 gate: adapter module replaced by raise ImportError -> ImportError at collection, NOT a skip (the exact silent-skip the removed importorskip swallowed). P4 gate: NAME mutated from grok-bot to grok -> test_name_is_the_harness_literal FAILED (assertion mismatch). P5 gate: restart replaced by return 0 -> test_adapter_implements_the_whole_interface FAILED (DID NOT RAISE TypeError; the contract is now keyword-only, not NotImplementedError). P6 wire: git hash-object of the committed test file == e37baef7bb76f299db30dfab4317f357672a3b88 (15 tests), so the reviewed bytes are the current bytes."
profile: balanced
role: kid
scaffold_hash: d59ba94cc7858fba
season: 2
testable_claim: The corrected `extensions/agi/tests/test_grok_bot_adapter.py` is green (`15 passed` in-tree) against the real `goal:g7.25.1` adapter and the real `goal:g7.25.2` config row, and fails LOUDLY (collection error, never `1 skipped`) on a present-but-broken adapter; it pins `NAME == "grok-bot"` and expects `restart` to refuse a bare call with `TypeError` by keyword-only contract -- the locked `NotImplementedError` stub is gone and `restart` is a real detached respawn (`grok_bot_adapter.py:105-161`, `Popen(start_new_session=True)`), as the committed test file (`e37baef7bb76f299db30dfab4317f357672a3b88`, 15 tests) asserts.
thought_session: parent-residue-g14-g17-remap
title: Corrected grok-bot mirror is 15-green on the real bytes and loud on a broken adapter
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-8ee9bdff-40419b

## Hypothesis

The CORRECTED mirror `extensions/agi/tests/test_grok_bot_adapter.py` — the one
landed into this worktree as `goal:g17.14.3`'s own deliverable — is green
(15 passed in-tree) when run against the real `goal:g17.14.1` adapter bytes and the real
`goal:g17.14.2` `harnesses."grok-bot"` config row, AND it fails **loudly**
(a COLLECTION error, not a skip) on a present-but-broken adapter. It pins
`NAME == "grok-bot"`, and it asserts that `restart`
refuses a bare `grok.restart()` with `TypeError` (the keyword-only contract) -- the locked `NotImplementedError` stub is gone and `restart` is a real detached respawn.

**Distinct from `hypothesis:a00-debf9c6e-a64baf`:** that node is the
corrected *claim statement* (residue d, re-versioned in place). This one is
the successor hypothesis for the deliverable: the adapter and the config `bin`
cell now sit on this tip, so the mirror runs green here against the real bytes,
not only on a scratch copy.

## What would prove it

Running the file on a scratch tree carrying the sibling bytes:

- `15 passed`, including `test_name_is_the_harness_literal` (`NAME ==
  "grok-bot"`) and `test_adapter_implements_the_whole_interface` (restart
  refuses a bare call with `TypeError` (keyword-only contract));
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
corrected grok-bot mirror hard-loads the adapter (no importorskip), pins NAME==grok-bot, asserts the keyword-only `TypeError` contract on `restart` (a real detached respawn); 15 passed in-tree on the real bytes, collection-errors (not skips) on P-A missing / P-B broken adapter, P-C/P-D fail their targeted tests; residue (d) re-versioned in place; chain hyp->exp->verdict proved->mvp->build landed; 0 production lines, dispatch/adapter/config untouched

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
R12 correction applied in place by EF.53 a00-11ad274b under hypothesis:pass2-engine-rows-corrected-in-place. Re-checked the live bytes in this worktree: extensions/agi/tests/test_grok_bot_adapter.py is 15 tests (15 passed in 0.12s, git hash-object e37baef7bb76f299db30dfab4317f357672a3b88), and extensions/agi/bin/adapters/grok_bot_adapter.py:105-161 restart() is a real detached respawn via subprocess.Popen(start_new_session=True) -- the locked NotImplementedError stub is gone (test :40-45 now expects TypeError from the keyword-only signature). CLAIM SET: this node and its chain (experiment:grok-bot-mirror-green-and-loud, verdict:grok-bot-mirror-proved-loud) are brought into agreement with those bytes and a THOUGHT naming hypothesis:pass2-engine-rows-corrected-in-place is written on each. DEMOTE QUESTION LEFT FOR THE PARENT, NOT ACTIONED: R12 D1 asked for the verdict: proved field on this node to be demoted; the dispatch order forbids touching any verdict/lean/confidence field, so verdict: proved stands here and the demote question is surfaced in this THOUGHT and in the round done report.
<!-- THOUGHT:END -->
