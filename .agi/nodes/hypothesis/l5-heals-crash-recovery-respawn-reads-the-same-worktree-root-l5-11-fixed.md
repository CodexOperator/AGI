---
id: hypothesis:l5-heals-crash-recovery-respawn-reads-the-same-worktree-root-l5-11-fixed
mint_id: f53ef178986e42c9949bf18cfc953a55
type: hypothesis
parents:
  - hypothesis:l5-rename-surfaces-and-the-successor-brief-resolve-from-the-rotating-worktree-root
next_edges: []
edited_by: director-belam
scaffold_hash: 1c14096a9efc1725
season: 2
testable_claim: "heal.py:2517 ('card = _rotate._sessions_dir(root) / \"quorum\" / f\"{seat}.md\"') hands a crash-recovered successor its prompt file via _sessions_dir, which routes through git_common_root to MAIN -- so for a worktree-resident seat it reads MAIN's stale quorum card instead of the worktree's own live one, even though heal's own _seat_tree_dir (heal.py:2303) already computes the correct worktree for the launch cwd. This is the same bug class L5.11 fixed for cmd_rotate_self's successor brief (rotate._own_card_path / rotate._own_sessions_dir), just unapplied in heal.py's separate crash-recovery respawn path (mur-l5-11 refuter finding, missed-2). Fix: heal.py's respawn should resolve the card through rotate._own_sessions_dir (or heal's own _seat_tree_dir) instead of _rotate._sessions_dir."
title: L5 heals crash recovery respawn reads the same worktree root l5 11 fixed
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-heals-crash-recovery-respawn-reads-the-same-worktree-root-l5-11-fixed

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
