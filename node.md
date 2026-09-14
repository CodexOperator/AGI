---
id: hypothesis:l4-the-keep-and-director-rows-carry-their-real-town-cell-and-a-live-cell-change-is-a-measured-rename-at-the-posts-boundary
mint_id: 21792dd66203404caabde2f198754b35
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 0d874b57f6753294
season: 2
testable_claim: "goal:g15.25 SM.32 (OWNER ORDER 01:06Z via belam XX, verbatim doc:l4-owner-decisions L773-775: sanctuary = the original town, overseen by the Sanctuary Master + Master Sensei; core = graph-function code + most config, the Prime presides directly in hybrid survival; local(-maxxing) = the Thought Master + his director. Prime 01:07Z: re-spell the town cells sanctuary-master, master-sensei, sensei-director -> sanctuary; belam, sanctuary-director, sanctuary-helper -> core; measure the branch-name consequence before applying; a round at rotation boundaries, SM.18/SM.25 scope). MEASURED on season2/main @4bd02c74c: posts.md rows belam, sanctuary-master, master-sensei, sanctuary-director, sensei-director, sanctuary-helper + the 7 legacy advisor/director rows all carry town=all; council-* and stream-master/thought-master carry their town; towns.derive_names (towns.py:283) spells <town>/season<N>/posts/<post>/main from the town cell, so a live cell change on a worktree post IS a branch rename (the director branch today: core/season2/posts/sensei-director/main, local-only per SM.25). PRECONDITIONS: SM.29 on MAIN (ladder declares sanctuary) and town:sanctuary minted by the Prime; SM.25 mirror so the rename never touches an origin head. CLAIM: (1) MEASURE FIRST: `rotate.py rename-post --dry-run`-class output (SM.18 apply path) for each of the 6 rows prints old -> new branch name, worktree path, mirror ref, and whether anything on origin is touched (expected: nothing — posts are local-only + refs/agi/posts mirror); the kid records the table in the experiment BEFORE any write; (2) the cell write is one Prime 0a line per row (`set town sanctuary` / `set town core`) the kid ships, applied at each post NEXT rotation boundary by the rotating post itself (rotate reads the new cell, renames the local branch + mirror ref via the SM.18 apply path, records old/new in the rotation record); MAIN-checkout posts (belam, sanctuary-master, master-sensei) have no post branch to rename — cell only; (3) `town=all` is retired from the row vocabulary: the schema (schemas/[config].md self_row) accepts a declared ladder town or `core`, refuses `all` BY NAME at write; (4) readers that filter by town (send.py rooms/audience, seat_status, viewport --theme keep) treat the keep rows as sanctuary and the Prime + point + review as core — a message from the director to `audience quorum` still resolves. FALSIFIERS: an origin head created or moved by the rename; a post seated on a branch whose name disagrees with its town cell; a row still spelling all after every post has rotated once. TESTS (<= 5): dry-run table for a worktree row and a MAIN row; the boundary rename on a fixture repo with a bare origin proves ls-remote unchanged; schema refuses all; audience resolution with the new cells. FILE SCOPE: rotate.py (SM.18 apply path reuse), schemas/[config].md, towns.py only if derive_names needs the keep case, send.py filter, the test files. CEILING: <= 60 production lines, <= 2 kids; RE-BRIEF at 2x. Order: after SM.29 + SM.25 land."
title: L4 the keep and director rows carry their real town cell and a live cell change is a measured rename at the posts boundary
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-keep-and-director-rows-carry-their-real-town-cell-and-a-live-cell-change-is-a-measured-rename-at-the-posts-boundary

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
