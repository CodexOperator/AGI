TARGET: hypothesis:l4-a-harvest-note-cites-only-what-resolves
You are the ONE kid on this target (parent a00-05a1eac0, iter L4.317). Read the
target node in full first: .agi/nodes/hypothesis/l4-a-harvest-note-cites-only-what-resolves.md
Its testable_claim IS your brief. Read it literally.

This is a WORDING ROUND. Nodes only. NO engine bytes. Three defects, each named
by the Prime (mur-45, verbatim, quoted in the target): "(3) L4.313 wording -
harvest note names a test that is not in test_dispatch_dry_run.py at 23d243b7d;
dispatch.py line cites drifted to 1900-1905; experiment title double-quoted."

THE MACHINE AS IT ACTUALLY IS (verify each yourself against file:line at
23d243b7d -- do not trust this brief, it is a pointer, not evidence):

DEFECT 1 -- wrong file attribution in the harvest note.
  File .agi/nodes/hypothesis/l4-a-parent-done-commits-on-every-grammar.md line
  26 says: "test_dispatch_dry_run.py gains
  `test_spawn_env_GIT_CONFIG_VALUE_pinned_to_this_trees_hooks` +
  `test_live_spawn_env_hooks_path_is_this_trees_hooks`".
  The machine: `grep -n 'def test_spawn_env_GIT_CONFIG_VALUE_pinned_to_this_trees_hooks'
  extensions/agi/tests/test_git_commit_guard.py` -> line 507;
  `grep -n 'def test_live_spawn_env_hooks_path_is_this_trees_hooks'
  extensions/agi/tests/test_dispatch_dry_run.py` -> line 405. Both true at
  23d243b7d too. So the first test is in test_git_commit_guard.py, NOT in
  test_dispatch_dry_run.py. Only the second is in test_dispatch_dry_run.py.
  FIX: correct the harvest note so each test is attributed to the file that
  actually holds it at 23d243b7d. Do NOT touch the node's title, testable_claim,
  or the parent's own round note.

DEFECT 2 -- drifted dispatch.py line cites.
  The L4.313 experiment node experiment:a00-0f7849e4-0fbfa8 body cites
  `dispatch.py:1853-1855` (twice: the wiring paragraph and the file:line list).
  The machine: at 23d243b7d `git show 23d243b7d:extensions/agi/bin/dispatch.py`
  has the GIT_CONFIG triple at lines 1903-1905 (1903 COUNT, 1904 KEY_0, 1905
  VALUE_0), inside the `if args.tier in ("kid","parent")` block that starts at
  ~1900. 1853-1855 is stale. The target names the correct window as 1900-1905.
  FIX: correct the cite to the lines that resolve at 23d243b7d (1903-1905, or
  the containing block 1900-1905), and state in the node which commit the cite
  is measured against. Scope note: the target's FILE SCOPE says the experiment
  node is in scope for "title quoting only" -- but the Prime's OWN finding names
  the drifted cite, so correcting it is required, not optional. Say plainly in
  your node's THOUGHT that you widened past the parenthetical for exactly that
  reason (a standing rule was deviated from; name the property of THIS case).

DEFECT 3 -- double-quoted experiment title.
  File .agi/nodes/experiment/a00-0f7849e4-0fbfa8.md: the title field VALUE
  literally contains surrounding double-quote characters. `python3 -c "import
  yaml;print(repr(yaml.safe_load(open('.agi/nodes/experiment/a00-0f7849e4-0fbfa8.md').read().split('---')[1])['title']))"`
  prints `'"Parent done commits on ... GIT_CONFIG triple"'` -- the leading and
  trailing `"` are part of the string, and node_writer then re-escapes them.
  The correct value is the same text WITHOUT the surrounding literal quotes:
  `Parent done commits on season2/loops/* and loop/*@s2, refused on
  season2/main and season2/posts/* -- pinned end-to-end through the dispatch
  GIT_CONFIG triple`. Compare a freshly written node's title (node_writer
  `_scalar`/`_needs_quoting` quotes only when YAML needs it; this value needs
  no quotes and must serialize bare).
  FIX: `write.py experiment:a00-0f7849e4-0fbfa8 'set title <plain value>'`.

DELIVERABLE:
1. Fix defects 1, 2, 3 through the sanctioned writer ONLY (write.py; a hand edit
   is flagged). For the harvest note use `write.py hypothesis:l4-a-parent-done-commits-on-every-grammar 'body_patch -'`
   with a unified diff on stdin, or `read body N:M` + `replace body N:M -`.
   Node body/payload edits: `write.py <id> 'read body N:M'` then
   `write.py <id> 'replace body N:M -'` with the new text on stdin (same ranges,
   replace is the exact inverse of read). The whole verb line is ONE quoted
   argument; chain verbs with && inside the quotes.
2. Keep the corrected note honest: state in one clause what was wrong (a test
   file attribution, a drifted cite, a quoting style) so `grid.py diff` reads as
   a changelog. Do not delete the original claim; correct it.
3. Write your result as your SCAFFOLDED EXPERIMENT node under the target
   (dispatch already created it -- see the SCAFFOLDED NODE FILE line at the end
   of this prompt). Its body must carry: the three original lines, the corrected
   lines, the exact grep/git commands, and the commit the cites are measured
   against. Set verdict honestly in your done call.

EVIDENCE / PROOF (from the target's testable_claim):
  - every test name the harvest note cites appears in
    `grep -n 'def test_' extensions/agi/tests/test_dispatch_dry_run.py` OR in
    the file you re-attribute it to;
  - every dispatch.py:NNNN cite you leave in the touched nodes resolves to the
    mechanism it names at 23d243b7d;
  - the experiment title serializes the way node_writer serializes titles (show
    `write.py` output and re-read the frontmatter);
  - `python3 extensions/agi/bin/links.py links` reads 0 broken;
  - `python3 extensions/agi/bin/links.py schema` shows NO NEW violator (baseline
    is 153 missing across the corpus; do not add one).

FILE SCOPE (nothing else): the HARVEST L4.313 note lines in
.agi/nodes/hypothesis/l4-a-parent-done-commits-on-every-grammar.md (never its
title, testable_claim, or the parent's own round note); the L4.313 experiment
node .agi/nodes/experiment/a00-0f7849e4-0fbfa8.md (its title and its drifted
dispatch.py cites); this target node; and your own scaffolded experiment node.
Never edit dispatch.py or any engine byte. Never touch refs/grid. Never commit.

RESIDUE TO NAME (do not try to fix): the parent node's testable_claim also
carries a stale cite (dispatch.py:1852-1854) but the target's FILE SCOPE forbids
editing testable_claim. Record that as residue in your node with the correct
lines, so a later round can carry it.

If you must escalate use send.py send a00-05a1eac0 <question> then stop.
