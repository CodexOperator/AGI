---
id: experiment:a00-38ccd381-9a9b49
mint_id: 872fe088f1244f5d941e14e98b12ede1
type: experiment
parents:
  - hypothesis:authority-publish-plumbing-git-calls-are-bounded-and-never-raise
next_edges: []
confidence: 0.99
edited_by: a00-20b26531
evidence_runs:
  - experiment:a00-38ccd381-9a9b49
loop: hypothesis:authority-publish-plumbing-git-calls-are-bounded-and-never-raise@s2
model: stealth/space-bunny-alpha
probes: "wire: parent_negative_probe.py forced TimeoutExpired at commit-tree, observed all six GIT_INDEX_FILE plumbing calls rev-parse/hash-object/read-tree/update-index/write-tree/commit-tree with truthy timeout, then observed authority FAILED naming timeout and retry preserving key/pending; 1 passed in 0.60s"
production_lines: 9
profile: balanced
role: kid
scaffold_hash: 9adc5a01bd58240b
season: 2
title: Independent verification of bounded authority plumbing calls
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-38ccd381-9a9b49

## Experiment

Independently verified the already-landed implementation for the parent claim. In `_publish_row_to_authority`, the local `_g` helper supplies `timeout=60` to every plumbing call (`rev-parse`, `hash-object`, `read-tree`, `update-index`, `write-tree`, and `commit-tree`). The enclosing build `try` translates `TimeoutExpired` and `OSError` into `last`, breaks without escaping, and the function's existing terminal path returns `authority: FAILED -- <cause>`.

The regression test exercises the timeout at `hash-object`, asserts the result is FAILED (not SKIPPED), records a truthy timeout, and verifies the authority retry preserves the active key and pending successor key.

```text
implementation: bounded plumbing timeout + narrow TimeoutExpired/OSError translation
result:         authority FAILED, retry deferral preserved
changed bytes:  none (duplicate experiment; implementation and tests already present)
```

## Evidence

```text
python3 -m pytest extensions/agi/tests/test_rotate_key_authority.py extensions/agi/tests/test_rotate_pending_swap_authority.py -q
27 passed in 4.64s
```

```text
git diff --numstat -- extensions/agi/bin/rotate.py
9	0	extensions/agi/bin/rotate.py
```

The 9-line production delta was already present in this checkout when the duplicate experiment was dispatched. This run independently inspected the implementation and reran the focused plus neighbour suite. No additional production or test bytes were changed.

## Agent Notes
Verified every authority plumbing call is timeout-bounded, exceptions yield FAILED, retry remains deferred, and 27 focused/neighbour tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Instruction: prove that hash-object TimeoutExpired yields authority FAILED, every _g call carries a timeout, and retry defers. Machine: rotate.py:10469-10471 inserts timeout=60 into _g; rotate.py:10499-10509 catches only TimeoutExpired/OSError, sets last, breaks, and finally unlinks; the parent wire probe (1 passed in 0.60s) forced the final commit-tree call to time out and observed all six index-scoped plumbing calls with truthy timeouts, the named FAILED line, and unchanged active key plus surviving pending. Near miss: the kid test stops at hash-object, so it sees only the first two plumbing calls and cannot by itself prove update-index/write-tree/commit-tree remain bounded; forcing the last call closes that gap. This duplicate independent run is accepted, while experiment:a00-c1c9aaee-097089 failed on a 401 before its own title/done and is not owned or credited by this node.
<!-- THOUGHT:END -->
