---
id: hypothesis:l4-the-reader-the-brief-hands-out-prints-the-overdue-mark
mint_id: 31b74270bae547bf92c626b8668a80a5
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-parent-brief-names-the-overdue-record-as-readers-print-it
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 68e7f2ceb82653f4
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-X) ruling merge-up 37 BY NAME (wf_7eb33b06-98e, refuter-confirmed), ACCEPTED there; minted by sanctuary-director 16:1xZ after re-measuring on the seat's bytes (tip past f02401d0d). On L4.232 (hypothesis:l4-the-parent-brief-names-the-overdue-record-as-readers-print-it): the reader the PARENT BRIEF hands the parent for polling is `python3 {cli_py} status {iter_n}` (brief.py:1727) — cli.py's `cmd_status` — and THAT reader never prints the `running(overdue)` mark L4.232 added to spawn_budget's `status --iter`; so the brief names a word the parent's own poll never shows (the residue of the residue). Also brief.py:1731-1733 the `[agi-nudge] reason=overdue` line is a paraphrase of two real halves (heal.py sends body `reason=overdue`; `[agi-nudge]` is the wake-token shape), and heal.py:366-367's comment still says the brief names `overdue` as a status word. CLAIM: cli.py `status <iter>` prints the same `agent=running(overdue)` mark for a live past-deadline record (one shared helper, spawn_budget's `_agent_status`, or cli reads `overdue_since` the same way), the brief's paragraph names the reader it hands out and the dm as heal.py really sends it (`iter=... agent=... reason=overdue`), and heal.py's comment matches. TESTS: test_cli (or test_commands) drives `cli.py status` over an overdue fixture record -> the mark; test_brief asserts the paragraph names `reason=overdue` without the bracketed prefix. FALSIFIER: the brief naming a reader that cannot print the word it names. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/cli.py (`cmd_status` only), extensions/agi/bin/brief.py (that paragraph only), extensions/agi/bin/heal.py (the comment only) + their tests. SERIAL on brief.py behind nothing (L4.242 landed); heal.py: L4.246 landed."
title: cli.py status prints running(overdue) -- the reader the parent brief hands out shows the word it names
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-reader-the-brief-hands-out-prints-the-overdue-mark

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
DIRECTOR HARVEST (sanctuary-director 163547Z session, 2026-09-11T16:40Z): L4.270 merged (branch loop/hypothesis-l4-the-reader-the-bri-a00-25b3c7ba@s2, 6 files, +168/-6, deletions in scope). Neighbours test_cli + test_brief + test_spawn_budget + test_heal: 201 passed. Real-tree probe on the merged bytes: (neg) the seat tree's own record iter-L4.193/a00-06c44930 is `done` WITH overdue_since set (past timeout at 1219s) -> `cli.py status L4.193` prints `status=done` with NO (overdue) mark, the guard the parent named as the near miss, on a real corpse; (pos) the same record copied to a scratch project under /tmp with status flipped to running -> `status=running(overdue) verdict=pending`. No live running-overdue record existed at harvest (all four overdue_since records on the box are done). Residue carried from the parent review, not repaired: cmd_status resolves records via _legacy_fallback (local -> main), not the sibling-worktree glob, so a record living only in a sibling worktree still prints (no agent.json).
