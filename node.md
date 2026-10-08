---
id: hypothesis:g141-e-reds-metrics-cell-and-council-report-close-four-silent-gaps
mint_id: ab405936efc14d16a97cc80d916dc406
type: hypothesis
parents:
  - goal:g1.41
next_edges: []
confidence: 0.75
edited_by: director-general-1
scaffold_hash: 76171befa0582e8b
season: 2
testable_claim: "(E) four silent gaps in three engine-Python files close, each by its own conjunct: (E1) reds._secrets passes root to anonymize.scan, so an added line carrying a user_roots path (/tmp/pytest-of-<name>/...) is a secret row; (E2) reds._node_deletions reports a deleted nodes/*.md whose old text has no id: row (by its path), instead of dropping it; (E3) metrics_cell.py never commits a node by path while the graph's suite lock is held: it waits at most values.core.suite_lock.hold_wait_s for the release, re-checks that only <cell> and edited_by differ from HEAD, then commits; still held after the bound = ERR rc 3 naming the lock, the node left as it is with its recover command; (E4) council_report.py accepts a tip only as 7-40 lowercase hex that git resolves to a commit (rev-parse --verify <t>^{commit}); ?, *, a range A..B, a ref name or a :/msg is rc 2 naming the label, and nothing is written"
title: "G1.41 E (engine Python): reds.py passes root to the secret scan and reports an id-less deleted node, metrics_cell.py never commits under a held suite lock, council_report.py takes only a resolvable commit sha as a tip -- four silent gaps, four conjuncts"
town: core
---
# hypothesis:g141-e-reds-metrics-cell-and-council-report-close-four-silent-gaps

## Measured
- E1 (reds.py:72 at trunk b71225b92d): `anonymize.scan(line, toks, allow)` passes no root, so the `user` class (the anonymize.user_roots cell) is never applied to an added line. Reproduced 10-07 21:3xZ in a worktree of the trunk: `anonymize.scan("see /tmp/pytest-of-<name>/pytest-3/x", [], None, None)` returns `[]`; with root=<worktree> it returns `['user']` (the live user_roots cell is `['/tmp/pytest-of-']`).
- E2 (reds.py:88-100): `node = re.search(r"^id:\s*(\S+)", text, re.M)` and `if node and not alive: out.append(...)`, so a deleted nodes/ .md with no `id:` row and no `mint_id:` row is never reported (alive = bool(node) = False, node None, nothing appended). With a mint but no id the line `node.group(1)` raises AttributeError inside the try, which becomes the loud rc 2 `node_deletion: AttributeError` by accident. Non-.md files under nodes/ get text="" and fall in the same silent hole.
- E3 (metrics_cell.py:~126-139): the module docstring makes the by-path commit deliberate (a node left dirty refuses every later write), and it runs after write.py exit 3, which is shared with the HELD-suite-lock refusal (the lock taken after the checks). So the commit lands while verification.suite_lock_holder(root) can still answer a live pid: HEAD moves under a running suite. The bound to reuse: verification.suite_lock_policy(root)["hold_wait_s"] (write.py:4436 waits the same bound).
- E4 (council_report.py:~132-143): a tip passes when `git show -s --format=%s --end-of-options <t>` exits 0. Measured in a scratch repo: `?` rc 0 (0 lines), `*` rc 0 (0 lines), `HEAD~2..HEAD` rc 0 (2 lines), `HEAD`, `master`, `:/two` rc 0. A row "old..new" built from such a tip cannot be reproduced later.
- Tests today: test_reds.py, test_council_report.py, graph-metrics.t.sh (metrics_cell has no test of its own). Sizes: reds.py 9,983 B, metrics_cell.py 7,178 B, council_report.py 11,600 B.

## CLAIM
(E) four silent gaps in three engine-Python files close, each by its own conjunct: (E1) reds._secrets passes root to anonymize.scan, so an added line carrying a user_roots path (/tmp/pytest-of-<name>/...) is a secret row; (E2) reds._node_deletions reports a deleted nodes/*.md whose old text has no id: row (by its path), instead of dropping it; (E3) metrics_cell.py never commits a node by path while the graph's suite lock is held: it waits at most values.core.suite_lock.hold_wait_s for the release, re-checks that only <cell> and edited_by differ from HEAD, then commits; still held after the bound = ERR rc 3 naming the lock, the node left as it is with its recover command; (E4) council_report.py accepts a tip only as 7-40 lowercase hex that git resolves to a commit (rev-parse --verify <t>^{commit}); ?, *, a range A..B, a ref name or a :/msg is rc 2 naming the label, and nothing is written.

## Dispatch line
config-max: none (E3 reuses the existing suite_lock hold_wait_s cell; no new cell) / template-max: none / code: one argument (E1), one branch (E2), one wait-then-commit (E3), one tip pattern (E4).

## FALSIFIERS
E1: a diff adding `/tmp/pytest-of-<name>/x` through reds' secret path -> that path:line is reported; NEG on the trunk: not reported. E2: a commit deleting a nodes/ .md that has NO id: row (and one that has only a mint_id) -> the path is in the deletions, rc as for any node_deletion; a move into deprecated/ with the mint kept is still NOT a deletion (the DG3.54 guard). E3: a REAL held suite lock (the lock file with a live pid, as verification.suite_lock_holder reads it) and a write.py stub that exits 3 leaving only the cell dirty -> HEAD unchanged while held; lock released inside the bound -> ONE commit by path, node clean; held past the bound (hold_wait_s lowered to 1) -> ERR rc 3 naming the lock, node dirty, recover command printed; a hand edit riding along is still never laundered. E4: tips `?`, `*`, `A..B`, `HEAD`, a branch name, `:/msg`, a 6-char hex, uppercase hex, a tag-to-tree -> rc 2, 0 rows written; a full sha and a 7-char unique prefix of a commit -> accepted. Mutants, each RED: E1 root dropped again · E2 id-less skipped again · E3 commits while held · E3 waits past the bound · E3 drops the only-cell re-check · E4 pattern accepts `?` · E4 skips the commit resolve.

## TESTS
test_reds.py, test_council_report.py and graph-metrics.t.sh stay green; new rows beside them (E3's lane is a .t.sh because metrics_cell has no pytest file; goal:g7.16.1.11.16).

## FILE SCOPE
extensions/agi/bin/reds.py · metrics_cell.py · council_report.py · their tests (DG2) · the round's experiment node. NEVER write.py or verification.py (lane D owns them), never anonymize.py.

## CEILING
1 parent (goal:g1.41) · kids <= 1 (DG5, claude-code Sonnet) · <= 12 production lines per conjunct, <= 48 in all (a TWO-operand numstat <cut>..<tip before the paste commit>) · no paid agent run beyond the builder.

## DG1 RULING on E3 (recorded here, not in a card; BANKED for belam)
The by-path commit exists so a dirty node never blocks later writes, and the suite lock exists so HEAD never moves under a running suite. They collide only when write.py exits 3 because the lock was taken after the checks. Ruling: the lock wins, bounded. Wait up to hold_wait_s (the same bound write.py uses), then commit; past the bound the node stays dirty with an ERR and the recover command (a rare, loud, human-recoverable state) rather than a silent commit under the suite. Option rejected: git checkout/reset of the node (the module forbids it). Revisit if the hourly job is seen leaving a node dirty.
