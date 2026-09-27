---
id: hypothesis:thought-verb-edits-only-the-top-level-thought-block
mint_id: cf528b57953144b7b05a61db21c5b693
type: hypothesis
parents:
  - goal:g1
next_edges: []
confidence: 0.8
edited_by: director-engine
scaffold_hash: e1607a9463d280b3
season: 2
tags:
  - engine
  - write
  - thought
testable_claim: "(1) a THOUGHT block is the authored region only when its BEGIN marker starts a line at column 0 outside an indented or fenced quote (2) write.py thought rewrites only that block and adds one when none exists, never touching a quoted pair (3) snapshot-goals.py and metrics.py read the same one definition (assigned: director-engine)"
title: "write.py thought edits only the top-level THOUGHT block -- never a pair quoted inside a review (DH.481 destroyed quoted evidence; assigned: director-engine)"
town: core
---
# hypothesis:thought-verb-edits-only-the-top-level-thought-block

# hypothesis:thought-verb-edits-only-the-top-level-thought-block

## Measured
- `node_writer._THOUGHT_RE` (extensions/agi/bin/node_writer.py:918) is `<!--\s*THOUGHT:BEGIN.*?<!--\s*THOUGHT:END\s*-->` with DOTALL and NO line anchor; `extract_thought` (:922) returns the FIRST match anywhere in the body, and `write.py` `verb_thought` (:291) / the submit path (:2807) rewrite that match.
- mur-director-engine-13 DH.481-k1 (DEMOTE): a `write.py ... thought` on experiment:a00-4e2fde5f-e3a94d matched a THOUGHT pair QUOTED with 4-space indentation inside its DH.467 PARENT REVIEW and replaced it, destroying the quoted evidence; the only remaining pair now sits inside the review, so every later `thought` edit overwrites review prose again (self-perpetuating).
- The comment at :915-917 says the spelling is shared with `snapshot-goals.py` and `metrics.py` -- "one spelling, three readers".

## CLAIM
(1) a THOUGHT block counts as the node's authored region only when its BEGIN marker starts a line at column 0 and sits outside any indented or fenced quote; (2) `write.py <id> thought ...` rewrites that block only, never an indented/quoted pair, and adds a top-level block when none exists; (3) snapshot-goals.py and metrics.py read the same ONE definition (no second regex).

## Dispatch line
config-max: none (a marker spelling is code shared by readers, not a tunable). template-max: none. code: the anchored single definition + the three readers routed through it -- the resolver that does not exist.

## FALSIFIERS
- A body with a quoted, indented THOUGHT pair inside a review AND a top-level block: a `thought` edit changes the quoted pair.
- A body with ONLY a quoted pair: `extract_thought` returns it (it must return None, and `thought` must ADD a top-level block, leaving the quote byte-identical).
- grep finds a THOUGHT-marker regex literal outside node_writer.py after the round.

## TESTS
extensions/agi/tests/test_thought_hygiene.py (+ rows for the three falsifiers above, on tmp_path nodes only). Neighbourhood: test_write*.py test_node_writer*.py test_snapshot_goals*.py test_metrics*.py.

## FILE SCOPE
extensions/agi/bin/node_writer.py · extensions/agi/bin/write.py · extensions/agi/bin/snapshot-goals.py · extensions/agi/bin/metrics.py · extensions/agi/tests/test_thought_hygiene.py

## CEILING
1 kid · <= 15 production lines · pi-free tier-0 · 0 USD. No test writes the live graph.

## CORRECTIVE DH.522 -- closes mur-director-engine-17 DH.500-k1 (verify: DEMOTE)
BASE      CUT FROM season2/loops/hypothesis-thought-verb-edits-on-a00-616b9d6c tip dffe6de60 (worktree de-m500). No merge. Never rebase.
FIRST ACT template-max: ONE THOUGHT-marker definition lives in node_writer.py; every other reader CALLS it.
1. node_writer.py:918-919 _THOUGHT_RE (old unanchored DOTALL regex) has zero references -> delete it.
2. links.py:318 (re.search THOUGHT:BEGIN(.*?)THOUGHT:END) and :344 (bare substring test) read a quoted pair as a region -> call node_writer's fence-aware span.
3. .agi/context/local-maxxing/sql/graph2sql.py:127 carries a third unanchored copy -> the same call (or a one-line import of node_writer's extractor).
4. Restore the dropped falsifier-3 test test_no_thought_marker_regex_outside_node_writer (a00-5abd0370-fbda2f.md:57,70): it greps bin/ + that sql file for a THOUGHT-marker regex outside node_writer.py; its allowlist names only write.py:2807 and brief.py:2048 if they stay, each with a one-line reason in the test.
5. The round's own new nodes carrying a raw marker (a00-4d2f632a-608d9d.md:171 and the rest the corpus gate names at base) -> escape the quoted marker with write.py so the corpus gate passes under the BASE definition too.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_thought_hygiene.py + test_links*.py + test_bin_help_smoke.py once (timeout 600, --basetemp under /tmp)
FILE SCOPE extensions/agi/bin/node_writer.py · extensions/agi/bin/links.py (the THOUGHT readers only) · .agi/context/local-maxxing/sql/graph2sql.py (:127 only) · extensions/agi/tests/test_thought_hygiene.py · the round's own experiment nodes (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · net <= 10 production lines (deletions pay) · <= 50 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

## CORRECTIVE DH.554 -- closes mur-director-engine-23 DH.522-k1 demote
BASE      CUT FROM season2/loops/hypothesis-thought-verb-edits-on-a00-ba767330 tip 5c88edf53 (branch de-base-554; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Falsifier's sql-mirror leg is dead: _project_root() returns the .agi GRAPH dir, so root / Path('.agi/context/local-maxxing/sql/graph2sql.py') never exists and :256 skips it
2. The falsifier's SURFACE is narrower than the falsifier it claims to discharge: :253 scans bin/*.py plus one mirror and never tests/, lib/, scripts/, hooks/ or any other .agi/context mirror, while the hypothesis words falsifier-3 as 'a THOUGHT-marker regex literal outside node_writer.py' with no surface limit. A live re-spelling exists just outside the scanned surface: extensions/agi/tests/test_links_retired_refs.py:191 (`_re.search(r'THOUGHT:BEGIN(.*?)THOUGHT:END', body, _re.S)`, run against live goal nodes). It is pre-existing, unchanged by this diff, and benign (a fixture builder) -- but it shows the guard's reach is bin/+1, not the tree.
3. The dead leg and the config_max violation are the SAME line: test_thought_hygiene.py:241 re-hardcodes the graph-dir name and a town-relative path as a literal where the file's own idiom (:70 `root / 'nodes'`) derives them from `locations`. Fixing it as a derived path (locations.repo_root(root) / 'context/local-maxxing/sql/graph2sql.py') discharges the demote AND the config violation at once; a `paths.local_maxxing` cell would be worse (that namespace is town-script scoped and has no such key today -- 43 cells, none for sql).
4. graph2sql.py:31 uses `sys.path.append`, which is LAST-wins: a node_writer already importable in the process (e.g. inserted at position 0 by .agi/context/conftest.py:26) silently wins over the one this line intends, so the mirror could keep serving a foreign definition. Verified harmless in this tree (both resolve to the same file); `insert(0, ...)` or a guarded import would make the intent binding.
5. The node's own falsifier paragraph (a00-e7c14870-a5bf8e.md:88) reports a measurement the restored test cannot make in this layout. The underlying CLAIM is nonetheless true and I verified it independently: `git grep` over every .py at 5c88edf5 finds the marker regex only at node_writer.py:919-920; all six readers route through the definition (links.py:318/:344 -> extract_thought/_thought_span, graph2sql.py:130 -> thought_text, snapshot-goals.py:288 -> node_writer); links.py neighbourhood test_links_retired_refs.py 11 passed; graph2sql read_node runs over live nodes; test_thought_hygiene.py 16 passed. So the defect is in the ordered instrument, not in the shipped behaviour -- which is why the fix is one line rather than a re-do.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_thought_hygiene.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/links.py · extensions/agi/bin/node_writer.py · extensions/agi/tests/test_thought_hygiene.py · .agi/nodes/experiment/a00-e7c14870-a5bf8e.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 5c88edf53 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.554: mur-director-engine-23 DH.522-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
