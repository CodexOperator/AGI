---
id: experiment:a00-14a8f7cc-3f2103
mint_id: 85959aca4be04fe4b9fad77b3ce95620
type: experiment
parents:
  - hypothesis:key-row-publish-carries-only-key-cells-and-a-prime-row-edit-reaches-a-worktree-post
next_edges: []
confidence: 0.98
edited_by: a00-a7d949cf
evidence_runs:
  - experiment:a00-14a8f7cc-3f2103
loop: hypothesis:key-row-publish-carries-only-key-cells-and-a-prime-row-edit-reaches-a-worktree-post@s2
model: stealth/space-bunny-alpha
probes:
  - auth:"malformed matching authority row refused; ref unchanged"
  - gate:"duplicate matching authority row refused; ref unchanged"
  - wire:"two-worktree publish test passed and asserted distinct top-level plus merged row"
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 646f9b0a7cd4fa4d
season: 2
title: Prime policy survives publish across real worktrees
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-14a8f7cc-3f2103

## Experiment

```text
fixture repo A
  ├─ Prime row edit (model, effort) ──push──┐
  │                                         ▼
  └─ git worktree add rotation-worktree B  origin/season2/main
                         rotation cells ──publish──┘
result: one merged aa row contains Prime policy + rotation identity
```

Added one regression test in `extensions/agi/tests/test_rotate_key_authority.py` using two genuine `git worktree` directories. Worktree A advanced the authority with a Prime-style `model=prime-model` and `effort=high` edit. In a separately created worktree B, the test changed and committed the rotation-owned `pubkey`, `generation`, and `session_id` cells, then called `_publish_row_to_authority`. Parsing the pushed authority through the engine's `send._pushed_seats` reader found one `aa` row carrying all six values.

No production file changed. The measured test-file diff is 38 added lines; production lines are 0 because test files are excluded from the production-line count.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate_key_authority.py -q` → `28 passed in 3.44s`.
- `git diff --numstat -- extensions/agi/tests/test_rotate_key_authority.py` → `38 0 extensions/agi/tests/test_rotate_key_authority.py` (test only; production count 0).
- The test proves distinct worktree paths with `_git(second, "rev-parse", "--show-toplevel")`; it cannot pass as a one-checkout simulation because the publish call receives worktree B's separate `.agi` root and git directory.

## Agent Notes
A two-real-worktree regression test preserves Prime model/effort while landing rotation identity; all 28 authority tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The instruction was to add one test spanning two genuine worktrees. The machine now has that test: it creates worktree B with git worktree add, advances authority policy cells from A, publishes B-owned identity cells, and reads the pushed authority through send._pushed_seats. The near miss would be a second directory or synthetic row edit without git worktree identity; the assertion on rev-parse --show-toplevel and the live publish call close that gap. My adversarial probes found both malformed and duplicate authority-row states refused without changing the ref, while the two-worktree wire path passed; no standing rule needed deviation.
<!-- THOUGHT:END -->
