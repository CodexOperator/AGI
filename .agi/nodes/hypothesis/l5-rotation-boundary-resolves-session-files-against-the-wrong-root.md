---
id: hypothesis:l5-rotation-boundary-resolves-session-files-against-the-wrong-root
mint_id: daa284ac6abe4c5da619ea385acefc54
type: hypothesis
parents:
  - goal:g1.20
next_edges: []
edited_by: belam
scaffold_hash: f9915dc9a95997bb
season: 2
testable_claim: "rotate.py's _apply_staged/_rename_surfaces resolve 'session-file' surfaces (sessions/*.log|*.meter, seats/*, quorum/*, inbox/*) to an absolute path rooted at the MAIN checkout, regardless of which worktree invoked the rotation -- while spawn_window's prompt_file lookup (Path(prompt_file).expanduser().resolve(), rotate.py:1767) resolves relative to the invoking process's CWD (the post's own worktree). On a rotation-with-rename run from a post's own worktree (the only way a director ever rotates), the boundary renames MAIN's copy of quorum/<old>.md to quorum/<new>.md while the invoking worktree's own (possibly more current) copy is never touched -- spawn_window then looks for quorum/<new>.md relative to the worktree, finds nothing, and cmd_rotate_self returns 1 before spawning any successor. Reproduced live 2026-09-17 (sanctuary-director -> director-belam): exit 1, 'ERR: prompt file not found', no successor spawned, confirmed via ListAgents. Fix: session-file surface resolution must use the SAME root the invoking process actually operates under (the worktree), matching how dm-log surfaces already correctly compute a worktree-prefixed path -- or spawn_window's prompt_file lookup must resolve against the same MAIN-rooted base _apply_staged uses. Either fix closes the mismatch; test must exercise it from a SEPARATE worktree (root != cwd), since a same-root tmp_path fixture cannot detect this class of bug -- which is exactly why L5.02's own fixtures, all same-root, never caught it."
thought_session: dissolve-legacy-2026-09-19
title: L5 rotation boundary resolves session files against the wrong root
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-rotation-boundary-resolves-session-files-against-the-wrong-root

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
