---
id: experiment:a00-cd8388f0-512d24
mint_id: 5fa9473d405548a9bc46f9e2a8276a21
type: experiment
parents:
  - hypothesis:rotate-stop-commit-converges-on-symlinked-card
next_edges: []
confidence: 0.97
edited_by: a00-78108e94
evidence_runs:
  - experiment:a00-cd8388f0-512d24
loop: hypothesis:rotate-stop-commit-converges-on-symlinked-card@s2
model: stealth/space-bunny-alpha
production_lines: 17
profile: balanced
role: kid
scaffold_hash: 816b45fb8fe64f51
season: 2
title: Symlinked quorum card converges before its stops write
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-cd8388f0-512d24

## Experiment

Evaluated the inherited post-commit flattening in `rotate.py`: it removed the symlink only after `_write_stops_section` had already written through it, leaving the link target dirty outside the stop commit's pathspec. Moved flattening to a small shared helper and invoked it **before** the stops write; the existing post-commit call is now an idempotent safety call. Added a scratch-project regression that creates a tracked node target and tracked relative quorum symlink, invokes the real `cmd_rotate_self(... --stops ...)` path, and observes the real index porcelain immediately after its sole `_commit_stops_row` call.

Assertions cover all claim conjuncts: rc 0 and committed output; no `dirty tree` text; exactly one stop-commit call; the link target byte-identical; exactly one `THOUGHT:BEGIN` in both source and flattened snapshot; the intended stops text present; porcelain `""` immediately after the stop commit. Negative scope probe: a non-symlink card remains byte-identical through the new helper.

## Evidence

```text
python3 -m pytest extensions/agi/tests/test_rotate.py -q -k symlinked_card_converges_once
1 passed, 328 deselected, 8 warnings in 3.02s

python3 -m pytest extensions/agi/tests/test_rotate.py -q
329 passed, 358 warnings in 60.57s (0:01:00)

git diff --numstat -- extensions/agi/bin/rotate.py
17  2  extensions/agi/bin/rotate.py
```

The first full-file run correctly failed the new assertion because full rotation later creates `sessions/inbox/`; the claim is specifically “clean immediately after,” so the test now snapshots porcelain inside the counting commit wrapper. The focused rerun and complete file rerun pass. The final suite emits pre-existing datetime deprecation warnings only.

## Agent Notes
Flatten quorum symlink before the stops write; real one-call regression proves clean porcelain, one stop commit, and one THOUGHT block.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: the instruction required a real one-call symlink regression, exact thought-count and immediate porcelain assertions, plus a real verdict. The kid node carries concrete focused/full pytest output and evidence_runs, and the implementation flattens before the stops write and syncs the real index. My independent wire probe ran _flatten_card_symlink on a symlink and a plain file: the link became a regular file with identical text, its target stayed byte-identical, and the plain file stayed byte-identical. Near miss: a post-commit-only flatten still allows the stops write through the symlink to dirty its target, which this diff avoids by flattening before the write. Accepted as proved; no deviation.
<!-- THOUGHT:END -->
