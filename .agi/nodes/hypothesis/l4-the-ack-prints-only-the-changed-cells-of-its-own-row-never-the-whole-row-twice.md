---
id: hypothesis:l4-the-ack-prints-only-the-changed-cells-of-its-own-row-never-the-whole-row-twice
mint_id: adfa784c01ad43e1b6d088d399907019
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: d7537ee3616306f6
season: 2
testable_claim: "goal:g15.25 SM.14 (intake: belam XIX 07:23Z, measured at 1d01c87bc: ack prints the whole own-row twice as +/-, ~3k tokens per wake). MEASURED on season2/main @a3bcc3e16: _ack_commit_seats rotate.py:7583-7700 commits the row through a temp index and then reads `git show` of the commit, keeping every line starting with + or - (:7676-7681) — the row is ONE JSON line (posts.md rows :10-26, the belam row ~2.5 kB with key_history), so the output is the full old line and the full new line; the successor needs only which cells moved. CLAIM: (1) _ack_commit_seats parses the one - line and the one + line as JSON (the row shape; a parse failure falls back to today output, say so) and prints `ack: committed own row write (<rel>): <cell>: <old> -> <new>` one line per changed cell, cells sorted, values truncated to 40 chars with `…`, `key_history` summarised as `key_history: N -> M entries`; unchanged cells never printed; (2) a commit that changed no cell prints `ack: committed own row write (<rel>): no cell changed` (or the existing `already` short-circuit — measure which path reaches here); (3) the `git -C <top> push` line unchanged (SL4.03); (4) the SAME cell printer is reused by the spawn row commit (SL5.01) if it prints a diff today — measure; if it does not, leave it. FALSIFIERS: a whole-row line in the output; a changed cell missing; the push line dropped; a JSON parse error surfacing as a traceback. TESTS (test_rotate.py <= 3 on the fixture repo the ack tests already use): a row commit changing session_ref + pid prints exactly two cell lines + the push line and NO line longer than 120 chars; a key_history change prints the N -> M summary; a non-JSON diff falls back to today. FILE SCOPE: rotate.py _ack_commit_seats tail only; test_rotate.py. CEILING: <= 30 lines net, <= 3 tests."
title: "the ack commit output names only the CHANGED cells of the own row (session_ref, session_name, pid, session_id: old -> new) instead of the whole JSON row twice as +/- — ~3k tokens per wake at 1d01c87bc (Prime XIX 07:2xZ)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-ack-prints-only-the-changed-cells-of-its-own-row-never-the-whole-row-twice

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
