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

## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.658 QUEUED (not yet dispatched); round work so far on loop branch season2/loops/hypothesis-thought-verb-edits-on-a00-35b211d9 tip 368e4fe8d.
ROUNDS    this post's rounds on this node: DH.607 DH.639 DH.658; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.

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

## CORRECTIVE DH.583 -- closes mur-director-engine-27 DH.554-k1 accept_with_residue (no verify)
BASE      CUT FROM season2/loops/hypothesis-thought-verb-edits-on-a00-4469ceda tip 5b79c031b (branch de-base-583; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Tree-wide marker guard scans sibling agent worktrees and goes red in the canonical checkout -- extensions/agi/tests/test_thought_hygiene.py:257 -- _SKIP_DIRS omits 'worktrees' while :272 rglobs every *.py under repo_root(root); from /data/work/agi that is 278 real worktrees each holding a test_links_retired_refs.py:191 re-spelling at a rel the allowlist (:249) does not key, so the declared `pytest extensions/agi/tests/ -q` fails on the owner's own tree. One-line fix in the same merge: add 'worktrees' to _SKIP_DIRS (or key the allowlist by basename); until then this is a merge-up blocker for a green canonical suite.
2. Guard exempts the definition by FILE NAME anywhere, so a second definition under another dir is invisible -- extensions/agi/tests/test_thought_hygiene.py:256 -- _DEFINITIONS = {"node_writer.py", Path(__file__).name} combined with `path.name in _DEFINITIONS` at :274 exempts every basename match in the tree; lib/node_writer.py carrying its own marker regex would not be reported, so the falsifier 'no THOUGHT-marker regex literal outside node_writer.py' is enforced by basename, not by path.
3. Single-line marker matcher: a re-spelling split across lines, or built from a variable, escapes the guard -- extensions/agi/tests/test_thought_hygiene.py:240 -- _MARKER_RE requires re.compile/search/match( and the marker on ONE line; `re.compile(\n r"THOUGHT:BEGIN..."\n)` or a pattern held in a constant is not an offender, so the instrument is partial against its own falsifier. The DH.481-class defect it exists for (a single-line unanchored regex) IS caught.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_thought_hygiene.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_thought_hygiene.py · .agi/nodes/experiment/a00-3e57de38-2acdcd.md · .agi/nodes/experiment/a00-4d2f632a-608d9d.md · .agi/nodes/experiment/a00-e7c14870-a5bf8e.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 5b79c031b · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.607 -- closes mur-director-engine-31 DH.583-k1 accept_with_residue (no verify)
BASE      CUT FROM season2/loops/hypothesis-thought-verb-edits-on-a00-138c1736 tip ad54638d4 (branch de-base-607; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. The worktree skip is a post-walk filter, so the canonical row still walks 397 sibling checkouts -- extensions/agi/tests/test_thought_hygiene.py:292 -- `repo.rglob('*.py')` is unconditional; _SKIP_DIRS is applied per file at :294, so the rows are silenced but the cost is untouched: _marker_offenders(/data/work/agi/.agi) hit exit=124 at 600s and a bare rglob capped at 60k .py hit exit=124 at 180s. Prune dirnames in an os.walk walk (or bound the scan root) or the canonical verify inherits a 10+ minute row.
2. Round overran the corrective's HARD CAP of 40 test lines -- extensions/agi/tests/test_thought_hygiene.py:240 -- `git diff --numstat 5b79c031b ad54638d4` = 63 added / 8 deleted (net +55) against the DH.583 order (commit 8875a46b8): '<= 40 test lines ... a byte or kid over it = the round is cut'. 0 production lines and all three items verifiably fixed; the overrun ruling is the Prime's.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_thought_hygiene.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_thought_hygiene.py · .agi/nodes/experiment/a00-3d6addb5-35610c.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over ad54638d4 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.639 -- closes mur-director-engine-35 DH.607-k1 accept_with_residue (no verify)
BASE      CUT FROM season2/loops/hypothesis-thought-verb-edits-on-a00-1c58fd1c tip 0140d122b (branch de-base-639; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. The live guard row is checkout-dependent and only passes post-merge by side selection, not by the fix -- extensions/agi/tests/test_thought_hygiene.py:316 -- Measured on the pre-merge season/s2 tree (/data/work/agi/.agi/worktrees/post-director-engine) the guard reports 5 real offenders (graph2sql.py:127, brief.py:2353, links.py:318, metrics.py:263, snapshot-goals.py:286); it passes at 0140d122b only because those five paths are untouched on the season/s2 side since base 027a215ae, so the branch's clean versions merge in (git merge-tree: no conflict). Any later edit to those files in season/s2 turns this row red and it is not this round's fix that keeps it green.
2. Pasted evidence number 136 canonical .py files is not reproducible on the named root -- .agi/nodes/experiment/a00-a18b675c-1e6a45.md:16 -- The probe (and the parent review's '136 canonical .py files') does not match the committed _SKIP_DIRS: I count 658 .py under the loop worktree and 648 under /data/work/agi on the same walk. The TIME claim does reproduce (0.31-0.32 s warm; 18.2 s cold on the canonical tree), so the cost conclusion stands, but the file count in the evidence is wrong.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_thought_hygiene.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_thought_hygiene.py · .agi/nodes/experiment/a00-3d6addb5-35610c.md · .agi/nodes/experiment/a00-a18b675c-1e6a45.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 0140d122b · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE DH.658 -- closes mur-director-engine-41 DH.639-k1 demote
BASE      CUT FROM season2/loops/hypothesis-thought-verb-edits-on-a00-35b211d9 tip 368e4fe8d (branch de-base-658; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Self-exemption by BASENAME blinds any file named test_thought_hygiene.py (extensions/agi/tests/test_thought_hygiene.py:297)
2. MISSED 1 (the important one, and stronger than what the first reviewer said): the diff's OWN new committed test REQUIRES the defect. 368e4fe8d:extensions/agi/tests/test_thought_hygiene.py:353 plants `tests/test_thought_hygiene.py` into a tmp repo (:349 tmp_path/repo/pkg) that contains no copy of the guard at all, and :360-361 asserts `kept == ["bin/node_writer.py", "bin/reader.py"]` -- i.e. the guard-basename plant IS exempt. So the blindfold is not merely unpinned by the new row (the first reviewer's note); it is asserted as required behaviour by it. Correcting defect 1 will turn this committed row red, so the fix is not a one-liner confined to :297 -- the test at :341-363 has to move with it.
3. MISSED 2: comment/assert mismatch at 368e4fe8d:extensions/agi/tests/test_thought_hygiene.py:362-363. The comment reads '# a node_writer.py under ANOTHER rel is a second definition: still caught' but the assertion is `not _is_exempt(scan / "bin/reader.py", ...)` -- a path that is trivially non-exempt under any shape of the predicate. The node_writer-under-another-rel leg therefore has no assertion of its own; it is covered only incidentally by the `kept` list at :360-361. Wording-level, but it means the second leg is asserted nowhere on its own terms.
4. MISSED 3 (director: the reviewer ran the POST branch head 810da5e44, not the tip; harvest at 368e4fe8d = test_thought_hygiene.py + smoke 95 passed, 6 skipped -- settle at your tip and paste): the round's evidence claim is not reproducible. The node pastes '23 passed in 8.67s' for this file, but I ran the committed test myself (env -u TMUX -u TMUX_PANE, worktree HEAD 810da5e44): `1 failed, 4 passed in 0.24s` -- test_the_real_corpus_has_no_node_with_two_thought_blocks is RED on five nodes (nodes/experiment/a00-4e2fde5f-e3a94d.md count 3, a00-511f142d-fe5190.md 3, a00-591924e2-a79f3c.md 3, a00-5c1c3862-c36247.md 2, a00-74f016df-05930f.md 5). The test exists in the base blob (grep count 2 at 0140d122b) and none of the five nodes is touched by the range, so this is pre-existing and out of file scope -- but the green number is in the round's own IN-SCOPE node. UNVERIFIED whether the row is green at 368e4fe8d itself: that commit is NOT an ancestor of this worktree's HEAD (git merge-base --is-ancestor -> NO) and I did not check it out.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_thought_hygiene.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_thought_hygiene.py · .agi/nodes/experiment/a00-e88afdb8-c7a039.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 368e4fe8d · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE EG.14 -- closes mur-eg-4 DH.658-k1 accept_with_residue (no verify)
BASE      CUT FROM season2/loops/hypothesis-thought-verb-edits-on-a00-d2eb9cf1 tip 6deb61be4 (branch de-base-EG.14; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Sentinel is a one-line literal, so any file can opt out of the guard -- extensions/agi/tests/test_thought_hygiene.py:297 -- _is_exempt exempts any file whose text contains _GUARD_SENTINEL (line 278), so a decoy writing one string plus a real marker pair is exempt again -- the parent probed it as [] and named it as the round's own residue. Not a demote: it is stated on the node, bounded (an unusual literal), and weaker than the basename blindfold it replaces; but no committed row pins it either way.
2. Round overran the DH.658 HARD CAP of 40 test lines (reading: added lines) -- extensions/agi/tests/test_thought_hygiene.py:1 -- 54 added / 36 removed against the order's '<= 40 test lines ... a byte or kid over it = the round is cut'. Every ordered item is verifiably fixed and 0 production lines landed; the ceiling ruling is explicitly the Prime's, and under a net reading (+18) the round is inside.
3. Falsifier 2's append-and-preserve leg has no committed row -- extensions/agi/tests/test_thought_hygiene.py:200 -- The only write._compose_body call site is line 220, driving three live nodes; only the mid-line prose node reaches the append branch (write.py:2813-2814), so 'a body with ONLY a fenced/indented pair -> a top-level block is added and the quote is byte-identical' is true in the bytes and unasserted.
4. (folds in the held EG.11, the EG.7 parent's 'the detector, not the corpus') the corpus test must hold on TODAY's corpus: run your tip's _count_thought_blocks over the 5 nodes AS THEY ARE on the post branch -- `git show cbbaf1e66:.agi/nodes/experiment/<id>.md` for a00-4e2fde5f-e3a94d a00-511f142d-fe5190 a00-591924e2-a79f3c a00-5c1c3862-c36247 a00-74f016df-05930f -- and paste the five counts; each must be <= 1 (every extra marker there is a QUOTATION). A count of 2 = fix the detector, NEVER those nodes (they stay byte-unchanged).
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_thought_hygiene.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_thought_hygiene.py · .agi/nodes/experiment/a00-5437a71f-4e8531.md · .agi/nodes/experiment/a00-e88afdb8-c7a039.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 6deb61be4 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE EG.20 -- closes mur-eg-6 EG.14-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-thought-verb-edits-on-a00-0f334381 tip be28db586 (branch de-base-EG.20; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Two-row opt-out remains — extensions/agi/tests/test_thought_hygiene.py:313 — _is_guard_copy is a conjunction of two writable substrings, so corrective item 1's mechanism is narrowed, not closed; only the one-string case is committed at :408.
2. HARD CAP breach 51/3 test lines against 40 — extensions/agi/tests/test_thought_hygiene.py:1 — the order's own text cuts the round; the ruling is the Prime's and the excess is 11 assertion lines for the two ordered items.
3. SETTLED by the director, NOT a defect: a loop-branch node is never grid-versioned (grid.py commit --all runs only off season2/main, CLAUDE.md "Git grid"); the grid versions it when the trunk lands. No action.
4. STALE COMMENT CONTRADICTING THE FIXED CODE (wording, not mechanism — does not demote). test_thought_hygiene.py:296-301 still reads 'CONTENT identity for the guard: a file carrying this literal IS a guard copy (it carries the exempt rows itself), whatever it is NAMED or wherever it lives' — the exact one-literal rule the round deleted at :333. It is contradicted six lines below by :304-306 and by :333. _GUARD_SENTINEL (:302) now survives only as the self-check assertion at :404, so nothing catches the staleness: :404 still passes. A future round editing the guard from :296 would reintroduce the one-line opt-out this round removed.
5. THE NODE'S SUITE NUMBER IS UNVERIFIED, AND UNVERIFIABLE FROM THIS WORKTREE. The node claims '98 passed, 6 skipped'. The permitted command cannot reproduce it here: this worktree's extensions/agi/tests/test_thought_hygiene.py is a 118-line file from lineage commit 2852e8697, and `git merge-base --is-ancestor HEAD:<file> be28db586:<file>` -> not an ancestor/incomparable, so pytest here would run different bytes entirely. Probe I WOULD run and did NOT run: cd <tree checked out at be28db586> && env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_thought_hygiene.py -q -p no:cacheprovider. I did not run it because the round's blob is not in this worktree and materializing it would be an edit.
6. CHECKED AND NOT FOUND, recorded so the next reviewer does not redo them: (a) the round did NOT fix the gate it passes through — the only 3 removed lines are 2 docstring lines plus the old `return … or _GUARD_SENTINEL in text`, all replaced by the STRICTER `or _is_guard_copy(text)` at :333; no assertion was deleted or relaxed. (b) No real-resource touch: both new rows use tmp_path only, and write._compose_body (be28db586:extensions/agi/bin/write.py:2775) resolves the node through the PASSED root via node_writer.find_node_file(root, edit.node_id), never locations.find_project_root, so the append test cannot reach the live graph; the pre-existing row at :244 already drives the same seam. (c) The append test at :195 exercises the real production branch (write.py:2813-2814, `spliced if spliced is not None else body.rstrip() + '\n\n' + block + '\n'`) rather than re-implementing it.
7. NEAR-MISS I HIT AND DISCARDED — reported so the corpus count is not re-litigated. My first corpus count flagged a00-4e2fde5f-e3a94d as a 2-block OFFENDER in both the worktree and the canonical checkout, which would have made test_the_real_corpus_has_no_node_with_two_thought_blocks RED and the node's item-4 paste false. Under the test's EXACT rule (_BEGIN_RE = r'^<!--\s*THOUGHT:BEGIN', node_writer.py:919 — column 0, plus _closed_fences) the indented quoted pair at lines 95/97 does not match, the count is 1, the node's 1/1/0/1/0 paste is exactly right, and a full scan gives 0 offenders across 4749 canonical and 4753 worktree nodes. My counter was wrong, not the round.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_thought_hygiene.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_thought_hygiene.py · .agi/nodes/experiment/a00-6b4afc29-a3d6c6.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over be28db586 · <= 40 test lines net over be28db586 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat be28db586 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.20: mur-eg-6 EG.14-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
