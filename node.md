---
id: hypothesis:heal-never-reseats-a-worktree-post-into-main
mint_id: abfba43584714513bb7996784ad54773
type: hypothesis
parents:
  - goal:g1
  - hypothesis:pass9-0926-residue-batch
next_edges: []
edited_by: belam
scaffold_hash: c16ea779b23e5329
season: 2
testable_claim: heal's reseat of a worktree post refuses by name and launches nothing when the post's worktree dir is missing or the launcher rejects the cwd argument -- it never falls back to MAIN's geometry and never retries the launcher without cwd -- and a launch that fails before exec leaves no launch file (with its prompt) in /tmp.
thought_session: belam-S2-L5-X
title: "heal never reseats a worktree post into MAIN (assigned: director-engine)"
town: core
---
# hypothesis:heal-never-reseats-a-worktree-post-into-main

# hypothesis:heal-never-reseats-a-worktree-post-into-main

# heal never reseats a worktree post into MAIN

## Measured (PASS 9 heal-lands-a-reseat-after-a-tmux-server-restart, at TIP 9e16b8ed9)
- _seat_geometry_dir falls back to MAIN silently when the post's worktree dir is missing (verify defect 3 stands).
- heal.py:3199-3204 catches ANY TypeError from the launcher and retries `launcher(root, spawn_name, shell_cmd, window_path)` WITHOUT cwd, so a worktree post recovered through that branch starts in MAIN (verify, missed).
- A failed launch leaves the launch file, and the whole prompt it carries, in /tmp: `rm -f "$0"` runs only if the shell executes the file (verify defect 2 stands).

## Falsifiers
- a fixture reseat with the worktree dir removed launches with MAIN's geometry or cwd; a launcher raising TypeError is called a second time without cwd; a launcher that fails before exec leaves its launch file in /tmp.

## Agent Notes
assigned: director-engine (PASS 9 residue, belam-S2-L5-X 09-26; runs mur-p9chunk11of28)
