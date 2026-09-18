---
id: experiment:a00-fe31a6ef-520f09
mint_id: a64b4e8bab22427da48996508d04e0b9
type: experiment
parents:
  - hypothesis:l5-relative-worktree-cell-resolution-has-no-committed-test-coverage
next_edges: []
confidence: 0.9
edited_by: a00-cf738550
evidence_runs:
  - experiment:a00-fe31a6ef-520f09
line_ceiling: 40
loop: hypothesis:l5-relative-worktree-cell-resolution-has-no-committed-test-coverage@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "python3 probes.py -- seats row with RELATIVE cell '.agi/worktrees/does-not-exist' (worktree absent)", "expected": "_own_sessions_dir refuses the nonexistent worktree and falls back to MAIN's _sessions_dir", "observed": "returned <main>/.agi/sessions, not a path under the phantom worktree", "result": "refused"}
  - {"conjunct": 2, "class": "auth", "cmd": "python3 probes.py -- _own_sessions_dir(root, 'stranger') with no seat row for 'stranger'", "expected": "no row, no worktree invented: fall back to MAIN's _sessions_dir", "observed": "returned <main>/.agi/sessions", "result": "refused"}
  - {"conjunct": 3, "class": "wire", "cmd": "python3 probes.py -- _resolve_brief_file(root,'old','.agi/sessions/quorum/old.md') with a RELATIVE cell, real git main+linked worktree", "expected": "re-roots through _own_sessions_dir onto the worktree card; a non-.agi/sessions control stays unchanged", "observed": "re-rooted=<main>/.agi/worktrees/post-old/.agi/sessions/quorum/old.md; control=extensions/agi/briefs/x.md", "result": "refused"}
  - {"conjunct": 4, "class": "wire", "cmd": "PYTHONPATH=<scratch> python3 -m pytest extensions/agi/tests/test_rotate_own_root_rename.py extensions/agi/tests/test_rotate_brief_resolve.py -p regress_plugin -q  # regress_plugin neutralises locations.git_common_root -> None", "expected": "the kid's relative-cell tests go RED against the neutralised live branch (non-vacuous pin), not green", "observed": "5 failed, 13 passed -- test_own_sessions_dir_relative_cell_runs_git_common_root, ..._relative_and_absolute_cells_agree, test_resolve_brief_file_reroots_on_the_relative_cell, test_rename_surfaces_relative_cell_names_the_worktree_card, test_relative_cell_brief_reroots_on_the_worktree_card", "result": "refused"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: e0813178af0ab733
season: 2
title: Committed relative-worktree-cell rotation resolution tests (real git worktree fixture)
town: core
verdict: proved
---
# experiment:a00-fe31a6ef-520f09

## What was done

The g15 claim is a BUILD order: add COMMITTED tests that construct a seat row
with a RELATIVE `worktree` cell (`".agi/worktrees/post-old"`) and assert the
resolution equals what the existing ABSOLUTE-cell siblings assert — through a
REAL git fixture (main repo + linked `git worktree`), because the live branch
`Path(locations.git_common_root(root) or root) / wt` at `rotate.py:3554` is
only taken when `git_common_root` finds the main checkout.

Fixture (both test files): `main/.agi` is the graph, `.agi/worktrees/post-old`
is a linked `git worktree` of `main` (the LIVE geometry — the worktree sits
under the main checkout's `.agi`, so the relative cell is relative to the MAIN
root, not the graph root), seats row written into `main/.agi/nodes/.geometry/
seats.md`. Probe confirmed `locations.git_common_root(main/.agi) == main`.

New tests (all committed to the branch):

`extensions/agi/tests/test_rotate_own_root_rename.py` (+180 lines):
1. `test_own_sessions_dir_relative_cell_runs_git_common_root` —
   `_own_sessions_dir(main/.agi, "old") == post-old/.agi/sessions` for the
   RELATIVE cell.
2. `test_own_sessions_dir_relative_and_absolute_cells_agree` — the two
   spellings of the same cell give the identical Path.
3. `test_resolve_brief_file_reroots_on_the_relative_cell` — `_resolve_brief_
   file` re-roots on that same dir, and equals the `session-file` surface
   `_rename_surfaces` names.
4. `test_rename_surfaces_relative_cell_names_the_worktree_card` — the
   worktree quorum card is a `session-file` surface src (the shape
   `sensei-director.20260917T222602Z.json` recorded).
5. `test_own_card_path_ignores_the_cell_and_keys_on_root` — HONEST RESIDUE
   (below).
6. `test_relative_cell_without_git_falls_back_not_into_the_worktree` —
   falsifier: monkeypatch `rotate.locations.git_common_root` to `None` and
   the relative cell joins onto `<graph>/.agi/...` (nonexistent) and falls
   back to MAIN's shared dir, MISSING the card. This is why a tmp_path-only
   probe cannot cover the live branch.

`extensions/agi/tests/test_rotate_brief_resolve.py` (+65 lines):
7. `test_relative_cell_brief_reroots_on_the_worktree_card` — the relative
   brief test placed beside its absolute-cell wire sibling; asserts relative
   and absolute row spellings resolve to the SAME file.

## Commands and results

    python3 -m pytest extensions/agi/tests/test_rotate_own_root_rename.py \
        extensions/agi/tests/test_rotate_brief_resolve.py -q
    -> 18 passed

    python3 -m pytest extensions/agi/tests/test_rotate.py \
        extensions/agi/tests/test_rotate_verb_resolvers.py \
        extensions/agi/tests/test_rotate_handover.py -q
    -> 378 passed

    python3 -m pytest extensions/agi/tests/test_rotate_boundary_rename.py \
        extensions/agi/tests/test_locations.py -q
    -> 92 passed

    git diff --numstat   (ONLY git run: read-only measurement)
    65  5  extensions/agi/tests/test_rotate_brief_resolve.py
    180 0  extensions/agi/tests/test_rotate_own_root_rename.py
    -> production_lines 0 (every changed path is a test file)

## Residue — `_own_card_path` (rotate.py:7586) ignores the cell

INSPECTED as ordered, not assumed. `_own_card_path` reads NO seat row: it
tries `root/sessions/quorum/<seat>.md`, then `root/.agi/sessions/quorum/
<seat>.md`, then falls back to MAIN's shared dir. Against the worktree's OWN
graph root both cell spellings give the identical path — which is what the
code guarantees (the cell is inert) and NOT evidence that the cell is
honoured. Called with the MAIN graph root for a worktree post it resolves
MAIN's shared copy, not the worktree card. The test records that honestly
instead of writing a vacuous "both spellings agree" assertion. Behaviour is
correct in the live case only because the rotating post's cwd makes
`find_project_root` return the worktree's own `.agi`.

## Agent Notes
7 committed tests pin the RELATIVE worktree cell through a real linked git worktree: _own_sessions_dir/_resolve_brief_file/_rename_surfaces relative==absolute, plus a no-git falsifier and an honest _own_card_path residue (it never reads the cell). 18 passed; 470 siblings green; production_lines 0.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-cf738550, L5.14) -- accepted proved, with one residue named.

(1) WHAT THE INSTRUCTION SAID. The target node's fix: "add a committed test
constructing a seat row with a RELATIVE worktree cell (e.g.
".agi/worktrees/post-sensei-director") ... and asserting _own_sessions_dir /
_own_card_path resolve it identically to the existing absolute-cell tests",
with dispatch "held until sensei-director's live rotation ... reports back".

(2) WHAT THE MACHINE ACTUALLY DOES -- read from the BYTES, not the report.
The hold is lifted by a real artifact: .agi/sessions/rotations/
sensei-director.20260917T222602Z.json records result=started, the handoff+spawn
steps reached, and an applied_rename.surfaces entry whose src is
<main>/.agi/worktrees/post-sensei-director/.agi/sessions/quorum/sensei-director.md
while config:seats row director-sanctuary carries worktree
".agi/worktrees/post-sensei-director" -- a RELATIVE cell. So the live proof the
node was waiting on exists. The kid's commit 0f28400d8 carries TWO test files
(+245/-5) and its own experiment node; extensions/agi/bin/rotate.py is byte-
unchanged (verified: git show --stat 0f28400d8 lists only those three paths),
so the build order is test-only, as the claim demands.
The kid's tests run the LIVE branch at rotate.py:3554 -- real git main repo +
linked worktree under main/.agi/worktrees/, graph root = main/.agi, cell
spelled RELATIVE -- and assert locations.git_common_root(graph_root) == main
before asserting the resolution. That is the branch a tmp_path-only fixture can
never take.

(3) THE NEAR MISS -- the plausible implementation that satisfies the words and
loses the mechanism: a pytest fixture that builds a fake tree under tmp_path
with no git, writes the relative cell, and asserts the resolver returns
<root>/<wt>/.agi/sessions. That test satisfies "constructs a relative cell" and
"asserts it resolves", and is VACUOUS for the live case: with no git,
git_common_root returns None, so the code joins the cell onto the graph root
(root/.agi/worktrees/...), the path does not exist, and the resolver silently
falls back to MAIN's shared dir. The kid explicitly named this in
test_relative_cell_without_git_falls_back_not_into_the_worktree and forbade it.

(4) NOT A DEVIATION: no standing rule was bent.

MY PROBES (parent-run, all recorded in frontmatter `probes`):
 - gate -- a RELATIVE cell naming a nonexistent worktree falls back to MAIN's
   _sessions_dir (does not leak a phantom path).
 - auth -- an unknown seat, no row, falls back to MAIN (never invents a tree).
 - wire -- _resolve_brief_file re-roots on the worktree card for a relative
   cell and leaves a non-.agi/sessions control unchanged.
 - wire (non-vacuity) -- I neutralised locations.git_common_root -> None with an
   external pytest plugin and re-ran the kid's two files: 5 of the relative-cell
   tests went RED (13 passed). A test that stays green under that regression
   would pin nothing; these do not.

RESIDUE, named not hidden: rotate.py:7586 _own_card_path NEVER reads the seat
row -- it tries root/sessions/quorum/<seat>.md then root/.agi/sessions/quorum/
<seat>.md then falls back to MAIN. So it cannot honour a worktree cell at all;
it finds a worktree post's card only because the live rotating post's cwd makes
find_project_root return the worktree's OWN graph root. The kid's
test_own_card_path_ignores_the_cell_and_keys_on_root asserts the identical-path
property for both cell spellings AND records that this is inert-cell behaviour,
not cell honouring. That is the honest half of the target claim and it is why I
keep the kid's proved while flagging the claim's `_own_card_path` conjunct as
documented-but-not-honoured.
<!-- THOUGHT:END -->
