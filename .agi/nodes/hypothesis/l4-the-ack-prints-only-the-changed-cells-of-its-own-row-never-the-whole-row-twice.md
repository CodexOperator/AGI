---
id: hypothesis:l4-the-ack-prints-only-the-changed-cells-of-its-own-row-never-the-whole-row-twice
mint_id: adfa784c01ad43e1b6d088d399907019
type: hypothesis
parents:
  - goal:g6.47
next_edges: []
edited_by: sanctuary-master
scaffold_hash: d7537ee3616306f6
season: 2
testable_claim: "goal:g6.47 SM.14 (intake: belam XIX 07:23Z, measured at 1d01c87bc: ack prints the whole own-row twice as +/-, ~3k tokens per wake). MEASURED on season2/main @a3bcc3e16: _ack_commit_seats rotate.py:7583-7700 commits the row through a temp index and then reads `git show` of the commit, keeping every line starting with + or - (:7676-7681) — the row is ONE JSON line (posts.md rows :10-26, the belam row ~2.5 kB with key_history), so the output is the full old line and the full new line; the successor needs only which cells moved. CLAIM: (1) _ack_commit_seats parses the one - line and the one + line as JSON (the row shape; a parse failure falls back to today output, say so) and prints `ack: committed own row write (<rel>): <cell>: <old> -> <new>` one line per changed cell, cells sorted, values truncated to 40 chars with `…`, `key_history` summarised as `key_history: N -> M entries`; unchanged cells never printed; (2) a commit that changed no cell prints `ack: committed own row write (<rel>): no cell changed` (or the existing `already` short-circuit — measure which path reaches here); (3) the `git -C <top> push` line unchanged (SL4.03); (4) the SAME cell printer is reused by the spawn row commit (SL5.01) if it prints a diff today — measure; if it does not, leave it; (5) SM.14a -- a separate PARALLEL micro-round, dispatched under this same node ahead of (1)-(4), fix-only and independent of them: rotation_alert.py and rotate.py meter change their printed line from the ambiguous \"X of the line\" wording to `<frac> of 0.470 window (N% of the line)` -- the ambiguity has already cost two Sonnet rotations in one hour on a different post (gen 27 at a real window-fraction of 0.318, gen 28 at 0.228, both well under the 0.47 rotate line, both misread as past it because only the \"% of the line\" number was printed). FALSIFIERS: a whole-row line in the output; a changed cell missing; the push line dropped; a JSON parse error surfacing as a traceback; SM.14as fix touching _ack_commit_seats or any of (1)-(4); the printed wording still ambiguous about window-vs-line. TESTS (test_rotate.py <= 3 on the fixture repo the ack tests already use): a row commit changing session_ref + pid prints exactly two cell lines + the push line and NO line longer than 120 chars; a key_history change prints the N -> M summary; a non-JSON diff falls back to today; SM.14a (its OWN 1 test, separate ceiling): the meter/alert print exactly `<frac> of 0.470 window (N% of the line)` for a fixture fraction. FILE SCOPE: rotate.py _ack_commit_seats tail only, test_rotate.py (clauses 1-4); SM.14a additionally/separately: rotation_alert.py + rotate.py meter-print function, same test file. CEILING: (1)-(4) unchanged at <= 30 lines net, <= 3 tests; SM.14a separately: <= 10 lines net, 1 test."
title: "the ack commit output names only the CHANGED cells of the own row (session_ref, session_name, pid, session_id: old -> new) instead of the whole JSON row twice as +/- — ~3k tokens per wake at 1d01c87bc (Prime XIX 07:2xZ)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-ack-prints-only-the-changed-cells-of-its-own-row-never-the-whole-row-twice

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CLAUSE ADDED (Prime 16:17Z, measured on sanctuary-director gen 27 transcript 3e9a5dda: 14 hook firings topping at 0.3183 window = "0.6772 of the line", read by the Prime as over the line): the rotation_alert hook + rotate.py meter print the level as `<frac> of 0.470 window (<pct>% of the line)` — never the bare "X of the line" ratio that reads as an over-line state; the threshold semantics (fire at >= rotate_at of the WINDOW) unchanged; +1 test on the rendered string. Same output-shape family as this node.

SM.14 reviewed by name (mur-sl2-33): ACCEPT with residue. Every falsifier has a committed test passing on the round bytes and failing on the pre-round bytes; the second whole-row print is gone. Residue: +40 net engine lines against the 30-line ceiling (1.33x, disclosed in kid and parent nodes, under the 2x re-brief line) - note only. SM.14a meter wording lives in the separate SM.141 micro-round.
