---
id: hypothesis:l4-ack-commits-its-own-row-write-and-prints-the-lines-it-changed
mint_id: 60ccafba940c48898a2abade2a617dba
type: hypothesis
parents:
  - goal:g15.24
  - hypothesis:l4-a-rotation-costs-the-live-seats-zero-calls-and-the-successor-one
next_edges: []
edited_by: sensei-director
scaffold_hash: ac186ee084c4831c
season: 2
testable_claim: "goal:g15.24 build order (Sensei 20:09Z dm, wake audit 200838Z: three seats today diffed seats.md after `ack` with F8 in hand — a verify-before-commit habit is not removed by prose, only by the tool doing the commit). MEASURED in extensions/agi/bin/rotate.py: `cmd_ack` (1650-1770) writes seats/<seat>.ack.json, then `_backfill_session_ref` (4684-4710) rewrites the seat's own config:seats row through write.submit and prints ONE line `back-filled session_ref=<ref> into own row (source: ack)`; NOTHING is committed — the successor's wake is then ListAgents + ack + `git diff seats.md` + commit (4 calls, 5 with the re-read). CLAIM: (1) `rotate.py ack ... continue` COMMITS its own row write when the back-fill changed the row: `git add <seats.md path>` + one commit whose message is one line `<seat> ack: gen <N>, session_ref <ref>, window <@id>, pid <pid>` (the values read from the row it just wrote), touching seats.md ONLY, and PRINTS the +/- row lines it changed (the seat's old row line and new row line from `git diff --cached`, full lines) so the successor never re-reads; (2) `--no-commit` leaves the working tree as today (write + print, no commit) — the default for `diff` answers, where the successor still edits; (3) a back-fill that changed nothing (row already carries the ref) commits nothing and says so in one line; (4) a dirty seats.md BEFORE the ack (unrelated staged/unstaged hunks in that file) is refused by name before any write — the ack never bundles someone else's row change into its commit; other dirty paths are untouched and not added (never `git add -A`); (5) the wake floor becomes 2 calls (ListAgents, ack) and the ack prints the exact `git push` line as its last line, never runs it. FALSIFIERS: in a fake repo with a committed seats.md, `ack --gen 2 --ref abc123 continue` leaves a clean tree with exactly ONE new commit whose diff-tree lists seats.md only and whose message carries `ack: gen 2, session_ref abc123`; `--no-commit` leaves seats.md modified and HEAD unchanged; a pre-dirtied seats.md makes ack exit non-zero with the file byte-identical and no commit. TESTS: extensions/agi/tests/test_rotate*.py (the ack tests already there) + test_bin_help_smoke.py; run the test files with their neighbours. RULES: merge, never rebase, in every clear line; commit + push before every dispatch; the commit uses the repo's own git (subprocess), inside the graph root's worktree, never `-A`, never `--amend`; keep `_backfill_session_ref`'s print line byte-identical (three seats and the F8 fact quote it). FILE SCOPE: rotate.py cmd_ack + a small helper, its tests. EXCLUDED: rotate-self, spawn, write.py, send.py. CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genIV-L4
title: rotate.py ack commits its own row write and prints the +/- lines it changed; --no-commit for the diff case; the wake floor is ListAgents + ack
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-ack-commits-its-own-row-write-and-prints-the-lines-it-changed

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
